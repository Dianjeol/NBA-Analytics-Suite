#!/usr/bin/env python3
"""
NBA Elo K-Factor Comparison - Decreasing vs Fixed K-Factor
"""

def print_k_factor_comparison():
    """Compare the two different K-factor systems"""
    
    # Decreasing K-factor results (K=40→10)
    decreasing_k = [
        ("Oklahoma City Thunder", 1248.8, "🏆"),
        ("Cleveland Cavaliers", 1156.8, "🥇"),
        ("Minnesota Timberwolves", 1150.8, "🔥"),
        ("Boston Celtics", 1150.8, "🥈"),
        ("Indiana Pacers", 1146.8, "📈"),
        ("LA Clippers", 1112.6, "💪"),
        ("Denver Nuggets", 1104.3, "⭐"),
        ("Golden State Warriors", 1084.7, "👑"),
        ("Houston Rockets", 1069.4, "🚀"),
        ("Milwaukee Bucks", 1068.0, "🦌"),
        ("Los Angeles Lakers", 1067.0, "🏀"),
        ("New York Knicks", 1064.9, "🗽"),
        ("Detroit Pistons", 1061.6, "🔧"),
        ("Portland Trail Blazers", 1020.7, "🌲"),
        ("Chicago Bulls", 1009.1, "🐂"),
    ]
    
    # Fixed K=20 results
    fixed_k = [
        ("Oklahoma City Thunder", 1213.7, "🏆"),
        ("Indiana Pacers", 1131.8, "📈"),
        ("Minnesota Timberwolves", 1128.6, "🔥"),
        ("Boston Celtics", 1125.8, "🥈"),
        ("Cleveland Cavaliers", 1124.6, "🥇"),
        ("LA Clippers", 1096.8, "💪"),
        ("Denver Nuggets", 1082.4, "⭐"),
        ("Golden State Warriors", 1066.8, "👑"),
        ("Houston Rockets", 1056.2, "🚀"),
        ("Milwaukee Bucks", 1054.9, "🦌"),
        ("New York Knicks", 1053.7, "🗽"),
        ("Los Angeles Lakers", 1048.0, "🏀"),
        ("Detroit Pistons", 1044.4, "🔧"),
        ("Portland Trail Blazers", 1012.6, "🌲"),
        ("Chicago Bulls", 1012.2, "🐂"),
    ]
    
    print("🏀 NBA ELO K-FACTOR COMPARISON - 2025 GAMES")
    print("="*90)
    print("📊 METHODOLOGY COMPARISON:")
    print("• Decreasing K: K=40 → K=10 (more weight to early games)")
    print("• Fixed K=20:   K=20 constant (equal weight to all games)")
    print("• Same games: 834 from Jan 1 - Jun 6, 2025")
    print("• Same MOV scaling and starting Elo (1000)")
    print("="*90)
    
    # Create lookup dictionaries
    decreasing_dict = {team: (elo, rank+1) for rank, (team, elo, _) in enumerate(decreasing_k)}
    fixed_dict = {team: (elo, rank+1) for rank, (team, elo, _) in enumerate(fixed_k)}
    
    print(f"\n{'SIDE-BY-SIDE COMPARISON (Top 15)':^90}")
    print("="*90)
    print(f"{'Rank':<4} {'Team':<25} {'Decreasing K':<15} {'Fixed K=20':<15} {'Diff':<10} {'Rank Δ'}")
    print("-"*90)
    
    # Get all teams that appear in top 15 of either system
    all_teams = set()
    for team, _, _ in decreasing_k[:15]:
        all_teams.add(team)
    for team, _, _ in fixed_k[:15]:
        all_teams.add(team)
    
    # Sort by fixed K ranking for primary display
    fixed_rankings = [(team, elo, emoji) for team, elo, emoji in fixed_k if team in all_teams]
    
    for i, (team, elo_fixed, emoji) in enumerate(fixed_rankings[:15], 1):
        elo_dec, rank_dec = decreasing_dict.get(team, (0, 999))
        elo_diff = elo_fixed - elo_dec if elo_dec > 0 else 0
        rank_diff = rank_dec - i if rank_dec < 999 else 0
        
        rank_str = f"{rank_diff:+d}" if rank_diff != 0 else "="
        
        print(f"{i:<4} {emoji} {team:<22} {elo_dec:>10.1f} {elo_fixed:>13.1f} {elo_diff:>8.1f} {rank_str:>8}")

def print_key_insights():
    """Print key insights from K-factor comparison"""
    
    print(f"\n{'🎯 KEY INSIGHTS - K-FACTOR IMPACT':^90}")
    print("="*90)
    
    insights = [
        ("🏆 Oklahoma City Thunder", "Still #1, but lower Elo", "1248.8 → 1213.7 (-35.1)"),
        ("📈 Indiana Pacers", "MAJOR BOOST: #5 → #2", "1146.8 → 1131.8 (-15.0)"),
        ("🥇 Cleveland Cavaliers", "Dropped: #2 → #5", "1156.8 → 1124.6 (-32.2)"),
        ("🔥 Minnesota Timberwolves", "Similar: #3 → #3", "1150.8 → 1128.6 (-22.2)"),
        ("🥈 Boston Celtics", "Slight drop: #4 → #4", "1150.8 → 1125.8 (-25.0)"),
        ("🗽 New York Knicks", "Small improvement: #12 → #11", "1064.9 → 1053.7 (-11.2)"),
    ]
    
    for team, change, scores in insights:
        print(f"• {team:<25} {change:<25} {scores}")

def print_statistical_comparison():
    """Print statistical comparison between systems"""
    
    print(f"\n{'STATISTICAL COMPARISON':^90}")
    print("="*90)
    
    # Stats for decreasing K system
    dec_highest = 1248.8
    dec_lowest = 785.4  # From previous calculation
    dec_range = dec_highest - dec_lowest
    dec_east_avg = 979.5
    dec_west_avg = 1020.5
    
    # Stats for fixed K system  
    fixed_highest = 1213.7
    fixed_lowest = 826.7
    fixed_range = fixed_highest - fixed_lowest
    fixed_east_avg = 985.0
    fixed_west_avg = 1015.0
    
    print(f"{'Metric':<30} {'Decreasing K':<15} {'Fixed K=20':<15} {'Difference'}")
    print("-"*90)
    print(f"{'Highest Elo':<30} {dec_highest:<15.1f} {fixed_highest:<15.1f} {fixed_highest-dec_highest:+.1f}")
    print(f"{'Lowest Elo':<30} {dec_lowest:<15.1f} {fixed_lowest:<15.1f} {fixed_lowest-dec_lowest:+.1f}")
    print(f"{'Elo Range':<30} {dec_range:<15.1f} {fixed_range:<15.1f} {fixed_range-dec_range:+.1f}")
    print(f"{'Eastern Conf Avg':<30} {dec_east_avg:<15.1f} {fixed_east_avg:<15.1f} {fixed_east_avg-dec_east_avg:+.1f}")
    print(f"{'Western Conf Avg':<30} {dec_west_avg:<15.1f} {fixed_west_avg:<15.1f} {fixed_west_avg-dec_west_avg:+.1f}")
    print(f"{'West Advantage':<30} {dec_west_avg-dec_east_avg:<15.1f} {fixed_west_avg-fixed_east_avg:<15.1f} {(fixed_west_avg-fixed_east_avg)-(dec_west_avg-dec_east_avg):+.1f}")

def print_system_analysis():
    """Analyze which system works better"""
    
    print(f"\n{'🔬 SYSTEM ANALYSIS':^90}")
    print("="*90)
    print("📈 DECREASING K-FACTOR (K=40→10):")
    print("  ✓ Rewards early season performance more heavily")
    print("  ✓ Stabilizes ratings as season progresses")
    print("  ✓ Less volatile late in season")
    print("  ✗ May undervalue late-season improvement")
    print()
    print("⚖️  FIXED K-FACTOR (K=20):")
    print("  ✓ Equal weight to all games throughout season")
    print("  ✓ Better reflects recent form")
    print("  ✓ More responsive to playoff performance")
    print("  ✗ More volatile throughout entire season")
    print()
    print("🎯 IMPACT ON INDIANA PACERS:")
    print("  • Strong finish boosted them from #5 to #2 with fixed K")
    print("  • Latest game (IND 111-110 OKC) had bigger impact")
    print("  • Shows how fixed K rewards recent performance")

def main():
    print_k_factor_comparison()
    print_key_insights()
    print_statistical_comparison()
    print_system_analysis()
    
    print(f"\n{'='*90}")
    print(f"{'✅ K-FACTOR COMPARISON COMPLETE':^90}")
    print(f"{'='*90}")
    print("📊 Fixed K=20 system shows more recent-form based rankings")
    print("🏀 Indiana Pacers biggest beneficiary of equal weighting")
    print("⚡ Oklahoma City still dominates in both systems")

if __name__ == "__main__":
    main() 