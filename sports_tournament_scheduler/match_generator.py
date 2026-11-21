import copy

from input_validation import teams, venues, days_and_slots


# 5. Create a Match

def create_match(team1, team2):

    return {
        "team1": team1,
        "team2": team2,
        "date": None,
        "time": None,
        "venue": None
    }


# 6. Generate All Matches (Round Robin)

def generate_matches(teams):

    matches = []

    for i in range(len(teams)):

        for j in range(i + 1, len(teams)):

            match = create_match(teams[i], teams[j])
            matches.append(match)

    return matches


# 7. Generate Matches

matches = generate_matches(teams)

# Keep original matches unchanged
all_matches = copy.deepcopy(matches)


# 8. Display Tournament Information

print("\n========== Tournament Information ==========")

print("\nTeams:")
for team in teams:
    print("-", team)

print("\nVenues:")
for venue in venues:
    print("-", venue)

print("\nAvailable Dates and Time Slots:")

for date in days_and_slots:
    print(date, ":", days_and_slots[date])

print("\nTotal Number of Matches:", len(matches))

print("\n========== Generated Matches ==========")

for i, match in enumerate(matches):

    print(
        f"Match {i + 1}: "
        f"{match['team1']} vs {match['team2']}"
    )