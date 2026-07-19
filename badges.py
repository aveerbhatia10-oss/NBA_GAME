"""
Basketball gameplay badges, organized by category.

Each badge has a description and a set of tiers. Every badge shares
the same tier structure (Bronze -> Legendary), representing how
strong the badge's effect is.
"""

TIERS = {
    "Tier 1": {"name": "Bronze", "boost": 2, "color": "bronze"},
    "Tier 2": {"name": "Silver", "boost": 4, "color": "silver"},
    "Tier 3": {"name": "Gold", "boost": 6, "color": "gold"},
    "Tier 4": {"name": "Hall of Fame", "boost": 10, "color": "purple"},
    "Tier 5": {"name": "Legendary", "boost": 15, "color": "diamond"},
}

BADGES = {
    "Finishing": {
        "Aerial Wizard": {
            "description": "Increases the ability to finish an alley-oop from a teammate, or putback a finish off an offensive rebound",
            "tiers": TIERS,
        },
        "Float Game": {
            "description": "Improves a player's ability to make floaters",
            "tiers": TIERS,
        },
        "Hook Specialist": {
            "description": "Improves a player's ability to make post hooks",
            "tiers": TIERS,
        },
        "Layup Mixmaster": {
            "description": "Improves a player's ability to finish fancy or acrobatic layups successfully.",
            "tiers": TIERS,
        },
        "Paint Prodigy": {
            "description": "Improves a player's ability to quickly and efficiently score while going to work in the paint.",
            "tiers": TIERS,
        },
        "Physical Finisher": {
            "description": "Improves a player's ability to battle through contact and convert contact layups.",
            "tiers": TIERS,
        },
        "Post Fade Phenom": {
            "description": "Improves a player's ability to make post fades and hop shots",
            "tiers": TIERS,
        },
        "Post Powerhouse": {
            "description": "Strengthens a player's ability at backing down defenders and moving them with dropsteps.",
            "tiers": TIERS,
        },
        "Post Up Poet": {
            "description": "Raises the chances of faking or getting by the defender, as well as scoring, when performing moves in the post.",
            "tiers": TIERS,
        },
        "Posterizer": {
            "description": "Increases the chances of throwing down a dunk on your defender",
            "tiers": TIERS,
        },
        "Rise Up": {
            "description": "Increases the likelihood of dunking or posterizing your opponent when standing in the painted area",
            "tiers": TIERS,
        },
        "Post Spin Technician": {
            "description": "Improves a player's ability to successfully spin around defenders while operating in the post.",
            "tiers": TIERS,
        },
        "Slithery Finisher": {
            "description": "Improves a player's ability to avoid contact and finish through traffic near the basket.",
            "tiers": TIERS,
        },
    },
    "Shooting": {
        "Deadeye": {
            "description": "Jump shots taken with a defender closing out receive less of a penalty from a shot contest",
            "tiers": TIERS,
        },
        "Limitless Range": {
            "description": "Extends the range from which a player can shoot three-pointers effectively from deep",
            "tiers": TIERS,
        },
        "Mini Marksman": {
            "description": "Elevates the likelihood of making shots over taller defenders.",
            "tiers": TIERS,
        },
        "Set Shot Specialist": {
            "description": "Boosts chances of knocking down stand-still jump shots.",
            "tiers": TIERS,
        },
        "Shifty Shooter": {
            "description": "Improves a player's ability to successfully make off-the-dribble, high-difficulty jump shots.",
            "tiers": TIERS,
        },
        "Sharpshooter": {
            "description": "Increases the overall consistency and accuracy of jump shots across all ranges.",
            "tiers": TIERS,
        },
        "Catch and Shoot": {
            "description": "Increases the shot percentage on jump shots taken shortly after catching a pass, without a dribble.",
            "tiers": TIERS,
        },
        "Corner Specialist": {
            "description": "Increases the chances of knocking down jump shots taken from the corners.",
            "tiers": TIERS,
        },
        "Green Machine": {
            "description": "Consecutive perfectly-timed ('green') releases build a temporary boost to shot success.",
            "tiers": TIERS,
        },
        "Volume Shooter": {
            "description": "Reduces the fatigue penalty and shot degradation that comes from taking a high number of shots in a game.",
            "tiers": TIERS,
        },
        "Fadeaway Ace": {
            "description": "Improves a player's accuracy on fadeaway jump shots.",
            "tiers": TIERS,
        },
    },
    "Playmaking": {
        "Ankle Assassin": {
            "description": "Increases the ability to break down the defender or cross them up.",
            "tiers": TIERS,
        },
        "Bail Out": {
            "description": "Passing out of a jump shot or layup yields fewer errant passes than normal. Additionally, helps passing out of double teams",
            "tiers": TIERS,
        },
        "Break Starter": {
            "description": "After grabbing a defensive board, deep outlet passes made up the court are more accurate. Passes must be made quickly following the defensive rebound",
            "tiers": TIERS,
        },
        "Dimer": {
            "description": "When in the half-court, passes by Dimers to open shooters yield a shot percentage boost",
            "tiers": TIERS,
        },
        "Handles for Days": {
            "description": "A player takes less of an energy hit when performing consecutive dribble moves, allowing them to chain together combos quicker and for longer periods of time",
            "tiers": TIERS,
        },
        "Lightning Launch": {
            "description": "Speeds up launches when attacking from the perimeter.",
            "tiers": TIERS,
        },
        "Strong Handle": {
            "description": "Reduces the likelihood of being bothered by defenders when dribbling.",
            "tiers": TIERS,
        },
        "Unpluckable": {
            "description": "Defenders have a tougher time poking the ball free with their steal attempts",
            "tiers": TIERS,
        },
        "Versatile Visionary": {
            "description": "Improves a player's ability to thread and fit tight passes, including alley-oops, quickly and on time.",
            "tiers": TIERS,
        },
        "Space Creator": {
            "description": "Improves a player's ability to create separation from the defender with dribble moves before pulling up for a jump shot.",
            "tiers": TIERS,
        },
        "Triple Threat Juke": {
            "description": "Improves the effectiveness of jab steps and juke moves out of the triple threat position.",
            "tiers": TIERS,
        },
    },
    "Defense": {
        "Challenger": {
            "description": "Improves the effectiveness of well-timed contests against perimeter shooters",
            "tiers": TIERS,
        },
        "Glove": {
            "description": "Increases the ability to successfully steal from ball-handlers, or strip layup attempts",
            "tiers": TIERS,
        },
        "Interceptor": {
            "description": "The frequency of successfully tipped or intercepted passes greatly increases",
            "tiers": TIERS,
        },
        "High Flying Denier": {
            "description": "Boosts the speed and leaping ability of a defensive player in anticipation of a block attempt.",
            "tiers": TIERS,
        },
        "Immovable Enforcer": {
            "description": "Improves a defensive player's strength when defending ball handlers and finishers",
            "tiers": TIERS,
        },
        "Off Ball Pest": {
            "description": "Makes players more difficult to get past when playing off-ball, as they can grab and hold their matchup and don't get their ankles broken as often",
            "tiers": TIERS,
        },
        "On-Ball Menace": {
            "description": "Hounds and bodies up while defending on the perimeter.",
            "tiers": TIERS,
        },
        "Paint Patroller": {
            "description": "Increases a player's ability to block or contest shots at the rim.",
            "tiers": TIERS,
        },
        "Pick Dodger": {
            "description": "Improves a player's ability to navigate through and around screens while on defense. At the highest tier, can blow through screens in the park or blacktop",
            "tiers": TIERS,
        },
        "Post Lockdown": {
            "description": "Strengthens a player's ability to effectively defend moves in the post, with an increased chance at stripping the opponent",
            "tiers": TIERS,
        },
        "Clamps": {
            "description": "Increases a player's on-ball defensive stopping power against opposing ball handlers on the perimeter.",
            "tiers": TIERS,
        },
        "Chase Down Artist": {
            "description": "Improves a player's ability to catch up to and block a fast break layup or dunk attempt from behind.",
            "tiers": TIERS,
        },
        "Rim Protector": {
            "description": "Increases the effectiveness of contesting and blocking shots directly at the basket.",
            "tiers": TIERS,
        },
    },
    "Rebounding": {
        "Boxout Beast": {
            "description": "Improves a player's ability to box out and fight for good rebounding position",
            "tiers": TIERS,
        },
        "Rebound Chaser": {
            "description": "Improves a player's ability to track down rebounds from farther distances than normal",
            "tiers": TIERS,
        },
        "Brick Wall": {
            "description": "Increases the effectiveness of screens and drains energy from opponents on physical contact",
            "tiers": TIERS,
        },
        "Slippery Off Ball": {
            "description": "When attempting to get open off screens, the player more effectively navigates through traffic",
            "tiers": TIERS,
        },
        "Pogo Stick": {
            "description": "Allows players to quickly go back up for another jump upon landing. This could be after a rebound, block attempt, or even jumpshot",
            "tiers": TIERS,
        },
        "Box Vacuum": {
            "description": "Widens the area around the rim where a player can effectively box out a nearby opponent before a shot goes up.",
            "tiers": TIERS,
        },
    },
}


def get_badge(name):
    """Look up a badge by name across all categories. Returns None if not found."""
    for category in BADGES.values():
        if name in category:
            return category[name]
    return None


def all_badge_names():
    """Return a flat list of every badge name across all categories."""
    names = []
    for category in BADGES.values():
        names.extend(category.keys())
    return names


if __name__ == "__main__":
    total = sum(len(v) for v in BADGES.values())
    print(f"Total badges: {total}")
    for category, badges in BADGES.items():
        print(f"\n{category} ({len(badges)} badges):")
        for name in badges:
            print(f"  - {name}")