"""
Random in-game events for the NBA game.

Each event has a description, a rough chance of firing (weight, used
for random selection - higher numbers are more common), and an
effect tag your game logic can key off of.
"""

EVENTS = {
    "Milestones": {
        "Rookie Debut": {
            "description": "A rookie makes their first career NBA appearance.",
            "weight": 8,
            "effect": "morale_boost",
        },
        "Season Debut": {
            "description": "A player returns for their first game of the season.",
            "weight": 10,
            "effect": "morale_boost",
        },
        "Career High": {
            "description": "A player sets a new career-high in points, rebounds, or assists.",
            "weight": 6,
            "effect": "stat_boost",
        },
        "Triple Double": {
            "description": "A player racks up double digits in three statistical categories.",
            "weight": 4,
            "effect": "morale_boost",
        },
        "1000th Career Game": {
            "description": "A veteran suits up for their 1,000th career NBA game.",
            "weight": 1,
            "effect": "legacy_boost",
        },
        "10,000 Point Club": {
            "description": "A player crosses the 10,000-point mark for their career.",
            "weight": 1,
            "effect": "legacy_boost",
        },
        "Jersey Retirement": {
            "description": "A franchise legend's jersey is retired in a pregame ceremony.",
            "weight": 1,
            "effect": "legacy_boost",
        },
    },
    "Streaks": {
        "Hot Start": {
            "description": "A team opens the game on a quick scoring run.",
            "weight": 10,
            "effect": "momentum_boost",
        },
        "10-0 Run": {
            "description": "A team is riding a 10-0 scoring run and has a chance to extend it.",
            "weight": 6,
            "effect": "momentum_boost",
        },
        "Winning Streak on the Line": {
            "description": "A team enters the game with a winning streak that could be extended or snapped.",
            "weight": 5,
            "effect": "pressure",
        },
        "Losing Skid": {
            "description": "A team is mired in a losing streak and desperate to turn things around.",
            "weight": 5,
            "effect": "pressure",
        },
        "Cold Shooting Night": {
            "description": "A player or team can't buy a bucket and is shooting well below their average.",
            "weight": 6,
            "effect": "stat_penalty",
        },
        "Shutdown Defense": {
            "description": "A defense locks in and holds the opponent scoreless for an extended stretch.",
            "weight": 5,
            "effect": "defense_boost",
        },
    },
    "Rivalry": {
        "Rivalry Game": {
            "description": "The two teams share a storied rivalry, raising the stakes and intensity.",
            "weight": 4,
            "effect": "intensity_boost",
        },
        "Revenge Game": {
            "description": "A player faces off against their former team for the first time.",
            "weight": 3,
            "effect": "morale_boost",
        },
        "Playoff Rematch": {
            "description": "The two teams meet again after a recent playoff series between them.",
            "weight": 2,
            "effect": "intensity_boost",
        },
        "Trash Talk": {
            "description": "Two players exchange words after a hard foul or big play, sparking tension.",
            "weight": 5,
            "effect": "intensity_boost",
        },
        "Bad Blood Ejection": {
            "description": "A rivalry-fueled scuffle results in a player getting ejected.",
            "weight": 1,
            "effect": "player_removed",
        },
    },
    "Injury": {
        "Minor Tweak": {
            "description": "A player tweaks something minor and plays through it at reduced effectiveness.",
            "weight": 5,
            "effect": "stat_penalty",
        },
        "Left the Game": {
            "description": "A player is forced to leave the game early due to injury.",
            "weight": 2,
            "effect": "player_removed",
        },
        "Questionable Return": {
            "description": "A player who left with an injury is questionable to return later in the game.",
            "weight": 2,
            "effect": "uncertain",
        },
    },
    "Morale": {
        "Home Crowd Roar": {
            "description": "The home crowd erupts, giving the home team an energy boost.",
            "weight": 7,
            "effect": "morale_boost",
        },
        "Clutch Moment": {
            "description": "The game is close in the final minutes and a player has a chance to be the hero.",
            "weight": 6,
            "effect": "pressure",
        },
        "Coach's Challenge": {
            "description": "A coach challenges a call, which can swing momentum depending on the result.",
            "weight": 3,
            "effect": "uncertain",
        },
        "Bench Mob Spark": {
            "description": "A team's bench unit comes in and sparks a run of their own.",
            "weight": 5,
            "effect": "momentum_boost",
        },
        "Technical Foul": {
            "description": "A player picks up a technical foul after arguing a call, fueling the opponent.",
            "weight": 3,
            "effect": "momentum_shift",
        },
    },
    "Media": {
        "Trade Rumor": {
            "description": "Trade rumors swirl around a player during the game, affecting focus.",
            "weight": 2,
            "effect": "stat_penalty",
        },
        "Nationally Televised Game": {
            "description": "The game is on national TV, and some players elevate their performance under the spotlight.",
            "weight": 4,
            "effect": "stat_boost",
        },
        "MVP Chatter": {
            "description": "A player's MVP case is a hot topic heading into the game.",
            "weight": 2,
            "effect": "morale_boost",
        },
    },
}


def get_event(name):
    """Look up an event by name across all categories. Returns None if not found."""
    for category in EVENTS.values():
        if name in category:
            return category[name]
    return None


def all_event_names():
    """Return a flat list of every event name across all categories."""
    names = []
    for category in EVENTS.values():
        names.extend(category.keys())
    return names


def random_event(category=None):
    """Pick a random event, weighted by each event's 'weight' value.
    Pass a category name to restrict the pool, e.g. random_event('Rivalry').
    """
    import random

    if category:
        pool = EVENTS[category]
    else:
        pool = {}
        for events in EVENTS.values():
            pool.update(events)

    names = list(pool.keys())
    weights = [pool[name]["weight"] for name in names]
    chosen = random.choices(names, weights=weights, k=1)[0]
    return chosen, pool[chosen]


if __name__ == "__main__":
    total = sum(len(v) for v in EVENTS.values())
    print(f"Total events: {total}")
    for category, events in EVENTS.items():
        print(f"\n{category} ({len(events)} events):")
        for name in events:
            print(f"  - {name}")

    name, event = random_event()
    print(f"\nRandom event: {name} -> {event['description']}")