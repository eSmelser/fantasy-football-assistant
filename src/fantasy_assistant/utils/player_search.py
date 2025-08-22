"""
Player search and validation utilities to prevent typos and improve UX.
"""

import re
from typing import List, Optional, Tuple
from difflib import SequenceMatcher, get_close_matches
from ..models.player import Player


class PlayerSearch:
    """
    Handles player name searching, validation, and typo correction.
    
    Provides fuzzy matching, autocomplete, and "did you mean?" suggestions
    to prevent draft errors from typos.
    """
    
    def __init__(self, players: List[Player]):
        """
        Initialize with list of available players.
        
        Args:
            players: List of Player objects to search through
        """
        self.players = players
        self._name_map = self._build_name_map()
        
    def _build_name_map(self) -> dict:
        """Build optimized name lookup map with variations."""
        name_map = {}
        
        for player in self.players:
            # Add exact name
            name_map[player.name.lower()] = player
            
            # Add variations (first+last, last name only, etc.)
            name_parts = player.name.split()
            if len(name_parts) >= 2:
                # First + Last (e.g. "Ja'Marr Chase" -> "jamarr chase")
                first_last = f"{name_parts[0]} {name_parts[-1]}".lower()
                name_map[first_last] = player
                
                # Last name only for unique cases
                last_name = name_parts[-1].lower()
                if last_name not in name_map:  # Only if unique
                    name_map[last_name] = player
                
                # Handle nicknames and abbreviations
                if "'" in player.name:  # Handle apostrophes
                    clean_name = player.name.replace("'", "").lower()
                    name_map[clean_name] = player
                    
        return name_map
    
    def find_player(self, search_term: str) -> Optional[Player]:
        """
        Find player by exact or fuzzy match.
        
        Args:
            search_term: Player name to search for
            
        Returns:
            Player object if found, None otherwise
        """
        if not search_term or not search_term.strip():
            return None
            
        search_term = search_term.strip().lower()
        
        # Try exact match first
        if search_term in self._name_map:
            return self._name_map[search_term]
        
        # Try fuzzy match
        matches = self.get_suggestions(search_term, limit=1, min_similarity=0.8)
        return matches[0] if matches else None
    
    def get_suggestions(self, search_term: str, limit: int = 5, 
                       min_similarity: float = 0.6) -> List[Player]:
        """
        Get player suggestions based on fuzzy matching.
        
        Args:
            search_term: Partial or misspelled player name
            limit: Maximum number of suggestions to return
            min_similarity: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            List of Player objects ordered by similarity
        """
        if not search_term or not search_term.strip():
            return []
            
        search_term = search_term.strip().lower()
        
        # Get close matches from name map
        close_names = get_close_matches(
            search_term, 
            self._name_map.keys(),
            n=limit * 2,  # Get more to filter by similarity
            cutoff=min_similarity
        )
        
        # Convert to players and sort by similarity
        suggestions = []
        for name in close_names:
            player = self._name_map[name]
            similarity = SequenceMatcher(None, search_term, name).ratio()
            suggestions.append((similarity, player))
        
        # Sort by similarity descending and return players
        suggestions.sort(key=lambda x: x[0], reverse=True)
        return [player for _, player in suggestions[:limit]]
    
    def autocomplete(self, partial_name: str, limit: int = 10) -> List[str]:
        """
        Provide autocomplete suggestions for partial player names.
        
        Args:
            partial_name: Partial player name being typed
            limit: Maximum suggestions to return
            
        Returns:
            List of player names that match the partial input
        """
        if not partial_name or len(partial_name) < 2:
            return []
            
        partial_lower = partial_name.lower().strip()
        matches = []
        
        for name, player in self._name_map.items():
            if name.startswith(partial_lower):
                matches.append(player.name)
        
        # Remove duplicates and sort
        unique_matches = list(set(matches))
        unique_matches.sort()
        
        return unique_matches[:limit]
    
    def search_by_position(self, position: str, limit: int = 20) -> List[Player]:
        """
        Get all available players at a specific position.
        
        Args:
            position: Position to filter by (QB, RB, WR, TE, K, DEF)
            limit: Maximum players to return
            
        Returns:
            List of available players at the position, sorted by rank
        """
        position_players = [
            p for p in self.players 
            if p.position.value.upper() == position.upper() and p.is_available
        ]
        
        # Sort by consensus rank (lower is better)
        position_players.sort(key=lambda p: p.consensus_rank or 999)
        
        return position_players[:limit]
    
    def validate_and_suggest(self, player_input: str) -> Tuple[Optional[Player], List[str]]:
        """
        Validate player input and provide suggestions if not found.
        
        Args:
            player_input: User's player name input
            
        Returns:
            Tuple of (found_player, suggestions_list)
            If player found: (Player, [])
            If not found: (None, [suggestion1, suggestion2, ...])
        """
        player = self.find_player(player_input)
        
        if player:
            return player, []
        
        # Player not found, provide suggestions
        suggestions = self.get_suggestions(player_input, limit=5)
        suggestion_names = [p.name for p in suggestions]
        
        return None, suggestion_names
    
    def get_available_players(self, sort_by: str = "rank") -> List[Player]:
        """
        Get all available (not drafted) players.
        
        Args:
            sort_by: How to sort results ("rank", "adp", "name", "position")
            
        Returns:
            List of available players sorted by specified criteria
        """
        available = [p for p in self.players if p.is_available]
        
        if sort_by == "rank":
            available.sort(key=lambda p: p.consensus_rank or 999)
        elif sort_by == "adp":
            available.sort(key=lambda p: p.adp or 999)
        elif sort_by == "name":
            available.sort(key=lambda p: p.name)
        elif sort_by == "position":
            available.sort(key=lambda p: (p.position.value, p.consensus_rank or 999))
        
        return available
    
    def search_with_filters(self, search_term: str = "", position: str = "", 
                           max_bye_week: int = 18, exclude_injured: bool = False,
                           limit: int = 20) -> List[Player]:
        """
        Advanced search with multiple filters.
        
        Args:
            search_term: Partial player name
            position: Position filter
            max_bye_week: Exclude players with bye week after this
            exclude_injured: Exclude players with injury designation
            limit: Maximum results to return
            
        Returns:
            Filtered list of players matching criteria
        """
        results = self.players.copy()
        
        # Apply filters
        if search_term:
            search_lower = search_term.lower()
            results = [p for p in results if search_lower in p.name.lower()]
            
        if position:
            results = [p for p in results if p.position.value.upper() == position.upper()]
            
        if max_bye_week < 18:
            results = [p for p in results if p.bye_week <= max_bye_week]
            
        if exclude_injured:
            results = [p for p in results if not p.is_injured]
            
        # Only available players
        results = [p for p in results if p.is_available]
        
        # Sort by rank
        results.sort(key=lambda p: p.consensus_rank or 999)
        
        return results[:limit]