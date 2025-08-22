-- Fantasy Football Draft Assistant Database Schema
-- SQLite database for 12-team PPR league

-- Main player rankings table
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    team TEXT NOT NULL,
    bye_week INTEGER NOT NULL,
    consensus_rank INTEGER,
    adp REAL,
    ppg_projection REAL,
    target_share REAL,
    receptions_2024 INTEGER,
    injury_status TEXT DEFAULT 'Healthy',
    notes TEXT,
    handcuff TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mock draft sources table
CREATE TABLE mock_draft_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    date TEXT NOT NULL,
    sample_size INTEGER,
    confidence_level TEXT,
    url TEXT
);

-- Individual mock draft picks
CREATE TABLE mock_draft_picks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER,
    pick_number INTEGER,
    player_name TEXT,
    position TEXT,
    team TEXT,
    round INTEGER,
    FOREIGN KEY (source_id) REFERENCES mock_draft_sources (id)
);

-- Current draft state
CREATE TABLE draft_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_size INTEGER DEFAULT 12,
    current_pick INTEGER DEFAULT 1,
    current_round INTEGER DEFAULT 1,
    user_draft_position INTEGER,
    snake_direction TEXT DEFAULT 'forward'
);

-- Drafted players tracking
CREATE TABLE drafted_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    position TEXT NOT NULL,
    team TEXT NOT NULL,
    pick_number INTEGER,
    round INTEGER,
    drafted_by_user BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User's team composition
CREATE TABLE user_roster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    position TEXT NOT NULL,
    team TEXT NOT NULL,
    bye_week INTEGER,
    round_drafted INTEGER,
    pick_number INTEGER,
    starter BOOLEAN DEFAULT TRUE
);

-- Injury reports table
CREATE TABLE injury_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    team TEXT NOT NULL,
    injury_type TEXT,
    status TEXT, -- Out, Questionable, Doubtful, Probable
    timeline TEXT,
    severity TEXT, -- Critical, Moderate, Minor
    fantasy_impact TEXT,
    report_date TEXT,
    source TEXT
);

-- Bye week conflicts tracking
CREATE TABLE bye_week_analysis (
    week_number INTEGER,
    teams_off TEXT,
    player_count INTEGER,
    severity TEXT, -- Byepocalypse, Heavy, Normal, Light
    fantasy_impact TEXT
);

-- AI recommendation history
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pick_number INTEGER,
    round INTEGER,
    recommended_player TEXT,
    position TEXT,
    reasoning TEXT,
    confidence_score REAL,
    alternative_1 TEXT,
    alternative_2 TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Strategy rules and preferences
CREATE TABLE strategy_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_type TEXT, -- position_priority, bye_week_limit, streaming, etc.
    position TEXT,
    rule_value TEXT,
    priority INTEGER,
    source TEXT -- research, league_winner, expert
);

-- Create indexes for performance
CREATE INDEX idx_players_position ON players(position);
CREATE INDEX idx_players_bye_week ON players(bye_week);
CREATE INDEX idx_players_consensus_rank ON players(consensus_rank);
CREATE INDEX idx_drafted_players_position ON drafted_players(position);
CREATE INDEX idx_injury_reports_player ON injury_reports(player_name);

-- Insert initial strategy rules
INSERT INTO strategy_rules (rule_type, position, rule_value, priority, source) VALUES
('position_timing', 'QB', 'Round 6+', 1, 'research'),
('position_timing', 'TE', 'Elite early or stream', 1, 'league_winner'),
('position_timing', 'K', 'Round 15-16', 1, 'league_winner'),
('position_timing', 'DEF', 'Round 15-16', 1, 'league_winner'),
('bye_week_limit', 'ALL', 'Max 2 same week same position', 2, 'league_winner'),
('streaming', 'K', 'Always stream', 1, 'league_winner'),
('streaming', 'DEF', 'Always stream', 1, 'league_winner'),
('ppr_priority', 'WR', 'Target share > efficiency', 1, 'research'),
('ppr_priority', 'RB', '40+ reception target', 1, 'research'),
('depth_strategy', 'RB', 'If weak, draft 4+ bench RBs', 1, 'league_winner');

-- Insert bye week analysis
INSERT INTO bye_week_analysis (week_number, teams_off, player_count, severity, fantasy_impact) VALUES
(5, 'ATL,CHI,GB,PIT', 4, 'Normal', 'Manageable week'),
(6, 'HOU,MIN', 2, 'Light', 'Easy to manage'),
(7, 'BAL,BUF', 2, 'Light', 'Elite QBs off'),
(8, 'JAX,LV,DET,ARI,SEA,LAR', 6, 'Byepocalypse', 'Many elite players off'),
(9, 'PHI,CLE,NYJ,TB', 4, 'Normal', 'Standard bye week'),
(10, 'KC,CIN,TEN,DAL', 4, 'Heavy', 'Chase and Lamb off'),
(11, 'IND,NO', 2, 'Light', 'Light week'),
(12, 'MIA,DEN,LAC,WAS', 4, 'Normal', 'Standard bye week'),
(14, 'NE,NYG,CAR,SF', 4, 'Heavy', 'Playoff week impact');