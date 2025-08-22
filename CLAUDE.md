# Fantasy Football Draft Assistant 🏈

## League Settings (CONFIRMED)
- **Format**: PPR (Point Per Reception) - 12 team redraft, snake draft
- **Roster**: 1 QB, 2RB, 2WR, 1TE, 1FLEX (WR/TE/RB), 1D, 1K, 7 bench
- **Scoring**: 
  - 1 point per 25 passing yards
  - 10 points per receiving/rushing touchdown  
  - 1 point per reception (PPR)
  - Partial point league
- **Draft**: Position revealed 1 hour before
- **Timeline**: ~1 week to prepare

## Research Completed (Aug 22, 2025)
- ✅ **Recent Mock Drafts**: ESPN, NBC Sports, Fantasy Football Calculator (8,997 drafts)
- ✅ **Current Injury Reports**: Daily updates through Aug 22
- ✅ **Bye Week Analysis**: 2025 NFL schedule integrated
- ✅ **League Winner Insights**: Strategy from 2024 champion
- ✅ **PPR Strategy Framework**: Volume-based approach confirmed

## Key PPR Strategy Notes
- **PPR format favors**:
  - Wide receivers (especially slot/target-heavy WRs)  
  - Pass-catching running backs (40+ receptions target)
  - Tight ends with high target share (100+ targets)
- **Volume > efficiency** in PPR
- **Target share is crucial** metric (CeeDee Lamb led with 135 catches)
- **First round trends**: 50/50 split RB/WR, no QBs until Round 3+

## Draft Data Intelligence (Current)
- **Top ADP**: Ja'Marr Chase (#1), Bijan Robinson (#2), Justin Jefferson (#3)
- **Rising Fast**: Ashton Jeanty (ADP 11 → mocks at #5)
- **Injury Concerns**: Chris Godwin (out until Oct), Matthew Stafford (back)
- **Opportunity Plays**: Nick Chubb (Mixon injury), Bucs WRs (Godwin out)

## Bye Week Danger Zones 🚨
- **Week 8 "Byepocalypse"**: 6 teams (DET, LV, LAR, JAX, ARI, SEA)
  - Key players: Gibbs, Jeanty, Nacua, St. Brown, Thomas Jr.
- **Week 10**: Chase (CIN) + Lamb (DAL) stack risk  
- **Week 14**: CMC (SF) + Nabers (NYG) - playoff impact

## League Winner Strategy Integration
- **Roster Management**: Elite QB/TE = roster 1, otherwise 2
- **Position Weakness**: "Hammer weak positions with bench spots" (4+ RBs if needed)
- **Bye Philosophy**: Talent first, byes as tiebreaker only
- **Streaming**: K/DEF weekly, TE if no elite option

## Commands for Draft Day
```bash
# Player lookup with bye week
grep -i "player_name" rankings/*with_byes.md

# Check injury status  
grep -i "player_name" injury_reports/august_22_2025.md

# Bye week conflict check
grep "Week 8" rankings/consensus_ppr_rankings.md

# Best available by position
head -20 rankings/position_guides_with_byes.md | grep "RB\|WR"

# Start Python draft assistant
python draft_assistant.py
```

## Data Sources (Confidence Levels)
- **HIGH**: Fantasy Football Calculator ADP (8,997 recent drafts)
- **MEDIUM**: ESPN/NBC Sports expert mocks (single draft analysis)
- **HIGH**: NFL injury reports (daily updates)
- **MEDIUM**: League winner insights (single championship experience)

## Professional Development Status (Updated Aug 22, 2025)

### 🏗️ **Architecture Transformation COMPLETED**
- ✅ **Git Repository**: Initialized with semantic commits
- ✅ **Professional Structure**: Modular architecture implemented
- ✅ **Clean Code**: Type hints, docstrings, validation throughout
- ✅ **Input Validation**: Typo prevention and player search system
- ✅ **Documentation**: Professional README, roadmap, contributing guidelines

### 🎯 **Current Project Status**
- **Phase 1**: Foundation & Code Quality - ✅ COMPLETED
- **Phase 2**: Refactor to Services/CLI - 🔄 IN PROGRESS  
- **Phase 3**: Testing & CI/CD - 📋 PLANNED
- **Phase 4**: Web Interface - 📋 PLANNED

### 📊 **Development Progress Tracking**
See `PROJECT_ROADMAP.md` for detailed sprint planning and technical debt management.

## Updated File Structure (Professional)
```
fantasy-football-assistant/
├── CLAUDE.md (this file - session persistence)
├── PROJECT_ROADMAP.md (development plan & sprints)
├── README.md (professional documentation)
├── requirements.txt (dependencies)
├── requirements-dev.txt (development tools)
├── .gitignore (git configuration)
├── src/fantasy_assistant/ (main codebase)
│   ├── __init__.py
│   ├── models/ (data models)
│   │   ├── __init__.py
│   │   ├── player.py (Player class with enums & validation)
│   │   ├── database.py (DatabaseManager - TODO)
│   │   └── draft_state.py (DraftState tracking - TODO)
│   ├── services/ (business logic - TODO)
│   │   ├── draft_engine.py (core draft management)
│   │   └── ai_recommender.py (AI recommendation system)
│   ├── utils/ (utilities)
│   │   ├── __init__.py
│   │   ├── player_search.py (fuzzy matching & autocomplete)
│   │   ├── validation.py (input validation & sanitization)
│   │   └── logging_config.py (logging setup - TODO)
│   ├── cli/ (command-line interface - TODO)
│   │   └── main.py (CLI application)
│   └── tests/ (test suite - TODO)
├── rankings/ (research data)
│   ├── consensus_ppr_rankings.md (top 50 with byes)
│   └── position_guides_with_byes.md (detailed by position)
├── mock_drafts/ (compiled mock draft data)
│   ├── draft_comparison_spreadsheet.md (3 sources compared)
│   ├── espn_recent_ppr_12team.md
│   └── nbc_recent_ppr_12team.md
├── injury_reports/
│   └── august_22_2025.md (latest updates)
├── draft_strategy.md (comprehensive framework)
├── league_winner_strategy.md (champion insights)
├── draft_assistant.py (legacy - being refactored)
└── database_schema.sql (database structure)
```

## Next Development Sessions

### 🔄 **Phase 2 Tasks (Current Sprint)**
- [ ] **Refactor draft_assistant.py** into service classes
- [ ] **Create DatabaseManager** class in models/database.py
- [ ] **Build DraftEngine** service for core draft logic
- [ ] **Implement AIRecommender** service with strategy rules
- [ ] **Create new CLI** interface using modular components
- [ ] **Migrate player data** to new Player model system

### 🧪 **Phase 3 Tasks (Next Sprint)**
- [ ] **Write unit tests** for all models and utilities
- [ ] **Integration tests** for draft scenarios
- [ ] **Set up pytest configuration** and test structure
- [ ] **Add code quality tools** (black, flake8, mypy)
- [ ] **Create pre-commit hooks** for consistent quality

### 🌐 **Phase 4 Tasks (Future Sprint)**
- [ ] **Choose Flask vs Django** for web interface
- [ ] **Design API endpoints** for draft operations
- [ ] **Create real-time draft board** interface
- [ ] **Build mobile-responsive** UI components

## Session Persistence Notes

### **Current Working State**
- **Git initialized** with professional structure
- **Player model** complete with validation and enums
- **PlayerSearch system** prevents typos with fuzzy matching
- **Input validation** comprehensive with custom exceptions
- **Documentation** professional-grade with roadmap

### **Key Decisions Made**
- **Architecture**: Modular design with models/services/utils/cli separation
- **Validation Strategy**: Comprehensive input validation with suggestions
- **Error Handling**: Custom exceptions with detailed messages
- **Code Quality**: Type hints, docstrings, professional standards
- **Git Workflow**: Semantic commits with detailed change logs

### **Technical Debt Identified**
- **Legacy code**: draft_assistant.py needs refactoring
- **Database layer**: Need to implement DatabaseManager
- **Service layer**: AI recommendation logic needs extraction
- **CLI interface**: Current CLI needs rebuilding with new architecture

## Commands for Continuing Work

### **Development Commands**
```bash
# Continue development
cd /Users/evansmelser/src/fantasy
git status                           # Check current state
git log --oneline                   # Review commit history

# Code quality
python -m flake8 src/               # Lint code
python -m mypy src/                 # Type checking
python -m black src/                # Format code

# Testing (when implemented)
pytest src/tests/ -v --cov=src/fantasy_assistant

# Run current system
python draft_assistant.py          # Legacy system
python -m src.fantasy_assistant.cli.main  # New system (when ready)
```

### **Data Management Commands**  
```bash
# Update injury reports
grep -i "injury\|out\|questionable" injury_reports/august_22_2025.md

# Check player data
grep -i "player_name" rankings/consensus_ppr_rankings.md

# Bye week analysis
grep "Week 8" rankings/position_guides_with_byes.md
```

## Draft Day Checklist (When Ready)
- [ ] **Update all rankings** 24 hours before draft
- [ ] **Check injury reports** day of draft  
- [ ] **Review bye weeks** for top targets
- [ ] **Test draft assistant** with mock scenarios
- [ ] **Prepare GitHub backup** of latest data
- [ ] **Set draft position** in system when revealed
- [ ] **Launch professional draft interface**