#!/usr/bin/env python3
"""
NBA Elo 2025 Comparison - Beautiful display comparing full season vs 2025-only
"""

def print_2025_summary():
    """Print the 2025-only Elo results with nice formatting"""
    
    # 2025-only rankings (from our calculation)
    rankings_2025 = [
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
        ("Los Angeles Lakers", 1067.0, "👑"),
        ("New York Knicks", 1064.9, "🗽"),
        ("Detroit Pistons", 1061.6, "🔧"),
        ("Portland Trail Blazers", 1020.7, "🌲"),
        ("Chicago Bulls", 1009.1, "🐂"),
        ("Memphis Grizzlies", 1006.2, "🐻"),
        ("Sacramento Kings", 988.5, "👑"),
        ("Orlando Magic", 979.5, "✨"),
        ("Miami Heat", 958.4, "🔥"),
        ("Atlanta Hawks", 946.2, "🦅"),
        ("Phoenix Suns", 941.7, "☀️"),
        ("Toronto Raptors", 936.2, "🦖"),
        ("San Antonio Spurs", 919.7, "⚡"),
        ("Dallas Mavericks", 913.3, "🐴"),
        ("New Orleans Pelicans", 868.9, "🦢"),
        ("Brooklyn Nets", 841.4, "🕸️"),
        ("Utah Jazz", 811.2, "🎵"),
        ("Philadelphia 76ers", 796.1, "🔔"),
        ("Charlotte Hornets", 790.8, "🐝"),
        ("Washington Wizards", 785.4, "🧙"),
    ]
    
    # Full season rankings for comparison
    full_season = [
        ("Oklahoma City Thunder", 1286.2),
        ("Cleveland Cavaliers", 1196.4),
        ("Boston Celtics", 1184.6),
        ("Minnesota Timberwolves", 1154.2),
        ("Indiana Pacers", 1146.9),
        ("LA Clippers", 1118.9),
        ("Denver Nuggets", 1111.0),
        ("New York Knicks", 1097.1),
        ("Houston Rockets", 1095.4),
        ("Golden State Warriors", 1085.8),
        ("Milwaukee Bucks", 1072.1),
        ("Los Angeles Lakers", 1064.4),
    ]
    
    print("🏀 NBA ELO COMPARISON - 2025 GAMES ONLY vs FULL SEASON")
    print("="*80)
    print("📊 METHODOLOGY:")
    print("• 2025 Only: 834 games from Jan 1 - Jun 6, 2025")
    print("• All teams reset to 1,000 Elo at start of 2025")
    print("• Same decreasing K-factor (40→10) and margin scaling")
    print("="*80)
    
    print(f"\n{'2025-ONLY ELO RANKINGS':^80}")
    print("="*80)
    print(f"{'Rank':<4} {'Team':<30} {'2025 Elo':<10} {'Full Season':<12} {'Diff':<8}")
    print("-"*80)
    
    # Create lookup for full season rankings
    full_season_dict = {team: elo for team, elo in full_season}
    
    for rank, (team, elo_2025, emoji) in enumerate(rankings_2025[:15], 1):
        full_elo = full_season_dict.get(team, 0)
        diff = elo_2025 - full_elo if full_elo > 0 else 0
        diff_str = f"{diff:+.1f}" if diff != 0 else "N/A"
        
        print(f"{rank:<4} {emoji} {team:<27} {elo_2025:>8.1f} {full_elo:>10.1f} {diff_str:>7}")

def print_key_differences():
    """Print key differences between full season and 2025-only"""
    
    print(f"\n{'KEY DIFFERENCES - 2025 vs FULL SEASON':^80}")
    print("="*80)
    
    differences = [
        ("Oklahoma City Thunder", "Still #1", "🏆 Dominant in both", "1248.8 vs 1286.2"),
        ("Minnesota Timberwolves", "Rank 3→4", "🔥 Higher in 2025-only", "1150.8 vs 1154.2"),
        ("Boston Celtics", "Rank 3→4", "🥈 Nearly tied with MIN", "1150.8 vs 1184.6"),
        ("Indiana Pacers", "Consistent", "📈 Strong in both periods", "1146.8 vs 1146.9"),
        ("Golden State Warriors", "Rank 10→8", "👑 Better 2025 performance", "1084.7 vs 1085.8"),
        ("New York Knicks", "Rank 8→12", "🗽 Weaker in 2025-only", "1064.9 vs 1097.1"),
    ]
    
    for team, change, note, scores in differences:
        print(f"• {team:<25} {change:<15} {note:<25} ({scores})")

def print_conference_comparison():
    """Print conference strength comparison"""
    
    print(f"\n{'CONFERENCE STRENGTH COMPARISON':^80}")
    print("="*80)
    
    # 2025 data
    east_2025 = 979.5
    west_2025 = 1020.5
    advantage_2025 = west_2025 - east_2025
    
    # Full season data  
    east_full = 979.0
    west_full = 1023.9
    advantage_full = west_full - east_full
    
    print(f"{'Metric':<30} {'2025-Only':<15} {'Full Season':<15} {'Difference'}")
    print("-"*80)
    print(f"{'Eastern Conference Avg':<30} {east_2025:<15.1f} {east_full:<15.1f} {east_2025-east_full:+.1f}")
    print(f"{'Western Conference Avg':<30} {west_2025:<15.1f} {west_full:<15.1f} {west_2025-west_full:+.1f}")
    print(f"{'Western Advantage':<30} {advantage_2025:<15.1f} {advantage_full:<15.1f} {advantage_2025-advantage_full:+.1f}")

def print_insights():
    """Print key insights from 2025-only analysis"""
    
    print(f"\n{'🎯 KEY INSIGHTS - 2025 GAMES ONLY':^80}")
    print("="*80)
    print("🏆 Oklahoma City Thunder: Still the clear #1 team (1248.8 Elo)")
    print("🔥 Minnesota Timberwolves: Virtually tied with Boston for #3")
    print("👑 Golden State Warriors: Moved up 2 spots in 2025-only rankings")
    print("🗽 New York Knicks: Dropped 4 spots without early season boost")
    print("⚖️  Conference Balance: Western advantage slightly reduced")
    print("📊 Elo Range: Tighter spread (463 vs 545 points)")
    print("📈 Sample Size: 834 games vs 1,386 full season games")
    print("🎮 Latest Game Impact: IND 111-110 OKC on June 6, 2025")

def main():
    print_2025_summary()
    print_key_differences()
    print_conference_comparison()
    print_insights()
    
    print(f"\n{'='*80}")
    print(f"{'✅ 2025-ONLY ANALYSIS COMPLETE':^80}")
    print(f"{'='*80}")
    print("📊 Shows how team strengths evolved during 2025 calendar year")
    print("🏀 Demonstrates impact of starting fresh vs cumulative ratings")
    print("⚡ Highlights which teams dominated the 2025 portion of season")

if __name__ == "__main__":
    main() 