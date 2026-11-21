"""Streamlit integration layer for the existing tournament scheduling modules.

The original team files are kept unchanged. This adapter supplies the UI inputs
through a temporary input_validation module, then reuses the team's functions.
"""
from __future__ import annotations

import contextlib
import copy
import importlib
import io
import random
import sys
import time
import types
from typing import Any
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
TEAM_CODE_DIR = PROJECT_DIR / "sports_tournament_scheduler"

if TEAM_CODE_DIR.exists():
    sys.path.insert(0, str(TEAM_CODE_DIR))

# constraints.py has no module-level side effects or dependencies, so it is
# safe to import its helpers directly for normalizing the UI constraint toggles.
from constraints import normalize_constraints


def _load_project_modules(teams, venues, days_and_slots):
    """Load existing modules with UI-provided inputs, without terminal prompts."""
    # These modules have module-level execution. Reload them for every run so
    # their globals reflect the current Streamlit configuration.
    module_names = [
        "genetic_algorithm", "memetic_algorithm", "fitness",
        "scheduler", "match_generator", "genetic_operators",
        "constraints", "input_validation",
    ]
    for name in module_names:
        sys.modules.pop(name, None)

    inputs = types.ModuleType("input_validation")
    inputs.teams = list(teams)
    inputs.venues = list(venues)
    inputs.days_and_slots = copy.deepcopy(days_and_slots)
    sys.modules["input_validation"] = inputs

    # Existing modules print diagnostic output at import time. Keep it out of
    # the Streamlit page while still allowing their functions to be imported.
    with contextlib.redirect_stdout(io.StringIO()):
        match_generator = importlib.import_module("match_generator")
        scheduler = importlib.import_module("scheduler")
        constraints = importlib.import_module("constraints")
        fitness = importlib.import_module("fitness")
        operators = importlib.import_module("genetic_operators")
        memetic = importlib.import_module("memetic_algorithm")

    return match_generator, scheduler, constraints, fitness, operators, memetic


# Which algorithms run for each "Optimization Method" choice in
# 04 / Algorithm Parameters:
#   "Genetic Algorithm"  -> evolution only (selection + crossover + mutation)
#   "Memetic Algorithm"  -> evolution + local search on the evolved population
#   "Both"               -> one evolution phase, GA keeps the raw best,
#                           Memetic improves the evolved population with
#                           local search, so the comparison is a fair A/B test
# The Baseline is always produced as the reference schedule.
ALGORITHM_MODES = {
    "Genetic Algorithm": ("ga",),
    "Memetic Algorithm": ("memetic",),
    "Both": ("ga", "memetic"),
}


def _evolve_population(
    population, all_matches, teams, venues, days_and_slots,
    population_size, generations, mutation_rate,
    fitness_module, operators, constraint_toggles, min_rest_hours
):
    """Run the generational evolution loop shared by both algorithms.

    Each generation: evaluate -> track the best individual -> tournament
    selection -> crossover -> mutation -> elitism. Returns the best
    individual ever seen and the final population (the Memetic Algorithm
    improves that population with local search).
    """
    best_individual = None

    for _ in range(generations):
        evaluated = fitness_module.evaluate_population(
            population, all_matches, teams,
            min_rest_hours=min_rest_hours, constraints=constraint_toggles
        )
        generation_best = max(evaluated, key=lambda item: item["fitness"])
        if best_individual is None or generation_best["fitness"] > best_individual["fitness"]:
            best_individual = copy.deepcopy(generation_best)

        parents = operators.tournament_selection(
            evaluated, population_size, tournament_size=3
        )
        offspring = []
        for index in range(0, len(parents) - 1, 2):
            child1 = operators.crossover(
                parents[index], parents[index + 1], all_matches, venues, days_and_slots,
                constraints=constraint_toggles, min_rest_hours=min_rest_hours
            )
            child2 = operators.crossover(
                parents[index + 1], parents[index], all_matches, venues, days_and_slots,
                constraints=constraint_toggles, min_rest_hours=min_rest_hours
            )
            offspring.append(operators.mutation(
                child1, all_matches, venues, days_and_slots, mutation_rate,
                constraints=constraint_toggles, min_rest_hours=min_rest_hours
            ))
            offspring.append(operators.mutation(
                child2, all_matches, venues, days_and_slots, mutation_rate,
                constraints=constraint_toggles, min_rest_hours=min_rest_hours
            ))
        if len(parents) % 2:
            offspring.append(copy.deepcopy(parents[-1]))
        if best_individual is not None:
            offspring[0] = copy.deepcopy(best_individual["schedule"])
        population = offspring

    final_evaluated = fitness_module.evaluate_population(
        population, all_matches, teams,
        min_rest_hours=min_rest_hours, constraints=constraint_toggles
    )
    final_best = max(final_evaluated, key=lambda item: item["fitness"])
    if best_individual is None or final_best["fitness"] > best_individual["fitness"]:
        best_individual = copy.deepcopy(final_best)

    return best_individual, population


def _evaluate_metrics(
    schedule, all_matches, teams,
    constraints, fitness_module,
    constraint_toggles=None, min_rest_hours=48
):
    # Violation counts are always measured for every constraint so the
    # Analytics page can show the full picture, even when a constraint
    # is switched off in the UI.
    team_conflicts = constraints.count_team_conflicts(schedule)
    venue_conflicts = constraints.count_venue_conflicts(schedule)
    unscheduled = constraints.count_unscheduled_matches(all_matches, schedule)
    rest_violations, rest_details = constraints.evaluate_rest_periods(
        schedule, min_rest_hours=min_rest_hours
    )
    balance_violations, balance_details = constraints.evaluate_game_balance(
        schedule, teams
    )
    # The fitness score only penalizes the constraints enabled in the UI.
    fitness_value = fitness_module.fitness_function(
        schedule, all_matches, teams,
        min_rest_hours=min_rest_hours,
        constraints=constraint_toggles
    )
    return {
        "fitness": fitness_value,
        "team_conflicts": team_conflicts,
        "venue_conflicts": venue_conflicts,
        "conflicts": team_conflicts + venue_conflicts,
        "unscheduled_matches": unscheduled,
        "rest_violations": rest_violations,
        "balance_violations": balance_violations,
        "rest_details": rest_details,
        "balance_details": balance_details,
    }


def run_tournament(
    teams,
    venues,
    days_and_slots,
    population_size=50,
    generations=100,
    mutation_rate=0.2,
    random_seed=None,
    constraints=None,
    min_rest_hours=48,
    algorithm="Both",
):
    """Run the Baseline plus the algorithm(s) chosen in the UI.

    Returns a dictionary containing each schedule and its measured metrics.
    Input format:
      teams: list[str]
      venues: list[str]
      days_and_slots: {"YYYY-MM-DD": ["HH:MM", ...]}
      constraints: optional toggles from the UI (05 / Scheduling Constraints)
        {"rest": bool, "venue": bool, "team": bool, "balance": bool}
      min_rest_hours: minimum rest period used when "rest" is enabled
      algorithm: "Genetic Algorithm", "Memetic Algorithm" or "Both"
        (04 / Algorithm Parameters). Only the selected algorithm(s) run
        and appear in the returned "results"; the Baseline is always
        included as the reference schedule.
    """
    mode = ALGORITHM_MODES.get(algorithm)

    if mode is None:
        raise ValueError(
            "Unknown algorithm. Choose 'Genetic Algorithm', "
            "'Memetic Algorithm' or 'Both'."
        )
    teams = list(teams)
    venues = list(venues)
    days_and_slots = copy.deepcopy(days_and_slots)

    # Normalize the UI toggles once, then use them everywhere
    # (fitness, schedule building, repair and local search).
    constraint_toggles = normalize_constraints(constraints)

    if len(teams) < 2:
        raise ValueError("At least two teams are required.")
    if not venues:
        raise ValueError("At least one venue is required.")
    if not days_and_slots or any(not slots for slots in days_and_slots.values()):
        raise ValueError("Add at least one available time slot for every tournament day.")
    if population_size < 2:
        raise ValueError("Population size must be at least 2.")
    if generations < 1:
        raise ValueError("Number of generations must be at least 1.")
    if min_rest_hours < 0:
        raise ValueError("Minimum rest period cannot be negative.")

    if random_seed is not None:
        random.seed(random_seed)

    match_generator, scheduler, constraints, fitness_module, operators, memetic = (
        _load_project_modules(teams, venues, days_and_slots)
    )
    all_matches = copy.deepcopy(match_generator.all_matches)

    if not scheduler.check_enough_slots(all_matches, venues, days_and_slots):
        total_slots = sum(len(slots) for slots in days_and_slots.values()) * len(venues)
        raise ValueError(
            f"Not enough available slots: {total_slots} slots for {len(all_matches)} matches."
        )

    # Baseline (respects the enabled constraints while placing matches)
    started = time.perf_counter()
    baseline_schedule = scheduler.create_baseline_schedule(
        copy.deepcopy(all_matches), venues, days_and_slots,
        constraints=constraint_toggles, min_rest_hours=min_rest_hours
    )
    baseline_time = time.perf_counter() - started
    baseline_metrics = _evaluate_metrics(
        baseline_schedule, all_matches, teams, constraints, fitness_module,
        constraint_toggles, min_rest_hours
    )

    # Genetic Algorithm: reuse the team's initialization, selection,
    # crossover, mutation, repair, and fitness functions. All of them
    # respect the constraint toggles from the UI.
    started = time.perf_counter()
    population = operators.initialize_population(
        population_size, all_matches, venues, days_and_slots,
        constraints=constraint_toggles, min_rest_hours=min_rest_hours
    )
    if not population:
        raise RuntimeError("The optimization algorithms could not create an initial population.")

    results = {
        "Baseline": {
            "schedule": baseline_schedule,
            "execution_time": baseline_time,
            **baseline_metrics,
        }
    }

    # One shared evolution phase (selection + crossover + mutation +
    # elitism). The Genetic Algorithm reports the raw best individual;
    # the Memetic Algorithm additionally improves the evolved population
    # with the team's local search.
    best_individual, evolved_population = _evolve_population(
        population, all_matches, teams, venues, days_and_slots,
        population_size, generations, mutation_rate,
        fitness_module, operators, constraint_toggles, min_rest_hours
    )
    evolution_time = time.perf_counter() - started

    if "ga" in mode:
        ga_schedule = copy.deepcopy(best_individual["schedule"])
        ga_metrics = _evaluate_metrics(
            ga_schedule, all_matches, teams, constraints, fitness_module,
            constraint_toggles, min_rest_hours
        )
        results["Genetic Algorithm"] = {
            "schedule": ga_schedule,
            "execution_time": evolution_time,
            **ga_metrics,
        }

    if "memetic" in mode:
        # Memetic Algorithm = evolutionary search + local search on the
        # best part of the evolved population.
        started = time.perf_counter()
        memetic_population = memetic.improve_population(
            evolved_population,
            all_matches,
            teams,
            venues,
            days_and_slots,
            selection_fraction=0.5,
            max_iterations=100,
            constraints=constraint_toggles,
            min_rest_hours=min_rest_hours,
        )
        memetic_evaluated = fitness_module.evaluate_population(
            memetic_population, all_matches, teams,
            min_rest_hours=min_rest_hours, constraints=constraint_toggles
        )
        memetic_best = max(memetic_evaluated, key=lambda item: item["fitness"])

        # Local search only accepts improvements, but keep the evolution
        # best as a safety net so the Memetic result can never be worse.
        if best_individual["fitness"] > memetic_best["fitness"]:
            memetic_best = copy.deepcopy(best_individual)

        memetic_schedule = copy.deepcopy(memetic_best["schedule"])
        memetic_time = evolution_time + (time.perf_counter() - started)
        memetic_metrics = _evaluate_metrics(
            memetic_schedule, all_matches, teams, constraints, fitness_module,
            constraint_toggles, min_rest_hours
        )
        results["Memetic Algorithm"] = {
            "schedule": memetic_schedule,
            "execution_time": memetic_time,
            **memetic_metrics,
        }

    return {
        "all_matches": all_matches,
        "algorithm": algorithm,
        "constraints_applied": constraint_toggles,
        "min_rest_hours": min_rest_hours,
        "results": results,
    }
