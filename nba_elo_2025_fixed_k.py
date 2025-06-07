#!/usr/bin/env python3
"""
NBA Elo Rating Calculator for 2025 Games Only - Fixed K-Factor
Calculates Elo ratings using only games played from January 1, 2025 onwards
Uses constant K-factor of 20 for all games
"""

import json
import math
from datetime import datetime, timezone
from collections import defaultdict

class EloCalculatorFixedK:
    def __init__(self, initial_elo=1000, k_factor=20):
        self.initial_elo = initial_elo
        self.k_factor = k_factor  # Fixed K-factor
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

def load_and_process_2025_games():
    """Load and process NBA games from 2025 only"""
    with open('nba_2024_games.json', 'r') as f:
        data = json.load(f)
    
    # Filter for 2025 games only (after December 31, 2024) - timezone aware
    cutoff_date = datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    
    games_2025 = []
    for game in data['response']:
        # Only process finished games with valid scores from 2025
        if (game['status']['short'] == 3 and 
            game['scores']['home']['points'] is not None and 
            game['scores']['visitors']['points'] is not None):
            
            game_date = datetime.fromisoformat(game['date']['start'].replace('Z', '+00:00'))
            
            # Only include games after December 31, 2024
            if game_date > cutoff_date:
                games_2025.append({
                    'id': game['id'],
                    'date': game_date,
                    'stage': game['stage'],
                    'home_team': game['teams']['home']['name'],
                    'visitor_team': game['teams']['visitors']['name'],
                    'home_score': int(game['scores']['home']['points']),
                    'visitor_score': int(game['scores']['visitors']['points'])
                })
    
    # Sort games by date
    games_2025.sort(key=lambda x: x['date'])
    return games_2025

def format_elo_display_fixed_k(team_elos, title):
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
    print("🏀 NBA Elo Calculator - 2025 Games Only (Fixed K=20)")
    print("="*70)
    print("FILTERING: Only games played from January 1, 2025 onwards")
    print("STARTING ELO: All teams reset to 1,000 points")
    print("K-FACTOR: Fixed at 20 for all games (no decrease)")
    print("="*70)
    
    # Load 2025 games only
    games_2025 = load_and_process_2025_games()
    print(f"\nLoaded {len(games_2025)} finished games from 2025")
    
    if len(games_2025) == 0:
        print("❌ No games found from 2025!")
        return
    
    # Show date range
    first_game = games_2025[0]
    last_game = games_2025[-1]
    print(f"Date Range: {first_game['date'].strftime('%Y-%m-%d')} to {last_game['date'].strftime('%Y-%m-%d')}")
    
    # Initialize Elo calculator with fixed K-factor
    elo_calc = EloCalculatorFixedK(k_factor=20)
    
    # Separate games by stage
    regular_season_games = [g for g in games_2025 if g['stage'] <= 2]
    playoff_games = [g for g in games_2025 if g['stage'] == 3]
    
    print(f"Regular Season games in 2025: {len(regular_season_games)}")
    print(f"Playoff games in 2025: {len(playoff_games)}")
    
    total_games = len(games_2025)
    
    # Process all 2025 games with fixed K-factor
    print(f"\nProcessing {total_games} games with K-factor = 20...")
    for i, game in enumerate(games_2025):
        elo_calc.update_elo(
            game['home_team'], 
            game['visitor_team'],
            game['home_score'], 
            game['visitor_score']
        )
        elo_calc.game_count += 1
    
    # Display final results
    format_elo_display_fixed_k(elo_calc.team_elos, "FINAL ELO RATINGS - 2025 GAMES (K=20 FIXED)")
    
    # Show statistics
    print(f"\n{'='*70}")
    print("2025 SEASON STATISTICS (K=20 FIXED)")
    print(f"{'='*70}")
    
    final_elos = dict(elo_calc.team_elos)
    teams_that_played = {team: elo for team, elo in final_elos.items() if elo != 1000}
    
    if teams_that_played:
        highest_team = max(teams_that_played.items(), key=lambda x: x[1])
        lowest_team = min(teams_that_played.items(), key=lambda x: x[1])
        
        print(f"Teams that played in 2025: {len(teams_that_played)}")
        print(f"Highest Elo: {highest_team[0]} ({highest_team[1]:.1f})")
        print(f"Lowest Elo:  {lowest_team[0]} ({lowest_team[1]:.1f})")
        print(f"Elo Range:   {highest_team[1] - lowest_team[1]:.1f} points")
        print(f"Average Elo (teams that played): {sum(teams_that_played.values()) / len(teams_that_played):.1f}")
        
        # Show conference breakdown
        team_conferences = create_conference_divisions()
        east_teams = [team for team in teams_that_played if team_conferences.get(team) == 'Eastern']
        west_teams = [team for team in teams_that_played if team_conferences.get(team) == 'Western']
        
        print(f"\nConference Breakdown:")
        print(f"Eastern Conference teams: {len(east_teams)}")
        print(f"Western Conference teams: {len(west_teams)}")
        
        if east_teams:
            east_avg = sum(final_elos[team] for team in east_teams) / len(east_teams)
            print(f"Eastern Conference Average: {east_avg:.1f}")
        
        if west_teams:
            west_avg = sum(final_elos[team] for team in west_teams) / len(west_teams)
            print(f"Western Conference Average: {west_avg:.1f}")
    
    # Show K-factor comparison
    print(f"\n{'='*70}")
    print("K-FACTOR COMPARISON")
    print(f"{'='*70}")
    print("Previous system: K=40 → K=10 (decreasing)")
    print("Current system:  K=20 (fixed)")
    print("Impact: More volatile ratings, larger swings throughout season")

if __name__ == "__main__":
    main() 