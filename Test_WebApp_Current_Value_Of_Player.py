import streamlit as st
import statsapi

players_ID_And_Name_Cache = []

player_grades = []

st.set_page_config("MLB Hitting Stats Grader")

st.title("MLB Hitting Stats Grader")

col_input, col_key = st.columns([1, 2])

with col_input:
    player_name = st.text_input("What current player would you like to look up?", placeholder='Enter the name of any current MLB Player')

with col_key:
    st.markdown("🎯 **How Grading Works**")
    st.markdown("**Grades:** 🔥S+ (Elite) → ⭐S (Great) → 💪A (Above Avg) → 👍B (Decent) → 👌C (Average) → 📉D (Below) → 💔F (Poor)")
    st.markdown("**Elite Stats:** BA(.300+) • OBP(.375+) • OPS(.880+) • Max Points: 145")

# used to debug any player 
# for player in statsapi.lookup_player("ohtani"):
#     st.write(player) 

# Checks if user inputed a name
if (player_name):
    try:
        player_results = statsapi.lookup_player(player_name)
    except:
        st.error("Unable to connect to MLB API. Please try again later.")
        player_results = None
        
    # If there are results
    if (player_results):

        # Cache player names to be used in selectbox
        list_player_names = []

        # Gets the players with same or similar names as input
        for player in player_results:
            players_ID_And_Name_Cache.append([player['id'], player['fullName']])
            list_player_names.append(player['fullName'])
        
        # Used to help sort names by relevence 
        def score_name(name):
            if player_name.lower() in name.lower():
                return 1
            else:
                return 2

        list_player_names.sort(key=score_name)
        
        # User selects a player from list
        with col_input:
            selected_player_name = st.selectbox("What player would you like from the list",placeholder="Select a player", index=None, options=list_player_names)

        selected_player_id = None

        col1_picture, col2_picture = st.columns(2)

        # Loop though cache names and get the player ID
        for player_data in players_ID_And_Name_Cache:
            if (player_data[1] == selected_player_name):
                selected_player_id = player_data[0]
                st.markdown(f"## 📋 Results for **{selected_player_name}**")
                st.markdown(f"*Player ID: {selected_player_id}*")

                # Action Shot of Player:
                headshot_url = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{selected_player_id}/headshot/67/current"

                action_url = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:action:hero:current.jpg/q_auto:good,w_800/v1/people/{selected_player_id}/action/hero/current"

                with col1_picture:
                    st.image(headshot_url, width=150, caption=f"{selected_player_name}")

                with col2_picture:
                    st.image(action_url, width=670, caption=f"{selected_player_name} - Action Shot")
                
                break
        
        if (selected_player_id):
            
            try:
                # All Stats
                player_Stats = statsapi.player_stats(selected_player_id, season='current')

                # Just there hitting stats - It is a string
                player_Hitting_Stats = statsapi.player_stats(selected_player_id, group='hitting', season='current')

                split_String = player_Hitting_Stats.split(':')

                try:

                    ba = split_String[13].split('\n')[0]
                    ba = ba[1:]
                    obp = split_String[15].split('\n')[0]
                    obp = obp[1:]
                    ops = split_String[17].split('\n')[0]
                    ops = ops[1:]


                    # 1 function to tally up the points and give a letter grade based on points

                    # BA (Batting Average) (Ranking) - 30 points max
                    # Rating for how good a hitter is at making contact for a basehit
                    # S+: .300+ (30 points) (elite)
                    # S: .280+ (22 points) (great)
                    # A: .265+ (20 points) (above average)
                    # B: .255+ (18 points) (slightly above average)
                    # C: .246+ (15 points) (league average)
                    # D: .225+ (8 points) (below average)
                    # F: Below .225 (4 points) (poor)

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
                    # S: .360+ (22 points) (great) 
                    # A: .345+ (20 points) (above average)
                    # B: .330+ (18 points) (slightly above average) 
                    # C: .300+ (15 points) (league average)
                    # D: .270+ (8 points) (below average)
                    # F: Below .270 (4 points) (poor)

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
                    # S+: .880+ (80 points) (elite)
                    # S: .830+ (70 points) (great)
                    # A: .780+ (60 points) (above average)
                    # B: .740+ (50 points) (slightly above average)
                    # C: .760+ (40 points) (league average)
                    # D: .620+ (30 points) (below average)
                    # F: Below .620 (20 points) (poor)

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

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        ba_points, ba_letter, ba_number = get_ba_points(ba_float)
                        st.metric(label="ba: ", value=ba)
                        st.progress(ba_points/30)

                    with col2:
                        obp_points, obp_letter, obp_number = get_obp_points(obp_float)
                        st.metric(label="obp: ", value=obp)
                        st.progress(obp_points/30)

                    with col3:
                        ops_points, ops_letter, ops_number = get_ops_points(ops_float)
                        st.metric(label="ops: ", value=ops)
                        st.progress(ops_points/80)

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
                        
                    # Each stat has a different point value 
                    # Add them all up and grade them 
                    # 145 max points
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
                        # st.write(get_ba_points(ba)[0])
                        # st.write(get_obp_points(ops)[0])
                        # st.write(get_ops_points(obp)[0])
                        # st.write(bonus_points(player_grades))
                        st.write(total_points)
                        return points_to_overall_grade(total_points)


                    final_Hitting_Grade = get_Hitting_Grade(player_grades, ba_float, ops_float, obp_float)

                    st.write(f"{selected_player_name} is ranked: {final_Hitting_Grade}")
                    

                except:
                    st.error("Player has no hitting Stats this season") 
            except:
                st.error("Unable to fetch player stats. API may be down - try again later.")
    else:
        st.error("No player found, please try again.")




