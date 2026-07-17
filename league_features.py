# ==========================================
# league_features.py
# Extended league tracking, stats, and displays
# ==========================================

import random
from typing import Dict, List, Optional, Tuple, Set

from colors import color_team_name, color_team_abbr, team_abbr, RESET, BOLD
from teams import team as team_meta

# ANSI (match game.py palette)
GREEN   = "\033[38;2;0;200;80m"
RED     = "\033[38;2;220;50;50m"
YELLOW  = "\033[38;2;255;210;0m"
CYAN    = "\033[38;2;0;210;230m"
ORANGE  = "\033[38;2;255;140;0m"
WHITE   = "\033[38;2;240;240;240m"
MAGENTA = "\033[38;2;210;0;210m"
DIM     = "\033[2m"
LBLUE   = "\033[38;2;80;160;255m"

EAST = {
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
    "Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers",
    "Miami Heat", "Milwaukee Bucks", "New York Knicks", "Orlando Magic",
    "Philadelphia 76ers", "Toronto Raptors", "Washington Wizards",
}
WEST = {
    "Dallas Mavericks", "Denver Nuggets", "Golden State Warriors", "Houston Rockets",
    "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
    "Minnesota Timberwolves", "New Orleans Pelicans", "Oklahoma City Thunder",
    "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings",
    "San Antonio Spurs", "Utah Jazz",
}

PREGAME_HEADLINES = [
    "{home} looks to defend home court against {away} tonight.",
    "All eyes on {star} as {home} hosts {away}.",
    "{away} hit the road — can they steal one in {home}'s building?",
    "Rivalry alert: {home} vs {away} — bad blood brewing.",
    "{home} riding momentum — {away} want to quiet the crowd.",
    "Injury report could swing {home} vs {away}.",
    "Playoff implications on the line: {home} vs {away}.",
]

BUZZER_BEATERS = [
    "{n} pulls up from DEEP at the buzzer — {BOLD}IT'S GOOD!{RESET} 🚨",
    "Buzzer sounds… {n} releases… {BOLD}BANG! GAME!{RESET} 🚨",
    "{n} drives baseline, reverse layup at the horn — {BOLD}COUNT IT!{RESET} 🚨",
    "{n} catches, one dribble, step-back THREE… {BOLD}SWISH!{RESET} 🚨",
]


class LeagueTracker:
    """Central store for streaks, rankings, rivalries, chemistry, and franchise records."""

    def __init__(self):
        self.reset_all()

    def reset_all(self):
        self.win_streak: Dict[str, int] = {}
        self.loss_streak: Dict[str, int] = {}
        self.last_5: Dict[str, List[str]] = {}
        self.h2h: Dict[Tuple[str, str], Dict[str, int]] = {}
        self.conf_record: Dict[str, Dict[str, int]] = {}
        self.team_chemistry: Dict[str, float] = {}
        self.fan_happiness: Dict[str, float] = {}
        self.trade_block: Dict[str, List[str]] = {}
        self.player_fatigue: Dict[str, float] = {}
        self.rivalries: Dict[Tuple[str, str], int] = {}
        self.franchise_team_records: Dict[str, Dict] = {}
        self.jersey_retired: Dict[str, List[str]] = {}
        self.weekly_rankings: List[Dict] = []
        self.breakout_players: Set[str] = set()
        self._teams: List[str] = []

    def init_season(self, all_teams: List[str]):
        self._teams = list(all_teams)
        for t in all_teams:
            self.win_streak.setdefault(t, 0)
            self.loss_streak.setdefault(t, 0)
            self.last_5.setdefault(t, [])
            self.team_chemistry.setdefault(t, random.uniform(65, 82))
            self.fan_happiness.setdefault(t, random.uniform(60, 80))
            self.trade_block.setdefault(t, [])
            self.conf_record.setdefault(t, {
                "east_w": 0, "east_l": 0, "west_w": 0, "west_l": 0,
            })
            self.franchise_team_records.setdefault(t, {
                "most_pts_game": 0, "most_wins_season": 0,
                "best_record": "0-0",
            })
            self.jersey_retired.setdefault(t, [])

    def h2h_key(self, a: str, b: str) -> Tuple[str, str]:
        return tuple(sorted([a, b]))

    def record_game(self, winner: str, loser: str, score: Dict[str, int],
                    game_stats: Dict, active_rosters: Dict, gm_season: int = 1):
        """Update all league trackers after a game."""
        for tm in [winner, loser]:
            if tm not in self.win_streak:
                self.init_season([tm])

        # Streaks + last 5
        self.win_streak[winner] = self.win_streak.get(winner, 0) + 1
        self.loss_streak[winner] = 0
        self.win_streak[loser] = 0
        self.loss_streak[loser] = self.loss_streak.get(loser, 0) + 1
        for tm, result in [(winner, "W"), (loser, "L")]:
            l5 = self.last_5.setdefault(tm, [])
            l5.append(result)
            self.last_5[tm] = l5[-5:]

        # Head-to-head
        key = self.h2h_key(winner, loser)
        rec = self.h2h.setdefault(key, {key[0]: 0, key[1]: 0})
        rec[winner] = rec.get(winner, 0) + 1

        # Conference records
        w_conf = EAST if winner in EAST else WEST
        l_conf = EAST if loser in EAST else WEST
        wc = self.conf_record.setdefault(winner, {"east_w": 0, "east_l": 0, "west_w": 0, "west_l": 0})
        lc = self.conf_record.setdefault(loser, {"east_w": 0, "east_l": 0, "west_w": 0, "west_l": 0})
        if l_conf == EAST:
            wc["east_w"] += 1
            lc["east_l"] += 1
        else:
            wc["west_w"] += 1
            lc["west_l"] += 1

        # Rivalry intensity (close games + repeat matchups)
        margin = abs(score[winner] - score[loser])
        rk = self.h2h_key(winner, loser)
        ri = self.rivalries.get(rk, 20)
        if margin <= 5:
            ri = min(100, ri + 8)
        total = rec.get(key[0], 0) + rec.get(key[1], 0)
        if total >= 3:
            ri = min(100, ri + 3)
        self.rivalries[rk] = ri

        # Chemistry + fan happiness
        margin = score[winner] - score[loser]
        self._update_chemistry(winner, True, margin)
        self._update_chemistry(loser, False, margin)
        self._update_fan(winner, True, margin)
        self._update_fan(loser, False, margin)

        # Franchise team game record
        for tm, pts in score.items():
            fr = self.franchise_team_records.setdefault(tm, {"most_pts_game": 0})
            if pts > fr.get("most_pts_game", 0):
                fr["most_pts_game"] = pts

        # Fatigue from minutes (approximate from stats activity)
        for tm, pls in active_rosters.items():
            for p in pls:
                n = p["name"]
                gs = game_stats.get(n, {})
                activity = gs.get("PTS", 0) + gs.get("REB", 0) + gs.get("AST", 0)
                if activity >= 25:
                    self.player_fatigue[n] = min(100, self.player_fatigue.get(n, 0) + 12)
                elif activity >= 15:
                    self.player_fatigue[n] = min(100, self.player_fatigue.get(n, 0) + 6)
                else:
                    self.player_fatigue[n] = max(0, self.player_fatigue.get(n, 0) - 4)

    def _update_chemistry(self, team: str, won: bool, margin: int):
        c = self.team_chemistry.get(team, 70)
        if won:
            c = min(100, c + min(4, margin * 0.3 + 1))
        else:
            c = max(0, c - min(4, margin * 0.2 + 1))
        self.team_chemistry[team] = round(c, 1)

    def _update_fan(self, team: str, won: bool, margin: int):
        f = self.fan_happiness.get(team, 70)
        if won:
            f = min(100, f + min(5, margin * 0.2 + 2))
        else:
            f = max(0, f - min(4, margin * 0.15 + 1.5))
        self.fan_happiness[team] = round(f, 1)

    def decay_fatigue_rest_day(self):
        for n in list(self.player_fatigue.keys()):
            self.player_fatigue[n] = max(0, self.player_fatigue[n] - 15)

    def pick_breakout_players(self, active_rosters: Dict) -> Set[str]:
        """Random role players get a breakout game boost."""
        self.breakout_players = set()
        for tm, pls in active_rosters.items():
            role = [p for p in pls if p.get("overall", 75) < 80
                    and not p.get("active_injury")]
            if role and random.random() < 0.35:
                self.breakout_players.add(random.choice(role)["name"])
        return self.breakout_players

    def get_h2h(self, t1: str, t2: str) -> Tuple[int, int]:
        key = self.h2h_key(t1, t2)
        rec = self.h2h.get(key, {key[0]: 0, key[1]: 0})
        return rec.get(t1, 0), rec.get(t2, 0)

    def form_string(self, team: str) -> str:
        l5 = self.last_5.get(team, [])
        if not l5:
            return "—"
        return "".join(l5)

    def playoff_status(self, team: str, gm_records: Dict, games_played: int) -> Optional[str]:
        if games_played < 55:
            return None
        r = gm_records.get(team, {"W": 0, "L": 0})
        w, l = r["W"], r["L"]
        remaining = max(0, 82 - w - l)
        conf = EAST if team in EAST else WEST
        conf_teams = [t for t in self._teams if t in conf and t in gm_records]
        ranked = sorted(conf_teams, key=lambda t: gm_records[t]["W"], reverse=True)
        try:
            seed = ranked.index(team) + 1
        except ValueError:
            seed = 15
        if seed <= 6 and w >= 40:
            return "CLINCHED"
        if seed >= 10 and w + remaining < 38:
            return "ELIMINATED"
        if seed <= 8:
            return "PLAYOFF HUNT"
        return None


league = LeagueTracker()


# ── Play style parsing ──

def parse_play_style(style: str) -> Dict[str, float]:
    s = (style or "").lower()
    mods = {"pace": 1.0, "three": 0.0, "two": 0.0, "defense": 0.0, "ft": 0.0}
    if any(k in s for k in ("fast", "transition", "pace")):
        mods["pace"] = 1.06
    if any(k in s for k in ("3pt", "three", "spacing", "motion")):
        mods["three"] = 0.045
    if any(k in s for k in ("defense", "physical", "switch")):
        mods["defense"] = 0.035
    if any(k in s for k in ("inside", "post", "two big")):
        mods["two"] = 0.04
    if "isolation" in s or "superstar" in s:
        mods["two"] = max(mods["two"], 0.025)
        mods["ft"] = 0.015
    return mods


def get_team_style_mods(team: str) -> Dict[str, float]:
    meta = team_meta.get(team, {})
    return parse_play_style(meta.get("style", ""))


def crowd_intensity(home_team: str, score: Dict, t1: str, t2: str,
                    gm_records: Dict) -> float:
    """0–1 crowd factor; spikes in close games."""
    home = home_team
    away = t2 if home == t1 else t1
    hs = score.get(home, 0)
    aws = score.get(away, 0)
    diff = abs(hs - aws)
    base = 0.4
    if diff <= 3:
        base = 0.95
    elif diff <= 8:
        base = 0.75
    elif diff <= 15:
        base = 0.55
    rec = gm_records.get(home, {"W": 0, "L": 0})
    gp = max(1, rec["W"] + rec["L"])
    win_pct = rec["W"] / gp
    base += win_pct * 0.2
    base += league.fan_happiness.get(home, 70) / 500
    return min(1.0, base)


def home_court_boost(home_team: str, away_team: str, gm_records: Dict,
                     crowd: float) -> float:
    """Combined home court advantage probability boost."""
    rec = gm_records.get(home_team, {"W": 0, "L": 0})
    gp = max(1, rec["W"] + rec["L"])
    home_pct = rec["W"] / gp
    base = 0.018 + home_pct * 0.012
    base += crowd * 0.022
    rk = league.h2h_key(home_team, away_team)
    if league.rivalries.get(rk, 0) >= 50:
        base += 0.008
    return base


def fatigue_penalty(player_name: str) -> float:
    f = league.player_fatigue.get(player_name, 0)
    if f >= 70:
        return -0.04
    if f >= 45:
        return -0.02
    if f >= 25:
        return -0.01
    return 0.0


def veteran_leadership_bonus(team: str, active_rosters: Dict) -> float:
    pls = active_rosters.get(team, [])
    vets = sum(1 for p in pls if p.get("age", 25) >= 32)
    return min(0.025, vets * 0.005)


def rookie_minutes_bonus(player: Dict, minutes_used: int) -> float:
    if player.get("age", 30) <= 22 and minutes_used >= 20:
        return 0.015
    return 0.0


def breakout_boost(player_name: str) -> float:
    return 0.06 if player_name in league.breakout_players else 0.0


def chemistry_boost(team: str) -> float:
    c = league.team_chemistry.get(team, 70)
    if c >= 85:
        return 0.025
    if c >= 70:
        return 0.012
    if c <= 45:
        return -0.02
    return 0.0


def calc_attendance(home_team: str, away_team: str, active_rosters: Dict,
                    gm_records: Dict) -> int:
    rec = gm_records.get(home_team, {"W": 0, "L": 0})
    gp = max(1, rec["W"] + rec["L"])
    win_pct = rec["W"] / gp
    star = max((p.get("overall", 70) for p in active_rosters.get(home_team, [])), default=70)
    away_star = max((p.get("overall", 70) for p in active_rosters.get(away_team, [])), default=70)
    base = 15000 + int(win_pct * 8000) + int(star * 80) + int(away_star * 40)
    base += int(league.fan_happiness.get(home_team, 70) * 30)
    return min(20000, max(8000, base))


def player_of_game(game_stats: Dict) -> Tuple[str, Dict]:
    if not game_stats:
        return "?", {}
    name = max(game_stats, key=lambda n: (
        game_stats[n]["PTS"] * 1.2 + game_stats[n]["REB"] * 0.5 +
        game_stats[n]["AST"] * 0.7 + game_stats[n]["STL"] * 1.2 +
        game_stats[n]["BLK"] * 1.0
    ))
    return name, game_stats[name]


def update_ai_trade_blocks(active_rosters: Dict):
    """AI teams list surplus or underperforming players."""
    for tm, pls in active_rosters.items():
        if len(pls) <= 10:
            continue
        sorted_p = sorted(pls, key=lambda p: p.get("overall", 0))
        surplus = [p["name"] for p in sorted_p[:2] if p.get("overall", 0) < 78]
        if surplus and random.random() < 0.5:
            block = league.trade_block.setdefault(tm, [])
            for n in surplus:
                if n not in block:
                    block.append(n)


def analyze_team_needs(active_rosters: Dict, team: str) -> Dict[str, str]:
    pls = active_rosters.get(team, [])
    pos_count = {"PG": 0, "SG": 0, "SF": 0, "PF": 0, "C": 0}
    for p in pls:
        pos = p.get("pos", "?")
        if pos in pos_count:
            pos_count[pos] += 1
    needs = {}
    for pos, cnt in pos_count.items():
        if cnt == 0:
            needs[pos] = "CRITICAL"
        elif cnt == 1:
            needs[pos] = "DEPTH"
    avg_off = sum(p.get("offense", 75) for p in pls) / max(1, len(pls))
    avg_def = sum(p.get("defense", 75) for p in pls) / max(1, len(pls))
    avg_sht = sum(p.get("shooting", 75) for p in pls) / max(1, len(pls))
    avg_reb = sum(p.get("rebounding", 75) for p in pls) / max(1, len(pls))
    if avg_sht < 76:
        needs["shooting"] = "NEED"
    if avg_def < 76:
        needs["defense"] = "NEED"
    if avg_reb < 74:
        needs["rebounding"] = "NEED"
    if avg_off < 76:
        needs["scoring"] = "NEED"
    return needs


def expiring_contracts(active_rosters: Dict, team: str) -> List[Dict]:
    return [p for p in active_rosters.get(team, [])
            if p.get("contract_years", 1) <= 1]


def retire_jersey_if_legend(team: str, player: Dict, franchise_history: Dict):
    cs = franchise_history.get("career_stats", {}).get(player["name"], {})
    pts = cs.get("PTS", 0)
    awards = sum(1 for a in franchise_history.get("award_history", [])
                 if a.get("name") == player["name"])
    if pts >= 12000 or awards >= 2 or player.get("overall", 0) >= 90:
        retired = league.jersey_retired.setdefault(team, [])
        if player["name"] not in retired:
            retired.append(player["name"])


# ── Display helpers ──

def show_pregame(t1: str, t2: str, home: str, active_rosters: Dict,
                 gm_records: Dict, gm_team: Optional[str], verbose: bool):
    if not verbose:
        return
    away = t2 if home == t1 else t1
    att = calc_attendance(home, away, active_rosters, gm_records)
    star_pl = max(active_rosters.get(home, []), key=lambda p: p.get("overall", 0),
                  default={"name": "the star"})
    headline = random.choice(PREGAME_HEADLINES).format(
        home=color_team_name(home), away=color_team_abbr(away),
        star=star_pl.get("name", "?"),
    )
    h1, h2 = league.get_h2h(t1, t2)
    form_h = league.form_string(home)
    form_a = league.form_string(away)
    chem = league.team_chemistry.get(home, 70)
    style_h = team_meta.get(home, {}).get("style", "?")
    style_a = team_meta.get(away, {}).get("style", "?")

    print(f"\n  {DIM}{'─'*56}{RESET}")
    print(f"  {YELLOW}📰 {headline}{RESET}")
    print(f"  {DIM}Attendance: {att:,}  │  {color_team_abbr(home)} chemistry: {chem:.0f}/100{RESET}")
    print(f"  {DIM}H2H: {color_team_abbr(t1)} {h1}–{h2} {color_team_abbr(t2)}"
          f"  │  Form: {form_h} vs {form_a}{RESET}")
    print(f"  {DIM}{color_team_abbr(home)}: {style_h}{RESET}")
    print(f"  {DIM}{color_team_abbr(away)}: {style_a}{RESET}")

    # Injury report
    injured = []
    for tm in [t1, t2]:
        for p in active_rosters.get(tm, []):
            inj = p.get("active_injury")
            if inj and inj.get("games_left", 0) > 0:
                injured.append((tm, p["name"], inj.get("name", "?"),
                                inj.get("games_left", 0)))
    if injured:
        print(f"  {ORANGE}🏥 INJURY REPORT:{RESET}")
        for tm, name, iname, gl in injured[:6]:
            print(f"    {color_team_abbr(tm)} {name} — {iname} ({gl}g)")
    if league.breakout_players:
        names = ", ".join(list(league.breakout_players)[:3])
        print(f"  {MAGENTA}👀 Breakout watch: {names}{RESET}")
    print(f"  {DIM}{'─'*56}{RESET}\n")


def try_buzzer_beater(quarter: int, poss_in_q: int, poss_total: int,
                      score: Dict, off_team: str, def_team: str,
                      active_rosters: Dict, scorer_name: str,
                      verbose: bool) -> Optional[str]:
    if quarter != 4 or poss_in_q < poss_total - 1:
        return None
    t1, t2 = list(score.keys())
    diff = abs(score.get(t1, 0) - score.get(t2, 0))
    if diff > 3:
        return None
    if random.random() > 0.12:
        return None
    tpl = random.choice(BUZZER_BEATERS)
    msg = tpl.format(n=scorer_name, BOLD=BOLD, RESET=RESET)
    if verbose:
        print(f"\n  {RED}{BOLD}🚨 BUZZER BEATER!{RESET}  {msg}\n")
    return msg


def show_league_hub(active_rosters: Dict, gm_records: Dict, gm_team: str,
                    gm_season: int, all_teams: List[str]):
    print(f"\n{BOLD}{LBLUE}{'═'*62}{RESET}")
    print(f"{BOLD}{LBLUE}  🏀 LEAGUE HUB — Season {gm_season}{RESET}")
    print(f"{BOLD}{LBLUE}{'═'*62}{RESET}")

    # Streaks
    print(f"\n  {BOLD}🔥 Active Streaks:{RESET}")
    hot = sorted(all_teams, key=lambda t: league.win_streak.get(t, 0), reverse=True)[:5]
    for t in hot:
        ws = league.win_streak.get(t, 0)
        if ws >= 3:
            you = f" {YELLOW}★{RESET}" if t == gm_team else ""
            print(f"    {color_team_abbr(t)} {GREEN}{ws}W streak{RESET}{you}  "
                  f"Form: {league.form_string(t)}")

    # Rankings
    print(f"\n  {BOLD}📊 Team Rankings (PPG / Opp PPG):{RESET}")
    ranked = sorted(all_teams, key=lambda t: gm_records.get(t, {}).get("PF", 0), reverse=True)
    for i, t in enumerate(ranked[:5], 1):
        r = gm_records.get(t, {"PF": 0, "PA": 0, "W": 0, "L": 0})
        gp = max(1, r["W"] + r["L"])
        print(f"    #{i} OFF  {color_team_abbr(t)}  {r['PF']/gp:.1f} PPG")
    def_rank = sorted(all_teams, key=lambda t: gm_records.get(t, {}).get("PA", 999))
    print(f"\n  {BOLD}🛡️  Top Defenses:{RESET}")
    for i, t in enumerate(def_rank[:5], 1):
        r = gm_records.get(t, {"PA": 0, "W": 0, "L": 0})
        gp = max(1, r["W"] + r["L"])
        print(f"    #{i} DEF  {color_team_abbr(t)}  {r['PA']/gp:.1f} opp PPG")

    # Your team extras
    if gm_team:
        needs = analyze_team_needs(active_rosters, gm_team)
        exp = expiring_contracts(active_rosters, gm_team)
        banners = league.jersey_retired.get(gm_team, [])
        print(f"\n  {BOLD}{color_team_name(gm_team)} Snapshot:{RESET}")
        print(f"    Chemistry: {league.team_chemistry.get(gm_team, 70):.0f}/100  "
              f"Fan happiness: {league.fan_happiness.get(gm_team, 70):.0f}/100")
        if needs:
            need_str = ", ".join(f"{k}({v})" for k, v in needs.items())
            print(f"    Needs: {ORANGE}{need_str}{RESET}")
        if exp:
            print(f"    {YELLOW}⚠ {len(exp)} contract(s) expiring soon{RESET}")
        if banners:
            print(f"    {DIM}Retired jerseys: {', '.join(banners)}{RESET}")

    # Trade block league-wide
    on_block = [(t, n) for t, names in league.trade_block.items() for n in names[:2]]
    if on_block:
        print(f"\n  {BOLD}🔄 Trade Block Rumors:{RESET}")
        for t, n in on_block[:8]:
            print(f"    {DIM}{n} ({color_team_abbr(t)}){RESET}")

    print(f"\n{BOLD}{LBLUE}{'═'*62}{RESET}\n")


def show_team_needs_page(active_rosters: Dict, team: str):
    needs = analyze_team_needs(active_rosters, team)
    exp = expiring_contracts(active_rosters, team)
    print(f"\n{BOLD}{CYAN}  📋 TEAM NEEDS — {color_team_name(team)}{RESET}\n")
    print(f"  Chemistry: {league.team_chemistry.get(team, 70):.0f}/100")
    print(f"  Fan happiness: {league.fan_happiness.get(team, 70):.0f}/100")
    style = team_meta.get(team, {}).get("style", "?")
    print(f"  Play style: {DIM}{style}{RESET}\n")
    pos_needs = {k: v for k, v in needs.items() if k in ("PG", "SG", "SF", "PF", "C")}
    skill_needs = {k: v for k, v in needs.items() if k not in pos_needs}
    if pos_needs:
        print(f"  {BOLD}Position needs:{RESET}")
        for pos, lvl in pos_needs.items():
            c = RED if lvl == "CRITICAL" else ORANGE
            print(f"    {pos}: {c}{lvl}{RESET}")
    if skill_needs:
        print(f"  {BOLD}Skill needs:{RESET}")
        for sk, lvl in skill_needs.items():
            print(f"    {sk}: {ORANGE}{lvl}{RESET}")
    if not needs:
        print(f"  {GREEN}Roster looks balanced.{RESET}")
    if exp:
        print(f"\n  {YELLOW}Contracts expiring:{RESET}")
        for p in exp:
            print(f"    {p['name']}  ({p.get('contract_years', 0)} yr left, "
                  f"${p.get('salary', '?')}M)")
    block = league.trade_block.get(team, [])
    if block:
        print(f"\n  {BOLD}On the trade block:{RESET} {', '.join(block)}")
    print()


def show_h2h(t1: str, t2: str):
    w1, w2 = league.get_h2h(t1, t2)
    rk = league.h2h_key(t1, t2)
    riv = league.rivalries.get(rk, 0)
    print(f"\n  {BOLD}Head-to-Head:{RESET} {color_team_name(t1)} {w1}–{w2} {color_team_name(t2)}")
    if riv >= 40:
        print(f"  {RED}🔥 Rivalry intensity: {riv}/100{RESET}")


def show_franchise_records(team: str, franchise_history: Dict):
    fr = league.franchise_team_records.get(team, {})
    rings = franchise_history.get("team_rings", {}).get(team, 0)
    banners = "🏆" * min(rings, 10) if rings else "None"
    print(f"\n  {BOLD}Franchise — {color_team_name(team)}{RESET}")
    print(f"  Championship banners: {YELLOW}{banners}{RESET} ({rings})")
    print(f"  Single-game scoring record: {fr.get('most_pts_game', 0)} pts")
    retired = league.jersey_retired.get(team, [])
    if retired:
        print(f"  Retired jerseys: {', '.join(retired)}")


def mvp_race_with_pct(gm_season_stats: Dict, gm_records: Dict,
                      player_team_fn) -> List[Tuple[str, float]]:
    qualified = [n for n, s in gm_season_stats.items() if s.get("GP", 0) >= 15]
    if not qualified:
        return []

    def score(n):
        s = gm_season_stats[n]
        gp = max(1, s["GP"])
        w = gm_records.get(player_team_fn(n), {"W": 0}).get("W", 0)
        return s["PTS"] / gp * 1.2 + s["AST"] / gp * 0.7 + s["REB"] / gp * 0.4 + w * 0.04

    scores = {n: score(n) for n in qualified}
    total = sum(scores.values()) or 1
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    return [(n, s / total * 100) for n, s in ranked]


def show_mvp_with_pct(gm_season_stats, gm_records, player_team_fn, gm_season):
    ranked = mvp_race_with_pct(gm_season_stats, gm_records, player_team_fn)
    if not ranked:
        print(f"  {DIM}No stats yet.{RESET}")
        return
    print(f"\n{'═'*58}\n{BOLD}{YELLOW}  🏅 MVP RACE — Season {gm_season}{RESET}\n{'═'*58}")
    for i, (n, pct) in enumerate(ranked, 1):
        t = player_team_fn(n)
        bar = "█" * int(pct / 3)
        print(f"  {i:>2}. {BOLD}{n:<24}{RESET} {color_team_abbr(t)}  "
              f"{CYAN}{pct:.1f}%{RESET}  {DIM}{bar}{RESET}")


def show_rookie_watch(active_rosters, gm_season_stats, gm_season):
    rookies = []
    for tm, pls in active_rosters.items():
        for p in pls:
            if p.get("age", 99) <= 23 and p["name"] in gm_season_stats:
                s = gm_season_stats[p["name"]]
                gp = max(1, s.get("GP", 1))
                if gp >= 8:
                    score = s["PTS"] / gp * 1.2 + s["AST"] / gp * 0.5 + s["REB"] / gp * 0.4
                    rookies.append((p["name"], tm, score, s, gp))
    if not rookies:
        print(f"  {DIM}No rookie stats yet.{RESET}")
        return
    rookies.sort(key=lambda x: x[2], reverse=True)
    total = sum(r[2] for r in rookies) or 1
    print(f"\n{'═'*58}\n{BOLD}{GREEN}  🌟 ROOKIE WATCH — Season {gm_season}{RESET}\n{'═'*58}")
    for i, (n, t, sc, s, gp) in enumerate(rookies[:10], 1):
        pct = sc / total * 100
        print(f"  {i:>2}. {BOLD}{n:<24}{RESET} {color_team_abbr(t)}  "
              f"{CYAN}{s['PTS']/gp:.1f}ppg{RESET}  {YELLOW}{pct:.1f}% ROY{RESET}")


def save_weekly_rankings(gm_records: Dict, gm_season: int, week: int):
    teams = list(gm_records.keys())

    def pr_score(t):
        r = gm_records.get(t, {"W": 0, "L": 0, "PF": 0, "PA": 0})
        gp = max(1, r["W"] + r["L"])
        return r["W"] / gp * 60 + (r.get("PF", 0) - r.get("PA", 0)) / gp * 0.5

    ranked = sorted(teams, key=pr_score, reverse=True)
    league.weekly_rankings.append({
        "season": gm_season, "week": week, "rankings": ranked[:10],
    })
