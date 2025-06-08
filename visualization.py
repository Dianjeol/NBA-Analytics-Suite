#!/usr/bin/env python3
"""
NBA Finals Betting Market Visualization Module
============================================

Interactive visualization tools for betting market analysis and probability comparisons.

Author: NBA Analytics Team
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Optional
import pandas as pd
from betting_market_vs_models import FinalsAnalyzer, ModelType, ProbabilityEstimate

# Set professional styling
plt.style.use('default')
sns.set_palette("husl")

class MarketVisualizer:
    """Professional visualization class for betting market analysis."""
    
    def __init__(self, analyzer):
        """Initialize with a FinalsAnalyzer instance."""
        self.analyzer = analyzer
        self.figure_size = (12, 8)
        
    def create_probability_chart(self, save_path: Optional[str] = None):
        """Create probability comparison bar chart."""
        if not self.analyzer.estimates:
            raise ValueError("No estimates available")
            
        models = [est.model_type.value for est in self.analyzer.estimates]
        team_a_probs = [est.team_a_probability for est in self.analyzer.estimates]
        team_b_probs = [est.team_b_probability for est in self.analyzer.estimates]
        
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        x = np.arange(len(models))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, team_a_probs, width, 
                      label=f'{self.analyzer.team_a} Win %', 
                      color='#2E86C1', alpha=0.8)
        bars2 = ax.bar(x + width/2, team_b_probs, width,
                      label=f'{self.analyzer.team_b} Win %', 
                      color='#E74C3C', alpha=0.8)
        
        ax.set_xlabel('Prediction Models', fontsize=12, fontweight='bold')
        ax.set_ylabel('Win Probability (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'NBA Finals Win Probability Analysis\n{self.analyzer.team_a} vs {self.analyzer.team_b}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for bar in bars1 + bars2:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def create_odds_comparison_chart(self, save_path: str = None) -> plt.Figure:
        """Create a chart showing implied odds from different models."""
        from betting_market_vs_models import BettingOddsConverter
        
        if not self.analyzer.estimates:
            raise ValueError("No probability estimates available for visualization")
            
        # Prepare data
        models = [est.model_type.value for est in self.analyzer.estimates]
        odds = [BettingOddsConverter.probability_to_american(est.team_a_probability) 
                for est in self.analyzer.estimates]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create horizontal bar chart
        bars = ax.barh(models, odds, color=['#27AE60' if o > 0 else '#E74C3C' for o in odds])
        
        # Customize chart
        ax.set_xlabel('American Odds', fontsize=12, fontweight='bold')
        ax.set_title(f'{self.analyzer.team_a} Championship Odds Comparison\nSeries State: {self.analyzer.series_state}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, odd) in enumerate(zip(bars, odds)):
            width = bar.get_width()
            ax.text(width + (10 if width > 0 else -10), bar.get_y() + bar.get_height()/2,
                   f'{odd:+d}', ha='left' if width > 0 else 'right', va='center',
                   fontsize=10, fontweight='bold')
        
        # Add vertical line at even odds
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax.text(0, len(models), 'Even Odds', ha='center', va='bottom', 
                fontsize=9, style='italic')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def create_market_edge_analysis(self, save_path: str = None) -> plt.Figure:
        """Create visualization showing potential market edges."""
        if len(self.analyzer.estimates) < 2:
            raise ValueError("Need at least 2 estimates for edge analysis")
            
        # Find market estimate
        market_est = next((e for e in self.analyzer.estimates 
                          if e.model_type == ModelType.BETTING_MARKET), None)
        if not market_est:
            raise ValueError("No betting market estimate found")
            
        # Calculate edges for other models
        edges = []
        model_names = []
        expected_values = []
        
        for est in self.analyzer.estimates:
            if est.model_type != ModelType.BETTING_MARKET:
                analysis = self.analyzer.calculate_market_edge(
                    market_est.team_a_probability, 
                    est.team_a_probability
                )
                edges.append(analysis.estimated_edge * 100)  # Convert to percentage
                expected_values.append(analysis.expected_value * 100)
                model_names.append(est.model_type.value)
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Edge analysis chart
        colors = ['#27AE60' if e > 0 else '#E74C3C' for e in edges]
        bars1 = ax1.bar(model_names, edges, color=colors, alpha=0.8)
        ax1.set_title('Market Edge Analysis', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Edge (%)', fontsize=11)
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, edge in zip(bars1, edges):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + (1 if height > 0 else -1),
                    f'{edge:+.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                    fontsize=9, fontweight='bold')
        
        # Expected value chart
        colors2 = ['#27AE60' if ev > 0 else '#E74C3C' for ev in expected_values]
        bars2 = ax2.bar(model_names, expected_values, color=colors2, alpha=0.8)
        ax2.set_title('Expected Value Analysis', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Expected Value (%)', fontsize=11)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, ev in zip(bars2, expected_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height + (1 if height > 0 else -1),
                    f'{ev:+.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                    fontsize=9, fontweight='bold')
        
        # Rotate x-axis labels
        for ax in [ax1, ax2]:
            ax.set_xticklabels(model_names, rotation=45, ha='right')
        
        plt.suptitle(f'Market Inefficiency Analysis: {self.analyzer.team_a} vs {self.analyzer.team_b}', 
                     fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def create_comprehensive_dashboard(self, save_path: str = None) -> plt.Figure:
        """Create a comprehensive dashboard combining all visualizations."""
        fig = plt.figure(figsize=(20, 12))
        
        # Create grid layout
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Probability comparison (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        models = [est.model_type.value for est in self.analyzer.estimates]
        team_a_probs = [est.team_a_probability for est in self.analyzer.estimates]
        team_b_probs = [est.team_b_probability for est in self.analyzer.estimates]
        
        x = np.arange(len(models))
        width = 0.35
        ax1.bar(x - width/2, team_a_probs, width, label=f'{self.analyzer.team_a}', 
                color='#2E86C1', alpha=0.8)
        ax1.bar(x + width/2, team_b_probs, width, label=f'{self.analyzer.team_b}', 
                color='#E74C3C', alpha=0.8)
        ax1.set_title('Win Probability Comparison', fontweight='bold')
        ax1.set_ylabel('Probability (%)')
        ax1.set_xticks(x)
        ax1.set_xticklabels(models, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add more subplots as needed...
        
        plt.suptitle(f'NBA Finals Market Analysis Dashboard\n{self.analyzer.team_a} vs {self.analyzer.team_b} | {self.analyzer.series_state}', 
                     fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig

def demo_visualization():
    """Demo the visualization system.""" 
    print("🎨 NBA Finals Market Analysis Visualization")
    print("📊 Charts available: probability comparison, odds analysis, market edge")
    print("💡 Install requirements: pip install matplotlib seaborn")

if __name__ == "__main__":
    demo_visualization() 