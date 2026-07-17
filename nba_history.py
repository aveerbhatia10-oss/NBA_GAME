# ==========================================
# nba_history.py
# Real-world NBA championship history
# ==========================================

from typing import Dict, List, Optional

from colors import color_team_name, teams as color_teams, RESET, BOLD

YELLOW = "\033[38;2;255;210;0m"
CYAN   = "\033[38;2;0;210;230m"
LBLUE  = "\033[38;2;80;160;255m"
DIM    = "\033[2m"
WHITE  = "\033[38;2;240;240;240m"

# Map historical franchise names to modern teams for color display.
HISTORICAL_TEAM_ALIASES: Dict[str, str] = {
    "Minneapolis Lakers": "Los Angeles Lakers",
    "St. Louis Hawks": "Atlanta Hawks",
    "Baltimore Bullets": "Washington Wizards",
    "Washington Bullets": "Washington Wizards",
    "Ft. Wayne Pistons": "Detroit Pistons",
    "Syracuse Nationals": "Philadelphia 76ers",
    "Rochester Royals": "Sacramento Kings",
    "Philadelphia Warriors": "Golden State Warriors",
    "San Francisco Warriors": "Golden State Warriors",
    "New Jersey Nets": "Brooklyn Nets",
    "Seattle SuperSonics": "Oklahoma City Thunder",
}

NBA_CHAMPIONS_HISTORY: List[Dict[str, str]] = [
    {"season": "2025-26", "champion": "New York Knicks",       "runner_up": "San Antonio Spurs",        "series": "4-1"},
    {"season": "2024-25", "champion": "Oklahoma City Thunder", "runner_up": "Indiana Pacers",           "series": "4-3"},
    {"season": "2023-24", "champion": "Boston Celtics",        "runner_up": "Dallas Mavericks",         "series": "4-1"},
    {"season": "2022-23", "champion": "Denver Nuggets",        "runner_up": "Miami Heat",               "series": "4-1"},
    {"season": "2021-22", "champion": "Golden State Warriors", "runner_up": "Boston Celtics",           "series": "4-2"},
    {"season": "2020-21", "champion": "Milwaukee Bucks",       "runner_up": "Phoenix Suns",             "series": "4-2"},
    {"season": "2019-20", "champion": "Los Angeles Lakers",    "runner_up": "Miami Heat",               "series": "4-2"},
    {"season": "2018-19", "champion": "Toronto Raptors",       "runner_up": "Golden State Warriors",    "series": "4-2"},
    {"season": "2017-18", "champion": "Golden State Warriors", "runner_up": "Cleveland Cavaliers",      "series": "4-0"},
    {"season": "2016-17", "champion": "Golden State Warriors", "runner_up": "Cleveland Cavaliers",      "series": "4-1"},
    {"season": "2015-16", "champion": "Cleveland Cavaliers",   "runner_up": "Golden State Warriors",    "series": "4-3"},
    {"season": "2014-15", "champion": "Golden State Warriors", "runner_up": "Cleveland Cavaliers",      "series": "4-2"},
    {"season": "2013-14", "champion": "San Antonio Spurs",     "runner_up": "Miami Heat",               "series": "4-1"},
    {"season": "2012-13", "champion": "Miami Heat",            "runner_up": "San Antonio Spurs",        "series": "4-3"},
    {"season": "2011-12", "champion": "Miami Heat",            "runner_up": "Oklahoma City Thunder",    "series": "4-1"},
    {"season": "2010-11", "champion": "Dallas Mavericks",      "runner_up": "Miami Heat",               "series": "4-2"},
    {"season": "2009-10", "champion": "Los Angeles Lakers",    "runner_up": "Boston Celtics",           "series": "4-3"},
    {"season": "2008-09", "champion": "Los Angeles Lakers",    "runner_up": "Orlando Magic",            "series": "4-1"},
    {"season": "2007-08", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-2"},
    {"season": "2006-07", "champion": "San Antonio Spurs",     "runner_up": "Cleveland Cavaliers",      "series": "4-0"},
    {"season": "2005-06", "champion": "Miami Heat",            "runner_up": "Dallas Mavericks",         "series": "4-2"},
    {"season": "2004-05", "champion": "San Antonio Spurs",     "runner_up": "Detroit Pistons",          "series": "4-3"},
    {"season": "2003-04", "champion": "Detroit Pistons",       "runner_up": "Los Angeles Lakers",       "series": "4-1"},
    {"season": "2002-03", "champion": "San Antonio Spurs",     "runner_up": "New Jersey Nets",          "series": "4-2"},
    {"season": "2001-02", "champion": "Los Angeles Lakers",    "runner_up": "New Jersey Nets",          "series": "4-0"},
    {"season": "2000-01", "champion": "Los Angeles Lakers",    "runner_up": "Philadelphia 76ers",       "series": "4-1"},
    {"season": "1999-00", "champion": "Los Angeles Lakers",    "runner_up": "Indiana Pacers",           "series": "4-2"},
    {"season": "1998-99", "champion": "San Antonio Spurs",     "runner_up": "New York Knicks",          "series": "4-1"},
    {"season": "1997-98", "champion": "Chicago Bulls",         "runner_up": "Utah Jazz",                "series": "4-2"},
    {"season": "1996-97", "champion": "Chicago Bulls",         "runner_up": "Utah Jazz",                "series": "4-2"},
    {"season": "1995-96", "champion": "Chicago Bulls",         "runner_up": "Seattle SuperSonics",      "series": "4-2"},
    {"season": "1994-95", "champion": "Houston Rockets",       "runner_up": "Orlando Magic",            "series": "4-0"},
    {"season": "1993-94", "champion": "Houston Rockets",       "runner_up": "New York Knicks",          "series": "4-3"},
    {"season": "1992-93", "champion": "Chicago Bulls",         "runner_up": "Phoenix Suns",             "series": "4-2"},
    {"season": "1991-92", "champion": "Chicago Bulls",         "runner_up": "Portland Trail Blazers",   "series": "4-2"},
    {"season": "1990-91", "champion": "Chicago Bulls",         "runner_up": "Los Angeles Lakers",       "series": "4-1"},
    {"season": "1989-90", "champion": "Detroit Pistons",       "runner_up": "Portland Trail Blazers",   "series": "4-1"},
    {"season": "1988-89", "champion": "Detroit Pistons",       "runner_up": "Los Angeles Lakers",       "series": "4-0"},
    {"season": "1987-88", "champion": "Los Angeles Lakers",    "runner_up": "Detroit Pistons",          "series": "4-3"},
    {"season": "1986-87", "champion": "Los Angeles Lakers",    "runner_up": "Boston Celtics",           "series": "4-2"},
    {"season": "1985-86", "champion": "Boston Celtics",        "runner_up": "Houston Rockets",          "series": "4-2"},
    {"season": "1984-85", "champion": "Los Angeles Lakers",    "runner_up": "Boston Celtics",           "series": "4-2"},
    {"season": "1983-84", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-3"},
    {"season": "1982-83", "champion": "Philadelphia 76ers",    "runner_up": "Los Angeles Lakers",       "series": "4-0"},
    {"season": "1981-82", "champion": "Los Angeles Lakers",    "runner_up": "Philadelphia 76ers",       "series": "4-2"},
    {"season": "1980-81", "champion": "Boston Celtics",        "runner_up": "Houston Rockets",          "series": "4-2"},
    {"season": "1979-80", "champion": "Los Angeles Lakers",    "runner_up": "Philadelphia 76ers",       "series": "4-2"},
    {"season": "1978-79", "champion": "Seattle SuperSonics",   "runner_up": "Washington Bullets",       "series": "4-1"},
    {"season": "1977-78", "champion": "Washington Bullets",    "runner_up": "Seattle SuperSonics",        "series": "4-3"},
    {"season": "1976-77", "champion": "Portland Trail Blazers","runner_up": "Philadelphia 76ers",       "series": "4-2"},
    {"season": "1975-76", "champion": "Boston Celtics",        "runner_up": "Phoenix Suns",             "series": "4-2"},
    {"season": "1974-75", "champion": "Golden State Warriors", "runner_up": "Washington Bullets",       "series": "4-0"},
    {"season": "1973-74", "champion": "Boston Celtics",        "runner_up": "Milwaukee Bucks",          "series": "4-3"},
    {"season": "1972-73", "champion": "New York Knicks",       "runner_up": "Los Angeles Lakers",       "series": "4-1"},
    {"season": "1971-72", "champion": "Los Angeles Lakers",    "runner_up": "New York Knicks",          "series": "4-1"},
    {"season": "1970-71", "champion": "Milwaukee Bucks",       "runner_up": "Baltimore Bullets",        "series": "4-0"},
    {"season": "1969-70", "champion": "New York Knicks",       "runner_up": "Los Angeles Lakers",       "series": "4-3"},
    {"season": "1968-69", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-3"},
    {"season": "1967-68", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-2"},
    {"season": "1966-67", "champion": "Philadelphia 76ers",    "runner_up": "San Francisco Warriors",   "series": "4-2"},
    {"season": "1965-66", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-3"},
    {"season": "1964-65", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-1"},
    {"season": "1963-64", "champion": "Boston Celtics",        "runner_up": "San Francisco Warriors",     "series": "4-1"},
    {"season": "1962-63", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-2"},
    {"season": "1961-62", "champion": "Boston Celtics",        "runner_up": "Los Angeles Lakers",       "series": "4-3"},
    {"season": "1960-61", "champion": "Boston Celtics",        "runner_up": "St. Louis Hawks",          "series": "4-1"},
    {"season": "1959-60", "champion": "Boston Celtics",        "runner_up": "St. Louis Hawks",          "series": "4-3"},
    {"season": "1958-59", "champion": "Boston Celtics",        "runner_up": "Minneapolis Lakers",       "series": "4-0"},
    {"season": "1957-58", "champion": "St. Louis Hawks",       "runner_up": "Boston Celtics",           "series": "4-2"},
    {"season": "1956-57", "champion": "Boston Celtics",        "runner_up": "St. Louis Hawks",          "series": "4-3"},
    {"season": "1955-56", "champion": "Philadelphia Warriors", "runner_up": "Ft. Wayne Pistons",         "series": "4-1"},
    {"season": "1954-55", "champion": "Syracuse Nationals",    "runner_up": "Ft. Wayne Pistons",        "series": "4-3"},
    {"season": "1953-54", "champion": "Minneapolis Lakers",   "runner_up": "Syracuse Nationals",       "series": "4-3"},
    {"season": "1952-53", "champion": "Minneapolis Lakers",   "runner_up": "New York Knicks",          "series": "4-1"},
    {"season": "1951-52", "champion": "Minneapolis Lakers",   "runner_up": "New York Knicks",          "series": "4-1"},
    {"season": "1950-51", "champion": "Rochester Royals",      "runner_up": "New York Knicks",          "series": "4-3"},
    {"season": "1949-50", "champion": "Minneapolis Lakers",   "runner_up": "Syracuse Nationals",       "series": "4-2"},
    {"season": "1948-49", "champion": "Minneapolis Lakers",   "runner_up": "Washington Capitols",        "series": "4-2"},
    {"season": "1947-48", "champion": "Baltimore Bullets",     "runner_up": "Philadelphia Warriors",    "series": "4-2"},
    {"season": "1946-47", "champion": "Philadelphia Warriors", "runner_up": "Chicago Stags",              "series": "4-1"},
]


def _color_hist_team(team_name: str) -> str:
    """Color a team name, including historical franchises."""
    lookup = HISTORICAL_TEAM_ALIASES.get(team_name, team_name)
    if lookup in color_teams:
        return color_team_name(lookup)
    return f"{BOLD}{WHITE}{team_name}{RESET}"


def _championship_totals() -> Dict[str, int]:
    totals: Dict[str, int] = {}
    for entry in NBA_CHAMPIONS_HISTORY:
        champ = entry["champion"]
        totals[champ] = totals.get(champ, 0) + 1
    return totals


def show_nba_champions_history(highlight_team: Optional[str] = None):
    """Display the full real-world NBA championship history."""
    print(f"\n{BOLD}{LBLUE}{'═'*66}{RESET}")
    print(f"{BOLD}{LBLUE}  🏆 NBA CHAMPIONS HISTORY  (1946–47 → 2025–26){RESET}")
    print(f"{BOLD}{LBLUE}{'═'*66}{RESET}")

    totals = _championship_totals()
    top = sorted(totals.items(), key=lambda x: (-x[1], x[0]))[:8]
    print(f"\n  {BOLD}Most Titles (listed name):{RESET}")
    for team, count in top:
        you = f" {YELLOW}★{RESET}" if highlight_team and team == highlight_team else ""
        print(f"    {YELLOW}{'🏆' * min(count, 5)}{RESET}  {_color_hist_team(team)} — {count}{you}")

    print(f"\n  {BOLD}Champions by Season:{RESET}")
    print(f"  {DIM}{'Season':<10} {'Champion':<28} {'Runner-Up':<28} Series{RESET}")
    print(f"  {DIM}{'─'*66}{RESET}")

    for entry in NBA_CHAMPIONS_HISTORY:
        season = entry["season"]
        champ = entry["champion"]
        runner = entry["runner_up"]
        series = entry["series"]
        crown = f"{YELLOW}🏆{RESET}" if highlight_team and champ == highlight_team else "  "
        print(
            f"  {crown} {CYAN}{season:<8}{RESET} "
            f"{_color_hist_team(champ):<38} "
            f"{DIM}def.{RESET} {_color_hist_team(runner):<38} "
            f"{BOLD}{series}{RESET}"
        )

    print(f"\n{BOLD}{LBLUE}{'═'*66}{RESET}")
    print(f"  {DIM}{len(NBA_CHAMPIONS_HISTORY)} NBA champions since 1946–47{RESET}\n")
