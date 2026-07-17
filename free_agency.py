# ==========================================
# free_agency.py
# NBA Free Agency System
# ==========================================

from typing import Dict, List, Tuple, Optional
from salary_cap import salary_config, SalaryCapCalculator, format_currency
from contracts import Contract, ContractGenerator, ContractManager
from luxury_tax import ApronRestrictions, ApronAlerts


# ==========================
# FREE AGENT CLASS
# ==========================

class FreeAgent:
    """Represents a free agent player."""
    
    def __init__(self, player_data: Dict):
        self.player_name = player_data.get("name", "Unknown")
        self.position = player_data.get("pos", "G")
        self.overall = player_data.get("overall", 75)
        self.age = player_data.get("age", 25)
        self.experience = player_data.get("experience", 5)
        self.previous_team = player_data.get("previous_team", None)
        
        # Contract preferences
        self.desired_salary = self._calculate_desired_salary()
        self.minimum_acceptable = self.desired_salary * 0.8
        self.preferred_years = random.randint(2, 4)
        self.bird_rights = player_data.get("bird_rights", False)
        
        # Free agent type
        self.fa_type = self._determine_fa_type()
    
    def _calculate_desired_salary(self) -> float:
        """Calculate desired salary based on overall and experience."""
        from salary_cap import get_salary_for_ovr
        return get_salary_for_ovr(self.overall, self.experience)
    
    def _determine_fa_type(self) -> str:
        """Determine type of free agent."""
        if self.bird_rights:
            return "bird"
        elif self.experience <= 2:
            return "restricted"
        else:
            return "unrestricted"
    
    def will_accept_offer(self, salary: float, years: int, team: str) -> Tuple[bool, str]:
        """Determine if player will accept contract offer."""
        # Salary too low
        if salary < self.minimum_acceptable:
            return False, f"Salary ${salary:.2f}M below minimum ${self.minimum_acceptable:.2f}M"
        
        # Years too short
        if years < 1:
            return False, "Contract must be at least 1 year"
        
        # Star players prefer longer deals
        if self.overall >= 85 and years < 2:
            return False, "Star player prefers multi-year deal"
        
        # Market factors (simplified)
        salary_match = salary / self.desired_salary
        
        if salary_match >= 1.2:
            return True, "Excellent offer - player accepts"
        elif salary_match >= 1.0:
            return True, "Good offer - player accepts"
        elif salary_match >= 0.9:
            # May accept if years are longer
            if years >= self.preferred_years:
                return True, "Acceptable with extra years"
            else:
                return False, "Salary slightly below asking, needs more years"
        else:
            return False, "Salary too low"


# ==========================
# FREE AGENCY MANAGER
# ==========================

class FreeAgencyManager:
    """Manage free agency signings and negotiations."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
        self.calculator = SalaryCapCalculator()
        self.apron = ApronRestrictions()
        self.alerts = ApronAlerts()
        self.free_agents = []  # List of FreeAgent objects
        self.signing_history = []  # Track all signings
    
    def add_free_agent(self, player_data: Dict):
        """Add a player to free agency."""
        fa = FreeAgent(player_data)
        self.free_agents.append(fa)
    
    def remove_free_agent(self, player_name: str):
        """Remove player from free agency (signed)."""
        self.free_agents = [fa for fa in self.free_agents if fa.player_name != player_name]
    
    def get_free_agents_by_position(self, position: str) -> List[FreeAgent]:
        """Get free agents filtered by position."""
        return [fa for fa in self.free_agents if fa.position == position]
    
    def get_free_agents_by_ovr(self, min_ovr: int, max_ovr: int = 99) -> List[FreeAgent]:
        """Get free agents filtered by overall rating."""
        return [fa for fa in self.free_agents if min_ovr <= fa.overall <= max_ovr]
    
    def can_sign_player(self, team: str, salary: float, years: int) -> Tuple[bool, str]:
        """Check if team can legally sign a player."""
        payroll = self.contract_manager.get_team_payroll(team)
        apron_status = self.apron.get_apron_status(payroll)
        
        # Check cap space
        if not apron_status["over_cap"]:
            # Under cap - can use cap space
            if self.calculator.can_sign_with_cap_space(payroll, salary):
                return True, "Can sign using cap space"
            else:
                return False, f"Insufficient cap space (need ${salary:.2f}M, have ${self.calculator.calculate_cap_space(payroll):.2f}M)"
        
        # Over cap - need exception
        can_use_mle, mle_type = self.calculator.can_use_mle(payroll)
        if can_use_mle:
            if mle_type == "non_taxpayer_mle" and salary <= salary_config.mle_non_taxpayer:
                return True, "Can sign using Non-Taxpayer MLE"
            elif mle_type == "taxpayer_mle" and salary <= salary_config.mle_taxpayer:
                return True, "Can sign using Taxpayer MLE"
        
        # Check BAE
        can_use_bae, _ = self.calculator.can_use_bae(payroll)
        if can_use_bae and salary <= salary_config.bae:
            return True, "Can sign using Bi-Annual Exception"
        
        # Check minimum salary
        if salary <= salary_config.min_salary:
            return True, "Can sign using Minimum Salary Exception"
        
        # Check Bird Rights
        # This would require checking if player has bird rights with this team
        # For now, return false
        return False, "No available exception for this salary amount"
    
    def sign_player(self, team: str, free_agent: FreeAgent, salary: float, years: int) -> Tuple[bool, str]:
        """Attempt to sign a free agent."""
        # Check if player accepts offer
        will_accept, reason = free_agent.will_accept_offer(salary, years, team)
        if not will_accept:
            return False, f"Player rejected offer: {reason}"
        
        # Check if team can legally sign
        can_sign, legal_reason = self.can_sign_player(team, salary, years)
        if not can_sign:
            return False, f"Cannot sign legally: {legal_reason}"
        
        # Check apron restrictions
        payroll = self.contract_manager.get_team_payroll(team)
        new_payroll = payroll + salary
        warning = self.alerts.get_warning_message(f"sign {free_agent.player_name}", new_payroll)
        if warning:
            return False, warning
        
        # Create contract
        contract = Contract(
            player_name=free_agent.player_name,
            team=team,
            years_remaining=years,
            annual_salary=salary,
            guaranteed=True,
            bird_rights=free_agent.bird_rights,
            contract_type="veteran"
        )
        
        # Add contract
        self.contract_manager.add_contract(contract)
        
        # Remove from free agency
        self.remove_free_agent(free_agent.player_name)
        
        # Record signing
        self.signing_history.append({
            "player": free_agent.player_name,
            "team": team,
            "salary": salary,
            "years": years,
            "previous_team": free_agent.previous_team
        })
        
        return True, f"Successfully signed {free_agent.player_name} to {years}-year, ${salary:.2f}M contract"
    
    def offer_contract(self, team: str, free_agent: FreeAgent, salary: float, years: int) -> Tuple[bool, str]:
        """Make a contract offer (for negotiation phase)."""
        # Check if player accepts
        will_accept, reason = free_agent.will_accept_offer(salary, years, team)
        
        if will_accept:
            # Check legal signing
            can_sign, legal_reason = self.can_sign_player(team, salary, years)
            if not can_sign:
                return False, f"Player accepts but illegal: {legal_reason}"
            
            return True, f"Player accepts offer - proceed to sign"
        else:
            return False, f"Player rejects: {reason}"
    
    def get_available_free_agents(self) -> List[FreeAgent]:
        """Get all available free agents sorted by overall."""
        return sorted(self.free_agents, key=lambda x: x.overall, reverse=True)
    
    def get_team_free_agents(self, team: str) -> List[FreeAgent]:
        """Get free agents who previously played for this team (for Bird Rights)."""
        return [fa for fa in self.free_agents if fa.previous_team == team]


# ==========================
# EXCEPTION TRACKING
# ==========================

class ExceptionTracker:
    """Track which exceptions teams have used."""
    
    def __init__(self):
        self.used_exceptions = {}  # {team: {exception_type: used_amount}}
    
    def use_exception(self, team: str, exception_type: str, amount: float) -> Tuple[bool, str]:
        """Record that a team used an exception."""
        if team not in self.used_exceptions:
            self.used_exceptions[team] = {}
        
        if exception_type not in self.used_exceptions[team]:
            self.used_exceptions[team][exception_type] = 0.0
        
        # Check exception limits
        if exception_type == "non_taxpayer_mle":
            if self.used_exceptions[team][exception_type] + amount > salary_config.mle_non_taxpayer:
                return False, f"Would exceed Non-Taxpayer MLE limit of ${salary_config.mle_non_taxpayer:.2f}M"
        elif exception_type == "taxpayer_mle":
            if self.used_exceptions[team][exception_type] + amount > salary_config.mle_taxpayer:
                return False, f"Would exceed Taxpayer MLE limit of ${salary_config.mle_taxpayer:.2f}M"
        elif exception_type == "bae":
            if self.used_exceptions[team][exception_type] + amount > salary_config.bae:
                return False, f"Would exceed BAE limit of ${salary_config.bae:.2f}M"
        
        self.used_exceptions[team][exception_type] += amount
        return True, f"Used {exception_type}: ${amount:.2f}M"
    
    def get_remaining_exception(self, team: str, exception_type: str) -> float:
        """Get remaining amount for an exception."""
        if team not in self.used_exceptions or exception_type not in self.used_exceptions[team]:
            used = 0.0
        else:
            used = self.used_exceptions[team][exception_type]
        
        if exception_type == "non_taxpayer_mle":
            return round(salary_config.mle_non_taxpayer - used, 2)
        elif exception_type == "taxpayer_mle":
            return round(salary_config.mle_taxpayer - used, 2)
        elif exception_type == "bae":
            return round(salary_config.bae - used, 2)
        
        return 0.0
    
    def reset_exceptions(self, team: str):
        """Reset exceptions for a team (new season)."""
        if team in self.used_exceptions:
            self.used_exceptions[team] = {}


# ==========================
# BIRD RIGHTS SYSTEM
# ==========================

class BirdRights:
    """Manage Bird Rights for free agents."""
    
    def __init__(self):
        self.bird_rights_tracking = {}  # {player_name: {team: years_played}}
    
    def add_year(self, player_name: str, team: str):
        """Add a year of service for Bird Rights."""
        if player_name not in self.bird_rights_tracking:
            self.bird_rights_tracking[player_name] = {}
        
        if team not in self.bird_rights_tracking[player_name]:
            self.bird_rights_tracking[player_name][team] = 0
        
        self.bird_rights_tracking[player_name][team] += 1
    
    def has_bird_rights(self, player_name: str, team: str) -> bool:
        """Check if team has Bird Rights for player."""
        if player_name not in self.bird_rights_tracking:
            return False
        
        if team not in self.bird_rights_tracking[player_name]:
            return False
        
        return self.bird_rights_tracking[player_name][team] >= 3
    
    def get_bird_type(self, player_name: str, team: str) -> str:
        """Determine type of Bird Rights."""
        if not self.has_bird_rights(player_name, team):
            return "none"
        
        years = self.bird_rights_tracking[player_name][team]
        
        if years >= 3:
            return "full_bird"
        elif years >= 2:
            return "early_bird"
        else:
            return "none"
    
    def get_bird_max_salary(self, player_name: str, team: str, current_salary: float) -> float:
        """Get maximum salary team can offer with Bird Rights."""
        bird_type = self.get_bird_type(player_name, team)
        
        if bird_type == "full_bird":
            # Can offer up to max contract or 105% of previous salary
            return max(current_salary * 1.05, salary_config.max_contract[2])
        elif bird_type == "early_bird":
            # Can offer up to 175% of previous salary or league average
            return current_salary * 1.75
        else:
            return current_salary


# ==========================
# RESTRICTED FREE AGENCY
# ==========================

class RestrictedFreeAgency:
    """Handle restricted free agent offer sheets."""
    
    def __init__(self):
        self.offer_sheets = []  # List of pending offer sheets
        self.matching_rights = {}  # {player_name: original_team}
    
    def submit_offer_sheet(self, player_name: str, offering_team: str, 
                          salary: float, years: int, original_team: str) -> Tuple[bool, str]:
        """Submit an offer sheet for a restricted free agent."""
        # Check if player is restricted
        if player_name not in self.matching_rights:
            return False, "Player is not a restricted free agent"
        
        if self.matching_rights[player_name] != original_team:
            return False, "Original team mismatch"
        
        # Check for existing offer sheet
        for offer in self.offer_sheets:
            if offer["player"] == player_name:
                return False, "Player already has a pending offer sheet"
        
        # Create offer sheet
        self.offer_sheets.append({
            "player": player_name,
            "offering_team": offering_team,
            "original_team": original_team,
            "salary": salary,
            "years": years,
            "matched": False
        })
        
        return True, f"Offer sheet submitted for {player_name}"
    
    def match_offer(self, player_name: str) -> Tuple[bool, str]:
        """Original team matches offer sheet."""
        for offer in self.offer_sheets:
            if offer["player"] == player_name and not offer["matched"]:
                offer["matched"] = True
                return True, f"{offer['original_team']} matched offer for {player_name}"
        
        return False, "No matching offer sheet found"
    
    def decline_match(self, player_name: str) -> Tuple[bool, str]:
        """Original team declines to match offer sheet."""
        for offer in self.offer_sheets:
            if offer["player"] == player_name and not offer["matched"]:
                offer["matched"] = False  # Explicitly declined
                return True, f"{offer['original_team']} declined to match - player signs with {offer['offering_team']}"
        
        return False, "No matching offer sheet found"
    
    def set_restricted(self, player_name: str, original_team: str):
        """Mark a player as restricted free agent."""
        self.matching_rights[player_name] = original_team


# ==========================
# FREE AGENCY DISPLAY
# ==========================

class FreeAgencyDisplay:
    """Display free agency information."""
    
    def __init__(self, fa_manager: FreeAgencyManager):
        self.fa_manager = fa_manager
    
    def display_free_agents(self, position_filter: str = None, min_ovr: int = 0):
        """Display available free agents."""
        from colors import RESET, BOLD, GREEN, YELLOW, CYAN, WHITE
        
        agents = self.fa_manager.get_available_free_agents()
        
        if position_filter:
            agents = [fa for fa in agents if fa.position == position_filter]
        
        if min_ovr > 0:
            agents = [fa for fa in agents if fa.overall >= min_ovr]
        
        print(f"\n{BOLD}{CYAN}  🏀 FREE AGENCY MARKET{RESET}")
        print(f"{'═'*70}")
        
        if not agents:
            print(f"  No free agents available.")
            print(f"{'═'*70}\n")
            return
        
        print(f"  {'PLAYER':<20} {'POS':>3} {'OVR':>3} {'AGE':>3} {'EXP':>3} {'TYPE':<12} {'ASKING':>8}")
        print(f"  {'─'*70}")
        
        for fa in agents:
            ovr_color = GREEN if fa.overall >= 85 else YELLOW if fa.overall >= 80 else WHITE
            type_color = CYAN if fa.fa_type == "bird" else WHITE
            print(f"  {fa.player_name:<20} {fa.position:>3} {ovr_color}{fa.overall:>3}{RESET} {fa.age:>3} "
                  f"{fa.experience:>3} {type_color}{fa.fa_type:<12}{RESET} ${fa.desired_salary:>7.2f}M")
        
        print(f"{'═'*70}\n")
    
    def display_signing_history(self):
        """Display recent signings."""
        from colors import RESET, BOLD, GREEN, WHITE
        
        history = self.fa_manager.signing_history[-10:]  # Last 10 signings
        
        print(f"\n{BOLD}{CYAN}  📝 RECENT SIGNINGS{RESET}")
        print(f"{'═'*70}")
        
        if not history:
            print(f"  No recent signings.")
            print(f"{'═'*70}\n")
            return
        
        print(f"  {'PLAYER':<20} {'TEAM':<20} {'SALARY':>8} {'YEARS':>5}")
        print(f"  {'─'*70}")
        
        for signing in reversed(history):
            print(f"  {signing['player']:<20} {signing['team']:<20} ${signing['salary']:>7.2f}M {signing['years']:>5}")
        
        print(f"{'═'*70}\n")


# ==========================
# INITIALIZATION
# ==========================

# These will be initialized with the contract manager when needed
# free_agency_manager = FreeAgencyManager(contract_manager)
# exception_tracker = ExceptionTracker()
# bird_rights = BirdRights()
# restricted_fa = RestrictedFreeAgency()
