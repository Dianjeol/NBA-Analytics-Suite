#!/usr/bin/env python3
"""
NBA Elo Visualizer - Creates detailed displays and exports data
"""

import json
import csv
from datetime import datetime
from collections import defaultdict

def load_games():
    """Load games from JSON file"""
    with open('nba_2024_games.json', 'r') as f:
        data = json.load(f)
    
    games = []
    for game in data['response']:
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
    
    games.sort(key=lambda x: x['date'])
    return games

def create_conference_divisions():
    """Create team conference and division mappings"""
    # NBA team divisions (2024 season)
    divisions = {
        # Eastern Conference
        'Atlantic': ['Boston Celtics', 'Brooklyn Nets', 'New York Knicks', 'Philadelphia 76ers', 'Toronto Raptors'],
        'Central': ['Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks'],
        'Southeast': ['Atlanta Hawks', 'Charlotte Hornets', 'Miami Heat', 'Orlando Magic', 'Washington Wizards'],
        
        # Western Conference  
        'Northwest': ['Denver Nuggets', 'Minnesota Timberwolves', 'Oklahoma City Thunder', 'Portland Trail Blazers', 'Utah Jazz'],
        'Pacific': ['Golden State Warriors', 'LA Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings'],
        'Southwest': ['Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Pelicans', 'San Antonio Spurs']
    }
    
    team_divisions = {}
    for division, teams in divisions.items():
        for team in teams:
            team_divisions[team] = division
    
    conferences = {
        'Eastern': ['Atlantic', 'Central', 'Southeast'],
        'Western': ['Northwest', 'Pacific', 'Southwest']
    }
    
    team_conferences = {}
    for conference, divs in conferences.items():
        for div in divs:
            for team in divisions.get(div, []):
                team_conferences[team] = conference
                
    return team_divisions, team_conferences

def calculate_detailed_elo():
    """Calculate Elo with detailed tracking"""
    games = load_games()
    
    # Initialize
    elos = defaultdict(lambda: 1000.0)
    elo_history = defaultdict(list)
    
    regular_season_games = [g for g in games if g['stage'] <= 2]
    playoff_games = [g for g in games if g['stage'] == 3]
    
    # Process regular season
    for i, game in enumerate(regular_season_games):
        # Calculate K-factor (decreasing over time)
        progress = i / len(regular_season_games)
        k = 40 * (1 - progress * 0.75) + 10 * progress * 0.75
        k = max(k, 10)
        
        # Update Elo
        home_elo = elos[game['home_team']]
        away_elo = elos[game['visitor_team']]
        
        # Expected scores
        home_expected = 1 / (1 + 10**((away_elo - home_elo) / 400))
        away_expected = 1 - home_expected
        
        # Actual results
        if game['home_score'] > game['visitor_score']:
            home_actual, away_actual = 1, 0
        else:
            home_actual, away_actual = 0, 1
            
        # Margin of victory multiplier
        import math
        score_diff = abs(game['home_score'] - game['visitor_score'])
        mov_multiplier = math.log(score_diff + 1) / math.log(20)
        
        # Update
        elos[game['home_team']] += k * mov_multiplier * (home_actual - home_expected)
        elos[game['visitor_team']] += k * mov_multiplier * (away_actual - away_expected)
        
        # Store history
        elo_history[game['home_team']].append({
            'date': game['date'],
            'elo': elos[game['home_team']],
            'stage': 'Regular Season'
        })
        elo_history[game['visitor_team']].append({
            'date': game['date'],
            'elo': elos[game['visitor_team']],
            'stage': 'Regular Season'
        })
    
    regular_season_elos = dict(elos)
    
    # Process playoffs
    for i, game in enumerate(playoff_games):
        progress = (len(regular_season_games) + i) / len(games)
        k = 40 * (1 - progress * 0.75) + 10 * progress * 0.75
        k = max(k, 10)
        
        home_elo = elos[game['home_team']]
        away_elo = elos[game['visitor_team']]
        
        home_expected = 1 / (1 + 10**((away_elo - home_elo) / 400))
        away_expected = 1 - home_expected
        
        if game['home_score'] > game['visitor_score']:
            home_actual, away_actual = 1, 0
        else:
            home_actual, away_actual = 0, 1
            
        import math
        score_diff = abs(game['home_score'] - game['visitor_score'])
        mov_multiplier = math.log(score_diff + 1) / math.log(20)
        
        elos[game['home_team']] += k * mov_multiplier * (home_actual - home_expected)
        elos[game['visitor_team']] += k * mov_multiplier * (away_actual - away_expected)
        
        elo_history[game['home_team']].append({
            'date': game['date'],
            'elo': elos[game['home_team']],
            'stage': 'Playoffs'
        })
        elo_history[game['visitor_team']].append({
            'date': game['date'],
            'elo': elos[game['visitor_team']],
            'stage': 'Playoffs'
        })
    
    return dict(elos), regular_season_elos, elo_history

def display_conference_rankings(final_elos, regular_elos):
    """Display rankings by conference and division"""
    team_divisions, team_conferences = create_conference_divisions()
    
    # Group teams by conference
    east_teams = []
    west_teams = []
    other_teams = []
    
    for team, elo in final_elos.items():
        conf = team_conferences.get(team)
        div = team_divisions.get(team, 'Unknown')
        reg_elo = regular_elos.get(team, 1000)
        change = elo - reg_elo
        
        team_data = {
            'team': team,
            'elo': elo,
            'division': div,
            'change': change
        }
        
        if conf == 'Eastern':
            east_teams.append(team_data)
        elif conf == 'Western':
            west_teams.append(team_data)
        else:
            other_teams.append(team_data)
    
    # Sort by Elo
    east_teams.sort(key=lambda x: x['elo'], reverse=True)
    west_teams.sort(key=lambda x: x['elo'], reverse=True)
    other_teams.sort(key=lambda x: x['elo'], reverse=True)
    
    print(f"\n{'='*80}")
    print(f"{'EASTERN CONFERENCE - FINAL ELO RANKINGS':^80}")
    print(f"{'='*80}")
    print(f"{'Rank':<4} {'Team':<25} {'Division':<12} {'Elo':<8} {'Playoff Δ':<10}")
    print(f"{'-'*80}")
    
    for i, team_data in enumerate(east_teams, 1):
        change_str = f"+{team_data['change']:.1f}" if team_data['change'] >= 0 else f"{team_data['change']:.1f}"
        print(f"{i:<4} {team_data['team']:<25} {team_data['division']:<12} {team_data['elo']:>7.1f} {change_str:>9}")
    
    print(f"\n{'='*80}")
    print(f"{'WESTERN CONFERENCE - FINAL ELO RANKINGS':^80}")
    print(f"{'='*80}")
    print(f"{'Rank':<4} {'Team':<25} {'Division':<12} {'Elo':<8} {'Playoff Δ':<10}")
    print(f"{'-'*80}")
    
    for i, team_data in enumerate(west_teams, 1):
        change_str = f"+{team_data['change']:.1f}" if team_data['change'] >= 0 else f"{team_data['change']:.1f}"
        print(f"{i:<4} {team_data['team']:<25} {team_data['division']:<12} {team_data['elo']:>7.1f} {change_str:>9}")
    
    if other_teams:
        print(f"\n{'='*80}")
        print(f"{'OTHER TEAMS':^80}")
        print(f"{'='*80}")
        for i, team_data in enumerate(other_teams, 1):
            change_str = f"+{team_data['change']:.1f}" if team_data['change'] >= 0 else f"{team_data['change']:.1f}"
            print(f"{i:<4} {team_data['team']:<25} {'N/A':<12} {team_data['elo']:>7.1f} {change_str:>9}")

def save_to_csv(final_elos, regular_elos):
    """Save results to CSV files"""
    team_divisions, team_conferences = create_conference_divisions()
    
    # Prepare data
    csv_data = []
    for team, final_elo in final_elos.items():
        regular_elo = regular_elos.get(team, 1000)
        change = final_elo - regular_elo
        
        csv_data.append({
            'Team': team,
            'Conference': team_conferences.get(team, 'Unknown'),
            'Division': team_divisions.get(team, 'Unknown'),
            'Regular_Season_Elo': round(regular_elo, 1),
            'Final_Elo': round(final_elo, 1),
            'Playoff_Change': round(change, 1),
            'Overall_Rank': 0  # Will be filled after sorting
        })
    
    # Sort and add rankings
    csv_data.sort(key=lambda x: x['Final_Elo'], reverse=True)
    for i, row in enumerate(csv_data, 1):
        row['Overall_Rank'] = i
    
    # Save to CSV
    with open('nba_2024_elo_ratings.csv', 'w', newline='') as f:
        fieldnames = ['Overall_Rank', 'Team', 'Conference', 'Division', 
                     'Regular_Season_Elo', 'Final_Elo', 'Playoff_Change']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"\n✅ Elo ratings saved to 'nba_2024_elo_ratings.csv'")

def main():
    print("🏀 NBA Elo Detailed Analysis - 2024 Season")
    print("Calculating detailed Elo ratings...")
    
    final_elos, regular_elos, elo_history = calculate_detailed_elo()
    
    # Display conference rankings
    display_conference_rankings(final_elos, regular_elos)
    
    # Save to CSV
    save_to_csv(final_elos, regular_elos)
    
    # Summary statistics
    print(f"\n{'='*80}")
    print(f"{'SUMMARY STATISTICS':^80}")
    print(f"{'='*80}")
    
    total_teams = len(final_elos)
    avg_elo = sum(final_elos.values()) / total_teams
    max_team = max(final_elos.items(), key=lambda x: x[1])
    min_team = min(final_elos.items(), key=lambda x: x[1])
    
    print(f"Total Teams Analyzed: {total_teams}")
    print(f"Average Final Elo: {avg_elo:.1f}")
    print(f"Highest Elo: {max_team[0]} ({max_team[1]:.1f})")
    print(f"Lowest Elo: {min_team[0]} ({min_team[1]:.1f})")
    print(f"Elo Range: {max_team[1] - min_team[1]:.1f} points")
    
    # Playoff performance analysis
    playoff_changes = []
    for team in final_elos:
        if team in regular_elos:
            change = final_elos[team] - regular_elos[team]
            playoff_changes.append((team, change))
    
    playoff_changes.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 5 Playoff Performers:")
    for team, change in playoff_changes[:5]:
        print(f"  {team}: +{change:.1f}")
    
    print(f"\nWorst 5 Playoff Performers:")
    for team, change in playoff_changes[-5:]:
        print(f"  {team}: {change:.1f}")

if __name__ == "__main__":
    main() 