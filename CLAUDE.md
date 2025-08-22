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

## Files Structure (Updated)
```
fantasy/
├── CLAUDE.md (this file)
├── draft_strategy.md (comprehensive framework)
├── league_winner_strategy.md (champion insights)
├── rankings/
│   ├── consensus_ppr_rankings.md (top 50 with byes)
│   └── position_guides_with_byes.md (detailed by position)
├── mock_drafts/
│   ├── draft_comparison_spreadsheet.md (3 sources compared)
│   ├── espn_recent_ppr_12team.md
│   └── nbc_recent_ppr_12team.md
├── injury_reports/
│   └── august_22_2025.md (latest updates)
└── draft_assistant.py (PLANNED - Python draft helper)
```

## Pre-Draft Checklist
- [ ] Update all rankings 24 hours before draft
- [ ] Check injury reports day of draft
- [ ] Review bye weeks for top targets
- [ ] Set up draft board by tier
- [ ] Identify sleepers and breakout candidates

## Draft Day Commands
```bash
# Quick position check
grep -c "QB\|RB\|WR\|TE" my_drafted_players.txt

# Find best available by position  
head -20 rankings/wr_rankings.md | grep -v "DRAFTED"
```