"""
NBA arena data: current arenas for all 30 teams, plus
future/proposed arenas under construction or planned.
"""

ARENAS = {
    "Atlanta Hawks": {
        "arena": "State Farm Arena",
        "location": "Atlanta, Georgia",
        "capacity": 17044,
        "opened": 1999,
        "first_season": "1999–2000",
    },
    "Boston Celtics": {
        "arena": "TD Garden",
        "location": "Boston, Massachusetts",
        "capacity": 18624,
        "opened": 1995,
        "first_season": "1995–96",
    },
    "Brooklyn Nets": {
        "arena": "Barclays Center",
        "location": "Brooklyn, New York",
        "capacity": 17732,
        "opened": 2012,
        "first_season": "2012–13",
    },
    "Charlotte Hornets": {
        "arena": "Spectrum Center",
        "location": "Charlotte, North Carolina",
        "capacity": 19077,
        "opened": 2005,
        "first_season": "2005–06",
    },
    "Chicago Bulls": {
        "arena": "United Center",
        "location": "Chicago, Illinois",
        "capacity": 20917,
        "opened": 1994,
        "first_season": "1994–95",
    },
    "Cleveland Cavaliers": {
        "arena": "Rocket Arena",
        "location": "Cleveland, Ohio",
        "capacity": 19432,
        "opened": 1994,
        "first_season": "1994–95",
    },
    "Dallas Mavericks": {
        "arena": "American Airlines Center",
        "location": "Dallas, Texas",
        "capacity": 19200,
        "opened": 2001,
        "first_season": "2001–02",
    },
    "Denver Nuggets": {
        "arena": "Ball Arena",
        "location": "Denver, Colorado",
        "capacity": 19520,
        "opened": 1999,
        "first_season": "1999–2000",
    },
    "Detroit Pistons": {
        "arena": "Little Caesars Arena",
        "location": "Detroit, Michigan",
        "capacity": 20332,
        "opened": 2017,
        "first_season": "2017–18",
    },
    "Golden State Warriors": {
        "arena": "Chase Center",
        "location": "San Francisco, California",
        "capacity": 18064,
        "opened": 2019,
        "first_season": "2019–20",
    },
    "Houston Rockets": {
        "arena": "Toyota Center",
        "location": "Houston, Texas",
        "capacity": 18055,
        "opened": 2003,
        "first_season": "2003–04",
    },
    "Indiana Pacers": {
        "arena": "Gainbridge Fieldhouse",
        "location": "Indianapolis, Indiana",
        "capacity": 17923,
        "opened": 1999,
        "first_season": "1999–2000",
    },
    "Los Angeles Clippers": {
        "arena": "Intuit Dome",
        "location": "Inglewood, California",
        "capacity": 18000,
        "opened": 2024,
        "first_season": "2024–25",
    },
    "Los Angeles Lakers": {
        "arena": "Crypto.com Arena",
        "location": "Los Angeles, California",
        "capacity": 18997,
        "opened": 1999,
        "first_season": "1999–2000",
    },
    "Memphis Grizzlies": {
        "arena": "FedExForum",
        "location": "Memphis, Tennessee",
        "capacity": 17794,
        "opened": 2004,
        "first_season": "2004–05",
    },
    "Miami Heat": {
        "arena": "Kaseya Center",
        "location": "Miami, Florida",
        "capacity": 19600,
        "opened": 1999,
        "first_season": "1999–2000",
    },
    "Milwaukee Bucks": {
        "arena": "Fiserv Forum",
        "location": "Milwaukee, Wisconsin",
        "capacity": 17341,
        "opened": 2018,
        "first_season": "2018–19",
    },
    "Minnesota Timberwolves": {
        "arena": "Target Center",
        "location": "Minneapolis, Minnesota",
        "capacity": 18024,
        "opened": 1990,
        "first_season": "1990–91",
    },
    "New Orleans Pelicans": {
        "arena": "Smoothie King Center",
        "location": "New Orleans, Louisiana",
        "capacity": 16867,
        "opened": 1999,
        "first_season": "2002–03",
    },
    "New York Knicks": {
        "arena": "Madison Square Garden",
        "location": "New York, New York",
        "capacity": 19812,
        "opened": 1968,
        "first_season": "1967–68",
    },
    "Oklahoma City Thunder": {
        "arena": "Paycom Center",
        "location": "Oklahoma City, Oklahoma",
        "capacity": 18203,
        "opened": 2002,
        "first_season": "2005–06",
    },
    "Orlando Magic": {
        "arena": "Kia Center",
        "location": "Orlando, Florida",
        "capacity": 18846,
        "opened": 2010,
        "first_season": "2010–11",
    },
    "Philadelphia 76ers": {
        "arena": "Xfinity Mobile Arena",
        "location": "Philadelphia, Pennsylvania",
        "capacity": 20007,
        "opened": 1996,
        "first_season": "1996–97",
    },
    "Phoenix Suns": {
        "arena": "Mortgage Matchup Center",
        "location": "Phoenix, Arizona",
        "capacity": 17071,
        "opened": 1992,
        "first_season": "1992–93",
    },
    "Portland Trail Blazers": {
        "arena": "Moda Center",
        "location": "Portland, Oregon",
        "capacity": 19411,
        "opened": 1995,
        "first_season": "1995–96",
    },
    "Sacramento Kings": {
        "arena": "Golden 1 Center",
        "location": "Sacramento, California",
        "capacity": 17611,
        "opened": 2016,
        "first_season": "2016–17",
    },
    "San Antonio Spurs": {
        "arena": "Frost Bank Center",
        "location": "San Antonio, Texas",
        "capacity": 18354,
        "opened": 2002,
        "first_season": "2002–03",
    },
    "Toronto Raptors": {
        "arena": "Scotiabank Arena",
        "location": "Toronto, Ontario",
        "capacity": 19800,
        "opened": 1999,
        "first_season": "1998–99",
    },
    "Utah Jazz": {
        "arena": "Delta Center",
        "location": "Salt Lake City, Utah",
        "capacity": 18306,
        "opened": 1991,
        "first_season": "1991–92",
    },
    "Washington Wizards": {
        "arena": "Capital One Arena",
        "location": "Washington, D.C.",
        "capacity": 20333,
        "opened": 1997,
        "first_season": "1997–98",
    },
}

# Future arenas: under construction or officially proposed.
FUTURE_ARENAS = {
    "Oklahoma City Thunder": {
        "arena": "Continental Coliseum",
        "location": "Oklahoma City, Oklahoma",
        "capacity": None,
        "opening": 2028,
        "status": "under construction",
    },
    "Philadelphia 76ers": {
        "arena": "New South Philadelphia Arena",
        "location": "Philadelphia, Pennsylvania",
        "capacity": None,
        "opening": 2030,
        "status": "proposed",
    },
    "Dallas Mavericks": {
        "arena": "New Dallas Arena",
        "location": "Dallas, Texas",
        "capacity": None,
        "opening": 2031,
        "status": "proposed",
    },
    "San Antonio Spurs": {
        "arena": "New Spurs Arena",
        "location": "San Antonio, Texas",
        "capacity": None,
        "opening": 2032,
        "status": "proposed",
    },
}


if __name__ == "__main__":
    print(f"Current arenas: {len(ARENAS)}")
    print(f"Future/proposed arenas: {len(FUTURE_ARENAS)}")
    for team, info in ARENAS.items():
        print(f"{team}: {info['arena']} ({info['capacity']} capacity, opened {info['opened']})")