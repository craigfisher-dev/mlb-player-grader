import streamlit as st
import statsapi

player_name = input("What current player would you like to look up? \n")

number_list_count = 1

players_ID_And_Name_Cache = []

player_grades = []

# used to debug any player 
# for player in statsapi.lookup_player("ohtani"):
#     print(player) 


while (True):
    player_results = statsapi.lookup_player(player_name)
    # If there are results
    if (player_results):
        # Gets the player with same name as input
        for player in statsapi.lookup_player(player_name):
            print(f"{number_list_count}. {player['fullName']}")
            players_ID_And_Name_Cache.append([player['id'], player['fullName']])
            number_list_count += 1
        break
    # If no results
    else:
        print("No player found, please try again.")
        player_name = input("What current player would you like to look up? \n")

# Needed for try expect to work
list_number = -1

# Need to index the array at 0 so need to subtract 1
try:
    list_number = int(input("Please enter a valid number? \n")) - 1
except:
    print("\nYour response needs to be a number\n")

while (True):
    # Checks if number is a valid number
    if (list_number >= 0 and list_number < len(players_ID_And_Name_Cache)):
        users_player_id = players_ID_And_Name_Cache[list_number][0]
        user_player_name = players_ID_And_Name_Cache[list_number][1]
        break
    else:
        try:
            list_number = int(input("Please enter a valid number? \n")) - 1
        except:
            print("\nYour response needs to be a number\n")

#             
print(f"Here is the Id of your player {users_player_id}")

# All Stats
player_Stats = statsapi.player_stats(users_player_id, season='current')

# Just there hitting stats - It is a string
player_Hitting_Stats = statsapi.player_stats(users_player_id, group='hitting', season='current')

split_String = player_Hitting_Stats.split(':')


# print(player_Hitting_Stats)

# Testing function used to find any stat you want to save for later and where it is indexed
# i = 0

# for item in split_String:
#     print(f"{i} {item}")
#     i += 1

# print(len(split_String))



# Some way to parse all the data to just get the 3 stats I need - Just for batting can be extended to work with other stats later
# Should take in a players_stats

try:
    ba = split_String[13].split('\n')[0]
    ba = ba[1:]
    print(f"BA: {ba}")
except:
    print("Player has no hitting Stats this season")
    # Ends program if player has no hitting stats
    exit()

try:
    obp = split_String[15].split('\n')[0]
    obp = obp[1:]
    print(f"obp: {obp}")
except:
    print("Player has no hitting Stats this season")
    # Ends program if player has no hitting stats
    exit()

try:
    ops = split_String[17].split('\n')[0]
    ops = ops[1:]
    print(f"ops: {ops}")
except:
    print("Player has no hitting Stats this season")
    # Ends program if player has no hitting stats
    exit()




# 1 function to tally up the points and give a letter grade based on points

# BA (Batting Average) (Ranking) - 30 points max
# Rating for how good a hitter is at making contact for a basehit
# S+: .300+ (30 points) (elite)
# S: .280+ (25 points) (great)
# A: .265+ (23 points) (above average)
# B: .255+ (18 points) (slightly above average)
# C: .246+ (15 points) (league average)
# D: .225+ (11 points) (below average)
# F: Below .225 (7 points) (poor)

def get_ba_points(ba_value):
    if ba_value >= 0.300:
        return 30, "S+", 6
    elif ba_value >= 0.280:
        return 22, "S", 5
    elif ba_value >= 0.265:
        return 20, "A", 4
    elif ba_value >= 0.255:
        return 18, "B", 3
    elif ba_value >= 0.246:
        return 15, "C", 2
    elif ba_value >= 0.225:
        return 8, "D", 1
    else:
        return 4, "F", 0

# OBP (On Base Percentage) (Ranking) - 30 points max
# Rating for plate discipline and getting on base
# S+: .375+ (30 points) (elite)
# S: .360+ (25 points) (great) 
# A: .345+ (23 points) (above average)
# B: .330+ (18 points) (slightly above average) 
# C: .316+ (15 points) (league average)
# D: .285+ (11 points) (below average)
# F: Below .285 (7 points) (poor)

def get_obp_points(obp_value):
    if obp_value >= 0.375:
        return 30, "S+", 6
    elif obp_value >= 0.360:
        return 22, "S", 5
    elif obp_value >= 0.345:
        return 20, "A", 4
    elif obp_value >= 0.330:
        return 18, "B", 3
    elif obp_value >= 0.300:
        return 15, "C", 2
    elif obp_value >= 0.270:
        return 8, "D", 1
    else:
        return 4, "F", 0


# OPS (On-Base + Slugging Percentage) (Ranking) - 80 points max
# Rating for combined power and on-base ability
# S+: .900+ (80 points) (elite)
# S: .850+ (70 points) (great)
# A: .800+ (60 points) (above average)
# B: .750+ (50 points) (slightly above average)
# C: .700+ (40 points) (league average)
# D: .650+ (30 points) (below average)
# F: Below .650 (20 points) (poor)

def get_ops_points(ops_value):
    if ops_value >= 0.880:
        return 80, "S+", 6
    elif ops_value >= 0.830:
        return 68, "S", 5
    elif ops_value >= 0.780:
        return 59, "A", 4
    elif ops_value >= 0.740:
        return 50, "B", 3
    elif ops_value >= 0.660:
        return 40, "C", 2
    elif ops_value >= 0.620:
        return 30, "D", 1
    else:
        return 20, "F", 0
    


ba_float = float(ba)
obp_float = float(obp)
ops_float = float(ops)

ba_points, ba_letter, ba_number = get_ba_points(ba_float)
obp_points, obp_letter, obp_number = get_obp_points(obp_float)
ops_points, ops_letter, ops_number = get_ops_points(ops_float)

player_grades.append(ba_number)
player_grades.append(obp_number) 
player_grades.append(ops_number)


# Bonus: +5 points for having 2+ elite stats (A tier or higher)
def bonus_points(player_grades):
    # 4 or above means A or better
    if ((player_grades[0] >= 4 and player_grades[1] >= 4) or
        (player_grades[0] >= 4 and player_grades[2] >= 4) or 
        (player_grades[1] >= 4 and player_grades[2] >= 4)):
        return 5
    else:
        return 0


# Each important stat has a different point value 
# Add them all up and grade them 
# 140 max points
# S+: 120+ points (elite)               6
# S: 110-119 points (great)             5
# A: 95-109 points (above average)      4
# B: 80-94 points (decent)              3
# C: 60-79 points (average)             2
# D: 45-59 points (below average)       1
# F: Below 45 points (poor)             0

def points_to_overall_grade(points):
    if points >= 120:
        return "S+"
    elif points >= 105:
        return "S"
    elif points >= 95:
        return "A"
    elif points >= 80:
        return "B"
    elif points >= 50:
        return "C"
    elif points >= 30:
        return "D"
    else:
        return "F"



def get_Hitting_Grade(player_grades, ba, ops, obp):
    total_points = (get_ba_points(ba)[0] + 
                   get_obp_points(obp)[0] + 
                   get_ops_points(ops)[0] + 
                   bonus_points(player_grades))
    # Used to see resulting grade point values
    # print(get_ba_points(ba)[0])
    # print(get_obp_points(ops)[0])
    # print(get_ops_points(obp)[0])
    # print(bonus_points(player_grades))
    print(total_points)
    return points_to_overall_grade(total_points)


final_Hitting_Grade = get_Hitting_Grade(player_grades, ba_float, ops_float, obp_float)

print(f"{user_player_name} is ranked a {final_Hitting_Grade}")








# Baserunning Grade - SB, CS, Speed, etc

