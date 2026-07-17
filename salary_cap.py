# ==========================================
# salary_cap.py
# NBA Salary Cap Configuration & Calculations
# ==========================================

from typing import Dict, List, Optional
import random


# ==========================
# SALARY CAP CONFIGURATION
# ==========================

class SalaryCapConfig:
    """Central configuration for all salary cap values."""
    
    def __init__(self):
        # Current Season Values (in millions)
        self.soft_cap = 170.0
        self.luxury_tax = 208.0
        self.first_apron = 218.0
        self.second_apron = 228.0
        
        # Minimum Salary (in millions)
        self.min_salary = 1.12
        
        # Maximum Contract Values (in millions)
        self.max_contract = {
            0: 40.0,   # 0-6 years experience
            1: 47.0,   # 7-9 years experience
            2: 56.0    # 10+ years experience
        }
        
        # Rookie Scale (in millions - approximate)
        self.rookie_scale = {
            1: 10.9,   # #1 pick
            2: 9.8,
            3: 8.8,
            4: 7.9,
            5: 7.2,
            6: 6.6,
            7: 6.1,
            8: 5.6,
            9: 5.2,
            10: 4.9,
            11: 4.6,
            12: 4.3,
            13: 4.0,
            14: 3.8,
            15: 3.6,
            16: 3.4,
            17: 3.2,
            18: 3.0,
            19: 2.9,
            20: 2.8,
            21: 2.7,
            22: 2.6,
            23: 2.5,
            24: 2.4,
            25: 2.3,
            26: 2.2,
            27: 2.1,
            28: 2.0,
            29: 2.0,
            30: 2.0
        }
        
        # Mid-Level Exception Values (in millions)
        self.mle_non_taxpayer = 12.4
        self.mle_taxpayer = 5.0
        self.mle_room = 5.0
        
        # Bi-Annual Exception (in millions)
        self.bae = 4.7
        
        # Salary Growth Rate (annual percentage increase)
        self.growth_rate_min = 0.03  # 3%
        self.growth_rate_max = 0.10  # 10%
    
    def apply_growth(self):
        """Apply salary cap growth for next season (3-10% increase)."""
        growth = random.uniform(self.growth_rate_min, self.growth_rate_max)
        
        self.soft_cap *= (1 + growth)
        self.luxury_tax *= (1 + growth)
        self.first_apron *= (1 + growth)
        self.second_apron *= (1 + growth)
        self.min_salary *= (1 + growth)
        
        # Update max contracts
        for tier in self.max_contract:
            self.max_contract[tier] *= (1 + growth)
        
        # Update rookie scale
        for pick in self.rookie_scale:
            self.rookie_scale[pick] *= (1 + growth)
        
        # Update exceptions
        self.mle_non_taxpayer *= (1 + growth)
        self.mle_taxpayer *= (1 + growth)
        self.mle_room *= (1 + growth)
        self.bae *= (1 + growth)
        
        return growth


# Global configuration instance
salary_config = SalaryCapConfig()


# ==========================
# SALARY CAP CALCULATIONS
# ==========================

class SalaryCapCalculator:
    """Calculate team salary cap status and related metrics."""
    
    def __init__(self, config: SalaryCapConfig = None):
        self.config = config or salary_config
    
    def calculate_payroll(self, contracts: List[Dict]) -> float:
        """Calculate total payroll from contract list (in millions)."""
        total = 0.0
        for contract in contracts:
            total += contract.get("annual_salary", 0)
        return round(total, 2)
    
    def calculate_cap_space(self, payroll: float) -> float:
        """Calculate remaining cap space (in millions)."""
        return round(self.config.soft_cap - payroll, 2)
    
    def calculate_luxury_tax(self, payroll: float) -> float:
        """Calculate luxury tax owed (in millions)."""
        if payroll <= self.config.luxury_tax:
            return 0.0
        
        over = payroll - self.config.luxury_tax
        
        # Progressive tax brackets (NBA rules)
        tax = 0.0
        
        # 0-5M over: $1.50 per $1
        if over > 0:
            bracket = min(over, 5.0)
            tax += bracket * 1.50
            over -= bracket
        
        # 5-10M over: $1.75 per $1
        if over > 0:
            bracket = min(over, 5.0)
            tax += bracket * 1.75
            over -= bracket
        
        # 10-15M over: $2.50 per $1
        if over > 0:
            bracket = min(over, 5.0)
            tax += bracket * 2.50
            over -= bracket
        
        # 15-20M over: $3.25 per $1
        if over > 0:
            bracket = min(over, 5.0)
            tax += bracket * 3.25
            over -= bracket
        
        # 20M+: $4.25 per $1 (increases progressively)
        if over > 0:
            tax += over * 4.25
        
        return round(tax, 2)
    
    def get_apron_status(self, payroll: float) -> Dict[str, bool]:
        """Check apron status for a team."""
        return {
            "over_cap": payroll > self.config.soft_cap,
            "over_tax": payroll > self.config.luxury_tax,
            "over_first_apron": payroll > self.config.first_apron,
            "over_second_apron": payroll > self.config.second_apron
        }
    
    def calculate_guaranteed_salary(self, contracts: List[Dict]) -> float:
        """Calculate total guaranteed salary (in millions)."""
        total = 0.0
        for contract in contracts:
            if contract.get("guaranteed", False):
                total += contract.get("annual_salary", 0)
        return round(total, 2)
    
    def calculate_non_guaranteed_salary(self, contracts: List[Dict]) -> float:
        """Calculate total non-guaranteed salary (in millions)."""
        total = 0.0
        for contract in contracts:
            if not contract.get("guaranteed", False):
                total += contract.get("annual_salary", 0)
        return round(total, 2)
    
    def calculate_dead_money(self, contracts: List[Dict]) -> float:
        """Calculate dead money from waived players (in millions)."""
        total = 0.0
        for contract in contracts:
            if contract.get("dead_money", 0) > 0:
                total += contract.get("dead_money", 0)
        return round(total, 2)
    
    def get_roster_spots_used(self, contracts: List[Dict]) -> int:
        """Count active roster spots (excluding dead money contracts)."""
        count = 0
        for contract in contracts:
            if not contract.get("dead_money", 0) > 0:
                count += 1
        return count
    
    def can_sign_with_cap_space(self, payroll: float, salary: float) -> bool:
        """Check if team can sign player using cap space."""
        return payroll + salary <= self.config.soft_cap
    
    def can_use_mle(self, payroll: float) -> tuple[bool, str]:
        """Check if team can use Mid-Level Exception and which type."""
        apron = self.get_apron_status(payroll)
        
        if apron["over_second_apron"]:
            return False, "Cannot use MLE - over second apron"
        
        if apron["over_tax"]:
            return True, "taxpayer_mle"
        
        if payroll + self.config.mle_non_taxpayer <= self.config.first_apron:
            return True, "non_taxpayer_mle"
        
        return True, "taxpayer_mle"
    
    def can_use_bae(self, payroll: float) -> tuple[bool, str]:
        """Check if team can use Bi-Annual Exception."""
        apron = self.get_apron_status(payroll)
        
        if apron["over_tax"]:
            return False, "Cannot use BAE - over luxury tax"
        
        if payroll + self.config.bae > self.config.first_apron:
            return False, "Cannot use BAE - would exceed first apron"
        
        return True, "bae_available"
    
    def get_available_exceptions(self, payroll: float) -> Dict[str, float]:
        """Get all available exceptions for a team."""
        exceptions = {}
        
        # Check MLE
        can_use_mle, mle_type = self.can_use_mle(payroll)
        if can_use_mle:
            if mle_type == "non_taxpayer_mle":
                exceptions["Non-Taxpayer MLE"] = self.config.mle_non_taxpayer
            else:
                exceptions["Taxpayer MLE"] = self.config.mle_taxpayer
        
        # Check BAE
        can_use_bae, _ = self.can_use_bae(payroll)
        if can_use_bae:
            exceptions["Bi-Annual Exception"] = self.config.bae
        
        # Room MLE (if under cap)
        cap_space = self.calculate_cap_space(payroll)
        if cap_space > 0:
            exceptions["Room MLE"] = self.config.mle_room
        
        return exceptions


# ==========================
# MULTI-YEAR PAYROLL TRACKING
# ==========================

class MultiYearPayroll:
    """Track payroll across multiple seasons."""
    
    def __init__(self):
        self.payroll_history = {}  # {season: {team: payroll}}
        self.future_payroll = {}   # {team: {year_offset: projected_payroll}}
    
    def record_season_payroll(self, season: int, team_payrolls: Dict[str, float]):
        """Record actual payroll for a completed season."""
        self.payroll_history[season] = team_payrolls.copy()
    
    def project_future_payroll(self, team: str, contracts: List[Dict], years_ahead: int = 3):
        """Project payroll for future seasons based on current contracts."""
        projections = {}
        
        for year_offset in range(1, years_ahead + 1):
            future_payroll = 0.0
            for contract in contracts:
                years_remaining = contract.get("years_remaining", 0)
                if years_remaining >= year_offset:
                    # Assume 5% annual salary increase for future years
                    future_salary = contract.get("annual_salary", 0) * (1.05 ** year_offset)
                    future_payroll += future_salary
            projections[year_offset] = round(future_payroll, 2)
        
        self.future_payroll[team] = projections
        return projections
    
    def get_payroll_trend(self, team: str) -> Dict[str, float]:
        """Get payroll trend for a team (past and future)."""
        trend = {}
        
        # Historical data
        for season, team_payrolls in self.payroll_history.items():
            if team in team_payrolls:
                trend[f"Season {season}"] = team_payrolls[team]
        
        # Future projections
        if team in self.future_payroll:
            for year_offset, payroll in self.future_payroll[team].items():
                trend[f"Year +{year_offset}"] = payroll
        
        return trend


# ==========================
# HELPER FUNCTIONS
# ==========================

def format_currency(amount: float) -> str:
    """Format monetary amount in millions."""
    return f"${amount:.2f}M"


def get_salary_for_ovr(ovr: int, years_experience: int = 5) -> float:
    """Estimate appropriate salary based on overall rating and experience."""
    base = max(1.12, (ovr - 60) * 2.5 + 3.0)
    
    # Experience multiplier
    if years_experience <= 2:
        multiplier = 0.7
    elif years_experience <= 5:
        multiplier = 1.0
    elif years_experience <= 9:
        multiplier = 1.3
    else:
        multiplier = 1.5
    
    salary = base * multiplier
    
    # Cap at maximum for experience tier
    tier = 0 if years_experience <= 6 else 1 if years_experience <= 9 else 2
    max_sal = salary_config.max_contract.get(tier, 40.0)
    
    return round(min(salary, max_sal), 2)


def get_rookie_salary(pick_number: int) -> float:
    """Get rookie scale salary for draft pick."""
    return salary_config.rookie_scale.get(pick_number, 2.0)


# ==========================
# INITIALIZATION
# ==========================

calculator = SalaryCapCalculator()
multi_year_tracker = MultiYearPayroll()
