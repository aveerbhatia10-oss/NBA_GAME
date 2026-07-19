"""
Season tracker: MVP race, award races, All-Star voting, power rankings,
player streaks, league leaders, rookie watch, playoff picture,
championship odds, tank watch, clutch players, matchups, records watch,
player awards tracker, hot topics, and the injury report — all in one
place for the NBA game.
"""

MVP_RACE = [
    {"player": "Nikola Jokic", "rank": 1, "reason": "Leading top seed with elite stats"},
    {"player": "Shai Gilgeous-Alexander", "rank": 2, "reason": "Scoring leader and elite defense"},
    {"player": "Giannis Antetokounmpo", "rank": 3, "reason": "Dominant two-way numbers on a winning team"},
    {"player": "Luka Doncic", "rank": 4, "reason": "Elite usage and playmaking on a top-4 seed"},
    {"player": "Jayson Tatum", "rank": 5, "reason": "Best player on the league's best record"},
    {"player": "Anthony Edwards", "rank": 6, "reason": "Breakout two-way star carrying his team"},
    {"player": "Victor Wembanyama", "rank": 7, "reason": "Historic defensive impact paired with rising scoring"},
    {"player": "Donovan Mitchell", "rank": 8, "reason": "Leading a surprise contender in the standings"},
]

AWARD_RACES = {
    "MVP": [
        {"player": "Nikola Jokic", "rank": 1, "reason": "Leading top seed with elite stats"},
        {"player": "Shai Gilgeous-Alexander", "rank": 2, "reason": "Scoring leader and elite defense"},
        {"player": "Giannis Antetokounmpo", "rank": 3, "reason": "Dominant two-way numbers on a winning team"},
    ],
    "DPOY": [
        {"player": "Victor Wembanyama", "rank": 1, "reason": "Leads the league in blocks and defensive rating"},
        {"player": "Rudy Gobert", "rank": 2, "reason": "Anchors the league's top-ranked defense"},
        {"player": "Evan Mobley", "rank": 3, "reason": "Versatile rim protection and switchability"},
    ],
    "ROY": [
        {"player": "Zaccharie Risacher", "rank": 1, "reason": "Most complete two-way rookie season"},
        {"player": "Alex Sarr", "rank": 2, "reason": "High-upside big with strong per-minute numbers"},
        {"player": "Reed Sheppard", "rank": 3, "reason": "Efficient scoring off the bench"},
    ],
    "Sixth Man": [
        {"player": "Naz Reid", "rank": 1, "reason": "Instant offense and floor spacing off the bench"},
        {"player": "Malik Monk", "rank": 2, "reason": "Elite scoring punch in a reserve role"},
        {"player": "Payton Pritchard", "rank": 3, "reason": "High-volume shooting and steady minutes"},
    ],
    "Most Improved": [
        {"player": "Cade Cunningham", "rank": 1, "reason": "Major leap in scoring and playmaking efficiency"},
        {"player": "Ivica Zubac", "rank": 2, "reason": "Career-best numbers as a full-time starter"},
        {"player": "Jalen Williams", "rank": 3, "reason": "Expanded role and improved shot-making"},
    ],
}

ALL_STAR_VOTES = {
    "LeBron James": 5200000,
    "Stephen Curry": 4800000,
    "Nikola Jokic": 4500000,
    "Luka Doncic": 4300000,
    "Giannis Antetokounmpo": 4100000,
    "Shai Gilgeous-Alexander": 3900000,
    "Jayson Tatum": 3600000,
    "Victor Wembanyama": 3400000,
    "Anthony Edwards": 3200000,
    "Kevin Durant": 3000000,
}

POWER_RANKINGS = {
    1: "Boston Celtics",
    2: "Denver Nuggets",
    3: "Oklahoma City Thunder",
    4: "Minnesota Timberwolves",
    5: "New York Knicks",
    6: "Cleveland Cavaliers",
    7: "Dallas Mavericks",
    8: "Los Angeles Lakers",
    9: "Milwaukee Bucks",
    10: "Indiana Pacers",
    11: "Phoenix Suns",
    12: "New Orleans Pelicans",
    13: "Orlando Magic",
    14: "Sacramento Kings",
    15: "Philadelphia 76ers",
    16: "Golden State Warriors",
    17: "Houston Rockets",
    18: "Miami Heat",
    19: "Los Angeles Clippers",
    20: "Atlanta Hawks",
    21: "Chicago Bulls",
    22: "Utah Jazz",
    23: "Memphis Grizzlies",
    24: "San Antonio Spurs",
    25: "Brooklyn Nets",
    26: "Toronto Raptors",
    27: "Portland Trail Blazers",
    28: "Charlotte Hornets",
    29: "Washington Wizards",
    30: "Detroit Pistons",
}

PLAYER_STREAKS = [
    {"player": "Anthony Edwards", "streak": "30+ point streak", "length": 4},
    {"player": "Domantas Sabonis", "streak": "Double-double streak", "length": 12},
    {"player": "Zach LaVine", "streak": "Shooting slump", "length": 5},
    {"player": "Tyrese Haliburton", "streak": "Double-digit assist streak", "length": 6},
    {"player": "Jaylen Brown", "streak": "Cold shooting slump", "length": 3},
    {"player": "Karl-Anthony Towns", "streak": "20+ point streak", "length": 8},
]

LEAGUE_LEADERS = {
    "Points": [
        {"player": "Shai Gilgeous-Alexander", "value": 32.4},
        {"player": "Luka Doncic", "value": 31.8},
        {"player": "Giannis Antetokounmpo", "value": 30.9},
    ],
    "Assists": [
        {"player": "Tyrese Haliburton", "value": 10.9},
        {"player": "Trae Young", "value": 10.6},
        {"player": "Nikola Jokic", "value": 9.8},
    ],
    "Rebounds": [
        {"player": "Domantas Sabonis", "value": 13.2},
        {"player": "Nikola Jokic", "value": 12.7},
        {"player": "Rudy Gobert", "value": 12.1},
    ],
    "Steals": [
        {"player": "Dyson Daniels", "value": 3.1},
        {"player": "Shai Gilgeous-Alexander", "value": 2.0},
        {"player": "Jalen Suggs", "value": 1.9},
    ],
    "Blocks": [
        {"player": "Victor Wembanyama", "value": 3.9},
        {"player": "Rudy Gobert", "value": 2.2},
        {"player": "Chet Holmgren", "value": 2.1},
    ],
    "3PM": [
        {"player": "Stephen Curry", "value": 4.8},
        {"player": "Klay Thompson", "value": 3.9},
        {"player": "Tyrese Maxey", "value": 3.6},
    ],
}

ROOKIE_WATCH = [
    "Rookie averaging 18 PPG",
    "Rookie climbing draft rankings",
    "Rookie leading all first-years in rebounding",
    "Rookie earning more crunch-time minutes",
    "Rookie named to the Rising Stars roster",
    "Rookie's efficiency improving each month",
    "Rookie drawing early Rookie of the Year buzz",
    "Rookie sidelined with a minor injury",
]

PLAYOFF_PICTURE = {
    "Eastern Conference": {
        "seeds": {
            1: "Boston Celtics",
            2: "New York Knicks",
            3: "Cleveland Cavaliers",
            4: "Milwaukee Bucks",
            5: "Indiana Pacers",
            6: "Orlando Magic",
        },
        "play_in": ["Philadelphia 76ers", "Miami Heat", "Atlanta Hawks", "Chicago Bulls"],
        "eliminated": ["Detroit Pistons", "Washington Wizards", "Charlotte Hornets"],
    },
    "Western Conference": {
        "seeds": {
            1: "Denver Nuggets",
            2: "Oklahoma City Thunder",
            3: "Minnesota Timberwolves",
            4: "Dallas Mavericks",
            5: "Los Angeles Lakers",
            6: "Phoenix Suns",
        },
        "play_in": ["New Orleans Pelicans", "Sacramento Kings", "Golden State Warriors", "Houston Rockets"],
        "eliminated": ["San Antonio Spurs", "Portland Trail Blazers", "Memphis Grizzlies"],
    },
}

CONTENDERS = {
    "Celtics": 20,
    "Thunder": 18,
    "Nuggets": 15,
    "Knicks": 10,
    "Cavaliers": 9,
    "Timberwolves": 7,
    "Mavericks": 6,
    "Lakers": 5,
    "Bucks": 4,
    "Pacers": 3,
}

TANK_WATCH = [
    "Detroit Pistons",
    "Washington Wizards",
    "Charlotte Hornets",
    "Portland Trail Blazers",
    "Memphis Grizzlies",
    "San Antonio Spurs",
    "Utah Jazz",
]

CLUTCH_PLAYERS = [
    {"player": "Jayson Tatum", "fourth_qtr_ppg": 7.8, "game_winners": 3, "clutch_rating": 9.1},
    {"player": "Shai Gilgeous-Alexander", "fourth_qtr_ppg": 8.2, "game_winners": 4, "clutch_rating": 9.4},
    {"player": "Luka Doncic", "fourth_qtr_ppg": 7.5, "game_winners": 2, "clutch_rating": 8.9},
    {"player": "Damian Lillard", "fourth_qtr_ppg": 6.9, "game_winners": 5, "clutch_rating": 9.0},
    {"player": "Devin Booker", "fourth_qtr_ppg": 7.1, "game_winners": 2, "clutch_rating": 8.6},
]

MATCHUPS = [
    {"type": "player", "matchup": "Jokic vs Embiid", "note": "Battle of two of the league's premier bigs"},
    {"type": "player", "matchup": "SGA vs Luka", "note": "Duel between elite isolation scorers"},
    {"type": "team", "matchup": "Lakers vs Celtics", "note": "The league's most storied rivalry"},
    {"type": "team", "matchup": "Knicks vs Pacers", "note": "Recent playoff bad blood renews"},
    {"type": "player", "matchup": "Wembanyama vs Chet Holmgren", "note": "Next-generation shot blockers face off"},
    {"type": "team", "matchup": "Nuggets vs Timberwolves", "note": "Two of the West's top defenses collide"},
]

RECORDS_WATCH = [
    "Curry is 15 threes away from 4,000 career 3PM",
    "LeBron is 200 points away from padding his all-time scoring record",
    "Jokic is 3 triple-doubles away from tying the single-season record",
    "Giannis is 50 dunks away from a new career high in a single season",
    "CP3 is 25 assists away from moving up the all-time assists list",
]

PLAYER_AWARDS_TRACKER = {
    "Devin Booker": {
        "needs": ["1 more All-Star", "1 more All-NBA", "1 more championship"],
    },
    "Trae Young": {
        "needs": ["2 more All-Stars", "1 more All-NBA", "1 playoff series win"],
    },
    "Domantas Sabonis": {
        "needs": ["1 more All-NBA", "1 more championship"],
    },
    "Anthony Edwards": {
        "needs": ["1 All-NBA First Team", "1 Finals appearance"],
    },
}

HOT_TOPICS = [
    "Can this team win 60 games?",
    "Rookie of the Year race heating up",
    "Trade rumors increasing",
    "Is this the year a young core finally breaks through?",
    "MVP race tightening down the stretch",
    "Coaching seat getting warm after a rough stretch",
    "Superteam experiment facing early questions",
    "Small-market team quietly building a contender",
]

INJURY_REPORT = [
    {"player": "Kawhi Leonard", "team": "Los Angeles Clippers", "status": "Out", "injury": "Knee"},
    {"player": "Joel Embiid", "team": "Philadelphia 76ers", "status": "Day-to-Day", "injury": "Knee"},
    {"player": "Ja Morant", "team": "Memphis Grizzlies", "status": "Questionable", "injury": "Shoulder"},
    {"player": "Zion Williamson", "team": "New Orleans Pelicans", "status": "Out", "injury": "Hamstring"},
    {"player": "Jamal Murray", "team": "Denver Nuggets", "status": "Probable", "injury": "Ankle"},
]

LEGACY_TRACKER = {
    "LeBron James": {
        "mvps": 4,
        "rings": 4,
        "finals_mvps": 4,
        "stats": "All-time leading scorer",
        "awards": ["20x All-Star", "20x All-NBA"],
    },
    "Stephen Curry": {
        "mvps": 2,
        "rings": 4,
        "finals_mvps": 1,
        "stats": "All-time leader in made three-pointers",
        "awards": ["10x All-Star", "unanimous MVP season"],
    },
    "Kevin Durant": {
        "mvps": 1,
        "rings": 2,
        "finals_mvps": 2,
        "stats": "Top-10 all-time scorer",
        "awards": ["14x All-Star", "scoring champion multiple times"],
    },
    "Nikola Jokic": {
        "mvps": 3,
        "rings": 1,
        "finals_mvps": 1,
        "stats": "Career triple-double average season",
        "awards": ["All-NBA First Team multiple times"],
    },
}