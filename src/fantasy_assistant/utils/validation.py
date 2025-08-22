"""
Input validation utilities for the fantasy football draft assistant.
"""

import re
from typing import Union, List, Optional
from ..models.player import Position


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_draft_position(position: Union[str, int]) -> int:
    """
    Validate and convert draft position to integer.
    
    Args:
        position: Draft position as string or int
        
    Returns:
        Valid draft position as integer (1-12)
        
    Raises:
        ValidationError: If position is invalid
    """
    try:
        pos = int(position)
        if not 1 <= pos <= 12:
            raise ValidationError(f"Draft position must be between 1-12, got {pos}")
        return pos
    except (ValueError, TypeError):
        raise ValidationError(f"Draft position must be a number, got {position}")


def validate_position(position: str) -> Position:
    """
    Validate and convert position string to Position enum.
    
    Args:
        position: Position string (QB, RB, WR, TE, K, DEF)
        
    Returns:
        Position enum value
        
    Raises:
        ValidationError: If position is invalid
    """
    if not position:
        raise ValidationError("Position cannot be empty")
    
    try:
        return Position(position.upper())
    except ValueError:
        valid_positions = [p.value for p in Position]
        raise ValidationError(f"Position must be one of {valid_positions}, got {position}")


def validate_player_name(name: str) -> str:
    """
    Validate and clean player name input.
    
    Args:
        name: Player name to validate
        
    Returns:
        Cleaned player name
        
    Raises:
        ValidationError: If name is invalid
    """
    if not name or not name.strip():
        raise ValidationError("Player name cannot be empty")
    
    # Clean the name
    cleaned = name.strip()
    
    # Basic validation
    if len(cleaned) < 2:
        raise ValidationError("Player name must be at least 2 characters")
    
    if len(cleaned) > 50:
        raise ValidationError("Player name too long (max 50 characters)")
    
    # Check for valid characters (letters, spaces, apostrophes, hyphens, periods)
    if not re.match(r"^[a-zA-Z\s'\-\.]+$", cleaned):
        raise ValidationError("Player name contains invalid characters")
    
    return cleaned


def validate_round_number(round_num: Union[str, int]) -> int:
    """
    Validate draft round number.
    
    Args:
        round_num: Round number as string or int
        
    Returns:
        Valid round number as integer
        
    Raises:
        ValidationError: If round number is invalid
    """
    try:
        rnd = int(round_num)
        if not 1 <= rnd <= 16:  # Typical fantasy draft rounds
            raise ValidationError(f"Round number must be between 1-16, got {rnd}")
        return rnd
    except (ValueError, TypeError):
        raise ValidationError(f"Round number must be a number, got {round_num}")


def validate_bye_week(bye_week: Union[str, int]) -> int:
    """
    Validate NFL bye week number.
    
    Args:
        bye_week: Bye week as string or int
        
    Returns:
        Valid bye week as integer
        
    Raises:
        ValidationError: If bye week is invalid
    """
    try:
        week = int(bye_week)
        if not 1 <= week <= 18:  # NFL season weeks
            raise ValidationError(f"Bye week must be between 1-18, got {week}")
        return week
    except (ValueError, TypeError):
        raise ValidationError(f"Bye week must be a number, got {bye_week}")


def validate_team_abbreviation(team: str) -> str:
    """
    Validate NFL team abbreviation.
    
    Args:
        team: Team abbreviation
        
    Returns:
        Validated team abbreviation in uppercase
        
    Raises:
        ValidationError: If team abbreviation is invalid
    """
    if not team or not team.strip():
        raise ValidationError("Team abbreviation cannot be empty")
    
    team_upper = team.strip().upper()
    
    # List of valid NFL team abbreviations
    valid_teams = {
        'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
        'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
        'LV', 'LAC', 'LAR', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
        'NYJ', 'PHI', 'PIT', 'SF', 'SEA', 'TB', 'TEN', 'WAS'
    }
    
    if team_upper not in valid_teams:
        raise ValidationError(f"Invalid team abbreviation: {team}. Must be one of {sorted(valid_teams)}")
    
    return team_upper


def validate_draft_input(player_input: str, available_players: List[str]) -> str:
    """
    Comprehensive validation for draft input with suggestions.
    
    Args:
        player_input: User's player name input
        available_players: List of available player names
        
    Returns:
        Validated player name
        
    Raises:
        ValidationError: If input is invalid with suggestions
    """
    # Basic name validation
    cleaned_name = validate_player_name(player_input)
    
    # Check if player is in available list (case-insensitive)
    available_lower = [name.lower() for name in available_players]
    
    if cleaned_name.lower() not in available_lower:
        # Find close matches for suggestion
        from difflib import get_close_matches
        suggestions = get_close_matches(
            cleaned_name.lower(), 
            available_lower, 
            n=3, 
            cutoff=0.6
        )
        
        if suggestions:
            # Convert back to original case
            original_suggestions = []
            for suggestion in suggestions:
                for original in available_players:
                    if original.lower() == suggestion:
                        original_suggestions.append(original)
                        break
            
            raise ValidationError(
                f"Player '{cleaned_name}' not found. Did you mean: {', '.join(original_suggestions)}?"
            )
        else:
            raise ValidationError(f"Player '{cleaned_name}' not found in available players")
    
    # Return the original case version
    for original in available_players:
        if original.lower() == cleaned_name.lower():
            return original
    
    return cleaned_name  # Fallback


def validate_numeric_input(value: Union[str, int, float], 
                          min_value: Optional[float] = None,
                          max_value: Optional[float] = None,
                          allow_none: bool = False) -> Optional[float]:
    """
    Validate numeric input with optional range checking.
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_none: Whether None/empty values are allowed
        
    Returns:
        Validated numeric value
        
    Raises:
        ValidationError: If value is invalid
    """
    if value is None or value == "":
        if allow_none:
            return None
        else:
            raise ValidationError("Value cannot be empty")
    
    try:
        num_value = float(value)
        
        if min_value is not None and num_value < min_value:
            raise ValidationError(f"Value must be at least {min_value}, got {num_value}")
        
        if max_value is not None and num_value > max_value:
            raise ValidationError(f"Value must be at most {max_value}, got {num_value}")
        
        return num_value
        
    except (ValueError, TypeError):
        raise ValidationError(f"Value must be a number, got {value}")


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection attacks and clean formatting.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Sanitized input string
    """
    if not user_input:
        return ""
    
    # Strip whitespace
    sanitized = user_input.strip()
    
    # Remove potential SQL injection characters (basic protection)
    dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    return sanitized