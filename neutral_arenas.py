"""
Neutral NBA venues: arenas that have hosted NBA games without being
any team's home arena (early neutral-site games, international games,
and temporary relocations like the 2023–2025 Las Vegas games).
"""

NEUTRAL_VENUES = {
    "Duquesne Gardens": {
        "location": "Pittsburgh, Pennsylvania",
        "dates": ["March 11, 1953"],
        "attendance": None,
    },
    "Civic Arena": {
        "location": "Pittsburgh, Pennsylvania",
        "dates": [
            "February 18, 1964", "December 14, 1964", "January 11, 1965",
            "February 15, 1966", "November 3, 1966", "January 5, 1967",
            "February 7, 1967", "February 24, 1967", "March 6, 1967",
            "December 7, 1972", "December 27, 1972", "January 12, 1973",
            "February 25, 1973", "March 11, 1973", "March 25, 1973",
        ],
        "attendance": None,
    },
    "Charleston Civic Center": {
        "location": "Charleston, West Virginia",
        "dates": ["December 6, 1965", "February 14, 1966"],
        "attendance": None,
    },
    "Mid-South Coliseum": {
        "location": "Memphis, Tennessee",
        "dates": [
            "December 19, 1966", "December 26, 1966", "January 2, 1967",
            "January 23, 1967", "January 30, 1967", "February 6, 1967",
            "February 13, 1967", "March 6, 1967", "March 13, 1967",
        ],
        "attendance": None,
    },
    "Curtis Hixon Hall": {
        "location": "Tampa, Florida",
        "dates": ["January 16, 1967"],
        "attendance": None,
    },
    "Greensboro Coliseum Complex": {
        "location": "Greensboro, North Carolina",
        "dates": ["January 30, 1967"],
        "attendance": 7168,
    },
    "St. Paul Auditorium": {
        "location": "Saint Paul, Minnesota",
        "dates": ["February 7, 1967"],
        "attendance": None,
    },
    "Tokyo Metropolitan Gymnasium": {
        "location": "Tokyo, Japan",
        "dates": ["November 2, 1990", "November 3, 1990"],
        "attendance": None,
    },
    "Yokohama Arena": {
        "location": "Yokohama, Japan",
        "dates": [
            "November 6, 1992", "November 7, 1992",
            "November 4, 1994", "November 5, 1994",
        ],
        "attendance": None,
    },
    "Tokyo Dome": {
        "location": "Tokyo, Japan",
        "dates": [
            "November 7, 1996", "November 9, 1996",
            "November 6, 1999", "November 7, 1999",
        ],
        "attendance": None,
    },
    "Palacio de los Deportes": {
        "location": "Mexico City, Mexico",
        "dates": ["December 7, 1997"],
        "attendance": None,
    },
    "Saitama Super Arena": {
        "location": "Saitama, Japan",
        "dates": ["October 30, 2003", "November 1, 2003"],
        "attendance": None,
    },
    "The O2 Arena": {
        "location": "London, United Kingdom",
        "dates": [
            "March 4, 2011", "March 5, 2011", "January 17, 2013",
            "January 16, 2014", "January 15, 2015", "January 14, 2016",
            "January 12, 2017", "January 11, 2018", "January 17, 2019",
            "January 18, 2026",
        ],
        "attendance": None,
    },
    "Bell Centre": {
        "location": "Montreal, Quebec",
        "dates": [
            "October 19, 2012", "October 20, 2013", "October 24, 2014",
            "October 23, 2015", "October 10, 2018", "October 14, 2022",
            "October 12, 2023", "October 6, 2024",
        ],
        "attendance": None,
    },
    "MTS Centre": {
        "location": "Winnipeg, Manitoba",
        "dates": ["October 24, 2012", "October 10, 2015"],
        "attendance": None,
    },
    "Mexico City Arena": {
        "location": "Mexico City, Mexico",
        "dates": [
            "November 12, 2014", "December 3, 2015", "January 12, 2017",
            "January 14, 2017", "December 7, 2017", "December 9, 2017",
            "December 13, 2018", "December 15, 2018", "December 12, 2019",
            "December 14, 2019", "November 9, 2023", "November 2, 2024",
            "November 1, 2025",
        ],
        "attendance": None,
    },
    "Canadian Tire Centre": {
        "location": "Ottawa, Ontario",
        "dates": ["October 14, 2015"],
        "attendance": None,
    },
    "Scotiabank Saddledome": {
        "location": "Calgary, Alberta",
        "dates": ["October 3, 2016"],
        "attendance": None,
    },
    "Accor Arena": {
        "location": "Paris, France",
        "dates": [
            "January 24, 2020", "January 19, 2023", "January 11, 2024",
            "January 23, 2025", "January 25, 2025",
        ],
        "attendance": None,
    },
    "ESPN Wide World of Sports Complex": {
        "location": "Bay Lake, Florida",
        "dates": ["July 30 – October 11, 2020"],
        "attendance": None,
    },
    "Rogers Place": {
        "location": "Edmonton, Alberta",
        "dates": ["October 2, 2022"],
        "attendance": None,
    },
    "T-Mobile Arena": {
        "location": "Paradise, Nevada",
        "dates": [
            "December 7–9, 2023", "December 14–17, 2024", "December 13–16, 2025",
        ],
        "attendance": 17427,
    },
    "Uber Arena": {
        "location": "Berlin, Germany",
        "dates": ["January 15, 2026"],
        "attendance": None,
    },
}


if __name__ == "__main__":
    print(f"Total neutral venues: {len(NEUTRAL_VENUES)}")
    for name, info in NEUTRAL_VENUES.items():
        print(f"{name} ({info['location']}): {len(info['dates'])} date entries")