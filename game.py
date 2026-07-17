from colors import color_team_name, color_team_abbr, team_abbr, teams as color_teams
from teams import team as team_meta
from players import rosters as base_rosters
from coaches import coaches as coach_data
import random, copy, math

# Import new financial system
from salary_cap import salary_config, calculator, multi_year_tracker, format_currency
from contracts import contract_manager, contract_generator, contract_extension, contract_validator
from luxury_tax import luxury_tax_calculator, apron_restrictions, apron_alerts, financial_display
from free_agency import FreeAgencyManager, ExceptionTracker, BirdRights, RestrictedFreeAgency
from trades import TradeValidator, TradeExecutor, TradeDisplay, AITradeLogic
from financial_reports import FinancialDashboard, FinancialAlerts
from ai_financial import AIFinancialManager, AIOffseasonStrategy, FinancialPersonality
from gameplay_enhancements import gameplay_manager
from league_features import (
    league, get_team_style_mods, crowd_intensity, home_court_boost,
    fatigue_penalty, veteran_leadership_bonus, rookie_minutes_bonus,
    breakout_boost, chemistry_boost, show_pregame, try_buzzer_beater,
    player_of_game, show_league_hub, show_team_needs_page, show_h2h,
    show_franchise_records, show_mvp_with_pct, show_rookie_watch,
    save_weekly_rankings, update_ai_trade_blocks, retire_jersey_if_legend,
    calc_attendance,
)

RESET   = "\033[0m"
GREEN   = "\033[38;2;0;200;80m"
RED     = "\033[38;2;220;50;50m"
YELLOW  = "\033[38;2;255;210;0m"
CYAN    = "\033[38;2;0;210;230m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
MAGENTA = "\033[38;2;210;0;210m"
ORANGE  = "\033[38;2;255;140;0m"
WHITE   = "\033[38;2;240;240;240m"
LBLUE   = "\033[38;2;80;160;255m"
BRED    = "\033[41m"      # red background for career/serious

# ══════════════════════════════════════════
# CONFERENCES
# ══════════════════════════════════════════
EAST = {
    "Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets",
    "Chicago Bulls","Cleveland Cavaliers","Detroit Pistons","Indiana Pacers",
    "Miami Heat","Milwaukee Bucks","New York Knicks","Orlando Magic",
    "Philadelphia 76ers","Toronto Raptors","Washington Wizards"
}
WEST = {
    "Dallas Mavericks","Denver Nuggets","Golden State Warriors","Houston Rockets",
    "Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies",
    "Minnesota Timberwolves","New Orleans Pelicans","Oklahoma City Thunder",
    "Phoenix Suns","Portland Trail Blazers","Sacramento Kings",
    "San Antonio Spurs","Utah Jazz"
}

FIRST_NAMES = ["Jaylen","Marcus","Tyler","Darius","Cam","Tre","Jalen","Kobe",
               "Isaiah","Jordan","Malik","Devin","Cade","Scottie","Evan",
               "Jabari","Markel","D'Andre","Keyante","RJ","Jaren","Paolo",
               "Amen","Scoot","Victor","Cooper","Bronny","Zach","Miles","Nick",
               "Quentin","Brayden","Tari","Jaxson","Killian","Trayce","Ochai"]
LAST_NAMES  = ["Smith","Johnson","Williams","Brown","Davis","Miller","Wilson",
               "Moore","Taylor","Anderson","Thomas","Jackson","White","Harris",
               "Martin","Garcia","Lee","Walker","Hall","Young","King","Scott",
               "Green","Adams","Baker","Carter","Mitchell","Perez","Campbell","Evans",
               "Murray","Butler","Henderson","Bridges","Powell","Love","Reed"]
POSITIONS   = ["PG","SG","SF","PF","C"]

# ══════════════════════════════════════════
# INJURY SYSTEM
# ══════════════════════════════════════════
# Each entry: name, severity, roll_weight (higher = more common),
#             games_out range, stat penalties, color
INJURY_CATALOG = [
    # ── Minor (very common, small penalties) ──
    {"name": "Cut",            "sev": "minor",   "weight": 120,
     "games": (0, 0),  "pen": {"shooting": -4},
     "col": YELLOW,    "msg": "🩹 {n} has a cut on their hand — shooting affected."},
    {"name": "Bruised Hand",   "sev": "minor",   "weight": 100,
     "games": (1, 3),  "pen": {"shooting": -6, "playmaking": -4},
     "col": YELLOW,    "msg": "🩹 {n} has a bruised hand — out {g} game(s)."},
    {"name": "Eye Irritation", "sev": "minor",   "weight": 80,
     "games": (1, 2),  "pen": {"shooting": -7},
     "col": YELLOW,    "msg": "🩹 {n} dealing with eye irritation — out {g} game(s)."},
    {"name": "Bruised Knee",   "sev": "minor",   "weight": 90,
     "games": (1, 4),  "pen": {"offense": -5, "defense": -3},
     "col": YELLOW,    "msg": "🩹 {n} bruised their knee — out {g} game(s)."},
    # ── Mild (moderate, week-scale) ──
    {"name": "Ankle Sprain",   "sev": "mild",    "weight": 40,
     "games": (5, 12), "pen": {"offense": -10, "shooting": -8, "overall": -5},
     "col": ORANGE,    "msg": "⚠️  {n} SPRAINS their ankle — out {g} games."},
    {"name": "Hip Flexor",     "sev": "mild",    "weight": 30,
     "games": (6, 14), "pen": {"offense": -12, "overall": -6},
     "col": ORANGE,    "msg": "⚠️  {n} strains their hip flexor — out {g} games."},
    {"name": "Hamstring Strain","sev": "mild",   "weight": 35,
     "games": (7, 16), "pen": {"offense": -10, "defense": -8, "overall": -7},
     "col": ORANGE,    "msg": "⚠️  {n} pulls their hamstring — out {g} games."},
    {"name": "Shoulder Sprain","sev": "mild",    "weight": 25,
     "games": (8, 15), "pen": {"shooting": -15, "playmaking": -10, "overall": -5},
     "col": ORANGE,    "msg": "⚠️  {n} sprains their shoulder — out {g} games."},
    # ── Serious (rare, month-scale) ──
    {"name": "Broken Finger",  "sev": "serious", "weight": 8,
     "games": (18, 28),"pen": {"shooting": -22, "playmaking": -18, "overall": -12},
     "col": RED,       "msg": f"{RED}🚨 {{n}} BREAKS A FINGER — out {{g}} games!{RESET}"},
    {"name": "Broken Hand",    "sev": "serious", "weight": 5,
     "games": (22, 35),"pen": {"shooting": -25, "playmaking": -20, "overall": -15},
     "col": RED,       "msg": f"{RED}🚨 {{n}} BREAKS THEIR HAND — out {{g}} games!{RESET}"},
    {"name": "Stress Fracture","sev": "serious", "weight": 4,
     "games": (25, 40),"pen": {"offense": -18, "defense": -15, "overall": -18},
     "col": RED,       "msg": f"{RED}🚨 {{n}} has a STRESS FRACTURE — out {{g}} games!{RESET}"},
    # ── Severe (very rare, season-ending) ──
    {"name": "Torn ACL",       "sev": "severe",  "weight": 2,
     "games": (60, 82),"pen": {"overall": -30},
     "col": RED,       "msg": f"{BRED}{BOLD}🚑 {{n}} TEARS THEIR ACL — OUT FOR THE SEASON!{RESET}"},
    {"name": "Torn Achilles",  "sev": "severe",  "weight": 2,
     "games": (60, 82),"pen": {"overall": -28},
     "col": RED,       "msg": f"{BRED}{BOLD}🚑 {{n}} TEARS THEIR ACHILLES — OUT FOR THE SEASON!{RESET}"},
    # ── Career-ending (extremely rare) ──
    {"name": "Career-Ending Injury", "sev": "career", "weight": 1,
     "games": (9999, 9999), "pen": {},
     "col": RED,
     "msg": f"{BRED}{BOLD}💀 {{n}} suffers a CAREER-ENDING INJURY. Their playing days are over.{RESET}"},
]

# Build weighted pool for random selection
_INJ_POOL = []
for inj in INJURY_CATALOG:
    _INJ_POOL.extend([inj] * inj["weight"])

def roll_injury():
    """Return a random injury from the catalog."""
    return random.choice(_INJ_POOL)

def apply_injury_to_player(player, inj):
    """Mark a player with an active injury. Returns display message."""
    g = random.randint(*inj["games"]) if inj["games"][1] > 0 else 0
    player["active_injury"] = {
        "name":     inj["name"],
        "sev":      inj["sev"],
        "games_left": g,
        "pen":      inj["pen"].copy(),
        "retired":  inj["sev"] == "career",
    }
    msg = inj["msg"].format(n=player["name"], g=g)
    return msg, g

def get_effective_stats(player):
    """Return player stats with injury and morale/confidence penalties applied."""
    stats = {k: player.get(k, 75)
             for k in ["overall","offense","defense","shooting","playmaking","rebounding"]}
    # Injury penalties
    inj = player.get("active_injury")
    if inj:
        for stat, penalty in inj["pen"].items():
            if stat in stats:
                stats[stat] = max(40, stats[stat] + penalty)
    # Morale/confidence effect — small, max ±4 points on any stat
    m = player.get("morale",     75)
    c = player.get("confidence", 75)
    mood = ((m - 75) * 0.03 + (c - 75) * 0.05)  # range roughly -4..+4
    for stat in ["offense", "shooting", "playmaking"]:
        stats[stat] = max(40, min(99, int(stats[stat] + mood)))
    return stats

def tick_injuries(active_rosters):
    """After each game: decrement injury counters, clear healed injuries."""
    healed = []
    for team, players in active_rosters.items():
        for p in players:
            inj = p.get("active_injury")
            if not inj: continue
            if inj["retired"]: continue
            if inj["games_left"] > 0:
                inj["games_left"] -= 1
            if inj["games_left"] == 0:
                p.pop("active_injury", None)
                healed.append(p["name"])
    return healed

def player_trade_value(player):
    """
    Exponential trade value based on OVR so stars are MUCH harder to get.
    OVR 99 = ~1560,  OVR 90 = ~900,  OVR 80 = ~400,  OVR 70 = ~150
    """
    ovr = max(60, min(99, player.get("overall", 75)))
    # Discount injured players
    inj = player.get("active_injury")
    if inj:
        sev = inj["sev"]
        if sev == "career": return 0
        if sev == "severe": ovr = max(60, ovr - 25)
        elif sev == "serious": ovr = max(60, ovr - 12)
        elif sev == "mild":   ovr = max(60, ovr - 6)
    return round((ovr - 60) ** 1.8)

def trade_value_str(val):
    if val >= 800:  return f"{GREEN}{BOLD}{val:>5}{RESET}"
    if val >= 400:  return f"{CYAN}{val:>5}{RESET}"
    if val >= 150:  return f"{WHITE}{val:>5}{RESET}"
    return f"{DIM}{val:>5}{RESET}"

# ══════════════════════════════════════════
# PHYSICAL ATTRIBUTES ENGINE
# ══════════════════════════════════════════
def parse_height(h_str):
    """Convert "6'8" string → total inches (80). Default 78 (≈ 6'6")."""
    try:
        h_str = str(h_str).replace('"', '').strip()
        ft, inch = h_str.split("'")
        return int(ft) * 12 + int(inch)
    except Exception:
        return 78

def physical_bonuses(player):
    """
    Return a dict of bonuses/penalties from height + weight.
    Height:  avg NBA player ≈ 79" (6'7").  Weight: avg ≈ 215 lbs.
    Driving/quickness favors shorter, lighter guards.
    Posting/finishing-through-contact favors taller, heavier bigs.
    Rebounding & shot-blocking also favor height + weight.
    """
    h  = parse_height(player.get("height", "6'6"))
    w  = player.get("weight", 210)

    h_diff = h - 79          # positive = taller than avg
    w_diff = w - 215         # positive = heavier than avg

    # Drive: shorter + lighter is better in the open court/off the dribble
    drive  = round(-h_diff * 0.55 - w_diff * 0.04)   # guard bonus: positive

    # Post: taller + heavier wins in the paint
    post   = round( h_diff * 0.70 + w_diff * 0.06)   # big bonus: positive

    # Rebounding: height + weight both help
    reb    = round( h_diff * 0.60 + w_diff * 0.03)

    # Shot-blocking: wingspan ≈ height proxy; taller = better
    block  = round( h_diff * 0.80)

    # Clamp to reasonable range
    return {
        "drive":  max(-15, min(15, drive)),
        "post":   max(-15, min(15, post)),
        "reb":    max(-12, min(12, reb)),
        "block":  max(-12, min(12, block)),
    }

def phys_label(player):
    """Return a short human-readable physical note for roster/quick-play display."""
    h = parse_height(player.get("height","6'6"))
    w = player.get("weight", 210)
    parts = []
    if h >= 84:   parts.append(f"{GREEN}Elite Length{RESET}")
    elif h >= 81: parts.append(f"{CYAN}Long{RESET}")
    elif h <= 73: parts.append(f"{YELLOW}Quick{RESET}")
    if w >= 240:  parts.append(f"{GREEN}Powerful{RESET}")
    elif w >= 225:parts.append(f"{CYAN}Strong{RESET}")
    elif w <= 185:parts.append(f"{YELLOW}Agile{RESET}")
    return ", ".join(parts) if parts else f"{DIM}Average build{RESET}"

# ══════════════════════════════════════════
# PLAYER ARCHETYPE ENGINE
# ══════════════════════════════════════════
def get_archetype(player):
    """
    Infer a play-style archetype from a player's stats and size.
    Returns (label, bonuses_dict) where bonuses affect simulation probabilities.
    """
    sht = player.get("shooting",  75)
    off = player.get("offense",   75)
    dfn = player.get("defense",   75)
    pmk = player.get("playmaking",75)
    reb = player.get("rebounding",75)
    h   = parse_height(player.get("height","6'6"))
    w   = player.get("weight", 210)

    if h >= 82 and dfn >= 82:
        return "Rim Protector",    {"block":+0.06, "reb":+0.04, "three":-0.04}
    if h >= 80 and sht >= 80 and off >= 78:
        return "Stretch Big",      {"three":+0.05, "two":+0.03, "drive":-0.03}
    if dfn >= 82 and sht >= 76 and h >= 76:
        return "3&D Wing",         {"three":+0.04, "def_boost":+3}
    if dfn >= 84:
        return "Lockdown Defender",{"def_boost":+5, "steal":+0.04}
    if pmk >= 83 and off >= 80:
        return "Floor General",    {"ast":+0.10, "three":+0.03, "drive":+0.02}
    if sht >= 85:
        return "Shot Creator",     {"three":+0.06, "two":+0.02}
    if off >= 84 and h <= 78:
        return "Slasher",          {"drive":+0.06, "ft":+0.04, "three":-0.04}
    if off >= 82 and reb >= 80:
        return "Offensive Engine", {"two":+0.05, "post":+0.04}
    return "Two-Way Player",       {}

# ══════════════════════════════════════════
# MORALE & CONFIDENCE SYSTEM
# ══════════════════════════════════════════
def init_player_meta(active_rosters):
    """
    Stamp every player with morale, confidence, clutch, and archetype
    if they don't already have them. Safe to call multiple times.
    """
    for team, players in active_rosters.items():
        for p in players:
            if "morale"     not in p: p["morale"]     = random.randint(65, 85)
            if "confidence" not in p: p["confidence"] = random.randint(60, 85)
            if "clutch"     not in p:
                ovr = p.get("overall", 75)
                # Better players tend to be more clutch, but with variance
                p["clutch"] = max(40, min(99, ovr + random.randint(-20, 20)))
            if "archetype"  not in p:
                p["archetype"], _ = get_archetype(p)

def morale_effect(player):
    """
    Returns a small float bonus/penalty to shooting/offense from morale+confidence.
    Capped at ±0.05 so it never overpowers ratings.
    """
    m = player.get("morale",     75)
    c = player.get("confidence", 75)
    combined = ((m - 75) + (c - 75) * 1.5) / 1000   # max ±0.075, effectively ±0.05
    return max(-0.05, min(0.05, combined))

def update_morale_postgame(active_rosters, result, game_stats, gm_team_name=None):
    """
    Update morale and confidence for all players after a game.
    Called from _play_82 after every game.
    Returns list of notable morale events to display.
    """
    winner = result["winner"]
    loser  = result["loser"]
    events = []

    for team, players in active_rosters.items():
        won = (team == winner)
        for p in players:
            n   = p["name"]
            s   = game_stats.get(n, {})
            pts = s.get("PTS", 0)
            gp  = s.get("GP",  0)   # not in per-game stats, so 0 ok
            old_m = p.get("morale",     75)
            old_c = p.get("confidence", 75)

            # ── Win/loss morale swing ──
            if won:
                p["morale"] = min(100, old_m + random.randint(1, 4))
            else:
                p["morale"] = max(10,  old_m - random.randint(1, 3))

            # ── Performance confidence swing ──
            if pts >= 30:
                p["confidence"] = min(100, old_c + random.randint(6, 12))
                if team == gm_team_name and random.random() < 0.6:
                    events.append(f"🔥 {n} is LOCKED IN after a {pts}-point game!")
            elif pts >= 20:
                p["confidence"] = min(100, old_c + random.randint(3, 6))
            elif pts <= 4 and s:
                p["confidence"] = max(10,  old_c - random.randint(4, 8))
                if team == gm_team_name and random.random() < 0.3:
                    events.append(f"😔 {n} is struggling — confidence dropping after {pts} pts.")
            else:
                # small natural drift toward 75
                p["confidence"] += (75 - p["confidence"]) // 8

            # ── Playing time morale ──
            mins = s.get("mins_used", 0)  # not tracked per-game, skip silently

    return events

# ── Module-level game context (set each game, read by simulate_possession) ──
_gctx: dict = {
    "quarter":      1,
    "t1":           "",
    "t2":           "",
    "score":        {},
    "hot":          set(),    # player names on a HOT streak this game
    "cold":         set(),    # player names on a COLD streak this game
    "shot_hist":    {},       # name → deque of last 4 True/False
    "momentum":     {},       # team → consecutive pts without opponent scoring
    "run_start":    {},       # team → score when run started
    "last_team":    None,     # last team to score
    "verbose":      False,
}

def _gctx_reset(t1, t2, verbose):
    _gctx.update({
        "quarter": 1, "t1": t1, "t2": t2,
        "score": {t1: 0, t2: 0},
        "hot": set(), "cold": set(), "shot_hist": {},
        "momentum": {t1: 0, t2: 0},
        "run_start": {t1: 0, t2: 0},
        "last_team": None, "verbose": verbose,
        "poss_in_q": 0, "poss_total_q": POSSESSIONS_PER_QUARTER,
        "style_mods": {t1: get_team_style_mods(t1), t2: get_team_style_mods(t2)},
        "active_rosters": None,
    })

def _update_shot_hist(name, made):
    """Track last 4 shots per player; update HOT/COLD status."""
    from collections import deque
    hist = _gctx["shot_hist"].setdefault(name, deque(maxlen=4))
    hist.append(made)
    if len(hist) < 3: return None
    streak = list(hist)[-3:]
    if all(streak):
        was_hot = name in _gctx["hot"]
        _gctx["hot"].discard(name); _gctx["cold"].discard(name)
        _gctx["hot"].add(name)
        return "hot" if not was_hot else None
    if not any(streak):
        was_cold = name in _gctx["cold"]
        _gctx["hot"].discard(name); _gctx["cold"].discard(name)
        _gctx["cold"].add(name)
        return "cold" if not was_cold else None
    # Broke streak
    _gctx["hot"].discard(name); _gctx["cold"].discard(name)
    return None

def _update_momentum(scoring_team, pts, other_team, verbose):
    """Track scoring runs; print 'X-0 run' when a team goes on a 8+ point run."""
    if pts == 0: return
    if _gctx["last_team"] != scoring_team:
        # Opponent scored last — reset this team's run
        _gctx["momentum"][scoring_team] = 0
        _gctx["run_start"][scoring_team] = _gctx["score"].get(scoring_team, 0)
    _gctx["momentum"][scoring_team] += pts
    _gctx["last_team"] = scoring_team
    run = _gctx["momentum"][scoring_team]
    opp_run = _gctx["momentum"].get(other_team, 0)
    thresholds = [8, 10, 12, 15, 18, 20]
    if run in thresholds and verbose:
        print(f"\n  {YELLOW}{BOLD}  📣 {run}-0 RUN by {color_team_abbr(scoring_team)}!{RESET}\n")

# ══════════════════════════════════════════
# SEASON / GM STATE
# ══════════════════════════════════════════
gm_active       = False
gm_team         = None
gm_season       = 1
gm_records      = {}
gm_season_stats = {}
gm_history      = []   # legacy simple list kept for compat

# ── Franchise History (persists forever) ──
franchise_history = {
    "champions":        [],   # [{season, team, score, finals_mvp}]
    "award_history":    [],   # [{season, award, name, team}]
    "retired_players":  [],   # [{name, age, team, ovr, seasons}]
    "team_rings":       {},   # {team: int}
    "career_stats":     {},   # {name: {PTS,REB,AST,STL,BLK,GP,seasons}}
    "career_pts_ldr":   [],   # sorted at display time
}

# ── Salary Cap ──
# Old constants kept for backward compatibility, now using new financial system
SALARY_CAP  = salary_config.soft_cap   # millions — NBA soft cap
LUXURY_TAX  = salary_config.luxury_tax # luxury tax threshold

# ── Draft Picks ──
team_picks = {}

def init_picks(all_teams, start_season, future_seasons=4):
    global team_picks
    team_picks = {t: [] for t in all_teams}
    for t in all_teams:
        for yr in range(start_season, start_season + future_seasons):
            team_picks[t].append({"year": yr, "round": 1, "original": t})
            team_picks[t].append({"year": yr, "round": 2, "original": t})

def picks_label(pk):
    r = "1st" if pk["round"] == 1 else "2nd"
    return f"{pk['year']} {r} (orig: {team_abbr(pk['original'])})"

def get_team_picks(team, year=None):
    picks = team_picks.get(team, [])
    if year: picks = [p for p in picks if p["year"] == year]
    return sorted(picks, key=lambda p: (p["year"], p["round"]))

def transfer_pick(pk, from_t, to_t):
    if pk in team_picks.get(from_t, []):
        team_picks[from_t].remove(pk)
        team_picks.setdefault(to_t, []).append(pk)

def advance_picks_year():
    global team_picks
    new_yr = gm_season + 3
    for t in team_picks:
        team_picks[t] = [p for p in team_picks[t] if p["year"] >= gm_season]
        if not any(p["year"] == new_yr for p in team_picks[t]):
            team_picks[t].append({"year": new_yr, "round": 1, "original": t})
            team_picks[t].append({"year": new_yr, "round": 2, "original": t})

# ── Records ──
def reset_season_records(team_list):
    global gm_records
    gm_records = {t: {"W":0,"L":0,"PF":0,"PA":0} for t in team_list}

def reset_season_stats():
    global gm_season_stats
    gm_season_stats = {}

def record_result(winner, loser, wp, lp):
    if winner in gm_records:
        gm_records[winner]["W"]  += 1; gm_records[winner]["PF"] += wp; gm_records[winner]["PA"] += lp
    if loser  in gm_records:
        gm_records[loser]["L"]   += 1; gm_records[loser]["PF"]  += lp; gm_records[loser]["PA"]  += wp

def add_to_season_stats(gs):
    for player, s in gs.items():
        if player not in gm_season_stats:
            gm_season_stats[player] = {"PTS":0,"REB":0,"AST":0,"STL":0,"BLK":0,"GP":0}
        for k in ["PTS","REB","AST","STL","BLK"]: gm_season_stats[player][k] += s[k]
        gm_season_stats[player]["GP"] += 1

# ══════════════════════════════════════════
# SCHEDULE GENERATOR
# ══════════════════════════════════════════
def generate_schedule(all_teams, target=82):
    teams   = all_teams[:]
    if len(teams) % 2 == 1: teams.append(None)
    n       = len(teams)
    half    = n // 2
    play    = {t: 0 for t in all_teams}
    sched   = []
    flip    = False
    while min(play.values()) < target:
        arr    = teams[:]
        rounds = []
        for _ in range(n - 1):
            rg = []
            for i in range(half):
                a, b = arr[i], arr[n-1-i]
                if a and b:
                    rg.append((b,a) if flip else (a,b))
            rounds.append(rg)
            arr = [arr[0]] + [arr[-1]] + arr[1:-1]
        flip = not flip
        random.shuffle(rounds)
        for rg in rounds:
            for t1,t2 in rg:
                if play[t1] < target and play[t2] < target:
                    sched.append((t1,t2)); play[t1]+=1; play[t2]+=1
            if all(v>=target for v in play.values()): break
        if all(v>=target for v in play.values()): break
    return sched

# ══════════════════════════════════════════
# DRAFT / PROSPECTS
# ══════════════════════════════════════════
def generate_prospect():
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    pos  = random.choice(POSITIONS)
    age  = random.randint(18, 22)
    t    = random.random()
    if   t < 0.05:  ovr = random.randint(82, 89)
    elif t < 0.20:  ovr = random.randint(74, 81)
    elif t < 0.55:  ovr = random.randint(67, 73)
    else:           ovr = random.randint(60, 66)
    def s(): return max(55, min(95, ovr + random.randint(-10,10)))
    return {"name":name,"pos":pos,"age":age,"overall":ovr,
            "offense":s(),"defense":s(),"shooting":s(),
            "playmaking":s(),"rebounding":s(),"injury_risk":random.randint(5,30)}

def run_draft(active_rosters, gm_team_name=None, rounds=2):
    print(f"\n{'═'*58}\n{BOLD}{YELLOW}  🎓 NBA DRAFT  —  Season {gm_season}{RESET}\n{'═'*58}")
    all_teams = list(active_rosters.keys())
    if gm_records:
        order = sorted(all_teams, key=lambda t:(gm_records.get(t,{"W":0})["W"],
                                                gm_records.get(t,{"PF":0})["PF"]))
    else:
        order = all_teams[:]; random.shuffle(order)
    pool = sorted([generate_prospect() for _ in range(len(all_teams)*rounds+20)],
                  key=lambda p: p["overall"], reverse=True)
    for rnd in range(1, rounds+1):
        print(f"\n  {BOLD}{CYAN}── Round {rnd} ──{RESET}")
        for pick_num, orig in enumerate(order, 1):
            if not pool: break
            owner = orig
            for t, pks in team_picks.items():
                for pk in pks:
                    if pk["year"]==gm_season and pk["round"]==rnd and pk["original"]==orig:
                        owner = t; break
            overall_pick = (rnd-1)*len(all_teams) + pick_num
            via = f" {DIM}(via {color_team_abbr(orig)}){RESET}" if owner!=orig else ""
            if owner == gm_team_name:
                print(f"\n  {YELLOW}{'★'*48}{RESET}")
                print(f"  {YELLOW}🏀 YOUR PICK — #{overall_pick}{via}{RESET}\n")
                cnt = min(12, len(pool))
                print(f"  {'#':>3}  {'PLAYER':<24} POS  OVR  AGE  SHT")
                print(f"  {'─'*50}")
                for i, p in enumerate(pool[:cnt], 1):
                    c = (GREEN if p["overall"]>=82 else ORANGE if p["overall"]>=74 else WHITE)
                    print(f"  {i:>3}. {c}{p['name']:<24}{RESET} {p['pos']:>3}  "
                          f"{p['overall']:>3}  {p['age']:>3}  {p['shooting']:>3}")
                while True:
                    c = input(f"\n  Pick 1-{cnt}: ").strip()
                    if c.isdigit() and 1<=int(c)<=cnt:
                        chosen = pool.pop(int(c)-1); break
                    print(RED+"  Invalid."+RESET)
                active_rosters[owner].append(chosen)
                print(GREEN+f"\n  ✅ {color_team_name(owner)} drafts {BOLD}{chosen['name']}{RESET}"
                      +GREEN+f" ({chosen['pos']}, OVR {chosen['overall']}){RESET}")
                print(f"  {YELLOW}{'★'*48}{RESET}")
            else:
                best = max(pool[:min(20,len(pool))], key=lambda p: p["overall"])
                pool.remove(best)
                active_rosters[owner].append(best)
                tier = (f"{GREEN}★{RESET}" if best["overall"]>=82 else
                        f"{ORANGE}◆{RESET}" if best["overall"]>=74 else " ")
                print(f"  #{overall_pick:>3}  {color_team_abbr(owner):<6} {tier} "
                      f"{best['name']:<24} OVR:{best['overall']:>3}  {best['pos']}{via}")
        for t in team_picks:
            team_picks[t] = [p for p in team_picks[t]
                             if not (p["year"]==gm_season and p["round"]==rnd)]
    print(f"\n  {GREEN}Draft complete!{RESET}")

# ══════════════════════════════════════════
# PLAYER PROGRESSION
# ══════════════════════════════════════════
def progress_players(active_rosters):
    print(f"\n{BOLD}{CYAN}  📈 PLAYER PROGRESSION{RESET}\n  {'─'*45}")
    bk, dk = [], []
    retired = []
    for team, players in active_rosters.items():
        to_remove = []
        for p in players:
            inj = p.get("active_injury")
            if inj and inj.get("retired"):
                retired.append((p["name"], team))
                to_remove.append(p)
                continue
            age = p.get("age", 25); p["age"] = age + 1
            if   age<=21: d=random.randint(2,5)
            elif age<=24: d=random.randint(1,3)
            elif age<=27: d=random.randint(-1,2)
            elif age<=30: d=random.randint(-2,1)
            elif age<=33: d=random.randint(-3,0)
            else:         d=random.randint(-4,-1)
            old = p.get("overall",75)
            for stat in ["overall","offense","defense","shooting","playmaking","rebounding"]:
                if stat in p: p[stat] = max(60, min(99, p[stat]+d))
            new = p.get("overall",75)
            if new-old>=4: bk.append((p["name"],team,old,new))
            elif old-new>=3: dk.append((p["name"],team,old,new))
        for p in to_remove: players.remove(p)
    if retired:
        print(f"\n  {RED}{BOLD}Retirements:{RESET}")
        for n,t in retired:
            print(f"  {RED}  🏁  {n} ({color_team_abbr(t)}) — career over{RESET}")
    if bk:
        print(f"\n  {GREEN}{BOLD}Breakouts:{RESET}")
        for n,t,o,nw in bk[:8]:
            print(f"  {GREEN}  ↑{RESET}  {n:<24} {color_team_abbr(t)}  {o}→{GREEN}{nw}{RESET}")
    if dk:
        print(f"\n  {RED}{BOLD}Declining:{RESET}")
        for n,t,o,nw in dk[:8]:
            print(f"  {RED}  ↓{RESET}  {n:<24} {color_team_abbr(t)}  {o}→{RED}{nw}{RESET}")

# ══════════════════════════════════════════
# CONTRACTS & SALARY CAP
# ══════════════════════════════════════════
def _salary_for(ovr, age):
    """Return a realistic salary (millions) for an OVR/age combo."""
    base = max(0.9, (ovr - 68) * 3.2 + 3)   # OVR70→~9M, OVR85→~58M
    age_disc = max(0, (age - 31) * 0.6)       # veterans get modest discount
    return round(max(0.9, min(55.0, base - age_disc)), 1)

def _assign_potential(p):
    """Return potential grade (A+/A/B+/B/C) based on OVR and age."""
    ovr = p.get("overall", 75); age = p.get("age", 27)
    if age <= 20:
        if ovr >= 84: return "A+"
        return random.choice(["A+","A","A","B+"])
    if age <= 22:
        if ovr >= 86: return "A+"
        if ovr >= 80: return "A"
        return random.choice(["B+","B+","B"])
    if age <= 25:
        if ovr >= 87: return "A"
        if ovr >= 82: return "B+"
        return "B"
    if age <= 29:
        return "B" if ovr >= 78 else "C"
    return "C"

def init_contracts(active_rosters):
    """
    Stamp players with contract_years, salary, and potential if missing.
    Called once at GM-mode start and again after each offseason.
    """
    for tm, pls in active_rosters.items():
        for p in pls:
            if "contract_years" not in p:
                p["contract_years"] = random.randint(1, 4)
            if "salary" not in p:
                p["salary"] = _salary_for(p.get("overall",75), p.get("age",27))
            if "potential" not in p:
                p["potential"] = _assign_potential(p)
    sync_contract_manager(active_rosters)

def sync_contract_manager(active_rosters, teams=None):
    """Keep contract_manager aligned with active rosters."""
    from contracts import Contract
    target_teams = teams if teams is not None else active_rosters.keys()
    for tm in target_teams:
        roster = active_rosters.get(tm, [])
        roster_names = {p["name"] for p in roster}
        for p in roster:
            sal = p.get("salary", _salary_for(p.get("overall", 75), p.get("age", 27)))
            yrs = p.get("contract_years", 1)
            existing = contract_manager.get_player_contract(tm, p["name"])
            if existing:
                existing.annual_salary = sal
                existing.years_remaining = yrs
                existing.total_value = sal * yrs
                continue
            for other_tm in list(contract_manager.contracts.keys()):
                if other_tm == tm:
                    continue
                if contract_manager.get_player_contract(other_tm, p["name"]):
                    contract_manager.remove_contract(other_tm, p["name"])
            contract_manager.add_contract(Contract(
                player_name=p["name"], team=tm,
                years_remaining=yrs, annual_salary=sal,
            ))
        for contract in list(contract_manager.get_team_contracts(tm)):
            if contract.player_name not in roster_names:
                contract_manager.remove_contract(tm, contract.player_name)

def get_payroll(active_rosters, team):
    """Return total payroll (millions) for a team."""
    roster_total = round(sum(p.get("salary", 5) for p in active_rosters.get(team, [])), 1)
    manager_total = contract_manager.get_team_payroll(team)
    if manager_total <= 0 and roster_total > 0:
        return roster_total
    return manager_total

def get_cap_space(active_rosters, team):
    """Return remaining cap space (may be negative = over cap)."""
    payroll = get_payroll(active_rosters, team)
    return calculator.calculate_cap_space(payroll)

def show_team_management(active_rosters, team):
    """Display salary cap, payroll, team ratings, and chemistry - using new financial system."""
    print(f"\n{BOLD}{LBLUE}{'╔'*60}{RESET}")
    print(f"{BOLD}{LBLUE}║{RESET}{BOLD}{WHITE}  📊 TEAM MANAGEMENT{RESET}{BOLD}{LBLUE}{' '*38}║{RESET}")
    print(f"{BOLD}{LBLUE}║{RESET}{BOLD}{CYAN}  {color_team_name(team)}{RESET}{BOLD}{LBLUE}{' '*38}║{RESET}")
    print(f"{BOLD}{LBLUE}{'╚'*60}{RESET}\n")
    
    pls     = sorted(active_rosters.get(team,[]), key=lambda x:x.get("salary",0), reverse=True)
    payroll = get_payroll(active_rosters, team)
    cap_sp  = get_cap_space(active_rosters, team)
    avg_ovr = round(sum(p.get("overall",75) for p in pls)/max(1,len(pls)), 1)
    avg_off = round(sum(p.get("offense",75)  for p in pls)/max(1,len(pls)), 1)
    avg_def = round(sum(p.get("defense",75)  for p in pls)/max(1,len(pls)), 1)
    avg_mor = round(sum(p.get("morale",75)   for p in pls)/max(1,len(pls)), 1)
    chemistry = round(avg_mor * 0.6 + (100 - abs(cap_sp)) * 0.1, 1)
    chemistry = max(0, min(100, chemistry))
    contention = round(avg_ovr * 0.5 + avg_off * 0.25 + avg_def * 0.25, 1)

    # Try to use new financial display system
    contracts = [contract_manager.get_player_contract(team, p['name'])
                 for p in pls if contract_manager.get_player_contract(team, p['name'])]
    contract_dicts = [c.to_dict() for c in contracts if c]
    if contract_dicts:
        financial_display.display_team_financial_summary(team, payroll, contract_dicts)
    else:
        cap_color  = RED if payroll > LUXURY_TAX else ORANGE if payroll > SALARY_CAP else GREEN
        print(f"\n{'═'*60}")
        print(f"{BOLD}{MAGENTA}  💼 TEAM MANAGEMENT — {color_team_name(team)}{RESET}")
        print(f"{'═'*60}")
        print(f"  {BOLD}Payroll:{RESET}  {cap_color}${payroll}M{RESET}"
              + (f"  {RED}⚠ LUXURY TAX +${round(payroll-LUXURY_TAX,1)}M{RESET}" if payroll>LUXURY_TAX else
                 f"  {ORANGE}(over cap by ${abs(cap_sp)}M)" if cap_sp<0 else
                 f"  {GREEN}(${cap_sp}M cap space){RESET}"))
        print(f"  {BOLD}Salary Cap:{RESET} ${SALARY_CAP}M   {BOLD}Luxury Tax:{RESET} ${LUXURY_TAX}M")
        print(f"\n  {BOLD}Team Ratings{RESET}")
        print(f"  Overall:   {WHITE}{avg_ovr}{RESET}   Off: {ORANGE}{avg_off}{RESET}"
              f"   Def: {CYAN}{avg_def}{RESET}")
        print(f"  Chemistry: {GREEN if chemistry>75 else ORANGE}{chemistry:.0f}/100{RESET}"
              f"   Contender Rating: {YELLOW}{contention:.0f}/100{RESET}")
        print(f"\n  {'PLAYER':<24} POS  OVR  SAL(M)  YRS  POT  STATUS")
        print(f"  {'─'*58}")
        for p in pls:
            pot_c = (GREEN if p.get("potential","C") in ("A+","A") else
                     ORANGE if p.get("potential","C") == "B+" else WHITE)
            yrs   = p.get("contract_years",1)
            yrs_c = RED if yrs==0 else YELLOW if yrs==1 else GREEN
            ai    = p.get("active_injury")
            st    = f"{RED}OUT{RESET}" if (ai and ai.get("games_left",0)>0) else f"{GREEN}✓{RESET}"
            print(f"  {p['name']:<24} {p.get('pos','?'):>3}  {p.get('overall',75):>3}"
                  f"  {YELLOW}${p.get('salary',5):<5}{RESET}"
                  f"  {yrs_c}{yrs}yr{RESET}  {pot_c}{p.get('potential','?'):>2}{RESET}  {st}")

# ══════════════════════════════════════════
# CAREER STATS ACCUMULATOR
# ══════════════════════════════════════════
def accumulate_career_stats(active_rosters):
    """
    After every season, fold gm_season_stats into franchise_history career_stats.
    Call this before resetting gm_season_stats.
    """
    cs = franchise_history["career_stats"]
    for name, s in gm_season_stats.items():
        if name not in cs:
            cs[name] = {"PTS":0,"REB":0,"AST":0,"STL":0,"BLK":0,"GP":0,"seasons":0}
        for stat in ("PTS","REB","AST","STL","BLK","GP"):
            cs[name][stat] += s.get(stat, 0)
        cs[name]["seasons"] += 1

# ══════════════════════════════════════════
# ENHANCED PLAYER PROGRESSION
# ══════════════════════════════════════════
def progress_players_full(active_rosters, season_num):
    """
    Full age-aware, potential-aware player development with retirements.
    Replaces the simpler progress_players() in offseason flow.
    Returns list of retired player dicts.
    """
    global franchise_history
    bk, dk, retired_out = [], [], []
    pot_mult = {"A+":1.5,"A":1.25,"B+":1.1,"B":1.0,"C":0.75}

    for team, players in active_rosters.items():
        to_remove = []
        for p in players:
            # ── Injury retirements ──
            inj = p.get("active_injury")
            if inj and inj.get("retired"):
                entry = {"name":p["name"],"age":p.get("age",30),"team":team,
                         "ovr":p.get("overall",70),"seasons":season_num}
                franchise_history["retired_players"].append(entry)
                retired_out.append(entry)
                to_remove.append(p); continue

            age = p.get("age", 25)
            p["age"] = age + 1

            # ── Natural retirement ──
            r_chance = (0.0 if age < 34 else 0.08 if age < 36 else
                        0.25 if age < 38 else 0.55 if age < 40 else 0.85)
            if age >= 34 and p.get("overall",75) < 73: r_chance += 0.15
            if random.random() < r_chance:
                entry = {"name":p["name"],"age":age+1,"team":team,
                         "ovr":p.get("overall",70),"seasons":season_num}
                franchise_history["retired_players"].append(entry)
                retired_out.append(entry)
                to_remove.append(p); continue

            # ── Progression / regression delta ──
            if   age <= 21: base_d = random.randint(2, 5)
            elif age <= 24: base_d = random.randint(1, 4)
            elif age <= 26: base_d = random.randint(0, 3)
            elif age <= 28: base_d = random.randint(-1, 2)
            elif age <= 30: base_d = random.randint(-2, 1)
            elif age <= 33: base_d = random.randint(-3, 0)
            else:           base_d = random.randint(-5, -1)

            # Award boost — winning awards accelerates growth
            award_bonus = sum(
                1 for a in franchise_history.get("award_history",[])
                if a["name"]==p["name"] and a["season"]==season_num
            )
            pm    = pot_mult.get(p.get("potential","B"), 1.0)
            delta = max(-6, min(6, round((base_d + award_bonus) * pm)))

            old = p.get("overall", 75)
            for stat in ["overall","offense","defense","shooting","playmaking","rebounding"]:
                if stat in p:
                    p[stat] = max(58, min(99, p[stat] + delta))
            new = p.get("overall", 75)

            # Tick contract down
            p["contract_years"] = max(0, p.get("contract_years",1) - 1)
            # Update salary to match new OVR (slight annual adjustment)
            p["salary"] = _salary_for(p.get("overall",75), p.get("age",27))
            # Refresh potential
            p["potential"] = _assign_potential(p)

            if new - old >= 4: bk.append((p["name"], team, old, new))
            elif old - new >= 3: dk.append((p["name"], team, old, new))

        for p in to_remove:
            players.remove(p)

    print(f"\n{BOLD}{CYAN}  📈 PLAYER DEVELOPMENT — Season {season_num}{RESET}\n  {'─'*48}")
    if retired_out:
        print(f"\n  {RED}{BOLD}Retirements:{RESET}")
        for e in retired_out:
            print(f"  {RED}🏁  {e['name']} (age {e['age']}, OVR {e['ovr']}) retires from {color_team_abbr(e['team'])}{RESET}")
    if bk:
        print(f"\n  {GREEN}{BOLD}Breakout Progressions:{RESET}")
        for n,t,o,nw in bk[:10]:
            print(f"  {GREEN}  ↑{RESET}  {n:<24} {color_team_abbr(t)}  {o} → {GREEN}{BOLD}{nw}{RESET}")
    if dk:
        print(f"\n  {RED}{BOLD}Declines:{RESET}")
        for n,t,o,nw in dk[:10]:
            print(f"  {RED}  ↓{RESET}  {n:<24} {color_team_abbr(t)}  {o} → {RED}{nw}{RESET}")
    return retired_out

# ══════════════════════════════════════════
# FREE AGENCY
# ══════════════════════════════════════════
def run_free_agency(active_rosters, all_teams, gm_team_name):
    """
    Full free agency flow:
      1. Build FA pool from players with contract_years == 0
      2. AI teams sign FAs to fill roster gaps
      3. User gets interactive signing menu for their team
    """
    print(f"\n{'═'*60}\n{BOLD}{GREEN}  🖊️  FREE AGENCY — Season {gm_season}{RESET}\n{'═'*60}")

    # ── Step 1: Collect FAs ──
    fa_pool = []
    for tm in all_teams:
        expired = [p for p in active_rosters.get(tm, []) if p.get("contract_years", 1) == 0]
        for p in expired:
            active_rosters[tm].remove(p)
            p["fa_prev_team"] = tm
            fa_pool.append(p)
    fa_pool.sort(key=lambda x: x.get("overall", 0), reverse=True)

    if not fa_pool:
        print(f"  {DIM}No free agents available.{RESET}")
        return

    print(f"  {len(fa_pool)} players entered free agency.")

    # ── Step 2: AI signings ──
    signed_by_ai = []
    for tm in all_teams:
        if tm == gm_team_name: continue
        roster = active_rosters.get(tm, [])
        target_size = 12
        for fa in fa_pool[:]:
            if len(roster) >= target_size: break
            cap = get_cap_space(active_rosters, tm)
            sal = fa.get("salary", 5)
            if cap < sal - 2: continue       # can't afford (allow minor overages)
            if random.random() < 0.70:       # 70% chance to sign any affordable FA
                yrs = random.randint(1, 3)
                fa["contract_years"] = yrs
                fa["salary"]         = _salary_for(fa.get("overall",75), fa.get("age",27))
                roster.append(fa)
                fa_pool.remove(fa)
                signed_by_ai.append((fa["name"], tm, fa["overall"]))

    if signed_by_ai:
        print(f"\n  {BOLD}AI Signings:{RESET}")
        for n, tm, ovr in signed_by_ai[:12]:
            print(f"  {DIM}  {n} ({ovr} OVR) → {color_team_abbr(tm)}{RESET}")
            if ovr >= 82:
                news_add("SIGNING",
                    f"{n} signs with {color_team_abbr(tm)}",
                    f"Free agent {n} (OVR {ovr}) agrees to join {tm} this offseason.")
        if len(signed_by_ai) > 12:
            print(f"  {DIM}  ... and {len(signed_by_ai)-12} more{RESET}")

    # ── Step 3: User signing menu ──
    gm_roster  = active_rosters.get(gm_team_name, [])
    gm_payroll = get_payroll(active_rosters, gm_team_name)
    remaining  = [fa for fa in fa_pool]   # FAs not yet signed

    print(f"\n  {BOLD}{YELLOW}YOUR TURN — {color_team_name(gm_team_name)}{RESET}"
          f"  Roster: {len(gm_roster)}/15  "
          f"Payroll: ${gm_payroll}M / ${SALARY_CAP}M")

    if not remaining:
        print(f"  {DIM}No free agents remaining.{RESET}")
        return

    while True:
        print(f"\n  {BOLD}Available Free Agents:{RESET}")
        page = remaining[:20]
        print(f"  {'#':>3}  {'PLAYER':<24} POS  OVR  SAL(M)  POT  AGE")
        print(f"  {'─'*55}")
        for i, fa in enumerate(page, 1):
            pot_c = GREEN if fa.get("potential","C") in ("A+","A") else ORANGE if fa.get("potential","C")=="B+" else WHITE
            print(f"  {i:>3}. {fa['name']:<24} {fa.get('pos','?'):>3}  {fa.get('overall',75):>3}"
                  f"  {YELLOW}${fa.get('salary',5):<5}{RESET}"
                  f"  {pot_c}{fa.get('potential','?'):>2}{RESET}  {fa.get('age','?')}")
        print(f"\n  {CYAN}[#]{RESET} Sign player  {CYAN}[s]{RESET} Skip to next season")
        ch = input("  > ").strip().lower()
        if ch == "s": break
        if ch.isdigit() and 1 <= int(ch) <= len(page):
            fa = page[int(ch)-1]
            cap = get_cap_space(active_rosters, gm_team_name)
            sal = fa.get("salary", 5)
            if cap < sal - 5:
                print(f"  {RED}Not enough cap space! (Need ${sal}M, have ${cap}M){RESET}")
                continue
            if len(gm_roster) >= 15:
                print(f"  {RED}Roster full (15 players max){RESET}")
                continue
            yrs_in = input(f"  Contract length (1-5 years): ").strip()
            try:
                yrs = int(yrs_in)
                if not 1 <= yrs <= 5:
                    raise ValueError
            except ValueError:
                print(f"  {RED}Invalid years — using 2-year default.{RESET}")
                yrs = 2
            fa["contract_years"] = yrs
            gm_roster.append(fa)
            remaining.remove(fa)
            gm_payroll = get_payroll(active_rosters, gm_team_name)
            print(f"  {GREEN}✅ Signed {fa['name']} ({fa.get('overall',75)} OVR) "
                  f"— ${sal}M / {yrs}yr{RESET}")
            print(f"  Payroll: ${gm_payroll}M / ${SALARY_CAP}M")
        else:
            print(f"  {RED}Invalid choice.{RESET}")

# ══════════════════════════════════════════
# FULL OFFSEASON ORCHESTRATOR
# ══════════════════════════════════════════
def _record_awards_history(active_rosters, champion, champion_score, loser_score):
    """
    Save season awards + champion into franchise_history.
    Called once at the end of the playoffs.
    """
    global franchise_history
    if not gm_season_stats: return None

    # Build helpers
    player_map = {}; team_map = {}
    for tm, pls in active_rosters.items():
        for p in pls:
            player_map[p["name"]] = p; team_map[p["name"]] = tm
    def avg(n, stat):
        s = gm_season_stats.get(n, {}); gp = max(1, s.get("GP",1))
        return s.get(stat,0) / gp
    qualified = [n for n,s in gm_season_stats.items() if s.get("GP",0)>=20]
    if not qualified: return None

    def mvp_score(n):
        p=player_map.get(n); ovr=p.get("overall",75) if p else 75
        w=gm_records.get(team_map.get(n,""),{}).get("W",0)
        return avg(n,"PTS")*1.2+avg(n,"AST")*0.8+avg(n,"REB")*0.4+w*0.05+ovr*0.02
    def dpoy_score(n):
        p=player_map.get(n); dfn=p.get("defense",75) if p else 75
        return dfn*0.5+avg(n,"STL")*5+avg(n,"BLK")*4

    mvp_name  = max(qualified, key=mvp_score)
    dpoy_name = max(qualified, key=dpoy_score)
    # Finals MVP — best scorer on champion's roster
    champ_players = [n for n in qualified if team_map.get(n)==champion]
    finals_mvp    = max(champ_players, key=lambda n:avg(n,"PTS")) if champ_players else mvp_name
    # ROY
    rookies  = [n for n in qualified if player_map.get(n,{}).get("age",30)<=23]
    roy_name = max(rookies, key=lambda n:avg(n,"PTS")*1.2+avg(n,"AST")*0.4+avg(n,"REB")*0.4, default=None)

    season = gm_season
    fh     = franchise_history
    fh["champions"].append({
        "season": season, "team": champion, "finals_mvp": finals_mvp,
        "score":  f"{champion_score}–{loser_score}"
    })
    fh["team_rings"][champion] = fh["team_rings"].get(champion, 0) + 1
    for award, name in [("MVP", mvp_name), ("DPOY", dpoy_name),
                         ("Finals MVP", finals_mvp)] + ([("ROY", roy_name)] if roy_name else []):
        fh["award_history"].append({"season":season,"award":award,
                                    "name":name,"team":team_map.get(name,"?")})
    return {"mvp":mvp_name,"dpoy":dpoy_name,"finals_mvp":finals_mvp,"roy":roy_name}

def run_full_offseason(active_rosters, all_teams, champion, champ_score=0, lose_score=0):
    """
    Full offseason sequence called after playoffs:
      1. Champion celebration
      2. Season awards display + history recording
      3. Player development / retirements
      4. Accumulate career stats
      5. NBA Draft (2 rounds)
      6. Free agency
      7. Re-init player meta (morale, clutch, archetype)
      8. Team management view option
      9. Advance to next season
    """
    global gm_season, franchise_history

    # ── 1. Champion Celebration ──
    rings = franchise_history["team_rings"].get(champion, 0) + 1
    ring_str = "🏆" * min(rings, 10)
    print(f"\n{'═'*60}")
    print(f"{BOLD}{YELLOW}  🏆 NBA CHAMPION — Season {gm_season}{RESET}")
    print(f"{'═'*60}")
    print(f"\n  {BOLD}{YELLOW}{color_team_name(champion)}{RESET} are your {gm_season} NBA Champions!")
    print(f"  {ring_str}  {'Franchise rings: '+str(rings)}")
    if champion == gm_team:
        print(f"\n  {GREEN}{BOLD}🎉 CONGRATULATIONS! YOUR FRANCHISE WINS THE CHAMPIONSHIP! 🎉{RESET}")

    # ── 2. Awards ──
    award_data = _record_awards_history(active_rosters, champion, champ_score, lose_score)
    show_awards(active_rosters)
    if award_data:
        print(f"\n  {YELLOW}🏅 Season {gm_season} Awards Summary:{RESET}")
        print(f"  MVP:       {BOLD}{award_data['mvp']}{RESET}")
        print(f"  DPOY:      {BOLD}{award_data['dpoy']}{RESET}")
        print(f"  Finals MVP:{BOLD}{award_data['finals_mvp']}{RESET}")
        if award_data.get("roy"):
            print(f"  ROY:       {BOLD}{award_data['roy']}{RESET}")

    # ── Season Recap + Owner Grades ──
    generate_season_recap(active_rosters, champion)
    news_add("GENERAL",
        f"🏆 {champion} WIN THE CHAMPIONSHIP — Season {gm_season}!",
        f"Congratulations to {champion} on winning the Season {gm_season} NBA Championship.")
    grade_season(all_teams, champion)
    input(f"\n  {DIM}Press ENTER to continue to Player Development...{RESET}")

    # ── 3. Career stats ──
    accumulate_career_stats(active_rosters)

    # ── 4. Player development ──
    progress_players_full(active_rosters, gm_season)

    input(f"\n  {DIM}Press ENTER to continue to the NBA Draft...{RESET}")

    # ── 5. Draft ──
    gm_season += 1
    advance_picks_year()
    run_draft(active_rosters, gm_team_name=gm_team, rounds=2)

    input(f"\n  {DIM}Press ENTER to continue to Free Agency...{RESET}")

    # ── 6. Free Agency ──
    init_contracts(active_rosters)   # give contracts to newly drafted players
    run_free_agency(active_rosters, all_teams, gm_team)

    # ── 7. Re-init meta ──
    init_player_meta(active_rosters)
    init_contracts(active_rosters)   # finalize any missing contracts

    # ── 8. Offseason menu ──
    print(f"\n{BOLD}{YELLOW}{'╔'*60}{RESET}")
    print(f"{BOLD}{YELLOW}║{RESET}{BOLD}{CYAN}  ☀️  OFFSEASON MENU — Season {gm_season}{RESET}{BOLD}{YELLOW}{' '*22}║{RESET}")
    print(f"{BOLD}{YELLOW}{'╚'*60}{RESET}\n")
    
    while True:
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}1.{RESET} {WHITE}View / Manage Roster{RESET}       {DIM}(your players){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}2.{RESET} {ORANGE}Trade Center{RESET}               {DIM}(make deals){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}3.{RESET} {LBLUE}Team Management{RESET}            {DIM}(payroll / ratings){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}4.{RESET} {MAGENTA}Franchise History{RESET}          {DIM}(championships / awards){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}5.{RESET} {YELLOW}My Draft Picks{RESET}             {DIM}(future assets){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}6.{RESET} {GREEN}Start Season {gm_season}{RESET}        {DIM}(begin games){RESET}")
        print(f"\n{DIM}{'─'*60}{RESET}")
        c = input(f"  {BOLD}{CYAN}Choose option:{RESET} ").strip()
        if   c == "1": _show_roster(active_rosters, gm_team)
        elif c == "2": trade_menu(active_rosters)
        elif c == "3": show_team_management(active_rosters, gm_team)
        elif c == "4": show_franchise_history(active_rosters)
        elif c == "5": _show_picks(gm_team)
        elif c == "6": break

    reset_season_records(all_teams)
    reset_season_stats()
    print(f"\n  {GREEN}Season {gm_season} ready! Good luck, GM.{RESET}\n")

# ══════════════════════════════════════════
# FRANCHISE HISTORY VIEWER
# ══════════════════════════════════════════
def show_franchise_history(active_rosters):
    """Display the full multi-season franchise history."""
    fh = franchise_history
    print(f"\n{BOLD}{YELLOW}{'╔'*62}{RESET}")
    print(f"{BOLD}{YELLOW}║{RESET}{BOLD}{WHITE}  🏀 FRANCHISE HISTORY{RESET}{BOLD}{YELLOW}{' '*38}║{RESET}")
    print(f"{BOLD}{YELLOW}{'╚'*62}{RESET}")

    # ── Champions ──
    if fh["champions"]:
        print(f"\n  {BOLD}NBA Champions by Season:{RESET}")
        for c in fh["champions"]:
            crown = f"{YELLOW}🏆{RESET}" if c["team"] == gm_team else "  "
            print(f"  {crown} Season {c['season']:>2}:  {color_team_name(c['team'])}"
                  f"  {DIM}(Finals MVP: {c['finals_mvp']}){RESET}")

    # ── Team Rings ──
    if fh["team_rings"]:
        print(f"\n  {BOLD}Championship Wins:{RESET}")
        sorted_rings = sorted(fh["team_rings"].items(), key=lambda x:-x[1])
        for tm, rings in sorted_rings[:10]:
            bar = "🏆" * rings
            print(f"  {bar}  {color_team_name(tm)} — {rings} ring{'s' if rings>1 else ''}")

    # ── Award History ──
    if fh["award_history"]:
        print(f"\n  {BOLD}Season Award History:{RESET}")
        for s_num in sorted({a["season"] for a in fh["award_history"]}):
            season_awards = [a for a in fh["award_history"] if a["season"]==s_num]
            print(f"  Season {s_num}: " + "  |  ".join(
                f"{a['award']}: {BOLD}{a['name']}{RESET}" for a in season_awards))

    # ── Career Pts Leaders ──
    cs = fh["career_stats"]
    if cs:
        print(f"\n  {BOLD}Career Points Leaders:{RESET}")
        leaders = sorted(cs.items(), key=lambda x: x[1].get("PTS",0), reverse=True)[:10]
        for rank, (name, stats) in enumerate(leaders, 1):
            gp  = max(1, stats.get("GP",1))
            pts = stats.get("PTS",0)
            reb = stats.get("REB",0)
            ast = stats.get("AST",0)
            print(f"  {rank:>2}. {BOLD}{name:<24}{RESET}  "
                  f"{pts:>5} PTS  {YELLOW}{pts/gp:.1f} PPG{RESET}  "
                  f"{reb:>4} REB  {ast:>4} AST  ({gp} GP)")
        print(f"\n  {BOLD}Career Assist Leaders:{RESET}")
        ast_leaders = sorted(cs.items(), key=lambda x: x[1].get("AST",0), reverse=True)[:5]
        for rank, (name, stats) in enumerate(ast_leaders, 1):
            gp  = max(1, stats.get("GP",1))
            print(f"  {rank:>2}. {BOLD}{name:<24}{RESET}  "
                  f"{stats.get('AST',0):>4} AST  {YELLOW}{stats.get('AST',0)/gp:.1f} APG{RESET}")
        print(f"\n  {BOLD}Career Rebounds Leaders:{RESET}")
        reb_leaders = sorted(cs.items(), key=lambda x: x[1].get("REB",0), reverse=True)[:5]
        for rank, (name, stats) in enumerate(reb_leaders, 1):
            gp  = max(1, stats.get("GP",1))
            print(f"  {rank:>2}. {BOLD}{name:<24}{RESET}  "
                  f"{stats.get('REB',0):>4} REB  {YELLOW}{stats.get('REB',0)/gp:.1f} RPG{RESET}")

    # ── Retired Players ──
    if fh["retired_players"]:
        print(f"\n  {BOLD}Hall of Legends (Retired):{RESET}")
        for r in sorted(fh["retired_players"], key=lambda x:x.get("ovr",0), reverse=True)[:15]:
            career = cs.get(r["name"],{})
            gp     = max(1,career.get("GP",1)); pts=career.get("PTS",0)
            print(f"  {DIM}🏁  {r['name']:<24}  OVR {r['ovr']}  "
                  f"Age {r['age']}  {round(pts/gp,1) if pts else '?'} PPG career{RESET}")

    print(f"\n{'═'*62}")

# ══════════════════════════════════════════
# DYNAMIC LEAGUE NEWS SYSTEM
# ══════════════════════════════════════════
league_news   = []   # [{game, season, category, headline, summary, date_label}]
_news_game_no = 0    # updated by _play_82 each game

NEWS_CATS = {
    "TRADE":   (ORANGE,  "🔄"),
    "INJURY":  (RED,     "🚑"),
    "SIGNING": (GREEN,   "🖊️"),
    "AWARDS":  (YELLOW,  "🏅"),
    "RECORD":  (CYAN,    "📊"),
    "RUMOR":   (MAGENTA, "🗣️"),
    "STREAK":  (LBLUE,   "🔥"),
    "PLAYOFF": (YELLOW,  "🏆"),
    "DRAFT":   (GREEN,   "🎓"),
    "RECAP":   (WHITE,   "📰"),
    "ALLSTAR": (YELLOW,  "⭐"),
    "GENERAL": (WHITE,   "📋"),
}

def news_add(category, headline, summary=""):
    """Add a news event to the league news feed."""
    cat  = category.upper()
    game = _news_game_no
    item = {
        "season":   gm_season,
        "game":     game,
        "category": cat,
        "headline": headline,
        "summary":  summary,
        "label":    f"S{gm_season} G{game}",
    }
    league_news.append(item)

def news_show(n=8, category=None, player=None, team=None, season=None):
    """Display recent news, with optional filters."""
    items = league_news[:]
    if season:   items = [x for x in items if x["season"] == season]
    if category: items = [x for x in items if x["category"] == category.upper()]
    if player:   items = [x for x in items if player.lower() in x["headline"].lower()
                                               or player.lower() in x["summary"].lower()]
    if team:
        ta = team_abbr(team) if len(team) > 5 else team
        items = [x for x in items if ta.lower() in x["headline"].lower()
                                     or ta in x["summary"]]
    items = items[-n:] if not (player or team or category) else items[-30:]
    if not items:
        print(f"  {DIM}No news found.{RESET}"); return
    for item in reversed(items):
        cat = item["category"]
        col, emoji = NEWS_CATS.get(cat, (WHITE, "📋"))
        print(f"\n  {col}{BOLD}{emoji} [{cat}]{RESET}  {DIM}{item['label']}{RESET}")
        print(f"  {col}{BOLD}{item['headline']}{RESET}")
        if item["summary"]:
            for line in item["summary"].split("\n"):
                print(f"  {DIM}{line}{RESET}")

def show_news_menu():
    """Interactive league news viewer."""
    while True:
        print(f"\n{BOLD}{LBLUE}{'╔'*58}{RESET}")
        print(f"{BOLD}{LBLUE}║{RESET}{BOLD}{WHITE}  📰 LEAGUE NEWS — Season {gm_season}{RESET}{BOLD}{LBLUE}{' '*21}║{RESET}")
        print(f"{BOLD}{LBLUE}{'╚'*58}{RESET}")
        total = len([x for x in league_news if x["season"]==gm_season])
        print(f"  {total} stories this season")
        print(f"\n  {CYAN}1.{RESET} Latest Headlines  "
              f"{CYAN}2.{RESET} Trades & Signings")
        print(f"  {CYAN}3.{RESET} Injuries           "
              f"{CYAN}4.{RESET} Records & Awards")
        print(f"  {CYAN}5.{RESET} Rumors             "
              f"{CYAN}6.{RESET} Power Rankings")
        print(f"  {CYAN}7.{RESET} Search by Player   "
              f"{CYAN}8.{RESET} Season Recap")
        print(f"  {CYAN}0.{RESET} Back")
        c = input("  > ").strip()
        if   c == "1": news_show(10, season=gm_season)
        elif c == "2":
            news_show(15, category="TRADE",   season=gm_season)
            news_show(15, category="SIGNING", season=gm_season)
        elif c == "3": news_show(15, category="INJURY", season=gm_season)
        elif c == "4":
            news_show(10, category="RECORD", season=gm_season)
            news_show(10, category="AWARDS", season=gm_season)
        elif c == "5": news_show(15, category="RUMOR", season=gm_season)
        elif c == "6": show_power_rankings(None)
        elif c == "7":
            pname = input("  Player name: ").strip()
            if pname: news_show(20, player=pname)
        elif c == "8":
            recap = next((x for x in reversed(league_news)
                          if x["category"]=="RECAP" and x["season"]==gm_season), None)
            if recap:
                print(f"\n  {BOLD}{WHITE}{recap['headline']}{RESET}")
                print(f"  {DIM}{recap['summary']}{RESET}")
            else: print(f"  {DIM}No season recap yet (play through the playoffs).{RESET}")
        elif c == "0": break

# ── News generators called from simulation ──
def _news_game_recap(t1, t2, score, gstats, winner):
    """Generate post-game news for notable performances."""
    best_n = max(gstats, key=lambda n: gstats[n]["PTS"])
    pts    = gstats[best_n]["PTS"]
    reb    = gstats[best_n]["REB"]
    ast    = gstats[best_n]["AST"]
    margin = abs(score[t1] - score[t2])
    loser  = t2 if winner == t1 else t1

    # 50-point game
    if pts >= 50:
        news_add("RECORD",
            f"{best_n} DROPS {pts} POINTS in historic performance!",
            f"{best_n} put on a masterclass for {color_team_abbr(winner)}, "
            f"dropping {pts} points on {color_team_abbr(loser)}. "
            f"The final score: {score[winner]}–{score[loser]}.")
    # 40-pt game
    elif pts >= 40:
        news_add("RECORD",
            f"{best_n} erupts for {pts} points — {score[winner]}–{score[loser]}",
            f"{best_n} carried {'their team' if gstats[best_n].get('team')==winner else 'their squad'} "
            f"to a {'blowout' if margin>15 else 'close'} {margin}-point {'win' if winner else 'loss'}.")
    # Triple-double
    if pts >= 10 and reb >= 10 and ast >= 10:
        news_add("RECORD",
            f"{best_n} records a TRIPLE-DOUBLE: {pts}/{reb}/{ast}",
            f"{best_n} dominated on all fronts as {color_team_abbr(winner)} "
            f"defeated {color_team_abbr(loser)} {score[winner]}–{score[loser]}.")
    # OT thriller
    if margin <= 2:
        news_add("GENERAL",
            f"THRILLER: {color_team_abbr(winner)} edges {color_team_abbr(loser)} {score[winner]}–{score[loser]}",
            f"A nail-biter decided by just {margin} {'point' if margin==1 else 'points'}.")

def _news_streak_check(team, wins_in_row):
    """Post news about winning streaks at 5, 8, 10, 15, 20."""
    if wins_in_row in (5, 8, 10, 15, 20):
        news_add("STREAK",
            f"{color_team_abbr(team)} WIN STREAK reaches {wins_in_row}!",
            f"{team} has won {wins_in_row} straight games and is surging "
            f"{'toward a top seed' if wins_in_row >= 10 else 'up the standings'}.")

def _news_playoff_race(all_teams, game_num):
    """Generate playoff race / MVP race updates every 15 games."""
    if not gm_records: return
    top = max(gm_records, key=lambda t: gm_records[t]["W"])
    tw  = gm_records[top]["W"]
    news_add("PLAYOFF",
        f"Power Rankings Update — Game {game_num}: {color_team_abbr(top)} leads all of basketball",
        f"{top} sits atop the league at {tw} wins. "
        f"{'Playoff races heating up in both conferences.' if game_num > 50 else 'The race is just getting started.'}")

def _news_mvp_race_update():
    """Post MVP race update based on current season stats."""
    if not gm_season_stats: return
    qualified = [(n, s) for n, s in gm_season_stats.items() if s.get("GP",0) >= 10]
    if not qualified: return
    top3 = sorted(qualified,
                  key=lambda x: x[1]["PTS"]/max(1,x[1]["GP"])*1.2 + x[1]["AST"]/max(1,x[1]["GP"])*0.5,
                  reverse=True)[:3]
    names = [f"{n} ({s['PTS']//max(1,s['GP']):.0f} PPG)" for n,s in top3]
    news_add("AWARDS",
        f"MVP Race Update: {top3[0][0]} leads the pack",
        "Top candidates: " + "  |  ".join(names))

def generate_trade_rumors(active_rosters, all_teams):
    """Generate pre-deadline trade rumors (not all become real)."""
    print(f"\n{'═'*58}\n{BOLD}{MAGENTA}  🗣️  TRADE DEADLINE RUMORS{RESET}\n{'═'*58}")
    rumors = []
    for tm in all_teams:
        pls = sorted(active_rosters.get(tm,[]), key=lambda p:p.get("overall",0), reverse=True)
        rec = gm_records.get(tm, {"W":0,"L":0})
        is_selling = rec["W"] < 28
        if is_selling and pls:
            star = pls[0]
            if star.get("overall",0) >= 78:
                suitors = [t for t in all_teams if t != tm and gm_records.get(t,{"W":0})["W"] > 35]
                if suitors:
                    suitor = random.choice(suitors)
                    rumors.append((star["name"], tm, suitor))
                    news_add("RUMOR",
                        f"RUMOR: {color_team_abbr(suitor)} eyeing {star['name']} from {color_team_abbr(tm)}",
                        f"Sources say {suitor} has interest in {star['name']} (OVR {star.get('overall',75)}) "
                        f"as the deadline approaches. No deal is imminent yet.")
    if rumors:
        for name, from_t, to_t in rumors[:6]:
            print(f"  {MAGENTA}🗣️{RESET}  {BOLD}{name}{RESET}  {color_team_abbr(from_t)} → {color_team_abbr(to_t)}?  "
                  f"{DIM}(unconfirmed){RESET}")
    else:
        print(f"  {DIM}No major rumors circulating.{RESET}")

def generate_season_recap(active_rosters, champion):
    """End-of-season feature story — saved to news feed."""
    if not gm_season_stats: return
    qualified = [(n,s) for n,s in gm_season_stats.items() if s.get("GP",0)>=20]
    if not qualified: return
    pts_ldr_n, pts_ldr_s = max(qualified, key=lambda x:x[1]["PTS"]/max(1,x[1]["GP"]))
    rec_ldr_n, rec_ldr_s = max(qualified, key=lambda x:x[1]["REB"]/max(1,x[1]["GP"]))
    ast_ldr_n, ast_ldr_s = max(qualified, key=lambda x:x[1]["AST"]/max(1,x[1]["GP"]))
    # Best young breakout
    young = [(n,s) for n,s in qualified if any(
        p.get("age",99)<=24 for tm in active_rosters.values() for p in tm if p["name"]==n)]
    breakout = max(young, key=lambda x:x[1]["PTS"]/max(1,x[1]["GP"]), default=(None,None))
    summary  = (
        f"Season {gm_season} is in the books. {champion} hoisted the Larry O'Brien Trophy.\n"
        f"Scoring leader: {pts_ldr_n} ({pts_ldr_s['PTS']//max(1,pts_ldr_s['GP'])} PPG).\n"
        f"Rebound leader: {rec_ldr_n} ({rec_ldr_s['REB']//max(1,rec_ldr_s['GP'])} RPG).\n"
        f"Assist leader:  {ast_ldr_n} ({ast_ldr_s['AST']//max(1,ast_ldr_s['GP'])} APG)."
        + (f"\nBreakout star: {breakout[0]}." if breakout[0] else "")
    )
    news_add("RECAP", f"SEASON {gm_season} RECAP — {champion} are YOUR NBA CHAMPIONS", summary)
    print(f"\n{'═'*60}\n{BOLD}{YELLOW}  📰 SEASON {gm_season} RECAP{RESET}\n{'═'*60}")
    print(f"  {DIM}{summary}{RESET}\n{'═'*60}")

# ══════════════════════════════════════════
# POWER RANKINGS & WEEKLY FEATURES
# ══════════════════════════════════════════
def show_power_rankings(active_rosters):
    """Display current power rankings for all 30 teams."""
    print(f"\n{BOLD}{MAGENTA}{'╔'*58}{RESET}")
    print(f"{BOLD}{MAGENTA}║{RESET}{BOLD}{WHITE}  📈 POWER RANKINGS{RESET}{BOLD}{MAGENTA}{' '*38}║{RESET}")
    print(f"{BOLD}{MAGENTA}{'╚'*58}{RESET}\n")
    
    if not gm_records:
        print(f"  {DIM}Play some games first.{RESET}"); return
    teams = list(gm_records.keys())
    def pr_score(t):
        r   = gm_records.get(t, {"W":0,"L":0,"PF":0,"PA":0})
        gp  = max(1, r["W"]+r["L"])
        pct = r["W"] / gp
        nrt = (r.get("PF",0) - r.get("PA",0)) / gp
        # blend win pct and net rating
        return pct * 60 + nrt * 0.5
    ranked = sorted(teams, key=pr_score, reverse=True)
    print(f"\n{'═'*58}")
    print(f"{BOLD}{LBLUE}  📊 POWER RANKINGS — Season {gm_season}{RESET}")
    print(f"{'═'*58}")
    print(f"  {'#':>3}  {'TEAM':<30}  W    L   PCT   DIFF")
    print(f"  {'─'*56}")
    for i, t in enumerate(ranked, 1):
        r   = gm_records.get(t, {"W":0,"L":0,"PF":0,"PA":0})
        gp  = max(1, r["W"]+r["L"])
        pct = r["W"]/gp
        diff= r.get("PF",0) - r.get("PA",0)
        dc  = GREEN if diff>=0 else RED
        you = f" {YELLOW}★{RESET}" if t==gm_team else ""
        tier= (f"{YELLOW}⚡{RESET}" if i<=5 else f"{ORANGE}▲{RESET}" if i<=10 else
               f"{DIM}▼{RESET}" if i>=25 else "  ")
        print(f"  {i:>3}. {tier} {color_team_abbr(t):<6} {color_team_name(t):<26}"
              f"{you}  {GREEN}{r['W']:>2}{RESET}  {RED}{r['L']:>2}{RESET}"
              f"  {WHITE}{pct:.3f}{RESET}  {dc}{diff:+d}{RESET}")
    print(f"{'═'*58}")

def show_mvp_ladder(active_rosters=None):
    """Top-10 MVP candidates with win-probability style percentages."""
    if not gm_season_stats:
        print(f"  {DIM}No stats yet.{RESET}")
        return
    show_mvp_with_pct(
        gm_season_stats, gm_records,
        lambda n: _player_team(n, active_rosters), gm_season,
    )

def show_rookie_ladder(active_rosters):
    """Top rookies with ROY race percentages."""
    show_rookie_watch(active_rosters, gm_season_stats, gm_season)

def _player_team(pname, active_rosters=None):
    """Reverse-lookup a player's team from active_rosters."""
    if active_rosters is None:
        active_rosters = _gctx.get("active_rosters")
    if active_rosters:
        for tm, pls in active_rosters.items():
            for p in pls:
                if p["name"] == pname:
                    return tm
    return "?"

# ══════════════════════════════════════════
# AI TRADE ENGINE
# ══════════════════════════════════════════
def _team_profile(team, active_rosters):
    """
    Determine a team's front-office personality and needs.
    Returns a dict used by AI trade evaluation.
    """
    pls  = active_rosters.get(team, [])
    rec  = gm_records.get(team, {"W":0,"L":0})
    wins = rec["W"]; gp = max(1, rec["W"]+rec["L"])
    avg_age = sum(p.get("age",27) for p in pls) / max(1,len(pls))
    avg_ovr = sum(p.get("overall",75) for p in pls) / max(1,len(pls))
    stars   = [p for p in pls if p.get("overall",0) >= 87]
    young_s = [p for p in pls if p.get("overall",0) >= 82 and p.get("age",30) <= 25]
    pct     = wins / gp

    if pct >= 0.62 and stars:        pers = "win-now"
    elif wins <= 22:                  pers = "rebuilding"
    elif young_s and avg_age < 26:    pers = "young-core"
    elif avg_age >= 29 and pct>0.50:  pers = "veteran"
    elif pct >= 0.48:                 pers = "contending"
    else:                             pers = "neutral"

    # What positions are thin?
    pos_cnt = {}
    for p in pls:
        pos_cnt[p.get("pos","PG")] = pos_cnt.get(p.get("pos","PG"),0) + 1
    needs = [pos for pos in POSITIONS if pos_cnt.get(pos,0) < 2]

    return {"personality":pers,"wins":wins,"avg_age":avg_age,"avg_ovr":avg_ovr,
            "stars":stars,"young_stars":young_s,"needs":needs,"payroll":get_payroll(active_rosters,team)}

def _ai_player_value(p, profile):
    """
    Return how much a team values a player given their profile.
    Modifies trade_value by team personality.
    """
    base = player_trade_value(p)
    pers = profile["personality"]
    age  = p.get("age",27)
    ovr  = p.get("overall",75)
    pot  = p.get("potential","B")

    if pers == "win-now":
        # Prefers proven veterans; pays premium for stars
        if ovr >= 85: base *= 1.4
        if age >= 28: base *= 1.1
        if age <= 22: base *= 0.7
    elif pers == "rebuilding":
        # Loves youth and picks
        if age <= 22 and pot in ("A+","A"): base *= 1.8
        if age >= 30: base *= 0.5
    elif pers == "young-core":
        if pot in ("A+","A") and age <= 25: base *= 1.5
        if age >= 32: base *= 0.6
    elif pers == "veteran":
        if 28 <= age <= 33: base *= 1.2
    return base

def _ai_pick_value(pk, profile):
    """How much the AI values a draft pick."""
    round_val = 200 if pk["round"]==1 else 60
    pers      = profile["personality"]
    mult      = (2.2 if pers=="rebuilding" else 0.5 if pers=="win-now" else 1.0)
    return round_val * mult

def ai_evaluate_trade(giving, getting, giving_pk, getting_pk, give_prof, get_prof):
    """
    Returns (True, reason) if the receiving side finds the trade acceptable.
    Both sides evaluated independently — trade goes through only if both agree.
    """
    give_val = sum(_ai_player_value(p, get_prof) for p in giving) \
             + sum(_ai_pick_value(pk, get_prof) for pk in giving_pk)
    get_val  = sum(_ai_player_value(p, give_prof) for p in getting) \
             + sum(_ai_pick_value(pk, give_prof) for pk in getting_pk)

    if get_val == 0: return False, "receiving nothing of value"
    ratio = give_val / max(1, get_val)

    if ratio < 0.55: return False, f"return too low ({ratio:.2f}x)"
    if ratio > 3.0:  return False, f"offer too generous — suspicious ({ratio:.2f}x)"
    return True, "fair deal"

def ai_trade_deadline_moves(active_rosters, all_teams):
    """
    At the trade deadline: generate 2-5 AI-vs-AI trades.
    Contenders buy veterans; rebuilders sell stars for picks.
    """
    print(f"\n{'═'*58}\n{BOLD}{ORANGE}  🔄 TRADE DEADLINE MOVES{RESET}\n{'═'*58}")
    deals_done = 0
    random.shuffle(all_teams)
    for seller in all_teams:
        if deals_done >= 5: break
        sell_prof = _team_profile(seller, active_rosters)
        if sell_prof["personality"] not in ("rebuilding","neutral"): continue
        # pick the best player they'd trade
        candidates = [p for p in active_rosters.get(seller,[])
                      if p.get("overall",0) >= 75 and p.get("age",30) <= 32]
        if not candidates: continue
        trade_bait = random.choice(candidates)
        # find a buyer
        buyers = [t for t in all_teams if t!=seller and
                  _team_profile(t,active_rosters)["personality"] in ("win-now","contending","veteran")]
        if not buyers: continue
        buyer = random.choice(buyers)
        buy_prof = _team_profile(buyer, active_rosters)
        # buyer sends back a lesser player + a 1st pick
        return_candidates = [p for p in active_rosters.get(buyer,[])
                              if 68 <= p.get("overall",0) <= trade_bait.get("overall",75)-2]
        return_player = random.choice(return_candidates) if return_candidates else None
        picks = get_team_picks(buyer, year=None)
        rnd1_picks = [pk for pk in picks if pk["round"]==1]

        if not return_player and not rnd1_picks: continue

        # Execute
        active_rosters[seller].remove(trade_bait)
        active_rosters[buyer].append(trade_bait)
        if return_player:
            active_rosters[buyer].remove(return_player)
            active_rosters[seller].append(return_player)
        if rnd1_picks:
            pk = rnd1_picks[0]
            transfer_pick(pk, buyer, seller)

        rp_str = f"{return_player['name']} + " if return_player else ""
        pk_str = f" + {picks_label(rnd1_picks[0])}" if rnd1_picks else ""
        print(f"\n  {ORANGE}🔄 DEAL:{RESET}  "
              f"{color_team_abbr(buyer)} gets {BOLD}{trade_bait['name']}{RESET}"
              f"  for  {rp_str}{YELLOW}{'1st Rd Pick' if rnd1_picks else ''}{RESET}")
        news_add("TRADE",
            f"TRADE: {trade_bait['name']} dealt to {color_team_abbr(buyer)}",
            f"{seller} trades {trade_bait['name']} (OVR {trade_bait.get('overall',75)}) "
            f"to {buyer} for {rp_str}{'a 1st-round pick' if rnd1_picks else 'future considerations'}{pk_str}.")
        deals_done += 1

    if deals_done == 0:
        print(f"  {DIM}No major trades completed at the deadline.{RESET}")

# ══════════════════════════════════════════
# ALL-STAR WEEKEND
# ══════════════════════════════════════════
def run_all_star_weekend(active_rosters):
    """
    Full All-Star Weekend event run at game 41 of the season.
    Events: Skills Challenge · 3PT Contest · Dunk Contest · All-Star Game
    """
    print(f"\n{'═'*60}")
    print(f"{BOLD}{YELLOW}  ⭐ ALL-STAR WEEKEND — Season {gm_season}{RESET}")
    print(f"{'═'*60}")
    input(f"  {DIM}Press ENTER to begin All-Star Weekend...{RESET}")

    # Select All-Stars: top 24 scorers (with team diversity)
    if not gm_season_stats:
        print(f"  {DIM}Not enough stats yet — skipping.{RESET}"); return
    qualified = [(n,s) for n,s in gm_season_stats.items() if s.get("GP",0)>=10]
    scored    = sorted(qualified, key=lambda x:x[1]["PTS"]/max(1,x[1]["GP"]), reverse=True)
    all_stars = [n for n,_ in scored[:24]]

    # Map names to players
    pmap = {}
    for tm, pls in active_rosters.items():
        for p in pls:
            if p["name"] in all_stars:
                pmap[p["name"]] = (p, tm)

    print(f"\n  {BOLD}{YELLOW}⭐ ALL-STAR SELECTIONS:{RESET}")
    for i, n in enumerate(all_stars, 1):
        p, tm = pmap.get(n, ({}, "?"))
        print(f"  {i:>2}. {BOLD}{n:<26}{RESET} {color_team_abbr(tm)}  "
              f"OVR {p.get('overall',75)}  {DIM}{p.get('archetype','?')}{RESET}")

    input(f"\n  {DIM}Press ENTER for the Skills Challenge...{RESET}")

    # ── Skills Challenge ──
    print(f"\n  {BOLD}{CYAN}🏃 SKILLS CHALLENGE{RESET}")
    skill_pool = [n for n in all_stars if pmap.get(n,({},))[0].get("playmaking",75) >= 70][:6]
    if not skill_pool: skill_pool = all_stars[:6]
    skill_winner = max(skill_pool,
        key=lambda n: pmap.get(n,({},))[0].get("playmaking",75) + random.randint(-15,15))
    print(f"  {GREEN}🏆 Winner: {BOLD}{skill_winner}{RESET}  — completes the course in record time!")
    news_add("ALLSTAR", f"All-Star Skills Challenge: {skill_winner} wins!",
             f"{skill_winner} beat out the competition in the Skills Challenge during All-Star Weekend.")

    input(f"  {DIM}Press ENTER for the 3-Point Contest...{RESET}")

    # ── 3-Point Contest ──
    print(f"\n  {BOLD}{ORANGE}🎯 THREE-POINT CONTEST{RESET}")
    three_pool = [n for n in all_stars if pmap.get(n,({},))[0].get("shooting",75) >= 72][:6]
    if not three_pool: three_pool = all_stars[:6]
    scores_3pt = {}
    for n in three_pool:
        sht = pmap.get(n,({},))[0].get("shooting",75)
        scores_3pt[n] = round(sht * 0.3 + random.randint(5, 30), 1)
        print(f"    {n:<26} {scores_3pt[n]:>5.1f} pts")
    winner_3 = max(scores_3pt, key=scores_3pt.get)
    print(f"\n  {GREEN}🏆 Winner: {BOLD}{winner_3}{RESET} with {scores_3pt[winner_3]} points!")
    news_add("ALLSTAR", f"3-Point Contest: {winner_3} is the champion!",
             f"{winner_3} drained shot after shot to win the 3-Point Contest "
             f"with a score of {scores_3pt[winner_3]}.")

    input(f"  {DIM}Press ENTER for the Slam Dunk Contest...{RESET}")

    # ── Dunk Contest ──
    print(f"\n  {BOLD}{RED}🤸 SLAM DUNK CONTEST{RESET}")
    dunk_pool = [n for n in all_stars
                 if pmap.get(n,({},))[0].get("offense",75) >= 75
                 and pmap.get(n,({},))[0].get("age",99) <= 28][:4]
    if not dunk_pool: dunk_pool = all_stars[:4]
    dunk_scores = {n: round(random.gauss(
        pmap.get(n,({},))[0].get("offense",75)*0.4 + 30, 8), 1)
        for n in dunk_pool}
    dunks = [
        "windmill 360!", "between-the-legs from the free throw line!",
        "reverse ally-oop off the glass!", "double-clutch baseline jam!",
        "cradle dunk from half-court run-up!"
    ]
    for n, sc in dunk_scores.items():
        print(f"    {n:<26} {sc:>5.1f}  — {random.choice(dunks)}")
    winner_d = max(dunk_scores, key=dunk_scores.get)
    print(f"\n  {GREEN}🏆 Winner: {BOLD}{winner_d}{RESET} — brings the house DOWN!")
    news_add("ALLSTAR", f"Dunk Contest: {winner_d} wins with an unforgettable performance!",
             f"{winner_d} wins the Slam Dunk Contest during All-Star Weekend.")

    input(f"  {DIM}Press ENTER for the All-Star Game...{RESET}")

    # ── All-Star Game ──
    print(f"\n  {BOLD}{YELLOW}⭐ ALL-STAR GAME{RESET}")
    team_a = all_stars[:12]; team_b = all_stars[12:]
    # Simulate: random high-scoring result
    score_a = random.randint(155, 210)
    score_b = random.randint(155, 210)
    while score_a == score_b:
        score_b = random.randint(155, 210)
    winner_team = "Team A" if score_a > score_b else "Team B"
    winner_stars = team_a if score_a > score_b else team_b
    game_mvp = max(winner_stars,
        key=lambda n: gm_season_stats.get(n,{}).get("PTS",0)/max(1,gm_season_stats.get(n,{}).get("GP",1))
                      + random.randint(-5,10))
    pts_mvp  = random.randint(22, 45)
    print(f"\n  FINAL:  Team A  {score_a}  —  {score_b}  Team B")
    print(f"\n  {YELLOW}⭐ ALL-STAR MVP: {BOLD}{game_mvp}{RESET} — {pts_mvp} points!")
    news_add("ALLSTAR",
        f"All-Star MVP: {game_mvp} dazzles in {score_a}–{score_b} All-Star Game",
        f"{game_mvp} led {winner_team} to victory with {pts_mvp} points. "
        f"The All-Star Game drew a packed crowd for another memorable showcase.")

    # Record in franchise history
    franchise_history.setdefault("allstar_winners",[]).append({
        "season": gm_season,
        "skills": skill_winner, "threepoint": winner_3,
        "dunk": winner_d, "gamemvp": game_mvp
    })
    print(f"\n{'═'*60}\n  All-Star Weekend complete! The regular season resumes.\n{'═'*60}")

# ══════════════════════════════════════════
# PLAYER CAREER MILESTONES & LEGACY
# ══════════════════════════════════════════
# career_highs tracks per-player season bests: {name: {PTS:0, REB:0, AST:0}}
career_highs   = {}
# career_totals  tracks per-player running career totals for milestone thresholds
career_totals  = {}

_MILESTONE_PTS = [1000, 5000, 10000, 15000, 20000, 25000, 30000]
_MILESTONE_REB = [1000, 3000, 5000, 10000]
_MILESTONE_AST = [500,  1000, 3000, 5000]

def check_milestones(name, game_pts, game_reb, game_ast):
    """
    After each game, accumulate career totals and detect milestone crossings.
    Called from add_to_season_stats override in _play_82.
    """
    if name not in career_totals:
        career_totals[name] = {"PTS":0,"REB":0,"AST":0}
    ct  = career_totals[name]
    old = {k: ct[k] for k in ct}
    ct["PTS"] += game_pts; ct["REB"] += game_reb; ct["AST"] += game_ast

    for thresh in _MILESTONE_PTS:
        if old["PTS"] < thresh <= ct["PTS"]:
            news_add("RECORD",
                f"{name} reaches {thresh:,} career points!",
                f"{name} crossed the {thresh:,}-point mark "
                f"(now {ct['PTS']:,} career points). A true NBA legend.")
            if thresh >= 10000:
                print(f"\n  {YELLOW}{BOLD}🏆 MILESTONE: {name} reaches {thresh:,} CAREER POINTS!{RESET}")
    for thresh in _MILESTONE_REB:
        if old["REB"] < thresh <= ct["REB"]:
            news_add("RECORD", f"{name} passes {thresh:,} career rebounds!",
                     f"Another milestone for {name}: {thresh:,} career boards.")
    for thresh in _MILESTONE_AST:
        if old["AST"] < thresh <= ct["AST"]:
            news_add("RECORD", f"{name} passes {thresh:,} career assists!",
                     f"{name} has now dished out {thresh:,} career assists.")

def update_career_highs(name, game_pts, game_reb, game_ast):
    """Track single-game career highs per player."""
    if name not in career_highs:
        career_highs[name] = {"PTS":0,"REB":0,"AST":0}
    ch = career_highs[name]
    if game_pts > ch["PTS"]:
        if ch["PTS"] > 0 and game_pts >= 35:   # only news if notable
            news_add("RECORD",
                f"CAREER HIGH: {name} scores {game_pts} points!",
                f"A new career best for {name} — {game_pts} points, surpassing their previous high of {ch['PTS']}.")
        ch["PTS"] = game_pts
    if game_reb > ch["REB"]: ch["REB"] = game_reb
    if game_ast > ch["AST"]: ch["AST"] = game_ast

def hof_score(player_name):
    """
    Compute a Hall of Fame eligibility score at retirement.
    Based on career points, awards, championships.
    """
    cs = franchise_history.get("career_stats",{}).get(player_name,{})
    aw = [a for a in franchise_history.get("award_history",[]) if a["name"]==player_name]
    ch = franchise_history.get("champions",[])
    rings = sum(1 for c in ch if
                any(p["name"]==player_name for t,pls in {}.items() for p in pls))

    pts_score = min(40, cs.get("PTS",0) / 1000)
    aw_score  = len(aw) * 8
    gp_score  = min(15, cs.get("GP",0) / 50)
    return round(pts_score + aw_score + gp_score, 1)

# ══════════════════════════════════════════
# COACHING SYSTEM
# ══════════════════════════════════════════
# Build a team → coach lookup at module load
_team_to_coach = {}
for _cname, _cdata in coach_data.items():
    _team_to_coach[_cdata["team"]] = {"name": _cname, **_cdata}

def get_team_coach(team):
    """Return the coach dict for a team (name + bonuses)."""
    return _team_to_coach.get(team, {"name":"Unknown Coach","bonuses":{}})

def coach_offense_bonus(team):
    """Return +float shooting bonus from coach offense/shooting/three_pt bonuses."""
    b = get_team_coach(team)["bonuses"]
    raw = b.get("offense",0)*0.003 + b.get("shooting",0)*0.003 + b.get("three_point_shooting",0)*0.004
    return min(0.05, raw)

def coach_defense_bonus(team):
    """Return +int def rating bonus from coach defense/strategy bonuses."""
    b = get_team_coach(team)["bonuses"]
    return min(6, b.get("defense",0) + b.get("strategy",0)//2)

def coach_development_bonus(team):
    """Return +int player development bonus (used in progress_players_full)."""
    b = get_team_coach(team)["bonuses"]
    return b.get("player_development",0) + b.get("development",0)//2

def show_coaching_staff(active_rosters, team):
    """Display a team's coaching staff and ratings."""
    c = get_team_coach(team)
    b = c["bonuses"]
    print(f"\n{'═'*54}")
    print(f"{BOLD}{CYAN}  👔 COACHING STAFF — {color_team_name(team)}{RESET}")
    print(f"{'═'*54}")
    print(f"  Head Coach:  {BOLD}{c['name']}{RESET}")
    print(f"\n  {'ATTRIBUTE':<22}  RATING")
    print(f"  {'─'*36}")
    attrs = [
        ("Offense",     b.get("offense",0)+b.get("three_point_shooting",0)//2),
        ("Defense",     b.get("defense",0)),
        ("Development", b.get("player_development",0)+b.get("development",0)//2),
        ("Strategy",    b.get("strategy",0)),
        ("Chemistry",   b.get("chemistry",0)+b.get("teamwork",0)//2),
        ("Pace",        b.get("pace",0)),
    ]
    for attr, val in attrs:
        if val > 0:
            bar = "█" * val
            c2  = GREEN if val>=5 else ORANGE if val>=3 else WHITE
            print(f"  {attr:<22}  {c2}{bar} {val}{RESET}")
    print(f"\n  Game Bonuses:")
    print(f"    Off boost:  {ORANGE}+{coach_offense_bonus(team)*100:.1f}%{RESET} shooting probability")
    print(f"    Def boost:  {CYAN}+{coach_defense_bonus(team)}{RESET} defensive rating")
    print(f"    Dev boost:  {GREEN}+{coach_development_bonus(team)}{RESET} development per offseason")

# ══════════════════════════════════════════
# TEAM GOALS & OWNER EXPECTATIONS
# ══════════════════════════════════════════
season_goals = {}   # {team: {goal, target_wins, result, grade}}

def assign_season_goals(active_rosters, all_teams):
    """
    Assign realistic season goals to every team based on their roster.
    Called at the start of each 82-game season.
    """
    global season_goals
    season_goals = {}
    for tm in all_teams:
        pls    = active_rosters.get(tm, [])
        avg_ovr = sum(p.get("overall",75) for p in pls) / max(1,len(pls))
        stars   = [p for p in pls if p.get("overall",0)>=87]

        if avg_ovr >= 84 and stars:
            goal = "Win the Championship"
            target_wins = 52
        elif avg_ovr >= 80:
            goal = "Reach the Conference Finals"
            target_wins = 48
        elif avg_ovr >= 76:
            goal = "Make the Playoffs"
            target_wins = 42
        elif avg_ovr >= 72:
            goal = "Finish .500"
            target_wins = 41
        else:
            goal = "Develop Young Players"
            target_wins = 25
        season_goals[tm] = {"goal":goal,"target":target_wins,"grade":None,"result":None}

def grade_season(all_teams, champion):
    """
    Grade every team at season end.
    Called after standings are final.
    """
    print(f"\n{'═'*60}\n{BOLD}{MAGENTA}  📋 OWNER EXPECTATIONS REPORT — Season {gm_season}{RESET}\n{'═'*60}")
    for tm in all_teams:
        g   = season_goals.get(tm)
        if not g: continue
        rec = gm_records.get(tm, {"W":0,"L":0})
        w   = rec["W"]
        goal = g["goal"]; target = g["target"]

        # Grade logic
        champ_bonus = (tm == champion)
        over = w - target
        if champ_bonus:              grade = "A+"
        elif over >= 8:              grade = "A"
        elif over >= 3:              grade = "B+"
        elif over >= -2:             grade = "B"
        elif over >= -8:             grade = "C"
        elif over >= -15:            grade = "D"
        else:                        grade = "F"
        g["grade"] = grade; g["result"] = w

        gc = (GREEN if grade in ("A+","A") else ORANGE if grade in ("B+","B") else
              YELLOW if grade=="C" else RED)
        you = f" {YELLOW}★ YOU{RESET}" if tm == gm_team else ""
        print(f"  {color_team_abbr(tm):<6} {color_team_name(tm):<30}{you}")
        print(f"    Goal: {DIM}{goal}{RESET}  Target: {target}W  Actual: {w}W  "
              f"Grade: {gc}{BOLD}{grade}{RESET}")

# ══════════════════════════════════════════
# ADVANCED STATISTICS
# ══════════════════════════════════════════
def compute_advanced_stats(name, active_rosters):
    """
    Compute PER, TS%, Usage Rate, +/- estimate, Win Shares for a player.
    Uses gm_season_stats (accumulated totals) + player OVR.
    """
    s  = gm_season_stats.get(name, {})
    gp = max(1, s.get("GP",1))
    pts= s.get("PTS",0); reb=s.get("REB",0); ast=s.get("AST",0)
    stl= s.get("STL",0); blk=s.get("BLK",0)

    # Find player OVR for additional context
    p = None
    for tm, pls in active_rosters.items():
        for pl in pls:
            if pl["name"] == name:
                p = pl; break
        if p: break
    ovr = p.get("overall",75) if p else 75

    # True Shooting % (simplified: pts / (2 * FGA estimate))
    fga_est = max(1, pts / 1.1)   # rough FGA from points
    ts_pct  = round(pts / (2 * fga_est) * 100, 1)

    # PER (simplified formula)
    per = round((pts/gp * 1.0 + reb/gp * 0.7 + ast/gp * 0.7
                 + stl/gp * 1.5 + blk/gp * 1.5 - 2.5) * (ovr/75), 1)
    per = max(0, per)

    # Usage Rate estimate
    usg = round(min(40, pts/gp * 1.2 + ast/gp * 0.5), 1)

    # Win Shares (simplified)
    ws  = round((pts/gp * 0.015 + reb/gp * 0.012 + ast/gp * 0.010) * gp / 82, 2)

    # +/- estimate based on team record vs league avg
    tm_wins = 0
    if p:
        for tm, pls in active_rosters.items():
            if p in pls:
                tm_wins = gm_records.get(tm, {"W":0})["W"]
                break
    plus_minus = round((tm_wins - 41) * 0.08 + (ovr - 75) * 0.12, 1)

    return {"PER":per,"TS%":ts_pct,"USG":usg,"WS":ws,"+/-":plus_minus,"GP":gp}

def show_advanced_stats(active_rosters):
    """Display advanced stats leaderboard."""
    if not gm_season_stats:
        print(f"  {DIM}No stats yet.{RESET}"); return
    qualified = [n for n,s in gm_season_stats.items() if s.get("GP",0)>=20]
    if not qualified: print(f"  {DIM}Need 20+ games.{RESET}"); return
    rows = []
    for n in qualified:
        adv = compute_advanced_stats(n, active_rosters)
        rows.append((n, adv))
    rows.sort(key=lambda x: x[1]["PER"], reverse=True)

    print(f"\n{'═'*68}\n{BOLD}{WHITE}  📊 ADVANCED STATS — Season {gm_season}{RESET}\n{'═'*68}")
    print(f"  {'PLAYER':<24}  PER    TS%   USG    WS   +/-   GP")
    print(f"  {'─'*60}")
    for n, adv in rows[:20]:
        per_c = GREEN if adv["PER"]>20 else ORANGE if adv["PER"]>14 else WHITE
        pm_c  = GREEN if adv["+/-"]>0 else RED
        print(f"  {n:<24}"
              f"  {per_c}{adv['PER']:>5.1f}{RESET}"
              f"  {adv['TS%']:>4.0f}%"
              f"  {adv['USG']:>4.1f}"
              f"  {CYAN}{adv['WS']:>4.2f}{RESET}"
              f"  {pm_c}{adv['+/-']:>+5.1f}{RESET}"
              f"  {adv['GP']:>4}")

def compare_players(active_rosters):
    """Side-by-side player comparison screen."""
    pmap = {}
    for tm, pls in active_rosters.items():
        for p in pls:
            pmap[p["name"]] = (p, tm)
    names = list(pmap.keys())
    print(f"\n{'═'*54}\n{BOLD}  🔍 PLAYER COMPARISON{RESET}\n{'═'*54}")
    for i, n in enumerate(names, 1):
        p, tm = pmap[n]
        print(f"  {i:>3}. {n:<26} {color_team_abbr(tm)} OVR:{p.get('overall',75)}")
    print()
    def pick(label):
        while True:
            raw = input(f"  {label} # (or name): ").strip()
            if raw.isdigit():
                idx = int(raw)-1
                if 0<=idx<len(names): return names[idx]
            else:
                for n in names:
                    if raw.lower() in n.lower(): return n
            print(RED+"  Not found."+RESET)
    n1 = pick("Player 1"); n2 = pick("Player 2")
    p1, t1 = pmap[n1]; p2, t2 = pmap[n2]
    adv1 = compute_advanced_stats(n1, active_rosters)
    adv2 = compute_advanced_stats(n2, active_rosters)
    s1   = gm_season_stats.get(n1,{"PTS":0,"REB":0,"AST":0,"STL":0,"BLK":0,"GP":1})
    s2   = gm_season_stats.get(n2,{"PTS":0,"REB":0,"AST":0,"STL":0,"BLK":0,"GP":1})
    gp1  = max(1,s1["GP"]); gp2  = max(1,s2["GP"])
    print(f"\n{'═'*60}")
    print(f"  {BOLD}{n1:<28}{RESET}  vs  {BOLD}{n2}{RESET}")
    print(f"  {color_team_abbr(t1):<28}       {color_team_abbr(t2)}")
    print(f"{'═'*60}")
    attrs = [
        ("Overall",    p1.get("overall",75),     p2.get("overall",75)),
        ("Offense",    p1.get("offense",75),      p2.get("offense",75)),
        ("Defense",    p1.get("defense",75),      p2.get("defense",75)),
        ("Shooting",   p1.get("shooting",75),     p2.get("shooting",75)),
        ("Playmaking", p1.get("playmaking",75),   p2.get("playmaking",75)),
        ("Rebounding", p1.get("rebounding",75),   p2.get("rebounding",75)),
        ("Clutch",     p1.get("clutch",70),        p2.get("clutch",70)),
        ("Age",        p1.get("age",27),           p2.get("age",27)),
        ("PPG",        round(s1["PTS"]/gp1,1),     round(s2["PTS"]/gp2,1)),
        ("RPG",        round(s1["REB"]/gp1,1),     round(s2["REB"]/gp2,1)),
        ("APG",        round(s1["AST"]/gp1,1),     round(s2["AST"]/gp2,1)),
        ("PER",        adv1["PER"],                adv2["PER"]),
        ("Win Shares", adv1["WS"],                 adv2["WS"]),
    ]
    for attr, v1, v2 in attrs:
        c1 = GREEN if v1 > v2 else (RED if v1 < v2 else WHITE)
        c2 = GREEN if v2 > v1 else (RED if v2 < v1 else WHITE)
        print(f"  {c1}{str(v1):>8}{RESET}  {attr:<12}  {c2}{v2}{RESET}")
    print(f"{'═'*60}")

# ══════════════════════════════════════════
# COMMENTARY
# ══════════════════════════════════════════
DRIVE_L = ["{n} blows past the defense and lays it in! 🏀",
           "{n} bursts into the lane and finishes strong! 💨",
           "{n} crosses over and drives baseline — GOOD! 🏀",
           "{n} splits the double-team and scores! 🔥",
           "{n} attacks the rim and converts! 💪"]
POST_L  = ["{n} backs down the defender — silky fadeaway! 😤",
           "{n} catches in the post, spins, scores! 🏀",
           "{n} uses their size for the easy bucket! 💪",
           "{n} seals their man and drops it in! 😤",
           "{n} powers through for the and-one! 🦾"]
MID_L   = ["{n} hits the pull-up mid-range — MONEY! 💰",
           "{n} pump-fakes once and rises — GOOD! 🎯",
           "{n} drains the elbow jumper! 💰",
           "{n} step-backs into the mid-range — splash! 💦"]
THREE_L = ["{n} steps back — DRILLS the three! 🔥","{n} fires from DEEP — GOOD! 🚀",
           "{n} catches and SPLASHES it! 💦","{n} pulls up from 30 feet — UNREAL! 🌟",
           "{n} drains the corner three — BANG! 🔥","{n} pump-fakes once, steps back — THREE! 💦"]
FT_L    = ["{n} calmly sinks the free throw 🎯","{n} steps up — GOOD ✅",
           "{n} converts from the stripe"]
MISS_L  = ["{n} rises up… rattles out! ❌","{n} off the back iron ❌",
           "{n} can't convert ❌","{n} pump-fakes and fires — BRICK 🧱"]
TO_L    = ["{n} telegraphs the pass — STOLEN! 💨","{n} dribbles off their own foot ⚠️",
           "{n} forces it into traffic — lost ⚠️"]
TECH_L  = ["{n} gets a TECHNICAL FOUL! 📋","Referee hits {n} with a tech! 📋",
           "{n} argues the call — TECHNICAL! 📋"]
# Flagrant fouls — very rare, carry suspension risk
FLAG_L  = [
    f"{RED}{{n}} throws a FLAGRANT FOUL on {{d}}! Ejected — facing a suspension! 🚨{RESET}",
    f"{RED}Dangerous play by {{n}} — FLAGRANT FOUL! Automatic ejection! 🚨{RESET}",
]
OFF_FOUL_L = [
    "{n} runs into a set defender — CHARGE! Offensive foul on {n}! ⚠️",
    "{n} barrels into {d} — offensive foul called! ⚠️",
    "Referee waves off the basket — offensive foul on {n}! ⚠️",
]
DEF_FOUL_L = [
    "{n} is fouled by {d} — to the line! 🎯",
    "{d} reaches in on {n} — shooting foul! 🎯",
    "{n} draws the defensive foul on {d}! 🎯",
]
VIOL_L  = {"double_dribble": "{n} — DOUBLE DRIBBLE! Turnover! ⚠️",
           "out_of_bounds":  "{n} steps out of bounds! Turnover! ⚠️",
           "3_seconds":      "3-second violation on {n}'s team! ⚠️",
           "shot_clock":     "SHOT CLOCK VIOLATION — {n}'s team loses possession! ⏱️"}

def _line(pool, name, d=None):
    return random.choice(pool).format(n=name, d=d or "")

# ══════════════════════════════════════════
# ROTATION / ROSTER HELPERS
# ══════════════════════════════════════════
def assign_minutes(team, active_rosters):
    available = [p for p in active_rosters[team]
                 if not p.get("active_injury",{}).get("retired",False)
                 and p.get("active_injury",{}).get("games_left",0) == 0]
    if not available: available = active_rosters[team]
    players = sorted(available, key=lambda x: x.get("overall",75), reverse=True)
    rot = {}
    for i, p in enumerate(players):
        if i<5:    mins=random.randint(32,38)
        elif i<10: mins=random.randint(8,22)
        else:       mins=random.randint(0,8)
        rot[p["name"]] = {"minutes":mins,"used":0,"out":False,"fouls":0}
    return rot

def get_active(team, rot, active_rosters):
    pool=[]
    for p in active_rosters[team]:
        n=p["name"]
        if n not in rot: continue
        if rot[n]["out"]: continue
        rem=rot[n]["minutes"]-rot[n]["used"]
        pool.extend([p]*max(rem,0))
    if not pool:
        pool=[p for p in active_rosters[team] if p["name"] in rot and not rot[p["name"]]["out"]]
    if not pool: pool=active_rosters[team]
    p=random.choice(pool)
    rot[p["name"]]["used"]+=1
    return p

def rnd_teammate(team, active_rosters, exclude=None):
    opts=[p for p in active_rosters[team] if exclude is None or p["name"]!=exclude]
    return random.choice(opts) if opts else None

def check_game_injuries(team, rot, active_rosters):
    hurt=[]
    for p in active_rosters[team]:
        n=p["name"]
        if n not in rot or rot[n]["out"] or rot[n]["used"]==0: continue
        if random.randint(1,1500)<=p.get("injury_risk",10):
            rot[n]["out"]=True
            inj=roll_injury()
            msg,g=apply_injury_to_player(p,inj)
            hurt.append({"player":p["name"],"msg":msg,"inj":inj,"games":g})
    return hurt

# ══════════════════════════════════════════
# SIMULATION CORE — POSSESSIONS WITH FOULS
# ══════════════════════════════════════════
def simulate_possession(off_t, def_t, rot_off, rot_def, active_rosters, gstats, verbose=True):
    """
    Returns (points, message, events_list).
    Physical attributes (height/weight) now influence drive/post/block/reb outcomes.
    Fouls split into: offensive foul (charge), defensive foul, technical, flagrant.
    """
    p  = get_active(off_t, rot_off, active_rosters)
    dp = get_active(def_t, rot_def, active_rosters)
    n, dn = p["name"], dp["name"]

    eff     = get_effective_stats(p)
    def_eff = get_effective_stats(dp)
    shooting  = eff["shooting"]
    offense   = eff["offense"]
    overall   = eff["overall"]
    def_ovr   = def_eff["defense"]
    def_reb   = def_eff.get("rebounding", 75)

    phys    = physical_bonuses(p)
    def_phys= physical_bonuses(dp)

    fatigue = 0
    if rot_off[n]["used"] > 32: fatigue = 6
    if rot_off[n]["used"] > 45: fatigue = 14

    events = []
    pts, msg = 0, ""

    # ── Violations (~1.2% per possession) ──
    if random.random() < 0.012:
        vtype = random.choice(list(VIOL_L.keys()))
        msg   = VIOL_L[vtype].format(n=n)
        if verbose: print(f"  {ORANGE}{msg}{RESET}")
        return 0, msg, events

    # ── Technical foul (~0.8%): other team 1 FT ──
    if random.random() < 0.008:
        msg = _line(TECH_L, n)
        if verbose: print(f"  {ORANGE}{msg}{RESET}")
        pts = 1
        gstats[n]["PTS"] += pts
        events.append(("tech", n))
        return pts, msg, events

    # ── Flagrant foul (~0.15%): player EJECTED, suspension risk ──
    if random.random() < 0.0015:
        msg = random.choice(FLAG_L).format(n=dn, d=n)
        rot_def[dn]["fouls"] = 6    # auto ejection
        rot_def[dn]["out"]   = True
        events.append(("foulout", dn))
        events.append(("flagrant", dn))
        if verbose: print(f"  {msg}")
        # 2 FT + offense keeps ball (simulated as 2 pts here)
        ft_pct = max(0.55, min(0.95, overall / 100))
        pts = sum(1 for _ in range(2) if random.random() < ft_pct)
        gstats[n]["PTS"] += pts
        return pts, msg, events

    # ── Offensive foul / charge (~3%): turnover, OFF player gets foul ──
    if random.random() < 0.03:
        msg = random.choice(OFF_FOUL_L).format(n=n, d=dn)
        rot_off[n]["fouls"] += 1
        events.append(("off_foul", n, rot_off[n]["fouls"]))
        if rot_off[n]["fouls"] >= 6:
            rot_off[n]["out"] = True
            events.append(("foulout", n))
            msg += f"  {RED}— {n} FOULS OUT! ({rot_off[n]['fouls']} fouls){RESET}"
        if verbose: print(f"  {ORANGE}{msg}{RESET}")
        return 0, msg, events

    # ── Defensive foul (~8-10%): shooter goes to the line ──
    def_foul_chance = 0.085 + max(0, (offense - def_ovr) * 0.002)
    # Physical: driving into a heavy/tall defender is harder → slightly less foul drawn
    def_foul_chance += phys["drive"] * 0.002  # smaller/quicker = draws more fouls driving
    if random.random() < def_foul_chance:
        rot_def[dn]["fouls"] += 1
        foul_msg = random.choice(DEF_FOUL_L).format(n=n, d=dn)
        events.append(("def_foul", dn, rot_def[dn]["fouls"]))
        if rot_def[dn]["fouls"] >= 6:
            rot_def[dn]["out"] = True
            events.append(("foulout", dn))
            foul_msg += f"  {RED}— {dn} FOULS OUT! ({rot_def[dn]['fouls']} fouls){RESET}"
        ft_pct = max(0.55, min(0.95, overall / 100))
        made   = sum(1 for _ in range(2) if random.random() < ft_pct)
        pts    = made
        gstats[n]["PTS"] += pts
        full_msg = f"{ORANGE}{foul_msg}  (+{pts} FT){RESET}"
        if verbose: print(f"  {color_team_abbr(off_t)}  {full_msg}")
        return pts, full_msg, events

    # ── Archetype bonuses ──
    _, arch_b = get_archetype(p)
    _, def_arch_b = get_archetype(dp)

    quarter = _gctx.get("quarter", 1)
    s       = _gctx.get("score", {})

    # ── Home court + crowd + play style + gameplay enhancements ──
    home_t = _gctx.get("home")
    crowd = crowd_intensity(home_t, s, _gctx.get("t1"), _gctx.get("t2"), gm_records)
    home_boost = home_court_boost(home_t, def_t if off_t == home_t else off_t,
                                  gm_records, crowd) if off_t == home_t else 0.0
    if off_t != home_t:
        def_style = _gctx.get("style_mods", {}).get(def_t, {})
        home_boost -= def_style.get("defense", 0) * 0.5

    off_style = _gctx.get("style_mods", {}).get(off_t, {})
    style_two = off_style.get("two", 0)
    style_three = off_style.get("three", 0)
    style_ft = off_style.get("ft", 0)

    mins_used = rot_off[n]["used"]
    fatigue_carry = fatigue_penalty(n)
    vet_boost = veteran_leadership_bonus(off_t, active_rosters)
    rook_boost = rookie_minutes_bonus(p, mins_used)
    brk_boost = breakout_boost(n)
    chem_boost = chemistry_boost(off_t)
    gp_boost = vet_boost + rook_boost + brk_boost + chem_boost + fatigue_carry

    # Gameplay manager boosts (clutch, streaks, momentum, chemistry)
    time_rem = max(0, (_gctx.get("poss_total_q", 35) - _gctx.get("poss_in_q", 0)) * 20)
    score_diff_off = s.get(off_t, 0) - s.get(def_t, 0)
    gp_mods = gameplay_manager.get_player_boost(
        p, off_t, quarter, time_rem, score_diff_off,
    )
    gp_boost += gp_mods.get("total", 0) * 0.001

    if crowd >= 0.85 and quarter >= 4 and verbose:
        if random.random() < 0.04:
            print(f"  {YELLOW}{BOLD}📣 CROWD IS ELECTRIC — {color_team_abbr(home_t)} feed off the energy!{RESET}")

    # ── Coaching bonuses ──
    coach_off  = coach_offense_bonus(off_t)
    coach_def  = coach_defense_bonus(def_t) * 0.001   # converted to probability scale

    # ── Hot/Cold streak effect on shooting ──
    streak_sht_mod = 0.0
    streak_tag     = ""
    if n in _gctx.get("hot",  set()):
        streak_sht_mod =  0.06
        streak_tag     = f"  {YELLOW}🔥 HOT{RESET}"
    elif n in _gctx.get("cold", set()):
        streak_sht_mod = -0.06
        streak_tag     = f"  {CYAN}🥶 COLD{RESET}"

    # ── Clutch modifier (Q4 or OT, score within 8) ──
    clutch_mod = 0.0
    if quarter >= 4:
        score_diff = abs(s.get(off_t, 0) - s.get(def_t, 0))
        if score_diff <= 8:
            clutch = p.get("clutch", 70)
            clutch_mod = (clutch - 70) * 0.001   # max ±0.029
            conf = p.get("confidence", 75)
            clutch_mod += (conf - 75) * 0.0008

    # ── Regular possession probabilities ──
    base_two   = 0.44 + (offense - 70) * 0.003
    base_three = 0.14 + max(0, (shooting - 72) * 0.003)

    phys_two_boost = (phys["drive"] + phys["post"]) * 0.003
    phys_blk_pen   = def_phys["block"] * 0.002
    def_boost      = def_arch_b.get("def_boost", 0) * 0.003

    # Archetype scoring bonuses
    arch_two_b   = arch_b.get("two",   0) + arch_b.get("drive", 0) + arch_b.get("post", 0)
    arch_three_b = arch_b.get("three", 0)

    two_pct   = max(0.12, min(0.58,
        base_two + phys_two_boost - phys_blk_pen - fatigue*0.001
        + arch_two_b + streak_sht_mod * 0.5 + clutch_mod - def_boost
        + home_boost + coach_off - coach_def
        + style_two + gp_boost))
    three_pct = max(0.04, min(0.30,
        base_three + arch_three_b + streak_sht_mod + clutch_mod
        + home_boost * 0.5 + coach_off + style_three + gp_boost))
    ft_pct    = max(0.04, min(0.12, 0.07 + arch_b.get("ft", 0) + style_ft))
    miss_pct  = max(0.06, 0.14 - phys_two_boost * 0.5 - arch_two_b * 0.3)

    # Momentum bonus — team on a run gets a small boost
    mom = _gctx.get("momentum", {}).get(off_t, 0)
    if mom >= 6:
        two_pct   = min(0.60, two_pct   + 0.015)
        three_pct = min(0.32, three_pct + 0.010)

    def _pick_two_line():
        if phys["drive"] >= phys["post"]: return random.choice(DRIVE_L).format(n=n)
        if phys["post"]  >= 4:            return random.choice(POST_L).format(n=n)
        return random.choice(MID_L).format(n=n)

    roll = random.random()
    if roll < two_pct:
        pts  = 2
        made = True
        msg  = _pick_two_line() + f"  (+2){streak_tag}"
        gstats[n]["PTS"] += 2
        tm = rnd_teammate(off_t, active_rosters, n)
        if tm and random.random() < 0.52 + arch_b.get("ast", 0):
            gstats[tm["name"]]["AST"] += 1

    elif roll < two_pct + three_pct:
        pts  = 3
        made = True
        msg  = random.choice(THREE_L).format(n=n) + f"  (+3){streak_tag}"
        gstats[n]["PTS"] += 3
        tm = rnd_teammate(off_t, active_rosters, n)
        if tm and random.random() < 0.48 + arch_b.get("ast", 0):
            gstats[tm["name"]]["AST"] += 1

    elif roll < two_pct + three_pct + ft_pct:
        pts  = 1
        made = True
        msg  = random.choice(FT_L).format(n=n) + "  (+1)"
        gstats[n]["PTS"] += 1

    elif roll < two_pct + three_pct + ft_pct + miss_pct:
        made = False
        msg  = random.choice(MISS_L).format(n=n) + (f"  {streak_tag}" if streak_tag else "")
        rb   = rnd_teammate(off_t, active_rosters, n)
        if rb: gstats[rb["name"]]["REB"] += 1
        blk_chance = max(0.02, 0.10 + def_phys["block"] * 0.010 + def_arch_b.get("block", 0))
        if random.random() < blk_chance: gstats[dn]["BLK"] += 1

    else:
        made = False
        msg  = random.choice(TO_L).format(n=n)
        steal_chance = 0.42 + def_arch_b.get("steal", 0)
        if random.random() < steal_chance: gstats[dn]["STL"] += 1

    # ── Update hot/cold streak + gameplay streaks ──
    streak_event = _update_shot_hist(n, made) if pts in (2, 3) or not made else None
    if pts in (2, 3) or not made:
        gameplay_manager.record_shot(n, off_t, made, pts if made else 0)
    if streak_event == "hot" and verbose:
        print(f"  {YELLOW}{BOLD}🔥 {n} IS ON FIRE! 3 makes in a row!{RESET}")
    elif streak_event == "cold" and verbose:
        print(f"  {CYAN}🥶 {n} can't buy a bucket — on a cold streak.{RESET}")
    if brk_boost > 0 and pts >= 2 and verbose and random.random() < 0.15:
        print(f"  {MAGENTA}{BOLD}💥 BREAKOUT GAME: {n} is having a night!{RESET}")

    # Buzzer-beater check on late Q4 scoring
    if pts >= 2 and made:
        try_buzzer_beater(
            quarter, _gctx.get("poss_in_q", 0), _gctx.get("poss_total_q", 35),
            s, off_t, def_t, active_rosters, n, verbose,
        )

    # ── Update momentum (score is updated by simulate_game — do not double-count here) ──
    other_t = def_t
    if pts > 0:
        _update_momentum(off_t, pts, other_t, verbose)

    return pts, msg, events

# ══════════════════════════════════════════
# GAME SIMULATOR
# ══════════════════════════════════════════
POSSESSIONS_PER_QUARTER = 35   # ~100 possessions per team per game (NBA average)
OT_POSSESSIONS = 14

def simulate_game(t1, t2, active_rosters, verbose=True, silent=False, home_team=None):
    _gctx_reset(t1, t2, verbose and not silent)
    # Store home team in context (t1 is home by default unless specified)
    _gctx["home"] = home_team if home_team else t1
    rot1=assign_minutes(t1,active_rosters)
    rot2=assign_minutes(t2,active_rosters)
    gstats={}
    for tm in [t1,t2]:
        for p in active_rosters[tm]:
            gstats[p["name"]]={"PTS":0,"REB":0,"AST":0,"STL":0,"BLK":0}

    if verbose and not silent:
        # Show archetypes of top starters
        def _starters(tm):
            pl = sorted(active_rosters[tm], key=lambda x:x.get("overall",0), reverse=True)[:2]
            return " · ".join(f"{p['name']} ({p.get('archetype','?')})" for p in pl)
        print(f"\n{'═'*56}")
        print(f"{BOLD}  {color_team_name(t1)}  {WHITE}vs{RESET}  {color_team_name(t2)}{RESET}")
        print(f"  {DIM}{_starters(t1)}{RESET}")
        print(f"  {DIM}{_starters(t2)}{RESET}")
        print(f"{'═'*56}")

    score={t1:0,t2:0}; qscores={t1:[],t2:[]}; inj_events=[]; offense=t1

    for quarter in range(1,5):
        _gctx["quarter"] = quarter
        _gctx["score"]   = score
        if verbose and not silent:
            print(f"\n{BOLD}{CYAN}  ── Q{quarter} ──{RESET}  "
                  f"{color_team_abbr(t1)} {score[t1]} — {score[t2]} {color_team_abbr(t2)}\n  {'─'*48}")
        qs1,qs2=score[t1],score[t2]
        for _ in range(POSSESSIONS_PER_QUARTER):
            v = verbose and not silent
            if offense==t1:
                pts,msg,ev=simulate_possession(t1,t2,rot1,rot2,active_rosters,gstats,v)
            else:
                pts,msg,ev=simulate_possession(t2,t1,rot2,rot1,active_rosters,gstats,v)
            score[offense]+=pts
            if v and not any(x[0] in ("foul","tech","flagrant","off_foul") for x in ev):
                print(f"  {color_team_abbr(offense)}  {msg}")
            offense=t2 if offense==t1 else t1
        for tm,rot in [(t1,rot1),(t2,rot2)]:
            for ev in check_game_injuries(tm,rot,active_rosters):
                inj=ev["inj"]
                if verbose and not silent:
                    print(f"\n  {inj['col']}{ev['msg']}{RESET}")
                inj_events.append(ev)
        qscores[t1].append(score[t1]-qs1)
        qscores[t2].append(score[t2]-qs2)

    # Overtime
    ot=1
    while score[t1]==score[t2]:
        _gctx["quarter"] = 4 + ot
        if verbose and not silent: print(f"\n{YELLOW}{BOLD}  🔥 OVERTIME {ot}!{RESET}")
        ots1,ots2=score[t1],score[t2]
        for _ in range(OT_POSSESSIONS):
            v = verbose and not silent
            if offense==t1:
                pts,msg,ev=simulate_possession(t1,t2,rot1,rot2,active_rosters,gstats,v)
            else:
                pts,msg,ev=simulate_possession(t2,t1,rot2,rot1,active_rosters,gstats,v)
            score[offense]+=pts
            if v: print(f"  {color_team_abbr(offense)}  {msg}")
            offense=t2 if offense==t1 else t1
        qscores[t1].append(score[t1]-ots1); qscores[t2].append(score[t2]-ots2); ot+=1

    winner=t1 if score[t1]>score[t2] else t2
    loser =t2 if winner==t1 else t1
    if verbose and not silent:
        _boxscore(t1,t2,score,qscores,gstats,active_rosters,inj_events,rot1,rot2)
    if silent:
        wc=GREEN; lc=RED
        print(f"  {color_team_abbr(t1)} {wc if winner==t1 else lc}{score[t1]:>3}{RESET}"
              f"  —  {color_team_abbr(t2)} {wc if winner==t2 else lc}{score[t2]:>3}{RESET}")
    return {"winner":winner,"loser":loser,"score":score,"game_stats":gstats}

def _boxscore(t1,t2,score,qscores,gstats,active_rosters,inj_events,rot1,rot2):
    print(f"\n{'═'*56}\n{BOLD}{WHITE}  📊 FINAL BOX SCORE{RESET}\n{'═'*56}")
    nq=len(qscores[t1])
    hdr=f"  {'TEAM':<6}"
    for i in range(nq): hdr+= f"  {'Q'+str(i+1) if i<4 else 'OT'+str(i-3):>4}"
    hdr+=f"  {'TOT':>5}"
    print(hdr); print(f"  {'─'*50}")
    for tm in [t1,t2]:
        row=f"  {color_team_abbr(tm):<6}"
        for q in qscores[tm]: row+=f"  {q:>4}"
        c=GREEN if score[tm]>score[(t2 if tm==t1 else t1)] else RED
        row+=f"  {c}{BOLD}{score[tm]:>5}{RESET}"
        print(row)

    # Foul counts
    print(f"\n  {ORANGE}Foul Leaders:{RESET}")
    for tm,rot in [(t1,rot1),(t2,rot2)]:
        for n,info in rot.items():
            if info["fouls"]>0:
                fo=" ❌FOULED OUT" if info["out"] and info["fouls"]>=6 else ""
                print(f"    {n:<24} {info['fouls']} fouls{fo}")

    print(f"\n{BOLD}{WHITE}  📋 PLAYER STATS{RESET}\n  {'─'*54}")
    print(f"  {'PLAYER':<24} {CYAN}PTS{RESET} {GREEN}REB{RESET} {YELLOW}AST{RESET} {ORANGE}STL{RESET} {MAGENTA}BLK{RESET}")
    print(f"  {'─'*54}")
    for tm in [t1,t2]:
        print(f"\n  {color_team_name(tm)}")
        for p in sorted(active_rosters[tm],key=lambda x:gstats[x["name"]]["PTS"],reverse=True):
            s=gstats[p["name"]]
            if any(v>0 for v in s.values()):
                inj_note=""
                ai=p.get("active_injury")
                if ai: inj_note=f"  {ai['col'] if isinstance(ai.get('col'),str) else RED}⚕ {ai['name']}{RESET}"
                print(f"  {p['name']:<24}"
                      f" {CYAN}{s['PTS']:>3}{RESET} {GREEN}{s['REB']:>3}{RESET}"
                      f" {YELLOW}{s['AST']:>3}{RESET} {ORANGE}{s['STL']:>3}{RESET}"
                      f" {MAGENTA}{s['BLK']:>3}{RESET}{inj_note}")

    if inj_events:
        print(f"\n  {RED}🚑 INJURY REPORT{RESET}")
        for ev in inj_events:
            sev=ev["inj"]["sev"]
            c=(RED if sev in ("severe","serious","career") else ORANGE if sev=="mild" else YELLOW)
            gl=ev.get("games",0)
            gl_str=f"  ({gl} games)" if gl>0 else ""
            print(f"  {c}  {ev['inj']['name']:<20} {ev['player']}{gl_str}{RESET}")

    winner=t1 if score[t1]>score[t2] else t2
    loser =t2 if winner==t1 else t1

    # ── Game MVP ──
    mvp_name = max(gstats, key=lambda n: (
        gstats[n]["PTS"]*1.2 + gstats[n]["REB"]*0.5 +
        gstats[n]["AST"]*0.7 + gstats[n]["STL"]*1.2 + gstats[n]["BLK"]*1.0
    ))
    mvp_s = gstats[mvp_name]
    print(f"\n  {YELLOW}{BOLD}⭐ GAME MVP: {mvp_name}{RESET}"
          f"  {CYAN}{mvp_s['PTS']}pts{RESET}"
          f"  {GREEN}{mvp_s['REB']}reb{RESET}"
          f"  {YELLOW}{mvp_s['AST']}ast{RESET}")

    print(f"\n{'═'*56}")
    print(f"  🏆 {BOLD}{YELLOW}WINNER: {color_team_name(winner)}{RESET}"
          f"  {GREEN}{score[winner]}{RESET} – {RED}{score[loser]}{RESET}")
    print(f"{'═'*56}\n")

# ══════════════════════════════════════════
# INTERACTIVE QUICK-PLAY MODE
# ══════════════════════════════════════════
def quick_play_mode(active_rosters):
    print(f"\n{'═'*54}")
    print(f"{BOLD}{CYAN}  🎮 INTERACTIVE QUICK-PLAY{RESET}")
    print(f"{'═'*54}")
    print("  YOU control 5 possessions per quarter. Opponent is auto-simulated.")

    # Pick teams
    avail={t:None for t in active_rosters}
    user_team = team_selector(1, avail)
    cpu_team  = team_selector(2, {t:None for t in avail})

    # Pick user's star player for narrative focus
    user_roster = sorted(active_rosters[user_team], key=lambda p:p.get("overall",0), reverse=True)
    print(f"\n  {BOLD}Pick YOUR go-to player:{RESET}")
    for i,p in enumerate(user_roster[:10], 1):
        c=GREEN if p.get("overall",0)>=88 else ORANGE if p.get("overall",0)>=80 else WHITE
        print(f"    {i:>2}. {c}{p['name']:<24}{RESET} {p['pos']:>3}  OVR:{p.get('overall','?')}")
    while True:
        c=input("  > ").strip()
        if c.isdigit() and 1<=int(c)<=min(10,len(user_roster)):
            hero=user_roster[int(c)-1]; break
        print(RED+"  Invalid."+RESET)

    score={user_team:0, cpu_team:0}
    qscores={user_team:[], cpu_team:[]}
    gstats={}
    for tm in [user_team, cpu_team]:
        for p in active_rosters[tm]:
            gstats[p["name"]]={"PTS":0,"REB":0,"AST":0,"STL":0,"BLK":0}

    rot_u=assign_minutes(user_team, active_rosters)
    rot_c=assign_minutes(cpu_team,  active_rosters)
    hero_fouls=0

    # Physical bonuses for hero
    hero_phys = physical_bonuses(hero)
    sht_bonus = (hero.get("shooting", 75) - 75) / 200
    off_bonus = (hero.get("offense",  75) - 75) / 200
    drv_bonus = hero_phys["drive"] / 100   # max ±0.15
    pst_bonus = hero_phys["post"]  / 100

    # Build action table with labels that hint at physical fit
    drv_tag = f"{GREEN}(your size helps){RESET}" if hero_phys["drive"] >= 4 else \
              f"{RED}(tough for your frame){RESET}" if hero_phys["drive"] <= -4 else ""
    pst_tag = f"{GREEN}(your size helps){RESET}" if hero_phys["post"] >= 4 else \
              f"{RED}(tough for your frame){RESET}" if hero_phys["post"] <= -4 else ""

    ACTIONS = [
        (f"Drive to the basket 🏀  {drv_tag}", "drive",
         {"two": max(0.30, 0.55 + drv_bonus + off_bonus),
          "three": 0.00,
          "ft":   max(0.08, 0.18 + drv_bonus),
          "miss": max(0.10, 0.27 - drv_bonus - off_bonus)}),
        ("Pull-up mid-range 🎯",  "mid",
         {"two": max(0.25, 0.46 + off_bonus * 0.5),
          "three": 0.00, "ft": 0.09,
          "miss": max(0.20, 0.45 - off_bonus * 0.5)}),
        ("Step-back THREE 🔥",    "three",
         {"two": 0.00,
          "three": max(0.22, 0.50 + sht_bonus * 2),
          "ft": 0.04,
          "miss": max(0.18, 0.46 - sht_bonus * 2)}),
        (f"Post up & score 💪  {pst_tag}", "post",
         {"two": max(0.28, 0.52 + pst_bonus + off_bonus),
          "three": 0.00,
          "ft":   max(0.10, 0.20 + pst_bonus),
          "miss": max(0.10, 0.28 - pst_bonus - off_bonus)}),
        ("Pass — find the open man 🎯", "pass",
         {"two": 0.48, "three": 0.24, "ft": 0.04, "miss": 0.24}),
    ]

    for quarter in range(1, 5):
        print(f"\n{'═'*58}")
        print(f"{BOLD}{CYAN}  Q{quarter}{RESET}  │  "
              f"{color_team_name(user_team)} {GREEN}{score[user_team]}{RESET}"
              f"  —  {RED}{score[cpu_team]}{RESET} {color_team_name(cpu_team)}")
        print(f"{'═'*58}")

        qu_start_u = score[user_team]
        qu_start_c = score[cpu_team]

        for poss in range(1, 6):
            print(f"\n  {BOLD}Your possession {poss}/5{RESET}  │  "
                  f"{color_team_abbr(user_team)} {GREEN}{score[user_team]}{RESET}"
                  f" — {RED}{score[cpu_team]}{RESET} {color_team_abbr(cpu_team)}")
            # Hero info line with physical profile
            h_ht   = hero.get("height","?")
            h_wt   = hero.get("weight","?")
            h_phys = phys_label(hero)
            print(f"  Hero: {YELLOW}{hero['name']}{RESET}  "
                  f"({hero.get('pos','?')}, OVR {hero.get('overall','?')}, "
                  f"{h_ht} / {h_wt}lbs)  {h_phys}")
            if hero_fouls > 0:
                fc = RED if hero_fouls >= 5 else ORANGE
                print(f"  {fc}⚠  Foul trouble: {hero_fouls}/6{RESET}")
            print()
            for i, (label, atype, _probs) in enumerate(ACTIONS, 1):
                print(f"    {CYAN}{i}.{RESET} {label}")

            while True:
                c = input("  > ").strip()
                if c.isdigit() and 1 <= int(c) <= len(ACTIONS):
                    _, atype, probs = ACTIONS[int(c) - 1]; break
                print(RED + "  Invalid." + RESET)

            adj = dict(probs)

            # ── Offensive foul/charge risk on drives ──
            if atype == "drive" and random.random() < 0.07:
                hero_fouls += 1
                msg_of = random.choice(OFF_FOUL_L).format(n=hero["name"], d="the defender")
                print(f"  {ORANGE}{msg_of}{RESET}")
                if hero_fouls >= 6:
                    print(f"  {RED}{BOLD}{hero['name']} FOULS OUT! ({hero_fouls} fouls){RESET}")
                # CPU still gets a possession
                cpu_pts, cpu_msg, _ = simulate_possession(
                    cpu_team, user_team, rot_c, rot_u, active_rosters, gstats, verbose=False)
                score[cpu_team] += cpu_pts
                print(f"  {DIM}  ↩ CPU: {cpu_msg}{RESET}")
                continue

            # ── Defensive foul drawn ──
            def_foul_drawn = False
            if atype in ("drive", "post") and random.random() < (0.14 + drv_bonus if atype == "drive" else 0.14 + pst_bonus):
                def_foul_drawn = True

            roll = random.random(); cum = 0.0; result = None
            for outcome, chance in adj.items():
                cum += chance
                if roll < cum: result = outcome; break
            if not result: result = "miss"

            if result == "two":
                pts = 2
                score[user_team] += pts
                gstats[hero["name"]]["PTS"] += pts
                tm = rnd_teammate(user_team, active_rosters, hero["name"])
                if atype == "pass" and tm: gstats[tm["name"]]["AST"] += 1
                line = (random.choice(DRIVE_L).format(n=hero["name"]) if atype == "drive" else
                        random.choice(POST_L).format(n=hero["name"])  if atype == "post"  else
                        random.choice(MID_L).format(n=hero["name"]))
                extra = f"  {ORANGE}And-one!{RESET}" if def_foul_drawn else ""
                if def_foul_drawn:
                    score[user_team] += 1
                    gstats[hero["name"]]["PTS"] += 1
                    pts += 1
                print(f"  {GREEN}{BOLD}✅ {line}  (+{pts}){extra}{RESET}")

            elif result == "three":
                pts = 3
                score[user_team] += pts
                gstats[hero["name"]]["PTS"] += pts
                print(f"  {YELLOW}{BOLD}🔥 {random.choice(THREE_L).format(n=hero['name'])}  (+3){RESET}")

            elif result == "ft":
                ft_rate = max(0.60, min(0.98, hero.get("shooting", 75) / 100 + 0.25))
                pts = sum(1 for _ in range(2) if random.random() < ft_rate)
                score[user_team] += pts
                gstats[hero["name"]]["PTS"] += pts
                print(f"  {CYAN}{hero['name']} to the line — makes {pts}/2  (+{pts}){RESET}")

            else:
                print(f"  {RED}{random.choice(MISS_L).format(n=hero['name'])}{RESET}")
                rb = rnd_teammate(user_team, active_rosters, hero["name"])
                if rb: gstats[rb["name"]]["REB"] += 1

            # CPU possession after each of yours
            cpu_pts, cpu_msg, _ = simulate_possession(
                cpu_team, user_team, rot_c, rot_u, active_rosters, gstats, verbose=False)
            score[cpu_team] += cpu_pts
            print(f"  {DIM}  ↩ CPU: {cpu_msg}{RESET}")

        qscores[user_team].append(score[user_team]-qu_start_u)
        qscores[cpu_team].append(score[cpu_team]-qu_start_c)
        print(f"\n  End of Q{quarter}:  "
              f"{color_team_abbr(user_team)} {GREEN}{score[user_team]}{RESET}"
              f"  —  {RED}{score[cpu_team]}{RESET} {color_team_abbr(cpu_team)}")

    # Final
    print(f"\n{'═'*54}")
    if score[user_team]>score[cpu_team]:
        print(f"{BOLD}{YELLOW}  🏆 YOU WIN!  {color_team_name(user_team)} {score[user_team]} – {score[cpu_team]}{RESET}")
    elif score[cpu_team]>score[user_team]:
        print(f"{BOLD}{RED}  ❌ YOU LOSE.  {score[user_team]} – {score[cpu_team]} {color_team_name(cpu_team)}{RESET}")
    else:
        print(f"{BOLD}{CYAN}  🤝 TIE GAME!{RESET}")
    print(f"  {hero['name']}: {gstats[hero['name']]['PTS']} PTS")
    print(f"{'═'*54}")

# ══════════════════════════════════════════
# STANDINGS
# ══════════════════════════════════════════
def _pad_col(colored, plain, w):
    return colored + " "*(max(0, w-len(plain)))

def show_standings(teams_list=None):
    if not gm_records: print(RED+"No season data yet."+RESET); return
    tl=teams_list or list(gm_records.keys())
    ranked=sorted(tl,key=lambda t:(gm_records[t]["W"],gm_records[t]["PF"]),reverse=True)
    east=[t for t in ranked if t in EAST]
    west=[t for t in ranked if t in WEST]
    other=[t for t in ranked if t not in EAST and t not in WEST]
    W=58
    print(f"\n{'═'*W}\n{BOLD}{YELLOW}  🏆 STANDINGS  —  Season {gm_season}{RESET}\n{'═'*W}")
    hdr=(f"        TEAM   {GREEN}{'W':>4}{RESET}  {RED}{'L':>4}{RESET}"
         f"   PCT   {'PF':>5}   {'PA':>5}   DIFF")
    for conf_label,conf_list in [("EASTERN",east),("WESTERN",west),("",other)]:
        if not conf_list: continue
        if conf_label:
            cc=LBLUE if conf_label=="EASTERN" else ORANGE
            print(f"\n  {cc}{BOLD}── {conf_label} CONFERENCE ──{RESET}")
            print(f"  {hdr}\n  {'─'*(W-2)}")
        for rank,t in enumerate(conf_list,1):
            r=gm_records[t]; g=r["W"]+r["L"]
            pct=r["W"]/g if g else 0.0
            diff=r["PF"]-r["PA"]
            ds=(f"{GREEN}+{diff}{RESET}" if diff>=0 else f"{RED}{diff}{RESET}")
            ap=team_abbr(t); ac=color_team_abbr(t)
            if rank==9:
                print(f"  {DIM}  ── playoff line ──────────────────────────────────{RESET}")
            star=f"{YELLOW}★{RESET}" if t==gm_team else " "
            medal=("🥇" if rank==1 else "🥈" if rank==2 else
                   "🥉" if rank==3 else f"{rank:>2}.")
            sc=(GREEN if rank<=3 else CYAN if rank<=6 else ORANGE if rank<=8 else DIM)
            pa=_pad_col(f"{sc}{ac}{RESET}",ap,4)
            print(f"  {medal} {star}{pa}  "
                  f"{GREEN}{r['W']:>4}{RESET}  {RED}{r['L']:>4}{RESET}  "
                  f"{WHITE}{pct:.3f}{RESET}  {r['PF']:>5}  {r['PA']:>5}  {ds}")

def show_awards(active_rosters):
    """
    Calculate and display end-of-season awards based on accumulated stats.
    Uses gm_season_stats (per-game averages) + player OVR for context.
    """
    if not gm_season_stats: return
    print(f"\n{'═'*58}")
    print(f"{BOLD}{YELLOW}  🏆 END-OF-SEASON AWARDS  —  Season {gm_season}{RESET}")
    print(f"{'═'*58}")

    # Build lookup: player_name → player_dict (for OVR, age, archetype, etc.)
    player_map = {}
    team_map   = {}
    for tm, pls in active_rosters.items():
        for p in pls:
            player_map[p["name"]] = p
            team_map[p["name"]]   = tm

    # Helper: per-game average
    def avg(n, stat): 
        s = gm_season_stats.get(n, {}); gp = max(1, s.get("GP", 1))
        return s.get(stat, 0) / gp

    # Filter to players with meaningful games
    qualified = [n for n, s in gm_season_stats.items() if s.get("GP", 0) >= 20]

    def _award(label, emoji, candidates, key_fn, color=YELLOW):
        best = max(candidates, key=key_fn, default=None)
        if not best: return
        p    = player_map.get(best)
        team = team_map.get(best, "?")
        kval = key_fn(best)
        arc  = p.get("archetype","?") if p else "?"
        print(f"\n  {color}{BOLD}{emoji} {label}{RESET}")
        print(f"     {BOLD}{best}{RESET}  ·  {color_team_abbr(team)}  ·  {arc}")
        if p: print(f"     OVR {p.get('overall','?')}  |  {avg(best,'PTS'):.1f} PPG  "
                    f"{avg(best,'REB'):.1f} RPG  {avg(best,'AST'):.1f} APG  "
                    f"{avg(best,'STL'):.1f} SPG  {avg(best,'BLK'):.1f} BPG")

    # ── MVP: PTS/game + AST/game weighted, favors team that won more ──
    def mvp_score(n):
        p   = player_map.get(n)
        ovr = p.get("overall", 75) if p else 75
        tm  = team_map.get(n, "")
        w   = gm_records.get(tm, {}).get("W", 0)
        return avg(n,"PTS")*1.2 + avg(n,"AST")*0.8 + avg(n,"REB")*0.4 + w*0.05 + ovr*0.02
    _award("Most Valuable Player (MVP)", "🏅", qualified, mvp_score, YELLOW)

    # ── DPOY: DEF rating + STL + BLK ──
    def dpoy_score(n):
        p = player_map.get(n); dfn = p.get("defense", 75) if p else 75
        return dfn*0.5 + avg(n,"STL")*5 + avg(n,"BLK")*4
    _award("Defensive Player of the Year", "🛡️", qualified, dpoy_score, CYAN)

    # ── ROY: best stats among age ≤ 23 ──
    rookies = [n for n in qualified if player_map.get(n,{}).get("age",30) <= 23]
    if rookies:
        def roy_score(n): return avg(n,"PTS")*1.2 + avg(n,"AST")*0.6 + avg(n,"REB")*0.4
        _award("Rookie of the Year", "🌟", rookies, roy_score, GREEN)

    # ── MIP: high-confidence players who scored a lot (proxy for improvement) ──
    def mip_score(n):
        p = player_map.get(n)
        conf = p.get("confidence", 75) if p else 75
        return avg(n,"PTS") + conf * 0.05
    non_stars = [n for n in qualified if player_map.get(n,{}).get("overall",0) < 87]
    if non_stars:
        _award("Most Improved Player", "📈", non_stars, mip_score, ORANGE)

    # ── Sixth Man: high scorer NOT in top-5 OVR on their team ──
    bench_players = []
    for tm, pls in active_rosters.items():
        top5 = sorted(pls, key=lambda x: x.get("overall",0), reverse=True)[:5]
        top5_names = {p["name"] for p in top5}
        for p in pls:
            if p["name"] in qualified and p["name"] not in top5_names:
                bench_players.append(p["name"])
    if bench_players:
        _award("Sixth Man of the Year", "💼", bench_players, lambda n: avg(n,"PTS"), MAGENTA)

    # ── All-NBA First Team (5 best by MVP score) ──
    print(f"\n  {BOLD}{YELLOW}📋 ALL-NBA FIRST TEAM{RESET}")
    all_nba = sorted(qualified, key=mvp_score, reverse=True)[:5]
    for rank, n in enumerate(all_nba, 1):
        p = player_map.get(n); tm = team_map.get(n,"")
        arc = p.get("archetype","?") if p else "?"
        print(f"    {rank}. {BOLD}{n}{RESET}  {color_team_abbr(tm)}  {DIM}{arc}{RESET}"
              f"  {avg(n,'PTS'):.1f}/{avg(n,'REB'):.1f}/{avg(n,'AST'):.1f}")

    # ── All-Defense Team (5 best by DPOY score) ──
    print(f"\n  {BOLD}{CYAN}📋 ALL-DEFENSE FIRST TEAM{RESET}")
    all_def = sorted(qualified, key=dpoy_score, reverse=True)[:5]
    for rank, n in enumerate(all_def, 1):
        p = player_map.get(n); tm = team_map.get(n,"")
        arc = p.get("archetype","?") if p else "?"
        print(f"    {rank}. {BOLD}{n}{RESET}  {color_team_abbr(tm)}  {DIM}{arc}{RESET}")

    print(f"\n{'═'*58}")

def show_season_stats():
    if not gm_season_stats: print(DIM+"No stats yet."+RESET); return
    cats=[("PTS",f"{CYAN}🏀 Points{RESET}"),("REB",f"{GREEN}💪 Rebounds{RESET}"),
          ("AST",f"{YELLOW}🎯 Assists{RESET}"),("STL",f"{ORANGE}💨 Steals{RESET}"),
          ("BLK",f"{MAGENTA}🛡  Blocks{RESET}")]
    print(f"\n{'═'*55}\n{BOLD}{WHITE}  📈 SEASON LEADERBOARD{RESET}\n{'═'*55}")
    for cat,label in cats:
        leaders=sorted([(p,s) for p,s in gm_season_stats.items() if s["GP"]>0],
                       key=lambda x:x[1][cat]/x[1]["GP"],reverse=True)[:5]
        print(f"\n  {BOLD}{label} (per game){RESET}\n  {'─'*38}")
        for i,(pn,s) in enumerate(leaders,1):
            avg=s[cat]/s["GP"]
            bar="█"*int(avg/40*18 if cat=="PTS" else avg/15*18)
            print(f"  {i}. {pn:<24} {WHITE}{avg:>5.1f}{RESET}  {DIM}{bar[:18]}{RESET}  ({s['GP']} GP)")

# ══════════════════════════════════════════
# PLAYOFFS
# ══════════════════════════════════════════
def _series(t1,t2,active_rosters,needed=4):
    wins={t1:0,t2:0}; gn=0
    while wins[t1]<needed and wins[t2]<needed:
        gn+=1
        home=t1 if gn in(1,2,5,7) else t2
        away=t2 if home==t1 else t1
        r=simulate_game(home,away,active_rosters,verbose=False,silent=False)
        wins[r["winner"]]+=1
        add_to_season_stats(r["game_stats"])
        wt=r["winner"]; lt=t2 if wt==t1 else t1
        lc=GREEN if wins[wt]>wins[lt] else WHITE
        print(f"    Game {gn}:  {color_team_abbr(wt)} {lc}wins{RESET}  "
              f"({GREEN}{wins[t1]}{RESET}–{RED}{wins[t2]}{RESET})")
    w=t1 if wins[t1]==needed else t2; l=t2 if w==t1 else t1
    print(f"  {GREEN}{BOLD}  → {color_team_name(w)} wins {wins[w]}–{wins[l]}{RESET}")
    return w

def run_playoffs(active_rosters):
    print(f"\n{'═'*56}\n{BOLD}{YELLOW}  🏆 PLAYOFFS — Season {gm_season}{RESET}\n{'═'*56}")
    tl=list(gm_records.keys())
    def seed(conf):
        m=[t for t in tl if t in conf and t in gm_records]
        return sorted(m,key=lambda t:(gm_records[t]["W"],gm_records[t]["PF"]),reverse=True)[:8]
    es=seed(EAST); ws=seed(WEST)
    if len(es)<4 or len(ws)<4:
        all_s=sorted(tl,key=lambda t:(gm_records[t]["W"],gm_records[t]["PF"]),reverse=True)[:min(16,len(tl))]
        h=len(all_s)//2; es,ws=all_s[:h],all_s[h:]
    def bracket(seeds,lbl,col):
        print(f"\n  {col}{BOLD}── {lbl} BRACKET ──{RESET}")
        for i,t in enumerate(seeds,1):
            r=gm_records.get(t,{"W":0,"L":0})
            you=f" {YELLOW}★ YOU{RESET}" if t==gm_team else ""
            print(f"  {i}. {color_team_abbr(t):<5} {GREEN}{r['W']}W{RESET}-{RED}{r['L']}L{RESET}{you}")
        cur=seeds[:]; rnames=["First Round","Conference Semifinals","Conference Finals"]; ri=0
        while len(cur)>1:
            print(f"\n  {BOLD}{rnames[min(ri,len(rnames)-1)]}{RESET}")
            nxt=[]
            for i in range(0,len(cur),2):
                if i+1<len(cur):
                    top,bot=cur[i],cur[i+1]
                    print(f"\n  {color_team_abbr(top)} vs {color_team_abbr(bot)}")
                    w=_series(top,bot,active_rosters); nxt.append(w)
                else: nxt.append(cur[i])
            cur=nxt; ri+=1
        return cur[0] if cur else None
    ec=bracket(es,"EASTERN",LBLUE)
    wc=bracket(ws,"WESTERN",ORANGE)
    if ec and wc:
        print(f"\n{'═'*56}\n{BOLD}{YELLOW}  🏆 NBA FINALS{RESET}\n{'═'*56}")
        print(f"\n  {color_team_name(ec)} {DIM}(East){RESET}  vs  {color_team_name(wc)} {DIM}(West){RESET}\n")
        champ=_series(ec,wc,active_rosters)
        print(f"\n{'═'*56}\n{BOLD}{YELLOW}  🏆 CHAMPION: {color_team_name(champ)}{RESET}\n{'═'*56}\n")
        return champ
    return ec or wc

# ══════════════════════════════════════════
# TRADE CENTER  (with value check)
# ══════════════════════════════════════════
def trade_menu(active_rosters):
    print(f"\n{BOLD}{ORANGE}{'╔'*54}{RESET}")
    print(f"{BOLD}{ORANGE}║{RESET}{BOLD}{WHITE}  🔄 TRADE CENTER{RESET}{BOLD}{ORANGE}{' '*35}║{RESET}")
    print(f"{BOLD}{ORANGE}{'╚'*54}{RESET}\n")
    tl=list(active_rosters.keys())
    for i,t in enumerate(tl,1):
        my_pks=get_team_picks(t)
        pk_str=f"  {DIM}[{len(my_pks)} picks]{RESET}" if my_pks else ""
        print(f"  {i:>2}. {color_team_abbr(t):<6} {color_team_name(t)}{pk_str}")
    print("\n  How many teams? (2–4, or 0 to cancel)")
    n_in=input("  > ").strip()
    if n_in=="0": return
    try: num=int(n_in); assert 2<=num<=4
    except: print(RED+"Invalid."+RESET); return
    trade_teams=[]
    for k in range(num):
        raw=input(f"  Team {k+1} #: ").strip()
        try:
            t=tl[int(raw)-1]
            if t not in trade_teams: trade_teams.append(t)
        except: print(RED+"Invalid."+RESET); return

    sends_p={t:[] for t in trade_teams}
    sends_pk={t:[] for t in trade_teams}

    for t in trade_teams:
        print(f"\n  {BOLD}{color_team_name(t)}{RESET}")
        print(f"  {'─'*52}")
        print(f"  {'#':>3}  {'PLAYER':<24} {'OVR':>4}  {'VAL':>5}  POS  INJ")
        print(f"  {'─'*52}")
        for i,p in enumerate(active_rosters[t],1):
            val=player_trade_value(p); vs=trade_value_str(val)
            ai=p.get("active_injury")
            inj_note=(f"  {RED}⚕ {ai['name']}{RESET}" if ai else "")
            c=(GREEN if p.get("overall",0)>=88 else ORANGE if p.get("overall",0)>=80 else WHITE)
            print(f"  {i:>3}. {c}{p['name']:<24}{RESET} "
                  f"{p.get('overall','?'):>4}  {vs}  {p.get('pos','?'):>3}{inj_note}")
        my_pks=get_team_picks(t)
        if my_pks:
            print(f"\n  PICKS:")
            for j,pk in enumerate(my_pks,1):
                c=YELLOW if pk["round"]==1 else CYAN
                print(f"    P{j}. {c}{picks_label(pk)}{RESET}")

        p_raw=input(f"\n  Players to SEND (space-sep #s, or 0): ").strip()
        if p_raw!="0":
            try:
                for idx in p_raw.split():
                    sends_p[t].append(active_rosters[t][int(idx)-1])
            except: print(RED+"  Parse error."+RESET)
        if my_pks:
            pk_raw=input(f"  Picks to SEND (P#s, or 0): ").strip()
            if pk_raw!="0":
                try:
                    for idx in pk_raw.split():
                        sends_pk[t].append(my_pks[int(idx[1:])-1])
                except: print(RED+"  Parse error."+RESET)

    # ── TRADE VALUE CHECK ──
    print(f"\n  {'═'*50}")
    print(f"  {BOLD}TRADE SUMMARY & FAIRNESS CHECK{RESET}")
    print(f"  {'─'*50}")
    side_vals={}
    for t in trade_teams:
        pval=sum(player_trade_value(p) for p in sends_p[t])
        pkval=sum(150 if pk["round"]==1 else 50 for pk in sends_pk[t])
        total=pval+pkval
        side_vals[t]=total
        pnames=", ".join(p["name"] for p in sends_p[t]) or "(no players)"
        pknames="  + "+", ".join(picks_label(pk) for pk in sends_pk[t]) if sends_pk[t] else ""
        vs=trade_value_str(total)
        print(f"  {color_team_abbr(t)} sends: {WHITE}{pnames}{RESET}{pknames}   Value: {vs}")

    # Warn on lopsided trades
    vals=list(side_vals.values())
    if len(vals)>=2:
        max_v=max(vals); min_v=min(vals)
        if min_v>0:
            ratio=max_v/min_v
            if ratio>=3.0:
                winner_t=max(side_vals,key=side_vals.get)
                loser_t=min(side_vals,key=side_vals.get)
                print(f"\n  {RED}{BOLD}⚠️  EXTREMELY LOPSIDED TRADE!{RESET}")
                print(f"  {RED}{color_team_name(winner_t)} wins this trade by {ratio:.1f}x{RESET}")
                print(f"  {RED}This would never happen in real life.{RESET}")
            elif ratio>=2.0:
                print(f"\n  {ORANGE}⚠️  This trade is fairly unbalanced (one side gets {ratio:.1f}x more value).{RESET}")
            elif ratio>=1.4:
                print(f"\n  {YELLOW}This trade is slightly uneven.{RESET}")
            else:
                print(f"\n  {GREEN}✅ Fairly balanced trade.{RESET}")
        elif max_v>0:
            print(f"\n  {RED}⚠️  One side is giving up nothing.{RESET}")

    conf=input("\n  Confirm trade? (y/n): ").strip().lower()
    if conf!="y": print(DIM+"Cancelled."+RESET); return

    # Execute player swaps (round-robin: each team sends to the next)
    for i, send in enumerate(trade_teams):
        recv = trade_teams[(i + 1) % len(trade_teams)]
        for p in sends_p[send]:
            if p in active_rosters[send]:
                active_rosters[send].remove(p)
                active_rosters[recv].append(p)
                print(GREEN+f"  ✅ {p['name']} → {color_team_abbr(recv)}"+RESET)
    sync_contract_manager(active_rosters)
    for i,send in enumerate(trade_teams):
        recv=trade_teams[(i+1)%len(trade_teams)]
        for pk in sends_pk[send]:
            transfer_pick(pk,send,recv)
            c=YELLOW if pk["round"]==1 else CYAN
            print(GREEN+f"  ✅ {c}{picks_label(pk)}{RESET}"+GREEN+f" → {color_team_abbr(recv)}"+RESET)
    print(GREEN+f"\n  Trade complete! 🤝{RESET}")

# ══════════════════════════════════════════
# TEAM SELECTOR
# ══════════════════════════════════════════
def team_selector(player_num, available_teams):
    print(f"\n{BOLD}🏀 TEAM SELECTOR{RESET}")
    print("="*50)
    names=list(available_teams.keys())
    for i,t in enumerate(names,1):
        tm=team_meta.get(t,{}); r=tm.get("team_rating","?"); s=tm.get("style","")
        print(f"  {i:>2}. {color_team_abbr(t):<6} {color_team_name(t):<32} [{r}] {DIM}{s}{RESET}")
    while True:
        c=input(f"\nPlayer {player_num} — choose (# or name): ").strip()
        sel=None
        if c.isdigit():
            n=int(c)
            if 1<=n<=len(names): sel=names[n-1]
        else:
            for t in names:
                if c.lower()==t.lower(): sel=t; break
            if not sel:
                for t in names:
                    if c.lower() in t.lower(): sel=t; break
        if sel:
            print(GREEN+f"\n  ✓ {color_team_name(sel)} selected!"+RESET)
            available_teams.pop(sel); return sel
        print(RED+"  Not found."+RESET)

# ══════════════════════════════════════════
# GM MODE
# ══════════════════════════════════════════
def gm_mode(active_rosters):
    global gm_active,gm_team,gm_season,gm_history,franchise_history
    # Reset franchise history for fresh GM session
    franchise_history = {
        "champions":[], "award_history":[], "retired_players":[],
        "team_rings":{}, "career_stats":{}, "career_pts_ldr":[],
    }
    print(f"\n{'═'*60}\n{BOLD}{MAGENTA}  🏀 GM MODE — Build Your Legacy{RESET}\n{'═'*60}")
    print("  Franchise mode: 82 games · playoffs · full offseason · multi-season\n")
    tl=list(active_rosters.keys())
    for i,t in enumerate(tl,1):
        tm=team_meta.get(t,{})
        ovr=tm.get("team_rating","?")
        payroll=sum(_salary_for(p.get("overall",75),p.get("age",27))
                    for p in active_rosters.get(t,[]))
        print(f"  {i:>2}. {color_team_abbr(t):<6} {color_team_name(t):<32} "
              f"[OVR:{ovr}] ${round(payroll,0):.0f}M")
    while True:
        c=input("\n  Pick YOUR franchise #: ").strip()
        if c.isdigit() and 1<=int(c)<=len(tl): gm_team=tl[int(c)-1]; break
        print(RED+"Invalid."+RESET)
    gm_active=True; gm_season=1
    reset_season_records(tl); reset_season_stats(); init_picks(tl,gm_season)
    # Initialize all player meta systems
    init_contracts(active_rosters)
    init_player_meta(active_rosters)
    print(f"\n{GREEN}  ✓ Your franchise: {color_team_name(gm_team)}{RESET}")
    payroll = get_payroll(active_rosters, gm_team)
    cap_clr = RED if payroll>LUXURY_TAX else ORANGE if payroll>SALARY_CAP else GREEN
    print(f"  Payroll: {cap_clr}${payroll}M{RESET} / ${SALARY_CAP}M cap  |  Season {gm_season} begins!\n")
    _run_gm_season(active_rosters,tl)

def _run_gm_season(active_rosters, all_teams):
    global gm_season, gm_history
    while True:
        ur = gm_records.get(gm_team, {"W":0,"L":0})
        rings = franchise_history["team_rings"].get(gm_team, 0)
        ring_str = f" {'🏆'*min(rings,5)}" if rings else ""
        print(f"\n{'═'*60}")
        print(f"{BOLD}{MAGENTA}  📅 SEASON {gm_season}  —  {color_team_name(gm_team)}{ring_str}{RESET}")
        print(f"  Record: {GREEN}{ur['W']}W{RESET}-{RED}{ur['L']}L{RESET}"
              f"   Payroll: ${get_payroll(active_rosters,gm_team)}M/{SALARY_CAP}M")
        print(f"{'═'*60}")
        print(f"  {CYAN}1.{RESET} Simulate Season  {DIM}(full play-by-play){RESET}   "
              f"{CYAN}2.{RESET} Simulate Season  {DIM}(fast mode){RESET}")
        print(f"  {CYAN}3.{RESET} Trade Center                              "
              f"{CYAN}4.{RESET} Standings")
        print(f"  {CYAN}5.{RESET} Stat Leaders                              "
              f"{CYAN}6.{RESET} Playoffs  {DIM}(after season){RESET}")
        print(f"  {CYAN}7.{RESET} My Roster                                 "
              f"{CYAN}8.{RESET} My Draft Picks")
        print(f"  {CYAN}9.{RESET} Team Management                           "
              f"{CYAN}H.{RESET} Franchise History")
        print(f"  {CYAN}─────── NEW SYSTEMS ─────────────────────────────────────{RESET}")
        print(f"  {YELLOW}N.{RESET} League News  {DIM}(headlines · rumors · recaps){RESET}    "
              f"{YELLOW}P.{RESET} Power Rankings")
        print(f"  {YELLOW}M.{RESET} MVP Ladder                                "
              f"{YELLOW}R.{RESET} Rookie Ladder")
        print(f"  {YELLOW}A.{RESET} Advanced Stats  {DIM}(PER · TS% · WS){RESET}          "
              f"{YELLOW}C.{RESET} Compare Players")
        print(f"  {YELLOW}G.{RESET} Season Goals / Owner Grade               "
              f"{YELLOW}K.{RESET} Coaching Staff")
        print(f"  {CYAN}0.{RESET} Exit GM Mode")
        c = input("  > ").strip().upper()
        if   c == "1": _play_82(active_rosters, all_teams, verbose=True)
        elif c == "2": _play_82(active_rosters, all_teams, verbose=False)
        elif c == "3": trade_menu(active_rosters)
        elif c == "4": show_standings(all_teams)
        elif c == "5": show_season_stats()
        elif c == "6":
            result = run_playoffs(active_rosters)
            if result:
                champ = result if isinstance(result, str) else result.get("winner", result)
                cs = result.get("champ_score", 0) if isinstance(result, dict) else 0
                ls = result.get("loser_score", 0) if isinstance(result, dict) else 0
                gm_history.append({"season":gm_season,"champion":champ,
                                   "your_team":gm_team,"records":copy.deepcopy(gm_records)})
                _offseason(active_rosters, all_teams, champ, cs, ls)
        elif c == "7": _show_roster(active_rosters, gm_team)
        elif c == "8": _show_picks(gm_team)
        elif c == "9": show_team_management(active_rosters, gm_team)
        elif c == "H": show_franchise_history(active_rosters)
        # ── New systems ──
        elif c == "N": show_news_menu()
        elif c == "P": show_power_rankings(active_rosters)
        elif c == "M": show_mvp_ladder()
        elif c == "R": show_rookie_ladder(active_rosters)
        elif c == "A": show_advanced_stats(active_rosters)
        elif c == "C": compare_players(active_rosters)
        elif c == "G":
            champ = None
            if gm_records:
                champ = max(gm_records, key=lambda t: gm_records[t]["W"])
            grade_season(all_teams, champ)
        elif c == "K": show_coaching_staff(active_rosters, gm_team)
        elif c == "0": show_franchise_history(active_rosters); break

_STORYLINES = [
    ("breakout",  lambda r,gs: max(gs.items(), key=lambda x:x[1]["PTS"], default=(None,{}))[1].get("PTS",0) >= 40,
     lambda r,gs: f"🔥 {max(gs.items(),key=lambda x:x[1]['PTS'])[0]} ERUPTS for "
                  f"{max(gs.items(),key=lambda x:x[1]['PTS'])[1]['PTS']} POINTS!"),
    ("upset",     lambda r,gs: True,  # evaluated separately
     lambda r,gs: ""),  # placeholder
    ("comeback",  lambda r,gs: abs(r["score"][r["winner"]] - r["score"][r["loser"]]) <= 3,
     lambda r,gs: f"🎯 NAIL-BITER!  {color_team_abbr(r['winner'])} wins by "
                  f"{abs(r['score'][r['winner']]-r['score'][r['loser']])} in a thriller!"),
]

def _check_storylines(r, gstats, t1_ovr, t2_ovr, verbose):
    """Print any notable game storylines."""
    if not verbose: return
    winner = r["winner"]; loser = r["loser"]
    ws = r["score"][winner]; ls = r["score"][loser]
    # 40-pt game
    best_n, best_s = max(gstats.items(), key=lambda x:x[1]["PTS"])
    if best_s["PTS"] >= 40:
        print(f"\n  {YELLOW}{BOLD}🔥 STORYLINE: {best_n} ERUPTS for {best_s['PTS']} PTS in a historic game!{RESET}")
    # Upset (lower OVR team wins)
    winner_ovr = t1_ovr if winner==r.get("t1") else t2_ovr
    loser_ovr  = t2_ovr if winner==r.get("t1") else t1_ovr
    if loser_ovr - winner_ovr >= 8:
        print(f"\n  {ORANGE}{BOLD}⚡ UPSET ALERT! {color_team_abbr(winner)} topples {color_team_abbr(loser)}!{RESET}")
    # Nail-biter
    if ws - ls <= 2:
        print(f"\n  {CYAN}🎯 THRILLER: {color_team_abbr(winner)} edges out {color_team_abbr(loser)} {ws}–{ls}!{RESET}")

def _team_avg_ovr(active_rosters, team):
    pls = active_rosters.get(team, [])
    if not pls: return 75
    return sum(p.get("overall",75) for p in pls) / len(pls)

def _play_82(active_rosters, all_teams, verbose):
    global gm_records, _news_game_no
    reset_season_records(all_teams); reset_season_stats()
    init_player_meta(active_rosters)
    # Assign season goals at the start of each season
    assign_season_goals(active_rosters, all_teams)
    sched = generate_schedule(all_teams, target=82)
    total = len(sched)
    print(f"\n{BOLD}{WHITE}  ⏱  {total} games scheduled{RESET}")
    print(f"  {DIM}Team goal: {season_goals.get(gm_team,{}).get('goal','?')} "
          f"(target {season_goals.get(gm_team,{}).get('target','?')} wins){RESET}")
    input(f"  {DIM}Press ENTER to start...{RESET}")
    mid=total//2; dl_done=False; as_done=False
    # Track consecutive wins for streak news
    _streak = {t: 0 for t in all_teams}

    for g,(t1,t2) in enumerate(sched,1):
        _news_game_no = g
        inv=(t1==gm_team or t2==gm_team)
        t1_ovr = _team_avg_ovr(active_rosters, t1)
        t2_ovr = _team_avg_ovr(active_rosters, t2)
        # t1 is home team for this matchup
        if verbose and inv:
            r=simulate_game(t1,t2,active_rosters,verbose=True,silent=False,home_team=t1)
            _check_storylines(r, r["game_stats"], t1_ovr, t2_ovr, True)
        else:
            r=simulate_game(t1,t2,active_rosters,verbose=False,silent=False,home_team=t1)
            if g%10==0 or inv:
                ur=gm_records.get(gm_team,{"W":0,"L":0})
                sc=r["score"]
                print(f"  Game {g:>4}/{total}  "
                      f"{color_team_abbr(t1)} {sc[t1]:>3} – {sc[t2]:>3} {color_team_abbr(t2)}"
                      f"  │  You: {GREEN}{ur['W']}W{RESET}-{RED}{ur['L']}L{RESET}")
                if inv: _check_storylines(r, r["game_stats"], t1_ovr, t2_ovr, True)

        record_result(r["winner"],r["loser"],r["score"][r["winner"]],r["score"][r["loser"]])
        add_to_season_stats(r["game_stats"])

        # Career highs + milestones after every game
        for pname, gs in r["game_stats"].items():
            update_career_highs(pname, gs["PTS"], gs["REB"], gs["AST"])
            check_milestones(pname, gs["PTS"], gs["REB"], gs["AST"])

        # News: notable game recap
        if inv or r["score"][r["winner"]] - r["score"][r["loser"]] <= 2:
            _news_game_recap(t1, t2, r["score"], r["game_stats"], r["winner"])

        # Streak tracking + streak news
        for tm in [t1, t2]:
            if tm == r["winner"]:
                _streak[tm] = _streak.get(tm, 0) + 1
                _news_streak_check(tm, _streak[tm])
            else:
                _streak[tm] = 0

        # Injury news
        if r.get("inj_events"):
            for ev in r["inj_events"]:
                sev = ev["inj"]["sev"]
                if sev in ("severe","serious","career"):
                    news_add("INJURY",
                        f"INJURY: {ev['player']} suffers {ev['inj']['name']}",
                        f"{ev['player']} left the game with a {ev['inj']['name']} "
                        f"and will miss approximately {ev.get('games',0)} games.")

        # Tick injuries + recovery news
        healed=tick_injuries(active_rosters)
        if healed:
            for pn in healed:
                news_add("INJURY", f"{pn} returns from injury!", f"{pn} has been cleared to return.")
                if inv and verbose: print(f"  {GREEN}✅ {pn} returns from injury!{RESET}")

        # Update morale after each game
        morale_events = update_morale_postgame(active_rosters, r, r["game_stats"], gm_team)
        if morale_events and inv and verbose:
            for ev in morale_events: print(f"  {ev}")

        # Weekly features every 15 games
        if g % 15 == 0:
            _news_mvp_race_update()
            _news_playoff_race(all_teams, g)

        # All-Star Weekend at the midpoint
        if g == mid and not as_done:
            as_done = True
            print(f"\n  {YELLOW}⭐ ALL-STAR BREAK!{RESET}")
            if input("  Watch All-Star Weekend? (y/n): ").strip().lower() == "y":
                run_all_star_weekend(active_rosters)

        # Trade deadline (just after midpoint)
        if g == mid + 3 and not dl_done:
            dl_done = True
            ur = gm_records.get(gm_team,{"W":0,"L":0})
            print(f"\n  {YELLOW}{BOLD}⏰ TRADE DEADLINE!{RESET}  Your record: "
                  f"{GREEN}{ur['W']}W{RESET}-{RED}{ur['L']}L{RESET}")
            generate_trade_rumors(active_rosters, all_teams)
            if input("  Make a trade? (y/n): ").strip().lower() == "y":
                trade_menu(active_rosters)
            # AI deadline moves
            ai_trade_deadline_moves(active_rosters, all_teams)

    ur=gm_records.get(gm_team,{"W":0,"L":0})
    print(f"\n  {GREEN}✓ Season complete!{RESET}  {color_team_name(gm_team)}: "
          f"{GREEN}{BOLD}{ur['W']}W{RESET} – {RED}{BOLD}{ur['L']}L{RESET}")
    show_standings(all_teams)
    show_awards(active_rosters)

def _offseason(active_rosters, all_teams, champion, champ_score=0, lose_score=0):
    """Full offseason — delegates to run_full_offseason."""
    run_full_offseason(active_rosters, all_teams, champion, champ_score, lose_score)

def _show_roster(active_rosters, team):
    players = sorted(active_rosters[team], key=lambda x: x.get("overall",0), reverse=True)
    payroll  = get_payroll(active_rosters, team)
    cap_clr  = RED if payroll>LUXURY_TAX else ORANGE if payroll>SALARY_CAP else GREEN
    print(f"\n{'═'*68}")
    print(f"  {BOLD}{color_team_name(team)} ROSTER{RESET}"
          f"  │  Payroll: {cap_clr}${payroll}M{RESET}/{SALARY_CAP}M"
          f"  │  {len(players)} players")
    print(f"{'═'*68}")
    print(f"  {'PLAYER':<24} POS AGE {WHITE}OVR{RESET} {ORANGE}OFF{RESET} {CYAN}DEF{RESET}"
          f" {YELLOW}SHT{RESET}  POT  SAL(M)  YRS  STATUS")
    print(f"  {'─'*68}")
    for p in players:
        ai = p.get("active_injury")
        if ai:
            if ai.get("retired"):            status = f"{RED}RETIRED{RESET}"
            elif ai["games_left"] > 0:       status = f"{RED}OUT {ai['games_left']}g  ⚕{ai['name']}{RESET}"
            else:                            status = f"{YELLOW}DTD{RESET}"
        else: status = f"{GREEN}✓{RESET}"
        tier    = (f"{GREEN}★ " if p.get("overall",0)>=88 else
                   f"{ORANGE}◆ " if p.get("overall",0)>=80 else "  ")
        pot     = p.get("potential","?")
        pot_c   = (GREEN if pot in ("A+","A") else ORANGE if pot=="B+" else WHITE)
        yrs     = p.get("contract_years", "?")
        yrs_c   = RED if yrs==0 else YELLOW if yrs==1 else GREEN
        sal     = p.get("salary", "?")
        arc     = p.get("archetype","?")
        print(f"  {tier}{p['name']:<24}{RESET}"
              f" {p.get('pos','?'):>3} {p.get('age','?'):>3}"
              f" {WHITE}{p.get('overall','?'):>3}{RESET}"
              f" {ORANGE}{p.get('offense','?'):>3}{RESET}"
              f" {CYAN}{p.get('defense','?'):>3}{RESET}"
              f" {YELLOW}{p.get('shooting','?'):>3}{RESET}"
              f"  {pot_c}{pot:>2}{RESET}  {YELLOW}${sal:<5}{RESET}"
              f"  {yrs_c}{yrs}yr{RESET}  {status}")
    print(f"  {'─'*68}")
    print(f"  {DIM}Archetypes: " +
          "  ".join(f"{p['name'].split()[0]}:{p.get('archetype','?')}"
                    for p in players[:5]) + f"{RESET}")

def _show_picks(team):
    picks=get_team_picks(team)
    print(f"\n  {BOLD}Picks owned by {color_team_name(team)}:{RESET}")
    if not picks: print(f"  {DIM}None.{RESET}"); return
    print(f"  {'─'*40}")
    for pk in picks:
        c=YELLOW if pk["round"]==1 else CYAN
        orig=f"  {DIM}(orig: {team_abbr(pk['original'])}){RESET}" if pk["original"]!=team else ""
        print(f"  {c}{'1st' if pk['round']==1 else '2nd'} Round {pk['year']}{RESET}{orig}")

def _show_history():
    """Legacy stub — now delegates to show_franchise_history."""
    show_franchise_history({})

# ══════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════
def main():
    active_rosters=copy.deepcopy(base_rosters)
    while True:
        print(f"\n{BOLD}{CYAN}{'╔'*54}{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}{' '*52}{BOLD}{CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}{BOLD}{YELLOW}      🏀  NBA SIMULATION GAME  🏀{RESET}{BOLD}{CYAN}      ║{RESET}")
        print(f"{BOLD}{CYAN}║{RESET}{' '*52}{BOLD}{CYAN}║{RESET}")
        print(f"{BOLD}{CYAN}{'╚'*54}{RESET}\n")
        
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}1.{RESET} {WHITE}Quick Game{RESET}           {DIM}(auto-simulated){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}2.{RESET} {MAGENTA}GM Mode{RESET}              {DIM}(franchise · 82 games · playoffs){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}3.{RESET} {YELLOW}Interactive Quick-Play{RESET} {DIM}(control possessions, fouls, etc.){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}4.{RESET} {ORANGE}Trade Center{RESET}          {DIM}(build your roster){RESET}")
        print(f"  {BOLD}{GREEN}▶{RESET} {CYAN}5.{RESET} {LBLUE}Draft{RESET}                 {DIM}(scout new talent){RESET}")
        print(f"  {BOLD}{RED}▶{RESET} {CYAN}0.{RESET} {RED}Exit{RESET}                   {DIM}(quit game){RESET}")
        print(f"\n{DIM}{'─'*54}{RESET}")
        c=input(f"  {BOLD}{CYAN}Choose option:{RESET} ").strip()
        if c=="1":
            avail={t:None for t in active_rosters}
            t1=team_selector(1,avail); t2=team_selector(2,{t:None for t in avail})
            simulate_game(t1,t2,active_rosters,verbose=True,silent=False)
        elif c=="2":
            gm_mode(copy.deepcopy(base_rosters))
        elif c=="3":
            quick_play_mode(active_rosters)
        elif c=="4":
            trade_menu(active_rosters)
        elif c=="5":
            run_draft(active_rosters,rounds=2)
        elif c=="0":
            print(f"\n{BOLD}{CYAN}{'╔'*54}{RESET}")
            print(f"{BOLD}{CYAN}║{RESET}{GREEN}      Thanks for playing! 🏀{RESET}{BOLD}{CYAN}{' '*24}║{RESET}")
            print(f"{BOLD}{CYAN}{'╚'*54}{RESET}\n"); break
        else:
            print(f"\n  {RED}✖ Invalid choice. Please try again.{RESET}\n")

if __name__ == "__main__":
    main()
