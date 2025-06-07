#!/usr/bin/env python3
"""
NBA Win Probability Calculator - Pacers vs Thunder
"""

import math

def expected_score(rating_a, rating_b):
    """Calculate expected score (win probability) for team A against team B"""
    return 1 / (1 + 10**((rating_b - rating_a) / 400))

def main():
    # Current Elo ratings from Fixed K=20 system
    thunder_elo = 1213.7  # #1 ranked team
    pacers_elo = 1131.8   # #2 ranked team
    
    # Calculate neutral court probabilities
    pacers_win_prob = expected_score(pacers_elo, thunder_elo)
    thunder_win_prob = expected_score(thunder_elo, pacers_elo)
    
    print("🏀 CURRENT WIN PROBABILITY: Pacers vs Thunder")
    print("="*65)
    print("📊 Based on Fixed K=20 Elo ratings (2025 games only):")
    print(f"• 🏆 Oklahoma City Thunder: {thunder_elo:.1f} Elo (#1)")
    print(f"• 📈 Indiana Pacers: {pacers_elo:.1f} Elo (#2)")
    print(f"• Rating difference: {thunder_elo - pacers_elo:.1f} points")
    print()
    
    print("⚖️  NEUTRAL COURT MATCHUP:")
    print(f"• Thunder win probability: {thunder_win_prob:.1%}")
    print(f"• Pacers win probability: {pacers_win_prob:.1%}")
    print()
    
    # Home court advantage analysis
    home_advantage = 40  # Typical NBA home court advantage
    
    print("🏠 WITH HOME COURT ADVANTAGE (+40 Elo):")
    print("="*65)
    
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
    
    # Historical context
    print("📈 RECENT CONTEXT:")
    print("="*65)
    print("• Latest matchup: Pacers 111-110 Thunder (Jun 6, 2025)")
    print("• That 1-point Pacers victory helped boost their ranking")
    print("• Thunder still favored due to higher overall Elo")
    print("• Pacers' #2 ranking shows strong recent form")
    print()
    
    # Betting odds conversion
    print("🎯 BETTING ODDS EQUIVALENT (American format):")
    print("="*65)
    
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
    
    print("🔥 KEY INSIGHT:")
    print("Despite being #2, Pacers are still underdogs due to")
    print("Thunder's 81.9 Elo point advantage!")

if __name__ == "__main__":
    main() 