#!/usr/bin/env python3
"""
NBA Elo Rating Calculator - Full Season with Fixed K-Factor
Calculates Elo ratings for the entire 2024 season using fixed K=20
"""

import json
import math
from datetime import datetime
from collections import defaultdict

class EloCalculatorFullSeasonFixedK:
    def __init__(self, initial_elo=1000, k_factor=20):
        self.initial_elo = initial_elo
        self.k_factor = k_factor  # Fixed K-factor for entire season
        self.team_elos = defaultdict(lambda: initial_elo)
        self.game_count = 0
    
    def expected_score(self, rating_a, rating_b):
        """Calculate expected score for team A against team B"""
        return 1 / (1 + 10**((rating_b - rating_a) / 400))
    
    def update_elo(self, team_a, team_b, score_a, score_b):
        """Update Elo ratings based on game result"""
        rating_a = self.team_elos[team_a]
        rating_b = self.team_elos[team_b]
        
        # Determine actual score (1 for win, 0 for loss)
        if score_a > score_b:
            actual_a, actual_b = 1, 0
        else:
            actual_a, actual_b = 0, 1
            
        # Calculate expected scores
        expected_a = self.expected_score(rating_a, rating_b)
        expected_b = self.expected_score(rating_b, rating_a)
        
        # Apply margin of victory multiplier
        score_diff = abs(score_a - score_b)
        mov_multiplier = math.log(score_diff + 1) / math.log(20)  # Logarithmic scaling
        
        # Update ratings using fixed K-factor
        new_rating_a = rating_a + self.k_factor * mov_multiplier * (actual_a - expected_a)
        new_rating_b = rating_b + self.k_factor * mov_multiplier * (actual_b - expected_b)
        
        self.team_elos[team_a] = new_rating_a
        self.team_elos[team_b] = new_rating_b
        
        return new_rating_a, new_rating_b

def load_and_process_all_games():
    """Load and process all NBA games from the 2024 season"""
    with open('nba_2024_games.json', 'r') as f:
        data = json.load(f)
    
    all_games = []
    for game in data['response']:
        # Only process finished games with valid scores
        if (game['status']['short'] == 3 and 
            game['scores']['home']['points'] is not None and 
            game['scores']['visitors']['points'] is not None):
            
            game_date = datetime.fromisoformat(game['date']['start'].replace('Z', '+00:00'))
            
            all_games.append({
                'id': game['id'],
                'date': game_date,
                'stage': game['stage'],
                'home_team': game['teams']['home']['name'],
                'visitor_team': game['teams']['visitors']['name'],
                'home_score': int(game['scores']['home']['points']),
                'visitor_score': int(game['scores']['visitors']['points'])
            })
    
    # Sort games by date
    all_games.sort(key=lambda x: x['date'])
    return all_games

def format_elo_display_full_season(team_elos, title):
    """Format Elo ratings for nice display"""
    print(f"\n{'='*70}")
    print(f"{title:^70}")
    print(f"{'='*70}")
    print(f"{'Rank':<5} {'Team':<35} {'Elo Rating':<15}")
    print(f"{'-'*70}")
    
    # Sort teams by Elo rating (descending)
    sorted_teams = sorted(team_elos.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (team, elo) in enumerate(sorted_teams, 1):
        print(f"{rank:<5} {team:<35} {elo:>10.1f}")

def create_conference_divisions():
    """Create team conference and division mappings"""
    divisions = {
        # Eastern Conference
        'Atlantic': ['Boston Celtics', 'Brooklyn Nets', 'New York Knicks', 'Philadelphia 76ers', 'Toronto Raptors'],
        'Central': ['Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks'],
        'Southeast': ['Atlanta Hawks', 'Charlotte Hornets', 'Miami Heat', 'Orlando Magic', 'Washington Wizards'],
        
        # Western Conference  
        'Northwest': ['Denver Nuggets', 'Minnesota Timberwolves', 'Oklahoma City Thunder', 'Portland Trail Blazers', 'Utah Jazz'],
        'Pacific': ['Golden State Warriors', 'LA Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings'],
        'Southwest': ['Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Pelicans', 'San Antonio Spurs']
    }
    
    team_conferences = {}
    for conf in ['Eastern', 'Western']:
        div_list = ['Atlantic', 'Central', 'Southeast'] if conf == 'Eastern' else ['Northwest', 'Pacific', 'Southwest']
        for div in div_list:
            for team in divisions.get(div, []):
                team_conferences[team] = conf
    
    return team_conferences

def main():
    print("🏀 NBA Elo Calculator - Full Season (Fixed K=20)")
    print("="*70)
    print("SEASON: Complete 2024 season (Oct 2024 - Jun 2025)")
    print("STARTING ELO: All teams reset to 1,000 points")
    print("K-FACTOR: Fixed at 20 for ALL games (no decrease)")
    print("="*70)
    
    # Load all games
    all_games = load_and_process_all_games()
    print(f"\nLoaded {len(all_games)} finished games from entire season")
    
    if len(all_games) == 0:
        print("❌ No games found!")
        return
    
    # Show date range
    first_game = all_games[0]
    last_game = all_games[-1]
    print(f"Date Range: {first_game['date'].strftime('%Y-%m-%d')} to {last_game['date'].strftime('%Y-%m-%d')}")
    
    # Initialize Elo calculator with fixed K-factor
    elo_calc = EloCalculatorFullSeasonFixedK(k_factor=20)
    
    # Separate games by stage
    preseason_games = [g for g in all_games if g['stage'] == 1]
    regular_season_games = [g for g in all_games if g['stage'] == 2]
    playoff_games = [g for g in all_games if g['stage'] == 3]
    
    print(f"Preseason games: {len(preseason_games)}")
    print(f"Regular Season games: {len(regular_season_games)}")
    print(f"Playoff games: {len(playoff_games)}")
    
    total_games = len(all_games)
    
    # Process all games with fixed K-factor
    print(f"\nProcessing {total_games} games with fixed K-factor = 20...")
    for i, game in enumerate(all_games):
        elo_calc.update_elo(
            game['home_team'], 
            game['visitor_team'],
            game['home_score'], 
            game['visitor_score']
        )
        elo_calc.game_count += 1
    
    # Display final results
    format_elo_display_full_season(elo_calc.team_elos, "FINAL ELO RATINGS - FULL SEASON (K=20 FIXED)")
    
    # Show statistics
    print(f"\n{'='*70}")
    print("FULL SEASON STATISTICS (K=20 FIXED)")
    print(f"{'='*70}")
    
    final_elos = dict(elo_calc.team_elos)
    sorted_teams = sorted(final_elos.items(), key=lambda x: x[1], reverse=True)
    
    highest_team = sorted_teams[0]
    lowest_team = sorted_teams[-1]
    
    print(f"Total games processed: {len(all_games)}")
    print(f"Highest Elo: {highest_team[0]} ({highest_team[1]:.1f})")
    print(f"Lowest Elo:  {lowest_team[0]} ({lowest_team[1]:.1f})")
    print(f"Elo Range:   {highest_team[1] - lowest_team[1]:.1f} points")
    print(f"Average Elo: {sum(final_elos.values()) / len(final_elos):.1f}")
    
    # Show conference breakdown
    team_conferences = create_conference_divisions()
    east_teams = [team for team, elo in final_elos.items() if team_conferences.get(team) == 'Eastern']
    west_teams = [team for team, elo in final_elos.items() if team_conferences.get(team) == 'Western']
    
    east_avg = sum(final_elos[team] for team in east_teams) / len(east_teams)
    west_avg = sum(final_elos[team] for team in west_teams) / len(west_teams)
    
    print(f"\nConference Breakdown:")
    print(f"Eastern Conference teams: {len(east_teams)}")
    print(f"Western Conference teams: {len(west_teams)}")
    print(f"Eastern Conference Average: {east_avg:.1f}")
    print(f"Western Conference Average: {west_avg:.1f}")
    print(f"Western Conference Advantage: {west_avg - east_avg:.1f} points")
    
    # Show comparison context
    print(f"\n{'='*70}")
    print("COMPARISON CONTEXT")
    print(f"{'='*70}")
    print("This uses fixed K=20 for the ENTIRE season vs previous systems:")
    print("• Original: K=40 → K=10 (decreasing), full season")
    print("• 2025-only: K=40 → K=10 (decreasing), 2025 games only") 
    print("• 2025-only: K=20 (fixed), 2025 games only")
    print("• Current: K=20 (fixed), FULL season")
    print("\nFixed K=20 gives equal weight to ALL games from Oct 2024-Jun 2025!")

if __name__ == "__main__":
    main() 