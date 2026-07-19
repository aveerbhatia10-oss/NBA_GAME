"""
NBA team rivalries, organized by division/conference grouping.
"""

RIVALRIES = {
    "Eastern Conference": {
        "Atlantic Division": [
            "76ers–Celtics rivalry",
            "Celtics–Knicks rivalry",
            "Knicks–Nets rivalry",
        ],
        "Central Division": [
            "Bulls–Cavaliers rivalry",
            "Bulls–Pistons rivalry",
            "Pacers–Pistons rivalry",
        ],
        "Southeast Division": [
            "Heat–Magic rivalry",
        ],
        "Interdivisional": [
            "Bulls–Knicks rivalry",
            "Celtics–Heat rivalry",
            "Celtics–Pistons rivalry",
            "Heat–Knicks rivalry",
            "Knicks–Pacers rivalry",
        ],
    },
    "Western Conference": {
        "Northwest Division": [
            "Jazz–Nuggets rivalry",
            "Nuggets–Timberwolves rivalry",
        ],
        "Pacific Division": [
            "Kings–Lakers rivalry",
            "Kings–Warriors rivalry",
            "Lakers–Clippers rivalry",
            "Lakers–Suns rivalry",
            "Lakers–Warriors rivalry",
            "SuperSonics–Trail Blazers rivalry (defunct/inactive)",
        ],
        "Southwest Division": [
            "Mavericks–Rockets rivalry",
            "Mavericks–Spurs rivalry",
            "Rockets–Spurs rivalry",
        ],
        "Interdivisional": [
            "Jazz–Rockets rivalry",
            "Lakers–Spurs rivalry",
            "Spurs–Suns rivalry",
        ],
    },
    "Interconference": [
        "Cavaliers–Warriors rivalry",
        "Celtics–Lakers rivalry",
        "Lakers–Pistons rivalry",
    ],
}

# Flat lookup: rivalry name -> Wikipedia URL
RIVALRY_LINKS = {
    "76ers–Celtics rivalry": "https://en.wikipedia.org/wiki/76ers%E2%80%93Celtics_rivalry",
    "Celtics–Knicks rivalry": "https://en.wikipedia.org/wiki/Celtics%E2%80%93Knicks_rivalry",
    "Knicks–Nets rivalry": "https://en.wikipedia.org/wiki/Knicks%E2%80%93Nets_rivalry",
    "Bulls–Cavaliers rivalry": "https://en.wikipedia.org/wiki/Bulls%E2%80%93Cavaliers_rivalry",
    "Bulls–Pistons rivalry": "https://en.wikipedia.org/wiki/Bulls%E2%80%93Pistons_rivalry",
    "Pacers–Pistons rivalry": "https://en.wikipedia.org/wiki/Malice_at_the_Palace",
    "Heat–Magic rivalry": "https://en.wikipedia.org/wiki/Heat%E2%80%93Magic_rivalry",
    "Bulls–Knicks rivalry": "https://en.wikipedia.org/wiki/Bulls%E2%80%93Knicks_rivalry",
    "Celtics–Heat rivalry": "https://en.wikipedia.org/wiki/Celtics%E2%80%93Heat_rivalry",
    "Celtics–Pistons rivalry": "https://en.wikipedia.org/wiki/Celtics%E2%80%93Pistons_rivalry",
    "Heat–Knicks rivalry": "https://en.wikipedia.org/wiki/Heat%E2%80%93Knicks_rivalry",
    "Knicks–Pacers rivalry": "https://en.wikipedia.org/wiki/Knicks%E2%80%93Pacers_rivalry",
    "Jazz–Nuggets rivalry": "https://en.wikipedia.org/wiki/Jazz%E2%80%93Nuggets_rivalry",
    "Nuggets–Timberwolves rivalry": "https://en.wikipedia.org/wiki/Nuggets%E2%80%93Timberwolves_rivalry",
    "Kings–Lakers rivalry": "https://en.wikipedia.org/wiki/Kings%E2%80%93Lakers_rivalry",
    "Kings–Warriors rivalry": "https://en.wikipedia.org/wiki/Kings%E2%80%93Warriors_rivalry",
    "Lakers–Clippers rivalry": "https://en.wikipedia.org/wiki/Lakers%E2%80%93Clippers_rivalry",
    "Lakers–Suns rivalry": "https://en.wikipedia.org/wiki/Lakers%E2%80%93Suns_rivalry",
    "Lakers–Warriors rivalry": "https://en.wikipedia.org/wiki/Lakers%E2%80%93Warriors_rivalry",
    "SuperSonics–Trail Blazers rivalry (defunct/inactive)": "https://en.wikipedia.org/wiki/I-5_rivalry",
    "Mavericks–Rockets rivalry": "https://en.wikipedia.org/wiki/Mavericks%E2%80%93Rockets_rivalry",
    "Mavericks–Spurs rivalry": "https://en.wikipedia.org/wiki/Mavericks%E2%80%93Spurs_rivalry",
    "Rockets–Spurs rivalry": "https://en.wikipedia.org/wiki/Rockets%E2%80%93Spurs_rivalry",
    "Jazz–Rockets rivalry": "https://en.wikipedia.org/wiki/Jazz%E2%80%93Rockets_rivalry",
    "Lakers–Spurs rivalry": "https://en.wikipedia.org/wiki/Lakers%E2%80%93Spurs_rivalry",
    "Spurs–Suns rivalry": "https://en.wikipedia.org/wiki/Spurs%E2%80%93Suns_rivalry",
    "Cavaliers–Warriors rivalry": "https://en.wikipedia.org/wiki/Cavaliers%E2%80%93Warriors_rivalry",
    "Celtics–Lakers rivalry": "https://en.wikipedia.org/wiki/Celtics%E2%80%93Lakers_rivalry",
    "Lakers–Pistons rivalry": "https://en.wikipedia.org/wiki/Lakers%E2%80%93Pistons_rivalry",
}


if __name__ == "__main__":
    total = len(RIVALRY_LINKS)
    print(f"Total rivalries: {total}")
    for conference, groups in RIVALRIES.items():
        if isinstance(groups, dict):
            for division, rivalries in groups.items():
                print(f"{conference} / {division}: {len(rivalries)}")
        else:
            print(f"{conference}: {len(groups)}")