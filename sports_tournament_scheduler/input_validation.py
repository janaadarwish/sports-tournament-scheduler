# ==================================================
# PROJECT 22: SPORTS TOURNAMENT SCHEDULING
# Genetic Algorithm (GA)
# ==================================================

# =========================
# IMPORTS
# =========================

from datetime import datetime, timedelta


# ==================================================
# TASK 1: SCHEDULE REPRESENTATION
# ==================================================


# 1. Input Validation Functions

def get_number(message, minimum):

    while True:
        try:
            number = int(input(message))

            if number >= minimum:
                return number

            print(f"Please enter a number greater than or equal to {minimum}.")

        except ValueError:
            print("Invalid input! Please enter a whole number.")


def get_unique_name(message, existing_names):

    while True:
        name = input(message).strip()

        if name == "":
            print("Name cannot be empty. Try again.")

        elif name.lower() in [n.lower() for n in existing_names]:
            print("This name already exists. Enter a different name.")

        else:
            return name


def is_valid_time(slot):

    parts = slot.split(":")

    if len(parts) != 2:
        return False

    if len(parts[0]) != 2 or len(parts[1]) != 2:
        return False

    if not parts[0].isdigit() or not parts[1].isdigit():
        return False

    hour = int(parts[0])
    minute = int(parts[1])

    return 0 <= hour <= 23 and 0 <= minute <= 59


def is_valid_date(date):

    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True

    except ValueError:
        return False


# 2. Get Teams

number_of_teams = get_number(
        "Enter number of teams (at least 2): ", 2
)

teams = []

for i in range(number_of_teams):

    team_name = get_unique_name(
        f"Enter team {i + 1} name: ",
        teams
    )

    teams.append(team_name)


# 3. Get Venues

number_of_venues = get_number(
    "\nEnter number of venues: ", 1
)

venues = []

for i in range(number_of_venues):

    venue_name = get_unique_name(
        f"Enter venue {i + 1} name: ",
        venues
    )

    venues.append(venue_name)


# 4. Get Tournament Dates and Time Slots

number_of_days = get_number(
    "\nEnter number of tournament days: ", 1
)

days_and_slots = {}

for i in range(number_of_days):

    while True:

        date = input(
            f"\nEnter date {i + 1} (YYYY-MM-DD): "
        ).strip()

        if not is_valid_date(date):
            print("Invalid date! Enter date in YYYY-MM-DD format.")

        elif date in days_and_slots:
            print("This date already exists. Enter another date.")

        else:
            break

    number_of_slots = get_number(
        f"How many available time slots on {date}? ", 1
    )

    time_slots = []

    for j in range(number_of_slots):

        while True:

            slot = input(
                f"Enter time slot {j + 1} for {date} (HH:MM): "
            ).strip()

            if not is_valid_time(slot):
                print("Invalid time! Enter time in HH:MM format.")

            elif slot in time_slots:
                print("This time slot already exists for this date.")

            else:
                time_slots.append(slot)
                break

    days_and_slots[date] = time_slots