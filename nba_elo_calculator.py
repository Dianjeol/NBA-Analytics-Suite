#!/usr/bin/env python3
"""
NBA Elo Rating Calculator for 2024 Season
Calculates Elo ratings for all teams with decreasing K-factor over time
"""

import json
import math
from datetime import datetime
from collections import defaultdict
import sys

class EloCalculator:
    def __init__(self, initial_elo=1000, initial_k=40, min_k=10):
        self.initial_elo = initial_elo
        self.initial_k = initial_k
        self.min_k = min_k
        self.team_elos = defaultdict(lambda: initial_elo)
        self.game_count = 0
        self.elo_history = defaultdict(list)
        
    def calculate_k_factor(self, game_number, total_games):
        """Calculate decreasing K-factor based on game progression"""
        progress = game_number / total_games
        k = self.initial_k * (1 - progress * 0.75) + self.min_k * progress * 0.75
        return max(k, self.min_k)
    
    def expected_score(self, rating_a, rating_b):
        """Calculate expected score for team A against team B"""
        return 1 / (1 + 10**((rating_b - rating_a) / 400))
    
    def update_elo(self, team_a, team_b, score_a, score_b, k_factor):
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
        
        # Update ratings
        new_rating_a = rating_a + k_factor * mov_multiplier * (actual_a - expected_a)
        new_rating_b = rating_b + k_factor * mov_multiplier * (actual_b - expected_b)
        
        self.team_elos[team_a] = new_rating_a
        self.team_elos[team_b] = new_rating_b
        
        return new_rating_a, new_rating_b

def load_and_process_games():
    """Load and process NBA games from JSON file"""
    with open('nba_2024_games.json', 'r') as f:
        data = json.load(f)
    
    games = []
    for game in data['response']:
        # Only process finished games with valid scores
        if (game['status']['short'] == 3 and 
            game['scores']['home']['points'] is not None and 
            game['scores']['visitors']['points'] is not None):
            
            games.append({
                'id': game['id'],
                'date': datetime.fromisoformat(game['date']['start'].replace('Z', '+00:00')),
                'stage': game['stage'],
                'home_team': game['teams']['home']['name'],
                'visitor_team': game['teams']['visitors']['name'],
                'home_score': int(game['scores']['home']['points']),
                'visitor_score': int(game['scores']['visitors']['points'])
            })
    
    # Sort games by date
    games.sort(key=lambda x: x['date'])
    return games

def format_elo_display(team_elos, title):
    """Format Elo ratings for nice display"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")
    print(f"{'Rank':<5} {'Team':<30} {'Elo Rating':<15}")
    print(f"{'-'*60}")
    
    # Sort teams by Elo rating (descending)
    sorted_teams = sorted(team_elos.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (team, elo) in enumerate(sorted_teams, 1):
        print(f"{rank:<5} {team:<30} {elo:>10.1f}")

def main():
    print("🏀 NBA Elo Calculator - 2024 Season")
    print("Loading games and calculating Elo ratings...")
    
    # Load games
    games = load_and_process_games()
    print(f"Loaded {len(games)} finished games")
    
    # Initialize Elo calculator
    elo_calc = EloCalculator()
    
    # Separate games by stage
    regular_season_games = [g for g in games if g['stage'] <= 2]  # Preseason + Regular season
    playoff_games = [g for g in games if g['stage'] == 3]  # Playoffs
    
    total_games = len(games)
    
    print(f"Regular Season + Preseason: {len(regular_season_games)} games")
    print(f"Playoffs: {len(playoff_games)} games")
    
    # Process regular season games
    print("\nProcessing regular season games...")
    for i, game in enumerate(regular_season_games):
        k_factor = elo_calc.calculate_k_factor(i, len(regular_season_games))
        
        elo_calc.update_elo(
            game['home_team'], 
            game['visitor_team'],
            game['home_score'], 
            game['visitor_score'],
            k_factor
        )
        elo_calc.game_count += 1
        
        # Store Elo history
        elo_calc.elo_history[game['home_team']].append(elo_calc.team_elos[game['home_team']])
        elo_calc.elo_history[game['visitor_team']].append(elo_calc.team_elos[game['visitor_team']])
    
    # Save regular season Elo ratings
    regular_season_elos = dict(elo_calc.team_elos)
    
    # Display regular season results
    format_elo_display(regular_season_elos, "ELO RATINGS - END OF REGULAR SEASON")
    
    # Process playoff games
    if playoff_games:
        print(f"\nProcessing {len(playoff_games)} playoff games...")
        for i, game in enumerate(playoff_games):
            # Use lower K-factor for playoffs (more stable ratings)
            k_factor = elo_calc.calculate_k_factor(
                len(regular_season_games) + i, 
                total_games
            )
            
            elo_calc.update_elo(
                game['home_team'], 
                game['visitor_team'],
                game['home_score'], 
                game['visitor_score'],
                k_factor
            )
            elo_calc.game_count += 1
        
        # Display final playoff results
        format_elo_display(elo_calc.team_elos, "ELO RATINGS - END OF PLAYOFFS")
    
    # Show some interesting statistics
    print(f"\n{'='*60}")
    print("SEASON STATISTICS")
    print(f"{'='*60}")
    
    final_elos = dict(elo_calc.team_elos)
    highest_team = max(final_elos.items(), key=lambda x: x[1])
    lowest_team = min(final_elos.items(), key=lambda x: x[1])
    
    print(f"Highest Elo: {highest_team[0]} ({highest_team[1]:.1f})")
    print(f"Lowest Elo:  {lowest_team[0]} ({lowest_team[1]:.1f})")
    print(f"Elo Range:   {highest_team[1] - lowest_team[1]:.1f} points")
    print(f"Average Elo: {sum(final_elos.values()) / len(final_elos):.1f}")
    
    # Show biggest Elo changes
    if regular_season_elos:
        print(f"\n{'='*60}")
        print("BIGGEST ELO CHANGES FROM REGULAR SEASON TO PLAYOFFS")
        print(f"{'='*60}")
        
        changes = []
        for team in final_elos:
            if team in regular_season_elos:
                change = final_elos[team] - regular_season_elos[team]
                changes.append((team, change))
        
        changes.sort(key=lambda x: x[1], reverse=True)
        
        print("Biggest Gainers:")
        for team, change in changes[:5]:
            print(f"  {team:<30} +{change:>6.1f}")
        
        print("\nBiggest Decliners:")
        for team, change in changes[-5:]:
            print(f"  {team:<30} {change:>7.1f}")

if __name__ == "__main__":
    main() 