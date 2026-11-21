import random
import copy

from constraints import (
    normalize_constraints,
    slot_conflict_tier,
    match_respects_rest,
    match_respects_balance
)


# ==================================================
# TASK 3: GENETIC ALGORITHM
# POPULATION INITIALIZATION + SELECTION
# ==================================================


# 1. Create a Random Schedule

def build_available_slots(venues, days_and_slots):
    """All (date, time, venue) combinations the UI allows."""

    available_slots = []

    for date in days_and_slots:
        for time in days_and_slots[date]:
            for venue in venues:
                available_slots.append((date, time, venue))

    return available_slots


def choose_slot(
    schedule, match, candidate_slots,
    constraints=None, min_rest_hours=48
):
    """Pick a random slot among the best conflict-free candidates.

    Random choice keeps diversity for the Genetic Algorithm while
    still preferring slots that respect rest and balance rules.
    Returns (date, time, venue) or None when no slot is usable.
    """

    best_tier = None
    best_slots = []

    for date, time, venue in candidate_slots:

        tier = slot_conflict_tier(
            schedule, match, date, time, venue,
            constraints, min_rest_hours
        )

        if tier is None:
            continue

        if best_tier is None or tier < best_tier:
            best_tier = tier
            best_slots = [(date, time, venue)]

        elif tier == best_tier:
            best_slots.append((date, time, venue))

    if not best_slots:
        return None

    return random.choice(best_slots)


def create_random_schedule(
    all_matches, venues, days_and_slots,
    constraints=None, min_rest_hours=48
):

    schedule = []

    shuffled_matches = copy.deepcopy(all_matches)

    random.shuffle(shuffled_matches)

    # Create available time and venue combinations

    available_slots = build_available_slots(venues, days_and_slots)

    # Schedule matches randomly

    for match in shuffled_matches:

        candidate_slots = available_slots.copy()

        random.shuffle(candidate_slots)

        chosen = choose_slot(
            schedule, match, candidate_slots,
            constraints, min_rest_hours
        )

        if chosen is not None:

            date, time, venue = chosen

            new_match = copy.deepcopy(match)

            new_match["date"] = date
            new_match["time"] = time
            new_match["venue"] = venue

            schedule.append(new_match)

    return schedule


# 2. Initialize Population

def initialize_population(
    population_size,
    all_matches,
    venues,
    days_and_slots,
    constraints=None,
    min_rest_hours=48
):

    population = []

    for i in range(population_size):

        schedule = create_random_schedule(
            all_matches,
            venues,
            days_and_slots,
            constraints,
            min_rest_hours
        )

        population.append(schedule)

    return population


# 4. Tournament Selection

def tournament_selection(
    evaluated_population,
    number_of_parents,
    tournament_size=3
):

    selected_parents = []

    for i in range(number_of_parents):

        tournament = random.sample(
            evaluated_population,
            min(tournament_size, len(evaluated_population))
        )

        winner = max(
            tournament,
            key=lambda individual: individual["fitness"]
        )

        selected_parents.append(
            copy.deepcopy(winner["schedule"])
        )

    return selected_parents

# ==================================================
# CROSSOVER + MUTATION
# ==================================================


# 1. Helper: Match Key (identifies a match regardless of its slot)

def match_key(match):

    return (match["team1"], match["team2"])


# 2. Helper: Check Conflict for a Slot

def has_conflict(
    match, date, time, venue, schedule,
    constraints=None
):

    enabled = normalize_constraints(constraints)

    for scheduled in schedule:

        same_time = (
            scheduled["date"] == date
            and scheduled["time"] == time
        )

        if not same_time:
            continue

        same_team = (
            match["team1"] == scheduled["team1"]
            or match["team1"] == scheduled["team2"]
            or match["team2"] == scheduled["team1"]
            or match["team2"] == scheduled["team2"]
        )

        same_venue = scheduled["venue"] == venue

        # Only enforce the conflict rules that are enabled

        if enabled["team"] and same_team:
            return True

        if enabled["venue"] and same_venue:
            return True

    return False


# 3. Repair Schedule (remove conflicts, place missing matches)

def repair_schedule(
    schedule, all_matches, venues, days_and_slots,
    constraints=None, min_rest_hours=48
):

    repaired = []

    # Keep only matches that do not conflict with already kept ones

    for match in schedule:

        if not has_conflict(
            match,
            match["date"],
            match["time"],
            match["venue"],
            repaired,
            constraints
        ):
            repaired.append(match)

    # Place missing matches in random free slots (prefer slots
    # that respect the enabled rest / balance rules)

    placed_keys = [match_key(m) for m in repaired]

    available_slots = build_available_slots(venues, days_and_slots)

    for match in all_matches:

        if match_key(match) in placed_keys:
            continue

        random.shuffle(available_slots)

        chosen = choose_slot(
            repaired, match, available_slots,
            constraints, min_rest_hours
        )

        if chosen is not None:

            date, time, venue = chosen

            new_match = copy.deepcopy(match)

            new_match["date"] = date
            new_match["time"] = time
            new_match["venue"] = venue

            repaired.append(new_match)

    return repaired


# 4. Crossover (one-point on the match order)

def crossover(
    parent1, parent2, all_matches, venues, days_and_slots,
    constraints=None, min_rest_hours=48
):

    lookup1 = {match_key(m): m for m in parent1}
    lookup2 = {match_key(m): m for m in parent2}

    keys = [match_key(m) for m in all_matches]

    point = random.randint(1, max(1, len(keys) - 1))

    child = []

    for i, key in enumerate(keys):

        source = lookup1 if i < point else lookup2

        if key in source:
            child.append(copy.deepcopy(source[key]))

    return repair_schedule(
        child, all_matches, venues, days_and_slots,
        constraints, min_rest_hours
    )


# 5. Mutation (swap two matches' slots OR move one match)

def mutation(
    schedule, all_matches, venues, days_and_slots,
    mutation_rate=0.2, constraints=None, min_rest_hours=48
):

    mutated = copy.deepcopy(schedule)

    if random.random() > mutation_rate or len(mutated) < 2:
        return mutated

    if random.random() < 0.5:

        # Swap Mutation

        i, j = random.sample(range(len(mutated)), 2)

        for field in ["date", "time", "venue"]:
            mutated[i][field], mutated[j][field] = (
                mutated[j][field], mutated[i][field]
            )

    else:

        # Move Mutation

        i = random.randrange(len(mutated))

        date = random.choice(list(days_and_slots.keys()))
        time = random.choice(days_and_slots[date])
        venue = random.choice(venues)

        mutated[i]["date"] = date
        mutated[i]["time"] = time
        mutated[i]["venue"] = venue

    return repair_schedule(
        mutated, all_matches, venues, days_and_slots,
        constraints, min_rest_hours
    )
