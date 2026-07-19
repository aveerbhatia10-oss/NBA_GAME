"""
Former NBA arenas.

FORMER_ARENAS is keyed by each team's current name and holds a list
of every arena the franchise has called home in the past (including
arenas used under earlier team names, e.g. Sacramento Kings includes
their Kansas City, Cincinnati, and Rochester days).

DEFUNCT_TEAM_ARENAS covers arenas used by teams that no longer exist.
"""

FORMER_ARENAS = {
    "Boston Celtics": [
        {"arena": "Hartford Civic Center (XL Center / PeoplesBank Arena)", "years_used": "1975–1995 (occasionally for home games)", "capacity": 16294, "opened": 1975, "location": "Hartford, Connecticut"},
        {"arena": "Boston Garden (Boston Madison Square Garden, 1928)", "years_used": "1946–1995", "capacity": 14890, "opened": 1928, "location": "Boston, Massachusetts"},
        {"arena": "Boston Arena (Matthews Arena)", "years_used": "1946–1947 (partial schedule)", "capacity": "5,900s", "opened": 1910, "location": "Boston, Massachusetts"},
    ],
    "Brooklyn Nets": [
        {"arena": "Prudential Center", "years_used": "2010–2012", "capacity": 18711, "opened": 2007, "location": "Newark, New Jersey"},
        {"arena": "Izod Center (Meadowlands Arena / Continental Airlines Arena / Brendan Byrne Arena)", "years_used": "1981–2010", "capacity": 20049, "opened": 1981, "location": "East Rutherford, New Jersey"},
        {"arena": "Rutgers Athletic Center (Louis Brown Athletic Center)", "years_used": "1977–1981", "capacity": 8500, "opened": 1977, "location": "Piscataway, New Jersey"},
        {"arena": "Nassau Coliseum", "years_used": "1972–1977", "capacity": 14890, "opened": 1972, "location": "Uniondale, New York"},
        {"arena": "Island Garden", "years_used": "1969–1972", "capacity": 5200, "opened": 1956, "location": "West Hempstead, New York"},
        {"arena": "Long Island Arena (Commack Arena)", "years_used": "1968–1969", "capacity": 6000, "opened": 1957, "location": "Commack, New York"},
        {"arena": "Teaneck Armory", "years_used": "1967–1968", "capacity": 5500, "opened": 1936, "location": "Teaneck, New Jersey"},
    ],
    "New York Knicks": [
        {"arena": "Madison Square Garden (III)", "years_used": "1946–1968", "capacity": 16000, "opened": 1925, "location": "New York City, New York"},
        {"arena": "69th Regiment Armory", "years_used": "1946–1960 (partial schedule)", "capacity": 5000, "opened": 1906, "location": "New York City, New York"},
    ],
    "Philadelphia 76ers": [
        {"arena": "The Spectrum (Wachovia Spectrum / First Union Spectrum / CoreStates Spectrum)", "years_used": "1967–1996", "capacity": 18176, "opened": 1967, "location": "Philadelphia, Pennsylvania"},
        {"arena": "Municipal Auditorium", "years_used": "1963–1967", "capacity": 12000, "opened": 1930, "location": "Syracuse, New York"},
        {"arena": "Philadelphia Arena", "years_used": None, "capacity": 7000, "opened": 1920, "location": "Philadelphia, Pennsylvania"},
        {"arena": "Onondaga War Memorial", "years_used": "1951–1963", "capacity": 6230, "opened": 1951, "location": "Syracuse, New York"},
        {"arena": "State Fair Coliseum", "years_used": "1949–1951", "capacity": 7500, "opened": 1927, "location": "Syracuse, New York"},
    ],
    "Toronto Raptors": [
        {"arena": "Benchmark International Arena (Amalie Arena / Tampa Bay Times Forum / St. Pete Times Forum / Ice Palace)", "years_used": "2020–2021", "capacity": 20500, "opened": 1996, "location": "Tampa, Florida"},
        {"arena": "SkyDome (Rogers Centre)", "years_used": "1995–1999", "capacity": 28708, "opened": 1989, "location": "Toronto, Ontario"},
        {"arena": "Maple Leaf Gardens", "years_used": "1997–1999 (for six home games)", "capacity": 17000, "opened": 1931, "location": "Toronto, Ontario"},
        {"arena": "Copps Coliseum (TD Coliseum / Hamilton Arena / FirstOntario Centre)", "years_used": "1995–1998 (for three home games)", "capacity": 18800, "opened": 1985, "location": "Hamilton, Ontario"},
    ],
    "Atlanta Hawks": [
        {"arena": "Georgia Dome", "years_used": "1997–1999 (partial schedule, primary stadium)", "capacity": 71228, "opened": 1992, "location": "Atlanta, Georgia"},
        {"arena": "Lakefront Arena", "years_used": "1984–1985 (partial schedule)", "capacity": 8933, "opened": 1983, "location": "New Orleans, Louisiana"},
        {"arena": "Omni Coliseum", "years_used": "1972–1997", "capacity": 16378, "opened": 1972, "location": "Atlanta, Georgia"},
        {"arena": "Alexander Memorial Coliseum (Hank McCamish Pavilion)", "years_used": "1997–1999 (partial, secondary stadium); 1968–1972", "capacity": 9191, "opened": 1956, "location": "Atlanta, Georgia"},
        {"arena": "Kiel Auditorium", "years_used": "1955–1968", "capacity": 9300, "opened": 1934, "location": "St. Louis, Missouri"},
        {"arena": "St. Louis Arena (The Checkerdome)", "years_used": "1955–1968 (partial)", "capacity": 20000, "opened": 1929, "location": "St. Louis, Missouri"},
        {"arena": "Milwaukee Arena (UW–Milwaukee Panther Arena / U.S. Cellular Arena / MECCA Arena)", "years_used": "1951–1955", "capacity": 10783, "opened": 1950, "location": "Milwaukee, Wisconsin"},
        {"arena": "Wharton Field House", "years_used": "1946–1951", "capacity": 6000, "opened": 1928, "location": "Moline, Illinois"},
    ],
    "Charlotte Hornets": [
        {"arena": "Charlotte Coliseum", "years_used": "1988–2002 (original Hornets); 2004–2005 (Bobcats)", "capacity": 24042, "opened": 1988, "location": "Charlotte, North Carolina"},
    ],
    "Miami Heat": [
        {"arena": "Miami Arena", "years_used": "1988–1999", "capacity": 15200, "opened": 1988, "location": "Miami, Florida"},
    ],
    "Orlando Magic": [
        {"arena": "Amway Arena (The Arena in Orlando / TD Waterhouse Centre / Orlando Arena)", "years_used": "1989–2010", "capacity": 17283, "opened": 1989, "location": "Orlando, Florida"},
    ],
    "Washington Wizards": [
        {"arena": "US Airways Arena (Capital Centre)", "years_used": "1973–1997", "capacity": 18756, "opened": 1973, "location": "Lake Arbor, Maryland"},
        {"arena": "Baltimore Civic Center (CFG Bank Arena / Royal Farms Arena / 1st Mariner Arena / Baltimore Arena)", "years_used": "1989–1997 (partial schedule); 1963–1973", "capacity": 11271, "opened": 1962, "location": "Baltimore, Maryland"},
        {"arena": "Chicago Coliseum", "years_used": "1962–1963", "capacity": 7000, "opened": 1899, "location": "Chicago, Illinois"},
        {"arena": "International Amphitheatre", "years_used": "1961–1962", "capacity": 9000, "opened": 1934, "location": "Chicago, Illinois"},
    ],
    "Chicago Bulls": [
        {"arena": "Chicago Stadium", "years_used": "1967–1994", "capacity": 18676, "opened": 1929, "location": "Chicago, Illinois"},
        {"arena": "International Amphitheatre", "years_used": "1966–1967", "capacity": 9000, "opened": 1934, "location": "Chicago, Illinois"},
    ],
    "Cleveland Cavaliers": [
        {"arena": "Richfield Coliseum", "years_used": "1974–1994", "capacity": 20273, "opened": 1974, "location": "Richfield, Ohio"},
        {"arena": "Cleveland Arena", "years_used": "1970–1974", "capacity": 10000, "opened": 1937, "location": "Cleveland, Ohio"},
    ],
    "Detroit Pistons": [
        {"arena": "The Palace of Auburn Hills", "years_used": "1988–2017", "capacity": 22076, "opened": 1988, "location": "Auburn Hills, Michigan"},
        {"arena": "Joe Louis Arena", "years_used": "1984–1985 (partial schedule)", "capacity": 20153, "opened": 1979, "location": "Detroit, Michigan"},
        {"arena": "Pontiac Silverdome (Pontiac Metropolitan Stadium)", "years_used": "1978–1988", "capacity": 33000, "opened": 1975, "location": "Pontiac, Michigan"},
        {"arena": "Cobo Arena", "years_used": "1961–1978", "capacity": 12191, "opened": 1960, "location": "Detroit, Michigan"},
        {"arena": "Olympia Stadium", "years_used": "1957–1961", "capacity": 15000, "opened": 1927, "location": "Detroit, Michigan"},
        {"arena": "War Memorial Coliseum", "years_used": "1952–1957", "capacity": 10000, "opened": 1952, "location": "Fort Wayne, Indiana"},
        {"arena": "North Side High School Gym", "years_used": "1948–1952", "capacity": 3000, "opened": 1927, "location": "Fort Wayne, Indiana"},
    ],
    "Indiana Pacers": [
        {"arena": "Market Square Arena", "years_used": "1974–1999", "capacity": 16530, "opened": 1974, "location": "Indianapolis, Indiana"},
        {"arena": "Indiana State Fairgrounds Coliseum (Corteva Coliseum / Indiana Farmers Coliseum / Pepsi Coliseum)", "years_used": "1967–1974", "capacity": 10000, "opened": 1939, "location": "Indianapolis, Indiana"},
    ],
    "Milwaukee Bucks": [
        {"arena": "Bradley Center (BMO Harris Bradley Center)", "years_used": "1988–2018", "capacity": 18717, "opened": 1988, "location": "Milwaukee, Wisconsin"},
        {"arena": "MECCA Arena (UW–Milwaukee Panther Arena / U.S. Cellular Arena / Milwaukee Arena)", "years_used": "1968–1988", "capacity": 10783, "opened": 1950, "location": "Milwaukee, Wisconsin"},
    ],
    "Dallas Mavericks": [
        {"arena": "Reunion Arena", "years_used": "1980–2001", "capacity": 18293, "opened": 1980, "location": "Dallas, Texas"},
    ],
    "Houston Rockets": [
        {"arena": "The Summit (Lakewood Church Central Campus / Compaq Center)", "years_used": "1975–2003", "capacity": 16285, "opened": 1975, "location": "Houston, Texas"},
        {"arena": "Hofheinz Pavilion (Fertitta Center)", "years_used": "1971–1975", "capacity": 10000, "opened": 1969, "location": "Houston, Texas"},
        {"arena": "San Diego Sports Arena (Pechanga Arena / Valley View Casino Center)", "years_used": "1967–1971", "capacity": 14500, "opened": 1966, "location": "San Diego, California"},
    ],
    "Memphis Grizzlies": [
        {"arena": "Pyramid Arena", "years_used": "2001–2004", "capacity": 20142, "opened": 1991, "location": "Memphis, Tennessee"},
        {"arena": "General Motors Place (Rogers Arena)", "years_used": "1995–2001", "capacity": 19193, "opened": 1995, "location": "Vancouver, British Columbia"},
    ],
    "New Orleans Pelicans": [
        {"arena": "Ford Center (Paycom Center / Chesapeake Energy Arena / Oklahoma City Arena)", "years_used": "2005–2007 (bulk of schedule)", "capacity": 19164, "opened": 2002, "location": "Oklahoma City, Oklahoma"},
    ],
    "San Antonio Spurs": [
        {"arena": "Alamodome", "years_used": "1993–2002", "capacity": 20557, "opened": 1993, "location": "San Antonio, Texas"},
        {"arena": "HemisFair Arena", "years_used": "1973–1993", "capacity": 16057, "opened": 1968, "location": "San Antonio, Texas"},
        {"arena": "Lubbock Municipal Coliseum (City Bank Coliseum)", "years_used": "1970–1971 (partial schedule)", "capacity": 11200, "opened": 1956, "location": "Lubbock, Texas"},
        {"arena": "Tarrant County Convention Center", "years_used": "1970–1971 (partial schedule)", "capacity": 16057, "opened": 1968, "location": "Fort Worth, Texas"},
        {"arena": "Moody Coliseum", "years_used": "1967–1973", "capacity": 8998, "opened": 1956, "location": "University Park, Texas"},
        {"arena": "Dallas Memorial Auditorium (Kay Bailey Hutchison Convention Center)", "years_used": "1967–1973", "capacity": 9815, "opened": 1957, "location": "Dallas, Texas"},
    ],
    "Denver Nuggets": [
        {"arena": "McNichols Sports Arena", "years_used": "1975–1999", "capacity": 17171, "opened": 1975, "location": "Denver, Colorado"},
        {"arena": "Denver Auditorium Arena", "years_used": "1967–1975", "capacity": 6841, "opened": 1908, "location": "Denver, Colorado"},
        {"arena": "Denver Coliseum", "years_used": "1967–1970 (partial schedule)", "capacity": 9000, "opened": 1950, "location": "Denver, Colorado"},
    ],
    "Minnesota Timberwolves": [
        {"arena": "Hubert H. Humphrey Metrodome", "years_used": "1989–1990", "capacity": 50000, "opened": 1982, "location": "Minneapolis, Minnesota"},
    ],
    "Oklahoma City Thunder": [
        {"arena": "KeyArena at Seattle Center (Climate Pledge Arena / Seattle Center Coliseum)", "years_used": "1995–2008; 1985–1994; 1967–1978", "capacity": 17072, "opened": 1962, "location": "Seattle, Washington"},
        {"arena": "Tacoma Dome", "years_used": "1994–1995", "capacity": 17100, "opened": 1983, "location": "Tacoma, Washington"},
        {"arena": "Kingdome", "years_used": "1978–1985", "capacity": 59166, "opened": 1976, "location": "Seattle, Washington"},
    ],
    "Portland Trail Blazers": [
        {"arena": "Memorial Coliseum (Veterans Memorial Coliseum)", "years_used": "1970–1995", "capacity": 12888, "opened": 1960, "location": "Portland, Oregon"},
    ],
    "Utah Jazz": [
        {"arena": "Salt Palace", "years_used": "1979–1991", "capacity": 12686, "opened": 1969, "location": "Salt Lake City, Utah"},
        {"arena": "Thomas & Mack Center", "years_used": "1983–1984 (partial schedule)", "capacity": 18500, "opened": 1983, "location": "Paradise, Nevada"},
        {"arena": "Louisiana Superdome (Caesars Superdome / Mercedes-Benz Superdome)", "years_used": "1975–1979", "capacity": 55675, "opened": 1975, "location": "New Orleans, Louisiana"},
        {"arena": "Loyola Field House", "years_used": "1974–1975 (partial schedule)", "capacity": 6500, "opened": 1950, "location": "New Orleans, Louisiana"},
        {"arena": "Municipal Auditorium", "years_used": "1974–1975", "capacity": 7853, "opened": 1934, "location": "New Orleans, Louisiana"},
    ],
    "Golden State Warriors": [
        {"arena": "Oracle Arena (Oakland Arena / The Arena in Oakland / Oakland-Alameda County Coliseum)", "years_used": "1971–1996; 1997–2019", "capacity": 19596, "opened": 1971, "location": "Oakland, California"},
        {"arena": "San Jose Arena (SAP Center at San Jose / HP Pavilion / Compaq Center at San Jose)", "years_used": "1996–1997", "capacity": 18500, "opened": 1993, "location": "San Jose, California"},
        {"arena": "USF War Memorial Gymnasium", "years_used": "1962–1965", "capacity": 5300, "opened": 1958, "location": "San Francisco, California"},
        {"arena": "San Francisco Civic Auditorium (Bill Graham Civic Auditorium)", "years_used": "1968–1971; 1964–1967", "capacity": 7000, "opened": 1915, "location": "San Francisco, California"},
        {"arena": "Cow Palace", "years_used": "1966–1971; 1962–1964", "capacity": 12953, "opened": 1941, "location": "Daly City, California"},
        {"arena": "Municipal Auditorium", "years_used": "1952–1962", "capacity": 12000, "opened": 1930, "location": "Philadelphia, Pennsylvania"},
        {"arena": "Philadelphia Arena", "years_used": "1946–1962 (partial schedule 1952–1962)", "capacity": 7000, "opened": 1920, "location": "Philadelphia, Pennsylvania"},
    ],
    "Los Angeles Clippers": [
        {"arena": "Crypto.com Arena (Staples Center)", "years_used": "1999–2024", "capacity": 19067, "opened": 1999, "location": "Los Angeles, California"},
        {"arena": "Arrowhead Pond of Anaheim (Honda Center / Pond of Anaheim)", "years_used": "1994–1999 (partial schedule)", "capacity": 18336, "opened": 1993, "location": "Anaheim, California"},
        {"arena": "Los Angeles Memorial Sports Arena", "years_used": "1984–1999", "capacity": 16161, "opened": 1959, "location": "Los Angeles, California"},
        {"arena": "San Diego Sports Arena (Pechanga Arena / Valley View Casino Center)", "years_used": "1978–1984", "capacity": 14500, "opened": 1966, "location": "San Diego, California"},
        {"arena": "Maple Leaf Gardens", "years_used": "1971–1975 (16 home games)", "capacity": 15000, "opened": 1931, "location": "Toronto, Ontario"},
        {"arena": "Buffalo Memorial Auditorium", "years_used": "1970–1978", "capacity": 15280, "opened": 1940, "location": "Buffalo, New York"},
    ],
    "Los Angeles Lakers": [
        {"arena": "The Forum (Kia Forum / Great Western Forum)", "years_used": "1967–1999", "capacity": 17505, "opened": 1967, "location": "Inglewood, California"},
        {"arena": "Long Beach Arena", "years_used": "1967 (when locked out of Sports Arena)", "capacity": 13609, "opened": 1962, "location": "Long Beach, California"},
        {"arena": "Los Angeles Memorial Sports Arena", "years_used": "1960–1967", "capacity": 16161, "opened": 1959, "location": "Los Angeles, California"},
        {"arena": "Minneapolis Armory", "years_used": "1959–1960; 1947–1959 (partial schedule)", "capacity": 10000, "opened": 1936, "location": "Minneapolis, Minnesota"},
        {"arena": "Minneapolis Auditorium", "years_used": "1947–1959", "capacity": 10000, "opened": 1927, "location": "Minneapolis, Minnesota"},
    ],
    "Phoenix Suns": [
        {"arena": "Arizona Veterans Memorial Coliseum", "years_used": "1968–1992", "capacity": 14870, "opened": 1965, "location": "Phoenix, Arizona"},
    ],
    "Sacramento Kings": [
        {"arena": "Sleep Train Arena (Power Balance Pavilion / ARCO Arena II)", "years_used": "1988–2016", "capacity": 17317, "opened": 1988, "location": "Sacramento, California"},
        {"arena": "ARCO Arena I (Sacramento Sports Arena)", "years_used": "1985–1988", "capacity": 10333, "opened": 1985, "location": "Sacramento, California"},
        {"arena": "Kemper Arena (Hy-Vee Arena / Mosaic Arena)", "years_used": "1974–1985", "capacity": 16700, "opened": 1974, "location": "Kansas City, Missouri"},
        {"arena": "Omaha Civic Auditorium", "years_used": "1972–1978 (partial schedule)", "capacity": 9300, "opened": 1954, "location": "Omaha, Nebraska"},
        {"arena": "Municipal Auditorium", "years_used": "1972–1974", "capacity": 9287, "opened": 1936, "location": "Kansas City, Missouri"},
        {"arena": "Cincinnati Gardens", "years_used": "1957–1972", "capacity": 11000, "opened": 1949, "location": "Cincinnati, Ohio"},
        {"arena": "Rochester Community War Memorial (Blue Cross Arena at War Memorial)", "years_used": "1955–1957", "capacity": 12428, "opened": 1955, "location": "Rochester, New York"},
        {"arena": "Edgerton Park Arena", "years_used": "1945–1955", "capacity": 4200, "opened": 1892, "location": "Rochester, New York"},
    ],
}

# Arenas used by teams that no longer exist (folded, merged, or relocated
# out of the NBA entirely).
DEFUNCT_TEAM_ARENAS = {
    "Anderson Packers": [
        {"arena": "The Wigwam", "years_used": "1949–1950", "capacity": 8996, "opened": 1925, "location": "Anderson, Indiana"},
    ],
    "Baltimore Bullets (1944–1954)": [
        {"arena": "Baltimore Coliseum", "years_used": "1944–1954", "capacity": 4500, "opened": 1930, "location": "Baltimore, Maryland"},
    ],
    "Chicago Stags": [
        {"arena": "Chicago Stadium", "years_used": "1946–1950", "capacity": 18676, "opened": 1929, "location": "Chicago, Illinois"},
    ],
    "Cleveland Rebels": [
        {"arena": "Cleveland Arena", "years_used": "1946–1947", "capacity": 10000, "opened": 1937, "location": "Cleveland, Ohio"},
    ],
    "Denver Nuggets (1948–1950)": [
        {"arena": "Denver Auditorium Arena", "years_used": "1948–1950", "capacity": 12000, "opened": 1908, "location": "Denver, Colorado"},
    ],
    "Detroit Falcons": [
        {"arena": "Detroit Olympia", "years_used": "1946–1947", "capacity": 15000, "opened": 1927, "location": "Detroit, Michigan"},
    ],
    "Indianapolis Jets / Kautskys": [
        {"arena": "Hinkle Fieldhouse", "years_used": "1948–1949", "capacity": 15000, "opened": 1928, "location": "Indianapolis, Indiana"},
    ],
    "Indianapolis Olympians": [
        {"arena": "Hinkle Fieldhouse", "years_used": "1949–1953", "capacity": 15000, "opened": 1928, "location": "Indianapolis, Indiana"},
    ],
    "Pittsburgh Ironmen": [
        {"arena": "Duquesne Gardens", "years_used": "1946–1947", "capacity": 6500, "opened": 1890, "location": "Pittsburgh, Pennsylvania"},
    ],
    "Providence Steamrollers": [
        {"arena": "Rhode Island Auditorium", "years_used": "1946–1949", "capacity": 5300, "opened": 1926, "location": "Providence, Rhode Island"},
    ],
    "Sheboygan Redskins / Enzo Jels": [
        {"arena": "Sheboygan Municipal Auditorium and Armory", "years_used": "1942–1951", "capacity": 3500, "opened": 1942, "location": "Sheboygan, Wisconsin"},
        {"arena": "Eagle Auditorium", "years_used": "1938–1942", "capacity": 1200, "opened": None, "location": "Sheboygan, Wisconsin"},
    ],
    "St. Louis Bombers": [
        {"arena": "St. Louis Arena (The Checkerdome)", "years_used": "1946–1950", "capacity": 15000, "opened": 1929, "location": "St. Louis, Missouri"},
    ],
    "Toronto Huskies": [
        {"arena": "Maple Leaf Gardens", "years_used": "1946–1947", "capacity": 15000, "opened": 1931, "location": "Toronto, Ontario"},
    ],
    "Washington Capitols": [
        {"arena": "Uline Arena (Washington Coliseum)", "years_used": "1946–1951", "capacity": 7000, "opened": 1941, "location": "Washington, D.C."},
    ],
    "Waterloo Hawks": [
        {"arena": "The Hippodrome", "years_used": "1948–1951", "capacity": 5155, "opened": 1936, "location": "Waterloo, Iowa"},
    ],
}


if __name__ == "__main__":
    total_former = sum(len(v) for v in FORMER_ARENAS.values())
    total_defunct = sum(len(v) for v in DEFUNCT_TEAM_ARENAS.values())
    print(f"Current teams with former arenas: {len(FORMER_ARENAS)} teams, {total_former} arena entries")
    print(f"Defunct teams: {len(DEFUNCT_TEAM_ARENAS)} teams, {total_defunct} arena entries")