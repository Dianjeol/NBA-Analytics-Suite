#!/usr/bin/env python3
"""
Enhanced NBA Elo Rating Calculator with Season Management
========================================================

Multi-season Elo calculation system with automatic season detection
and historical data management.

Author: NBA Analytics Suite
Version: 1.0.0
"""

import json
import math
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from season_manager import SeasonManager

class EnhancedEloCalculator:
    """Enhanced Elo calculator with season management capabilities."""
    
    def __init__(self, initial_elo=1000, initial_k=40, min_k=10):
        self.initial_elo = initial_elo
        self.initial_k = initial_k
        self.min_k = min_k
        self.season_manager = SeasonManager()
        self.current_season_id = None
        self.season_data = {}  # Store data for each season
        
    def initialize_season(self, season_id: Optional[str] = None):
        """Initialize calculator for a specific season."""
        if season_id is None:
            current_season = self.season_manager.get_current_season()
            season_id = current_season.season_id if current_season else "2024-25"
        
        self.current_season_id = season_id
        
        if season_id not in self.season_data:
            self.season_data[season_id] = {
                'team_elos': defaultdict(lambda: self.initial_elo),
                'game_count': 0,
                'elo_history': defaultdict(list),
                'games_processed': []
            }
    
    def get_season_data(self, season_id: Optional[str] = None) -> Dict:
        """Get data for a specific season."""
        season_id = season_id or self.current_season_id
        if season_id not in self.season_data:
            self.initialize_season(season_id)
        return self.season_data[season_id]
    
    def calculate_k_factor(self, game_number: int, total_games: int, is_playoffs: bool = False) -> float:
        """Calculate K-factor based on game progression and stage."""
        base_k = self.initial_k
        
        # Higher K-factor for playoffs
        if is_playoffs:
            base_k *= 1.5
        
        # Decrease K-factor over season progression
        progress = game_number / max(total_games, 1)
        k = base_k * (1 - progress * 0.75) + self.min_k * progress * 0.75
        return max(k, self.min_k)
    
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        """Calculate expected score for team A against team B."""
        return 1 / (1 + 10**((rating_b - rating_a) / 400))
    
    def calculate_mov_multiplier(self, score_diff: int) -> float:
        """Calculate margin of victory multiplier."""
        return math.log(score_diff + 1) / math.log(20)
    
    def update_elo(self, team_a: str, team_b: str, score_a: int, score_b: int, 
                   k_factor: float, season_id: Optional[str] = None) -> Tuple[float, float]:
        """Update Elo ratings for two teams based on game result."""
        season_data = self.get_season_data(season_id)
        
        rating_a = season_data['team_elos'][team_a]
        rating_b = season_data['team_elos'][team_b]
        
        # Determine actual scores
        actual_a = 1 if score_a > score_b else 0
        actual_b = 1 - actual_a
        
        # Calculate expected scores
        expected_a = self.expected_score(rating_a, rating_b)
        expected_b = self.expected_score(rating_b, rating_a)
        
        # Apply margin of victory multiplier
        score_diff = abs(score_a - score_b)
        mov_multiplier = self.calculate_mov_multiplier(score_diff)
        
        # Update ratings
        new_rating_a = rating_a + k_factor * mov_multiplier * (actual_a - expected_a)
        new_rating_b = rating_b + k_factor * mov_multiplier * (actual_b - expected_b)
        
        season_data['team_elos'][team_a] = new_rating_a
        season_data['team_elos'][team_b] = new_rating_b
        
        # Store in history
        season_data['elo_history'][team_a].append(new_rating_a)
        season_data['elo_history'][team_b].append(new_rating_b)
        
        return new_rating_a, new_rating_b
    
    def load_season_games(self, season_id: Optional[str] = None, data_file: Optional[str] = None) -> List[Dict]:
        """Load games for a specific season."""
        if data_file is None:
            # Try to find appropriate data file
            data_files_to_try = [
                'nba_2024_games.json',
                f'nba_{season_id}_games.json' if season_id else None,
                'nba_games.json'
            ]
            
            for file_path in data_files_to_try:
                if file_path:
                    try:
                        return self._load_games_from_file(file_path)
                    except FileNotFoundError:
                        continue
            
            raise FileNotFoundError("No NBA games data file found")
        else:
            return self._load_games_from_file(data_file)
    
    def _load_games_from_file(self, file_path: str) -> List[Dict]:
        """Load games from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            games = []
            for game in data['response']:
                # Only process finished games with valid scores
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
            
            # Sort games by date
            games.sort(key=lambda x: x['date'])
            return games
            
        except Exception as e:
            raise Exception(f"Error loading games from {file_path}: {e}")
    
    def process_season(self, season_id: Optional[str] = None, data_file: Optional[str] = None) -> Dict:
        """Process all games for a season and return results."""
        self.initialize_season(season_id)
        season_data = self.get_season_data(season_id)
        
        print(f"🏀 Processing Season: {season_id or self.current_season_id}")
        
        # Load games
        games = self.load_season_games(season_id, data_file)
        print(f"Loaded {len(games)} finished games")
        
        # Separate games by stage
        regular_season_games = [g for g in games if g['stage'] <= 2]
        playoff_games = [g for g in games if g['stage'] == 3]
        
        print(f"Regular Season: {len(regular_season_games)} games")
        print(f"Playoffs: {len(playoff_games)} games")
        
        # Process regular season
        print("Processing regular season...")
        for i, game in enumerate(regular_season_games):
            k_factor = self.calculate_k_factor(i, len(regular_season_games), False)
            
            self.update_elo(
                game['home_team'], 
                game['visitor_team'],
                game['home_score'], 
                game['visitor_score'],
                k_factor,
                season_id
            )
            season_data['game_count'] += 1
            season_data['games_processed'].append(game)
        
        # Store regular season state
        regular_season_elos = dict(season_data['team_elos'])
        
        # Process playoffs
        if playoff_games:
            print(f"Processing {len(playoff_games)} playoff games...")
            for i, game in enumerate(playoff_games):
                k_factor = self.calculate_k_factor(
                    len(regular_season_games) + i, 
                    len(games),
                    True  # is_playoffs
                )
                
                self.update_elo(
                    game['home_team'], 
                    game['visitor_team'],
                    game['home_score'], 
                    game['visitor_score'],
                    k_factor,
                    season_id
                )
                season_data['game_count'] += 1
                season_data['games_processed'].append(game)
        
        return {
            'season_id': season_id or self.current_season_id,
            'total_games': len(games),
            'regular_season_games': len(regular_season_games),
            'playoff_games': len(playoff_games),
            'final_elos': dict(season_data['team_elos']),
            'regular_season_elos': regular_season_elos
        }
    
    def get_season_rankings(self, season_id: Optional[str] = None) -> List[Tuple[str, float]]:
        """Get team rankings for a season."""
        season_data = self.get_season_data(season_id)
        return sorted(season_data['team_elos'].items(), key=lambda x: x[1], reverse=True)
    
    def compare_seasons(self, season_ids: List[str]) -> Dict:
        """Compare team performance across multiple seasons."""
        comparison = {}
        
        for season_id in season_ids:
            if season_id in self.season_data:
                rankings = self.get_season_rankings(season_id)
                comparison[season_id] = {
                    'rankings': rankings,
                    'top_team': rankings[0] if rankings else None,
                    'average_elo': sum(elo for _, elo in rankings) / len(rankings) if rankings else 0
                }
        
        return comparison
    
    def format_season_display(self, season_id: Optional[str] = None, title: Optional[str] = None) -> str:
        """Format season Elo ratings for display."""
        season_data = self.get_season_data(season_id)
        display_season_id = season_id or self.current_season_id
        
        if title is None:
            title = f"ELO RATINGS - {display_season_id.upper()} SEASON"
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"{title:^60}")
        lines.append("=" * 60)
        lines.append(f"{'Rank':<5} {'Team':<30} {'Elo Rating':<15}")
        lines.append("-" * 60)
        
        rankings = self.get_season_rankings(season_id)
        for rank, (team, elo) in enumerate(rankings, 1):
            lines.append(f"{rank:<5} {team:<30} {elo:>10.1f}")
        
        return "\n".join(lines)

    def get_available_seasons(self) -> List:
        """Get list of available seasons."""
        return self.season_manager.get_available_seasons()

def main():
    """Demonstrate enhanced Elo calculator with season management."""
    print("🏀 Enhanced NBA Elo Calculator with Season Management")
    print("=" * 60)
    
    # Initialize calculator
    calculator = EnhancedEloCalculator()
    
    # Check for new seasons
    if calculator.season_manager.add_new_season_if_needed():
        print("✅ New season detected and added!")
    
    # Show available seasons
    print("\n📅 Available Seasons:")
    for season in calculator.get_available_seasons():
        marker = "→" if season.is_current else " "
        print(f"  {marker} {season.season_id}: {season.display_name}")
    
    # Process current season
    current_season = calculator.season_manager.get_current_season()
    if current_season:
        try:
            print(f"\n🔄 Processing current season: {current_season.season_id}")
            results = calculator.process_season(current_season.season_id)
            
            print("\n" + calculator.format_season_display(current_season.season_id))
            
            print(f"\n📊 Season Statistics:")
            print(f"Total games processed: {results['total_games']}")
            print(f"Regular season: {results['regular_season_games']}")
            print(f"Playoffs: {results['playoff_games']}")
            
            # Show top teams
            final_elos = results['final_elos']
            if final_elos:
                highest_team = max(final_elos.items(), key=lambda x: x[1])
                lowest_team = min(final_elos.items(), key=lambda x: x[1])
                
                print(f"\n🏆 Top Team: {highest_team[0]} ({highest_team[1]:.1f})")
                print(f"📉 Lowest Team: {lowest_team[0]} ({lowest_team[1]:.1f})")
                print(f"📈 Elo Range: {highest_team[1] - lowest_team[1]:.1f} points")
            
        except Exception as e:
            print(f"❌ Error processing season: {e}")
            print("💡 Make sure NBA games data file is available")
    else:
        print("⚠️  No current season found")

if __name__ == "__main__":
    main() 