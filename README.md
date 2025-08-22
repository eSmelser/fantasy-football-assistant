# Fantasy Football Draft Assistant 🏈

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Professional-grade fantasy football draft assistant with AI-powered recommendations**

A comprehensive tool for dominating your 12-team PPR fantasy football draft, featuring real-time tracking, intelligent recommendations, and data-driven insights from 8,997+ mock drafts.

## ✨ Features

### 🎯 Core Functionality
- **Real-time draft tracking** with snake draft simulation
- **AI-powered recommendations** based on compiled strategy research
- **Intelligent player search** with typo prevention and autocomplete
- **Bye week conflict detection** to avoid roster disasters
- **Injury status monitoring** with real-time alerts
- **Best available lists** by position with detailed analysis

### 📊 Data Intelligence
- **8,997 recent mock drafts** from Fantasy Football Calculator
- **Expert analysis** from ESPN, NBC Sports, CBS Sports
- **Current injury reports** (updated August 2025)
- **2025 NFL bye week schedule** with conflict warnings
- **League winner insights** from championship strategies

### 🛡️ Professional Quality
- **Clean architecture** with modular design
- **Comprehensive input validation** prevents errors
- **Type hints and documentation** for maintainability
- **Error handling and logging** for robust operation
- **Test suite** with high coverage (coming soon)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/evansmelser/fantasy-football-assistant.git
   cd fantasy-football-assistant
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the assistant**
   ```bash
   python -m src.fantasy_assistant.cli.main
   ```

### First Time Setup

1. Enter your draft position (1-12) when prompted
2. The system will load all player data and rankings
3. Start tracking picks as your draft begins!

## 🎮 Usage

### Basic Commands

```bash
# Draft tracking
draft Ja'Marr Chase      # Record YOUR pick
pick Bijan Robinson      # Record opponent's pick

# Get recommendations  
recommend                # AI-powered suggestion for your turn
best                     # Top available players overall
best RB                  # Best available running backs

# Team management
roster                   # View your current team
bye                      # Check bye week conflicts
search justin            # Find players with autocomplete

# Utilities
help                     # Show all commands
quit                     # Exit the program
```

### Advanced Features

```bash
# Filtered searches
search --position RB --exclude-injured    # Healthy RBs only
best WR --max-bye 10                      # WRs with early byes
autocomplete jus                          # Type-ahead suggestions

# Analysis
analyze roster                            # Get roster composition analysis
conflicts                                 # Detailed bye week conflicts
injuries                                  # Current injury report
```

## 🏗️ Architecture

```
src/fantasy_assistant/
├── models/              # Data models and database operations
│   ├── player.py       # Player data class with validation
│   ├── database.py     # Database manager
│   └── draft_state.py  # Draft tracking
├── services/           # Business logic
│   ├── draft_engine.py # Core draft management
│   └── ai_recommender.py # AI recommendation system
├── utils/              # Utilities and helpers
│   ├── player_search.py # Smart player search/validation
│   ├── validation.py   # Input validation
│   └── logging_config.py # Logging setup
├── cli/                # Command-line interface
│   └── main.py        # CLI application entry point
└── tests/              # Test suite
    ├── test_models/
    ├── test_services/
    └── test_utils/
```

## 📊 Data Sources & Confidence

| Source | Sample Size | Confidence | Notes |
|--------|------------|------------|--------|
| Fantasy Football Calculator | 8,997 drafts | **HIGH** | Real user behavior |
| ESPN Expert Mocks | 1 draft | Medium | Professional analysis |
| NBC Sports Panel | 1 draft | Medium | Multi-expert consensus |
| NFL Injury Reports | Daily | **HIGH** | Official sources |
| League Winner Strategy | 1 champion | Medium | Proven success |

## 🎯 Key Intelligence

### 🚨 Bye Week Danger Zones
- **Week 8 "Byepocalypse"**: 6 teams off (DET, LV, LAR, JAX, ARI, SEA)
  - Key players: Gibbs, Jeanty, Nacua, St. Brown, Thomas Jr.
- **Week 10**: Chase (CIN) + Lamb (DAL) stack risk
- **Week 14**: CMC (SF) + Nabers (NYG) - playoff impact

### ⚠️ Current Injury Alerts
- **Chris Godwin (TB)**: Out until October - **AVOID**
- **Matthew Stafford (LAR)**: Back injury - Late round only
- **De'Von Achane (MIA)**: Calf issues - Monitor closely

### 📈 Rising Players
- **Ashton Jeanty (RB, LV)**: ADP 11 → Going top 5 in recent mocks
- **Nick Chubb (HOU)**: Opportunity with Mixon injury

## 🧪 Development

### Running Tests
```bash
pytest src/tests/ -v --cov=src/fantasy_assistant
```

### Code Quality
```bash
# Format code
black src/

# Lint code  
flake8 src/

# Type checking
mypy src/
```

### Development Installation
```bash
pip install -r requirements-dev.txt
pre-commit install  # Set up git hooks
```

## 🗺️ Roadmap

- [x] **Phase 1**: Core functionality and clean architecture
- [x] **Phase 2**: Input validation and player search
- [ ] **Phase 3**: Comprehensive test suite
- [ ] **Phase 4**: Web interface (Flask/Django)
- [ ] **Phase 5**: Advanced AI features and ML integration
- [ ] **Phase 6**: Cloud deployment and real-time data feeds

See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for detailed development plans.

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run the test suite (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for all public methods
- Include tests for new functionality
- Update documentation as needed

## 🤝 Acknowledgments

- **Fantasy Football Calculator** for providing extensive mock draft data
- **ESPN, NBC Sports, CBS Sports** for expert analysis
- **2024 League Champion** for sharing winning strategies
- **Fantasy football community** for continuous insights and feedback

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

Having issues? Check out:

1. **[Issues](https://github.com/evansmelser/fantasy-football-assistant/issues)** - Report bugs or request features
2. **[Wiki](https://github.com/evansmelser/fantasy-football-assistant/wiki)** - Detailed documentation
3. **[Discussions](https://github.com/evansmelser/fantasy-football-assistant/discussions)** - Community support

---

**Built for fantasy football champions** 🏆

*May your draft picks be wise and your waiver claims successful!* 🏈