import pandas as pd

# Load the player statistics CSV file
df = pd.read_csv("player_statistics.csv")

# Define batting points calculation
def calculate_batting_points(row):
    points = 0
    points += row['runs']  # +1 per run
    points += row['fours'] * 1  # +1 per boundary
    points += row['sixes'] * 2  # +2 per six
    
    # Half-century and century bonuses
    if row['runs'] >= 100:
        points += 8  # Century bonus only
    elif row['runs'] >= 50:
        points += 4  # Half-century bonus only

    # Dismissal for a duck
    if row['runs'] == 0 and row['balls_faced'] > 0:
        points -= 3  # Duck penalty

    # Strike rate bonus/penalty (only if player faced balls)
    if row['balls_faced'] >= 20:
        strike_rate = row['strike_rate']
        if strike_rate > 140:
            points += 6
        elif 120.01 <= strike_rate <= 140:
            points += 4
        elif 100 <= strike_rate <= 120:
            points += 2
        elif 40 <= strike_rate < 50:
            points -= 2
        elif 30 <= strike_rate < 40:
            points -= 4
        elif strike_rate < 30:
            points -= 6

    return points

# Define bowling points calculation
def calculate_bowling_points(row):
    points = 0
    points += row['wickets'] * 25  # +25 per wicket
    points += row.get('bowled_or_lbw', 0) * 8  # +8 for LBW or Bowled dismissals

    # Wicket bonuses
    if row['wickets'] >= 5:
        points += 8  # 5-wicket bonus
    elif row['wickets'] >= 4:
        points += 4  # 4-wicket bonus

    # Economy rate points (only if player bowled balls)
    if row['balls_bowled'] >= 30:
        economy_rate = row['economy_rate']
        if economy_rate < 2.5:
            points += 6
        elif 2.5 <= economy_rate <= 3.49:
            points += 4
        elif 3.5 <= economy_rate <= 4.5:
            points += 2
        elif 7 <= economy_rate <= 8:
            points -= 2
        elif 8.01 <= economy_rate <= 9:
            points -= 4
        elif economy_rate > 9:
            points -= 6

    return points

# Calculate batting and bowling points for each player
df['batting_points'] = df.apply(calculate_batting_points, axis=1)
df['bowling_points'] = df.apply(calculate_bowling_points, axis=1)

# Calculate total points
df['total_points'] = df['batting_points'] + df['bowling_points']

# Display the DataFrame with points
print(df[['player', 'batting_points', 'bowling_points', 'total_points']])

# Optionally save to CSV
df.to_csv("player_points_summary.csv", index=False)
