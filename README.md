# NBA Analytics Suite

A comprehensive statistical analysis framework for NBA data modeling, implementing Elo rating systems, betting market analysis, and advanced probability calculations.

## Overview

This suite provides production-ready tools for NBA statistical analysis:

- **Elo Rating System**: Real-time calculations with adaptive K-factors
- **Market Analysis**: Betting odds comparison with statistical models  
- **Probability Modeling**: Game and series outcome predictions
- **Data Visualization**: Professional charts and statistical plots
- **Risk Assessment**: Kelly Criterion and expected value calculations

## Architecture

### Core Components

```
nba-analytics-suite/
├── app.py                    # Web interface (Flask)
├── betting_market_vs_models.py    # Market analysis engine
├── visualization.py          # Chart generation
├── elo_*.py                 # Elo rating implementations
├── setup.py                 # Automated installation
└── static/templates/        # Web assets
```

### Dependencies

- Python 3.8+
- Flask 2.3.3
- NumPy 1.24.3
- Pandas 2.1.0
- Matplotlib 3.7.2
- Seaborn 0.12.2

## Installation

### Automated Setup

```bash
git clone https://github.com/yourusername/nba-analytics-suite.git
cd nba-analytics-suite
python3 setup.py
```

### Manual Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Market Analysis Engine

```python
from betting_market_vs_models import FinalsAnalyzer, ModelType

analyzer = FinalsAnalyzer("TeamA", "TeamB", "1-0")
analyzer.add_estimate(ModelType.BETTING_MARKET, 25.0)
analyzer.add_estimate(ModelType.ELO_ADAPTIVE, 32.5)

report = analyzer.generate_comprehensive_report()
analysis_data = analyzer.export_to_json()
```

### Elo Rating Calculations

```python
from nba_elo_calculator import EloCalculator

calculator = EloCalculator(k_factor=20)
new_ratings = calculator.update_ratings(team_a_rating, team_b_rating, result)
```

### Web Interface

```bash
python app.py
# Access: http://localhost:5000
```

## API Reference

### Market Analysis Classes

#### `FinalsAnalyzer`
Core analysis engine for market inefficiency detection.

**Methods:**
- `add_estimate(model_type, probability, confidence)`: Add probability estimate
- `calculate_market_edge(market_prob, true_prob)`: Calculate betting edge
- `generate_comprehensive_report()`: Generate analysis report
- `export_to_json(filename)`: Export structured data

#### `BettingOddsConverter`
Utility class for odds format conversion.

**Static Methods:**
- `odds_to_probability(american_odds)`: Convert American odds to probability
- `probability_to_american_odds(probability)`: Convert probability to American odds

### Data Structures

#### `ProbabilityEstimate`
```python
@dataclass
class ProbabilityEstimate:
    model_type: ModelType
    team_a_probability: float
    team_b_probability: float
    confidence_level: Optional[str]
```

#### `MarketAnalysis`
```python
@dataclass
class MarketAnalysis:
    estimated_edge: float
    expected_value: float
    kelly_criterion: float
    risk_level: str
```

## Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/teams` | GET | Team list |
| `/api/calculate` | POST | Elo calculations |
| `/api/win_probability` | POST | Game probability |
| `/api/series_probability` | POST | Series probability |

## Configuration

### Environment Variables

Create `.env` file for web application:
```
SECRET_KEY=your-secret-key
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
```

### Elo Parameters

Default K-factors by game importance:
- Regular season: 20
- Playoffs: 30
- Finals: 40

## Testing

Run test suite:
```bash
python3 setup.py  # Includes functionality tests
```

Individual module testing:
```bash
python3 betting_market_vs_models.py
python3 visualization.py
```

## Output Formats

### JSON Export Structure
```json
{
  "metadata": {
    "team_a": "string",
    "team_b": "string", 
    "series_state": "string",
    "analysis_timestamp": "ISO-8601",
    "version": "1.0.0"
  },
  "estimates": [
    {
      "model_type": "string",
      "team_a_probability": "float",
      "team_b_probability": "float",
      "confidence_level": "string"
    }
  ]
}
```

### Visualization Outputs
- PNG format, 300 DPI resolution
- Professional styling with configurable themes
- Export-ready for publications and presentations

## Performance

### Benchmarks
- Elo calculations: ~1000 games/second
- Market analysis: Sub-second response time
- Visualization generation: 2-5 seconds per chart
- JSON export: Minimal overhead

### Memory Usage
- Base system: ~50MB RAM
- With visualizations: ~200MB RAM
- Large datasets (full season): ~500MB RAM

## Deployment

### Production Web Server

Using Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Container Deployment

```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Cloud Platforms

Tested and compatible with:
- Render.com
- Railway.app  
- Heroku
- DigitalOcean App Platform

## Data Sources

- NBA Official Statistics (1947-2024)
- Basketball Reference historical data
- Real-time season data via JSON imports
- Market odds (manual input for analysis)

## Algorithm Details

### Elo Rating System
Implementation follows standard Elo with margin-of-victory adjustments:
```
new_rating = old_rating + K * (actual_score - expected_score)
expected_score = 1 / (1 + 10^((opponent_rating - player_rating) / 400))
```

### Kelly Criterion Implementation
Optimal bet sizing calculation:
```
f = (bp - q) / b
where: b = odds-1, p = true_probability, q = 1-p
```

## Contributing

### Development Setup
1. Fork repository
2. Create feature branch: `git checkout -b feature-name`
3. Implement changes with tests
4. Submit pull request with detailed description

### Code Standards
- Python 3.8+ compatibility
- Type hints required for all functions
- Docstrings for all public methods
- Unit tests for new functionality

### Documentation
- Update README for API changes
- Include code examples for new features
- Maintain changelog for version updates

## License

MIT License. See LICENSE file for full terms.

## Disclaimer

This software is provided for educational and research purposes only. It is not intended as financial advice or gambling recommendations. Users should understand the risks involved in any betting or investment activities.

---

**Maintainers:** NBA Analytics Team  
**Repository:** https://github.com/yourusername/nba-analytics-suite  
**Documentation:** See individual module docstrings and BETTING_ANALYSIS.md