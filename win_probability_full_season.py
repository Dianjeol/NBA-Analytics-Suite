#!/usr/bin/env python3
"""
NBA Win Probability Calculator - Pacers vs Thunder (Full Season K=20)
"""

import math

def expected_score(rating_a, rating_b):
    """Calculate expected score (win probability) for team A against team B"""
    return 1 / (1 + 10**((rating_b - rating_a) / 400))

def main():
    # Current Elo ratings from Full Season K=20 system
    thunder_elo = 1255.9  # #1 ranked team
    pacers_elo = 1139.5   # #5 ranked team
    
    # Calculate neutral court probabilities
    pacers_win_prob = expected_score(pacers_elo, thunder_elo)
    thunder_win_prob = expected_score(thunder_elo, pacers_elo)
    
    print("🏀 WIN PROBABILITY: Pacers vs Thunder (FULL SEASON)")
    print("="*75)
    print("📊 Based on Full Season K=20 Elo ratings (complete 2024 season):")
    print(f"• 🏆 Oklahoma City Thunder: {thunder_elo:.1f} Elo (#1)")
    print(f"• 📈 Indiana Pacers: {pacers_elo:.1f} Elo (#5)")
    print(f"• Rating difference: {thunder_elo - pacers_elo:.1f} points")
    print()
    
    print("⚖️  NEUTRAL COURT MATCHUP:")
    print(f"• Thunder win probability: {thunder_win_prob:.1%}")
    print(f"• Pacers win probability: {pacers_win_prob:.1%}")
    print()
    
    # Home court advantage analysis
    home_advantage = 40  # Typical NBA home court advantage
    
    print("🏠 WITH HOME COURT ADVANTAGE (+40 Elo):")
    print("="*75)
    
    # Thunder hosting
    thunder_home_elo = thunder_elo + home_advantage
    pacers_away_prob = expected_score(pacers_elo, thunder_home_elo)
    thunder_home_prob = 1 - pacers_away_prob
    
    print("If Thunder host in Oklahoma City:")
    print(f"• Thunder win probability: {thunder_home_prob:.1%}")
    print(f"• Pacers win probability: {pacers_away_prob:.1%}")
    print()
    
    # Pacers hosting
    pacers_home_elo = pacers_elo + home_advantage
    thunder_away_prob = expected_score(thunder_elo, pacers_home_elo)
    pacers_home_prob = 1 - thunder_away_prob
    
    print("If Pacers host in Indianapolis:")
    print(f"• Pacers win probability: {pacers_home_prob:.1%}")
    print(f"• Thunder win probability: {thunder_away_prob:.1%}")
    print()
    
    # System comparison
    print("🔄 COMPARISON WITH OTHER SYSTEMS:")
    print("="*75)
    
    # Other system ratings
    other_systems = {
        "2025-Only K=20": {"thunder": 1213.7, "pacers": 1131.8, "pacers_rank": 2},
        "Original Full": {"thunder": 1286.2, "pacers": 1146.9, "pacers_rank": 5},
        "2025-Only K↓": {"thunder": 1248.8, "pacers": 1146.8, "pacers_rank": 5}
    }
    
    for system_name, ratings in other_systems.items():
        t_elo = ratings["thunder"]
        p_elo = ratings["pacers"]
        p_rank = ratings["pacers_rank"]
        neutral_prob = expected_score(p_elo, t_elo)
        print(f"{system_name:<15}: Pacers #{p_rank} → {neutral_prob:.1%} chance vs Thunder")
    
    print(f"{'Full Season K=20':<15}: Pacers #5 → {pacers_win_prob:.1%} chance vs Thunder ⬅️ CURRENT")
    print()
    
    # Statistical context
    print("📈 FULL SEASON CONTEXT:")
    print("="*75)
    print("• Season span: October 2024 - June 2025 (1,386 games)")
    print("• Latest game: Pacers 111-110 Thunder (June 6, 2025)")
    print("• Fixed K=20 gives equal weight to ALL games")
    print("• Pacers rank #5 vs #2 in recent-only systems")
    print("• Thunder's dominance consistent across all systems")
    print()
    
    # Betting odds conversion
    print("🎯 BETTING ODDS EQUIVALENT (American format):")
    print("="*75)
    
    def prob_to_american_odds(prob):
        if prob >= 0.5:
            return int(-100 * prob / (1 - prob))
        else:
            return int(100 * (1 - prob) / prob)
    
    thunder_neutral_odds = prob_to_american_odds(thunder_win_prob)
    pacers_neutral_odds = prob_to_american_odds(pacers_win_prob)
    
    print("Neutral court:")
    print(f"• Thunder: {thunder_neutral_odds:+d} ({thunder_win_prob:.1%})")
    print(f"• Pacers: {pacers_neutral_odds:+d} ({pacers_win_prob:.1%})")
    print()
    
    print("Thunder home court:")
    thunder_home_odds = prob_to_american_odds(thunder_home_prob)
    pacers_away_odds = prob_to_american_odds(pacers_away_prob)
    print(f"• Thunder: {thunder_home_odds:+d} ({thunder_home_prob:.1%})")
    print(f"• Pacers: {pacers_away_odds:+d} ({pacers_away_prob:.1%})")
    print()
    
    print("🔥 FULL SEASON INSIGHT:")
    print("Thunder have 116.4 Elo advantage - slightly larger than recent-only")
    print("systems, reflecting their season-long dominance!")

if __name__ == "__main__":
    main() 