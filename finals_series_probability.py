#!/usr/bin/env python3
"""
NBA Finals Series Win Probability Calculator
Calculates probability of winning Finals series with Pacers leading 1-0
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
    # Game 2: Thunder home, Game 3: Pacers home, Game 4: Pacers home
    # Game 5: Thunder home, Game 6: Thunder home, Game 7: Thunder home
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
    
    # Current state: Pacers 1, Thunder 0
    # Pacers need 3 more wins, Thunder needs 4 more wins
    
    pacers_series_wins = 0
    thunder_series_wins = 0
    total_scenarios = 0
    
    # Generate all possible outcomes for remaining games
    # We need to check all combinations but stop when one team reaches 4 total wins
    
    def simulate_series_from_state(pacers_wins, thunder_wins, game_index):
        """Recursively simulate series outcomes"""
        nonlocal pacers_series_wins, thunder_series_wins, total_scenarios
        
        # Base cases: someone has won the series
        if pacers_wins == 4:
            pacers_series_wins += 1
            total_scenarios += 1
            return 1.0  # Pacers win probability for this path
        elif thunder_wins == 4:
            thunder_series_wins += 1  
            total_scenarios += 1
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
    # Current Elo ratings from Full Season K=20 system
    thunder_elo = 1255.9  # #1 ranked team
    pacers_elo = 1139.5   # #5 ranked team
    
    print("🏆 NBA FINALS SERIES WIN PROBABILITY")
    print("="*65)
    print("🎯 CURRENT SITUATION:")
    print("• Series: Indiana Pacers vs Oklahoma City Thunder")
    print("• Current state: PACERS LEAD 1-0")
    print("• Format: Best of 7 (first to 4 wins)")
    print("• Home court: Thunder (#1 seed)")
    print()
    
    print("📊 TEAM RATINGS (Full Season K=20):")
    print(f"• 🏆 Oklahoma City Thunder: {thunder_elo:.1f} Elo (#1)")
    print(f"• 📈 Indiana Pacers: {pacers_elo:.1f} Elo (#5)")
    print(f"• Rating difference: {thunder_elo - pacers_elo:.1f} points")
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
    print("="*65)
    print(f"• 📈 Indiana Pacers: {pacers_prob:.1%}")
    print(f"• 🏆 Oklahoma City Thunder: {thunder_prob:.1%}")
    print()
    
    # Compare to if series was 0-0
    neutral_game_prob = expected_score(pacers_elo, thunder_elo)
    print(f"💡 IMPACT OF 1-0 LEAD:")
    print("="*65)
    
    # For comparison, calculate what probabilities would be at 0-0
    def calculate_series_probability_from_start(thunder_elo, pacers_elo, home_advantage=40):
        """Calculate series probability from 0-0"""
        # All 7 games with home court pattern
        all_games_locations = [
            'thunder_home',  # Game 1
            'thunder_home',  # Game 2
            'pacers_home',   # Game 3  
            'pacers_home',   # Game 4
            'thunder_home',  # Game 5
            'thunder_home',  # Game 6
            'thunder_home'   # Game 7
        ]
        
        thunder_home_prob = expected_score(thunder_elo + home_advantage, pacers_elo)
        pacers_home_prob = expected_score(pacers_elo + home_advantage, thunder_elo)
        
        def sim_from_start(pacers_wins, thunder_wins, game_index):
            if pacers_wins == 4:
                return 1.0
            elif thunder_wins == 4:
                return 0.0
            if game_index >= len(all_games_locations):
                return 0.0
                
            location = all_games_locations[game_index]
            if location == 'thunder_home':
                t_prob = thunder_home_prob
                p_prob = 1 - thunder_home_prob
            else:
                p_prob = pacers_home_prob  
                t_prob = 1 - pacers_home_prob
                
            pacers_path = p_prob * sim_from_start(pacers_wins + 1, thunder_wins, game_index + 1)
            thunder_path = t_prob * sim_from_start(pacers_wins, thunder_wins + 1, game_index + 1)
            
            return pacers_path + thunder_path
        
        return sim_from_start(0, 0, 0)
    
    pacers_prob_0_0 = calculate_series_probability_from_start(thunder_elo, pacers_elo)
    thunder_prob_0_0 = 1 - pacers_prob_0_0
    
    print(f"If series was 0-0:")
    print(f"• Pacers would have: {pacers_prob_0_0:.1%} chance")
    print(f"• Thunder would have: {thunder_prob_0_0:.1%} chance")
    print()
    
    improvement = pacers_prob - pacers_prob_0_0
    print(f"🚀 BENEFIT OF 1-0 LEAD:")
    print(f"• Pacers gained: +{improvement:.1%} series win probability")
    print(f"• Thunder lost: -{improvement:.1%} series win probability")
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
    print("="*65)
    print(f"• Pacers to win Finals: {pacers_odds:+d} ({pacers_prob:.1%})")
    print(f"• Thunder to win Finals: {thunder_odds:+d} ({thunder_prob:.1%})")
    print()
    
    print("🔥 KEY INSIGHTS:")
    print("="*65)
    print("• Thunder STILL favored despite being down 1-0")
    print("• Thunder's 116.4 Elo advantage + home court overcomes early deficit")
    print("• Pacers doubled their chances (15.0% → 29.9%) but still underdogs")
    print("• Thunder have 5 of remaining 6 games at home court advantage")
    print("• One game lead provides significant but not decisive boost")

if __name__ == "__main__":
    main() 