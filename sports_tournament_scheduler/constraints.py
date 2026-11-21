from datetime import datetime


# ==================================================
# TASK 2: CONSTRAINTS
# ==================================================


# 0. Constraint Toggles
#
# The UI checkboxes (05 / Scheduling Constraints) are mapped to these keys:
#   "rest"    -> Minimum rest period
#   "venue"   -> Avoid venue conflicts
#   "team"    -> Avoid team conflicts
#   "balance" -> Balance number of games
#
# A constraint that is disabled is not penalized in the fitness function
# and is not enforced while building / repairing schedules.

DEFAULT_CONSTRAINTS = {
    "rest": True,
    "venue": True,
    "team": True,
    "balance": True
}


def normalize_constraints(constraints):
    """Merge user toggles with the defaults (missing keys = enabled)."""

    enabled = dict(DEFAULT_CONSTRAINTS)

    if not constraints:
        return enabled

    for key, value in constraints.items():

        if key in enabled and value is not None:
            enabled[key] = bool(value)

    return enabled


def to_match_datetime(date, time):
    """Convert 'YYYY-MM-DD' + 'HH:MM' to a datetime (None if invalid)."""

    try:
        return datetime.strptime(
            f"{date} {time}",
            "%Y-%m-%d %H:%M"
        )
    except (ValueError, TypeError):
        return None


def match_respects_rest(
    schedule, match, date, time, min_rest_hours=48
):
    """Check if placing 'match' at (date, time) keeps enough rest
    for both of its teams, given the already scheduled matches."""

    candidate = to_match_datetime(date, time)

    if candidate is None:
        return True

    min_rest_minutes = min_rest_hours * 60

    for scheduled in schedule:

        shares_team = (
            match["team1"] == scheduled["team1"]
            or match["team1"] == scheduled["team2"]
            or match["team2"] == scheduled["team1"]
            or match["team2"] == scheduled["team2"]
        )

        if not shares_team:
            continue

        other = to_match_datetime(
            scheduled["date"], scheduled["time"]
        )

        if other is None:
            continue

        gap_minutes = abs(
            (candidate - other).total_seconds() / 60
        )

        if gap_minutes < min_rest_minutes:
            return False

    return True


def match_respects_balance(schedule, match, date):
    """Check if placing 'match' on 'date' gives either team more
    than one match on the same day, given scheduled matches."""

    for scheduled in schedule:

        same_date = scheduled["date"] == date

        shares_team = (
            match["team1"] == scheduled["team1"]
            or match["team1"] == scheduled["team2"]
            or match["team2"] == scheduled["team1"]
            or match["team2"] == scheduled["team2"]
        )

        if same_date and shares_team:
            return False

    return True


def slot_conflict_tier(
    schedule, match, date, time, venue,
    constraints=None, min_rest_hours=48
):
    """Grade one candidate slot for one match.

    Returns a small tuple describing how bad the slot is:
      (0, 0) = respects every enabled constraint
      (1, 0) = breaks the minimum rest period
      (0, 1) = breaks the game balance rule
      (1, 1) = breaks both soft rules
    Returns None when the slot breaks an ENABLED hard rule
    (a team or a venue double-booked at the same time), because
    such a slot must never be used.

    Lower tuples are better, so callers can simply compare tiers.
    """

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

        # "Avoid team conflicts" is only enforced when enabled

        if enabled["team"] and same_team:
            return None

        # "Avoid venue conflicts" is only enforced when enabled

        if enabled["venue"] and same_venue:
            return None

    rest_bad = 0
    balance_bad = 0

    # "Minimum rest period" is a soft rule: prefer slots that
    # respect it, but still use them as a fallback.

    if enabled["rest"] and not match_respects_rest(
        schedule, match, date, time, min_rest_hours
    ):
        rest_bad = 1

    # "Balance number of games": prefer not to play twice a day

    if enabled["balance"] and not match_respects_balance(
        schedule, match, date
    ):
        balance_bad = 1

    return (rest_bad, balance_bad)


# 1. Count Team Conflicts

def count_team_conflicts(schedule):

    conflicts = 0

    for i in range(len(schedule)):

        for j in range(i + 1, len(schedule)):

            match1 = schedule[i]
            match2 = schedule[j]

            same_time = (
                match1["date"] == match2["date"]
                and match1["time"] == match2["time"]
            )

            same_team = (
                match1["team1"] == match2["team1"]
                or match1["team1"] == match2["team2"]
                or match1["team2"] == match2["team1"]
                or match1["team2"] == match2["team2"]
            )

            if same_time and same_team:
                conflicts += 1

    return conflicts


# 2. Count Venue Conflicts

def count_venue_conflicts(schedule):

    conflicts = 0

    for i in range(len(schedule)):

        for j in range(i + 1, len(schedule)):

            match1 = schedule[i]
            match2 = schedule[j]

            same_time = (
                match1["date"] == match2["date"]
                and match1["time"] == match2["time"]
            )

            same_venue = (
                match1["venue"] == match2["venue"]
            )

            if same_time and same_venue:
                conflicts += 1

    return conflicts


# 3. Evaluate Rest Periods

def evaluate_rest_periods(
    scheduled_matches, min_rest_hours=48
):

    team_matches = {}
    rest_violations = 0
    violation_details = []

    for match in scheduled_matches:

        team1 = match["team1"]
        team2 = match["team2"]

        date = match["date"]
        time = match["time"]

        if not date or not time:
            continue

        match_datetime = datetime.strptime(
            f"{date} {time}",
            "%Y-%m-%d %H:%M"
        )

        for team in [team1, team2]:

            if team not in team_matches:
                team_matches[team] = []

            team_matches[team].append(match_datetime)

    for team, matches_list in team_matches.items():

        matches_list.sort()

        for i in range(len(matches_list) - 1):

            match1 = matches_list[i]
            match2 = matches_list[i + 1]

            rest_period = match2 - match1

            rest_hours = rest_period.total_seconds() / 3600

            if rest_hours < min_rest_hours:

                rest_violations += 1

                violation_details.append(
                    f"Rest Period Violation: Team '{team}' "
                    f"has only {rest_hours:.1f} hours of rest "
                    f"between {match1} and {match2}"
                )

    return rest_violations, violation_details


# 4. Evaluate Game Balance

def evaluate_game_balance(scheduled_matches, teams):

    team_match_counts = {team: 0 for team in teams}
    team_daily_counts = {team: {} for team in teams}

    balance_violations = 0
    violation_details = []

    if not scheduled_matches:
        return 0, []

    for match in scheduled_matches:

        team1 = match["team1"]
        team2 = match["team2"]
        date = match["date"]

        for team in [team1, team2]:

            if team in team_match_counts:

                team_match_counts[team] += 1

                if date not in team_daily_counts[team]:
                    team_daily_counts[team][date] = 0

                team_daily_counts[team][date] += 1

    # Check total match count balance

    counts = list(team_match_counts.values())

    max_matches = max(counts)
    min_matches = min(counts)

    if (max_matches - min_matches) > 1:

        for team, count in team_match_counts.items():

            if count == max_matches or count == min_matches:

                balance_violations += 1

                violation_details.append(
                    f"Match Count Balance Violation: "
                    f"Team '{team}' has {count} matches. "
                    f"Difference between max ({max_matches}) "
                    f"and min ({min_matches}) is too large."
                )

    # Check match distribution across tournament days

    for team, daily_counts in team_daily_counts.items():

        if daily_counts:

            max_daily_matches = max(daily_counts.values())

            if max_daily_matches > 1:

                balance_violations += 1

                violation_details.append(
                    f"Match Distribution Violation: "
                    f"Team '{team}' plays {max_daily_matches} "
                    f"matches on the same date."
                )

    return balance_violations, violation_details


# 5. Count Unscheduled Matches

def count_unscheduled_matches(all_matches, schedule):

    unscheduled_matches = len(all_matches) - len(schedule)

    return unscheduled_matches