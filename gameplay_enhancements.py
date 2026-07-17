# ==========================================
# gameplay_enhancements.py
# NBA Gameplay Enhancement Systems
# ==========================================

from typing import Dict, List, Tuple, Optional
import random


# ==========================
# HOME COURT ADVANTAGE
# ==========================

class HomeCourtAdvantage:
    """Manage home court advantage mechanics."""
    
    def __init__(self):
        self.home_team_bonus = 3.0  # Base 3-point advantage
        self.crowd_factor = 0.0     # Dynamic crowd impact
        self.fatigue_factor = 0.0   # Travel fatigue
    
    def calculate_home_bonus(self, home_team: str, away_team: str, 
                           back_to_back: bool = False) -> float:
        """Calculate home court advantage bonus."""
        bonus = self.home_team_bonus
        
        # Back-to-back penalty for away team
        if back_to_back:
            bonus += 1.5
        
        # Random variance
        bonus += random.uniform(-1.0, 1.0)
        
        return round(max(0, bonus), 1)
    
    def get_crowd_impact(self, home_record: Tuple[int, int]) -> float:
        """Calculate crowd impact based on home team record."""
        wins, losses = home_record
        win_pct = wins / max(1, wins + losses)
        
        # Better home record = louder crowd
        if win_pct >= 0.700:
            return 2.0
        elif win_pct >= 0.600:
            return 1.5
        elif win_pct >= 0.500:
            return 1.0
        else:
            return 0.5


# ==========================
# CLUTCH PERFORMANCE
# ==========================

class ClutchSystem:
    """Manage clutch player performance in 4th quarter."""
    
    def __init__(self):
        self.clutch_time_remaining = 300  # 5 minutes = clutch time
        self.clutch_margin = 10          # Within 10 points = clutch situation
    
    def is_clutch_situation(self, quarter: int, time_remaining: int, 
                          score_diff: int) -> bool:
        """Determine if current situation is clutch."""
        if quarter != 4:
            return False
        
        if time_remaining > self.clutch_time_remaining:
            return False
        
        if abs(score_diff) > self.clutch_margin:
            return False
        
        return True
    
    def calculate_clutch_boost(self, player: Dict, situation: bool) -> float:
        """Calculate clutch performance boost for player."""
        if not situation:
            return 0.0
        
        clutch_rating = player.get("clutch", 75)
        overall = player.get("overall", 75)
        
        # High clutch players get bigger boost
        if clutch_rating >= 90:
            boost = 8.0
        elif clutch_rating >= 85:
            boost = 5.0
        elif clutch_rating >= 80:
            boost = 3.0
        else:
            boost = 1.0
        
        # Stars perform better in clutch
        if overall >= 85:
            boost *= 1.2
        
        return round(boost, 1)
    
    def get_clutch_moment_description(self, time_remaining: int, score_diff: int) -> str:
        """Get description of clutch moment."""
        if time_remaining < 60:
            if abs(score_diff) <= 3:
                return "FINAL SECONDS DRAMA"
            elif score_diff > 0:
                return "LAST CHANCE FOR TRAILING TEAM"
            else:
                return "LEADING TEAM TRYING TO CLOSE IT OUT"
        elif time_remaining < 120:
            return "CRUNCH TIME"
        else:
            return "CLUTCH SITUATION"


# ==========================
# HOT/COLD STREAKS
# ==========================

class StreakSystem:
    """Track player hot and cold streaks."""
    
    def __init__(self):
        self.player_streaks = {}  # {player_name: {"type": "hot"/"cold", "length": int, "shots": []}}
    
    def record_shot(self, player_name: str, made: bool):
        """Record a shot result for streak tracking."""
        if player_name not in self.player_streaks:
            self.player_streaks[player_name] = {"type": None, "length": 0, "shots": []}
        
        streak = self.player_streaks[player_name]
        streak["shots"].append(made)
        
        # Keep last 10 shots
        if len(streak["shots"]) > 10:
            streak["shots"] = streak["shots"][-10:]
        
        # Update streak
        recent_shots = streak["shots"][-5:]  # Last 5 shots determine streak
        
        if all(recent_shots):
            streak["type"] = "hot"
            streak["length"] = len([s for s in streak["shots"][-10:] if s])
        elif not any(recent_shots):
            streak["type"] = "cold"
            streak["length"] = len([s for s in streak["shots"][-10:] if not s])
        else:
            streak["type"] = None
            streak["length"] = 0
    
    def get_streak_bonus(self, player_name: str) -> float:
        """Get performance bonus based on streak."""
        if player_name not in self.player_streaks:
            return 0.0
        
        streak = self.player_streaks[player_name]
        
        if streak["type"] == "hot":
            # Hot streak bonus
            if streak["length"] >= 5:
                return 5.0
            elif streak["length"] >= 3:
                return 3.0
            else:
                return 1.0
        elif streak["type"] == "cold":
            # Cold streak penalty
            if streak["length"] >= 5:
                return -5.0
            elif streak["length"] >= 3:
                return -3.0
            else:
                return -1.0
        
        return 0.0
    
    def get_streak_description(self, player_name: str) -> str:
        """Get description of player's current streak."""
        if player_name not in self.player_streaks:
            return ""
        
        streak = self.player_streaks[player_name]
        
        if streak["type"] == "hot":
            return f"🔥 ON FIRE ({streak['length']} made shots)"
        elif streak["type"] == "cold":
            return f"❄️ ICE COLD ({streak['length']} missed shots)"
        else:
            return ""


# ==========================
# MOMENTUM METER
# ==========================

class MomentumSystem:
    """Track game momentum between teams."""
    
    def __init__(self):
        self.momentum = {}  # {team: momentum_value (-100 to 100)}
        self.run_history = {}  # {team: [run_lengths]}
    
    def initialize_game(self, team1: str, team2: str):
        """Initialize momentum for a new game."""
        self.momentum = {team1: 0, team2: 0}
        self.run_history = {team1: [], team2: []}
    
    def update_momentum(self, scoring_team: str, points: int, consecutive: int):
        """Update momentum after a score."""
        if scoring_team not in self.momentum:
            return
        
        # Scoring team gains momentum
        self.momentum[scoring_team] += points * 2
        
        # Consecutive scores boost momentum more
        if consecutive >= 3:
            self.momentum[scoring_team] += consecutive * 3
        elif consecutive >= 2:
            self.momentum[scoring_team] += consecutive * 2
        
        # Other team loses momentum
        other_team = [t for t in self.momentum.keys() if t != scoring_team][0]
        self.momentum[other_team] -= points
        
        # Clamp momentum
        for team in self.momentum:
            self.momentum[team] = max(-100, min(100, self.momentum[team]))
        
        # Track runs
        if consecutive >= 5:
            self.run_history[scoring_team].append(consecutive)
    
    def get_momentum_bonus(self, team: str) -> float:
        """Get performance bonus based on momentum."""
        if team not in self.momentum:
            return 0.0
        
        momentum = self.momentum[team]
        
        # Momentum affects shooting and defense
        if momentum >= 50:
            return 4.0
        elif momentum >= 25:
            return 2.0
        elif momentum <= -50:
            return -4.0
        elif momentum <= -25:
            return -2.0
        
        return 0.0
    
    def get_momentum_description(self, team: str) -> str:
        """Get description of team's momentum."""
        if team not in self.momentum:
            return "NEUTRAL"
        
        momentum = self.momentum[team]
        
        if momentum >= 75:
            return "🚀 UNSTOPPABLE"
        elif momentum >= 50:
            return "🔥 HUGE MOMENTUM"
        elif momentum >= 25:
            return "⬆️ BUILDING MOMENTUM"
        elif momentum <= -75:
            return "💀 COMPLETELY STALLED"
        elif momentum <= -50:
            return "📉 LOSING STEAM"
        elif momentum <= -25:
            return "⬇️ LOSING MOMENTUM"
        else:
            return "➡️ NEUTRAL"


# ==========================
# TEAM CHEMISTRY
# ==========================

class ChemistrySystem:
    """Manage team chemistry bonuses."""
    
    def __init__(self):
        self.team_chemistry = {}  # {team: chemistry_value (0-100)}
        self.player_relationships = {}  # {(player1, player2): relationship_score}
    
    def initialize_team(self, team: str, players: List[Dict]):
        """Initialize chemistry for a team."""
        # Base chemistry from morale
        avg_morale = sum(p.get("morale", 75) for p in players) / max(1, len(players))
        
        # Chemistry affected by playing time consistency
        chemistry = avg_morale * 0.7 + 25  # Base 25 + morale impact
        
        self.team_chemistry[team] = round(max(0, min(100, chemistry)), 1)
    
    def update_chemistry(self, team: str, win: bool, margin: int):
        """Update chemistry after a game."""
        if team not in self.team_chemistry:
            return
        
        chemistry = self.team_chemistry[team]
        
        if win:
            # Wins improve chemistry
            boost = min(5, margin * 0.5)
            chemistry = min(100, chemistry + boost)
        else:
            # Losses decrease chemistry
            penalty = min(5, abs(margin) * 0.3)
            chemistry = max(0, chemistry - penalty)
        
        self.team_chemistry[team] = round(chemistry, 1)
    
    def get_chemistry_bonus(self, team: str) -> float:
        """Get team chemistry bonus."""
        if team not in self.team_chemistry:
            return 0.0
        
        chemistry = self.team_chemistry[team]
        
        # High chemistry = better teamwork
        if chemistry >= 85:
            return 3.0
        elif chemistry >= 70:
            return 2.0
        elif chemistry >= 55:
            return 1.0
        elif chemistry <= 40:
            return -2.0
        else:
            return 0.0
    
    def get_chemistry_description(self, team: str) -> str:
        """Get description of team chemistry."""
        if team not in self.team_chemistry:
            return "UNKNOWN"
        
        chemistry = self.team_chemistry[team]
        
        if chemistry >= 90:
            return "💎 ELITE CHEMISTRY"
        elif chemistry >= 80:
            return "🤝 EXCELLENT"
        elif chemistry >= 70:
            return "👍 GOOD"
        elif chemistry >= 55:
            return "😐 AVERAGE"
        elif chemistry >= 40:
            return "😕 POOR"
        else:
            return "💔 TOXIC"


# ==========================
# GAMEPLAY MANAGER
# ==========================

class GameplayManager:
    """Coordinate all gameplay enhancement systems."""
    
    def __init__(self):
        self.home_court = HomeCourtAdvantage()
        self.clutch = ClutchSystem()
        self.streaks = StreakSystem()
        self.momentum = MomentumSystem()
        self.chemistry = ChemistrySystem()
    
    def initialize_game(self, team1: str, team2: str, team1_players: List[Dict], 
                       team2_players: List[Dict], team1_record: Tuple[int, int],
                       team2_record: Tuple[int, int], back_to_back: bool = False):
        """Initialize all systems for a new game."""
        # Initialize momentum
        self.momentum.initialize_game(team1, team2)
        
        # Initialize chemistry
        self.chemistry.initialize_team(team1, team1_players)
        self.chemistry.initialize_team(team2, team2_players)
        
        # Calculate home court advantage (team1 is home)
        self.home_bonus = self.home_court.calculate_home_bonus(
            team1, team2, back_to_back
        )
        
        # Store game context
        self.home_team = team1
        self.away_team = team2
        self.team1_record = team1_record
        self.team2_record = team2_record
    
    def get_player_boost(self, player: Dict, team: str, quarter: int, 
                        time_remaining: int, score_diff: int) -> Dict[str, float]:
        """Get total performance boost for a player."""
        boosts = {
            "home_court": 0.0,
            "clutch": 0.0,
            "streak": 0.0,
            "momentum": 0.0,
            "chemistry": 0.0,
            "total": 0.0
        }
        
        # Home court advantage
        if team == self.home_team:
            boosts["home_court"] = self.home_bonus * 0.3
        
        # Clutch boost
        is_clutch = self.clutch.is_clutch_situation(quarter, time_remaining, score_diff)
        boosts["clutch"] = self.clutch.calculate_clutch_boost(player, is_clutch)
        
        # Streak bonus
        boosts["streak"] = self.streaks.get_streak_bonus(player["name"])
        
        # Momentum bonus
        boosts["momentum"] = self.momentum.get_momentum_bonus(team) * 0.5
        
        # Chemistry bonus
        boosts["chemistry"] = self.chemistry.get_chemistry_bonus(team) * 0.3
        
        # Calculate total
        boosts["total"] = sum(boosts.values())
        
        return boosts
    
    def record_shot(self, player_name: str, team: str, made: bool, points: int):
        """Record a shot and update relevant systems."""
        # Update streaks
        self.streaks.record_shot(player_name, made)
        
        # Update momentum if made
        if made:
            consecutive = self.streaks.player_streaks.get(player_name, {}).get("length", 0)
            self.momentum.update_momentum(team, points, consecutive)
    
    def end_game(self, winner: str, loser: str, margin: int):
        """Update systems after game completion."""
        # Update chemistry
        self.chemistry.update_chemistry(winner, True, margin)
        self.chemistry.update_chemistry(loser, False, margin)
        
        # Reset streaks for next game
        self.streaks.player_streaks = {}


# ==========================
# GAMEPLAY DISPLAY
# ==========================

class GameplayDisplay:
    """Display gameplay enhancement information."""
    
    def __init__(self, gameplay_manager: GameplayManager):
        self.manager = gameplay_manager
    
    def display_game_status(self, team1: str, team2: str, quarter: int, 
                          time_remaining: int, score1: int, score2: int):
        """Display current game status with enhancements."""
        from colors import RESET, BOLD, CYAN, GREEN, RED, YELLOW, WHITE
        
        score_diff = score1 - score2
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  🏀 GAME STATUS - Q{quarter} {time_remaining//60}:{time_remaining%60:02d}")
        print(f"{'='*70}{RESET}\n")
        
        # Momentum display
        mom1 = self.manager.momentum.get_momentum_description(team1)
        mom2 = self.manager.momentum.get_momentum_description(team2)
        
        print(f"  {team1}: {score1}  {mom1}")
        print(f"  {team2}: {score2}  {mom2}")
        
        # Clutch situation
        is_clutch = self.manager.clutch.is_clutch_situation(quarter, time_remaining, score_diff)
        if is_clutch:
            clutch_desc = self.manager.clutch.get_clutch_moment_description(time_remaining, score_diff)
            print(f"\n  {RED}{BOLD}⚡ {clutch_desc}{RESET}")
        
        # Chemistry
        chem1 = self.manager.chemistry.get_chemistry_description(team1)
        chem2 = self.manager.chemistry.get_chemistry_description(team2)
        
        print(f"\n  Chemistry: {team1} {chem1} | {team2} {chem2}")
        
        print(f"\n{BOLD}{CYAN}{'='*70}{RESET}\n")
    
    def display_player_boosts(self, player: Dict, team: str, quarter: int,
                             time_remaining: int, score_diff: int):
        """Display current boosts for a player."""
        from colors import RESET, BOLD, GREEN, RED, YELLOW, WHITE
        
        boosts = self.manager.get_player_boost(player, team, quarter, time_remaining, score_diff)
        
        print(f"  {player['name']} Boosts:")
        
        for boost_type, value in boosts.items():
            if boost_type == "total":
                continue
            
            color = GREEN if value > 0 else RED if value < 0 else WHITE
            symbol = "+" if value > 0 else ""
            print(f"    {boost_type}: {color}{symbol}{value}{RESET}")
        
        print(f"    {BOLD}Total: {GREEN if boosts['total'] > 0 else RED}{boosts['total']}{RESET}")


# ==========================
# INITIALIZATION
# ==========================

gameplay_manager = GameplayManager()
gameplay_display = GameplayDisplay(gameplay_manager)
