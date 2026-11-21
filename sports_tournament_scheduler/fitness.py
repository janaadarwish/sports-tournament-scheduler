from input_validation import teams
from match_generator import all_matches
from scheduler import baseline
from constraints import (
    normalize_constraints,
    count_team_conflicts,
    count_venue_conflicts,
    count_unscheduled_matches,
    evaluate_rest_periods,
    evaluate_game_balance
)


# ==================================================
# FITNESS FUNCTION
# ==================================================

def fitness_function(
    schedule, all_matches, teams,
    min_rest_hours=48, constraints=None
):

    # Which constraints are enabled (UI checkboxes 05 / Scheduling
    # Constraints). A disabled constraint is not penalized.

    enabled = normalize_constraints(constraints)

    # Weights

    hard_weight = 10000
    rest_weight = 10
    balance_weight = 5

    # Hard Constraints

    hard_violations = 0

    if enabled["team"]:
        hard_violations += count_team_conflicts(schedule)

    if enabled["venue"]:
        hard_violations += count_venue_conflicts(schedule)

    # Scheduling every match is always required, so unscheduled
    # matches stay penalized even if other constraints are off.

    unscheduled_matches = count_unscheduled_matches(
        all_matches,
        schedule
    )

    hard_violations += unscheduled_matches

    # Soft Constraints

    soft_penalty = 0

    if enabled["rest"]:
        rest_violations, rest_details = evaluate_rest_periods(
            schedule,
            min_rest_hours
        )
        soft_penalty += rest_weight * rest_violations

    if enabled["balance"]:
        balance_violations, balance_details = evaluate_game_balance(
            schedule,
            teams
        )
        soft_penalty += balance_weight * balance_violations

    # Total Penalty

    total_penalty = (
        hard_weight * hard_violations
        + soft_penalty
    )

    # Fitness Score

    fitness = 1 / (1 + total_penalty)

    return fitness


# 3. Evaluate Population

def evaluate_population(
    population, all_matches, teams,
    min_rest_hours=48, constraints=None
):

    evaluated_population = []

    for schedule in population:

        fitness = fitness_function(
            schedule,
            all_matches,
            teams,
            min_rest_hours,
            constraints
        )

        individual = {
            "schedule": schedule,
            "fitness": fitness
        }

        evaluated_population.append(individual)

    return evaluated_population


# ==================================================
# EVALUATE BASELINE FITNESS
# ==================================================

print("\n========== Fitness Evaluation ==========")

team_conflicts = count_team_conflicts(baseline)

venue_conflicts = count_venue_conflicts(baseline)

unscheduled_matches = count_unscheduled_matches(
    all_matches,
    baseline
)

rest_violations, rest_details = evaluate_rest_periods(
    baseline,
    min_rest_hours=48
)

balance_violations, balance_details = evaluate_game_balance(
    baseline,
    teams
)

baseline_fitness = fitness_function(
    baseline,
    all_matches,
    teams
)

print("\nHard Constraints:")
print("Team Conflicts:", team_conflicts)
print("Venue Conflicts:", venue_conflicts)
print("Unscheduled Matches:", unscheduled_matches)

print("\nSoft Constraints:")
print("Rest Period Violations:", rest_violations)
print("Game Balance Violations:", balance_violations)

print("\nRest Violation Details:")
for detail in rest_details:
    print("-", detail)

print("\nBalance Violation Details:")
for detail in balance_details:
    print("-", detail)

print("\nBaseline Fitness Score:", baseline_fitness)