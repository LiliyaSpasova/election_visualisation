from typing import List
from models import Party


def calculate_seats(parties: List[Party], total_seats: int = 240, threshold: float = 4.0):
    # 1. Reset all seats to 0 (important for live slider updates)
    for p in parties:
        p.seats = 0

    # 2. Filter parties that meet the 4% threshold
    eligible_parties = [p for p in parties if p.prc_votes >= threshold]
    
    # If no one makes the cut (unlikely!), return early
    if not eligible_parties:
        return parties

    # 3. Calculate the sum of percentages of ONLY the eligible parties
    # This is how "wasted" votes are redistributed in the Bulgarian system
    total_eligible_pct = sum(p.prc_votes for p in eligible_parties)
    
    # 4. First Round: Hare Quota (Integer parts)
    allocated_seats = 0
    remainders = []

    for party in eligible_parties:
        # Calculate precise share: (Party % / Total Eligible %) * 240
        precise_seats = (party.prc_votes / total_eligible_pct) * total_seats
        
        # Assign initial seats (integer part)
        party.seats = int(precise_seats)
        allocated_seats += party.seats
        
        # Store the decimal remainder for the second round
        remainders.append({
            "party": party, 
            "rem_value": precise_seats - int(precise_seats)
        })

    # 5. Second Round: Distribute remaining seats to largest remainders
    seats_left = total_seats - allocated_seats
    
    # Sort by remainder value descending
    remainders.sort(key=lambda x: x["rem_value"], reverse=True)
    
    for i in range(seats_left):
        remainders[i]["party"].seats += 1

    return parties