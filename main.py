import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from models import all_parties

from calculate_seats import calculate_seats


def generate_parliament_coords(total_seats=240):
    """Calculates x, y coordinates for a semi-circle layout."""
    rows = 6
    seats_per_row = total_seats // rows
    x, y = [], []
    
    for r_idx in range(rows):
        radius = 5 + r_idx  # Increasing radius for each row
        # Distribute dots along the 180-degree arc
        angles = np.linspace(np.pi, 0, seats_per_row)
        for angle in angles:
            x.append(radius * np.cos(angle))
            y.append(radius * np.sin(angle))
    return x, y

# --- UI Setup ---
st.title("🇧🇬 Bulgaria 2026 Coalition Visualizer")

selected_parties = []
current_total_seats = 0
updated_pcts = {}
# --- 1. Update Percentages via Sliders ---
st.sidebar.header("Poll Percentages")

for party in all_parties:
    # Update the Pydantic object's prc_votes attribute directly
    party.prc_votes = st.sidebar.number_input(
        f"{party.name} %",
        0.0, 50.0,
        float(party.prc_votes)
    )

# --- 2. Calculate Seats ---
# This updates the .seats attribute for each party in the list in-place
calculate_seats(all_parties)

# --- 3. Coalition Selection ---
st.sidebar.markdown("---")
st.sidebar.header("Select Coalition")

selected_party_names = []
current_total_seats = 0

for party in all_parties:
    if party.seats > 0:
        # Create a checkbox for each party that made it into parliament
        if st.sidebar.checkbox(f"{party.name} ({party.seats} seats)"):
            selected_party_names.append(party.name)
            current_total_seats += party.seats

# --- 4. Math & Metrics ---
threshold = 121
is_majority = current_total_seats >= threshold

st.metric("Total Seats", f"{current_total_seats} / 240", 
          delta=current_total_seats - threshold, 
          delta_color="normal" if is_majority else "inverse")

if is_majority:
    st.success("✅ Majority Reached! This coalition can form a government.")
else:
    st.error(f"❌ Minority. Need {threshold - current_total_seats} more seats for a majority.")

# --- 5. Visualization Logic ---
fig, ax = plt.subplots(figsize=(10, 5))
x_coords, y_coords = generate_parliament_coords()

# Map colors to dots
dot_colors = []
for party in all_parties:
    # Use the party color if selected, otherwise light grey
    color = party.color if party.name in selected_party_names else "#E0E0E0"
    
    # Add one color entry for every seat the party has
    for _ in range(party.seats):
        if len(dot_colors) < 240:
            dot_colors.append(color)

# Fill any remaining dots (due to rounding or non-allocated seats) with grey
while len(dot_colors) < 240:
    dot_colors.append("#E0E0E0")

ax.scatter(x_coords, y_coords, c=dot_colors, s=100, edgecolors='white', linewidth=0.5)
ax.axis('off')
st.pyplot(fig)
