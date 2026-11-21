import copy

from input_validation import venues, days_and_slots
from match_generator import all_matches
from constraints import (
    normalize_constraints,
    slot_conflict_tier
)


# 9. Create Baseline Schedule

def create_baseline_schedule(
    matches, venues, days_and_slots,
    constraints=None, min_rest_hours=48
):

    scheduled_matches = []

    enabled = normalize_constraints(constraints)

    for match in matches:

        # Scan all slots in chronological order and keep the first
        # slot with the best constraint tier. Slots that break the
        # enabled "Minimum rest period" or "Balance number of games"
        # rules are only used when nothing better exists.

        best_tier = None
        best_slot = None

        for date in days_and_slots:
            for time in days_and_slots[date]:
                for venue in venues:

                    tier = slot_conflict_tier(
                        scheduled_matches, match,
                        date, time, venue,
                        enabled, min_rest_hours
                    )

                    # tier is None when the slot breaks an enabled
                    # hard rule (team or venue double-booking)

                    if tier is None:
                        continue

                    if best_tier is None or tier < best_tier:
                        best_tier = tier
                        best_slot = (date, time, venue)

                        # (0, 0) is a perfect slot in the earliest
                        # position, so we can stop scanning early

                        if tier == (0, 0):
                            break

                if best_tier == (0, 0):
                    break

            if best_tier == (0, 0):
                break

        if best_slot is not None:

            date, time, venue = best_slot

            new_match = copy.deepcopy(match)

            new_match["date"] = date
            new_match["time"] = time
            new_match["venue"] = venue

            scheduled_matches.append(new_match)

    return scheduled_matches


# 10. Check Enough Slots

def check_enough_slots(matches, venues, days_and_slots):

    total_slots = (
        sum(len(slots) for slots in days_and_slots.values())
        * len(venues)
    )

    if total_slots < len(matches):

        print(
            f"Warning: {total_slots} slots only, "
            f"but {len(matches)} matches needed."
        )

        return False

    return True


# 11. Run Baseline Algorithm

baseline = create_baseline_schedule(
    copy.deepcopy(all_matches),
    venues,
    days_and_slots
)


# 12. Display Baseline Schedule

print("\n========== Baseline Schedule ==========")

for match in baseline:

    print(
        match["team1"], "vs", match["team2"],
        "|", match["date"],
        "|", match["time"],
        "|", match["venue"]
    )