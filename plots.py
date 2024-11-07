import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV files
team_stats_df = pd.read_csv("team_statistics.csv")
player_stats_df = pd.read_csv("player_statistics.csv")

# Set up Seaborn style for plots
sns.set(style="whitegrid")

# Create plots for team statistics
def plot_team_statistics():
    # Plot total matches played by each team
    plt.figure(figsize=(10, 6))
    sns.barplot(data=team_stats_df, x='team', y='matches_played', color='skyblue')
    plt.title("Total Matches Played by Each Team")
    plt.xlabel("Team")
    plt.ylabel("Matches Played")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("matches_played_by_team.png")
    plt.show()

    # Plot win percentage by team
    team_stats_df['win_percentage'] = (team_stats_df['wins'] / team_stats_df['matches_played']) * 100
    plt.figure(figsize=(10, 6))
    sns.barplot(data=team_stats_df, x='team', y='win_percentage', color='salmon')
    plt.title("Win Percentage by Team")
    plt.xlabel("Team")
    plt.ylabel("Win Percentage")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("win_percentage_by_team.png")
    plt.show()

# Create plots for player statistics with filtering conditions
def plot_player_statistics():
    # Top 10 scorers
    top_scorers = player_stats_df.nlargest(10, 'runs')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_scorers['player'], y=top_scorers['runs'], color='lightgreen')
    plt.title("Top 10 Scorers")
    plt.xlabel("Player")
    plt.ylabel("Total Runs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_scorers.png")
    plt.show()

    # Top 10 players by strike rate (minimum 30 balls faced)
    top_strike_rate = player_stats_df[player_stats_df['balls_faced'] >= 30].nlargest(10, 'strike_rate')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_strike_rate['player'], y=top_strike_rate['strike_rate'], color='orange')
    plt.title("Top 10 Players by Strike Rate (Min 30 Balls Faced)")
    plt.xlabel("Player")
    plt.ylabel("Strike Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_strike_rate.png")
    plt.show()

    # Top 10 bowlers by economy rate (minimum 30 balls bowled)
    top_economy_rate = player_stats_df[player_stats_df['balls_bowled'] >= 30].nsmallest(10, 'economy_rate')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_economy_rate['player'], y=top_economy_rate['economy_rate'], color='purple')
    plt.title("Top 10 Bowlers by Economy Rate (Min 30 Balls Bowled)")
    plt.xlabel("Player")
    plt.ylabel("Economy Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_economy_rate.png")
    plt.show()

# Generate Excel with best performers in batting, bowling, and fielding
def generate_best_performers_excel():
    with pd.ExcelWriter("best_performers.xlsx", engine="xlsxwriter") as writer:
        # Best Batting Performers
        batting_df = player_stats_df[['player', 'runs', 'strike_rate', 'balls_faced']]
        batting_df['batting_average'] = batting_df['runs'] / batting_df['balls_faced']
        top_batting_runs = batting_df.nlargest(5, 'runs')
        top_batting_strike_rate = batting_df[batting_df['balls_faced'] >= 30].nlargest(5, 'strike_rate')
        top_batting_average = batting_df.nlargest(5, 'batting_average')

        # Combine into one sheet
        batting_summary = pd.concat([top_batting_runs, top_batting_strike_rate, top_batting_average])
        batting_summary.drop_duplicates(inplace=True)
        batting_summary.to_excel(writer, sheet_name="Best Batting Performances", index=False)

        # Best Bowling Performers
        bowling_df = player_stats_df[['player', 'wickets', 'balls_bowled', 'economy_rate']]
        bowling_df['bowling_average'] = player_stats_df['runs'] / player_stats_df['wickets']
        top_bowling_wickets = bowling_df.nlargest(5, 'wickets')
        top_bowling_economy = bowling_df[bowling_df['balls_bowled'] >= 30].nsmallest(5, 'economy_rate')
        top_bowling_average = bowling_df.nlargest(5, 'bowling_average')

        # Combine into one sheet
        bowling_summary = pd.concat([top_bowling_wickets, top_bowling_economy, top_bowling_average])
        bowling_summary.drop_duplicates(inplace=True)
        bowling_summary.to_excel(writer, sheet_name="Best Bowling Performances", index=False)

        # Best Fielding Performers (assuming 'catches', 'stumpings', and 'run_outs' columns are in `player_stats_df`)
        fielding_df = player_stats_df[['player', 'catches', 'stumpings', 'run_outs']].fillna(0)
        top_fielding_catches = fielding_df.nlargest(5, 'catches')
        top_fielding_stumpings = fielding_df.nlargest(5, 'stumpings')
        top_fielding_run_outs = fielding_df.nlargest(5, 'run_outs')

        # Combine into one sheet
        fielding_summary = pd.concat([top_fielding_catches, top_fielding_stumpings, top_fielding_run_outs])
        fielding_summary.drop_duplicates(inplace=True)
        fielding_summary.to_excel(writer, sheet_name="Best Fielding Performances", index=False)

def generate_best_performers_csv():
    # Best Batting Performers
    batting_df = player_stats_df[['player', 'runs', 'strike_rate', 'balls_faced']].copy()
    
    # Top 5 players by runs
    top_batting_runs = batting_df.nlargest(5, 'runs')
    
    # Top 5 players by strike rate (only considering those who faced 30 balls or more)
    top_batting_strike_rate = batting_df[batting_df['balls_faced'] >= 30].nlargest(5, 'strike_rate')
    
    # Concatenate without dropping duplicates to ensure all top performers are shown
    batting_summary = pd.concat([top_batting_runs, top_batting_strike_rate])
    batting_summary.to_csv("best_batting_performers.csv", index=False)

    # Best Bowling Performers
    bowling_df = player_stats_df[['player', 'wickets', 'balls_bowled', 'economy_rate']].copy()
    
    # Top 5 players by wickets
    top_bowling_wickets = bowling_df.nlargest(5, 'wickets')
    
    # Top 5 players by economy rate (only considering those who bowled 30 balls or more)
    top_bowling_economy = bowling_df[bowling_df['balls_bowled'] >= 30].nsmallest(5, 'economy_rate')
    
    # Concatenate without dropping duplicates to ensure all top performers are shown
    bowling_summary = pd.concat([top_bowling_wickets, top_bowling_economy])
    bowling_summary.to_csv("best_bowling_performers.csv", index=False)

# Execute functions
plot_team_statistics()
plot_player_statistics()
generate_best_performers_csv()
print("Analysis complete! Charts saved and best performers csv file generated.")
