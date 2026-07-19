"""
UI and gameplay reference data for the NBA game.
"""

# Different UI themes.
THEMES = {
    "classic": {
        "primary": "blue",
        "secondary": "white"
    },
    "dark": {
        "primary": "black",
        "secondary": "purple"
    }
}

# Player titles/nicknames.
TITLES = {
    "GOAT": "🐐",
    "Legend": "👑",
    "Superstar": "⭐",
    "Rookie": "🌟",
    "Veteran": "🧓"
}

# Gameplay streak names.
STREAKS = {
    "Heating Up": "🔥",
    "On Fire": "🔥🔥",
    "Unstoppable": "💥"
}

# Player skills / play types.
PLAY_TYPES = {
    "Dunk": "💥",
    "Layup": "🏀",
    "Fadeaway": "🌙",
    "Stepback": "↩️",
    "Alley Oop": "🚀"
}

# Icons for badges.
BADGE_ICONS = {
    "shooting": "🎯",
    "finishing": "💥",
    "playmaking": "🧠",
    "defense": "🛡️",
    "rebounding": "💪"
}

# Rarities for players/items.
RARITIES = {
    "Common": "⚪",
    "Rare": "🔵",
    "Elite": "🟣",
    "Legendary": "🟡",
    "GOAT": "🐐"
}

# Player grades.
GRADES = {
    "A+": "🔥",
    "A": "⭐",
    "B": "👍",
    "C": "➖",
    "D": "⚠️"
}

# Position icons.
POSITIONS = {
    "PG": "🎯",
    "SG": "🏹",
    "SF": "⭐",
    "PF": "💪",
    "C": "🛡️"
}

# Career achievements.
ACHIEVEMENTS = {
    "First Triple Double": "🏀",
    "10000 Points": "🔥",
    "Championship": "🏆",
    "MVP": "🥇"
}

# Player personalities.
PERSONALITIES = {
    "Leader": "👑",
    "Quiet": "🤫",
    "Competitive": "🔥",
    "Clutch": "⏱️"
}

# NBA eras.
ERAS = {
    "60s": "🕰️",
    "80s": "📼",
    "90s": "📺",
    "2000s": "💿",
    "Modern": "📱"
}


if __name__ == "__main__":
    groups = {
        "THEMES": THEMES,
        "TITLES": TITLES,
        "STREAKS": STREAKS,
        "PLAY_TYPES": PLAY_TYPES,
        "BADGE_ICONS": BADGE_ICONS,
        "RARITIES": RARITIES,
        "GRADES": GRADES,
        "POSITIONS": POSITIONS,
        "ACHIEVEMENTS": ACHIEVEMENTS,
        "PERSONALITIES": PERSONALITIES,
        "ERAS": ERAS,
    }
    for name, data in groups.items():
        print(f"{name}: {len(data)} entries")