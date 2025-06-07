#!/usr/bin/env python3
"""
Betting Market vs Statistical Models: Pacers Championship Analysis
Comparing market odds with historical precedent and Elo predictions
"""

def odds_to_probability(american_odds):
    """Convert American odds to probability percentage"""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)

def probability_to_american_odds(prob):
    """Convert probability to American odds"""
    if prob >= 0.5:
        return int(-100 * prob / (1 - prob))
    else:
        return int(100 * (1 - prob) / prob)

def main():
    print("🎲 BETTING MARKET vs STATISTICAL MODELS ANALYSIS")
    print("="*75)
    print("📊 CURRENT SITUATION: Pacers lead Finals 1-0, market pricing analysis")
    print("🤔 QUESTION: Are the betting markets undervaluing the Pacers?")
    print("="*75)
    
    # Different probability estimates
    estimates = {
        "Betting Markets": 25.0,
        "Elo Model (Adaptive K)": 32.5,
        "Historical Precedent": 44.4,
        "Historical (Game 1 Winners)": 70.1,
    }
    
    print("\n📈 PROBABILITY ESTIMATES COMPARISON:")
    print("="*75)
    print(f"{'Model/Source':<25} {'Pacers Win %':<12} {'Implied Odds':<12} {'Thunder Win %'}")
    print("-" * 75)
    
    for source, pacers_prob in estimates.items():
        thunder_prob = 100 - pacers_prob
        pacers_odds = probability_to_american_odds(pacers_prob / 100)
        thunder_odds = probability_to_american_odds(thunder_prob / 100)
        
        print(f"{source:<25} {pacers_prob:>6.1f}%      {pacers_odds:>+6d}        {thunder_prob:>6.1f}%")
    
    print()
    
    # Market analysis
    print("🎯 MARKET INEFFICIENCY ANALYSIS:")
    print("="*75)
    print("• Betting markets: 25% (most conservative)")
    print("• Elo model: 32.5% (moderate)")  
    print("• Historical road G1 winners: 44.4% (optimistic)")
    print("• Historical G1 winners overall: 70.1% (very optimistic)")
    print()
    print("💡 POTENTIAL VALUE OPPORTUNITIES:")
    print("• If historical precedent holds → Pacers are undervalued")
    print("• Market may be overweighting Thunder's season dominance")
    print("• Road Game 1 victories historically more impactful than markets believe")
    print()
    
    # Why markets might be conservative
    print("🤔 WHY MARKETS MIGHT BE CONSERVATIVE:")
    print("="*75)
    reasons = [
        ("Thunder's dominance", "1286 Elo rating, #1 all season", "Market respects consistency"),
        ("Small sample size", "Only 18 road G1 wins in Finals history", "Limited historical data"),
        ("Recency bias", "Recent dynasties (Warriors, Lakers)", "Market expects favorites to win"),
        ("Public betting", "Thunder more popular/recognizable", "Market adjustment for public money"),
        ("Injury concerns", "Pacers seen as lucky to reach Finals", "Market questions sustainability"),
        ("Home court remaining", "Thunder get 4 of next 6 at home", "Structural advantage remains"),
    ]
    
    for reason, detail, market_view in reasons:
        print(f"• {reason:<20}: {detail:<35} {market_view}")
    print()
    
    # Why historical data might be right
    print("🎯 WHY HISTORICAL DATA MIGHT BE RIGHT:")
    print("="*75)
    historical_factors = [
        ("Momentum matters", "Game 1 road wins create massive psychological shift", "44.4% win rate isn't luck"),
        ("Home court neutralized", "Thunder's biggest advantage eliminated", "Series now essentially neutral"),
        ("Playoff basketball", "Different from regular season", "Elo may overweight regular season"),
        ("Championship experience", "Pacers proved they belong here", "Market underestimating their growth"),
        ("Pressure reversal", "Now on Thunder to respond", "Favorites often crack under pressure"),
        ("Historical precedent", "1995 Rockets, 2011 Mavs, etc.", "Upsets happen in Finals"),
    ]
    
    for factor, explanation, implication in historical_factors:
        print(f"• {factor:<20}: {explanation:<40} {implication}")
    print()
    
    # Value betting analysis
    print("💰 VALUE BETTING ANALYSIS:")
    print("="*75)
    print("🎲 IF YOU BELIEVE HISTORICAL DATA (44.4%):")
    market_pacers_odds = probability_to_american_odds(0.25)
    true_pacers_odds = probability_to_american_odds(0.444)
    
    print(f"• Market odds: {market_pacers_odds:+d} (25% implied)")
    print(f"• 'True' odds: {true_pacers_odds:+d} (44.4% implied)")
    print(f"• Expected value: +{((0.444 * 4) - (0.556 * 1)) * 100:.1f}% on Pacers bet")
    print()
    print("🎲 IF YOU BELIEVE ELO MODEL (32.5%):")
    elo_pacers_odds = probability_to_american_odds(0.325)
    print(f"• Market odds: {market_pacers_odds:+d} (25% implied)")
    print(f"• Elo 'true' odds: {elo_pacers_odds:+d} (32.5% implied)")
    print(f"• Expected value: +{((0.325 * 4) - (0.675 * 1)) * 100:.1f}% on Pacers bet")
    print()
    
    # Risk assessment
    print("⚠️ RISK ASSESSMENT:")
    print("="*75)
    print("🚫 REASONS TO BE CAUTIOUS:")
    print("• Thunder still have superior talent")
    print("• 105.9 Elo point gap is substantial")
    print("• Home court advantage worth 3-4 points per game")
    print("• Sample size of road G1 winners is small (18 cases)")
    print("• Modern NBA may be different from historical average")
    print()
    print("✅ REASONS TO TRUST HISTORICAL DATA:")
    print("• Road Game 1 wins are rare and meaningful events")
    print("• 44.4% represents significant sample over 70+ years")
    print("• Psychological factors are real in championship series")
    print("• Market may be overweighting regular season performance")
    print("• Pacers have already exceeded expectations multiple times")
    print()
    
    # Final recommendation
    print("🎯 FINAL ASSESSMENT:")
    print("="*75)
    print("📊 CONSENSUS PROBABILITY ESTIMATE:")
    weighted_avg = (25 * 0.3 + 32.5 * 0.4 + 44.4 * 0.3)  # Weight market/elo/historical
    print(f"• Weighted average: ~{weighted_avg:.1f}% (30% market, 40% Elo, 30% historical)")
    print(f"• Market pricing: 25%")
    print(f"• Suggested 'true' probability: 35-40%")
    print()
    print("💡 CONCLUSION:")
    print("Markets appear to be undervaluing Pacers by 10-15 percentage points")
    print("Historical precedent suggests legitimate value opportunity exists")
    print("Road Game 1 victories are rarer and more impactful than markets believe")

if __name__ == "__main__":
    main() 