#!/usr/bin/env python3
"""
NBA Analytics Suite Visualization Module
=======================================

Professional visualization tools for NBA team analysis, Elo ratings, and statistical comparisons.

Author: NBA Analytics Team
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import matplotlib.patches as mpatches

# Set professional styling
plt.style.use('default')
sns.set_palette("husl")

class NBAVisualization:
    """Professional visualization class for NBA analytics."""
    
    def __init__(self):
        """Initialize the visualization class."""
        self.figure_size = (14, 10)
        self.dpi = 300
        self.color_palette = {
            'Eastern': '#E74C3C',
            'Western': '#3498DB',
            'primary': '#2C3E50',
            'secondary': '#95A5A6',
            'accent': '#F39C12'
        }
        
        # NBA team conferences
        self.conferences = {
            'Atlanta Hawks': 'Eastern', 'Boston Celtics': 'Eastern', 'Brooklyn Nets': 'Eastern',
            'Charlotte Hornets': 'Eastern', 'Chicago Bulls': 'Eastern', 'Cleveland Cavaliers': 'Eastern',
            'Detroit Pistons': 'Eastern', 'Indiana Pacers': 'Eastern', 'Miami Heat': 'Eastern',
            'Milwaukee Bucks': 'Eastern', 'New York Knicks': 'Eastern', 'Orlando Magic': 'Eastern',
            'Philadelphia 76ers': 'Eastern', 'Toronto Raptors': 'Eastern', 'Washington Wizards': 'Eastern',
            'Dallas Mavericks': 'Western', 'Denver Nuggets': 'Western', 'Golden State Warriors': 'Western',
            'Houston Rockets': 'Western', 'LA Clippers': 'Western', 'Los Angeles Lakers': 'Western',
            'Memphis Grizzlies': 'Western', 'Minnesota Timberwolves': 'Western', 'New Orleans Pelicans': 'Western',
            'Oklahoma City Thunder': 'Western', 'Phoenix Suns': 'Western', 'Portland Trail Blazers': 'Western',
            'Sacramento Kings': 'Western', 'San Antonio Spurs': 'Western', 'Utah Jazz': 'Western'
        }
    
    def create_elo_rankings_chart(self, team_data: List[Dict], save_path: Optional[str] = None):
        """Create horizontal bar chart of Elo rankings."""
        df = pd.DataFrame(team_data)
        df = df.sort_values('elo', ascending=True)
        
        # Add conference information
        df['conference'] = df['team'].map(self.conferences)
        
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create colors based on conference
        colors = [self.color_palette[conf] for conf in df['conference']]
        
        # Create horizontal bar chart
        bars = ax.barh(df['team'], df['elo'], color=colors, alpha=0.8)
        
        # Customize chart
        ax.set_xlabel('Elo Rating', fontsize=14, fontweight='bold')
        ax.set_title('NBA Team Elo Rankings', fontsize=18, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for i, (bar, elo) in enumerate(zip(bars, df['elo'])):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2,
                   f'{elo:.1f}', ha='left', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def create_elo_distribution_chart(self, team_data: List[Dict], save_path: Optional[str] = None):
        """Create distribution chart showing Elo rating spread."""
        df = pd.DataFrame(team_data)
        df['conference'] = df['team'].map(self.conferences)
        
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Histogram with KDE
        eastern_teams = df[df['conference'] == 'Eastern']['elo']
        western_teams = df[df['conference'] == 'Western']['elo']
        
        ax.hist([eastern_teams, western_teams], bins=12, alpha=0.7, 
                color=[self.color_palette['Eastern'], self.color_palette['Western']],
                label=['Eastern Conference', 'Western Conference'])
        
        ax.set_xlabel('Elo Rating', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Teams', fontsize=12, fontweight='bold')
        ax.set_title('Elo Rating Distribution by Conference', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_conference_comparison_chart(self, team_data: List[Dict], save_path: Optional[str] = None):
        """Create conference comparison visualization."""
        df = pd.DataFrame(team_data)
        df['conference'] = df['team'].map(self.conferences)
        df['win_pct'] = df['wins'] / (df['wins'] + df['losses'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Average Elo by Conference
        conf_stats = df.groupby('conference')['elo'].mean()
        
        bars1 = ax1.bar(conf_stats.index, conf_stats.values, 
                       color=[self.color_palette[conf] for conf in conf_stats.index],
                       alpha=0.8)
        ax1.set_title('Average Elo Rating by Conference', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Elo Rating', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        for bar, mean in zip(bars1, conf_stats.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Top 10 Teams
        top_teams = df.nlargest(10, 'elo')
        colors_top = [self.color_palette[self.conferences[team]] for team in top_teams['team']]
        
        bars2 = ax2.barh(range(len(top_teams)), top_teams['elo'], color=colors_top, alpha=0.8)
        ax2.set_yticks(range(len(top_teams)))
        ax2.set_yticklabels(top_teams['team'], fontsize=10)
        ax2.set_xlabel('Elo Rating', fontsize=12, fontweight='bold')
        ax2.set_title('Top 10 Teams by Elo', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle('NBA Conference Analysis', fontsize=18, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def create_team_performance_radar(self, team_data: List[Dict], top_n: int = 8, 
                                    save_path: Optional[str] = None):
        """Create radar chart for top teams showing multiple metrics."""
        df = pd.DataFrame(team_data)
        df['conference'] = df['team'].map(self.conferences)
        df['win_pct'] = df['wins'] / (df['wins'] + df['losses'])
        
        # Get top teams
        top_teams = df.nlargest(top_n, 'elo')
        
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
        
        # Metrics for radar chart
        metrics = ['Elo Rating', 'Win %', 'Total Wins']
        
        # Normalize metrics to 0-100 scale
        elo_norm = (top_teams['elo'] - df['elo'].min()) / (df['elo'].max() - df['elo'].min()) * 100
        win_pct_norm = top_teams['win_pct'] * 100
        wins_norm = (top_teams['wins'] - df['wins'].min()) / (df['wins'].max() - df['wins'].min()) * 100
        
        # Setup angles
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Colors for each team
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_teams)))
        
        for i, (_, team) in enumerate(top_teams.iterrows()):
            values = [elo_norm.iloc[i], win_pct_norm.iloc[i], wins_norm.iloc[i]]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=team['team'], color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        # Customize chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=12, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.set_title('Top Teams Performance Radar', fontsize=16, fontweight='bold', pad=30)
        ax.grid(True)
        
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            
        return fig


def demo_nba_visualization():
    """Demo function showing visualization capabilities."""
    # Sample team data
    sample_data = [
        {'team': 'Boston Celtics', 'elo': 1650, 'wins': 45, 'losses': 15},
        {'team': 'Oklahoma City Thunder', 'elo': 1620, 'wins': 42, 'losses': 18},
        {'team': 'Denver Nuggets', 'elo': 1580, 'wins': 40, 'losses': 20},
        {'team': 'Phoenix Suns', 'elo': 1560, 'wins': 38, 'losses': 22},
        {'team': 'Milwaukee Bucks', 'elo': 1540, 'wins': 36, 'losses': 24},
        {'team': 'Miami Heat', 'elo': 1520, 'wins': 34, 'losses': 26},
        {'team': 'Golden State Warriors', 'elo': 1500, 'wins': 32, 'losses': 28},
        {'team': 'Los Angeles Lakers', 'elo': 1480, 'wins': 30, 'losses': 30},
    ]
    
    viz = NBAVisualization()
    
    # Create all visualization types
    fig1 = viz.create_elo_rankings_chart(sample_data, 'elo_rankings_demo.png')
    fig2 = viz.create_elo_distribution_chart(sample_data, 'elo_distribution_demo.png')
    fig3 = viz.create_conference_comparison_chart(sample_data, 'conference_comparison_demo.png')
    fig4 = viz.create_team_performance_radar(sample_data, 6, 'team_radar_demo.png')
    
    plt.show()


if __name__ == '__main__':
    demo_nba_visualization() 