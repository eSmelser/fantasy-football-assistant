#!/usr/bin/env python3
"""Test script for the Fantasy Draft Assistant"""

from draft_assistant import FantasyDraftAssistant

def test_assistant():
    """Test the basic functionality"""
    assistant = FantasyDraftAssistant()
    assistant.load_player_data()
    
    # Test setting draft position
    assistant.set_draft_position(8)
    
    # Test getting best available
    print("🎯 TESTING BEST AVAILABLE")
    best = assistant.get_best_available(limit=5)
    for player in best:
        print(f"  {player['name']} ({player['position']}, {player['team']}) - Rank {player['rank']}")
    
    # Test drafting a player
    print("\n📝 TESTING DRAFT FUNCTIONALITY")
    assistant.draft_player("Ja'Marr Chase", drafted_by_user=True)
    assistant.draft_player("Bijan Robinson", drafted_by_user=False)
    
    # Test AI recommendation
    print("\n🤖 TESTING AI RECOMMENDATIONS")
    recommendations = assistant.get_ai_recommendation()
    
    print(f"Current pick: {recommendations['current_situation']['pick']}")
    print(f"Round: {recommendations['current_situation']['round']}")
    
    for i, rec in enumerate(recommendations['recommendations'][:3], 1):
        player = rec['player']
        print(f"  {i}. {player['name']} ({player['position']}) - Score: {rec['score']:.1f}")
        print(f"     💡 {rec['reasoning']}")
    
    # Show roster
    print("\n📋 TESTING ROSTER DISPLAY")
    assistant.show_roster()
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_assistant()