#!/usr/bin/env python3
"""
NBA Ultimate Comprehensive Elo System Comparison
Compares all five different Elo calculation methods
"""

def main():
    # All five systems we've calculated
    systems = {
        "Original (Full, K↓)": [
            ("Oklahoma City Thunder", 1286.2, "🏆"),
            ("Cleveland Cavaliers", 1196.4, "🥇"),
            ("Boston Celtics", 1184.6, "🥈"),
            ("Minnesota Timberwolves", 1154.2, "🔥"),
            ("Indiana Pacers", 1146.9, "📈"),
            ("LA Clippers", 1118.9, "💪"),
            ("Denver Nuggets", 1111.0, "⭐"),
            ("New York Knicks", 1097.1, "🗽"),
            ("Houston Rockets", 1095.4, "🚀"),
            ("Golden State Warriors", 1085.8, "👑"),
            ("Milwaukee Bucks", 1072.1, "🦌"),
            ("Los Angeles Lakers", 1064.4, "🏀"),
        ],
        "2025-Only (K↓)": [
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
        ],
        "2025-Only (K=20)": [
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
        ],
        "Full Season (K=20)": [
            ("Oklahoma City Thunder", 1255.9, "🏆"),
            ("Cleveland Cavaliers", 1167.0, "🥇"),
            ("Boston Celtics", 1165.5, "🥈"),
            ("Minnesota Timberwolves", 1141.3, "🔥"),
            ("Indiana Pacers", 1139.5, "📈"),
            ("LA Clippers", 1113.8, "💪"),
            ("Denver Nuggets", 1096.3, "⭐"),
            ("New York Knicks", 1086.0, "🗽"),
            ("Houston Rockets", 1082.9, "🚀"),
            ("Golden State Warriors", 1077.0, "👑"),
            ("Milwaukee Bucks", 1063.5, "🦌"),
            ("Los Angeles Lakers", 1051.8, "🏀"),
        ],
        "Adaptive K (15→25)": [
            ("Oklahoma City Thunder", 1264.3, "🏆"),
            ("Boston Celtics", 1165.5, "🥈"),
            ("Cleveland Cavaliers", 1164.9, "🥇"),
            ("Indiana Pacers", 1158.4, "📈"),
            ("Minnesota Timberwolves", 1157.4, "🔥"),
            ("LA Clippers", 1123.1, "💪"),
            ("Denver Nuggets", 1106.6, "⭐"),
            ("New York Knicks", 1086.8, "🗽"),
            ("Golden State Warriors", 1082.0, "👑"),
            ("Houston Rockets", 1081.6, "🚀"),
            ("Milwaukee Bucks", 1068.2, "🦌"),
            ("Los Angeles Lakers", 1056.4, "🏀"),
        ]
    }
    
    print("🏀 ULTIMATE NBA ELO SYSTEM COMPARISON")
    print("="*110)
    print("📊 FIVE DIFFERENT CALCULATION METHODS:")
    print("1. Original (Full, K↓):     Full season, K=40→10 decreasing")
    print("2. 2025-Only (K↓):         2025 games only, K=40→10 decreasing") 
    print("3. 2025-Only (K=20):       2025 games only, K=20 fixed")
    print("4. Full Season (K=20):     Full season, K=20 fixed")
    print("5. Adaptive K (15→25):     Full season, K=15 for 2024, K=25 for 2025")
    print("="*110)
    
    # Create comprehensive ranking table
    print(f"\n{'ULTIMATE RANKING TABLE (Top 12)':^110}")
    print("="*110)
    print(f"{'Team':<25} {'Orig':<8} {'25K↓':<8} {'25K20':<9} {'FullK20':<9} {'Adapt':<8} {'Best':<6} {'Worst':<6}")
    print("-"*110)
    
    # Get all teams that appear in top 12 of any system
    all_teams = set()
    for system_name, rankings in systems.items():
        for team, elo, emoji in rankings[:12]:
            all_teams.add(team)
    
    # Create lookup dictionaries for each system
    system_lookups = {}
    for system_name, rankings in systems.items():
        system_lookups[system_name] = {team: (elo, rank+1) for rank, (team, elo, emoji) in enumerate(rankings)}
    
    # Sort teams by best ranking across all systems
    team_best_ranks = {}
    for team in all_teams:
        ranks = []
        for system_name in systems.keys():
            if team in system_lookups[system_name]:
                ranks.append(system_lookups[system_name][team][1])
            else:
                ranks.append(999)
        team_best_ranks[team] = min(ranks)
    
    sorted_teams = sorted(all_teams, key=lambda x: team_best_ranks[x])
    
    for team in sorted_teams[:12]:
        # Get rankings from each system
        orig_elo, orig_rank = system_lookups["Original (Full, K↓)"].get(team, (0, 999))
        k2025_elo, k2025_rank = system_lookups["2025-Only (K↓)"].get(team, (0, 999))
        f2025_elo, f2025_rank = system_lookups["2025-Only (K=20)"].get(team, (0, 999))
        full_elo, full_rank = system_lookups["Full Season (K=20)"].get(team, (0, 999))
        adapt_elo, adapt_rank = system_lookups["Adaptive K (15→25)"].get(team, (0, 999))
        
        all_ranks = [orig_rank, k2025_rank, f2025_rank, full_rank, adapt_rank]
        valid_ranks = [r for r in all_ranks if r < 999]
        best_rank = min(valid_ranks) if valid_ranks else 999
        worst_rank = max(valid_ranks) if valid_ranks else 999
        
        # Format rankings
        orig_str = f"#{orig_rank}" if orig_rank < 999 else "---"
        k2025_str = f"#{k2025_rank}" if k2025_rank < 999 else "---"
        f2025_str = f"#{f2025_rank}" if f2025_rank < 999 else "---"
        full_str = f"#{full_rank}" if full_rank < 999 else "---"
        adapt_str = f"#{adapt_rank}" if adapt_rank < 999 else "---"
        
        print(f"{team:<25} {orig_str:<8} {k2025_str:<8} {f2025_str:<9} {full_str:<9} {adapt_str:<8} #{best_rank:<5} #{worst_rank}")

    # Key insights
    print(f"\n{'🎯 ULTIMATE INSIGHTS ACROSS ALL SYSTEMS':^110}")
    print("="*110)
    
    insights = [
        ("🏆 Oklahoma City Thunder", "DOMINANT #1 in ALL 5 systems", "Undisputed best team"),
        ("📈 Indiana Pacers", "MASSIVE variance: #5 → #2 → #4", "System choice critical"),
        ("🥇 Cleveland Cavaliers", "Strong but varies: #2 → #5 → #3", "Early season strength"),
        ("🥈 Boston Celtics", "Consistent top 4, improved in adaptive", "Steady excellence"), 
        ("🔥 Minnesota Timberwolves", "Steady #3-5 range across all", "Reliable performance"),
        ("🗽 New York Knicks", "Best in original (#8), worst in recent", "Early season helped"),
        ("👑 Golden State Warriors", "Very consistent across systems", "Steady contributor"),
    ]
    
    for team, variance, note in insights:
        print(f"• {team:<25} {variance:<35} {note}")

    # Statistical comparison
    print(f"\n{'STATISTICAL COMPARISON':^110}")
    print("="*110)
    
    stats = [
        ("System", "Logic", "Games", "Highest", "Range", "Thunder", "Pacers", "P-Rank"),
        ("-" * 15, "-" * 20, "-" * 8, "-" * 8, "-" * 8, "-" * 8, "-" * 8, "-" * 6),
        ("Original", "K40→10, full season", "1,386", "1286.2", "~545", "1286.2", "1146.9", "#5"),
        ("2025-K↓", "K40→10, recent only", "834", "1248.8", "463.4", "1248.8", "1146.8", "#5"),
        ("2025-K20", "K20 fixed, recent", "834", "1213.7", "387.0", "1213.7", "1131.8", "#2"),
        ("Full-K20", "K20 fixed, full", "1,386", "1255.9", "483.9", "1255.9", "1139.5", "#5"),
        ("Adaptive", "K15→25 by year", "1,386", "1264.3", "497.8", "1264.3", "1158.4", "#4"),
    ]
    
    for row in stats:
        print(f"{row[0]:<15} {row[1]:<20} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[5]:<8} {row[6]:<8} {row[7]:<6}")

    # System recommendations
    print(f"\n{'🔬 ULTIMATE SYSTEM RECOMMENDATIONS':^110}")
    print("="*110)
    print("🏆 FOR CHAMPIONSHIP PREDICTION:")
    print("   → Use 'Adaptive K (15→25)' - balances full data with recency emphasis")
    print()
    print("📈 FOR SEASON REVIEW:")
    print("   → Use 'Original (Full, K↓)' - rewards consistency over time")
    print()
    print("⚡ FOR CURRENT FORM:")
    print("   → Use '2025-Only (K=20)' - pure recent performance")
    print()
    print("🏀 FOR BALANCED ANALYSIS:")
    print("   → Use 'Full Season (K=20)' - equal weight to all games")
    print()
    print("🎯 FOR TRENDING ANALYSIS:")
    print("   → Use '2025-Only (K↓)' - recent with some stability")
    
    print(f"\n{'='*110}")
    print(f"{'✅ ULTIMATE COMPARISON COMPLETE':^110}")
    print(f"{'='*110}")
    print("🏆 Thunder absolutely dominates - #1 in ALL five systems!")
    print("📈 Pacers most volatile - ranking varies dramatically by system")
    print("🎯 Adaptive K system appears most balanced for predictions")
    print("⚖️  System choice has MASSIVE impact on team evaluation!")

if __name__ == "__main__":
    main() 