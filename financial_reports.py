# ==========================================
# financial_reports.py
# NBA Financial Reports & Dashboard
# ==========================================

from typing import Dict, List, Tuple
from salary_cap import salary_config, SalaryCapCalculator, format_currency
from contracts import ContractManager
from luxury_tax import LuxuryTaxCalculator, ApronRestrictions


# ==========================
# FINANCIAL METRICS
# ==========================

class FinancialMetrics:
    """Calculate financial metrics for teams."""
    
    def __init__(self, contract_manager: ContractManager):
        self.contract_manager = contract_manager
        self.calculator = SalaryCapCalculator()
        self.tax_calc = LuxuryTaxCalculator()
        self.apron = ApronRestrictions()
    
    def get_team_financial_data(self, team: str) -> Dict:
        """Get complete financial data for a team."""
        contracts = self.contract_manager.get_team_contracts(team)
        payroll = self.contract_manager.get_team_payroll(team)
        
        return {
            "team": team,
            "payroll": payroll,
            "cap_space": self.calculator.calculate_cap_space(payroll),
            "luxury_tax": self.tax_calc.calculate_tax_owed(payroll)["total_tax"],
            "total_cost": payroll + self.tax_calc.calculate_tax_owed(payroll)["total_tax"],
            "over_cap": payroll > salary_config.soft_cap,
            "over_tax": payroll > salary_config.luxury_tax,
            "over_first_apron": payroll > salary_config.first_apron,
            "over_second_apron": payroll > salary_config.second_apron,
            "guaranteed": self.calculator.calculate_guaranteed_salary([c.to_dict() for c in contracts]),
            "non_guaranteed": self.calculator.calculate_non_guaranteed_salary([c.to_dict() for c in contracts]),
            "dead_money": self.calculator.calculate_dead_money([c.to_dict() for c in contracts]),
            "roster_spots": self.calculator.get_roster_spots_used([c.to_dict() for c in contracts]),
            "contracts": len(contracts)
        }
    
    def get_all_teams_financial_data(self) -> List[Dict]:
        """Get financial data for all teams."""
        all_data = []
        for team in self.contract_manager.contracts:
            data = self.get_team_financial_data(team)
            all_data.append(data)
        return all_data


# ==========================
# FINANCIAL RANKINGS
# ==========================

class FinancialRankings:
    """Generate financial rankings across the league."""
    
    def __init__(self, contract_manager: ContractManager):
        self.metrics = FinancialMetrics(contract_manager)
    
    def biggest_payroll(self) -> List[Dict]:
        """Rank teams by payroll (highest to lowest)."""
        all_data = self.metrics.get_all_teams_financial_data()
        return sorted(all_data, key=lambda x: x["payroll"], reverse=True)
    
    def lowest_payroll(self) -> List[Dict]:
        """Rank teams by payroll (lowest to highest)."""
        all_data = self.metrics.get_all_teams_financial_data()
        return sorted(all_data, key=lambda x: x["payroll"])
    
    def luxury_tax_teams(self) -> List[Dict]:
        """Get teams paying luxury tax, ranked by tax amount."""
        all_data = self.metrics.get_all_teams_financial_data()
        tax_teams = [d for d in all_data if d["luxury_tax"] > 0]
        return sorted(tax_teams, key=lambda x: x["luxury_tax"], reverse=True)
    
    def cap_space_rankings(self) -> List[Dict]:
        """Rank teams by cap space (highest to lowest)."""
        all_data = self.metrics.get_all_teams_financial_data()
        cap_space_teams = [d for d in all_data if d["cap_space"] > 0]
        return sorted(cap_space_teams, key=lambda x: x["cap_space"], reverse=True)
    
    def worst_contracts(self) -> List[Tuple[str, str, float]]:
        """Identify worst value contracts (salary vs overall)."""
        worst = []
        
        for team in self.contract_manager.contracts:
            contracts = self.contract_manager.get_team_contracts(team)
            for contract in contracts:
                if contract.dead_money > 0:
                    continue  # Skip dead money
                
                # Simple value calculation: salary / overall (lower is worse value)
                # This would be enhanced with actual player data in full system
                value_ratio = contract.annual_salary / 75  # Placeholder overall
                worst.append((team, contract.player_name, value_ratio))
        
        return sorted(worst, key=lambda x: x[2], reverse=True)[:10]
    
    def best_value_contracts(self) -> List[Tuple[str, str, float]]:
        """Identify best value contracts."""
        best = []
        
        for team in self.contract_manager.contracts:
            contracts = self.contract_manager.get_team_contracts(team)
            for contract in contracts:
                if contract.dead_money > 0:
                    continue
                
                value_ratio = contract.annual_salary / 75  # Placeholder overall
                best.append((team, contract.player_name, value_ratio))
        
        return sorted(best, key=lambda x: x[2])[:10]
    
    def expiring_contracts(self) -> List[Tuple[str, str, float]]:
        """Get all expiring contracts."""
        expiring = []
        
        for team in self.contract_manager.contracts:
            contracts = self.contract_manager.get_team_contracts(team)
            for contract in contracts:
                if contract.years_remaining == 1 and contract.dead_money == 0:
                    expiring.append((team, contract.player_name, contract.annual_salary))
        
        return sorted(expiring, key=lambda x: x[2], reverse=True)
    
    def most_future_cap_space(self) -> List[Tuple[str, float]]:
        """Rank teams by future cap space (simplified)."""
        # This would use multi-year projections in full system
        future_space = []
        
        for team in self.contract_manager.contracts:
            contracts = self.contract_manager.get_team_contracts(team)
            expiring_salary = sum(c.annual_salary for c in contracts if c.years_remaining == 1)
            future_space.append((team, expiring_salary))
        
        return sorted(future_space, key=lambda x: x[1], reverse=True)


# ==========================
# FINANCIAL DASHBOARD
# ==========================

class FinancialDashboard:
    """Display comprehensive financial dashboard."""
    
    def __init__(self, contract_manager: ContractManager):
        self.metrics = FinancialMetrics(contract_manager)
        self.rankings = FinancialRankings(contract_manager)
    
    def display_main_dashboard(self):
        """Display main financial dashboard."""
        from colors import RESET, BOLD, CYAN, GREEN, RED, YELLOW, WHITE
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  📊 NBA FINANCIAL DASHBOARD")
        print(f"{'='*70}{RESET}\n")
        
        # League Summary
        self._display_league_summary()
        
        # Top Payrolls
        self._display_top_payrolls()
        
        # Luxury Tax Teams
        self._display_luxury_tax_teams()
        
        # Cap Space Leaders
        self._display_cap_space_leaders()
        
        print(f"\n{BOLD}{CYAN}{'='*70}{RESET}\n")
    
    def _display_league_summary(self):
        """Display league-wide financial summary."""
        from colors import RESET, BOLD, CYAN, WHITE
        
        all_data = self.metrics.get_all_teams_financial_data()
        
        total_payroll = sum(d["payroll"] for d in all_data)
        total_tax = sum(d["luxury_tax"] for d in all_data)
        tax_teams = len([d for d in all_data if d["luxury_tax"] > 0])
        apron_teams = len([d for d in all_data if d["over_second_apron"]])
        
        print(f"{BOLD}League Summary{RESET}")
        print(f"  Total League Payroll:  {format_currency(total_payroll)}")
        print(f"  Total Luxury Tax:      {RED if total_tax > 0 else WHITE}{format_currency(total_tax)}{RESET}")
        print(f"  Teams Paying Tax:      {tax_teams}/30")
        print(f"  Teams Over 2nd Apron:  {RED if apron_teams > 0 else WHITE}{apron_teams}/30{RESET}")
        print()
    
    def _display_top_payrolls(self):
        """Display teams with highest payrolls."""
        from colors import RESET, BOLD, YELLOW, WHITE
        
        top_payrolls = self.rankings.biggest_payroll()[:5]
        
        print(f"{BOLD}Top 5 Payrolls{RESET}")
        print(f"  {'TEAM':<20} {'PAYROLL':>12} {'CAP SPACE':>12}")
        print(f"  {'─'*44}")
        
        for data in top_payrolls:
            cap_color = GREEN if data["cap_space"] > 0 else RED
            print(f"  {data['team']:<20} {format_currency(data['payroll']):>12} {cap_color}{format_currency(data['cap_space']):>12}{RESET}")
        
        print()
    
    def _display_luxury_tax_teams(self):
        """Display teams paying luxury tax."""
        from colors import RESET, BOLD, RED, WHITE
        
        tax_teams = self.rankings.luxury_tax_teams()[:5]
        
        print(f"{BOLD}Luxury Tax Teams{RESET}")
        print(f"  {'TEAM':<20} {'TAX OWED':>12} {'TOTAL COST':>12}")
        print(f"  {'─'*44}")
        
        for data in tax_teams:
            print(f"  {data['team']:<20} {RED}{format_currency(data['luxury_tax']):>12}{RESET} {format_currency(data['total_cost']):>12}")
        
        if not tax_teams:
            print(f"  {WHITE}No teams paying luxury tax{RESET}")
        
        print()
    
    def _display_cap_space_leaders(self):
        """Display teams with most cap space."""
        from colors import RESET, BOLD, GREEN, WHITE
        
        cap_leaders = self.rankings.cap_space_rankings()[:5]
        
        print(f"{BOLD}Cap Space Leaders{RESET}")
        print(f"  {'TEAM':<20} {'CAP SPACE':>12} {'PAYROLL':>12}")
        print(f"  {'─'*44}")
        
        for data in cap_leaders:
            print(f"  {data['team']:<20} {GREEN}{format_currency(data['cap_space']):>12}{RESET} {format_currency(data['payroll']):>12}")
        
        if not cap_leaders:
            print(f"  {WHITE}No teams with cap space{RESET}")
        
        print()
    
    def display_contract_rankings(self):
        """Display contract value rankings."""
        from colors import RESET, BOLD, CYAN, GREEN, RED, WHITE
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  💰 CONTRACT VALUE ANALYSIS")
        print(f"{'='*70}{RESET}\n")
        
        # Worst Contracts
        worst = self.rankings.worst_contracts()[:5]
        
        print(f"{BOLD}Worst Value Contracts{RESET}")
        print(f"  {'TEAM':<20} {'PLAYER':<20} {'SALARY':>10}")
        print(f"  {'─'*50}")
        
        for team, player, ratio in worst:
            print(f"  {team:<20} {player:<20} ${ratio*75:>9.2f}M")
        
        print()
        
        # Best Value Contracts
        best = self.rankings.best_value_contracts()[:5]
        
        print(f"{BOLD}Best Value Contracts{RESET}")
        print(f"  {'TEAM':<20} {'PLAYER':<20} {'SALARY':>10}")
        print(f"  {'─'*50}")
        
        for team, player, ratio in best:
            print(f"  {team:<20} {player:<20} ${ratio*75:>9.2f}M")
        
        print()
    
    def display_expiring_contracts(self):
        """Display all expiring contracts."""
        from colors import RESET, BOLD, CYAN, WHITE
        
        expiring = self.rankings.expiring_contracts()[:15]
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  📋 EXPIRING CONTRACTS")
        print(f"{'='*70}{RESET}\n")
        
        print(f"  {'TEAM':<20} {'PLAYER':<20} {'SALARY':>10}")
        print(f"  {'─'*50}")
        
        for team, player, salary in expiring:
            print(f"  {team:<20} {player:<20} ${salary:>9.2f}M")
        
        print()
    
    def display_team_comparison(self, teams: List[str]):
        """Display financial comparison between specific teams."""
        from colors import RESET, BOLD, CYAN, GREEN, RED, YELLOW, WHITE
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  📈 TEAM FINANCIAL COMPARISON")
        print(f"{'='*70}{RESET}\n")
        
        print(f"  {'TEAM':<20} {'PAYROLL':>12} {'CAP SPACE':>12} {'TAX':>10} {'APRON':>8}")
        print(f"  {'─'*62}")
        
        for team in teams:
            data = self.metrics.get_team_financial_data(team)
            
            payroll_color = RED if data["over_tax"] else YELLOW if data["over_cap"] else GREEN
            cap_color = GREEN if data["cap_space"] > 0 else RED
            tax_color = RED if data["luxury_tax"] > 0 else WHITE
            apron_status = "2nd" if data["over_second_apron"] else "1st" if data["over_first_apron"] else "Tax" if data["over_tax"] else "Cap" if data["over_cap"] else "None"
            apron_color = RED if data["over_second_apron"] else YELLOW if data["over_first_apron"] else tax_color
            
            print(f"  {team:<20} {payroll_color}{format_currency(data['payroll']):>12}{RESET} "
                  f"{cap_color}{format_currency(data['cap_space']):>12}{RESET} "
                  f"{tax_color}{format_currency(data['luxury_tax']):>10}{RESET} "
                  f"{apron_color}{apron_status:>8}{RESET}")
        
        print()


# ==========================
# FINANCIAL ALERTS
# ==========================

class FinancialAlerts:
    """Generate financial alerts and warnings."""
    
    def __init__(self, contract_manager: ContractManager):
        self.metrics = FinancialMetrics(contract_manager)
    
    def get_critical_alerts(self) -> List[str]:
        """Get critical financial alerts."""
        alerts = []
        
        all_data = self.metrics.get_all_teams_financial_data()
        
        # Teams over second apron
        for data in all_data:
            if data["over_second_apron"]:
                alerts.append(f"🚨 {data['team']} is over Second Apron (${salary_config.second_apron}M)")
        
        # Teams with high dead money
        for data in all_data:
            if data["dead_money"] > 20:
                alerts.append(f"⚠️ {data['team']} has ${data['dead_money']:.2f}M in dead money")
        
        # Teams near apron
        for data in all_data:
            if not data["over_first_apron"] and data["payroll"] > salary_config.first_apron - 5:
                alerts.append(f"📊 {data['team']} approaching First Apron (${salary_config.first_apron}M)")
        
        return alerts
    
    def display_alerts(self):
        """Display all financial alerts."""
        from colors import RESET, BOLD, CYAN, RED, YELLOW, WHITE
        
        alerts = self.get_critical_alerts()
        
        if not alerts:
            return
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  ⚠️ FINANCIAL ALERTS")
        print(f"{'='*70}{RESET}\n")
        
        for alert in alerts:
            color = RED if "🚨" in alert else YELLOW
            print(f"  {color}{alert}{RESET}")
        
        print()


# ==========================
# INITIALIZATION
# ==========================

# These will be initialized with the contract manager when needed
# financial_metrics = FinancialMetrics(contract_manager)
# financial_rankings = FinancialRankings(contract_manager)
# financial_dashboard = FinancialDashboard(contract_manager)
# financial_alerts = FinancialAlerts(contract_manager)
