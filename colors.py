# ==========================================
# colors.py
# NBA Team Color Engine
# ==========================================
RESET = "\033[0m"
BOLD = "\033[1m"    


def hex_to_ansi(hex_color):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"\033[38;2;{r};{g};{b}m"



def team_abbr(team_name):

    return teams[team_name]["abbr"]



def color_team_abbr(team_name):

    abbr = teams[team_name]["abbr"]
    team_colors = teams[team_name]["colors"]

    output = ""

    for i, letter in enumerate(abbr):

        color = team_colors[i % len(team_colors)]

        output += f"{hex_to_ansi(color)}{letter}"

    output += RESET

    return output
teams = {

    # =========================
    # EASTERN CONFERENCE
    # ATLANTIC DIVISION
    # =========================

    "Boston Celtics": {
        "abbr": "BOS",
        "colors": ["#007A33", "#BA9653", "#000000", "#FFFFFF"]
    },

    "Brooklyn Nets": {
        "abbr": "BKN",
        "colors": ["#000000", "#FFFFFF"]
    },

    "New York Knicks": {
        "abbr": "NYK",
        "colors": ["#006BB6", "#F58426", "#BEC0C2", "#000000"]
    },

    "Philadelphia 76ers": {
        "abbr": "PHI",
        "colors": ["#006BB6", "#ED174C", "#002B5C", "#C4CED4"]
    },

    "Toronto Raptors": {
        "abbr": "TOR",
        "colors": ["#CE1141", "#000000", "#A1A1A4", "#B4975A"]
    },


    # =========================
    # CENTRAL DIVISION
    # =========================

    "Chicago Bulls": {
        "abbr": "CHI",
        "colors": ["#CE1141", "#000000"]
    },

    "Cleveland Cavaliers": {
        "abbr": "CLE",
        "colors": ["#860038", "#041E42", "#FDBB30", "#000000"]
    },

    "Detroit Pistons": {
        "abbr": "DET",
        "colors": ["#C8102E", "#1D42BA", "#BEC0C2", "#002D62"]
    },

    "Indiana Pacers": {
        "abbr": "IND",
        "colors": ["#002D62", "#FDBB30", "#BEC0C2"]
    },

    "Milwaukee Bucks": {
        "abbr": "MIL",
        "colors": ["#00471B", "#EEE1C6", "#0077C0", "#000000"]
    },


    # =========================
    # SOUTHEAST DIVISION
    # =========================

    "Atlanta Hawks": {
        "abbr": "ATL",
        "colors": ["#E03A3E", "#C1D32F", "#26282A"]
    },

    "Charlotte Hornets": {
        "abbr": "CHA",
        "colors": ["#1D1160", "#00788C", "#A1A1A4"]
    },

    "Miami Heat": {
        "abbr": "MIA",
        "colors": ["#98002E", "#F9A01B", "#000000"]
    },

    "Orlando Magic": {
        "abbr": "ORL",
        "colors": ["#0077C0", "#C4CED4", "#000000"]
    },

    "Washington Wizards": {
        "abbr": "WAS",
        "colors": ["#002B5C", "#E31837", "#C4CED4"]
    },

    # =========================
    # WESTERN CONFERENCE
    # NORTHWEST DIVISION
    # =========================

    "Denver Nuggets": {
        "abbr": "DEN",
        "colors": ["#0E2240", "#FEC524", "#8B2131", "#1D428A"]
    },

    "Minnesota Timberwolves": {
        "abbr": "MIN",
        "colors": ["#0C2340", "#236192", "#9EA2A2", "#78BE20"]
    },

    "Oklahoma City Thunder": {
        "abbr": "OKC",
        "colors": ["#007AC1", "#EF3B24", "#002D62", "#FDBB30"]
    },

    "Portland Trail Blazers": {
        "abbr": "POR",
        "colors": ["#E03A3E", "#000000"]
    },

    "Utah Jazz": {
        "abbr": "UTA",
        "colors": ["#002B5C", "#00471B", "#F9A01B"]
    },


    # =========================
    # PACIFIC DIVISION
    # =========================

    "Golden State Warriors": {
        "abbr": "GSW",
        "colors": ["#1D428A", "#FFC72C"]
    },

    "Los Angeles Clippers": {
        "abbr": "LAC",
        "colors": ["#C8102E", "#1D428A", "#BEC0C2", "#000000"]
    },

    "Los Angeles Lakers": {
        "abbr": "LAL",
        "colors": ["#552583", "#FDB927", "#000000"]
    },

    "Phoenix Suns": {
        "abbr": "PHX",
        "colors": ["#1D1160", "#E56020", "#000000", "#63727A", "#F9AD1B"]
    },

    "Sacramento Kings": {
        "abbr": "SAC",
        "colors": ["#5A2D81", "#63727A", "#000000"]
    },


    # =========================
    # SOUTHWEST DIVISION
    # =========================

    "Dallas Mavericks": {
        "abbr": "DAL",
        "colors": ["#00538C", "#002B5E", "#B8C4CA", "#000000"]
    },

    "Houston Rockets": {
        "abbr": "HOU",
        "colors": ["#CE1141", "#000000", "#C4CED4"]
    },

    "Memphis Grizzlies": {
        "abbr": "MEM",
        "colors": ["#5D76A9", "#12173F", "#F5B112", "#707271"]
    },

    "New Orleans Pelicans": {
        "abbr": "NOP",
        "colors": ["#0C2340", "#C8102E", "#85714D"]
    },

    "San Antonio Spurs": {
        "abbr": "SAS",
        "colors": ["#C4CED4", "#000000"]
    }

}


# ==========================================
# Team Name Coloring Function
# ==========================================

def color_team_name(team_name, chunk_size=2):
    team = teams[team_name]
    colors = []

    for color in team["colors"]:
        colors.append(hex_to_ansi(color))

    result = ""
    color_index = 0

    for i in range(0, len(team_name), chunk_size):
        chunk = team_name[i:i + chunk_size]
        result += (
            BOLD
            + colors[color_index]
            + chunk
        )

        color_index += 1

        if color_index >= len(colors):
            color_index = 0

    return result + RESET


# ==========================================
# TEST ALL NBA TEAMS
# ==========================================

if __name__ == "__main__":
    print()
    print("====================================")
    print("       NBA TEAM COLOR TEST")
    print("====================================")
    print()

    for team in teams:
        print(color_team_name(team))

    print()
    print("====================================")
    print("          TEST COMPLETE")
    print("====================================")