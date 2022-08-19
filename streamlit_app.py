import pandas as pd
import snowflake.connector
import streamlit as st
import altair as alt
import os

# sn_user = os.environ['SN_USER']
# sn_password = os.environ['SNPASS']
# sn_account = os.environ['ACCOUNT']
# sn_warehouse = os.environ['WAREHOUSE']
# sn_database = os.environ['DATABASE']
# sn_schema = os.environ['SCHEMA']

sn_user = "shelwyn"
sn_password = "Stevo@#2012!"
sn_account = "lksupym-sm39588"
sn_warehouse = "COMPUTE_WH"
sn_database = "ENGLISH_PREMIER_LEAGUE"
sn_schema = "PLAYER_DATA"

conn = snowflake.connector.connect(user=sn_user,password=sn_password,account=sn_account,warehouse=sn_warehouse,database=sn_database,schema=sn_schema)
sql=""
#->
html_img="<img src='https://shelwyn.in/images/fpl_small.png'>"
st.sidebar.markdown(html_img, unsafe_allow_html=True)
player_type = st.sidebar.selectbox('',['Select Player Type','All Players','Goalkeeper','Defender','Midfielder','Forward'])
if player_type == 'Select Player Type':
    element_type=""
    PT=""
elif player_type == 'All Players':
    element_type=""
    PT=""
else:
    PT=player_type + " >"
    element_type = " and element_type = '" + str(player_type) + "' "
    
player_form = st.sidebar.selectbox('',['Current form greater than','1','2','3','4','5','6','7','8','9','10'])
if player_form == 'Current form greater than':
    form=""
    PF=""
else:
    PF=" Form greater than " +  str(player_form) + " >"
    form = " and form >=" + str(player_form) + " "
    
playing_at= st.sidebar.selectbox('',['Playing at','Any','Home','Away'])
if playing_at == 'Playing at':
    home_away=""
    PA=""
elif playing_at == 'Any':
    home_away=""
    PA=""
else:
    PA=" Playing @" + str(playing_at) + " >"
    home_away = " and playing_at='" + str(playing_at) + "' "

points_per_game= st.sidebar.selectbox('',['Points/game greater than','Any','3','4','5','6','7','8','9','10'])
if points_per_game == 'Points/game greater than':
    ppg =""
    PG=""
elif points_per_game == 'Any':
    ppg =""
    PG=""
else:
    PG=" Points/Game greater than " + str(points_per_game) + " >"
    ppg = " and points_per_game >=" + str(points_per_game) + " "

cost= st.sidebar.selectbox('',['Cost under','Any','3','4','5','6','7','8','9','10'])
if cost == 'Cost under':
    PR=""
    now_cost = ""
elif cost == 'Any':
    now_cost = ""
    PR=""
else:
    PR=" Price under " + str(cost) + " >"
    cost = int(cost) * 10
    now_cost = " and now_cost <=" + str(cost) + " "




html_header=str(PT) + str(PF) + str(PA) + str(PG) + str(PR)

if html_header=="":
    html_header="Top 10 selcted by the algorithm"
    sql="select * From PLAYER_STATS where chance_of_playing_next_round>=0 and team_strength >= opponent_strength order by form desc, points_per_game desc,creativity desc,now_cost desc  LIMIT 10"
else:
    strength_wise= st.selectbox('',['Show all','Show players playing against weaker teams'])
    html_hr="<hr>"
    st.markdown(html_hr, unsafe_allow_html=True)
    if strength_wise=="Show players playing against weaker teams":
        add_logic=" and team_strength >= opponent_strength "
    else:
        add_logic=""
    sql="select * From PLAYER_STATS where chance_of_playing_next_round>=0 " + str(form) + str(element_type) + str(home_away) + str(ppg) + str(now_cost) + str(add_logic)  + "  order by form desc, points_per_game desc,creativity desc,now_cost desc  LIMIT 10"
    


cur_players = conn.cursor()
cur_players.execute(sql)
rows_players = cur_players.fetchall()





st.markdown(html_header, unsafe_allow_html=True)
html_code = """
        <table border=1 width="100%" class="eli5-weights eli5-feature-importances" style="border-collapse: collapse; border: solid; margin-top: 0em; table-layout: auto;">
        <thead>
        <tr style="border: none;">
            <th style="padding: 0 1em 0 0.5em; text-align: right; border: dotted;"><font size="2">Player</font></th>
            <th style="padding: 0 1em 0 0.5em; text-align: right; border: dotted;"><font size="2">Position</font></th>
            <th style="padding: 0 1em 0 0.5em; text-align: right; border: dotted;"><font size="2">Points per game</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Team</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Price</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Form</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Playing @</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Playing against</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;">-</th>
        </tr>
        </thead>
        <tbody>"""
for player in rows_players:
    now_cost_table= player[18] /10
    player_image = player[19].replace("jpg","png") 
    html_code= html_code + """<tr style="background-color: hsl(120, 100.00%, 80.00%); border: solid;">
                <td style="padding: 0 1em 0 0.5em; text-align: right; border: solid;">
                    <font size="2">""" + player[5] + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + player[3] + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + str(player[21]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + player[6] + """</font>
                </td>
                <td style="padding: 0 1em 0 0.5em; text-align: right; border: solid;">
                      <font size="2">""" + str(now_cost_table) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                       <font size="2">""" + str(player[20]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                    <font size="2">""" + str(player[26]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + str(player[29]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                    <img src="https://resources.premierleague.com/premierleague/photos/players/110x140/p""" + str(player_image) + """" width="50">
                </td>
            </tr>

        </tbody>
        """

st.markdown(html_code, unsafe_allow_html=True)
if html_header=="Top 10 selcted by the algorithm":
    sql_pd="select full_name From PLAYER_STATS where chance_of_playing_next_round>=0 and team_strength >= opponent_strength order by form desc, points_per_game desc,creativity desc,now_cost desc  LIMIT 10"
else:
    sql_pd="select full_name From PLAYER_STATS  where chance_of_playing_next_round>=0 " + str(form) + str(element_type) + str(home_away) + str(ppg) + str(now_cost) + str(add_logic)  + " order by form desc, points_per_game desc,creativity desc,now_cost desc LIMIT 10"


players_selected = pd.read_sql(sql_pd,conn)

html_hr="<hr>"
st.markdown(html_hr, unsafe_allow_html=True)
players_dd= st.selectbox('Select Player',players_selected)

cur_get_last_gameweek = conn.cursor()
cur_get_last_gameweek.execute("select max(event) from player_detailed_stats")
rows_last_gameweek = cur_get_last_gameweek.fetchall()
for last_gameweek in rows_last_gameweek:
    max_event=last_gameweek[0]

gameweek=[]
goalsscored=[]
assist=[]
bonus=[]
saves=[]
yellow_cards=[]
red_cards=[]

cur_get_stats_to_arrange = conn.cursor()
cur_get_stats_to_arrange.execute("select event,identifier,value From player_detailed_stats where identifier in ('goals_scored','assists','bonus','saves','yellow_cards','red_cards') and player='" + str(players_dd) + "' group by event, identifier, value")
rows_stats_to_arrange = cur_get_stats_to_arrange.fetchall()
for GW in range(1, max_event + 1):
    assist_present = 0
    goalsscored_present = 0
    bonus_present = 0
    saves_present = 0
    yellow_cards_present = 0
    red_cards_present = 0
    assist_value = 0
    goalsscored_value = 0
    bonus_value = 0
    saves_value = 0
    yellow_cards_value = 0
    red_cards_value = 0
    gameweek.append(GW)
    for stats_to_arrange in rows_stats_to_arrange:
        event = stats_to_arrange[0]
        if event==GW:
            print("Gameweek",GW)
            identifier = stats_to_arrange[1]
            value = stats_to_arrange[2]
            if identifier=="assists":
                assist_present=1
                assist_value=value
            if identifier=="bonus":
                bonus_present=1
                bonus_value=value
            if identifier=="goals_scored":
                goalsscored_present=1
                goalsscored_value=value
            if identifier=="saves":
                saves_present=1
                saves_value=value
            if identifier=="yellow_cards":
                yellow_cards_present=1
                yellow_cards_value=value
            if identifier=="red_cards":
                red_cards_present=1
                red_cards_value=value

    goalsscored.append(goalsscored_value)
    assist.append(assist_value)
    bonus.append(bonus_value)
    saves.append(saves_value)
    yellow_cards.append(yellow_cards_value)
    red_cards.append(red_cards_value)

dataFrame_stats = pd.DataFrame()
dataFrame_stats['gameweek']=gameweek
dataFrame_stats['goalsscored']=goalsscored
dataFrame_stats['assist']=assist
dataFrame_stats['bonus']=bonus
dataFrame_stats['saves']=saves
dataFrame_stats['yellow_cards']=yellow_cards
dataFrame_stats['red_cards']=red_cards

source = dataFrame_stats

col_goal, col_assist= st.columns(2)
with col_goal:
    goals_chart = alt.Chart(source).mark_bar().encode(
    x='gameweek',
    y='goalsscored',
    tooltip=['gameweek', 'goalsscored'])
    st.altair_chart(goals_chart, use_container_width=True)    
with col_assist:
    assist_chart = alt.Chart(source).mark_bar().encode(
    x='gameweek',
    y='assist',
    tooltip=['gameweek', 'assist'])
    st.altair_chart(assist_chart, use_container_width=True)  

col_bonus, col_saves= st.columns(2)
with col_bonus:
    bonus_chart = alt.Chart(source).mark_bar().encode(
    x='gameweek',
    y='bonus',
    tooltip=['gameweek', 'bonus'])
    st.altair_chart(bonus_chart, use_container_width=True)    
with col_saves:
    saves_chart = alt.Chart(source).mark_bar().encode(
    x='gameweek',
    y='saves',
    tooltip=['gameweek', 'saves'])
    st.altair_chart(saves_chart, use_container_width=True)  

col_yellow, col_red= st.columns(2)
with col_yellow:
    yellow_chart = alt.Chart(source).mark_bar().encode(
    x='gameweek',
    y='yellow_cards',
    tooltip=['gameweek', 'yellow_cards'])
    st.altair_chart(yellow_chart, use_container_width=True)    
with col_red:
    red_chart = alt.Chart(source).mark_bar().encode(
    x='gameweek',
    y='red_cards',
    tooltip=['gameweek', 'red_cards'])
    st.altair_chart(red_chart, use_container_width=True)  

sq_rest_details="select * From PLAYER_STATS where full_name='" + str(players_dd) + "'"
cur_players_rest_details = conn.cursor()
cur_players_rest_details.execute(sq_rest_details)
rows_players_rest_details = cur_players_rest_details.fetchall()

html_code_rest_details = """
        <table border=1 width="100%" class="eli5-weights eli5-feature-importances" style="border-collapse: collapse; border: solid; margin-top: 0em; table-layout: auto;">
        <thead>
        <tr style="border: none;">
            <th style="padding: 0 1em 0 0.5em; text-align: right; border: dotted;"><font size="2">Minutes Played</font></th>
            <th style="padding: 0 1em 0 0.5em; text-align: right; border: dotted;"><font size="2">Total Points</font></th>
            <th style="padding: 0 1em 0 0.5em; text-align: right; border: dotted;"><font size="2">Total Goals/Assists</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Influence</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Creativity</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Threat</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Clean Sheets</font></th>
            <th style="padding: 0 0.5em 0 0.5em; text-align: left; border: dotted;"><font size="2">Goals Conceded</font></th>
        </tr>
        </thead>
        <tbody>"""
for player_rest_details in rows_players_rest_details:
    html_code_rest_details= html_code_rest_details + """<tr style="background-color: hsl(120, 100.00%, 80.00%); border: solid;">
                <td style="padding: 0 1em 0 0.5em; text-align: right; border: solid;">
                    <font size="2">""" + str(player_rest_details[8]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + str(player_rest_details[7]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + str(player_rest_details[9]) + "/" + str(player_rest_details[10]) +  """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + str(player_rest_details[23]) + """</font>
                </td>
                <td style="padding: 0 1em 0 0.5em; text-align: right; border: solid;">
                      <font size="2">""" + str(player_rest_details[24]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                       <font size="2">""" + str(player_rest_details[25])+ """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                    <font size="2">""" + str(player_rest_details[11]) + """</font>
                </td>
                <td style="padding: 0 0.5em 0 0.5em; text-align: left; border: solid;">
                     <font size="2">""" + str(player_rest_details[12]) + """</font>
                </td>
            </tr>

        </tbody>
        """

st.markdown(html_code_rest_details, unsafe_allow_html=True)
