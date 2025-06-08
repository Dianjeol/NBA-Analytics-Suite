#!/usr/bin/env python3
"""
NBA Season Management System
===========================

Handles multiple NBA seasons with automatic season detection and updates.
New seasons are added every November 1st.

Author: NBA Analytics Suite
Version: 1.0.0
"""

import json
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SeasonInfo:
    """Data class for NBA season information."""
    season_id: str
    display_name: str
    start_date: datetime.date
    end_date: datetime.date
    is_current: bool
    data_file: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "season_id": self.season_id,
            "display_name": self.display_name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "is_current": self.is_current,
            "data_file": self.data_file
        }

class SeasonManager:
    """Manages NBA seasons with automatic detection and updates."""
    
    SEASONS_CONFIG_FILE = "seasons_config.json"
    
    def __init__(self):
        """Initialize season manager."""
        self.seasons: List[SeasonInfo] = []
        self.current_season: Optional[SeasonInfo] = None
        self._load_or_create_seasons()
    
    def _create_season(self, start_year: int) -> SeasonInfo:
        """Create a season info object for given start year."""
        end_year = start_year + 1
        season_id = f"{start_year}-{str(end_year)[2:]}"
        display_name = f"{start_year}-{end_year} NBA Season"
        start_date = datetime.date(start_year, 11, 1)
        end_date = datetime.date(end_year, 6, 30)
        
        return SeasonInfo(
            season_id=season_id,
            display_name=display_name,
            start_date=start_date,
            end_date=end_date,
            is_current=False
        )
    
    def _load_or_create_seasons(self):
        """Load existing seasons or create default configuration."""
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        
        # Determine base year for seasons
        if current_month >= 11:  # November or later
            base_year = current_year
        else:  # January to October
            base_year = current_year - 1
        
        # Create seasons from 2020 to current + 2
        for year in range(2020, base_year + 3):
            season = self._create_season(year)
            self.seasons.append(season)
        
        self._update_current_season()
    
    def _update_current_season(self):
        """Update which season is current based on today's date."""
        today = datetime.date.today()
        
        for season in self.seasons:
            season.is_current = False
            if season.start_date <= today <= season.end_date:
                season.is_current = True
                self.current_season = season
    
    def get_available_seasons(self) -> List[SeasonInfo]:
        """Get list of all available seasons."""
        return sorted(self.seasons, key=lambda s: s.start_date, reverse=True)
    
    def get_current_season(self) -> Optional[SeasonInfo]:
        """Get the current season."""
        return self.current_season
    
    def add_new_season_if_needed(self) -> bool:
        """Check if a new season should be added (on/after November 1st)."""
        today = datetime.date.today()
        
        if today.month >= 11:
            current_year = today.year
            season_id = f"{current_year}-{str(current_year + 1)[2:]}"
            
            # Check if season already exists
            if not any(s.season_id == season_id for s in self.seasons):
                new_season = self._create_season(current_year)
                self.seasons.append(new_season)
                self._update_current_season()
                return True
        
        return False

def main():
    """Demonstrate season manager functionality."""
    print("🏀 NBA Season Manager")
    print("=" * 50)
    
    manager = SeasonManager()
    
    if manager.add_new_season_if_needed():
        print("✅ New season added automatically!")
    
    print(f"\nCurrent Season: {manager.get_current_season().season_id}")
    print("\nAvailable Seasons:")
    for season in manager.get_available_seasons():
        marker = "→" if season.is_current else " "
        print(f"  {marker} {season.season_id}: {season.display_name}")

if __name__ == "__main__":
    main() 