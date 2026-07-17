# ==========================================
# luxury_tax.py
# NBA Luxury Tax & Apron System
# ==========================================

from typing import Dict, List, Tuple
from salary_cap import salary_config, SalaryCapCalculator, format_currency


# ==========================
# LUXURY TAX CALCULATOR
# ==========================

class LuxuryTaxCalculator:
    """Calculate luxury tax penalties and apron restrictions."""
    
    def __init__(self, config=None):
        self.config = config or salary_config
        self.calculator = SalaryCapCalculator(config)
    
    def calculate_tax_owed(self, payroll: float) -> Dict[str, float]:
        """Calculate total luxury tax owed with breakdown."""
        if payroll <= self.config.luxury_tax:
            return {
                "total_tax": 0.0,
                "over_tax": 0.0,
                "bracket_1": 0.0,
                "bracket_2": 0.0,
                "bracket_3": 0.0,
                "bracket_4": 0.0,
                "bracket_5": 0.0
            }
        
        over = payroll - self.config.luxury_tax
        tax_breakdown = {
            "total_tax": 0.0,
            "over_tax": over,
            "bracket_1": 0.0,  # 0-5M over: $1.50 per $1
            "bracket_2": 0.0,  # 5-10M over: $1.75 per $1
            "bracket_3": 0.0,  # 10-15M over: $2.50 per $1
            "bracket_4": 0.0,  # 15-20M over: $3.25 per $1
            "bracket_5": 0.0   # 20M+: $4.25 per $1
        }
        
        # Bracket 1: 0-5M over
        if over > 0:
            bracket = min(over, 5.0)
            tax_breakdown["bracket_1"] = bracket * 1.50
            tax_breakdown["total_tax"] += tax_breakdown["bracket_1"]
            over -= bracket
        
        # Bracket 2: 5-10M over
        if over > 0:
            bracket = min(over, 5.0)
            tax_breakdown["bracket_2"] = bracket * 1.75
            tax_breakdown["total_tax"] += tax_breakdown["bracket_2"]
            over -= bracket
        
        # Bracket 3: 10-15M over
        if over > 0:
            bracket = min(over, 5.0)
            tax_breakdown["bracket_3"] = bracket * 2.50
            tax_breakdown["total_tax"] += tax_breakdown["bracket_3"]
            over -= bracket
        
        # Bracket 4: 15-20M over
        if over > 0:
            bracket = min(over, 5.0)
            tax_breakdown["bracket_4"] = bracket * 3.25
            tax_breakdown["total_tax"] += tax_breakdown["bracket_4"]
            over -= bracket
        
        # Bracket 5: 20M+ over (progressive)
        if over > 0:
            tax_breakdown["bracket_5"] = over * 4.25
            tax_breakdown["total_tax"] += tax_breakdown["bracket_5"]
        
        # Round all values
        for key in tax_breakdown:
            tax_breakdown[key] = round(tax_breakdown[key], 2)
        
        return tax_breakdown
    
    def get_tax_rate(self, payroll: float) -> str:
        """Get current tax rate description."""
        if payroll <= self.config.luxury_tax:
            return "No Tax"
        
        over = payroll - self.config.luxury_tax
        
        if over <= 5:
            return "$1.50 per $1"
        elif over <= 10:
            return "$1.75 per $1"
        elif over <= 15:
            return "$2.50 per $1"
        elif over <= 20:
            return "$3.25 per $1"
        else:
            return "$4.25+ per $1"


# ==========================
# APRON RESTRICTIONS
# ==========================

class ApronRestrictions:
    """Manage apron restrictions and penalties."""
    
    def __init__(self, config=None):
        self.config = config or salary_config
        self.calculator = SalaryCapCalculator(config)
    
    def get_apron_status(self, payroll: float) -> Dict[str, any]:
        """Get complete apron status for a team."""
        apron_status = self.calculator.get_apron_status(payroll)
        
        return {
            "payroll": payroll,
            "soft_cap": self.config.soft_cap,
            "luxury_tax": self.config.luxury_tax,
            "first_apron": self.config.first_apron,
            "second_apron": self.config.second_apron,
            "over_cap": apron_status["over_cap"],
            "over_tax": apron_status["over_tax"],
            "over_first_apron": apron_status["over_first_apron"],
            "over_second_apron": apron_status["over_second_apron"],
            "cap_space": self.calculator.calculate_cap_space(payroll),
            "distance_to_tax": round(self.config.luxury_tax - payroll, 2),
            "distance_to_first_apron": round(self.config.first_apron - payroll, 2),
            "distance_to_second_apron": round(self.config.second_apron - payroll, 2)
        }
    
    def get_first_apron_restrictions(self, payroll: float) -> List[str]:
        """Get list of first apron restrictions."""
        restrictions = []
        
        if payroll > self.config.first_apron:
            restrictions.append("Cannot use full Mid-Level Exception")
            restrictions.append("Cannot aggregate salaries in trades if restricted")
            restrictions.append("Cannot sign certain waived players")
            restrictions.append("Cannot take back significantly more salary than sent out")
            restrictions.append("Cannot use Bi-Annual Exception")
        
        return restrictions
    
    def get_second_apron_restrictions(self, payroll: float) -> List[str]:
        """Get list of second apron restrictions (severe penalties)."""
        restrictions = []
        
        if payroll > self.config.second_apron:
            restrictions.append("NO taxpayer/non-taxpayer Mid-Level Exception")
            restrictions.append("NO cash in trades")
            restrictions.append("CANNOT aggregate salaries in trades")
            restrictions.append("CANNOT trade distant future first-round picks when restricted")
            restrictions.append("REDUCED roster building flexibility")
            restrictions.append("INCREASED luxury tax rates")
            restrictions.append("Future draft pick penalties apply")
        
        return restrictions
    
    def can_use_full_mle(self, payroll: float) -> Tuple[bool, str]:
        """Check if team can use full Non-Taxpayer MLE."""
        if payroll > self.config.first_apron:
            return False, "Over first apron - cannot use full MLE"
        
        if payroll + self.config.mle_non_taxpayer > self.config.first_apron:
            return False, "Using full MLE would exceed first apron"
        
        return True, "Can use full Non-Taxpayer MLE"
    
    def can_use_bae(self, payroll: float) -> Tuple[bool, str]:
        """Check if team can use Bi-Annual Exception."""
        if payroll > self.config.luxury_tax:
            return False, "Over luxury tax - cannot use BAE"
        
        if payroll + self.config.bae > self.config.first_apron:
            return False, "Using BAE would exceed first apron"
        
        return True, "Can use Bi-Annual Exception"
    
    def can_aggregate_salaries(self, payroll: float) -> Tuple[bool, str]:
        """Check if team can aggregate salaries in trades."""
        if payroll > self.config.second_apron:
            return False, "Over second apron - cannot aggregate salaries"
        
        if payroll > self.config.first_apron:
            return False, "Over first apron - restricted aggregation"
        
        return True, "Can aggregate salaries"
    
    def can_send_cash(self, payroll: float) -> Tuple[bool, str]:
        """Check if team can send cash in trades."""
        if payroll > self.config.second_apron:
            return False, "Over second apron - cannot send cash"
        
        return True, "Can send cash (max $5.4M)"
    
    def can_trade_future_picks(self, payroll: float) -> Tuple[bool, str]:
        """Check if team can trade distant future first-round picks."""
        if payroll > self.config.second_apron:
            return False, "Over second apron - cannot trade distant future firsts"
        
        return True, "Can trade future first-round picks"


# ==========================
# APRON ALERTS
# ==========================

class ApronAlerts:
    """Generate alerts for apron violations and warnings."""
    
    def __init__(self, config=None):
        self.config = config or salary_config
        self.restrictions = ApronRestrictions(config)
    
    def check_first_apron_entry(self, team: str, payroll: float, previous_payroll: float) -> str:
        """Check if team just entered first apron."""
        if previous_payroll <= self.config.first_apron and payroll > self.config.first_apron:
            return f"⚠️ {team} has entered the First Apron (${self.config.first_apron}M). Restrictions apply."
        return None
    
    def check_second_apron_entry(self, team: str, payroll: float, previous_payroll: float) -> str:
        """Check if team just entered second apron."""
        if previous_payroll <= self.config.second_apron and payroll > self.config.second_apron:
            return f"🚨 {team} has entered the Second Apron (${self.config.second_apron}M). Severe penalties apply!"
        return None
    
    def check_tax_entry(self, team: str, payroll: float, previous_payroll: float) -> str:
        """Check if team just entered luxury tax."""
        if previous_payroll <= self.config.luxury_tax and payroll > self.config.luxury_tax:
            tax_calc = LuxuryTaxCalculator()
            tax_owed = tax_calc.calculate_tax_owed(payroll)["total_tax"]
            return f"💰 {team} has entered the Luxury Tax. Estimated tax: ${tax_owed:.2f}M"
        return None
    
    def get_all_alerts(self, team: str, payroll: float, previous_payroll: float) -> List[str]:
        """Get all apron/tax alerts for a team."""
        alerts = []
        
        alert = self.check_tax_entry(team, payroll, previous_payroll)
        if alert:
            alerts.append(alert)
        
        alert = self.check_first_apron_entry(team, payroll, previous_payroll)
        if alert:
            alerts.append(alert)
        
        alert = self.check_second_apron_entry(team, payroll, previous_payroll)
        if alert:
            alerts.append(alert)
        
        return alerts
    
    def get_warning_message(self, action: str, payroll: float) -> str:
        """Get warning message for restricted action."""
        restrictions = self.restrictions.get_first_apron_restrictions(payroll)
        second_restrictions = self.restrictions.get_second_apron_restrictions(payroll)
        
        if second_restrictions:
            return f"❌ CANNOT {action}: Team is over Second Apron. Severe restrictions apply."
        
        if restrictions:
            return f"⚠️ WARNING: {action} restricted - Team is over First Apron."
        
        return ""


# ==========================
# REPEATER TAX
# ==========================

class RepeaterTax:
    """Handle repeater tax for teams consistently over luxury tax."""
    
    def __init__(self):
        self.tax_history = {}  # {team: [years_over_tax]}
    
    def record_tax_year(self, team: str, over_tax: bool):
        """Record whether team was over tax this year."""
        if team not in self.tax_history:
            self.tax_history[team] = []
        
        self.tax_history[team].append(over_tax)
        
        # Keep only last 4 years
        if len(self.tax_history[team]) > 4:
            self.tax_history[team] = self.tax_history[team][-4:]
    
    def is_repeater(self, team: str) -> bool:
        """Check if team is repeater (3 of 4 years over tax)."""
        if team not in self.tax_history:
            return False
        
        recent_years = self.tax_history[team][-4:]
        if len(recent_years) < 3:
            return False
        
        tax_years = sum(1 for year in recent_years if year)
        return tax_years >= 3
    
    def get_repeater_penalty_multiplier(self, team: str) -> float:
        """Get repeater tax penalty multiplier."""
        if self.is_repeater(team):
            return 1.5  # 50% additional tax
        return 1.0


# ==========================
# FINANCIAL DISPLAY
# ==========================

class FinancialDisplay:
    """Display financial information in formatted tables."""
    
    def __init__(self, config=None):
        self.config = config or salary_config
        self.tax_calc = LuxuryTaxCalculator(config)
        self.apron = ApronRestrictions(config)
    
    def display_team_financial_summary(self, team: str, payroll: float, contracts: List[Dict]):
        """Display complete financial summary for a team."""
        from colors import RESET, BOLD, GREEN, RED, YELLOW, ORANGE, CYAN, WHITE
        
        status = self.apron.get_apron_status(payroll)
        tax_breakdown = self.tax_calc.calculate_tax_owed(payroll)
        
        # Calculate contract breakdown
        guaranteed = sum(c.get("annual_salary", 0) for c in contracts if c.get("guaranteed", True))
        non_guaranteed = sum(c.get("annual_salary", 0) for c in contracts if not c.get("guaranteed", True))
        dead_money = sum(c.get("dead_money", 0) for c in contracts)
        roster_spots = len([c for c in contracts if c.get("dead_money", 0) == 0])
        
        print(f"\n{'═'*70}")
        print(f"{BOLD}{CYAN}  💰 FINANCIAL SUMMARY — {team}{RESET}")
        print(f"{'═'*70}")
        
        # Payroll Information
        print(f"\n{BOLD}  PAYROLL INFORMATION{RESET}")
        print(f"  Current Payroll:      {GREEN if payroll <= self.config.soft_cap else YELLOW if payroll <= self.config.luxury_tax else RED}{format_currency(payroll)}{RESET}")
        print(f"  Salary Cap:           {format_currency(self.config.soft_cap)}")
        print(f"  Cap Space:            {GREEN if status['cap_space'] > 0 else RED}{format_currency(status['cap_space'])}{RESET}")
        print(f"  Luxury Tax Line:      {format_currency(self.config.luxury_tax)}")
        print(f"  First Apron:          {format_currency(self.config.first_apron)}")
        print(f"  Second Apron:         {format_currency(self.config.second_apron)}")
        
        # Tax Information
        print(f"\n{BOLD}  LUXURY TAX{RESET}")
        if tax_breakdown["total_tax"] > 0:
            print(f"  Tax Owed:             {RED}{format_currency(tax_breakdown['total_tax'])}{RESET}")
            print(f"  Over Tax:             {format_currency(tax_breakdown['over_tax'])}")
            print(f"  Tax Rate:             {self.tax_calc.get_tax_rate(payroll)}")
            print(f"  Total Cost:           {RED}{format_currency(payroll + tax_breakdown['total_tax'])}{RESET}")
        else:
            print(f"  Tax Owed:             {GREEN}No Tax{RESET}")
        
        # Apron Status
        print(f"\n{BOLD}  APRON STATUS{RESET}")
        print(f"  Over Cap:              {GREEN if not status['over_cap'] else YELLOW}{'Yes' if status['over_cap'] else 'No'}{RESET}")
        print(f"  Over Luxury Tax:      {GREEN if not status['over_tax'] else YELLOW}{'Yes' if status['over_tax'] else 'No'}{RESET}")
        print(f"  Over First Apron:     {GREEN if not status['over_first_apron'] else ORANGE}{'Yes' if status['over_first_apron'] else 'No'}{RESET}")
        print(f"  Over Second Apron:    {GREEN if not status['over_second_apron'] else RED}{'Yes' if status['over_second_apron'] else 'No'}{RESET}")
        
        # Contract Breakdown
        print(f"\n{BOLD}  CONTRACT BREAKDOWN{RESET}")
        print(f"  Guaranteed Salary:    {format_currency(guaranteed)}")
        print(f"  Non-Guaranteed:       {format_currency(non_guaranteed)}")
        print(f"  Dead Money:           {RED if dead_money > 0 else GREEN}{format_currency(dead_money)}{RESET}")
        print(f"  Roster Spots Used:    {roster_spots}/15")
        print(f"  Minimum Salary:       {format_currency(self.config.min_salary)}")
        
        # Available Exceptions
        exceptions = self.calculator.get_available_exceptions(payroll)
        if exceptions:
            print(f"\n{BOLD}  AVAILABLE EXCEPTIONS{RESET}")
            for name, amount in exceptions.items():
                print(f"  {name}:              {format_currency(amount)}")
        
        # Restrictions
        first_restrictions = self.apron.get_first_apron_restrictions(payroll)
        second_restrictions = self.apron.get_second_apron_restrictions(payroll)
        
        if first_restrictions or second_restrictions:
            print(f"\n{BOLD}  RESTRICTIONS{RESET}")
            for restriction in first_restrictions:
                print(f"  {ORANGE}⚠️ {restriction}{RESET}")
            for restriction in second_restrictions:
                print(f"  {RED}🚨 {restriction}{RESET}")
        
        print(f"{'═'*70}\n")
    
    def display_tax_brackets(self):
        """Display luxury tax bracket information."""
        from colors import RESET, BOLD, CYAN, WHITE
        
        print(f"\n{BOLD}{CYAN}  LUXURY TAX BRACKETS{RESET}")
        print(f"{'═'*50}")
        print(f"  0-5M over:     $1.50 per $1")
        print(f"  5-10M over:    $1.75 per $1")
        print(f"  10-15M over:   $2.50 per $1")
        print(f"  15-20M over:   $3.25 per $1")
        print(f"  20M+ over:     $4.25+ per $1")
        print(f"{'═'*50}\n")


# ==========================
# INITIALIZATION
# ==========================

luxury_tax_calculator = LuxuryTaxCalculator()
apron_restrictions = ApronRestrictions()
apron_alerts = ApronAlerts()
repeater_tax = RepeaterTax()
financial_display = FinancialDisplay()
