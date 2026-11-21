import random
import copy

from fitness import fitness_function
from genetic_operators import repair_schedule


def create_neighbor(
    schedule, all_matches, venues, days_and_slots,
    constraints=None, min_rest_hours=48
):

    # Make a copy of the original schedule
    neighbor = copy.deepcopy(schedule)

    # If there are less than 2 matches, return the schedule
    if len(neighbor) < 2:
        return neighbor

    # Choose a random operation
    if random.random() < 0.5:

        # Swap two matches
        i, j = random.sample(range(len(neighbor)), 2)

        for field in ("date", "time", "venue"):
            neighbor[i][field], neighbor[j][field] = (
                neighbor[j][field], neighbor[i][field]
            )

    else:

        # Move one match
        i = random.randrange(len(neighbor))

        date = random.choice(list(days_and_slots.keys()))
        time = random.choice(days_and_slots[date])
        venue = random.choice(venues)

        neighbor[i]["date"] = date
        neighbor[i]["time"] = time
        neighbor[i]["venue"] = venue

    # Repair the new schedule (respects the enabled constraints)
    neighbor = repair_schedule(
        neighbor,
        all_matches,
        venues,
        days_and_slots,
        constraints,
        min_rest_hours
    )

    return neighbor

def local_search(
    schedule,
    all_matches,
    teams,
    venues,
    days_and_slots,
    max_iterations=100,
    constraints=None,
    min_rest_hours=48
):

    # Start with the original schedule
    current = copy.deepcopy(schedule)

    # Calculate original fitness (only enabled constraints count)
    current_fitness = fitness_function(
        current,
        all_matches,
        teams,
        min_rest_hours,
        constraints
    )

    # Try to improve the schedule
    for _ in range(max_iterations):

        # Create a new neighbor
        candidate = create_neighbor(
            current,
            all_matches,
            venues,
            days_and_slots,
            constraints,
            min_rest_hours
        )

        # Calculate new fitness
        candidate_fitness = fitness_function(
            candidate,
            all_matches,
            teams,
            min_rest_hours,
            constraints
        )

        # Keep the new schedule if it is better
        if candidate_fitness > current_fitness:

            current = candidate
            current_fitness = candidate_fitness

    return current 

def improve_population(
    population,
    all_matches,
    teams,
    venues,
    days_and_slots,
    selection_fraction=0.5,
    max_iterations=100,
    constraints=None,
    min_rest_hours=48
):

    # Copy the population
    improved_population = copy.deepcopy(population)

    if not improved_population:
        return improved_population

    # Sort schedules from best to worst (only enabled constraints count)
    ranked_indices = sorted(
        range(len(improved_population)),
        key=lambda i: fitness_function(
            improved_population[i],
            all_matches,
            teams,
            min_rest_hours,
            constraints
        ),
        reverse=True
    )

    # Calculate how many schedules to improve
    number_to_improve = max(
        1,
        int(len(improved_population) * selection_fraction)
    )

    # Improve the selected schedules
    for index in ranked_indices[:number_to_improve]:

        improved_population[index] = local_search(
            improved_population[index],
            all_matches,
            teams,
            venues,
            days_and_slots,
            max_iterations,
            constraints,
            min_rest_hours
        )

    return improved_population
