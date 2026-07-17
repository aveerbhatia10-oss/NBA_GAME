# ==========================================
# contracts.py
# NBA Contract Management System
# ==========================================

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

from salary_cap import salary_config, get_salary_for_ovr, get_rookie_salary


# ==========================
# CONTRACT DATA STRUCTURES
# ==========================

class Contract:
    """Represents an NBA player contract."""
    
    def __init__(self, player_name: str, team: str, **kwargs):
        self.player_name = player_name
        self.team = team
        
        # Contract Terms
        self.years_remaining = kwargs.get("years_remaining", 1)
        self.annual_salary = kwargs.get("annual_salary", 0.0)
        self.total_value = self.annual_salary * self.years_remaining
        
        # Contract Status
        self.guaranteed = kwargs.get("guaranteed", True)
        self.partial_guarantee = kwargs.get("partial_guarantee", 0.0)  # Amount guaranteed
        self.team_option = kwargs.get("team_option", False)
        self.player_option = kwargs.get("player_option", False)
        self.option_year = kwargs.get("option_year", None)  # Which year has option
        
        # Special Rights
        self.bird_rights = kwargs.get("bird_rights", False)
        self.extension_eligible = kwargs.get("extension_eligible", False)
        self.no_trade_clause = kwargs.get("no_trade_clause", False)
        
        # Contract Type
        self.contract_type = kwargs.get("contract_type", "standard")  # standard, rookie, veteran, minimum, maximum, supermax, two_way
        
        # Dead Money (if waived)
        self.dead_money = kwargs.get("dead_money", 0.0)
        self.stretch_years = kwargs.get("stretch_years", 0)
        
        # Metadata
        self.sign_date = kwargs.get("sign_date", datetime.now())
        self.original_team = kwargs.get("original_team", team)
    
    def to_dict(self) -> Dict:
        """Convert contract to dictionary for storage."""
        return {
            "player_name": self.player_name,
            "team": self.team,
            "years_remaining": self.years_remaining,
            "annual_salary": self.annual_salary,
            "total_value": self.total_value,
            "guaranteed": self.guaranteed,
            "partial_guarantee": self.partial_guarantee,
            "team_option": self.team_option,
            "player_option": self.player_option,
            "option_year": self.option_year,
            "bird_rights": self.bird_rights,
            "extension_eligible": self.extension_eligible,
            "no_trade_clause": self.no_trade_clause,
            "contract_type": self.contract_type,
            "dead_money": self.dead_money,
            "stretch_years": self.stretch_years,
            "sign_date": self.sign_date,
            "original_team": self.original_team
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contract':
        """Create contract from dictionary."""
        return cls(**data)
    
    def is_expired(self) -> bool:
        """Check if contract has expired."""
        return self.years_remaining <= 0
    
    def has_option_this_year(self) -> bool:
        """Check if current year has an option."""
        if self.option_year is None:
            return False
        return self.option_year == (self.years_remaining)
    
    def get_guaranteed_amount(self) -> float:
        """Get guaranteed amount for this season."""
        if self.guaranteed:
            return self.annual_salary
        return self.partial_guarantee
    
    def advance_year(self):
        """Advance contract by one year."""
        if self.years_remaining > 0:
            self.years_remaining -= 1
            
            # Handle option years
            if self.has_option_this_year():
                if self.team_option:
                    # Team declined - contract ends
                    self.years_remaining = 0
                elif self.player_option:
                    # Player opted in - continue
                    pass


# ==========================
# CONTRACT GENERATION
# ==========================

class ContractGenerator:
    """Generate contracts based on player attributes and NBA rules."""
    
    @staticmethod
    def generate_rookie_contract(player_name: str, team: str, pick_number: int, years: int = 2) -> Contract:
        """Generate a rookie scale contract."""
        salary = get_rookie_salary(pick_number)
        
        # Rookie contracts are 2 years + 2 team options
        return Contract(
            player_name=player_name,
            team=team,
            years_remaining=4,
            annual_salary=salary,
            guaranteed=True,
            team_option=True,
            option_year=3,  # 3rd year is team option
            contract_type="rookie",
            bird_rights=True
        )
    
    @staticmethod
    def generate_veteranContract(player_name: str, team: str, ovr: int, years: int, 
                                 experience: int = 5, bird_rights: bool = False) -> Contract:
        """Generate a veteran contract based on overall rating."""
        salary = get_salary_for_ovr(ovr, experience)
        
        return Contract(
            player_name=player_name,
            team=team,
            years_remaining=years,
            annual_salary=salary,
            guaranteed=True,
            bird_rights=bird_rights,
            contract_type="veteran"
        )
    
    @staticmethod
    def generate_minimum_contract(player_name: str, team: str, experience: int = 0) -> Contract:
        """Generate a minimum salary contract."""
        # Minimum salary varies by experience
        if experience <= 0:
            salary = salary_config.min_salary
        elif experience <= 1:
            salary = salary_config.min_salary * 1.2
        elif experience <= 2:
            salary = salary_config.min_salary * 1.4
        else:
            salary = salary_config.min_salary * 1.7
        
        return Contract(
            player_name=player_name,
            team=team,
            years_remaining=1,
            annual_salary=salary,
            guaranteed=True,
            contract_type="minimum"
        )
    
    @staticmethod
    def generate_maximum_contract(player_name: str, team: str, ovr: int, 
                                   experience: int, years: int = 5) -> Contract:
        """Generate a maximum contract for a star player."""
        tier = 0 if experience <= 6 else 1 if experience <= 9 else 2
        salary = salary_config.max_contract.get(tier, 40.0)
        
        # Supermax eligibility (if OVR 90+ and meets criteria)
        contract_type = "supermax" if ovr >= 90 else "maximum"
        
        return Contract(
            player_name=player_name,
            team=team,
            years_remaining=years,
            annual_salary=salary,
            guaranteed=True,
            bird_rights=True,
            contract_type=contract_type
        )
    
    @staticmethod
    def generate_two_way_contract(player_name: str, team: str) -> Contract:
        """Generate a two-way contract."""
        salary = salary_config.min_salary * 0.5  # Two-way pays less
        
        return Contract(
            player_name=player_name,
            team=team,
            years_remaining=1,
            annual_salary=salary,
            guaranteed=False,
            contract_type="two_way"
        )


# ==========================
# CONTRACT EXTENSIONS
# ==========================

class ContractExtension:
    """Handle contract extensions."""
    
    @staticmethod
    def can_extend_rookie(contract: Contract) -> Tuple[bool, str]:
        """Check if rookie contract can be extended."""
        if contract.contract_type != "rookie":
            return False, "Not a rookie contract"
        
        if contract.years_remaining != 2:
            return False, "Rookie extension only available after 2nd season"
        
        return True, "Eligible for rookie extension"
    
    @staticmethod
    def can_extend_veteran(contract: Contract) -> Tuple[bool, str]:
        """Check if veteran contract can be extended."""
        if contract.years_remaining < 1:
            return False, "Contract expiring - cannot extend"
        
        if contract.years_remaining > 3:
            return False, "Too many years remaining to extend"
        
        return True, "Eligible for veteran extension"
    
    @staticmethod
    def calculate_extension_salary(current_salary: float, ovr: int, 
                                   years: int = 4) -> float:
        """Calculate extension salary based on current salary and performance."""
        # Base increase
        increase = 0.05  # 5% minimum increase
        
        # Performance bonus
        if ovr >= 90:
            increase += 0.15  # 15% bonus for superstars
        elif ovr >= 85:
            increase += 0.10  # 10% bonus for stars
        elif ovr >= 80:
            increase += 0.05  # 5% bonus for above-average
        
        new_salary = current_salary * (1 + increase)
        
        # Cap at maximum for player's experience tier
        tier = 0 if ovr <= 85 else 1 if ovr <= 90 else 2
        max_sal = salary_config.max_contract.get(tier, 40.0)
        
        return round(min(new_salary, max_sal), 2)
    
    @staticmethod
    def create_extension(contract: Contract, ovr: int, extension_years: int = 4) -> Contract:
        """Create an extended contract."""
        new_salary = ContractExtension.calculate_extension_salary(
            contract.annual_salary, ovr, extension_years
        )
        
        # Create new contract with extended years
        extended_contract = Contract(
            player_name=contract.player_name,
            team=contract.team,
            years_remaining=contract.years_remaining + extension_years,
            annual_salary=new_salary,
            guaranteed=True,
            bird_rights=contract.bird_rights,
            contract_type="veteran" if contract.contract_type == "rookie" else contract.contract_type
        )
        
        return extended_contract


# ==========================
# CONTRACT MANAGEMENT
# ==========================

class ContractManager:
    """Manage all contracts for all teams."""
    
    def __init__(self):
        self.contracts = {}  # {team: [Contract]}
        self.free_agents = []  # List of Contract objects for free agents
    
    def add_contract(self, contract: Contract):
        """Add a contract to a team."""
        team = contract.team
        if team not in self.contracts:
            self.contracts[team] = []
        self.contracts[team].append(contract)
    
    def remove_contract(self, team: str, player_name: str) -> bool:
        """Remove a contract from a team."""
        if team not in self.contracts:
            return False
        
        for i, contract in enumerate(self.contracts[team]):
            if contract.player_name == player_name:
                self.contracts[team].pop(i)
                return True
        
        return False
    
    def get_player_contract(self, team: str, player_name: str) -> Optional[Contract]:
        """Get contract for a specific player."""
        if team not in self.contracts:
            return None
        
        for contract in self.contracts[team]:
            if contract.player_name == player_name:
                return contract
        
        return None
    
    def get_team_contracts(self, team: str) -> List[Contract]:
        """Get all contracts for a team."""
        return self.contracts.get(team, [])
    
    def get_team_payroll(self, team: str) -> float:
        """Calculate total payroll for a team."""
        contracts = self.get_team_contracts(team)
        total = 0.0
        for contract in contracts:
            if contract.dead_money > 0:
                total += contract.dead_money
            else:
                total += contract.annual_salary
        return round(total, 2)
    
    def advance_all_contracts(self):
        """Advance all contracts by one year (offseason)."""
        for team in self.contracts:
            expired_contracts = []
            
            for contract in self.contracts[team]:
                contract.advance_year()
                
                if contract.is_expired():
                    expired_contracts.append(contract)
            
            # Move expired contracts to free agency
            for contract in expired_contracts:
                self.contracts[team].remove(contract)
                if contract.dead_money == 0:  # Only if not dead money
                    self.free_agents.append(contract)
    
    def process_waivers(self, team: str, player_name: str, stretch: bool = False) -> Tuple[bool, str]:
        """Waive a player and handle dead money."""
        contract = self.get_player_contract(team, player_name)
        if not contract:
            return False, "Player not found on team"
        
        if contract.no_trade_clause:
            return False, "Cannot waive - no-trade clause"
        
        remaining_salary = contract.annual_salary * contract.years_remaining
        
        if stretch:
            # Stretch over 2x remaining years (max 5)
            stretch_years = min(contract.years_remaining * 2, 5)
            contract.dead_money = remaining_salary / stretch_years
            contract.stretch_years = stretch_years
        else:
            # Immediate dead money
            contract.dead_money = remaining_salary
            contract.stretch_years = 1
        
        # Remove from active roster but keep for dead money tracking
        contract.years_remaining = contract.stretch_years
        contract.annual_salary = contract.dead_money
        
        return True, f"Player waived with ${contract.dead_money:.2f}M dead money"
    
    def process_buyout(self, team: str, player_name: str, buyout_amount: float) -> Tuple[bool, str]:
        """Negotiate a buyout with a player."""
        contract = self.get_player_contract(team, player_name)
        if not contract:
            return False, "Player not found on team"
        
        remaining_salary = contract.annual_salary * contract.years_remaining
        
        if buyout_amount >= remaining_salary:
            return False, "Buyout amount must be less than remaining salary"
        
        # Create dead money for the difference
        contract.dead_money = remaining_salary - buyout_amount
        contract.stretch_years = contract.years_remaining
        
        # Remove from team
        self.remove_contract(team, player_name)
        
        # Create new free agent contract with buyout terms
        new_contract = Contract(
            player_name=player_name,
            team="Free Agent",
            years_remaining=0,
            annual_salary=0,
            guaranteed=False,
            contract_type="buyout"
        )
        self.free_agents.append(new_contract)
        
        return True, f"Buyout complete. Dead money: ${contract.dead_money:.2f}M"
    
    def get_expiring_contracts(self, team: str) -> List[Contract]:
        """Get contracts expiring this season."""
        contracts = self.get_team_contracts(team)
        return [c for c in contracts if c.years_remaining == 1]
    
    def get_team_options(self, team: str) -> List[Contract]:
        """Get contracts with team options this year."""
        contracts = self.get_team_contracts(team)
        return [c for c in contracts if c.team_option and c.has_option_this_year()]
    
    def get_player_options(self, team: str) -> List[Contract]:
        """Get contracts with player options this year."""
        contracts = self.get_team_contracts(team)
        return [c for c in contracts if c.player_option and c.has_option_this_year()]


# ==========================
# CONTRACT VALIDATION
# ==========================

class ContractValidator:
    """Validate contracts against NBA rules."""
    
    @staticmethod
    def validate_contract_structure(contract: Contract) -> Tuple[bool, str]:
        """Validate basic contract structure."""
        if contract.annual_salary < 0:
            return False, "Salary cannot be negative"
        
        if contract.years_remaining < 0:
            return False, "Years remaining cannot be negative"
        
        if contract.partial_guarantee < 0 or contract.partial_guarantee > contract.annual_salary:
            return False, "Partial guarantee out of range"
        
        return True, "Valid contract structure"
    
    @staticmethod
    def validate_maximum_contract(contract: Contract, experience: int) -> Tuple[bool, str]:
        """Validate if contract exceeds maximum allowed."""
        tier = 0 if experience <= 6 else 1 if experience <= 9 else 2
        max_sal = salary_config.max_contract.get(tier, 40.0)
        
        if contract.annual_salary > max_sal:
            return False, f"Salary exceeds maximum of ${max_sal:.2f}M for experience tier"
        
        return True, "Within maximum contract limits"
    
    @staticmethod
    def validate_rookie_contract(contract: Contract, pick_number: int) -> Tuple[bool, str]:
        """Validate rookie scale contract."""
        expected_salary = get_rookie_salary(pick_number)
        
        # Allow small variance for negotiations
        if abs(contract.annual_salary - expected_salary) > 0.5:
            return False, f"Rookie salary ${contract.annual_salary:.2f}M deviates from scale ${expected_salary:.2f}M"
        
        if contract.years_remaining != 4:
            return False, "Rookie contracts must be 4 years (2 + 2 team options)"
        
        return True, "Valid rookie contract"


# ==========================
# INITIALIZATION
# ==========================

contract_manager = ContractManager()
contract_generator = ContractGenerator()
contract_extension = ContractExtension()
contract_validator = ContractValidator()
