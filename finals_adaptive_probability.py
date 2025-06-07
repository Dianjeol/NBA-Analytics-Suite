#!/usr/bin/env python3
"""
NBA Finals Series Win Probability Calculator - Adaptive K System
Uses Adaptive K (15→25) ratings for ultimate prediction accuracy
"""

import math
from itertools import product

def expected_score(rating_a, rating_b):
    """Calculate expected score (win probability) for team A against team B"""
    return 1 / (1 + 10**((rating_b - rating_a) / 400))

def calculate_series_probability(thunder_elo, pacers_elo, home_advantage=40):
    """
    Calculate series win probability from current state (Pacers lead 1-0)
    NBA Finals format: Best of 7 (first to 4 wins)
    Home court pattern: 2-2-1-1-1 (higher seed gets games 1,2,6,7)
    """
    
    # Thunder (#1 seed) has home court advantage
    # Game locations for remaining games (games 2-7):
    remaining_games_locations = [
        'thunder_home',  # Game 2
        'pacers_home',   # Game 3  
        'pacers_home',   # Game 4
        'thunder_home',  # Game 5
        'thunder_home',  # Game 6
        'thunder_home'   # Game 7
    ]
    
    # Calculate win probabilities for each location
    thunder_home_prob = expected_score(thunder_elo + home_advantage, pacers_elo)
    pacers_home_prob = expected_score(pacers_elo + home_advantage, thunder_elo)
    
    print(f"Individual game win probabilities:")
    print(f"• Thunder at home: {thunder_home_prob:.1%}")
    print(f"• Pacers at home: {pacers_home_prob:.1%}")
    print()
    
    def simulate_series_from_state(pacers_wins, thunder_wins, game_index):
        """Recursively simulate series outcomes"""
        # Base cases: someone has won the series
        if pacers_wins == 4:
            return 1.0  # Pacers win probability for this path
        elif thunder_wins == 4:
            return 0.0  # Thunder win probability for this path
        
        # If we've played all 7 games, someone must have won
        if game_index >= len(remaining_games_locations):
            return 0.0
        
        # Get the win probability for the current game
        location = remaining_games_locations[game_index]
        if location == 'thunder_home':
            thunder_win_prob = thunder_home_prob
            pacers_win_prob = 1 - thunder_home_prob
        else:  # pacers_home
            pacers_win_prob = pacers_home_prob
            thunder_win_prob = 1 - pacers_home_prob
        
        # Calculate probability weighted outcomes
        # Pacers win this game
        pacers_path_prob = pacers_win_prob * simulate_series_from_state(
            pacers_wins + 1, thunder_wins, game_index + 1
        )
        
        # Thunder win this game  
        thunder_path_prob = thunder_win_prob * simulate_series_from_state(
            pacers_wins, thunder_wins + 1, game_index + 1
        )
        
        return pacers_path_prob + thunder_path_prob
    
    # Start simulation from current state: Pacers 1, Thunder 0, Game 2 next
    pacers_series_probability = simulate_series_from_state(1, 0, 0)
    thunder_series_probability = 1 - pacers_series_probability
    
    return pacers_series_probability, thunder_series_probability

def main():
    # Current Elo ratings from Adaptive K (15→25) system
    thunder_elo = 1264.3  # #1 ranked team
    pacers_elo = 1158.4   # #4 ranked team
    
    print("🏆 NBA FINALS SERIES WIN PROBABILITY - ADAPTIVE K SYSTEM")
    print("="*75)
    print("🎯 CURRENT SITUATION:")
    print("• Series: Indiana Pacers vs Oklahoma City Thunder")
    print("• Current state: PACERS LEAD 1-0")
    print("• Format: Best of 7 (first to 4 wins)")
    print("• Home court: Thunder (#1 seed)")
    print()
    
    print("📊 TEAM RATINGS (Adaptive K: 15→25):")
    print(f"• 🏆 Oklahoma City Thunder: {thunder_elo:.1f} Elo (#1)")
    print(f"• 📈 Indiana Pacers: {pacers_elo:.1f} Elo (#4)")
    print(f"• Rating difference: {thunder_elo - pacers_elo:.1f} points")
    print("• System: K=15 for 2024 games, K=25 for 2025 games")
    print()
    
    print("🏠 HOME COURT ADVANTAGE PATTERN:")
    print("Games 1-2: Thunder home (Game 1 already played)")
    print("Games 3-4: Pacers home") 
    print("Game 5: Thunder home")
    print("Games 6-7: Thunder home (if necessary)")
    print()
    
    # Calculate series probabilities
    pacers_prob, thunder_prob = calculate_series_probability(thunder_elo, pacers_elo)
    
    print("🎯 SERIES WIN PROBABILITIES:")
    print("="*75)
    print(f"• 📈 Indiana Pacers: {pacers_prob:.1%}")
    print(f"• 🏆 Oklahoma City Thunder: {thunder_prob:.1%}")
    print()
    
    # Compare across all systems
    print("🔄 COMPARISON ACROSS ALL SYSTEMS:")
    print("="*75)
    
    # Other system probabilities (calculated separately)
    other_systems = {
        "Original (Full K↓)": {"thunder": 1286.2, "pacers": 1146.9, "pacers_rank": 5},
        "2025-Only (K↓)": {"thunder": 1248.8, "pacers": 1146.8, "pacers_rank": 5},
        "2025-Only (K=20)": {"thunder": 1213.7, "pacers": 1131.8, "pacers_rank": 2},
        "Full Season (K=20)": {"thunder": 1255.9, "pacers": 1139.5, "pacers_rank": 5}
    }
    
    for system_name, ratings in other_systems.items():
        t_elo = ratings["thunder"]
        p_elo = ratings["pacers"]
        p_rank = ratings["pacers_rank"]
        
        # Quick series probability calculation
        t_home_prob = expected_score(t_elo + 40, p_elo)
        p_home_prob = expected_score(p_elo + 40, t_elo)
        
        # Simplified calculation for comparison
        def quick_sim(p_wins, t_wins, games_left, home_pattern):
            if p_wins == 4: return 1.0
            if t_wins == 4: return 0.0
            if games_left == 0: return 0.0
            
            if home_pattern[6-games_left] == 'thunder':
                p_win_prob = 1 - t_home_prob
            else:
                p_win_prob = p_home_prob
                
            return (p_win_prob * quick_sim(p_wins+1, t_wins, games_left-1, home_pattern) + 
                   (1-p_win_prob) * quick_sim(p_wins, t_wins+1, games_left-1, home_pattern))
        
        pattern = ['thunder', 'pacers', 'pacers', 'thunder', 'thunder', 'thunder']
        series_prob = quick_sim(1, 0, 6, pattern)
        
        print(f"{system_name:<18}: Pacers #{p_rank} → {series_prob:.1%} series win chance")
    
    print(f"{'Adaptive K (15→25)':<18}: Pacers #4 → {pacers_prob:.1%} series win chance ⬅️ CURRENT")
    print()
    
    # Statistical context
    print("📈 ADAPTIVE K SYSTEM CONTEXT:")
    print("="*75)
    print("• K=15 for 2024 games (552 games): Early season, less predictive")
    print("• K=25 for 2025 games (834 games): Recent form, more weight")
    print("• Balances complete data with recency emphasis")
    print("• Pacers ranked #4 (vs #2 in pure recent, #5 in most others)")
    print("• Thunder's dominance consistent across ALL systems")
    print()
    
    # Betting odds
    def prob_to_american_odds(prob):
        if prob >= 0.5:
            return int(-100 * prob / (1 - prob))
        else:
            return int(100 * (1 - prob) / prob)
    
    pacers_odds = prob_to_american_odds(pacers_prob)
    thunder_odds = prob_to_american_odds(thunder_prob)
    
    print("🎲 BETTING ODDS EQUIVALENT:")
    print("="*75)
    print(f"• Pacers to win Finals: {pacers_odds:+d} ({pacers_prob:.1%})")
    print(f"• Thunder to win Finals: {thunder_odds:+d} ({thunder_prob:.1%})")
    print()
    
    # Impact analysis
    neutral_game_prob = expected_score(pacers_elo, thunder_elo)
    print("💡 IMPACT OF ADAPTIVE K SYSTEM:")
    print("="*75)
    print(f"• Pacers individual game chance: {neutral_game_prob:.1%} (neutral court)")
    print(f"• Thunder's 105.9 Elo advantage creates {thunder_prob:.1%} series edge")
    print(f"• Pacers' #4 ranking better than most systems (#5)")
    print(f"• 1-0 lead helps but Thunder still heavily favored")
    print()
    
    print("🔥 ULTIMATE INSIGHTS:")
    print("="*75)
    print("• Thunder STILL overwhelming favorites despite 1-0 deficit")
    print("• Adaptive K system gives Pacers slight boost vs other systems")
    print("• Recent form emphasis helps Pacers but not enough")
    print("• Thunder's season-long dominance + home court too strong")
    print("• System shows Pacers have legitimate but slim championship hopes")

if __name__ == "__main__":
    main() 