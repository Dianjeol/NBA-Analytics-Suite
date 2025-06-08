#!/usr/bin/env python3
"""
NBA Finals Betting Market Analysis Tool
=====================================

A comprehensive analysis tool comparing betting market odds with statistical models
and historical precedent for championship series predictions.

Author: NBA Analytics Team
Version: 1.0.0
"""

import json
import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    """Enumeration of different prediction models."""
    BETTING_MARKET = "Betting Markets"
    ELO_ADAPTIVE = "Elo Model (Adaptive K)"
    HISTORICAL_PRECEDENT = "Historical Precedent"
    GAME_ONE_WINNERS = "Historical (Game 1 Winners)"

@dataclass
class ProbabilityEstimate:
    """Data class for probability estimates."""
    model_type: ModelType
    team_a_probability: float
    team_b_probability: float
    confidence_level: Optional[str] = None
    
    def __post_init__(self):
        """Validate probabilities sum to 100%."""
        if abs(self.team_a_probability + self.team_b_probability - 100.0) > 0.1:
            raise ValueError("Probabilities must sum to 100%")

@dataclass
class MarketAnalysis:
    """Data class for market analysis results."""
    estimated_edge: float
    expected_value: float
    kelly_criterion: float
    risk_level: str

class BettingOddsConverter:
    """Utility class for converting between different odds formats."""
    
    @staticmethod
    def american_to_probability(american_odds: int) -> float:
        """
        Convert American odds to probability percentage.
        
        Args:
            american_odds: American odds format (e.g., +300, -150)
            
        Returns:
            Probability as percentage (0-100)
        """
        if american_odds > 0:
            return 100 / (american_odds + 100)
        else:
            return abs(american_odds) / (abs(american_odds) + 100)
    
    @staticmethod
    def probability_to_american(probability: float) -> int:
        """
        Convert probability to American odds.
        
        Args:
            probability: Probability as decimal (0-1) or percentage (0-100)
            
        Returns:
            American odds format
        """
        # Convert percentage to decimal if needed
        if probability > 1:
            probability = probability / 100
            
        if probability >= 0.5:
            return int(-100 * probability / (1 - probability))
        else:
            return int(100 * (1 - probability) / probability)
    
    @staticmethod
    def decimal_to_american(decimal_odds: float) -> int:
        """Convert decimal odds to American odds."""
        if decimal_odds >= 2.0:
            return int((decimal_odds - 1) * 100)
        else:
            return int(-100 / (decimal_odds - 1))

class FinalsAnalyzer:
    """Main class for analyzing NBA Finals betting markets and predictions."""
    
    def __init__(self, team_a: str, team_b: str, series_state: str = "1-0"):
        """
        Initialize the analyzer.
        
        Args:
            team_a: Name of team A (e.g., "Pacers")
            team_b: Name of team B (e.g., "Thunder")  
            series_state: Current series state (e.g., "1-0", "tied 0-0")
        """
        self.team_a = team_a
        self.team_b = team_b
        self.series_state = series_state
        self.estimates: List[ProbabilityEstimate] = []
        self.analysis_timestamp = datetime.datetime.now()
        
    def add_estimate(self, model_type: ModelType, team_a_prob: float, 
                    confidence: Optional[str] = None) -> None:
        """Add a probability estimate from a specific model."""
        team_b_prob = 100.0 - team_a_prob
        estimate = ProbabilityEstimate(
            model_type=model_type,
            team_a_probability=team_a_prob,
            team_b_probability=team_b_prob,
            confidence_level=confidence
        )
        self.estimates.append(estimate)
    
    def calculate_market_edge(self, market_prob: float, true_prob: float) -> MarketAnalysis:
        """
        Calculate potential market edge and Kelly criterion bet sizing.
        
        Args:
            market_prob: Market implied probability
            true_prob: Estimated true probability
            
        Returns:
            MarketAnalysis object with edge calculations
        """
        edge = (true_prob - market_prob) / market_prob
        
        # Convert to decimal odds for expected value calculation
        market_odds = 1 / (market_prob / 100)
        expected_value = (true_prob / 100 * market_odds) - 1
        
        # Kelly Criterion: f = (bp - q) / b where b = odds-1, p = true prob, q = 1-p
        if market_odds > 1:
            kelly = ((true_prob / 100) * (market_odds - 1) - (1 - true_prob / 100)) / (market_odds - 1)
            kelly = max(0, kelly)  # Don't bet if Kelly is negative
        else:
            kelly = 0
            
        # Determine risk level
        if abs(edge) < 0.05:
            risk_level = "Low Edge"
        elif abs(edge) < 0.15:
            risk_level = "Moderate Edge"
        else:
            risk_level = "High Edge"
            
        return MarketAnalysis(
            estimated_edge=edge,
            expected_value=expected_value,
            kelly_criterion=kelly,
            risk_level=risk_level
        )
    
    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive analysis report."""
        report = []
        
        # Header
        report.append("🏀 NBA FINALS BETTING MARKET ANALYSIS")
        report.append("=" * 80)
        report.append(f"📊 Analysis Date: {self.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"🏆 Matchup: {self.team_a} vs {self.team_b}")
        report.append(f"📈 Series State: {self.team_a} leads {self.series_state}")
        report.append("=" * 80)
        
        # Probability comparison table
        report.append("\n📈 PROBABILITY ESTIMATES COMPARISON:")
        report.append("=" * 80)
        report.append(f"{'Model/Source':<28} {f'{self.team_a} Win %':<12} {'Implied Odds':<12} {f'{self.team_b} Win %'}")
        report.append("-" * 80)
        
        for estimate in self.estimates:
            odds = BettingOddsConverter.probability_to_american(estimate.team_a_probability)
            report.append(
                f"{estimate.model_type.value:<28} "
                f"{estimate.team_a_probability:>6.1f}%      "
                f"{odds:>+6d}        "
                f"{estimate.team_b_probability:>6.1f}%"
            )
        
        # Market inefficiency analysis
        if len(self.estimates) > 1:
            market_estimate = next((e for e in self.estimates if e.model_type == ModelType.BETTING_MARKET), None)
            if market_estimate:
                report.append(f"\n🎯 MARKET INEFFICIENCY ANALYSIS:")
                report.append("=" * 80)
                
                for estimate in self.estimates:
                    if estimate.model_type != ModelType.BETTING_MARKET:
                        analysis = self.calculate_market_edge(
                            market_estimate.team_a_probability,
                            estimate.team_a_probability
                        )
                        report.append(
                            f"• {estimate.model_type.value}: "
                            f"{analysis.estimated_edge:+.1%} edge, "
                            f"{analysis.expected_value:+.1%} EV, "
                            f"Kelly: {analysis.kelly_criterion:.1%}, "
                            f"Risk: {analysis.risk_level}"
                        )
        
        return "\n".join(report)
    
    def export_to_json(self, filename: Optional[str] = None) -> str:
        """Export analysis to JSON format."""
        if filename is None:
            filename = f"finals_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        data = {
            "metadata": {
                "team_a": self.team_a,
                "team_b": self.team_b,
                "series_state": self.series_state,
                "analysis_timestamp": self.analysis_timestamp.isoformat(),
                "version": "1.0.0"
            },
            "estimates": [
                {
                    "model_type": est.model_type.value,
                    "team_a_probability": est.team_a_probability,
                    "team_b_probability": est.team_b_probability,
                    "confidence_level": est.confidence_level
                }
                for est in self.estimates
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        return filename

def main():
    """Main execution function demonstrating the analysis."""
    # Initialize analyzer
    analyzer = FinalsAnalyzer("Pacers", "Thunder", "1-0")
    
    # Add probability estimates
    analyzer.add_estimate(ModelType.BETTING_MARKET, 25.0, "High Confidence")
    analyzer.add_estimate(ModelType.ELO_ADAPTIVE, 32.5, "Moderate Confidence")
    analyzer.add_estimate(ModelType.HISTORICAL_PRECEDENT, 44.4, "Moderate Confidence")
    analyzer.add_estimate(ModelType.GAME_ONE_WINNERS, 70.1, "Low Confidence")
    
    # Generate and display comprehensive report
    report = analyzer.generate_comprehensive_report()
    print(report)
    
    # Additional detailed analysis
    print("\n\n💡 DETAILED MARKET INSIGHTS:")
    print("=" * 80)
    
    # Market factors analysis
    market_factors = {
        "Conservative Factors": [
            ("Thunder's Regular Season Dominance", "1286 Elo rating, consistent #1 ranking"),
            ("Limited Historical Sample", "Only 18 road Game 1 wins in Finals history"),
            ("Recency Bias", "Recent championships favor higher seeds"),
            ("Public Betting Patterns", "Thunder more popular team nationally"),
            ("Injury/Sustainability Concerns", "Questions about Pacers' playoff run"),
            ("Remaining Home Court", "Thunder still have structural advantage")
        ],
        "Historical Support Factors": [
            ("Psychological Momentum", "Road Game 1 wins create massive confidence shift"),
            ("Home Court Neutralization", "Thunder's biggest advantage now eliminated"),
            ("Playoff vs Regular Season", "Different dynamics favor underdogs"),
            ("Championship Pressure", "Favorites often struggle with expectations"),
            ("Precedent Examples", "1995 Rockets, 2011 Mavs, upset patterns"),
            ("Sample Significance", "44.4% win rate over 70+ years of data")
        ]
    }
    
    for category, factors in market_factors.items():
        print(f"\n📊 {category.upper()}:")
        for factor, explanation in factors:
            print(f"• {factor:<25}: {explanation}")
    
    # Export analysis
    json_file = analyzer.export_to_json()
    print(f"\n💾 Analysis exported to: {json_file}")
    
    # Final recommendation
    print(f"\n🎯 EXECUTIVE SUMMARY:")
    print("=" * 80)
    print("• Market appears to be undervaluing Pacers by 10-15 percentage points")
    print("• Historical precedent suggests legitimate value opportunity")
    print("• Road Game 1 victories are rarer and more impactful than markets price")
    print("• Recommended position sizing: Conservative (2-5% of bankroll)")
    print("• Risk level: Moderate to High")
    print("• Time horizon: Series completion (next 2-3 weeks)")

if __name__ == "__main__":
    main() 