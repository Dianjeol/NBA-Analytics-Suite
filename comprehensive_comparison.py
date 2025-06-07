#!/usr/bin/env python3
"""
NBA Comprehensive Elo System Comparison
Compares all four different Elo calculation methods
"""

def main():
    # All four systems we've calculated
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
        ]
    }
    
    print("🏀 COMPREHENSIVE NBA ELO SYSTEM COMPARISON")
    print("="*100)
    print("📊 FOUR DIFFERENT CALCULATION METHODS:")
    print("1. Original (Full, K↓):     Full season, K=40→10 decreasing")
    print("2. 2025-Only (K↓):         2025 games only, K=40→10 decreasing") 
    print("3. 2025-Only (K=20):       2025 games only, K=20 fixed")
    print("4. Full Season (K=20):     Full season, K=20 fixed")
    print("="*100)
    
    # Create comprehensive ranking table
    print(f"\n{'COMPREHENSIVE RANKING TABLE (Top 12)':^100}")
    print("="*100)
    print(f"{'Team':<25} {'Original':<12} {'2025-K↓':<12} {'2025-K20':<12} {'Full-K20':<12} {'Best Rank':<10}")
    print("-"*100)
    
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
        
        best_rank = min([orig_rank, k2025_rank, f2025_rank, full_rank])
        
        # Format rankings
        orig_str = f"#{orig_rank}" if orig_rank < 999 else "---"
        k2025_str = f"#{k2025_rank}" if k2025_rank < 999 else "---"
        f2025_str = f"#{f2025_rank}" if f2025_rank < 999 else "---"
        full_str = f"#{full_rank}" if full_rank < 999 else "---"
        
        print(f"{team:<25} {orig_str:<12} {k2025_str:<12} {f2025_str:<12} {full_str:<12} #{best_rank}")

    # Key insights
    print(f"\n{'🎯 KEY INSIGHTS ACROSS ALL SYSTEMS':^100}")
    print("="*100)
    
    insights = [
        ("🏆 Oklahoma City Thunder", "Dominant #1 in ALL systems", "Consistently elite"),
        ("📈 Indiana Pacers", "HUGE variance: #5 → #2 → #5", "Benefits from fixed K systems"),
        ("🥇 Cleveland Cavaliers", "Strong but declining: #2 → #5 → #2", "Early season strength"),
        ("🥈 Boston Celtics", "Consistent top 4 in all systems", "Reliable performance"),
        ("🔥 Minnesota Timberwolves", "Steady #3-4 range", "Consistent throughout"),
        ("🗽 New York Knicks", "Best in original system (#8)", "Early season helped them"),
        ("👑 Golden State Warriors", "Similar across all systems", "Steady performer"),
    ]
    
    for team, variance, note in insights:
        print(f"• {team:<25} {variance:<35} {note}")

    # Statistical comparison
    print(f"\n{'STATISTICAL COMPARISON':^100}")
    print("="*100)
    
    stats = [
        ("System", "Games", "Highest", "Lowest", "Range", "East Avg", "West Avg"),
        ("-" * 20, "-" * 8, "-" * 8, "-" * 8, "-" * 8, "-" * 8, "-" * 8),
        ("Original (Full, K↓)", "1,386", "1286.2", "~740", "~545", "979.0", "1023.9"),
        ("2025-Only (K↓)", "834", "1248.8", "785.4", "463.4", "979.5", "1020.5"),
        ("2025-Only (K=20)", "834", "1213.7", "826.7", "387.0", "985.0", "1015.0"),
        ("Full Season (K=20)", "1,386", "1255.9", "772.0", "483.9", "982.4", "1019.1"),
    ]
    
    for row in stats:
        print(f"{row[0]:<20} {row[1]:<8} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[5]:<8} {row[6]:<8}")

    # System recommendations
    print(f"\n{'🔬 SYSTEM RECOMMENDATIONS':^100}")
    print("="*100)
    print("📈 FOR SEASON-LONG ANALYSIS:")
    print("   → Use 'Original (Full, K↓)' - rewards consistency, stabilizes over time")
    print()
    print("⚡ FOR CURRENT FORM:")
    print("   → Use '2025-Only (K=20)' - equal weight to recent games")
    print()
    print("🏀 FOR BALANCED VIEW:")
    print("   → Use 'Full Season (K=20)' - complete data, equal weighting")
    print()
    print("🎯 FOR RECENCY BIAS:")
    print("   → Use '2025-Only (K↓)' - recent games but still some stability")
    
    print(f"\n{'='*100}")
    print(f"{'✅ COMPREHENSIVE COMPARISON COMPLETE':^100}")
    print(f"{'='*100}")
    print("🏆 Thunder dominates all systems - clearly the best team")
    print("📈 Pacers benefit most from equal weighting systems")
    print("⚖️  Choice of system significantly impacts team rankings!")

if __name__ == "__main__":
    main() 