# ==========================================
# trades.py
# NBA Trade System with Salary Matching & Apron Restrictions
# ==========================================

from typing import Dict, List, Tuple, Optional
from salary_cap import salary_config, SalaryCapCalculator, format_currency
from contracts import Contract, ContractManager
from luxury_tax import ApronRestrictions, ApronAlerts


# ==========================
# TRADE PROPOSAL CLASS
# ==========================

class TradeProposal:
    """Represents a trade proposal between teams."""
    
    def __init__(self, team1: str, team2: str):
        self.team1 = team1
        self.team2 = team2
        self.players_from_team1 = []  # List of player names
        self.players_from_team2 = []  # List of player names
        self.picks_from_team1 = []    # List of draft picks
        self.picks_from_team2 = []    # List of draft picks
        self.cash_from_team1 = 0.0    # Cash in millions
        self.cash_from_team2 = 0.0    # Cash in millions
    
    def add_player(self, team: str, player_name: str):
        """Add a player to the trade."""
        if team == self.team1:
            self.players_from_team1.append(player_name)
        elif team == self.team2:
            self.players_from_team2.append(player_name)
    
    def add_pick(self, team: str, pick: Dict):
        """Add a draft pick to the trade."""
        if team == self.team1:
            self.picks_from_team1.append(pick)
        elif team == self.team2:
            self.picks_from_team2.append(pick)
    
    def add_cash(self, team: str, amount: float):
        """Add cash to the trade."""
        if team == self.team1:
            self.cash_from_team1 = amount
        elif team == self.team2:
            self.cash_from_team2 = amount
    
    def get_salary_difference(self, contract_manager: ContractManager) -> Tuple[float, float]:
        """Get salary difference for both teams."""
        salary1 = 0.0
        salary2 = 0.0
        
        for player in self.players_from_team1:
            contract = contract_manager.get_player_contract(self.team1, player)
            if contract:
                salary1 += contract.annual_salary
        
        for player in self.players_from_team2:
            contract = contract_manager.get_player_contract(self.team2, player)
            if contract:
                salary2 += contract.annual_salary
        
        return salary1, salary2


# ==========================
# TRADE VALIDATOR
# ==========================

class TradeValidator:
    """Validate trades against NBA rules."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
        self.calculator = SalaryCapCalculator()
        self.apron = ApronRestrictions()
        self.alerts = ApronAlerts()
    
    def validate_trade(self, trade: TradeProposal) -> Tuple[bool, List[str]]:
        """Validate a complete trade proposal."""
        errors = []
        
        # Check roster size (must have at least 1 player after trade)
        errors.extend(self._check_roster_size(trade))
        
        # Check salary matching
        errors.extend(self._check_salary_matching(trade))
        
        # Check apron restrictions
        errors.extend(self._check_apron_restrictions(trade))
        
        # Check cash rules
        errors.extend(self._check_cash_rules(trade))
        
        # Check draft pick rules
        errors.extend(self._check_draft_pick_rules(trade))
        
        # Check no-trade clauses
        errors.extend(self._check_no_trade_clauses(trade))
        
        return len(errors) == 0, errors
    
    def _check_roster_size(self, trade: TradeProposal) -> List[str]:
        """Ensure teams won't have empty rosters."""
        errors = []
        
        team1_contracts = self.contract_manager.get_team_contracts(trade.team1)
        team2_contracts = self.contract_manager.get_team_contracts(trade.team2)
        
        team1_after = len(team1_contracts) - len(trade.players_from_team1) + len(trade.players_from_team2)
        team2_after = len(team2_contracts) - len(trade.players_from_team2) + len(trade.players_from_team1)
        
        if team1_after < 1:
            errors.append(f"{trade.team1} would have empty roster after trade")
        
        if team2_after < 1:
            errors.append(f"{trade.team2} would have empty roster after trade")
        
        if team1_after > 15:
            errors.append(f"{trade.team1} would exceed 15 player roster limit")
        
        if team2_after > 15:
            errors.append(f"{trade.team2} would exceed 15 player roster limit")
        
        return errors
    
    def _check_salary_matching(self, trade: TradeProposal) -> List[str]:
        """Check NBA salary matching rules."""
        errors = []
        
        salary1, salary2 = trade.get_salary_difference(self.contract_manager)
        
        payroll1 = self.contract_manager.get_team_payroll(trade.team1)
        payroll2 = self.contract_manager.get_team_payroll(trade.team2)
        
        apron1 = self.apron.get_apron_status(payroll1)
        apron2 = self.apron.get_apron_status(payroll2)
        
        # Team 1 salary matching
        if apron1["over_cap"]:
            if len(trade.players_from_team1) == 0 and len(trade.players_from_team2) > 0:
                # Team 1 receiving players while over cap
                if len(trade.players_from_team2) == 1:
                    # Single player - must match within 125% + $100k
                    min_salary = salary2 * 0.75 - 0.1
                    max_salary = salary2 * 1.25 + 0.1
                    if salary1 < min_salary or salary1 > max_salary:
                        errors.append(f"{trade.team1} salary ${salary1:.2f}M not within 125% rule for ${salary2:.2f}M")
                else:
                    # Multiple players - must match within 110% + $100k
                    min_salary = salary2 * 0.9 - 0.1
                    max_salary = salary2 * 1.1 + 0.1
                    if salary1 < min_salary or salary1 > max_salary:
                        errors.append(f"{trade.team1} salary ${salary1:.2f}M not within 110% rule for ${salary2:.2f}M")
        
        # Team 2 salary matching
        if apron2["over_cap"]:
            if len(trade.players_from_team2) == 0 and len(trade.players_from_team1) > 0:
                # Team 2 receiving players while over cap
                if len(trade.players_from_team1) == 1:
                    # Single player - must match within 125% + $100k
                    min_salary = salary1 * 0.75 - 0.1
                    max_salary = salary1 * 1.25 + 0.1
                    if salary2 < min_salary or salary2 > max_salary:
                        errors.append(f"{trade.team2} salary ${salary2:.2f}M not within 125% rule for ${salary1:.2f}M")
                else:
                    # Multiple players - must match within 110% + $100k
                    min_salary = salary1 * 0.9 - 0.1
                    max_salary = salary1 * 1.1 + 0.1
                    if salary2 < min_salary or salary2 > max_salary:
                        errors.append(f"{trade.team2} salary ${salary2:.2f}M not within 110% rule for ${salary1:.2f}M")
        
        # Check apron restrictions on salary difference
        if apron1["over_first_apron"]:
            max_takeback = salary1 * 1.1  # Can only take back 110% of what they send
            if salary2 > max_takeback:
                errors.append(f"{trade.team1} over first apron - cannot take back more than 110% of sent salary")
        
        if apron2["over_first_apron"]:
            max_takeback = salary2 * 1.1
            if salary1 > max_takeback:
                errors.append(f"{trade.team2} over first apron - cannot take back more than 110% of sent salary")
        
        return errors
    
    def _check_apron_restrictions(self, trade: TradeProposal) -> List[str]:
        """Check apron-related restrictions."""
        errors = []
        
        payroll1 = self.contract_manager.get_team_payroll(trade.team1)
        payroll2 = self.contract_manager.get_team_payroll(trade.team2)
        
        apron1 = self.apron.get_apron_status(payroll1)
        apron2 = self.apron.get_apron_status(payroll2)
        
        salary1, salary2 = trade.get_salary_difference(self.contract_manager)
        new_payroll1 = payroll1 - salary1 + salary2
        new_payroll2 = payroll2 - salary2 + salary1
        
        # Check if trade would push team over apron
        if apron1["over_second_apron"]:
            errors.append(f"{trade.team1} already over second apron - severe restrictions apply")
        
        if apron2["over_second_apron"]:
            errors.append(f"{trade.team2} already over second apron - severe restrictions apply")
        
        # Warn about apron entry
        if not apron1["over_second_apron"] and new_payroll1 > salary_config.second_apron:
            errors.append(f"WARNING: {trade.team1} would enter second apron (${salary_config.second_apron}M)")
        
        if not apron2["over_second_apron"] and new_payroll2 > salary_config.second_apron:
            errors.append(f"WARNING: {trade.team2} would enter second apron (${salary_config.second_apron}M)")
        
        return errors
    
    def _check_cash_rules(self, trade: TradeProposal) -> List[str]:
        """Check cash trading rules."""
        errors = []
        
        payroll1 = self.contract_manager.get_team_payroll(trade.team1)
        payroll2 = self.contract_manager.get_team_payroll(trade.team2)
        
        apron1 = self.apron.get_apron_status(payroll1)
        apron2 = self.apron.get_apron_status(payroll2)
        
        # Max cash is $5.4M
        max_cash = 5.4
        
        if trade.cash_from_team1 > max_cash:
            errors.append(f"{trade.team1} cash ${trade.cash_from_team1:.2f}M exceeds maximum ${max_cash:.2f}M")
        
        if trade.cash_from_team2 > max_cash:
            errors.append(f"{trade.team2} cash ${trade.cash_from_team2:.2f}M exceeds maximum ${max_cash:.2f}M")
        
        # Teams over second apron cannot send cash
        if apron1["over_second_apron"] and trade.cash_from_team1 > 0:
            errors.append(f"{trade.team1} over second apron - cannot send cash")
        
        if apron2["over_second_apron"] and trade.cash_from_team2 > 0:
            errors.append(f"{trade.team2} over second apron - cannot send cash")
        
        return errors
    
    def _check_draft_pick_rules(self, trade: TradeProposal) -> List[str]:
        """Check draft pick trading rules."""
        errors = []
        
        payroll1 = self.contract_manager.get_team_payroll(trade.team1)
        payroll2 = self.contract_manager.get_team_payroll(trade.team2)
        
        apron1 = self.apron.get_apron_status(payroll1)
        apron2 = self.apron.get_apron_status(payroll2)
        
        # Teams over second apron cannot trade distant future first-round picks
        if apron1["over_second_apron"]:
            for pick in trade.picks_from_team1:
                if pick.get("round") == 1 and pick.get("year", 0) - 2024 >= 7:
                    errors.append(f"{trade.team1} over second apron - cannot trade distant future first-round pick")
        
        if apron2["over_second_apron"]:
            for pick in trade.picks_from_team2:
                if pick.get("round") == 1 and pick.get("year", 0) - 2024 >= 7:
                    errors.append(f"{trade.team2} over second apron - cannot trade distant future first-round pick")
        
        # Stepien rule (cannot trade first-round picks in consecutive years)
        # This would require tracking pick history - simplified check here
        if len(trade.picks_from_team1) > 2:
            errors.append(f"{trade.team1} trading too many first-round picks - check Stepien rule")
        
        if len(trade.picks_from_team2) > 2:
            errors.append(f"{trade.team2} trading too many first-round picks - check Stepien rule")
        
        return errors
    
    def _check_no_trade_clauses(self, trade: TradeProposal) -> List[str]:
        """Check for no-trade clauses."""
        errors = []
        
        for player in trade.players_from_team1:
            contract = self.contract_manager.get_player_contract(trade.team1, player)
            if contract and contract.no_trade_clause:
                errors.append(f"{player} has no-trade clause - cannot be traded without consent")
        
        for player in trade.players_from_team2:
            contract = self.contract_manager.get_player_contract(trade.team2, player)
            if contract and contract.no_trade_clause:
                errors.append(f"{player} has no-trade clause - cannot be traded without consent")
        
        return errors


# ==========================
# TRADE EXECUTOR
# ==========================

class TradeExecutor:
    """Execute validated trades."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
        self.trade_history = []  # Track all completed trades
    
    def execute_trade(self, trade: TradeProposal) -> Tuple[bool, str]:
        """Execute a trade proposal."""
        # Get contracts for all players
        team1_contracts = []
        team2_contracts = []
        
        for player in trade.players_from_team1:
            contract = self.contract_manager.get_player_contract(trade.team1, player)
            if contract:
                team1_contracts.append(contract)
        
        for player in trade.players_from_team2:
            contract = self.contract_manager.get_player_contract(trade.team2, player)
            if contract:
                team2_contracts.append(contract)
        
        # Remove from old teams
        for contract in team1_contracts:
            self.contract_manager.remove_contract(trade.team1, contract.player_name)
        
        for contract in team2_contracts:
            self.contract_manager.remove_contract(trade.team2, contract.player_name)
        
        # Update contract teams
        for contract in team1_contracts:
            contract.team = trade.team2
            self.contract_manager.add_contract(contract)
        
        for contract in team2_contracts:
            contract.team = trade.team1
            self.contract_manager.add_contract(contract)
        
        # Record trade
        self.trade_history.append({
            "team1": trade.team1,
            "team2": trade.team2,
            "players_from_team1": trade.players_from_team1,
            "players_from_team2": trade.players_from_team2,
            "picks_from_team1": trade.picks_from_team1,
            "picks_from_team2": trade.picks_from_team2,
            "cash_from_team1": trade.cash_from_team1,
            "cash_from_team2": trade.cash_from_team2
        })
        
        return True, f"Trade executed: {trade.team1} ↔ {trade.team2}"


# ==========================
# TRADE DISPLAY
# ==========================

class TradeDisplay:
    """Display trade information."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
    
    def display_trade_summary(self, trade: TradeProposal):
        """Display a summary of the trade."""
        from colors import RESET, BOLD, CYAN, GREEN, YELLOW, WHITE
        
        salary1, salary2 = trade.get_salary_difference(self.contract_manager)
        
        print(f"\n{BOLD}{CYAN}  🔄 TRADE PROPOSAL{RESET}")
        print(f"{'═'*70}")
        
        print(f"\n{BOLD}{trade.team1} receives:{RESET}")
        if trade.players_from_team2:
            for player in trade.players_from_team2:
                contract = self.contract_manager.get_player_contract(trade.team2, player)
                salary = contract.annual_salary if contract else 0
                print(f"  • {player} (${salary:.2f}M)")
        else:
            print(f"  • No players")
        
        if trade.picks_from_team2:
            for pick in trade.picks_from_team2:
                print(f"  • {pick['year']} {pick['round']}{'st' if pick['round'] == 1 else 'nd'} round pick")
        
        if trade.cash_from_team2 > 0:
            print(f"  • ${trade.cash_from_team2:.2f}M cash")
        
        print(f"\n{BOLD}{trade.team2} receives:{RESET}")
        if trade.players_from_team1:
            for player in trade.players_from_team1:
                contract = self.contract_manager.get_player_contract(trade.team1, player)
                salary = contract.annual_salary if contract else 0
                print(f"  • {player} (${salary:.2f}M)")
        else:
            print(f"  • No players")
        
        if trade.picks_from_team1:
            for pick in trade.picks_from_team1:
                print(f"  • {pick['year']} {pick['round']}{'st' if pick['round'] == 1 else 'nd'} round pick")
        
        if trade.cash_from_team1 > 0:
            print(f"  • ${trade.cash_from_team1:.2f}M cash")
        
        print(f"\n{BOLD}Salary Summary:{RESET}")
        print(f"  {trade.team1} sends: ${salary1:.2f}M")
        print(f"  {trade.team2} sends: ${salary2:.2f}M")
        print(f"  Difference: ${abs(salary1 - salary2):.2f}M")
        
        print(f"{'═'*70}\n")
    
    def display_trade_validation(self, is_valid: bool, errors: List[str]):
        """Display trade validation results."""
        from colors import RESET, BOLD, GREEN, RED
        
        if is_valid:
            print(f"{GREEN}{BOLD}✅ Trade is VALID{RESET}\n")
        else:
            print(f"{RED}{BOLD}❌ Trade is INVALID{RESET}")
            print(f"{RED}Errors:{RESET}")
            for error in errors:
                print(f"  • {error}")
            print()


# ==========================
# AI TRADE LOGIC
# ==========================

class AITradeLogic:
    """AI decision-making for trades."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
        self.validator = TradeValidator(contract_manager)
    
    def evaluate_trade_interest(self, team: str, trade: TradeProposal) -> float:
        """Evaluate AI team's interest in a trade (0-100)."""
        # Simplified evaluation - in full system would consider:
        # - Team needs (position, overall rating)
        # - Financial impact
        # - Future draft capital
        # - Win-now vs rebuild mode
        
        salary1, salary2 = trade.get_salary_difference(self.contract_manager)
        
        if team == trade.team1:
            incoming_salary = salary2
            outgoing_salary = salary1
            incoming_players = len(trade.players_from_team2)
        else:
            incoming_salary = salary1
            outgoing_salary = salary2
            incoming_players = len(trade.players_from_team1)
        
        # Base interest
        interest = 50.0
        
        # Prefer getting more talent
        if incoming_players > 0:
            interest += 20.0
        
        # Financial considerations
        payroll = self.contract_manager.get_team_payroll(team)
        new_payroll = payroll - outgoing_salary + incoming_salary
        
        # If over cap, prefer salary reduction
        if payroll > salary_config.soft_cap:
            if incoming_salary < outgoing_salary:
                interest += 15.0
            else:
                interest -= 10.0
        
        # Cap at 0-100
        return max(0, min(100, interest))
    
    def should_accept_trade(self, team: str, trade: TradeProposal) -> Tuple[bool, str]:
        """Determine if AI team should accept trade."""
        # Validate trade first
        is_valid, errors = self.validator.validate_trade(trade)
        if not is_valid:
            return False, "Trade violates NBA rules"
        
        # Evaluate interest
        interest = self.evaluate_trade_interest(team, trade)
        
        # Accept if interest is high enough
        if interest >= 60:
            return True, f"Trade accepted (interest: {interest:.0f})"
        elif interest >= 40:
            # Maybe accept with some randomness
            import random
            if random.random() < 0.5:
                return True, f"Trade accepted (interest: {interest:.0f})"
            else:
                return False, f"Trade declined (interest: {interest:.0f})"
        else:
            return False, f"Trade declined (interest: {interest:.0f})"


# ==========================
# INITIALIZATION
# ==========================

# These will be initialized with the contract manager when needed
# trade_validator = TradeValidator(contract_manager)
# trade_executor = TradeExecutor(contract_manager)
# trade_display = TradeDisplay(contract_manager)
# ai_trade_logic = AITradeLogic(contract_manager)
