#!/usr/bin/env python3
"""
Fantasy Football Draft Assistant
12-Team PPR League Helper with AI Recommendations

Features:
- Track drafted players
- Show best available by position
- AI-powered recommendations based on strategy
- Bye week conflict detection
- Injury status monitoring
- Real-time draft state management
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import requests


class FantasyDraftAssistant:
    def __init__(self, db_path: str = "fantasy_draft.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize database with schema and data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
        if not cursor.fetchone():
            # Read and execute schema only if tables don't exist
            if os.path.exists("database_schema.sql"):
                with open("database_schema.sql", 'r') as f:
                    conn.executescript(f.read())
                print("📊 Database schema created successfully")
            else:
                print("⚠️ database_schema.sql not found, creating minimal schema")
                # Create minimal schema inline
                cursor.execute("""
                    CREATE TABLE players (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        position TEXT NOT NULL,
                        team TEXT NOT NULL,
                        bye_week INTEGER,
                        consensus_rank INTEGER,
                        adp REAL,
                        injury_status TEXT DEFAULT 'Healthy',
                        notes TEXT
                    )
                """)
                cursor.execute("""
                    CREATE TABLE drafted_players (
                        id INTEGER PRIMARY KEY,
                        player_name TEXT NOT NULL,
                        position TEXT NOT NULL,
                        team TEXT NOT NULL,
                        pick_number INTEGER,
                        round INTEGER,
                        drafted_by_user BOOLEAN DEFAULT FALSE
                    )
                """)
                cursor.execute("""
                    CREATE TABLE user_roster (
                        id INTEGER PRIMARY KEY,
                        player_name TEXT NOT NULL,
                        position TEXT NOT NULL,
                        team TEXT NOT NULL,
                        bye_week INTEGER,
                        round_drafted INTEGER
                    )
                """)
                cursor.execute("""
                    CREATE TABLE draft_state (
                        id INTEGER PRIMARY KEY,
                        current_pick INTEGER DEFAULT 1,
                        current_round INTEGER DEFAULT 1,
                        user_draft_position INTEGER
                    )
                """)
        else:
            print("📊 Database already exists")
        
        conn.commit()
        conn.close()
    
    def load_player_data(self):
        """Load all compiled player data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing player data
        cursor.execute("DELETE FROM players")
        
        # Top consensus players with bye weeks and data
        players_data = [
            # Tier 1
            ("Ja'Marr Chase", "WR", "CIN", 10, 1, 1.5, 18.5, 0.28, 100, "Healthy", "Elite target share", None),
            ("Jahmyr Gibbs", "RB", "DET", 8, 2, 1.5, 16.8, 0.18, 52, "Healthy", "Pass-catching stud", "David Montgomery"),
            ("Justin Jefferson", "WR", "MIN", 6, 3, 3.0, 18.2, 0.26, 68, "Healthy", "Elite WR1", None),
            ("Bijan Robinson", "RB", "ATL", 5, 4, 3.0, 16.2, 0.15, 58, "Healthy", "3-down back", "Tyler Allgeier"),
            
            # Rising/Elite tier
            ("Ashton Jeanty", "RB", "LV", 8, 5, 7.5, 14.5, 0.12, 0, "Healthy", "Rookie rising fast", "Alexander Mattison"),
            ("Saquon Barkley", "RB", "PHI", 9, 6, 6.0, 15.8, 0.14, 47, "Healthy", "Fresh start", "Kenneth Gainwell"),
            ("Christian McCaffrey", "RB", "SF", 14, 7, 7.0, 17.2, 0.16, 67, "Questionable", "Injury concerns, playoff bye", "Jordan Mason"),
            ("CeeDee Lamb", "WR", "DAL", 10, 8, 8.0, 17.8, 0.31, 135, "Healthy", "Target monster", None),
            ("Malik Nabers", "WR", "NYG", 14, 9, 9.0, 15.5, 0.25, 0, "Healthy", "Rookie WR1, playoff bye", None),
            ("Puka Nacua", "WR", "LAR", 8, 10, 10.0, 16.2, 0.24, 105, "Healthy", "PPR machine", None),
            ("Amon-Ra St. Brown", "WR", "DET", 8, 11, 11.0, 15.8, 0.23, 119, "Healthy", "Slot king", None),
            ("Brian Thomas Jr.", "WR", "JAX", 8, 12, 12.0, 13.5, 0.20, 0, "Healthy", "Deep threat rookie", None),
            
            # Round 2 targets
            ("Derrick Henry", "RB", "BAL", 7, 13, 13.0, 14.2, 0.08, 15, "Healthy", "Goal line back", "Justice Hill"),
            ("Nico Collins", "WR", "HOU", 6, 14, 14.0, 14.8, 0.22, 80, "Healthy", "Target monster", None),
            ("De'Von Achane", "RB", "MIA", 12, 15, 15.0, 15.2, 0.13, 58, "Questionable", "Calf injury concern", "Raheem Mostert"),
            ("Alvin Kamara", "RB", "NO", 11, 16, 16.0, 13.8, 0.17, 75, "Healthy", "PPR veteran", "Jamaal Williams"),
            ("Breece Hall", "RB", "NYJ", 9, 17, 17.0, 14.5, 0.15, 76, "Healthy", "Bounce back year", "Braelon Allen"),
            ("A.J. Brown", "WR", "PHI", 9, 18, 18.0, 15.5, 0.21, 106, "Healthy", "Red zone threat", None),
            
            # QBs
            ("Josh Allen", "QB", "BUF", 7, 35, 35.0, 24.5, 0.0, 0, "Healthy", "Elite dual-threat", None),
            ("Lamar Jackson", "QB", "BAL", 7, 40, 40.0, 23.8, 0.0, 0, "Healthy", "Rushing upside", None),
            ("Anthony Richardson", "QB", "IND", 11, 42, 42.0, 22.5, 0.0, 0, "Healthy", "High ceiling", None),
            ("C.J. Stroud", "QB", "HOU", 6, 45, 45.0, 21.8, 0.0, 0, "Healthy", "Sophomore surge", None),
            
            # TEs
            ("Travis Kelce", "TE", "KC", 10, 25, 25.0, 12.8, 0.19, 93, "Healthy", "Elite TE", None),
            ("Mark Andrews", "TE", "BAL", 7, 28, 28.0, 11.5, 0.16, 55, "Healthy", "Bounce back", None),
            ("Sam LaPorta", "TE", "DET", 8, 30, 30.0, 11.2, 0.15, 86, "Healthy", "Sophomore success", None),
            ("Trey McBride", "TE", "ARI", 8, 32, 32.0, 10.8, 0.18, 81, "Healthy", "Target monster", None),
        ]
        
        # Insert player data
        for player in players_data:
            cursor.execute("""
                INSERT INTO players (name, position, team, bye_week, consensus_rank, adp, 
                                   ppg_projection, target_share, receptions_2024, injury_status, 
                                   notes, handcuff)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, player)
        
        # Load injury data
        injury_data = [
            ("Chris Godwin", "TB", "Ankle", "Out", "Until October", "Critical", "Avoid completely", "2025-08-22", "NFL.com"),
            ("Matthew Stafford", "LAR", "Back", "Questionable", "Week 1 uncertain", "Moderate", "Late round only", "2025-08-22", "ESPN"),
            ("De'Von Achane", "MIA", "Calf", "Questionable", "Preventative rest", "Minor", "Monitor closely", "2025-08-22", "Yahoo"),
            ("Isaiah Likely", "BAL", "Foot", "Out", "6+ weeks", "Moderate", "Draft replacement", "2025-08-22", "NBC Sports"),
        ]
        
        cursor.execute("DELETE FROM injury_reports")
        for injury in injury_data:
            cursor.execute("""
                INSERT INTO injury_reports (player_name, team, injury_type, status, timeline, 
                                          severity, fantasy_impact, report_date, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, injury)
        
        conn.commit()
        conn.close()
        print("✅ Player data loaded successfully")
    
    def set_draft_position(self, position: int):
        """Set user's draft position (1-12)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM draft_state")
        cursor.execute("""
            INSERT INTO draft_state (league_size, current_pick, current_round, user_draft_position)
            VALUES (12, 1, 1, ?)
        """, (position,))
        
        conn.commit()
        conn.close()
        print(f"🎯 Draft position set to #{position}")
    
    def draft_player(self, player_name: str, drafted_by_user: bool = False):
        """Record a player being drafted"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current draft state
        cursor.execute("SELECT current_pick, current_round FROM draft_state")
        current_pick, current_round = cursor.fetchone()
        
        # Get player info
        cursor.execute("SELECT position, team FROM players WHERE name = ?", (player_name,))
        result = cursor.fetchone()
        if not result:
            print(f"❌ Player '{player_name}' not found in database")
            conn.close()
            return
        
        position, team = result
        
        # Record the pick
        cursor.execute("""
            INSERT INTO drafted_players (player_name, position, team, pick_number, round, drafted_by_user)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (player_name, position, team, current_pick, current_round, drafted_by_user))
        
        # If drafted by user, add to roster
        if drafted_by_user:
            cursor.execute("SELECT bye_week FROM players WHERE name = ?", (player_name,))
            bye_week = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO user_roster (player_name, position, team, bye_week, round_drafted, pick_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (player_name, position, team, bye_week, current_round, current_pick))
        
        # Update draft state
        next_pick = current_pick + 1
        next_round = current_round
        if next_pick > 12:  # End of round
            next_pick = 1
            next_round += 1
        
        cursor.execute("""
            UPDATE draft_state 
            SET current_pick = ?, current_round = ?
        """, (next_pick, next_round))
        
        conn.commit()
        conn.close()
        
        status = "✅ YOUR PICK" if drafted_by_user else "📝 Drafted"
        print(f"{status}: {player_name} ({position}, {team}) - Pick {current_pick}, Round {current_round}")
    
    def get_best_available(self, position: str = None, limit: int = 10) -> List[Dict]:
        """Get best available players, optionally filtered by position"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get drafted players
        cursor.execute("SELECT player_name FROM drafted_players")
        drafted = [row[0] for row in cursor.fetchall()]
        
        # Build query
        query = """
            SELECT p.name, p.position, p.team, p.bye_week, p.consensus_rank, p.adp, 
                   p.injury_status, p.notes, i.status as injury_report
            FROM players p
            LEFT JOIN injury_reports i ON p.name = i.player_name
            WHERE p.name NOT IN ({})
        """.format(','.join('?' * len(drafted)))
        
        params = drafted.copy()
        
        if position:
            query += " AND p.position = ?"
            params.append(position)
        
        query += " ORDER BY p.consensus_rank LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        conn.close()
        
        players = []
        for row in results:
            players.append({
                'name': row[0],
                'position': row[1], 
                'team': row[2],
                'bye_week': row[3],
                'rank': row[4],
                'adp': row[5],
                'injury_status': row[6],
                'notes': row[7],
                'injury_report': row[8]
            })
        
        return players
    
    def get_ai_recommendation(self, num_recommendations: int = 3) -> Dict:
        """Generate AI-powered draft recommendation based on current state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current draft state
        cursor.execute("SELECT current_pick, current_round, user_draft_position FROM draft_state")
        current_pick, current_round, user_position = cursor.fetchone()
        
        # Get user's current roster
        cursor.execute("""
            SELECT position, COUNT(*) as count 
            FROM user_roster 
            GROUP BY position
        """)
        roster_counts = dict(cursor.fetchall())
        
        # Get best available overall
        best_available = self.get_best_available(limit=20)
        
        # Calculate needs
        needs = self._calculate_position_needs(roster_counts, current_round)
        
        # Get bye week conflicts for user's team
        bye_conflicts = self._check_bye_week_conflicts()
        
        conn.close()
        
        # AI reasoning logic
        recommendations = []
        
        for player in best_available[:10]:
            score = self._calculate_recommendation_score(
                player, current_round, needs, bye_conflicts, user_position, current_pick
            )
            
            if score > 0:
                recommendations.append({
                    'player': player,
                    'score': score,
                    'reasoning': self._generate_reasoning(player, current_round, needs, bye_conflicts)
                })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'current_situation': {
                'pick': current_pick,
                'round': current_round,
                'position': user_position,
                'roster_needs': needs
            },
            'recommendations': recommendations[:num_recommendations],
            'bye_week_alerts': bye_conflicts
        }
    
    def _calculate_position_needs(self, roster_counts: Dict, current_round: int) -> Dict:
        """Calculate position needs based on roster and round"""
        needs = {
            'QB': 1 - roster_counts.get('QB', 0),
            'RB': max(0, 3 - roster_counts.get('RB', 0)),  # Want 3+ RBs
            'WR': max(0, 3 - roster_counts.get('WR', 0)),  # Want 3+ WRs
            'TE': 1 - roster_counts.get('TE', 0),
            'K': 1 - roster_counts.get('K', 0),
            'DEF': 1 - roster_counts.get('DEF', 0)
        }
        
        # Adjust based on round
        if current_round <= 6:
            needs['K'] = 0  # Don't draft K early
            needs['DEF'] = 0  # Don't draft DEF early
        
        return needs
    
    def _check_bye_week_conflicts(self) -> List[str]:
        """Check for bye week conflicts in user's roster"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT bye_week, position, COUNT(*) as count
            FROM user_roster 
            GROUP BY bye_week, position
            HAVING count > 1
        """)
        
        conflicts = []
        for bye_week, position, count in cursor.fetchall():
            if bye_week == 8:
                conflicts.append(f"⚠️ Week 8 BYEPOCALYPSE: {count} {position}s")
            elif bye_week == 14:
                conflicts.append(f"⚠️ Week 14 PLAYOFFS: {count} {position}s")
            else:
                conflicts.append(f"Week {bye_week}: {count} {position}s")
        
        conn.close()
        return conflicts
    
    def _calculate_recommendation_score(self, player: Dict, current_round: int, 
                                      needs: Dict, bye_conflicts: List, 
                                      user_position: int, current_pick: int) -> float:
        """Calculate recommendation score for a player"""
        score = 0.0
        
        # Base value (inverse of consensus rank)
        if player['rank']:
            score += (200 - player['rank']) / 10
        
        # Position need multiplier
        position_need = needs.get(player['position'], 0)
        if position_need > 0:
            score *= (1 + position_need * 0.5)
        
        # Round appropriateness
        if player['position'] in ['QB'] and current_round < 6:
            score *= 0.3  # Penalize early QB
        elif player['position'] in ['K', 'DEF'] and current_round < 15:
            score *= 0.1  # Heavily penalize early K/DEF
        
        # Injury penalty
        if player['injury_status'] != 'Healthy':
            if player['injury_report'] == 'Out':
                score *= 0.2
            elif player['injury_report'] == 'Questionable':
                score *= 0.7
        
        # Bye week penalty
        if player['bye_week'] == 8:  # Byepocalypse week
            score *= 0.8
        elif player['bye_week'] == 14:  # Playoff week
            score *= 0.9
        
        return score
    
    def _generate_reasoning(self, player: Dict, current_round: int, 
                          needs: Dict, bye_conflicts: List) -> str:
        """Generate AI reasoning for recommendation"""
        reasons = []
        
        # Position need
        need = needs.get(player['position'], 0)
        if need > 0:
            reasons.append(f"Fills {player['position']} need")
        
        # Value
        if player['rank'] and player['rank'] <= current_round * 12:
            reasons.append("Good value at current ADP")
        
        # PPR specific
        if player['position'] in ['WR', 'RB'] and 'target' in player.get('notes', '').lower():
            reasons.append("PPR upside")
        
        # Injury concerns
        if player['injury_status'] != 'Healthy':
            reasons.append(f"⚠️ {player['injury_status']}")
        
        # Bye week
        if player['bye_week'] == 8:
            reasons.append("⚠️ Week 8 bye (Byepocalypse)")
        elif player['bye_week'] == 14:
            reasons.append("⚠️ Week 14 bye (Playoffs)")
        
        return " | ".join(reasons) if reasons else "Solid pick"
    
    def show_roster(self):
        """Display current user roster"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT player_name, position, team, bye_week, round_drafted
            FROM user_roster
            ORDER BY round_drafted, position
        """)
        
        roster = cursor.fetchall()
        conn.close()
        
        if not roster:
            print("📋 Your roster is empty")
            return
        
        print("\n📋 YOUR CURRENT ROSTER")
        print("=" * 50)
        for player_name, position, team, bye_week, round_drafted in roster:
            print(f"R{round_drafted:2d} | {player_name:20s} | {position:2s} {team:3s} | Bye {bye_week:2d}")
        
        # Show position counts
        cursor = sqlite3.connect(self.db_path).cursor()
        cursor.execute("""
            SELECT position, COUNT(*) as count
            FROM user_roster
            GROUP BY position
            ORDER BY position
        """)
        
        counts = cursor.fetchall()
        if counts:
            print("\nPosition Summary:")
            for pos, count in counts:
                print(f"  {pos}: {count}")
    
    def run_interactive_draft(self):
        """Run interactive draft interface"""
        print("🏈 FANTASY FOOTBALL DRAFT ASSISTANT")
        print("=" * 50)
        
        # Get draft position if not set
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_draft_position FROM draft_state")
        result = cursor.fetchone()
        
        if not result or not result[0]:
            while True:
                try:
                    position = int(input("Enter your draft position (1-12): "))
                    if 1 <= position <= 12:
                        self.set_draft_position(position)
                        break
                    else:
                        print("Please enter a number between 1 and 12")
                except ValueError:
                    print("Please enter a valid number")
        
        conn.close()
        
        print("\nCommands:")
        print("  'draft [player name]' - Record your pick")
        print("  'pick [player name]' - Record someone else's pick")  
        print("  'best' - Show best available overall")
        print("  'best [pos]' - Show best available by position (QB/RB/WR/TE)")
        print("  'recommend' - Get AI recommendation")
        print("  'roster' - Show your current roster")
        print("  'bye' - Check bye week conflicts")
        print("  'help' - Show commands")
        print("  'quit' - Exit")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    break
                elif command == 'help':
                    self._show_help()
                elif command == 'best':
                    self._show_best_available()
                elif command.startswith('best '):
                    position = command.split()[1].upper()
                    self._show_best_available(position)
                elif command == 'recommend':
                    self._show_recommendations()
                elif command == 'roster':
                    self.show_roster()
                elif command == 'bye':
                    self._show_bye_conflicts()
                elif command.startswith('draft '):
                    player_name = ' '.join(command.split()[1:]).title()
                    self.draft_player(player_name, drafted_by_user=True)
                elif command.startswith('pick '):
                    player_name = ' '.join(command.split()[1:]).title()
                    self.draft_player(player_name, drafted_by_user=False)
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting draft assistant...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_help(self):
        """Show help commands"""
        print("\n🎯 DRAFT ASSISTANT COMMANDS")
        print("=" * 40)
        print("draft [player]  - Record YOUR pick")
        print("pick [player]   - Record other team's pick")
        print("best           - Show top available players")
        print("best QB/RB/WR/TE - Show best by position")  
        print("recommend      - Get AI recommendation")
        print("roster         - Show your current roster")
        print("bye           - Check bye week conflicts")
        print("quit          - Exit program")
    
    def _show_best_available(self, position: str = None):
        """Show best available players"""
        players = self.get_best_available(position, limit=15)
        
        if not players:
            print("No players found")
            return
            
        title = f"BEST AVAILABLE {position}S" if position else "BEST AVAILABLE PLAYERS"
        print(f"\n📊 {title}")
        print("=" * 60)
        
        for i, player in enumerate(players, 1):
            injury_flag = "⚠️" if player['injury_status'] != 'Healthy' else ""
            bye_flag = "🚨" if player['bye_week'] in [8, 14] else ""
            
            print(f"{i:2d}. {player['name']:18s} | {player['position']:2s} {player['team']:3s} | "
                  f"Bye {player['bye_week']:2d} | Rank {player['rank']:3d} {injury_flag}{bye_flag}")
    
    def _show_recommendations(self):
        """Show AI recommendations"""
        rec_data = self.get_ai_recommendation()
        
        print(f"\n🤖 AI RECOMMENDATIONS - Pick {rec_data['current_situation']['pick']}, "
              f"Round {rec_data['current_situation']['round']}")
        print("=" * 60)
        
        for i, rec in enumerate(rec_data['recommendations'], 1):
            player = rec['player']
            print(f"\n{i}. {player['name']} ({player['position']}, {player['team']})")
            print(f"   Rank: {player['rank']} | Bye: {player['bye_week']} | Score: {rec['score']:.1f}")
            print(f"   💡 {rec['reasoning']}")
        
        if rec_data['bye_week_alerts']:
            print(f"\n🚨 BYE WEEK ALERTS:")
            for alert in rec_data['bye_week_alerts']:
                print(f"   {alert}")
    
    def _show_bye_conflicts(self):
        """Show bye week conflicts"""
        conflicts = self._check_bye_week_conflicts()
        
        if conflicts:
            print("\n🚨 BYE WEEK CONFLICTS")
            print("=" * 30)
            for conflict in conflicts:
                print(f"  {conflict}")
        else:
            print("✅ No bye week conflicts detected")


def main():
    """Main function to run the draft assistant"""
    assistant = FantasyDraftAssistant()
    
    # Load data if database is empty
    conn = sqlite3.connect(assistant.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players")
    player_count = cursor.fetchone()[0]
    conn.close()
    
    if player_count == 0:
        print("Loading player data...")
        assistant.load_player_data()
    
    # Run interactive draft
    assistant.run_interactive_draft()


if __name__ == "__main__":
    main()