#!/usr/bin/env python3
"""
NBA Analytics Suite Web Application
A comprehensive web interface for NBA statistical analysis, betting market analysis, and visualizations
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import math
import os
from datetime import datetime
from collections import defaultdict
from season_manager import SeasonManager
from betting_market_vs_models import FinalsAnalyzer, ModelType, BettingOddsConverter
from nba_visualization import NBAVisualization
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Initialize Flask app with production-ready configuration
app = Flask(__name__)

# Initialize modules
season_manager = SeasonManager()
visualizer = NBAVisualization()

# Security configuration using environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Optional: Database configuration (if you add a database later)
# app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')

# CORS and security headers for production
@app.after_request
def after_request(response):
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # CORS headers (adjust origin as needed)
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*')
    response.headers['Access-Control-Allow-Origin'] = allowed_origins
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    return response

class EloCalculator:
    def __init__(self, initial_elo=1000, k_factor_type='fixed', k_factor_value=20):
        self.initial_elo = initial_elo
        self.k_factor_type = k_factor_type
        self.k_factor_value = k_factor_value
        self.team_elos = defaultdict(lambda: initial_elo)
        self.team_records = defaultdict(lambda: {'wins': 0, 'losses': 0})
        self.game_count = 0
        self.elo_history = defaultdict(list)
    
    def get_k_factor(self, game_number, total_games):
        """Get K-factor based on type and game progression"""
        if self.k_factor_type == 'fixed':
            return self.k_factor_value
        elif self.k_factor_type == 'decreasing':
            # K-factor decreases from 40 to 10 over the season
            progress = game_number / total_games
            return 40 - (30 * progress)
        return 20
    
    def expected_score(self, rating_a, rating_b):
        """Calculate expected score for team A against team B"""
        return 1 / (1 + 10**((rating_b - rating_a) / 400))
    
    def update_elo(self, team_a, team_b, score_a, score_b, game_number, total_games):
        """Update Elo ratings based on game result"""
        rating_a = self.team_elos[team_a]
        rating_b = self.team_elos[team_b]
        
        # Determine actual score (1 for win, 0 for loss) and update records
        if score_a > score_b:
            actual_a, actual_b = 1, 0
            self.team_records[team_a]['wins'] += 1
            self.team_records[team_b]['losses'] += 1
        else:
            actual_a, actual_b = 0, 1
            self.team_records[team_b]['wins'] += 1
            self.team_records[team_a]['losses'] += 1
            
        # Calculate expected scores
        expected_a = self.expected_score(rating_a, rating_b)
        expected_b = self.expected_score(rating_b, rating_a)
        
        # Apply margin of victory multiplier
        score_diff = abs(score_a - score_b)
        mov_multiplier = math.log(score_diff + 1) / math.log(20)
        
        # Get K-factor for this game
        k_factor = self.get_k_factor(game_number, total_games)
        
        # Update ratings
        new_rating_a = rating_a + k_factor * mov_multiplier * (actual_a - expected_a)
        new_rating_b = rating_b + k_factor * mov_multiplier * (actual_b - expected_b)
        
        self.team_elos[team_a] = new_rating_a
        self.team_elos[team_b] = new_rating_b
        
        # Store history
        self.elo_history[team_a].append({'game': game_number, 'elo': new_rating_a, 'date': datetime.now().isoformat()})
        self.elo_history[team_b].append({'game': game_number, 'elo': new_rating_b, 'date': datetime.now().isoformat()})
        
        return new_rating_a, new_rating_b

def load_games_data(season=None):
    """Load NBA games data for specified season"""
    try:
        # Use season manager to get correct data file
        if season:
            filename = f'nba_{season}_games.json'
        else:
            filename = 'nba_2024_games.json'  # Default fallback
            
        with open(filename, 'r') as f:
            data = json.load(f)
        
        all_games = []
        for game in data['response']:
            # Only process finished games with valid scores, exclude preseason
            if (game['status']['short'] == 3 and 
                game['scores']['home']['points'] is not None and 
                game['scores']['visitors']['points'] is not None and
                game['stage'] != 1):  # Stage 1 = Preseason, 2 = Regular Season, 3+ = Playoffs
                
                game_date = datetime.fromisoformat(game['date']['start'].replace('Z', '+00:00'))
                
                all_games.append({
                    'id': game['id'],
                    'date': game_date,
                    'stage': game['stage'],
                    'home_team': game['teams']['home']['name'],
                    'visitor_team': game['teams']['visitors']['name'],
                    'home_score': int(game['scores']['home']['points']),
                    'visitor_score': int(game['scores']['visitors']['points'])
                })
        
        all_games.sort(key=lambda x: x['date'])
        return all_games
    except FileNotFoundError:
        return []

def get_team_conferences():
    """Get team conference mappings"""
    divisions = {
        'Atlantic': ['Boston Celtics', 'Brooklyn Nets', 'New York Knicks', 'Philadelphia 76ers', 'Toronto Raptors'],
        'Central': ['Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks'],
        'Southeast': ['Atlanta Hawks', 'Charlotte Hornets', 'Miami Heat', 'Orlando Magic', 'Washington Wizards'],
        'Northwest': ['Denver Nuggets', 'Minnesota Timberwolves', 'Oklahoma City Thunder', 'Portland Trail Blazers', 'Utah Jazz'],
        'Pacific': ['Golden State Warriors', 'LA Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings'],
        'Southwest': ['Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Pelicans', 'San Antonio Spurs']
    }
    
    team_conferences = {}
    for conf in ['Eastern', 'Western']:
        div_list = ['Atlantic', 'Central', 'Southeast'] if conf == 'Eastern' else ['Northwest', 'Pacific', 'Southwest']
        for div in div_list:
            for team in divisions.get(div, []):
                team_conferences[team] = conf
    
    return team_conferences

def calculate_win_probability(elo_a, elo_b, home_advantage=0):
    """Calculate win probability between two teams"""
    adjusted_elo_a = elo_a + home_advantage
    prob_a = 1 / (1 + 10**((elo_b - adjusted_elo_a) / 400))
    return prob_a

def calculate_series_probability_nba_format(wins_a, wins_b, prob_a_home, prob_a_away, a_has_home_court=True, games_needed=4):
    """
    Calculate probability that team A wins a best-of-7 NBA playoff series given current standing
    Uses proper 2-2-1-1-1 home court advantage format, accounting for games already played
    wins_a: Current wins for team A
    wins_b: Current wins for team B  
    prob_a_home: Probability team A wins when they have home court
    prob_a_away: Probability team A wins when team B has home court
    a_has_home_court: Whether team A has overall home court advantage (better record)
    games_needed: Games needed to win series (4 for best-of-7)
    """
    if wins_a >= games_needed:
        return 1.0
    if wins_b >= games_needed:
        return 0.0
    
    # NBA playoff format: 2-2-1-1-1
    # Games where higher seed (home court advantage team) is at home: 1, 2, 5, 7
    # Games where lower seed is at home: 3, 4, 6
    higher_seed_home_games = {1, 2, 5, 7}
    
    # Dynamic programming approach
    memo = {}
    
    def dp(a_wins, b_wins, current_game):
        if a_wins >= games_needed:
            return 1.0
        if b_wins >= games_needed:
            return 0.0
        
        if current_game > 7:  # Series can't go beyond 7 games
            return 0.0
        
        if (a_wins, b_wins, current_game) in memo:
            return memo[(a_wins, b_wins, current_game)]
        
        # Determine if team A is playing at home in this specific game
        if a_has_home_court:
            # Team A has home court advantage (higher seed)
            a_at_home = current_game in higher_seed_home_games
        else:
            # Team B has home court advantage (higher seed)
            a_at_home = current_game not in higher_seed_home_games
        
        # Get probability for this specific game
        prob_a_this_game = prob_a_home if a_at_home else prob_a_away
        
        # Team A wins this game OR loses this game
        result = (prob_a_this_game * dp(a_wins + 1, b_wins, current_game + 1) + 
                 (1 - prob_a_this_game) * dp(a_wins, b_wins + 1, current_game + 1))
        
        memo[(a_wins, b_wins, current_game)] = result
        return result
    
    # Start from the next game to be played
    next_game_number = wins_a + wins_b + 1
    return dp(wins_a, wins_b, next_game_number)

def get_remaining_games_breakdown(wins_a, wins_b, a_has_home_court):
    """
    Get breakdown of remaining home/away games for both teams
    """
    games_played = wins_a + wins_b
    higher_seed_home_games = {1, 2, 5, 7}
    
    remaining_games = list(range(games_played + 1, 8))  # Games still to be played
    
    if a_has_home_court:
        # Team A is higher seed
        a_remaining_home = sum(1 for game in remaining_games if game in higher_seed_home_games)
        a_remaining_away = len(remaining_games) - a_remaining_home
        b_remaining_home = a_remaining_away
        b_remaining_away = a_remaining_home
    else:
        # Team B is higher seed
        a_remaining_home = sum(1 for game in remaining_games if game not in higher_seed_home_games)
        a_remaining_away = len(remaining_games) - a_remaining_home
        b_remaining_home = a_remaining_away
        b_remaining_away = a_remaining_home
    
    return {
        'a_remaining_home': a_remaining_home,
        'a_remaining_away': a_remaining_away,
        'b_remaining_home': b_remaining_home,
        'b_remaining_away': b_remaining_away,
        'remaining_games': remaining_games
    }

@app.route('/')
def index():
    """Main dashboard with all analytics tools"""
    # Update seasons on each request
    season_manager.update_seasons()
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_elo():
    """Calculate Elo ratings with optional season selection"""
    try:
        data = request.json
        k_factor_type = data.get('k_factor_type', 'fixed')
        k_factor_value = int(data.get('k_factor_value', 20))
        date_filter = data.get('date_filter', 'full_season')
        selected_season = data.get('season', None)
        
        # Load games for selected season
        all_games = load_games_data(selected_season)
        
        if not all_games:
            return jsonify({'error': 'No game data available for selected season'}), 400
        
        # Apply date filter logic
        if date_filter == "2025_only":
            filtered_games = [game for game in all_games if game['date'].year == 2025]
        else:
            filtered_games = all_games
        
        if not filtered_games:
            return jsonify({'error': 'No games found for selected period'}), 400
        
        # Initialize calculator and process games
        calculator = EloCalculator(k_factor_type=k_factor_type, k_factor_value=k_factor_value)
        total_games = len(filtered_games)
        
        for i, game in enumerate(filtered_games, 1):
            calculator.update_elo(
                game['home_team'], game['visitor_team'],
                game['home_score'], game['visitor_score'],
                i, total_games
            )
        
        # Prepare results
        team_conferences = get_team_conferences()
        results = []
        
        for team, elo in calculator.team_elos.items():
            record = calculator.team_records[team]
            results.append({
                'team': team,
                'elo': round(elo, 1),
                'wins': record['wins'],
                'losses': record['losses'],
                'conference': team_conferences.get(team, 'Unknown')
            })
        
        results.sort(key=lambda x: x['elo'], reverse=True)
        
        # Calculate statistics
        elos = [r['elo'] for r in results]
        stats = {
            'total_games': total_games,
            'highest_elo': max(elos),
            'lowest_elo': min(elos),
            'average_elo': round(sum(elos) / len(elos), 1),
            'elo_range': max(elos) - min(elos)
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'stats': stats,
            'season': selected_season or season_manager.get_current_season()['season_id']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/win_probability', methods=['POST'])
def win_probability():
    """Calculate win probability between two teams"""
    try:
        data = request.json
        team_a = data.get('team_a')
        team_b = data.get('team_b')
        season = data.get('season', None)
        
        # Calculate current Elo ratings for selected season
        all_games = load_games_data(season)
        
        if not all_games:
            return jsonify({'error': 'No game data available'}), 400
        
        calculator = EloCalculator()
        for i, game in enumerate(all_games, 1):
            calculator.update_elo(
                game['home_team'], game['visitor_team'],
                game['home_score'], game['visitor_score'],
                i, len(all_games)
            )
        
        elo_a = calculator.team_elos[team_a]
        elo_b = calculator.team_elos[team_b]
        
        # Calculate probabilities
        neutral_prob_a = calculate_win_probability(elo_a, elo_b)
        home_prob_a = calculate_win_probability(elo_a, elo_b, home_advantage=65)
        away_prob_a = calculate_win_probability(elo_a, elo_b, home_advantage=-65)
        
        return jsonify({
            'success': True,
            'team_a': team_a,
            'team_b': team_b,
            'elo_a': round(elo_a, 1),
            'elo_b': round(elo_b, 1),
            'neutral_site': {
                'team_a_prob': round(neutral_prob_a * 100, 1),
                'team_b_prob': round((1 - neutral_prob_a) * 100, 1)
            },
            'team_a_home': {
                'team_a_prob': round(home_prob_a * 100, 1),
                'team_b_prob': round((1 - home_prob_a) * 100, 1)
            },
            'team_b_home': {
                'team_a_prob': round(away_prob_a * 100, 1),
                'team_b_prob': round((1 - away_prob_a) * 100, 1)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/series_probability', methods=['POST'])
def series_probability():
    """Calculate best-of-7 NBA playoff series probability given current standing"""
    data = request.json
    
    team_a = data.get('team_a')
    team_b = data.get('team_b')
    elo_a = data.get('elo_a')
    elo_b = data.get('elo_b')
    rank_a = data.get('rank_a')
    rank_b = data.get('rank_b')
    wins_a = data.get('wins_a', 0)
    wins_b = data.get('wins_b', 0)
    
    if not all([team_a, team_b, elo_a, elo_b, rank_a, rank_b]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    if wins_a < 0 or wins_b < 0 or wins_a > 4 or wins_b > 4:
        return jsonify({'error': 'Invalid wins count (must be 0-4)'}), 400
    
    if wins_a >= 4 or wins_b >= 4:
        return jsonify({'error': 'Series is already over'}), 400
    
    # Determine home court advantage based on rankings (better rank = lower number)
    a_has_home_court = rank_a < rank_b
    higher_seed = team_a if a_has_home_court else team_b
    lower_seed = team_b if a_has_home_court else team_a
    
    # Calculate game probabilities for different scenarios
    prob_a_neutral = calculate_win_probability(elo_a, elo_b)
    prob_a_home = calculate_win_probability(elo_a, elo_b, home_advantage=40)
    prob_a_away = calculate_win_probability(elo_a, elo_b, home_advantage=-40)
    
    # Calculate series probability using NBA format
    series_prob_a = calculate_series_probability_nba_format(
        wins_a, wins_b, prob_a_home, prob_a_away, a_has_home_court
    )
    
    # Get remaining games breakdown
    remaining_breakdown = get_remaining_games_breakdown(wins_a, wins_b, a_has_home_court)
    
    return jsonify({
        'team_a': team_a,
        'team_b': team_b,
        'elo_a': elo_a,
        'elo_b': elo_b,
        'rank_a': rank_a,
        'rank_b': rank_b,
        'current_standing': f"{wins_a}-{wins_b}",
        'wins_a': wins_a,
        'wins_b': wins_b,
        'higher_seed': higher_seed,
        'lower_seed': lower_seed,
        'home_court_advantage_team': higher_seed,
        'neutral_prob_a': round(prob_a_neutral * 100, 1),
        'neutral_prob_b': round((1 - prob_a_neutral) * 100, 1),
        'series_prob_a': round(series_prob_a * 100, 1),
        'series_prob_b': round((1 - series_prob_a) * 100, 1),
        'remaining_games': remaining_breakdown['remaining_games'],
        'a_remaining_home': remaining_breakdown['a_remaining_home'],
        'a_remaining_away': remaining_breakdown['a_remaining_away'],
        'b_remaining_home': remaining_breakdown['b_remaining_home'],
        'b_remaining_away': remaining_breakdown['b_remaining_away'],
        'format_explanation': f"NBA 2-2-1-1-1 format: {higher_seed} has home court advantage"
    })

@app.route('/api/teams')
def get_teams():
    """Get list of NBA teams"""
    teams = [
        'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
        'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
        'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
        'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
        'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
        'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'
    ]
    return jsonify({'teams': teams})

@app.route('/api/seasons')
def get_seasons():
    """Get available seasons"""
    season_manager.add_new_season_if_needed()
    seasons = season_manager.get_available_seasons()
    current_season = season_manager.get_current_season()
    
    # Convert seasons to dictionaries for JSON serialization
    seasons_data = [season.to_dict() for season in seasons]
    current_season_data = current_season.to_dict() if current_season else None
    
    return jsonify({
        'seasons': seasons_data,
        'current_season': current_season_data,
        'total_seasons': len(seasons)
    })

@app.route('/api/betting_analysis', methods=['POST'])
def betting_analysis():
    """Perform betting market analysis"""
    try:
        data = request.json
        team_a = data.get('team_a')
        team_b = data.get('team_b')
        series_state = data.get('series_state', '0-0')
        market_odds_a = data.get('market_odds_a')  # American odds
        season = data.get('season', None)
        
        # Calculate current Elo-based probabilities
        all_games = load_games_data(season)
        calculator = EloCalculator()
        
        for i, game in enumerate(all_games, 1):
            calculator.update_elo(
                game['home_team'], game['visitor_team'],
                game['home_score'], game['visitor_score'],
                i, len(all_games)
            )
        
        elo_a = calculator.team_elos[team_a]
        elo_b = calculator.team_elos[team_b]
        
        # Calculate Elo-based probability
        elo_prob_a = calculate_win_probability(elo_a, elo_b) * 100
        
        # Convert market odds to probability
        market_prob_a = BettingOddsConverter.odds_to_probability(market_odds_a)
        
        # Create analyzer and add estimates
        analyzer = FinalsAnalyzer(team_a, team_b, series_state)
        analyzer.add_estimate(ModelType.BETTING_MARKET, market_prob_a)
        analyzer.add_estimate(ModelType.ELO_ADAPTIVE, elo_prob_a)
        
        # Generate analysis
        report = analyzer.generate_comprehensive_report()
        analysis_data = analyzer.export_to_json()
        
        return jsonify({
            'success': True,
            'report': report,
            'market_probability': round(market_prob_a, 1),
            'elo_probability': round(elo_prob_a, 1),
            'analysis': analysis_data,
            'edge_detected': abs(market_prob_a - elo_prob_a) > 5.0  # 5% threshold
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualization', methods=['POST'])
def create_visualization():
    """Generate visualization charts"""
    try:
        data = request.json
        chart_type = data.get('chart_type', 'elo_rankings')
        season = data.get('season', None)
        
        # Load data for selected season
        all_games = load_games_data(season)
        calculator = EloCalculator()
        
        for i, game in enumerate(all_games, 1):
            calculator.update_elo(
                game['home_team'], game['visitor_team'],
                game['home_score'], game['visitor_score'],
                i, len(all_games)
            )
        
        # Prepare data for visualization
        team_data = []
        for team, elo in calculator.team_elos.items():
            record = calculator.team_records[team]
            team_data.append({
                'team': team,
                'elo': elo,
                'wins': record['wins'],
                'losses': record['losses']
            })
        
        # Generate visualization based on type
        if chart_type == 'elo_rankings':
            fig = visualizer.create_elo_rankings_chart(team_data)
        elif chart_type == 'elo_distribution':
            fig = visualizer.create_elo_distribution_chart(team_data)
        elif chart_type == 'conference_comparison':
            fig = visualizer.create_conference_comparison_chart(team_data)
        else:
            return jsonify({'error': 'Unknown chart type'}), 400
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode()
        plt.close(fig)
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'chart_type': chart_type
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # Ensure static and templates directories exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Production-ready server configuration
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🏀 NBA Analytics Suite starting on {host}:{port}")
    print(f"📊 Debug mode: {debug}")
    print(f"🔄 Season manager initialized with {len(season_manager.get_available_seasons())} seasons")
    
    app.run(host=host, port=port, debug=debug) 