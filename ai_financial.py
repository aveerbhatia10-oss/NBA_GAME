# ==========================================
# ai_financial.py
# AI Financial Personalities & Decision Making
# ==========================================

from typing import Dict, List, Tuple
from salary_cap import salary_config, SalaryCapCalculator
from contracts import ContractManager
from luxury_tax import ApronRestrictions
import random


# ==========================
# FINANCIAL PERSONALITIES
# ==========================

class FinancialPersonality:
    """Define AI team financial personalities."""
    
    PERSONALITIES = {
        "cheap_owner": {
            "name": "Cheap Owner",
            "description": "Minimizes spending, avoids luxury tax",
            "spending_multiplier": 0.7,
            "tax_aversion": 0.95,
            "risk_tolerance": 0.3,
            "win_now_priority": 0.4
        },
        "balanced": {
            "name": "Balanced",
            "description": "Moderate spending with competitive focus",
            "spending_multiplier": 1.0,
            "tax_aversion": 0.6,
            "risk_tolerance": 0.5,
            "win_now_priority": 0.6
        },
        "aggressive": {
            "name": "Aggressive",
            "description": "Willing to spend for talent",
            "spending_multiplier": 1.3,
            "tax_aversion": 0.4,
            "risk_tolerance": 0.7,
            "win_now_priority": 0.8
        },
        "win_now": {
            "name": "Win Now",
            "description": "Spend whatever it takes to win immediately",
            "spending_multiplier": 1.5,
            "tax_aversion": 0.2,
            "risk_tolerance": 0.9,
            "win_now_priority": 1.0
        },
        "tax_avoider": {
            "name": "Luxury Tax Avoider",
            "description": "Will never pay luxury tax",
            "spending_multiplier": 0.9,
            "tax_avoider": 1.0,
            "risk_tolerance": 0.4,
            "win_now_priority": 0.5
        },
        "big_market": {
            "name": "Big Market",
            "description": "High revenue, willing to spend big",
            "spending_multiplier": 1.4,
            "tax_aversion": 0.3,
            "risk_tolerance": 0.8,
            "win_now_priority": 0.7
        },
        "small_market": {
            "name": "Small Market",
            "description": "Budget-conscious, develops young talent",
            "spending_multiplier": 0.6,
            "tax_aversion": 0.9,
            "risk_tolerance": 0.4,
            "win_now_priority": 0.3
        }
    }
    
    @staticmethod
    def assign_random_personality() -> str:
        """Assign a random personality to a team."""
        personalities = list(FinancialPersonality.PERSONALITIES.keys())
        weights = [15, 25, 20, 10, 15, 10, 5]  # Weighted distribution
        return random.choices(personalities, weights=weights)[0]
    
    @staticmethod
    def get_personality_data(personality_type: str) -> Dict:
        """Get personality data for a specific type."""
        return FinancialPersonality.PERSONALITIES.get(personality_type, FinancialPersonality.PERSONALITIES["balanced"])


# ==========================
# AI FINANCIAL MANAGER
# ==========================

class AIFinancialManager:
    """Manage AI team financial decisions."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
        self.calculator = SalaryCapCalculator()
        self.apron = ApronRestrictions()
        self.team_personalities = {}  # {team: personality_type}
    
    def assign_personality(self, team: str, personality_type: str = None):
        """Assign a personality to a team."""
        if personality_type is None:
            personality_type = FinancialPersonality.assign_random_personality()
        self.team_personalities[team] = personality_type
    
    def get_team_personality(self, team: str) -> str:
        """Get a team's personality."""
        return self.team_personalities.get(team, "balanced")
    
    def should_pay_luxury_tax(self, team: str) -> bool:
        """Determine if team is willing to pay luxury tax."""
        personality = self.get_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        tax_aversion = data.get("tax_aversion", 0.6)
        
        # If tax_avoider is 1.0, never pay tax
        if tax_aversion >= 1.0:
            return False
        
        # Random chance based on aversion
        return random.random() > tax_aversion
    
    def should_sign_free_agent(self, team: str, salary: float, player_ovr: int) -> Tuple[bool, str]:
        """Determine if AI team should sign a free agent."""
        personality = self.get_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        payroll = self.contract_manager.get_team_payroll(team)
        apron_status = self.apron.get_apron_status(payroll)
        
        spending_mult = data.get("spending_multiplier", 1.0)
        win_now = data.get("win_now_priority", 0.6)
        
        # Check if signing would push over luxury tax
        new_payroll = payroll + salary
        would_pay_tax = new_payroll > salary_config.luxury_tax
        
        if would_pay_tax and not self.should_pay_luxury_tax(team):
            return False, "Team avoids luxury tax"
        
        # Check apron restrictions
        if apron_status["over_second_apron"]:
            return False, "Team over second apron - restricted"
        
        # Evaluate player value vs cost
        value_score = player_ovr / (salary * 10)  # Simple value metric
        
        # Adjust based on personality
        adjusted_score = value_score * spending_mult
        
        # Win-now teams value high overall players more
        if player_ovr >= 85:
            adjusted_score *= (1 + win_now * 0.5)
        
        # Decision threshold
        if adjusted_score > 0.8:
            return True, "Good value for team"
        elif adjusted_score > 0.5:
            # Maybe sign with some randomness
            if random.random() < 0.4:
                return True, "Acceptable value"
            else:
                return False, "Value uncertain"
        else:
            return False, "Poor value for team"
    
    def should_make_trade(self, team: str, incoming_salary: float, outgoing_salary: float, 
                         incoming_ovr: int, outgoing_ovr: int) -> Tuple[bool, str]:
        """Determine if AI team should accept a trade."""
        personality = self.get_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        payroll = self.contract_manager.get_team_payroll(team)
        new_payroll = payroll - outgoing_salary + incoming_salary
        
        # Financial impact
        salary_change = incoming_salary - outgoing_salary
        spending_mult = data.get("spending_multiplier", 1.0)
        risk_tol = data.get("risk_tolerance", 0.5)
        
        # Check if trade would cause apron issues
        apron_status = self.apron.get_apron_status(new_payroll)
        if apron_status["over_second_apron"] and risk_tol < 0.7:
            return False, "Trade would push team over second apron"
        
        # Talent evaluation
        talent_change = incoming_ovr - outgoing_ovr
        
        # Financial score (positive = good for team)
        financial_score = -salary_change * spending_mult
        
        # Talent score
        talent_score = talent_change * 2
        
        # Win-now teams value immediate talent more
        win_now = data.get("win_now_priority", 0.6)
        if talent_change > 0:
            talent_score *= (1 + win_now * 0.5)
        
        # Total score
        total_score = financial_score + talent_score
        
        if total_score > 5:
            return True, "Strongly favorable trade"
        elif total_score > 0:
            return True, "Favorable trade"
        elif total_score > -5:
            # Maybe accept with randomness
            if random.random() < risk_tol:
                return True, "Acceptable risk"
            else:
                return False, "Too much risk"
        else:
            return False, "Unfavorable trade"
    
    def should_extend_contract(self, team: str, player_ovr: int, current_salary: float, 
                             extension_salary: float) -> Tuple[bool, str]:
        """Determine if AI team should extend a player's contract."""
        personality = self.get_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        spending_mult = data.get("spending_multiplier", 1.0)
        win_now = data.get("win_now_priority", 0.6)
        
        # Value assessment
        salary_increase = extension_salary - current_salary
        value_ratio = player_ovr / (extension_salary * 10)
        
        # Star players are worth extending
        if player_ovr >= 85:
            if salary_increase * spending_mult < 15:  # Willing to pay up to $15M more
                return True, "Star player worth extension"
        
        # Good value players
        if value_ratio > 0.8 and salary_increase < 10:
            return True, "Good value extension"
        
        # Win-now teams more likely to extend
        if win_now > 0.7 and player_ovr >= 80:
            return True, "Win-now team extends key player"
        
        return False, "Extension not justified"
    
    def should_waive_player(self, team: str, player_ovr: int, salary: float, 
                           years_remaining: int) -> Tuple[bool, str]:
        """Determine if AI team should waive a player."""
        personality = self.get_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        risk_tol = data.get("risk_tolerance", 0.5)
        
        # High salary, low production players
        value_ratio = player_ovr / (salary * 10)
        
        if value_ratio < 0.3 and salary > 10:
            # Very bad contract
            if risk_tol > 0.6:
                return True, "Waive bad contract"
        
        # Young players with potential usually kept
        if player_ovr < 75 and years_remaining > 2:
            return False, "Young player with potential"
        
        # End of bench players
        if player_ovr < 70 and salary < 3:
            return True, "Waive end of bench player"
        
        return False, "Keep player"
    
    def get_max_offer(self, team: str, player_ovr: int, years: int) -> float:
        """Get maximum salary offer AI team would make for a player."""
        personality = self.get_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        spending_mult = data.get("spending_multiplier", 1.0)
        win_now = data.get("win_now_priority", 0.6)
        
        payroll = self.contract_manager.get_team_payroll(team)
        apron_status = self.apron.get_apron_status(payroll)
        
        # Base salary calculation
        from salary_cap import get_salary_for_ovr
        base_salary = get_salary_for_ovr(player_ovr, 5)
        
        # Adjust for personality
        max_offer = base_salary * spending_mult
        
        # Win-now teams pay more for stars
        if player_ovr >= 85:
            max_offer *= (1 + win_now * 0.3)
        
        # Cap considerations
        if apron_status["over_cap"]:
            # Must use exceptions - lower max
            max_offer = min(max_offer, salary_config.mle_taxpayer)
        elif apron_status["over_tax"]:
            max_offer = min(max_offer, salary_config.mle_taxpayer)
        
        return round(max_offer, 2)


# ==========================
# AI OFFSEASON DECISIONS
# ==========================

class AIOffseasonStrategy:
    """Coordinate AI financial decisions during offseason."""
    
    def __init__(self, financial_manager: AIFinancialManager):
        self.financial_manager = financial_manager
    
    def plan_offseason_moves(self, team: str) -> Dict:
        """Plan financial moves for offseason."""
        personality = self.financial_manager.get_team_personality(team)
        data = FinancialPersonality.get_personality_data(personality)
        
        payroll = self.financial_manager.contract_manager.get_team_payroll(team)
        
        plan = {
            "team": team,
            "personality": personality,
            "priorities": [],
            "budget": payroll,
            "targets": []
        }
        
        # Set priorities based on personality
        win_now = data.get("win_now_priority", 0.6)
        
        if win_now > 0.8:
            plan["priorities"].append("Acquire star players")
            plan["priorities"].append("Win immediately")
        elif win_now > 0.5:
            plan["priorities"].append("Balance present and future")
        else:
            plan["priorities"].append("Develop young talent")
            plan["priorities"].append("Accumulate draft picks")
        
        # Budget planning
        if payroll > salary_config.luxury_tax:
            plan["priorities"].append("Reduce payroll to avoid tax")
        elif payroll > salary_config.soft_cap:
            plan["priorities"].append("Monitor tax threshold")
        else:
            plan["priorities"].append("Use cap space effectively")
        
        return plan
    
    def execute_offseason_plan(self, team: str, plan: Dict) -> List[str]:
        """Execute offseason plan (simplified - would call actual functions in full system)."""
        actions = []
        
        actions.append(f"{team} offseason plan:")
        for priority in plan["priorities"]:
            actions.append(f"  - {priority}")
        
        return actions


# ==========================
# INITIALIZATION
# ==========================

# These will be initialized with the contract manager when needed
# ai_financial_manager = AIFinancialManager(contract_manager)
# ai_offseason_strategy = AIOffseasonStrategy(ai_financial_manager)
