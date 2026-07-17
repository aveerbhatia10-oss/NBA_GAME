# ==========================================
# news_system.py
# NBA Financial News System
# ==========================================

from typing import Dict, List, Tuple
from datetime import datetime
from salary_cap import salary_config, format_currency
import random


# ==========================
# NEWS ARTICLE CLASS
# ==========================

class NewsArticle:
    """Represents a news article about financial events."""
    
    def __init__(self, headline: str, content: str, article_type: str, 
                 teams: List[str] = None, timestamp: datetime = None):
        self.headline = headline
        self.content = content
        self.article_type = article_type  # trade, signing, tax, apron, extension, waiver, buyout
        self.teams = teams or []
        self.timestamp = timestamp or datetime.now()
        self.priority = self._determine_priority()
    
    def _determine_priority(self) -> int:
        """Determine article priority (1-5, 5 = highest)."""
        high_priority_types = ["tax", "apron", "major_trade"]
        medium_priority_types = ["signing", "extension"]
        
        if self.article_type in high_priority_types:
            return 5
        elif self.article_type in medium_priority_types:
            return 3
        else:
            return 2
    
    def to_dict(self) -> Dict:
        """Convert article to dictionary."""
        return {
            "headline": self.headline,
            "content": self.content,
            "article_type": self.article_type,
            "teams": self.teams,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority
        }


# ==========================
# NEWS GENERATOR
# ==========================

class NewsGenerator:
    """Generate news articles about financial events."""
    
    def __init__(self):
        self.templates = {
            "tax": [
                "{team} enters luxury tax with ${tax}M bill",
                "{team} pays ${tax}M in luxury tax this season",
                "Heavy spending: {team} faces ${tax}M luxury tax penalty"
            ],
            "apron": [
                "{team} crosses first apron - restrictions apply",
                "🚨 {team} enters second apron - severe penalties",
                "{team} apron breach limits roster flexibility"
            ],
            "signing": [
                "{team} signs {player} to ${salary}M contract",
                "Major addition: {player} joins {team} for ${salary}M",
                "{team} lands {player} in ${salary}M deal"
            ],
            "trade": [
                "{team1} trades {player} to {team2}",
                "Blockbuster: {team1} and {team2} complete trade",
                "{team1} acquires {player} from {team2}"
            ],
            "extension": [
                "{team} extends {player} for ${salary}M",
                "{player} signs extension with {team}",
                "{team} locks up {player} with ${salary}M extension"
            ],
            "waiver": [
                "{team} waives {player}",
                "{player} waived by {team}",
                "{team} cuts ties with {player}"
            ],
            "buyout": [
                "{player} reaches buyout agreement with {team}",
                "{team} buyouts {player}",
                "{player} bought out by {team}"
            ],
            "cap_space": [
                "{team} creates ${space}M in cap room",
                "{team} positioned with ${space}M cap space",
                "Financial flexibility: {team} has ${space}M available"
            ]
        }
    
    def generate_tax_news(self, team: str, tax_amount: float) -> NewsArticle:
        """Generate news about luxury tax."""
        template = random.choice(self.templates["tax"])
        headline = template.format(team=team, tax=tax_amount)
        
        content = (
            f"{team} will pay ${tax_amount:.2f}M in luxury tax this season. "
            f"The team's payroll exceeded the luxury tax threshold of ${salary_config.luxury_tax}M. "
            f"This impacts their financial flexibility for future moves."
        )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="tax",
            teams=[team]
        )
    
    def generate_apron_news(self, team: str, apron_type: str) -> NewsArticle:
        """Generate news about apron violations."""
        template = random.choice(self.templates["apron"])
        headline = template.format(team=team)
        
        if apron_type == "second":
            content = (
                f"🚨 BREAKING: {team} has crossed the second apron (${salary_config.second_apron}M). "
                f"This triggers severe penalties including no taxpayer MLE, no cash in trades, "
                f"and restrictions on trading future draft picks. The team's roster building "
                f"flexibility will be significantly impacted."
            )
        else:
            content = (
                f"{team} has crossed the first apron (${salary_config.first_apron}M). "
                f"The team can no longer use the full Mid-Level Exception and faces "
                f"restrictions on salary aggregation in trades."
            )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="apron",
            teams=[team]
        )
    
    def generate_signing_news(self, team: str, player: str, salary: float, years: int) -> NewsArticle:
        """Generate news about free agent signing."""
        template = random.choice(self.templates["signing"])
        headline = template.format(team=team, player=player, salary=salary)
        
        content = (
            f"{team} has signed {player} to a {years}-year, ${salary:.2f}M contract. "
            f"This move addresses {team}'s roster needs and impacts their cap position. "
            f"The deal includes {years} years of guaranteed salary."
        )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="signing",
            teams=[team]
        )
    
    def generate_trade_news(self, team1: str, team2: str, players1: List[str], players2: List[str]) -> NewsArticle:
        """Generate news about trade."""
        template = random.choice(self.templates["trade"])
        
        if len(players1) == 1 and len(players2) == 1:
            headline = template.format(team1=team1, team2=team2, player=players1[0])
        else:
            headline = f"{team1} and {team2} complete multi-player trade"
        
        content = (
            f"{team1} and {team2} have agreed to a trade. "
            f"{team1} sends {', '.join(players1)} to {team2} "
            f"in exchange for {', '.join(players2)}. "
            f"Both teams look to improve their roster construction."
        )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="trade",
            teams=[team1, team2]
        )
    
    def generate_extension_news(self, team: str, player: str, salary: float, years: int) -> NewsArticle:
        """Generate news about contract extension."""
        template = random.choice(self.templates["extension"])
        headline = template.format(team=team, player=player, salary=salary)
        
        content = (
            f"{team} has extended {player}'s contract for {years} years at ${salary:.2f}M per season. "
            f"This move secures a key piece of their roster long-term and provides "
            f"financial stability for both player and team."
        )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="extension",
            teams=[team]
        )
    
    def generate_waiver_news(self, team: str, player: str, dead_money: float = 0) -> NewsArticle:
        """Generate news about waiver."""
        template = random.choice(self.templates["waiver"])
        headline = template.format(team=team, player=player)
        
        if dead_money > 0:
            content = (
                f"{team} has waived {player}, creating ${dead_money:.2f}M in dead money. "
                f"The move clears a roster spot but impacts the team's cap flexibility "
                f"for the remainder of the contract term."
            )
        else:
            content = (
                f"{team} has waived {player}. The player becomes an unrestricted free agent "
                f"and can sign with any team."
            )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="waiver",
            teams=[team]
        )
    
    def generate_buyout_news(self, team: str, player: str, buyout_amount: float) -> NewsArticle:
        """Generate news about contract buyout."""
        template = random.choice(self.templates["buyout"])
        headline = template.format(team=team, player=player)
        
        content = (
            f"{player} has reached a buyout agreement with {team} worth ${buyout_amount:.2f}M. "
            f"The player will become a free agent and can sign with any team. "
            f"This move provides {team} with immediate cap relief."
        )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="buyout",
            teams=[team]
        )
    
    def generate_cap_space_news(self, team: str, cap_space: float) -> NewsArticle:
        """Generate news about cap space creation."""
        template = random.choice(self.templates["cap_space"])
        headline = template.format(team=team, space=cap_space)
        
        content = (
            f"{team} has created ${cap_space:.2f}M in cap space through recent moves. "
            f"This financial flexibility positions the team to be active in free agency "
            f"and pursue additional roster improvements."
        )
        
        return NewsArticle(
            headline=headline,
            content=content,
            article_type="cap_space",
            teams=[team]
        )


# ==========================
# NEWS FEED MANAGER
# ==========================

class NewsFeedManager:
    """Manage news feed and article distribution."""
    
    def __init__(self):
        self.articles = []  # List of NewsArticle objects
        self.generator = NewsGenerator()
    
    def add_article(self, article: NewsArticle):
        """Add an article to the news feed."""
        self.articles.append(article)
    
    def get_recent_articles(self, count: int = 10) -> List[NewsArticle]:
        """Get most recent articles."""
        return sorted(self.articles, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_articles_by_type(self, article_type: str, count: int = 10) -> List[NewsArticle]:
        """Get articles filtered by type."""
        filtered = [a for a in self.articles if a.article_type == article_type]
        return sorted(filtered, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_articles_by_team(self, team: str, count: int = 10) -> List[NewsArticle]:
        """Get articles about a specific team."""
        filtered = [a for a in self.articles if team in a.teams]
        return sorted(filtered, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_headlines(self, count: int = 5) -> List[str]:
        """Get recent headlines."""
        recent = self.get_recent_articles(count)
        return [article.headline for article in recent]
    
    def clear_old_articles(self, days: int = 30):
        """Remove articles older than specified days."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        self.articles = [a for a in self.articles if a.timestamp > cutoff]


# ==========================
# NEWS DISPLAY
# ==========================

class NewsDisplay:
    """Display news articles in formatted output."""
    
    def __init__(self, news_manager: NewsFeedManager):
        self.news_manager = news_manager
    
    def display_headlines(self, count: int = 5):
        """Display recent headlines."""
        from colors import RESET, BOLD, CYAN, YELLOW, WHITE
        
        headlines = self.news_manager.get_headlines(count)
        
        print(f"\n{BOLD}{CYAN}📰 NBA FINANCIAL NEWS{RESET}")
        print(f"{'═'*70}")
        
        if not headlines:
            print(f"  {WHITE}No recent news.{RESET}")
        else:
            for i, headline in enumerate(headlines, 1):
                print(f"  {YELLOW}{i}.{RESET} {headline}")
        
        print(f"{'═'*70}\n")
    
    def display_full_article(self, article: NewsArticle):
        """Display a full news article."""
        from colors import RESET, BOLD, CYAN, GREEN, WHITE
        
        print(f"\n{BOLD}{CYAN}{'═'*70}")
        print(f"  📰 {article.headline}")
        print(f"{'═'*70}{RESET}")
        
        print(f"\n  {article.content}\n")
        
        print(f"  {WHITE}Type: {article.article_type.upper()}{RESET}")
        print(f"  {WHITE}Teams: {', '.join(article.teams)}{RESET}")
        print(f"  {WHITE}Priority: {article.priority}/5{RESET}")
        print(f"  {WHITE}Posted: {article.timestamp.strftime('%Y-%m-%d %H:%M')}{RESET}")
        
        print(f"\n{BOLD}{CYAN}{'═'*70}{RESET}\n")
    
    def display_news_feed(self, count: int = 10):
        """Display multiple news articles."""
        from colors import RESET, BOLD, CYAN, GREEN, RED, WHITE
        
        articles = self.news_manager.get_recent_articles(count)
        
        print(f"\n{BOLD}{CYAN}{'='*70}")
        print(f"  📰 NBA FINANCIAL NEWS FEED")
        print(f"{'='*70}{RESET}\n")
        
        if not articles:
            print(f"  {WHITE}No recent news articles.{RESET}\n")
            return
        
        for i, article in enumerate(articles, 1):
            # Color code by priority
            if article.priority >= 5:
                priority_color = RED
            elif article.priority >= 3:
                priority_color = YELLOW
            else:
                priority_color = WHITE
            
            print(f"{priority_color}[{article.priority}]{RESET} {article.headline}")
            print(f"  {DIM}{article.timestamp.strftime('%Y-%m-%d %H:%M')}{RESET}")
            print(f"  {article.content[:100]}...")
            print()
        
        print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")


# ==========================
# AUTO-NEWS GENERATION
# ==========================

class AutoNewsGenerator:
    """Automatically generate news based on financial events."""
    
    def __init__(self, news_manager: NewsFeedManager):
        self.news_manager = news_manager
        self.generator = NewsGenerator()
    
    def on_tax_payment(self, team: str, tax_amount: float):
        """Generate news when team pays luxury tax."""
        if tax_amount > 0:
            article = self.generator.generate_tax_news(team, tax_amount)
            self.news_manager.add_article(article)
    
    def on_apron_cross(self, team: str, apron_type: str):
        """Generate news when team crosses apron."""
        article = self.generator.generate_apron_news(team, apron_type)
        self.news_manager.add_article(article)
    
    def on_signing(self, team: str, player: str, salary: float, years: int):
        """Generate news when player signs."""
        if salary >= 10:  # Only significant signings
            article = self.generator.generate_signing_news(team, player, salary, years)
            self.news_manager.add_article(article)
    
    def on_trade(self, team1: str, team2: str, players1: List[str], players2: List[str]):
        """Generate news when trade occurs."""
        article = self.generator.generate_trade_news(team1, team2, players1, players2)
        self.news_manager.add_article(article)
    
    def on_extension(self, team: str, player: str, salary: float, years: int):
        """Generate news when extension signed."""
        if salary >= 15:  # Only significant extensions
            article = self.generator.generate_extension_news(team, player, salary, years)
            self.news_manager.add_article(article)
    
    def on_waiver(self, team: str, player: str, dead_money: float = 0):
        """Generate news when player waived."""
        if dead_money >= 5 or player in ["Star Player"]:  # Significant waivers
            article = self.generator.generate_waiver_news(team, player, dead_money)
            self.news_manager.add_article(article)
    
    def on_buyout(self, team: str, player: str, buyout_amount: float):
        """Generate news when buyout occurs."""
        article = self.generator.generate_buyout_news(team, player, buyout_amount)
        self.news_manager.add_article(article)
    
    def on_cap_space_created(self, team: str, cap_space: float):
        """Generate news when significant cap space created."""
        if cap_space >= 15:  # Only significant cap space
            article = self.generator.generate_cap_space_news(team, cap_space)
            self.news_manager.add_article(article)


# ==========================
# INITIALIZATION
# ==========================

news_feed_manager = NewsFeedManager()
news_display = NewsDisplay(news_feed_manager)
auto_news_generator = AutoNewsGenerator(news_feed_manager)
