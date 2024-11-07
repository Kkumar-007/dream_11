import json
import pandas as pd
from collections import defaultdict
import glob

# Define the path where the files are located
file_paths = glob.glob("*.json")  # Modify the path if necessary

# Initialize data structures for team and player statistics
teams_data = defaultdict(lambda: {"matches_played": 0, "wins": 0, "venues": defaultdict(int)})
players_data = defaultdict(lambda: {
    "runs": 0,
    "balls_faced": 0,
    "fours": 0,
    "sixes": 0,
    "wickets": 0,
    "balls_bowled": 0,
    "runs_given": 0  # New field to track runs conceded by the bowler
})

for file_path in file_paths:
    with open(file_path) as file:
        data = json.load(file)
        
        # Debugging output: Verify file path and data structure
        print(f"Processing file: {file_path}")
        print(f"Keys in data: {data.keys()}")

        # Check for 'info' and 'innings' keys
        if 'info' not in data or 'innings' not in data:
            print(f"Skipping file {file_path}: Missing 'info' or 'innings'")
            continue
        
        # Extract match-level information
        match_info = data['info']
        teams = match_info['teams']
        venue = match_info['venue']
        winner = match_info.get('outcome', {}).get('winner', None)
        
        # Update team statistics
        for team in teams:
            teams_data[team]["matches_played"] += 1
            teams_data[team]["venues"][venue] += 1
            if team == winner:
                teams_data[team]["wins"] += 1

        # Process each innings and extract player stats
        for inning in data['innings']:
            team_name = inning['team']
            for over_data in inning['overs']:
                for delivery in over_data['deliveries']:
                    # Extract batting details
                    batter = delivery['batter']
                    runs_scored = delivery['runs']['batter']
                    players_data[batter]['runs'] += runs_scored
                    players_data[batter]['balls_faced'] += 1
                    
                    # Check if it's a boundary
                    if runs_scored == 4:
                        players_data[batter]['fours'] += 1
                    elif runs_scored == 6:
                        players_data[batter]['sixes'] += 1
                    
                    # Extract bowling details
                    bowler = delivery['bowler']
                    players_data[bowler]['balls_bowled'] += 1
                    players_data[bowler]['runs_given'] += delivery['runs']['total']  # Total runs conceded by bowler
                    
                    # Count wickets if present
                    if 'wickets' in delivery:
                        players_data[bowler]['wickets'] += len(delivery['wickets'])

# Debugging output: Display sample data after processing
print("Sample teams_data:", list(teams_data.items())[:3])
print("Sample players_data:", list(players_data.items())[:3])

# Convert data to DataFrames for analysis
team_stats_df = pd.DataFrame.from_dict(teams_data, orient='index')
player_stats_df = pd.DataFrame.from_dict(players_data, orient='index')

# Set 'team' as the first column in team statistics and 'player' as the first column in player statistics
team_stats_df.reset_index(inplace=True)
team_stats_df.rename(columns={'index': 'team'}, inplace=True)

player_stats_df.reset_index(inplace=True)
player_stats_df.rename(columns={'index': 'player'}, inplace=True)

# Calculate additional metrics for players, ensuring that empty values are set if criteria are not met
player_stats_df['strike_rate'] = player_stats_df.apply(
    lambda row: (row['runs'] / row['balls_faced']) * 100 if row['balls_faced'] > 0 else None,
    axis=1
)
player_stats_df['economy_rate'] = player_stats_df.apply(
    lambda row: row['runs_given'] / (row['balls_bowled'] / 6) if row['balls_bowled'] > 0 else None,
    axis=1
)

# Save to CSV
team_stats_df.to_csv("team_statistics.csv", index=False)
player_stats_df.to_csv("player_statistics.csv", index=False)

# Display the DataFrames (Optional)
print("\nTeam Statistics:")
print(team_stats_df)
print("\nPlayer Statistics:")
print(player_stats_df)
