import streamlit as st
import statsapi

players_ID_And_Name_Cache = []

player_grades = []

player_name = st.text_input("What current player would you like to look up?", placeholder='Enter the name of any current MLB Player')

# used to debug any player 
# for player in statsapi.lookup_player("ohtani"):
#     st.write(player) 

# Checks if user inputed a name
if (player_name):
    player_results = statsapi.lookup_player(player_name)
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
        selected_player_name = st.selectbox("What player would you like from the list",placeholder="Select a player", index=None, options=list_player_names)

        # Loop though cache names and get the player ID
        for player_data in players_ID_And_Name_Cache:
            if (player_data[1] == selected_player_name):
                selected_player_id = player_data[0]
                st.write(f"Selected player ID: {selected_player_id}")
                break
        

    else:
        st.error("No player found, please try again.")




