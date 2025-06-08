# NBA Analytics Suite 🏀📊

A comprehensive, professional-grade analytics suite for NBA data analysis, featuring Elo ratings, betting market analysis, and advanced statistical modeling.

## Features

### 🏀 Elo Rating System
- **Real-time Elo Calculations**: Process 2024-2025 NBA season data with customizable K-factors
- **Team Rankings**: Live standings with win-loss records and conference breakdowns  
- **Win Probability Calculator**: Single game predictions with home court advantage
- **Playoff Series Calculator**: Best-of-7 series probabilities using proper NBA 2-2-1-1-1 format
- **Modern Web UI**: Responsive design with Tailwind CSS and smooth animations

### 📊 Betting Market Analysis
- **Market Inefficiency Detection**: Compare betting odds with statistical models
- **Historical Analysis**: Leverage 70+ years of NBA Finals data
- **Risk Assessment**: Kelly Criterion and expected value calculations
- **Professional Visualization**: Publication-ready charts and graphs
- **Multiple Model Integration**: Elo ratings, historical precedent, market odds

### 🔧 Professional Tools
- **Data Export**: JSON format for further analysis
- **Comprehensive Reports**: Detailed analysis with executive summaries
- **Type-Safe Code**: Professional Python with dataclasses and type hints
- **Automated Setup**: One-command installation and testing

## Quick Start

### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/nba-analytics-suite.git
cd nba-analytics-suite

# Run automated setup
python3 setup.py
```

### Manual Setup

1. **Set up virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run betting market analysis**
   ```bash
   python betting_market_vs_models.py
   ```

3. **Start web application**
   ```bash
   python app.py
   # Open browser: http://localhost:5000
   ```

4. **Generate visualizations**
   ```bash
   python visualization.py
   ```

## Deployment to Render 🚀

### Step 1: Prepare Your Repository

**IMPORTANT**: Never commit secrets to Git!

```bash
# Ensure .env is in .gitignore (already done)
git add .
git commit -m "Initial commit - NBA Elo app ready for deployment"
git push origin main
```

### Step 2: Environment Variables in Render

When deploying to Render, set these environment variables in the Render dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | `your-generated-secret-key` | **REQUIRED**: Strong secret key for Flask sessions |
| `FLASK_DEBUG` | `False` | **REQUIRED**: Disable debug mode in production |
| `HOST` | `0.0.0.0` | Allow connections from anywhere |
| `PORT` | `10000` | Render's default port (or use Render's PORT env var) |
| `ALLOWED_ORIGINS` | `https://yourdomain.onrender.com` | Replace with your actual domain |

#### How to Set Environment Variables in Render:

1. **Go to your service** in the Render dashboard
2. **Click "Environment"** in the left sidebar
3. **Add each variable** one by one:
   - Click "Add Environment Variable"
   - Enter the key and value
   - Click "Save Changes"

#### Generate a Secure SECRET_KEY:

```python
# Run this in Python to generate a secure key:
import secrets
print(secrets.token_hex(32))
```

### Step 3: Deploy to Render

1. **Create a new Web Service** on [Render](https://render.com)
2. **Connect your GitHub repository**
3. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3
4. **Set environment variables** (see table above)
5. **Deploy!** 🎉

## Security Best Practices ✅

### ✅ What We Do Right:

- **Environment Variables**: All secrets stored in environment variables
- **Git Ignore**: `.env` files never committed to Git
- **Security Headers**: X-Frame-Options, X-XSS-Protection, etc.
- **CORS Configuration**: Configurable allowed origins
- **Production Mode**: Debug disabled in production

### 🔒 Additional Security Tips:

1. **Rotate Secrets Regularly**: Change SECRET_KEY periodically
2. **Monitor Access**: Check Render logs for suspicious activity
3. **HTTPS Only**: Render provides automatic HTTPS
4. **Environment Isolation**: Use different keys for dev/staging/production

## Alternative Hosting Options

### Railway ($5/month)
- Automatic deployments from Git
- Built-in environment variable management
- PostgreSQL add-ons available

### Fly.io (Free tier available)
- Global deployment network
- Docker-based deployments
- Automatic scaling

### Heroku
- Classic PaaS option
- Many add-ons available
- Higher pricing than alternatives

## 📊 Betting Market Analysis

### Core Features
- **Market Inefficiency Detection**: Compare betting odds with statistical models
- **Kelly Criterion Calculations**: Optimal bet sizing recommendations
- **Historical Precedent Analysis**: 70+ years of NBA Finals data
- **Professional Visualizations**: Publication-ready charts and graphs

### Example Usage
```python
from betting_market_vs_models import FinalsAnalyzer, ModelType

# Initialize analyzer
analyzer = FinalsAnalyzer("Pacers", "Thunder", "1-0")

# Add probability estimates
analyzer.add_estimate(ModelType.BETTING_MARKET, 25.0, "High Confidence")
analyzer.add_estimate(ModelType.ELO_ADAPTIVE, 32.5, "Moderate Confidence")
analyzer.add_estimate(ModelType.HISTORICAL_PRECEDENT, 44.4, "Moderate Confidence")

# Generate comprehensive report
report = analyzer.generate_comprehensive_report()
print(report)

# Export analysis
json_file = analyzer.export_to_json()
```

### Risk Management
- **Conservative Position Sizing**: 2-5% of bankroll recommendations
- **Edge Detection**: Identify market inefficiencies
- **Expected Value Calculations**: Quantify potential returns
- **Professional Risk Disclaimers**: Educational use only

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/teams` | GET | List all NBA teams |
| `/api/calculate` | POST | Calculate Elo ratings |
| `/api/win_probability` | POST | Single game win probability |
| `/api/series_probability` | POST | Best-of-7 series probability |

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, JavaScript (Vanilla), Tailwind CSS
- **Data**: JSON file with NBA 2024-2025 season games
- **Algorithms**: Elo rating system with margin of victory, dynamic programming for series probabilities
- **Deployment**: Render, Railway, or any Python-compatible platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

---

**Made with ❤️ for NBA fans and data enthusiasts** 