from input_validation import teams, venues, days_and_slots
from match_generator import all_matches
from scheduler import check_enough_slots
from fitness import fitness_function, evaluate_population, baseline_fitness
from genetic_operators import (
    initialize_population,
    tournament_selection,
    crossover,
    mutation
)
from memetic_algorithm import improve_population


# ==================================================
# RUN TASK 3: POPULATION + SELECTION
# ==================================================

# Check available slots

if not check_enough_slots(all_matches, venues, days_and_slots):

    print("\nNot enough slots to schedule all matches.")

else:

    population_size = 10
    number_of_parents = 10

    # Initialize Population

    population = initialize_population(
        population_size,
        all_matches,
        venues,
        days_and_slots
    )

    print("\n========== Initial Population ==========")

    print("Population Size:", len(population))

    # Evaluate Population

    evaluated_population = evaluate_population(
        population,
        all_matches,
        teams
    )

    # Display Fitness

    print("\n========== Population Fitness ==========")

    for i, individual in enumerate(evaluated_population):

        print(
            f"Schedule {i + 1}: "
            f"Fitness = {individual['fitness']:.6f}"
        )

    # Select Parents

    selected_parents = tournament_selection(
        evaluated_population,
        number_of_parents,
        tournament_size=3
    )

    # Display Selection Results

    print("\n========== Selection Results ==========")

    print("Number of Selected Parents:", len(selected_parents))

    for i, parent in enumerate(selected_parents):

        fitness = fitness_function(
            parent,
            all_matches,
            teams
        )

        print(
            f"Parent {i + 1}: "
            f"Fitness = {fitness:.6f}"
        )

            # Crossover + Mutation

    offspring = []

    for i in range(0, len(selected_parents) - 1, 2):

        child1 = crossover(
            selected_parents[i], selected_parents[i + 1],
            all_matches, venues, days_and_slots
        )

        child2 = crossover(
            selected_parents[i + 1], selected_parents[i],
            all_matches, venues, days_and_slots
        )

        offspring.append(
            mutation(child1, all_matches, venues, days_and_slots)
        )

        offspring.append(
            mutation(child2, all_matches, venues, days_and_slots)
        )

    print("\n========== Offspring Fitness ==========")

    for i, child in enumerate(offspring):

        print(
            f"Child {i + 1}: "
            f"Fitness = {fitness_function(child, all_matches, teams):.6f}"

        )

    # Apply Memetic Algorithm (inside the else branch so it only
    # runs when there were enough slots to build a population)

    memetic_population = improve_population(
        offspring,
        all_matches,
        teams,
        venues,
        days_and_slots,
        selection_fraction=0.5,
        max_iterations=100
    )

    # Display MA Results

    print("\n========== Memetic Algorithm Results ==========")

    for i, schedule in enumerate(memetic_population):

        print(
            f"Schedule {i + 1}: "
            f"Fitness = {fitness_function(schedule, all_matches, teams):.6f}"
        )