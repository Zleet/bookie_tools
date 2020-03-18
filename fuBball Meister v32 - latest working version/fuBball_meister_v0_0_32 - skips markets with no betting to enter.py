# ===============================================================================================
# FuBball Meister
#
# Takes the pain out of football betting editing.
# ===============================================================================================
# imports
import pyautogui, time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# ===============================================================================================
# global variables
current_line_no = 0 # keep a record of the current line index (from zero upwards)

# coordinate information for:
# (1) the save button
# (2) the next market button
# (3) the handicap cell
# (4) the top left cell
# (5) windows onscreen accessibility keyboard q button
# (6) test line text
# (7) total test lines
# (8) the match betting market for match #1
# (8) the match betting market for match #2
# (8) the match betting market for match #3
save_x = -1
save_y = -1
next_market_x = -1
next_market_y = -1
handicap_cell_x = -1
handicap_cell_y = -1
top_left_cell_x = -1
top_left_cell_y = -1
keyboard_q_x = -1
keyboard_q_y = -1
test_cell_x = -1
test_cell_y = -1
top_price_cell_x = -1
top_price_cell_y = -1
test_line_text = -1
total_test_lines = -1
match1_match_betting_x = -1
match1_match_betting_y = -1
match2_match_betting_x = -1
match2_match_betting_y = -1
match3_match_betting_x = -1
match3_match_betting_y = -1

# delay between typing letters on the window onscreen accessibility keyboard
# was 0.2; changed
letter_typing_delay = 0

# Football betting, extracted from the football betting webpage
football_betting = []

# Index of the current match (displayed in the text widget)
current_match_index = 0

# all of the Text widgets in the set coordinates window should be global to access them from
# different functions
save_button_x_text = -1
save_button_y_text = -1
next_market_button_x_text = -1
next_market_button_y_text = -1
handicap_cell_x_text = -1
handicap_cell_y_text = -1
top_left_cell_x_text = -1
top_left_cell_y_text = -1
keyboard_q_x_text = -1
keyboard_q_y_text = -1
test_cell_x_text = -1
text_cell_y_text = -1
letter_typing_delay_entry = -1
test_line_text_text = -1
total_test_lines_text = -1
top_price_cell_x_text = -1
top_price_cell_y_text = -1
match1_match_betting_x_text = -1
match1_match_betting_y_text = -1
match2_match_betting_x_text = -1
match2_match_betting_y_text = -1
match3_match_betting_x_text = -1
match3_match_betting_y_text = -1

# The clickable settings window
clickable_settings_window = -1

# global dictionary to hold the pixel coordinates for the letter keys
# It's structured like this:
# keys = {
#       "a" : {"x" : 345, "y" : 75},
#       "b" : {"x" : 127, "y" : 439},
#       etc...
#       }
keys = {
        "A" : {"x" : -1, "y" : -1},
        "B" : {"x" : -1, "y" : -1},
        "C" : {"x" : -1, "y" : -1},
        "D" : {"x" : -1, "y" : -1},
        "E" : {"x" : -1, "y" : -1},
        "F" : {"x" : -1, "y" : -1},
        "G" : {"x" : -1, "y" : -1},
        "H" : {"x" : -1, "y" : -1},
        "I" : {"x" : -1, "y" : -1},
        "J" : {"x" : -1, "y" : -1},
        "K" : {"x" : -1, "y" : -1},
        "L" : {"x" : -1, "y" : -1},
        "M" : {"x" : -1, "y" : -1},
        "N" : {"x" : -1, "y" : -1},
        "O" : {"x" : -1, "y" : -1},
        "P" : {"x" : -1, "y" : -1},
        "Q" : {"x" : -1, "y" : -1},
        "R" : {"x" : -1, "y" : -1},
        "S" : {"x" : -1, "y" : -1},
        "T" : {"x" : -1, "y" : -1},
        "U" : {"x" : -1, "y" : -1},
        "V" : {"x" : -1, "y" : -1},
        "W" : {"x" : -1, "y" : -1},
        "X" : {"x" : -1, "y" : -1},
        "Y" : {"x" : -1, "y" : -1},
        "Z" : {"x" : -1, "y" : -1},
        "," : {"x" : -1, "y" : -1},
        "backspace" : {"x" : -1, "y" : -1},
        "delete"    : {"x" : -1, "y" : -1},
        "tab"       : {"x" : -1, "y" : -1},
        "shift"     : {"x" : -1, "y" : -1},
        "control"   : {"x" : -1, "y" : -1},
        " "         : {"x" : -1, "y" : -1},
        "enter"     : {"x" : -1, "y" : -1},
        "home"      : {"x" : -1, "y" : -1},
        "end"       : {"x" : -1, "y" : -1},
        "up"        : {"x" : -1, "y" : -1},
        "down"      : {"x" : -1, "y" : -1},
        "left"      : {"x" : -1, "y" : -1},
        "right"     : {"x" : -1, "y" : -1}
        }
# ====================================================================================================
# Map the letters a to z to the pixel coordinates of their keys on the
# onscreen keyboard. The global dictionary that holds the pixel coordinates
# for the letter keys is structured like this:
# keys = {
#       "a" : {"x" : 345, "y" : 75},
#       "b" : {"x" : 127, "y" : 439},
#       etc...
#       }
#
# Updated 22/8/17 for new onscreen keyboard (post data migration; McLeans servers now based in Madrid)
# ====================================================================================================
def map_keys():

    global keys
    global keyboard_q_x
    global keyboard_q_y

    # horizontal distance between letters on the onscreen keyboard (in pixels)
    # and vertical distance between letter rows
    horizontal_key_distance = 41    # updated for Madrid servers 22/9/17
    vertical_key_distance = 39      # updated for Madrid servers 22/9/17

    # map the number row plus the three rows of letters
    letter_rows = ['Z1234567890-=', 'qwertyuiop[]', "asdfghjkl;'#", 'zxcvbnm,./'] # ignore initial Z kludge (22/8/17)
    for count in range(len(letter_rows)):
        current_letter_row = letter_rows[count]
        row_start_x = keyboard_q_x - (horizontal_key_distance / 2) + (0.5 * horizontal_key_distance * count) # changed
        row_y = keyboard_q_y - vertical_key_distance + (count * vertical_key_distance)
        for inner_count in range(len(current_letter_row)):
            current_letter = current_letter_row[inner_count]
            keys[current_letter.upper()] = {"x": -1, "y" : -1}
            keys[current_letter.upper()]["x"] = int(row_start_x + (inner_count * horizontal_key_distance))
            keys[current_letter.upper()]["y"] = row_y

    # map the backspace (delete) key to the right of the equals sign at the top of
    # the onscreen keyboard
    x = keys["="]["x"] + horizontal_key_distance
    y = keys["="]["y"]
    keys["backspace"] = {"x" : x, "y" : y}

    # map the tab key on the left of the screen
    x = keys["Q"]["x"] - horizontal_key_distance
    y = keys["Q"]["y"]
    keys["tab"] = {"x" : x, "y" : y}

    # map the shift key on the left of the screen
    x = keys["Z"]["x"] - (horizontal_key_distance * 2)
    y = keys["Z"]["y"]
    keys["shift"] = {"x" : x, "y" : y}

    # map the control key on the bottom left of the onscreen keyboard
    x = keys["Z"]["x"] - (3 * horizontal_key_distance)
    y = keys["Z"]["y"] + vertical_key_distance
    keys["control"] = {"x" : x, "y" : y}

    # map the space key
    x = keys["B"]["x"]
    y = keys["B"]["y"] + vertical_key_distance
    keys[" "] = {"x" : x, "y" : y}
    keys["space"] = {"x" : x, "y" : y}

    # map the enter key
    x = keys["P"]["x"] + (4 * horizontal_key_distance)
    y = keys["P"]["y"]
    keys["enter"] = {"x" : x, "y" : y}

    # map the hm (home) key
    x = keys["]"]["x"] + (4 * horizontal_key_distance)
    y = keys["="]["y"] - vertical_key_distance
    keys["hm"] = {"x" : x, "y" : y}
    keys["home"] = {"x" : x, "y" : y}

    # map the delete key
    x = keys["="]["x"] + horizontal_key_distance
    y = keys["="]["y"]
    keys["delete"] = {"x" : x, "y": y}

    # map the end key
    x = keys["home"]["x"]
    y = keys["P"]["y"]
    keys["end"] = {"x" : x, "y" : y}

    # map up, down, left and right keys
    # up
    x = keys["]"]["x"] + (horizontal_key_distance * 1.5)
    y = keys["N"]["y"]
    keys["up"] = {"x" : x, "y" : y}
    # left
    x = keys["up"]["x"] - horizontal_key_distance
    y = keys["space"]["y"]
    keys["left"] = {"x" : x, "y" : y}
    # down
    x = keys["up"]["x"]
    y = keys["space"]["y"]
    keys["down"] = {"x" : x, "y" : y}
    # right
    x = keys["down"]["x"] + horizontal_key_distance
    y = keys["space"]["y"]
    keys["right"] = {"x" : x, "y" : y}

    return
# ====================================================================================================
# Read all the coordinate information:
# save_x, save_y (x and y coordinates of the SAVE button at the top of the screen)
# plus_x, plus_y (x and y coordinates of the plus button at the top left of the
#                 input cells at the bottom of the screen)
# input_x, input_y (x and y coordinates of the text line where you search for
#                   a participant in the McLeans system)
# ====================================================================================================
def read_coordinate_information():

    global save_x
    global save_y
    global plus_x
    global plus_y
    global input_x
    global input_y
    global keyboard_q_x
    global keyboard_q_y
    global letter_delay

    save_x = save_x_text_box.get("1.0", END)
    save_x = int(save_x.strip())
    # print('save_x =', save_x)
    save_y = save_y_text_box.get("1.0", END)
    save_y = int(save_y.strip())
    # print('save_y =', save_y)

    plus_x = plus_x_text_box.get("1.0", END)
    plus_x = int(plus_x.strip())
    # print('plus_x =', plus_x)

    plus_y = plus_y_text_box.get("1.0", END)
    plus_y = int(plus_y.strip())
    # print('plus_y =', plus_y)

    input_x = input_x_text_box.get("1.0", END)
    input_x = int(input_x.strip())
    # print('input_x =', input_x)

    input_y = input_y_text_box.get("1.0", END)
    input_y = int(input_y.strip())
    # print('input_y =', input_y)

    keyboard_q_x = keyboard_q_key_x_text_box.get("1.0", END)
    keyboard_q_x = int(keyboard_q_x.strip())
    # print('keyboard_q_x =', keyboard_q_x)

    keyboard_q_y = keyboard_q_key_y_text_box.get("1.0", END)
    keyboard_q_y = int(keyboard_q_y.strip())
    # print('keyboard_q_y =', keyboard_q_y)

    letter_delay = letter_delay_text_box.get("1.0", END)
    letter_delay = float(letter_delay.strip())
    # print('letter_delay =', letter_delay)

    return
# ====================================================================================================
# Type text by using pyautogui to click on the windows accessibility onscreen
# keyboard. In between each character, pause pause_between_letters seconds
def kb_type(text):

    for character in text:
        if character.upper() in keys.keys():
            x = keys[character.upper()]["x"]
            y = keys[character.upper()]["y"]
            # if uppercase character, press shift first
            if (character.upper() == character) and character.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                kb_press("shift")
            pyautogui.click(x, y)
            time.sleep(letter_typing_delay) # changed

    return
# ====================================================================================================
# Press one or more special keys on the keyboard e.g. enter, up, down, shift etc.
# Accepts either a list of key strings or a single key string as parameters
# e.g. "up" or ["down", "right", "shift"]
def kb_press(key_param, pause_between_keys = 0.1):

    # if key_param is a string, get the x and y coordinate for the key and
    # pyautogui.click() it
    if isinstance(key_param, str):
        x = keys[key_param]["x"]
        y = keys[key_param]["y"]
        pyautogui.click(x, y)
        time.sleep(pause_between_keys)

    # if key_param is a list, loop through each key in the list, look up its
    # x and y coordinates and pyautogui.click() it, pausing pause_between_keys
    # seconds between keys
    if isinstance(key_param, list):
        for key in key_param:
            x = keys[key]["x"]
            y = keys[key]["y"]
            pyautogui.click(x, y)
            time.sleep(pause_between_keys)

    return
# ====================================================================================================
# Extract the football betting from the football betting webpage, stick it in the global variable list
# football_betting
# Each football match will be represented by a dictionary in the form:
#
# {
#   "home_team"                 : "Crusaders",
#   "away_team"                 : "Coleraine",
#   "kick_off"                  : "0.625",
#   "match_betting_home"        : "1/2"
#   "match_betting_draw"        : "14/5",
#   "match_betting_away"        : "5/1",
#   "handicap_betting_home"     : "6/5",
#   "handicap_betting_draw"     : "11/4",
#   "handicap_betting_away"     : "13/8",
#   "handicap_home"             : "-1",
#   "handicap_away"             : "+1",
#   "total_goals_under_2p5"     : "4/5",
#   "total_goals_over_2p5"      : "10/11",
#   "new_goal_rush_yes"         : "19/20",
#   "new_goal_rush_no"          : "3/4",
#   "goal_rush_plus_home"       : "13/5",
#   "goal_rush_plus_draw"       : "4/1",
#   "goal_rush_plus_away"       : "19/2",
#   "win_to_nil_home"           : "13/8",
#   "win_to_nil_away"           : "13/2",
#   "over_two_goals_plus_home"  : "9/5",
#   "over_two_goals_plus_draw"  : "12/1",
#   "over_two_goals_plus_away"  : "8/1",
#   "win_to_nil_yes"            : "15/8",
#   "win_to_nil_no"             : "1/100",   # This is always "1/100"
#   "total_goals_under_1p5"     : "4/5",
#   "total_goals_over_1p5"      : "10/11",
#   "total_goals_under_3p5"     : "6/5",
#   "total_goals_over_3p5"      : "11/10",
#   "total_goals_under_4p5"     : "8/11",
#   "total_goals_over_4p5"      : "3/10"
# }
#
# ====================================================================================================
def read_football_webpage():

    global football_betting
    global current_match_index
    football_betting = []
    current_match_index = 0

    # read the betting from "football_betting_webpage.htm"
    infile = open('football_betting_webpage.htm', 'r', encoding='latin-1')
    html = infile.read()
    infile.close()

    # Split html into code_blocks; each football match code block begins with '<table style="width:100%">'
    code_blocks = html.split('<table style="width:100%">')
    # First code block doesn't contain any betting information; discard it
    code_blocks = code_blocks[1:]

    # Loop through code blocks; for each code block, extract the betting data
    for code_block in code_blocks:
        match_betting_data = extract_match_betting_data_from_code_block(code_block)
        football_betting.append(match_betting_data)

    # generate confirmation popup window here
    total_code_blocks = len(code_blocks)
    the_text = str(total_code_blocks) + " matches extracted from file"
    popup_window = Toplevel()
    popup_window.title(":D")
    message_widget = Message(popup_window, text=the_text)
    message_widget.pack()
    button = Button(popup_window, text="OK", command=popup_window.destroy)
    button.pack()

    # display the first football match in the match_display_text_box Text widget
    display_football_match_in_text_widget(current_match_index)

    return
# ====================================================================================================
# Display a football match in the match_display_text_box Text widget
# ====================================================================================================
def display_football_match_in_text_widget(match_index):

    global football_betting
    match_dictionary = football_betting[match_index]
    total_matches = len(football_betting)

    # test print
    keys = match_dictionary.keys()
    # for key in keys:
    #     print(key, "\t: ", match_dictionary[key])

    # first line contains kick off time and x/y for what number current match is
    text = "Kick Off: " + match_dictionary["kick_off"] + "                    (" + str(match_index + 1) + '/'
    text += str(total_matches) + ')'
    
    # second line contains match and betting
    text += "\n" + match_dictionary["match_betting_home"] + " " + match_dictionary["home_team"] + " "
    text += match_dictionary["match_betting_draw"] + " " + match_dictionary["away_team"] + " "
    text += match_dictionary["match_betting_away"]
    
    # third line contains handicap betting
    text += "\n" + match_dictionary["handicap_betting_home"] + " " + match_dictionary["handicap_home"]
    # work out how many spaces we need to add to get the draw price and draw handicap price line up
    # (1) calculate length of home price + home team + draw price + 2
    # (2) calculate length of home handicap price + home handicap + handicap draw price + 1
    # (3) total spaces to add = (1) - (2)
    target_length = len(match_dictionary["match_betting_home"])
    target_length += len(match_dictionary["home_team"]) + len(match_dictionary["match_betting_draw"]) + 2
    second_line_occupied = len(match_dictionary["handicap_betting_home"])
    second_line_occupied += len(match_dictionary["handicap_home"]) + len(match_dictionary["handicap_betting_draw"])
    second_line_occupied += 1
    spaces_to_add = target_length - second_line_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["handicap_betting_draw"]
    # work out how many spaces to add before the away handicap and away handicap price
    away_team_and_price_length = len(match_dictionary["away_team"])
    away_team_and_price_length += len(match_dictionary["match_betting_away"]) + 2
    away_hcap_and_price_length = len(match_dictionary["handicap_away"])
    away_hcap_and_price_length += len(match_dictionary["handicap_betting_away"]) + 2
    spaces_to_add = away_team_and_price_length - away_hcap_and_price_length + 1
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["handicap_away"] + " " + match_dictionary["handicap_betting_away"]

    # work out the width of the left column
    left_col_width = max(
        len("2.5 Goals"),
        len("Under 2.5 " + match_dictionary["total_goals_under_2p5"]),
        len("Over 2.5 " + match_dictionary["total_goals_over_2p5"]),
        len("New Goal Rush"),
        len("Both teams to score " + match_dictionary["new_goal_rush_yes"]),
        len("Either team not to score " + match_dictionary["new_goal_rush_no"]),
        len("Goal Rush Plus"),
        len(match_dictionary["home_team"] + " " + match_dictionary["goal_rush_plus_home"]),
        len("Draw " + match_dictionary["goal_rush_plus_draw"]),
        len(match_dictionary["away_team"] + " " + match_dictionary["goal_rush_plus_away"]),
        len("Win To Nil"),
        len(match_dictionary["home_team"] + " " + match_dictionary["win_to_nil_home"]),
        len(match_dictionary["away_team"] + " " + match_dictionary["win_to_nil_away"]),
        len("Over Two Goals Plus"),
        len(match_dictionary["home_team"] + " " + match_dictionary["over_two_goals_plus_home"]),
        len("Draw " + match_dictionary["over_two_goals_plus_draw"]),
        len(match_dictionary["away_team"] + " " + match_dictionary["over_two_goals_plus_away"])
                        )

    # work out the width of the right column
    right_col_width = max(
        len("WTN-ET"),
        len("Yes " + match_dictionary["win_to_nil_yes"]),
        len("1.5 Goals"),
        len("Under 1.5 " + match_dictionary["total_goals_under_1p5"]),
        len("Over 1.5 " + match_dictionary["total_goals_over_1p5"]),
        len("3.5 Goals"),
        len("Under 3.5 " + match_dictionary["total_goals_under_3p5"]),
        len("Over 3.5 " + match_dictionary["total_goals_over_3p5"]),
        len("4.5 Goals"),
        len("Under 4.5 " + match_dictionary["total_goals_under_4p5"]),
        len("Over 4.5 " + match_dictionary["total_goals_over_4p5"])
                        )

    # print('left_col_width =', left_col_width)
    # print('right_col_width =', right_col_width)

    # work out total line width
    total_line_width = left_col_width + right_col_width + 1

    # fourth line contains "2.5 Goals" and "WTN-ET"
    text += "\n2.5 Goals"
    spaces_to_add = left_col_width - 9
    for count in range(spaces_to_add):
        text += " "
    text += " WTN-ET"

    # Line #5 contains under 2.5 goals and WTN-ET yes
    text += "\nUnder 2.5"
    spaces_to_add = left_col_width - len("Under 2.5" + match_dictionary["total_goals_under_2p5"])
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_under_2p5"]
    text += " Yes "    
    right_col_occupied = len("Yes ")
    right_col_occupied += len(match_dictionary["win_to_nil_yes"])
    spaces_to_add = right_col_width - right_col_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["win_to_nil_yes"]

    # Line #6 contains over 2.5 goals and that's it
    text += "\nOver 2.5"
    spaces_to_add = left_col_width - len("Over 2.5" + match_dictionary["total_goals_over_2p5"])
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_over_2p5"]

    # Line #7 contains "New Goal Rush" and "1.5 Goals"
    text += "\nNew Goal Rush"
    spaces_to_add = left_col_width - 12
    for count in range(spaces_to_add):
        text += " "
    text += "1.5 Goals"    

    # Line #8 contains New Goal Rush Yes and Under 1.5 Goals
    text += "\nBoth teams to score"
    spaces_to_add = left_col_width - (18 + len(match_dictionary["new_goal_rush_yes"])) - 1
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["new_goal_rush_yes"] + " Under 1.5"


    right_col_occupied = len("Under 1.5")
    right_col_occupied += len(match_dictionary["total_goals_under_1p5"])
    spaces_to_add = right_col_width - right_col_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_under_1p5"]

    # Line #9 contains New Goal Rush No and over 1.5 goals
    text += "\nEither Team Not To Score"
    spaces_to_add = left_col_width - (24 + len(match_dictionary["new_goal_rush_no"]))
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["new_goal_rush_no"] + " Over 1.5"
    spaces_to_add = right_col_width - ( len("Over 1.5") + len(match_dictionary["total_goals_over_1p5"]) )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_over_1p5"]

    # Line #10 contains Goal Rush Plus header plus 3.5 Goals header
    text += "\nGoal Rush Plus"
    spaces_to_add = left_col_width - 13
    for count in range(spaces_to_add):
        text += " "
    text += "3.5 Goals"

    # Line #11 contains goal rush plus home and under 3.5 goals # THIS IS MISSING THE PRICE; FIX THIS
    text += "\n" + match_dictionary["home_team"]
    left_col_occupied = len( match_dictionary["home_team"] + match_dictionary["goal_rush_plus_home"] )
    spaces_to_add = left_col_width - left_col_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["goal_rush_plus_home"] ###
    text += " Under 3.5"
    spaces_to_add = right_col_width - ( len('Under 3.5') + len(match_dictionary["total_goals_under_3p5"]) )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_under_3p5"]

    # Line #12 contains goal rush plus draw and over 3.5 goals
    text += "\nDraw"
    left_col_occupied = 4 + len(match_dictionary["goal_rush_plus_draw"])
    spaces_to_add = left_col_width - left_col_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["goal_rush_plus_draw"] + " Over 3.5"
    right_col_occupied = len( "Over 3.5" + match_dictionary["total_goals_over_3p5"] )
    spaces_to_add = right_col_width - right_col_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_over_3p5"]

    # Line #13 contains goal rush plus away
    text += "\n" + match_dictionary["away_team"]
    left_col_occupied = len(match_dictionary["away_team"])
    left_col_occupied += len(match_dictionary["goal_rush_plus_away"])
    spaces_to_add = left_col_width - left_col_occupied
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["goal_rush_plus_away"]

    # Line #14 contains "Win To Nil" and "4.5 Goals" headers
    text += "\nWin To Nil"
    spaces_to_add = left_col_width - len("Win To Nil")
    for count in range(spaces_to_add):
        text += " "
    text += " 4.5 Goals"

    # Line #15 contains win to nil home price and under 4.5 goals price
    text += "\n" + match_dictionary["home_team"]
    spaces_to_add = left_col_width - len( match_dictionary["home_team"] + match_dictionary["win_to_nil_home"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["win_to_nil_home"] + " Under 4.5"
    spaces_to_add = right_col_width - len( "Under 4.5" + match_dictionary["total_goals_under_4p5"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_under_4p5"]

    # Line #16 contains win to nil away price plus over 4.5 goals
    text += "\n" + match_dictionary["away_team"]
    spaces_to_add = left_col_width - len( match_dictionary["away_team"] + match_dictionary["win_to_nil_away"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["win_to_nil_away"] + " Over 4.5"
    spaces_to_add = right_col_width - len( "Over 4.5" + match_dictionary["total_goals_over_4p5"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["total_goals_over_4p5"]

    # Line #17 contains "Over Two Goals Plus Header"
    text += "\nOver Two Goals Plus"

    # Line #18 contains over two goals plus home price
    text += "\n" + match_dictionary["home_team"]
    spaces_to_add = left_col_width - len( match_dictionary["home_team"] + match_dictionary["over_two_goals_plus_home"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["over_two_goals_plus_home"]

    # Line #19 contains over two goals plus draw price
    text += "\nDraw"
    spaces_to_add = left_col_width - len( "Draw" + match_dictionary["over_two_goals_plus_draw"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["over_two_goals_plus_draw"]

    # Line #20 contains over two goals plus away price
    text += "\n" + match_dictionary["away_team"]
    spaces_to_add = left_col_width - len( match_dictionary["away_team"] + match_dictionary["over_two_goals_plus_away"] )
    for count in range(spaces_to_add):
        text += " "
    text += match_dictionary["over_two_goals_plus_away"]

    # stick the text in the text widget
    match_display_text_box.delete("1.0", END)
    match_display_text_box.insert(END, text)

    # Do all the colour and fontstyling here +++++++++++++++++++++++++++++++++++++++++++++++++++

    # Set top line font and regular font
    # top_line_font = ("Courier", 10, "bold")
    # regular_font = ("Courier", 10, "bold")
    top_line_font = ("Courier", 8)
    regular_font = ("Courier", 8)


    # ***** TONNES OF OLD FORMATTING CODE (NOW SCRAPPED) USED TO BE HERE *****

    # format line 1 (kick off time and x/y match line) in Aquamarine regular font
    match_display_text_box.tag_add("line_1", "1.0", "1.end")
    match_display_text_box.tag_config("line_1", foreground="Aquamarine", font=regular_font)
    
    # format line 2 (match betting line) as top line font in Chartreuse
    match_display_text_box.tag_add("line_2", "2.0", "2.end")
    match_display_text_box.tag_config("line_2", foreground="Chartreuse", font=top_line_font)

    # format line 3 (handicap line) as top line font in Fuchsia
    match_display_text_box.tag_add("line_3", "3.0", "3.end")
    match_display_text_box.tag_config("line_3", foreground="Fuchsia", font=top_line_font)

    # format lines 4 to 20 with a basic font that can be overwritten
    match_display_text_box.tag_add("lines_4_to_20", "4.0", "20.end")
    match_display_text_box.tag_config("lines_4_to_20", foreground="Yellow", font=regular_font)

    # format line 4 (2.5 Goals and WTN-ET headers) as regular font in Red
    match_display_text_box.tag_add("line_4", "4.0", "4.end")
    match_display_text_box.tag_config("line_4", foreground="Red", font=regular_font)

    # format line 7 (New Goal Rush and 1.5 Goals headers) as regular font in Red
    match_display_text_box.tag_add("line_7", "7.0", "7.end")
    match_display_text_box.tag_config("line_7", foreground="Red", font=regular_font)

    # format line 10 (Goal Rush Plus header and 3.5 Goals header) as regular font in red
    match_display_text_box.tag_add("line_10", "10.0", "10.end")
    match_display_text_box.tag_config("line_10", foreground="Red", font=regular_font)

    # format line 14 (Win To Nil header and 4.5 Goals header) as regular font in red
    match_display_text_box.tag_add("line_14", "14.0", "14.end")
    match_display_text_box.tag_config("line_14", foreground="Red", font=regular_font)

    # format line 17 (Over Two Goals Plus header) as regular font in red
    match_display_text_box.tag_add("line_17", "17.0", "17.end")
    match_display_text_box.tag_config("line_17", foreground="Red", font=regular_font)

    # +++++ LEFT COLUMN +++++

    # We're going to style all the market selections in DarkOrange, regular font
    # total goals under 2.5
    match_display_text_box.tag_add("total_goals_under_2p5", "5.0", "5.9")
    match_display_text_box.tag_config("total_goals_under_2p5", foreground="DarkOrange", font=regular_font)
    # total goals over 2.5
    match_display_text_box.tag_add("total_goals_over_2p5", "6.0", "6.8")
    match_display_text_box.tag_config("total_goals_over_2p5", foreground="DarkOrange", font=regular_font)
    # both teams to score
    match_display_text_box.tag_add("both_teams_to_score", "8.0", "8.19")
    match_display_text_box.tag_config("both_teams_to_score", foreground="DarkOrange", font=regular_font)
    # Either team not to score
    match_display_text_box.tag_add("either_team_not_to_score", "9.0", "9.24")
    match_display_text_box.tag_config("either_team_not_to_score", foreground="DarkOrange", font=regular_font)
    # goal rush plus home
    match_display_text_box.tag_add("goal rush plus home", "11.0", "11." + str(len(match_dictionary["home_team"])))
    match_display_text_box.tag_config("goal rush plus home", foreground="DarkOrange", font=regular_font)
    # goal rush plus draw
    match_display_text_box.tag_add("goal rush plus draw", "12.0", "12.4")
    match_display_text_box.tag_config("goal rush plus draw", foreground="DarkOrange", font=regular_font)
    # goal rush plus away
    match_display_text_box.tag_add("goal rush plus away", "13.0", "13." + str(len(match_dictionary["away_team"])))
    match_display_text_box.tag_config("goal rush plus away", foreground="DarkOrange", font=regular_font)
    # win to nil home
    match_display_text_box.tag_add("win to nil home", "15.0", "15." + str(len(match_dictionary["home_team"])))
    match_display_text_box.tag_config("win to nil home", foreground="DarkOrange", font=regular_font)
    # win to nil away
    match_display_text_box.tag_add("win to nil away", "16.0", "16." + str(len(match_dictionary["away_team"])))
    match_display_text_box.tag_config("win to nil away", foreground="DarkOrange", font=regular_font)
    # over two goals plus home
    match_display_text_box.tag_add("over two goals plus home", "18.0", "18." + str(len(match_dictionary["home_team"])))
    match_display_text_box.tag_config("over two goals plus home", foreground="DarkOrange", font=regular_font)
    # over two goals plus draw
    match_display_text_box.tag_add("over two goals plus draw", "19.0", "19.4")
    match_display_text_box.tag_config("over two goals plus draw", foreground="DarkOrange", font=regular_font)
    # over two goals plus away
    match_display_text_box.tag_add("over two goals plus away", "20.0", "20." + str(len(match_dictionary["away_team"])))
    match_display_text_box.tag_config("over two goals plus away", foreground="DarkOrange", font=regular_font)

    # +++++ RIGHT COLUMN +++++

    # win to nil yes
    start_index = "5." + str(left_col_width + 1)
    end_index = "5." + str(left_col_width + 1 + len("Yes"))
    match_display_text_box.tag_add("wtn-et", start_index, end_index)
    match_display_text_box.tag_config("wtn-et", foreground="DarkOrange", font=regular_font)
    # under 1.5 goals
    start_index = "8." + str(left_col_width + 1)
    end_index = "8." + str(left_col_width + 1 + len("Under 1.5"))
    match_display_text_box.tag_add("under_1p5_goals", start_index, end_index)
    match_display_text_box.tag_config("under_1p5_goals", foreground="DarkOrange", font=regular_font)
    # over 1.5 goals
    start_index = "9." + str(left_col_width + 1)
    end_index = "9." + str(left_col_width + 1 + len("Over 1.5"))
    match_display_text_box.tag_add("over_1p5_goals", start_index, end_index)
    match_display_text_box.tag_config("over_1p5_goals", foreground="DarkOrange", font=regular_font)
    # under 3.5 goals
    start_index = "11." + str(left_col_width + 1)
    end_index = "11." + str(left_col_width + 1 + len("Under 3.5"))
    match_display_text_box.tag_add("under_3p5_goals", start_index, end_index)
    match_display_text_box.tag_config("under_3p5_goals", foreground="DarkOrange", font=regular_font)
    # over 3.5 goals
    start_index = "12." + str(left_col_width + 1)
    end_index = "12." + str(left_col_width + 1 + len("Over 3.5"))
    match_display_text_box.tag_add("over_3p5_goals", start_index, end_index)
    match_display_text_box.tag_config("over_3p5_goals", foreground="DarkOrange", font=regular_font)
    # under 4.5 goals
    start_index = "15." + str(left_col_width + 1)
    end_index = "15." + str(left_col_width + 1 + len("Under 4.5"))
    match_display_text_box.tag_add("under_4p5_goals", start_index, end_index)
    match_display_text_box.tag_config("under_4p5_goals", foreground="DarkOrange", font=regular_font)
    # over 4.5 goals
    start_index = "16." + str(left_col_width + 1)
    end_index = "16." + str(left_col_width + 1 + len("Over 4.5"))
    match_display_text_box.tag_add("over_4p5_goals", start_index, end_index)
    match_display_text_box.tag_config("over_4p5_goals", foreground="DarkOrange", font=regular_font)

    return
# ====================================================================================================
# Dev note (22/4/17): handicap price extraction code will be made conditional. When the program encounters
# a blank space for a price, it will set the relevant price to an empty string.
# The price entering functions will be rewritten to deal with the case where a price is not present to
# be entered.
# ====================================================================================================
def extract_match_betting_data_from_code_block(code_block):

    match_dictionary = {}

    # get kick off string
    kick_off_string, code_block = extract_and_remove(code_block, '<i>', '</i>')
    kick_off_string = kick_off_string.replace('Kick off: ', '')
    match_dictionary["kick_off"] = kick_off_string

    # get match_betting_home
    match_betting_home, code_block = extract_and_remove(code_block, '<div class="big_price">', '</div>')
    match_dictionary["match_betting_home"] = match_betting_home

    # get home_team
    home_team, code_block = extract_and_remove(code_block, '<h1>', '</h1>')
    match_dictionary["home_team"] = home_team
    
    # get match_betting_draw
    match_betting_draw, code_block = extract_and_remove(code_block, '"text-align: center;">', '</span>')
    match_dictionary["match_betting_draw"] = match_betting_draw

    # get away_team
    away_team, code_block = extract_and_remove(code_block, '<h1>', '</h1>')
    match_dictionary["away_team"] = away_team

    # get match_betting_away
    match_betting_away, code_block = extract_and_remove(code_block, 'class="big_price">', '</div>')
    match_dictionary["match_betting_away"] = match_betting_away

    # get handicap_betting_home and handicap_home (e.g. "10/11" and "+1"
    handicap_price_and_size, code_block = extract_and_remove(code_block, 'div class="hcap_price">', '</div>')
    elements = handicap_price_and_size.split(' ')
    # print('Total elements =', len(elements))
    # print(elements)
    if len(elements) == 2:
        handicap_betting_home = elements[0]
        handicap_home = elements[1]
    else:
        handicap_betting_home = ''
        handicap_home = ''
    match_dictionary["handicap_betting_home"] = handicap_betting_home
    match_dictionary["handicap_home"] = handicap_home

    # get handicap_betting_draw
    handicap_betting_draw, code_block = extract_and_remove(code_block, 'class="hcap_price">', '</div>')
    match_dictionary["handicap_betting_draw"] = handicap_betting_draw

    # get handicap_betting_away and handicap_away (e.g. "10/11" and "+1"
    handicap_price_and_size, code_block = extract_and_remove(code_block, 'div class="hcap_price">', '</div>')
    elements = handicap_price_and_size.split(' ')
    if len(elements) == 2:
        handicap_betting_away = elements[1]
        handicap_away = elements[0]
    else:
        handicap_betting_away = ''
        handicap_away = ''
    match_dictionary["handicap_betting_away"] = handicap_betting_away    
    match_dictionary["handicap_away"] = handicap_away

    # get total_goals_under_2p5
    total_goals_under_2p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_under_2p5"] = total_goals_under_2p5

    # get win_to_nil_yes
    win_to_nil_yes, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["win_to_nil_yes"] = win_to_nil_yes

    # get total_goals_over_2p5
    total_goals_over_2p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_over_2p5"] = total_goals_over_2p5

    # get new_goal_rush_yes
    new_goal_rush_yes, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["new_goal_rush_yes"] = new_goal_rush_yes

    # get total_goals_under_1p5
    total_goals_under_1p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_under_1p5"] = total_goals_under_1p5

    # get new_goal_rush_no
    new_goal_rush_no, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["new_goal_rush_no"] = new_goal_rush_no

    # get total_goals_over_1p5
    total_goals_over_1p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_over_1p5"] = total_goals_over_1p5

    # get goal_rush_plus_home
    goal_rush_plus_home, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["goal_rush_plus_home"] = goal_rush_plus_home

    # get total_goals_under_3p5
    total_goals_under_3p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_under_3p5"] = total_goals_under_3p5

    # get goal_rush_plus_draw
    goal_rush_plus_draw, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["goal_rush_plus_draw"] = goal_rush_plus_draw

    # get total_goals_over_3p5
    total_goals_over_3p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_over_3p5"] = total_goals_over_3p5

    # get goal_rush_plus_away
    goal_rush_plus_away, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["goal_rush_plus_away"] = goal_rush_plus_away

    # get win_to_nil_home
    win_to_nil_home, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["win_to_nil_home"] = win_to_nil_home

    # get total_goals_under_4p5
    total_goals_under_4p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_under_4p5"] = total_goals_under_4p5
    # print('total_goals_under_4p5 =', total_goals_under_4p5)

    # get win_to_nil_away
    win_to_nil_away, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["win_to_nil_away"] = win_to_nil_away

    # get total_goals_over_4p5
    total_goals_over_4p5, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["total_goals_over_4p5"] = total_goals_over_4p5

    # get over_two_goals_plus_home
    over_two_goals_plus_home, code_block = extract_and_remove(code_block, '<div class="price">', '</div>')
    match_dictionary["over_two_goals_plus_home"] = over_two_goals_plus_home

    # get over_two_goals_plus_draw
    over_two_goals_plus_draw, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["over_two_goals_plus_draw"] = over_two_goals_plus_draw

    # get over_two_goals_plus_away
    over_two_goals_plus_away, code_block = extract_and_remove(code_block, 'class="price">', '</div>')
    match_dictionary["over_two_goals_plus_away"] = over_two_goals_plus_away

    # set win_to_nil_no; it's always "1/100"
    match_dictionary["win_to_nil_no"] = "1/100"
    
    # print('=========================================================')
    # print('match_dictionary:')
    # keys = list(match_dictionary.keys())
    # keys.sort()
    # for key in keys:
        # print(key, "\t:", match_dictionary[key])

    return match_dictionary
# ====================================================================================================
# Helper function for extracting betting data from a code block. Does this:
# 1. searches big_string for start_string and end_string
# 2. extracts the substring located between start_string and end_string
# 3. removes text from big_string up to the end of end_string
# 4. returns [extracted_string, big_string]
# ====================================================================================================
def extract_and_remove(big_string, start_string, end_string):

    # extract string
    start = big_string.find(start_string) + len(start_string)
    loc = start # used to have +1 on end
    while big_string[loc:loc + len(end_string)] != end_string:
        loc += 1
    extracted_string = big_string[start:loc]
    big_string = big_string[loc + len(end_string):]

    return [extracted_string, big_string]
# ====================================================================================================
# Move to previous match. If we're at the first match, cycle round to the last match.
def move_to_previous_match():

    global football_betting
    global current_match_index

    if current_match_index > 0:
        current_match_index -= 1
    else:
        current_match_index = len(football_betting) - 1

    # display match
    display_football_match_in_text_widget(current_match_index)

    update_match_list_window()

    return
# ====================================================================================================
# Move to next match. If we're at the last match, cycle round to the first match.
def move_to_next_match():

    global football_betting
    global current_match_index

    if current_match_index == len(football_betting) - 1:
        current_match_index = 0
    else:
        current_match_index += 1

    # display match
    display_football_match_in_text_widget(current_match_index)

    update_match_list_window()

    return
# ====================================================================================================
# Type a bunch of test lines; used to get the focus onto the remote desktop window as there is
# sometimes a delay before the remote window reacts to actions initiated by the pyautogui library
# ====================================================================================================
def type_test_lines():

    direction = 0
    for count in range(total_test_lines):
        kb_type("test test")
        time.sleep(0.2)
        if direction == 0:
            kb_press('down')
        else:
            kb_press('up')
            kb_press('up')
        direction = 1 - direction

    kb_press('up')
    time.sleep(0.5)
    kb_press('up')
    
    return
# ====================================================================================================
# Rebuild a team name string with capital letters at the beginning of each word.
# e.g. Change "manchester united" to "Manchester United"
def rebuild_team_name_with_capital_first_letters(team_name):

    team_name = team_name.strip()
    words = team_name.split(" ")
    rebuilt_name = ''
    rebuilt_words = []
    for word in words:
        rebuilt_word = word[0].upper()
        if len(word) > 1:
            rebuilt_word += word[1:]
        rebuilt_words.append(rebuilt_word)
    rebuilt_name = " ".join(rebuilt_words)

    return rebuilt_name
# ====================================================================================================
def show_clickable_settings_window():

    # make these widgets global so we can access them from save_clickable_coordinates()
    global save_button_x_text
    global save_button_y_text
    global next_market_button_x_text
    global next_market_button_y_text
    global handicap_cell_x_text
    global handicap_cell_y_text
    global top_left_cell_x_text
    global top_left_cell_y_text
    global keyboard_q_x_text
    global keyboard_q_y_text
    global letter_typing_delay_entry
    global test_cell_x_text
    global test_cell_y_text
    global test_line_text_text
    global top_price_cell_x_text
    global top_price_cell_y_text
    global total_test_lines_text

    global match1_match_betting_x_text
    global match1_match_betting_y_text
    global match2_match_betting_x_text
    global match2_match_betting_y_text
    global match3_match_betting_x_text
    global match3_match_betting_y_text

    global clickable_settings_window

    # access the following global variables in order to store the values we read from
    # "settings_csv"
    global save_x
    global save_y
    global next_market_x
    global next_market_y
    global handicap_cell_x
    global handicap_cell_y
    global top_left_cell_x
    global top_left_cell_y
    global keyboard_q_x
    global keyboard_q_y
    global test_cell_x
    global test_cell_y
    global top_price_cell_x
    global top_price_cell_y
    global letter_typing_delay
    global test_line_text
    global total_test_lines

    global match1_match_betting_x
    global match1_match_betting_y
    global match2_match_betting_x
    global match2_match_betting_y
    global match3_match_betting_x
    global match3_match_betting_y

    # read the settings from "settings.csv"
    infile = open('settings.csv', 'r')
    lines = infile.readlines()
    infile.close()

    # get rid of blank/whitespace lines
    kept_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            kept_lines.append(line)
    lines = kept_lines

    # extract settings
    settings_dictionary = {}
    for line in lines:
        elements = line.split(',')
        # print(elements)
        settings_dictionary[elements[0].strip()] = elements[1].strip()

    # Test print
    # keys = list(settings_dictionary.keys())
    # for key in keys:
        # print(key, "\t", settings_dictionary[key])

    # Build the settings window
    clickable_settings_window = Toplevel(root)
    clickable_settings_window.title("Set Coordinates")
    clickable_settings_window.grab_set()

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # create frame to hold the x,y coordinate entries
    # Format will be:
    #
    #                         X     Y
    # Save Button
    # Next Market Button
    # Handicap Cell
    # Top Left Cell
    # +++++++++++++++++++++++++++++++++++++++++++++++
    x_y_frame = ttk.Frame(clickable_settings_window)

    # First row contains X and Y labels
    x_label = Label(clickable_settings_window, text="X", width="5")
    x_label.grid(row=0, column=1, sticky=W)
    y_label = Label(clickable_settings_window, text="Y", width="5")
    y_label.grid(row=0, column=2, sticky=W)
    # Save Button label and Text entries
    save_button_label = Label(clickable_settings_window, text="Save Button")
    save_button_label.grid(row=1, column=0, sticky=E)
    save_button_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    save_button_x_text.grid(row=1, column=1)
    save_button_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    save_button_y_text.grid(row=1, column=2)
    # Next market button label and Text entries
    next_market_button_label = Label(clickable_settings_window, text="Next Market Button")
    next_market_button_label.grid(row=2, column=0, sticky=E)
    next_market_button_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    next_market_button_x_text.grid(row=2, column=1)
    next_market_button_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    next_market_button_y_text.grid(row=2, column=2)
    # Handicap cell label and Text entries
    handicap_cell_label = Label(clickable_settings_window, text="Handicap Cell")
    handicap_cell_label.grid(row=3, column=0, sticky=E)
    handicap_cell_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    handicap_cell_x_text.grid(row=3, column=1)
    handicap_cell_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    handicap_cell_y_text.grid(row=3, column=2)
    # Top left cell label and Text entries
    top_left_cell_label = Label(clickable_settings_window, text="Top Left Cell")
    top_left_cell_label.grid(row=4, column=0, sticky=E)
    top_left_cell_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    top_left_cell_x_text.grid(row=4, column=1)
    top_left_cell_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    top_left_cell_y_text.grid(row=4, column=2)
    # Virtual keyboard letter Q - x and y coordinates
    keyboard_q_label = Label(clickable_settings_window, text="Keyboard Q")
    keyboard_q_label.grid(row=5, column=0, sticky=E)
    keyboard_q_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    keyboard_q_x_text.grid(row=5, column=1)
    keyboard_q_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    keyboard_q_y_text.grid(row=5, column=2)
    # Test cell coordinates
    test_cell_label = Label(clickable_settings_window, text="Scroll Down")
    test_cell_label.grid(row=6, column=0, sticky=E)
    test_cell_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    test_cell_x_text.grid(row=6, column=1)
    test_cell_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    test_cell_y_text.grid(row=6, column=2)
    # Top price cell coordinates
    top_price_cell_label = Label(clickable_settings_window, text="Top Price Cell")
    top_price_cell_label.grid(row=7, column=0, sticky=E)
    top_price_cell_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    top_price_cell_x_text.grid(row=7, column=1)
    top_price_cell_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    top_price_cell_y_text.grid(row=7, column=2)

    # Letter typing delay on row 8
    letter_typing_delay_label = Label(clickable_settings_window, text="Typing Delay")
    letter_typing_delay_label.grid(row=8, column=0, sticky=E)
    letter_typing_delay_entry = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    letter_typing_delay_entry.grid(row=8, column=1)
    # Label on row 9 to separate letter typing delay above from save button below
    coordinates_spacer_label_2 = Label(clickable_settings_window, text=" ", height=1)
    coordinates_spacer_label_2.grid(row=9, column=0, sticky=E)
    # Test line text
    test_line_text_label = Label(clickable_settings_window, text="Test Line Text")
    test_line_text_label.grid(row=10, column=0, sticky=E)
    
    test_line_text_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    test_line_text_text.grid(row=10, column=1)
    # Total test lines text widget
    total_test_lines_label = Label(clickable_settings_window, text="Total Test Lines")
    total_test_lines_label.grid(row=11, column=0, sticky=E)
    
    total_test_lines_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    total_test_lines_text.grid(row=11, column=1)
    # Label on row 12 to separate coordinate entries above from letter typing delay below
    coordinates_spacer_label_3 = Label(clickable_settings_window, text=" ", height=1)
    coordinates_spacer_label_3.grid(row=12, column=0, sticky=E)

    # Match #1 match betting coordinates on row 13
    match1_match_betting_label = Label(clickable_settings_window, text="Match #1 Match Betting")
    match1_match_betting_label.grid(row=13, column=0, sticky=E)
    match1_match_betting_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    match1_match_betting_x_text.grid(row=13, column=1)
    match1_match_betting_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    match1_match_betting_y_text.grid(row=13, column=2)

    # Match #2 match betting coordinates on row 14
    match2_match_betting_label = Label(clickable_settings_window, text="Match #2 Match Betting")
    match2_match_betting_label.grid(row=14, column=0, sticky=E)
    match2_match_betting_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    match2_match_betting_x_text.grid(row=14, column=1)
    match2_match_betting_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    match2_match_betting_y_text.grid(row=14, column=2)

    # Match #3 match betting coordinates on row 15
    match3_match_betting_label = Label(clickable_settings_window, text="Match #3 Match Betting")
    match3_match_betting_label.grid(row=15, column=0, sticky=E)
    match3_match_betting_x_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    match3_match_betting_x_text.grid(row=15, column=1)
    match3_match_betting_y_text = Text(clickable_settings_window, width=5, height=1, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold'))
    match3_match_betting_y_text.grid(row=15, column=2)

    # Spacer label in row 16
    coordinates_spacer_label_4 = Label(clickable_settings_window, text=" ", height=1)
    coordinates_spacer_label_4.grid(row=16, column=0, sticky=E)

    # Save button on row 17
    coordinates_save_button = ttk.Button(clickable_settings_window, text='Save', width=5,
                                            command=save_clickable_coordinates)
    coordinates_save_button.grid(row=17, column=1, sticky=E)

    # Stuff all the information in settings_dictionary into the relevant settings window widgets
    save_button_x_text.insert(END, settings_dictionary["save_x"])
    save_button_y_text.insert(END, settings_dictionary["save_y"])
    next_market_button_x_text.insert(END, settings_dictionary["next_market_x"])
    next_market_button_y_text.insert(END, settings_dictionary["next_market_y"])
    handicap_cell_x_text.insert(END, settings_dictionary["handicap_cell_x"])
    handicap_cell_y_text.insert(END, settings_dictionary["handicap_cell_y"])
    top_left_cell_x_text.insert(END, settings_dictionary["top_left_cell_x"])
    top_left_cell_y_text.insert(END, settings_dictionary["top_left_cell_y"])
    keyboard_q_x_text.insert(END, settings_dictionary["keyboard_q_x"])
    keyboard_q_y_text.insert(END, settings_dictionary["keyboard_q_y"])
    test_cell_x_text.insert(END, settings_dictionary["test_cell_x"])
    test_cell_y_text.insert(END, settings_dictionary["test_cell_y"])
    top_price_cell_x_text.insert(END, settings_dictionary["top_price_cell_x"])
    top_price_cell_y_text.insert(END, settings_dictionary["top_price_cell_y"])
    letter_typing_delay_entry.insert(END, settings_dictionary["letter_typing_delay"])
    test_line_text_text.insert(END, settings_dictionary["test_line_text"])
    total_test_lines_text.insert(END, settings_dictionary["total_test_lines"])

    match1_match_betting_x_text.insert(END, settings_dictionary["match1_match_betting_x"])
    match1_match_betting_y_text.insert(END, settings_dictionary["match1_match_betting_y"])
    match2_match_betting_x_text.insert(END, settings_dictionary["match2_match_betting_x"])
    match2_match_betting_y_text.insert(END, settings_dictionary["match2_match_betting_y"])
    match3_match_betting_x_text.insert(END, settings_dictionary["match3_match_betting_x"])
    match3_match_betting_y_text.insert(END, settings_dictionary["match3_match_betting_y"])

    # Grid the x_y_frame
    x_y_frame.grid(row=0, column=0, sticky=W)

    return
# ====================================================================================================
# Check each of the Text widgets in the set coordinates window. If they contain a number, set the
# relevant global variables, destroy the set coordinates window and fire up a confirmation popup.
#
# Save the settings in a csv file named "settings.csv"
#
# If keyboard Q x and y coordinates have been entered, call the function to map the windows
# accessibility onscreen keyboard.
# ====================================================================================================
def save_clickable_coordinates():

    # We need to access the clickable settings window
    global clickable_settings_window

    # Inside this function, we're going to set the following global variables:
    global save_x
    global save_y
    global next_market_x
    global next_market_y
    global handicap_cell_x
    global handicap_cell_y
    global top_left_cell_x
    global top_left_cell_y
    global keyboard_q_x
    global keyboard_q_y
    global test_cell_x
    global test_cell_y
    global top_price_cell_x
    global top_price_cell_y
    global letter_typing_delay
    global test_line_text
    global total_test_lines
    
    global match1_match_betting_x
    global match1_match_betting_y
    global match2_match_betting_x
    global match2_match_betting_y
    global match3_match_betting_x
    global match3_match_betting_y

    # Get the text in all the Text widgets in the Set Coordinates window.
    # If the text isn't entirely whitespace, set the relevant global variable.
    # save_x
    text = save_button_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        save_x = int(text)
    else:
        save_x = -1
    # save_y
    text = save_button_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        save_y = int(text)
    else:
        save_y = -1
    # next_market_x
    text = next_market_button_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        next_market_x = int(text)
    else:
        next_market_x = -1
    # next_market_y
    text = next_market_button_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        next_market_y = int(text)
    else:
        next_market_y = -1
    # handicap_cell_x
    text = handicap_cell_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        handicap_cell_x = int(text)
    else:
        handicap_cell_x = -1
    # handicap_cell_y
    text = handicap_cell_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        handicap_cell_y = int(text)
    else:
        handicap_cell_y = -1
    # top_left_cell_x
    text = top_left_cell_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        top_left_cell_x = int(text)
    else:
        top_left_cell_x = -1
    # top_left_cell_y
    text = top_left_cell_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        top_left_cell_y = int(text)
    else:
        top_left_cell_y = -1
    # keyboard_q_x
    text = keyboard_q_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        keyboard_q_x = int(text)
    else:
        keyboard_q_x = -1
    # keyboard_q_y
    text = keyboard_q_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        keyboard_q_y = int(text)
    else:
        keyboard_q_y = -1
    # test_cell_x
    text = test_cell_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        test_cell_x = int(text)
    else:
        test_cell_x = -1
    # test_cell_y
    text = test_cell_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        test_cell_y = int(text)
    else:
        test_cell_y = -1
    # top_price_cell_x
    text = top_price_cell_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        top_price_cell_x = int(text)
    else:
        top_price_cell_x = -1
    # top_price_cell_y
    text = top_price_cell_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        top_price_cell_y = int(text)
    else:
        top_price_cell_y = -1
    # letter_typing_delay
    text = letter_typing_delay_entry.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        letter_typing_delay = float(text)
    else:
        letter_typing_delay = 0
    # test_line_text
    text = test_line_text_text.get("1.0", END) #####
    text = text.strip()
    if len(text) > 0:
        test_line_text = text
    else:
        test_line_text = 'test'
    # total_test_lines
    text = total_test_lines_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        total_test_lines = int(text)
    else:
        total_test_lines = 3
        
    # match1_match_betting_x
    text = match1_match_betting_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        match1_match_betting_x = int(text)
    else:
        match1_match_betting_x = -1
    # match1_match_betting_y
    text = match1_match_betting_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        match1_match_betting_y = int(text)
    else:
        match1_match_betting_y = -1

    # match2_match_betting_x
    text = match2_match_betting_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        match2_match_betting_x = int(text)
    else:
        match2_match_betting_x = -1
    # match2_match_betting_y
    text = match2_match_betting_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        match2_match_betting_y = int(text)
    else:
        match2_match_betting_y = -1

    # match3_match_betting_x
    text = match3_match_betting_x_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        match3_match_betting_x = int(text)
    else:
        match3_match_betting_x = -1
    # match3_match_betting_y
    text = match3_match_betting_y_text.get("1.0", END)    
    text = text.strip()
    if len(text) > 0:
        match3_match_betting_y = int(text)
    else:
        match3_match_betting_y = -1

    # print('coordinates read from settings window:')
    # print('match1_match_betting_x =', match1_match_betting_x)
    # print('match1_match_betting_y =', match1_match_betting_y)
    # print('match2_match_betting_x =', match2_match_betting_x)
    # print('match2_match_betting_y =', match2_match_betting_y)
    # print('match3_match_betting_x =', match3_match_betting_x)
    # print('match3_match_betting_y =', match3_match_betting_y)

    # build settings_text to write to the file "settings.csv"
    # format is:
    # save_x,<value>
    # save_y,<value>
    # next_market_x,<value>
    # next_market_y,<value>
    # handicap_cell_x,<value>
    # handicap_cell_y,<value>
    # top_left_cell_x,<value>
    # top_left_cell_y,<value>
    # keyboard_q_x,<value>
    # keyboard_q_y,<value>
    # test_cell_x,<value>
    # test_cell_y,<value>
    # letter_typing_delay,<value>
    # test_line_text,<value>
    # total_test_lines,<value>
    settings_text = 'save_x,' + str(save_x) + "\n"
    settings_text += 'save_y,' + str(save_y) + "\n"
    settings_text += 'next_market_x,' + str(next_market_x) + "\n"
    settings_text += 'next_market_y,' + str(next_market_y) + "\n"
    settings_text += 'handicap_cell_x,' + str(handicap_cell_x) + "\n"
    settings_text += 'handicap_cell_y,' + str(handicap_cell_y) + "\n"
    settings_text += 'top_left_cell_x,' + str(top_left_cell_x) + "\n"
    settings_text += 'top_left_cell_y,' + str(top_left_cell_y) + "\n"
    settings_text += 'keyboard_q_x,' + str(keyboard_q_x) + "\n"
    settings_text += 'keyboard_q_y,' + str(keyboard_q_y) + "\n"
    settings_text += 'test_cell_x,' + str(test_cell_x) + "\n"
    settings_text += 'test_cell_y,' + str(test_cell_y) + "\n"
    settings_text += 'top_price_cell_x,' + str(top_price_cell_x) + "\n"
    settings_text += 'top_price_cell_y,' + str(top_price_cell_y) + "\n"
    settings_text += 'letter_typing_delay,' + str(letter_typing_delay) + "\n"
    settings_text += 'test_line_text,' + str(test_line_text) + "\n"
    settings_text += 'total_test_lines,' + str(total_test_lines) + "\n"
    settings_text += 'match1_match_betting_x,' + str(match1_match_betting_x) + "\n"
    settings_text += 'match1_match_betting_y,' + str(match1_match_betting_y) + "\n"
    settings_text += 'match2_match_betting_x,' + str(match2_match_betting_x) + "\n"
    settings_text += 'match2_match_betting_y,' + str(match2_match_betting_y) + "\n"
    settings_text += 'match3_match_betting_x,' + str(match3_match_betting_x) + "\n"
    settings_text += 'match3_match_betting_y,' + str(match3_match_betting_y) + "\n"

    # write settings to outfile
    outfile = open('settings.csv', 'w')
    outfile.write(settings_text)
    outfile.close()
    
    # if keyboard_q_x and keyboard_q_y have been called, map the keyboard
    map_keys()

    # destroy clickable_settings_window
    clickable_settings_window.destroy()    

    # Create "Settings Saved" confirmation popup
    messagebox.showinfo("Settings Saved", "Clickable coordinates have been saved.")

    return
# ====================================================================================================
# Enter the match betting for a match; assumes the match betting market is onscreen and the cell
# containing the home price has been clicked
# ====================================================================================================
def enter_match_betting():

    current_match = football_betting[current_match_index]

    # check if there's betting to enter; if not, return without doing anything
    total_betting_length = len(current_match["match_betting_home"])
    total_betting_length += len(current_match["match_betting_draw"])
    total_betting_length += len(current_match["match_betting_away"])
    if total_betting_length == 0:
        time.sleep(1)
        return

    # if we've fallen through, there's betting to enter, so let's get on with it...
    map_keys()

    # type test lines
    type_test_lines()

    # enter prices
    kb_type(current_match["match_betting_home"])
    kb_press('down')
    # time.sleep(0.2)
    kb_type(current_match["match_betting_draw"])
    kb_press('down')
    # time.sleep(0.2)
    kb_type(current_match["match_betting_away"])
    kb_press('up')
    time.sleep(0.2)

    # click save button
    pyautogui.click(save_x, save_y)
    time.sleep(0.5)
    
    return
# ====================================================================================================
# Enter the handicap betting for a match; assumes the handicap betting market is onscreen and the home
# price cell has been clicked
# ====================================================================================================
def enter_handicap_betting():

    # get current match
    current_match = football_betting[current_match_index]

    # check if there's betting to enter; if not, return without doing anything
    total_betting_length = len(current_match["handicap_betting_home"])
    total_betting_length += len(current_match["handicap_betting_draw"])
    total_betting_length += len(current_match["handicap_betting_away"])
    if total_betting_length == 0 or ((total_betting_length == 3) and (current_match["handicap_betting_draw"]) == "==="):
        time.sleep(1)
        return

    # if we've fallen through, there's betting to enter, so let's get on with it...
    map_keys()

    # enter home, draw, away betting
    kb_type(current_match["handicap_betting_home"])
    kb_press('down')
    time.sleep(0.2)
    kb_type(current_match["handicap_betting_draw"])
    kb_press('down')
    time.sleep(0.2)
    kb_type(current_match["handicap_betting_away"])
    kb_press('up')
    time.sleep(0.2)
    
    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Regenerate the correct scores for a match; assumes the correct score market is onscreen and the user
# has clicked one of the cells
# ====================================================================================================
def regenerate_correct_scores():

    # get current match
    current_match = football_betting[current_match_index]

    # if there's no match betting, we don't need to generate correct scores
    total_match_betting_length = len(current_match["match_betting_home"])
    total_match_betting_length += len(current_match["match_betting_draw"])
    total_match_betting_length += len(current_match["match_betting_away"])
    if total_match_betting_length == 0:
        time.sleep(1)
        return

    # if we've fallen through, we've entered match betting, so let's regenerate the correct scores...
    map_keys()
    # type_test_lines()

    # right click the top left cell
    pyautogui.rightClick(top_left_cell_x, top_left_cell_y)
    time.sleep(1) # changed 18/6/18
    # click the "Regenerate Correct Scores" option; this assumes that the menu that pops up upon
    # right-clicking the top cell has its bottom left corner at the click position, not its
    # top left corner at the click position (i.e. that the menu is drawn up to the right of the
    # click position, not down to the right)
    pyautogui.click(top_left_cell_x + 107, top_left_cell_y - 278)
    time.sleep(1) # changed 18/6/18
    # click the save button
    pyautogui.click(save_x, save_y)
    time.sleep(1) # changed 18/6/18

    return
# ====================================================================================================
# Regenerate the halftime/fulltime market; assumes the halftime/fulltime market is onscreen and the
# user has clicked a price cell somewhere in the market
# ====================================================================================================
def regenerate_halftime_fulltime():

    # get current match
    current_match = football_betting[current_match_index]

    # if there's no match betting, we don't need to generate halftime fulltime
    total_match_betting_length = len(current_match["match_betting_home"])
    total_match_betting_length += len(current_match["match_betting_draw"])
    total_match_betting_length += len(current_match["match_betting_away"])
    if total_match_betting_length == 0:
        time.sleep(1)
        return

    # if we've fallen through, we've entered match betting, so let's regenerate halftime fulltime...
    map_keys()
    # type_test_lines()

    # right click the top left cell
    pyautogui.rightClick(top_left_cell_x, top_left_cell_y)
    time.sleep(1)
    # click the "Regenerate Halftime/Fulltime Scores" option
    pyautogui.click(top_left_cell_x + 107, top_left_cell_y - 278)
    time.sleep(1)
    # click the save button
    pyautogui.click(save_x, save_y)
    time.sleep(1)

    return
# ====================================================================================================
# Enter the 2.5 Goals betting market; assumes the user has clicked the under 2.5 price cell
# ====================================================================================================
def enter_2p5_goals_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["total_goals_under_2p5"].strip()) == 0)
         and (len(current_match["total_goals_over_2p5"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["total_goals_under_2p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["total_goals_over_2p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type('n/')
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the new goal rush betting market; assumes the user has clicked the "both teams to score"
# price cell.
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_new_goal_rush_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["new_goal_rush_yes"].strip()) == 0)
         and (len(current_match["new_goal_rush_no"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["new_goal_rush_yes"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["new_goal_rush_no"])
    kb_press("down")
    time.sleep(0.2)
    kb_type('n/')
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the goal rush plus betting market; assumes the user has clicked the home price cell
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_goal_rush_plus_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    len_1 = len(current_match["goal_rush_plus_home"].strip())
    len_2 = len(current_match["goal_rush_plus_draw"].strip())
    len_3 = len(current_match["goal_rush_plus_away"].strip())
    if (((len_1 == 0) and (len_2 == 0)) and (len_3 == 0)):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["goal_rush_plus_home"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["goal_rush_plus_draw"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["goal_rush_plus_away"])
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the win to nil betting market; assumes the user has clicked the home price cell
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_win_to_nil_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["win_to_nil_home"].strip()) == 0)
         and (len(current_match["win_to_nil_away"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["win_to_nil_home"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["win_to_nil_away"])
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the over two goals plus betting market; assumes the user has clicked on the home price cell.
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_over_two_goals_plus_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test; if there are no prices to enter, immediately return
    len_1 = len(current_match["over_two_goals_plus_home"].strip())
    len_2 = len(current_match["over_two_goals_plus_draw"].strip())
    len_3 = len(current_match["over_two_goals_plus_away"].strip())
    if (((len_1 == 0) and (len_2 == 0)) and (len_3 == 0)):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["over_two_goals_plus_home"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["over_two_goals_plus_draw"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["over_two_goals_plus_away"])
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the WTN-ET betting market (aka Goal Rush Winner). Assumes the user has clicked the Yes price
# cell.
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_wtn_et_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["win_to_nil_yes"].strip()) == 0)
         and (len(current_match["win_to_nil_no"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["win_to_nil_yes"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["win_to_nil_no"])
    kb_press("down")
    time.sleep(0.2)
    kb_type('n/')
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the 1.5 Goals betting market; assumes the user has clicked the under 1.5 goals price cell.
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_1p5_goals_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["total_goals_under_1p5"].strip()) == 0)
         and (len(current_match["total_goals_over_1p5"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["total_goals_under_1p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["total_goals_over_1p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type('n/')
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the 3.5 Goals betting market; assumes the user has clicked the under 3.5 goals price cell.
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_3p5_goals_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["total_goals_under_3p5"].strip()) == 0)
         and (len(current_match["total_goals_over_3p5"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["total_goals_under_3p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["total_goals_over_3p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type('n/')
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter the 4.5 Goals betting market; assumes the user has clicked the under 4.5 goals price cell.
# Pass a value of zero to the enter_test_lines parameter in order to skip entering test lines.
# ====================================================================================================
def enter_4p5_goals_betting(enter_test_lines = 1):

    # get current match
    current_match = football_betting[current_match_index]

    # sanity test - if there are no prices to enter, immediately return
    if ( (len(current_match["total_goals_under_4p5"].strip()) == 0)
         and (len(current_match["total_goals_over_4p5"].strip()) == 0) ):
        return

    map_keys()
    if enter_test_lines:
        type_test_lines()
    else:
        time.sleep(0.2)

    # type in the prices
    kb_type(current_match["total_goals_under_4p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type(current_match["total_goals_over_4p5"])
    kb_press("down")
    time.sleep(0.2)
    kb_type('n/')
    kb_press("up")
    time.sleep(0.2)

    # click the save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter match betting, then last 9 markets (2.5 goals down to 4.5 goals)
# Assumes the user has clicked on the cell containing the home price in the match betting market,
# just before clicking the button that calls this function
#
# Optionally enter handicap betting, depending on hcap_checkbutton_value
# ====================================================================================================
def enter_match_betting_then_2p5_goals_down_to_4p5_goals_markets():

    enter_match_betting()

    # move to next market (handicap market)
    click_next_market_and_move_to_home_price_cell()

    # if the "Enter Handicap Betting" checkbutton is ticked, enter the handicap betting
    enter_the_handicap_betting = hcap_checkbutton_value.get()
    if enter_the_handicap_betting:
        # enter handicap betting
        enter_handicap_betting()

    # move to next market (correct scores)
    click_next_market_and_move_to_home_price_cell()

    # if the "Regenerate correct scores" button is ticked, regenerate the correct scores
    regenerate_the_correct_scores = cscores_checkbutton_value.get()
    if regenerate_the_correct_scores:
        regenerate_correct_scores()

    # move to next market (halftime/fulltime prices)
    click_next_market_and_move_to_home_price_cell()

    # if "Regenerate ht/ft" button is ticked, regenerate the halftime/fulltime prices
    regenerate_the_htft = htft_checkbutton_value.get()
    if regenerate_the_htft:
        regenerate_halftime_fulltime()

    # move to next market (total Goals)
    click_next_market_and_move_to_home_price_cell()

    enter_2p5_goals_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_new_goal_rush_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_goal_rush_plus_betting(0)
    
    click_next_market_and_move_to_home_price_cell()

    enter_win_to_nil_betting(0)
    
    click_next_market_and_move_to_home_price_cell()

    enter_over_two_goals_plus_betting(0)
    
    click_next_market_and_move_to_home_price_cell()

    enter_wtn_et_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_1p5_goals_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_3p5_goals_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_4p5_goals_betting(0)

    return
# ====================================================================================================
# Click the next market button then move to the home price cell
# (This works for transitioning between 2.5 Goals market all the way down to 4.5 Goals market,
# a single market at a time)
# ====================================================================================================
def click_next_market_and_move_to_home_price_cell():

    # click next market button
    # time.sleep(0.1) # was 0.5, then 0.1
    pyautogui.click(next_market_x, next_market_y)

    # click top (home) price cell
    # time.sleep(0.1) # was 0.5, then 0.1
    pyautogui.click(top_price_cell_x, top_price_cell_y)
    # time.sleep(0.1) # was 0.2, then 0.1

    return
# ====================================================================================================
# Enter betting from 2.5 goals onwards; assumes the user has clicked on the top price cell in the
# 2.5 goals or more betting market
# ====================================================================================================
def enter_2p5_goals_betting_onwards():

    type_test_lines()

    # enter 2.5 goals
    enter_2p5_goals_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_new_goal_rush_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_goal_rush_plus_betting(0)
    
    click_next_market_and_move_to_home_price_cell()

    enter_win_to_nil_betting(0)
    
    click_next_market_and_move_to_home_price_cell()

    enter_over_two_goals_plus_betting(0)
    
    click_next_market_and_move_to_home_price_cell()

    enter_wtn_et_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_1p5_goals_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_3p5_goals_betting(0)

    click_next_market_and_move_to_home_price_cell()

    enter_4p5_goals_betting(0)

    return
# ====================================================================================================
# Calculate the max line width for a match in the match list window.
#
# Matches in the match list window are in the following format:
# <match no> <home team> v <away team>
# For example:
# 001 Man Utd v Chelsea
# 002 Wigan v Southend
# 003 Dumbarton v Eastleigh
# etc.
# ====================================================================================================
def calculate_match_list_max_line_width():

    # football_betting[current_line_no]
    max_line_length = 0
    for match in football_betting:
        line_length = len(match['home_team']) + len(match['away_team']) + 7
        if line_length > max_line_length:
            max_line_length = line_length

    print('max_line_length =', max_line_length)

    return max_line_length
# ====================================================================================================
# Build a list of matches and stick it in the match_list_window
# Matches in the match list window are in the following format:
# <match no> <home team> v <away team>
# For example:
# 001 Man Utd v Chelsea
# 002 Wigan v Southend
# 003 Dumbarton v Eastleigh
# etc.
# ====================================================================================================
def update_match_list_window():

    text = ''
    match_no = 1

    for match in football_betting:
        # add match no
        match_no_string = str(match_no)
        while len(match_no_string) < 3:
            match_no_string = '0' + match_no_string
        text += match_no_string + ' '
        # build match line
        text += match['home_team'] + ' v ' + match['away_team'] + "\n"
        match_no += 1
    text = text.strip()

    # stuff text into match_list_text_widget
    match_list_text_widget.delete(1.0, END)
    match_list_text_widget.insert(END, text)

    # tag each line so that the match number is aqua
    # match_display_text_box.tag_add("line_1", "1.0", "1.end")
    # match_display_text_box.tag_config("line_1", foreground="Aquamarine", font=regular_font)
    for count in range(1, len(football_betting) + 1):
        # tag match no and make it green
        tag_name = "line_" + str(count)
        tag_start_string = str(count) + '.0'
        tag_end_string = str(count) + '.3'
        match_list_text_widget.tag_add(tag_name, tag_start_string, tag_end_string)
        match_list_text_widget.tag_config(tag_name, foreground="Chartreuse")
        # tag the 'v' between home and away teams and make it aqua
        match = football_betting[count - 1]
        tag_name = "line_" + str(count) + '_v'
        start_pos = len(match['home_team']) + 4
        end_pos = start_pos + 3
        tag_start_string = str(count) + '.' + str(start_pos)
        tag_end_string = str(count) + '.' + str(end_pos)
        match_list_text_widget.tag_add(tag_name, tag_start_string, tag_end_string)
        match_list_text_widget.tag_config(tag_name, foreground="Aqua")

    # highlight the current match in the match list window
    # football_betting[current_match_index]
    current_match = football_betting[current_match_index]
    line_length = len(current_match['home_team']) + len(current_match['away_team']) + 7
    tag_start_string = str(current_match_index + 1) + '.0'
    tag_end_string = str(current_match_index + 1) + '.' + str(line_length)
    match_list_text_widget.tag_add("current_match", tag_start_string, tag_end_string)
    match_list_text_widget.tag_config("current_match", foreground="Black", background="Yellow")

    # We want to see the current match plus up to the next 20 lines
    # ensure the current match is visible in the match list widget
    index_to_see = current_match_index + 19
    if index_to_see > len(football_betting):
        index_to_see = len(football_betting) + 1
    index_to_see = str(index_to_see + 1) + '.0'
    match_list_text_widget.see(index_to_see)

    return
# ====================================================================================================
# Enter all the markets for three matches in a row.
# Yep, we're going to enter 30 markets at the click of a button...
# Assumes we're already focused the cursor on the home price of the match betting market of the
# first match for which we're entering betting.
# ====================================================================================================
def enter_three_matches():

    # enter betting for first match
    enter_match_betting_then_2p5_goals_down_to_4p5_goals_markets()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # pause, then move to match #2
    time.sleep(2)

    # move to next match in betting
    pyautogui.click(match2_match_betting_x, match2_match_betting_y)
    time.sleep(1)
    pyautogui.click(top_price_cell_x, top_price_cell_y)
    time.sleep(1)

    # display betting for match #2 in window, update match list window
    move_to_next_match()
    time.sleep(1)
    
    # enter betting for match #2
    enter_match_betting_then_2p5_goals_down_to_4p5_goals_markets()
    time.sleep(1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # pause, then move to match #3
    time.sleep(2)

    # move to next match in betting
    pyautogui.click(match3_match_betting_x, match3_match_betting_y)
    time.sleep(1)
    pyautogui.click(top_price_cell_x, top_price_cell_y)
    time.sleep(1)

    # display betting for match #3 in window, update match list window
    move_to_next_match()
    time.sleep(1)
    
    # enter betting for match #3
    enter_match_betting_then_2p5_goals_down_to_4p5_goals_markets()

    return
# ====================================================================================================
# Enter nine matches
# ====================================================================================================
def enter_nine_matches():

    global current_match_index

    scroll_down_x = test_cell_x
    scroll_down_y = test_cell_y

    # test print
    print('scroll_down_x =', scroll_down_x)
    print('scroll_down_y =', scroll_down_y)

    # do matches 1 to 3
    enter_three_matches()
    # scroll down
    time.sleep(1)
    pyautogui.click(scroll_down_x, scroll_down_y)
    time.sleep(1)
    # click match betting
    pyautogui.click(match1_match_betting_x, match1_match_betting_y)
    time.sleep(1)
    # click top price cell
    pyautogui.click(top_price_cell_x, top_price_cell_y)
    time.sleep(1)
    # increment match at end to keep on correct betting
    if current_match_index == len(football_betting) - 1:
        current_match_index = 0
    else:
        current_match_index += 1

    # do matches 4 to 6
    enter_three_matches()
    # scroll down
    time.sleep(1)
    pyautogui.click(scroll_down_x, scroll_down_y)
    time.sleep(1)
    # click match betting
    pyautogui.click(match1_match_betting_x, match1_match_betting_y)
    time.sleep(1)
    # click top price cell
    pyautogui.click(top_price_cell_x, top_price_cell_y)
    time.sleep(1)
    # increment match at end to keep on correct betting
    if current_match_index == len(football_betting) - 1:
        current_match_index = 0
    else:
        current_match_index += 1

    # do matches 7 to 9
    enter_three_matches()
    # increment match at end to keep on correct betting
    if current_match_index == len(football_betting) - 1:
        current_match_index = 0
    else:
        current_match_index += 1

    return
# ====================================================================================================
# Set up the interface
# Basic window
root = Tk()
root.wm_title("FuBball Meister (Amelyn Technologies 2017)")

# Create forward_backward_frame to hold forward and backward buttons and
# "read football webpage" button
forward_backward_frame = ttk.Frame(root)

# Previous and Next Match buttons ('<' and '>')
previous_match_button = ttk.Button(forward_backward_frame, text='<', width=3,
                                            command=move_to_previous_match)
previous_match_button.grid(row=0, column=0, sticky=W)
next_match_button = ttk.Button(forward_backward_frame, text='>', width=3,
                                            command=move_to_next_match)
next_match_button.grid(row=0, column=1, sticky=W)

# Set up read football webpage button
read_football_webpage_button = ttk.Button(forward_backward_frame, text='Read Football Webpage',
                                            command=read_football_webpage)
read_football_webpage_button.grid(row=0, column=2, sticky=W)

# set up the Settings button
settings_button = ttk.Button(forward_backward_frame, text='Settings',
                                            command=show_clickable_settings_window)
settings_button.grid(row=0, column=3, sticky=W)

# grid the forward_backward_frame into root
forward_backward_frame.grid(row=0, column=0, sticky=W)

# Set up Text widget to display the current match
match_display_text_box = Text(root, width=45, height=21, background='#000000',
                              foreground='#FFFF00', font=('Courier', 12, 'bold')) # changed!!!!!!!
match_display_text_box.grid(row=1, column=0, sticky=W)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create new window containing 13 buttons, one for each market (including halftime/fulltime and
# correct scores); each button will enter the betting for a market
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
market_button_window = Toplevel(root)
market_button_window.wm_title("Enter Betting")

# frame to hold the eleven market buttons
market_button_frame = ttk.Frame(market_button_window)

# Enter betting label
enter_betting_label = Label(market_button_frame, text="", width="16", height="1")
enter_betting_label.grid(row=0, column=0, sticky=W)

# match betting button
match_betting_button = ttk.Button(market_button_frame, text='Match Betting', width=16,
                                            command=enter_match_betting)
match_betting_button.grid(row=1, column=0, sticky=W)
# NEW (25/9/17):
# button for entering all markets from match betting downwards; goes to the right of
# the match betting button
the_match_betting_onwards_button = ttk.Button(market_button_frame, text='V', width=2,
                    command=enter_match_betting_then_2p5_goals_down_to_4p5_goals_markets)
the_match_betting_onwards_button.grid(row=1, column=1, sticky=W)

# NEW (15/3/18):
# button for entering all the betting for 3 matches in a row
# yep, we're going to enter three matches at the click of a button(!)
enter_three_matches_button = ttk.Button(market_button_frame, text='3', width=2,
                    command=enter_three_matches)
enter_three_matches_button.grid(row=1, column=2, sticky=W)

#NEW (24/4/18)
# button for entering 9 matches in a row
enter_nine_matches_button = ttk.Button(market_button_frame, text='9', width=2,
                    command=enter_nine_matches)
enter_nine_matches_button.grid(row=2, column=2, sticky=W)

# handicap betting button
handicap_betting_button = ttk.Button(market_button_frame, text='Handicap Betting', width=16,
                                            command=enter_handicap_betting)
handicap_betting_button.grid(row=2, column=0, sticky=W)

# spacer label #1
spacer_label_1 = Label(market_button_frame, text="", width="16", height="1")
spacer_label_1.grid(row=5, column=0, sticky=W)

# 2.5 goals betting button
two_p5_goals_button = ttk.Button(market_button_frame, text='2.5 Goals', width=16,
                                            command=enter_2p5_goals_betting)
two_p5_goals_button.grid(row=6, column=0, sticky=W)

# NEW (29/8/17):
# "start here" button beside the 2.5 goals betting button
from_two_p5_goals_onwards_button = ttk.Button(market_button_frame, text='V', width=2,
                                            command=enter_2p5_goals_betting_onwards)
from_two_p5_goals_onwards_button.grid(row=6, column=1, sticky=W)

# new goal rush betting button
new_goal_rush_button = ttk.Button(market_button_frame, text='New Goal Rush', width=16,
                                            command=enter_new_goal_rush_betting)
new_goal_rush_button.grid(row=7, column=0, sticky=W)
# goal rush plus betting button
goal_rush_plus_button = ttk.Button(market_button_frame, text='Goal Rush Plus', width=16,
                                            command=enter_goal_rush_plus_betting)
goal_rush_plus_button.grid(row=8, column=0, sticky=W)
# win to nil betting button
win_to_nil_button = ttk.Button(market_button_frame, text='Win To Nil', width=16,
                                            command=enter_win_to_nil_betting)
win_to_nil_button.grid(row=9, column=0, sticky=W)
# over two goals plus betting button
over_two_goals_plus_button = ttk.Button(market_button_frame, text='Over Two Goals Plus', width=16,
                                            command=enter_over_two_goals_plus_betting)
over_two_goals_plus_button.grid(row=10, column=0, sticky=W)
# spacer label #2
spacer_label_2 = Label(market_button_frame, text="", width="16", height="1")
spacer_label_2.grid(row=11, column=0, sticky=W)
# WTN-ET betting button
wtn_et_button = ttk.Button(market_button_frame, text='WTN-ET', width=16,
                                            command=enter_wtn_et_betting)
wtn_et_button.grid(row=12, column=0, sticky=W)
# goals_1p5 betting button
goals_1p5_button = ttk.Button(market_button_frame, text='1.5 Goals', width=16,
                                            command=enter_1p5_goals_betting)
goals_1p5_button.grid(row=13, column=0, sticky=W)
# goals_3p5 betting button
goals_3p5_button = ttk.Button(market_button_frame, text='3.5 Goals', width=16,
                                            command=enter_3p5_goals_betting)
goals_3p5_button.grid(row=14, column=0, sticky=W)
# goals_4p5 betting button
goals_4p5_button = ttk.Button(market_button_frame, text='4.5 Goals', width=16,
                                            command=enter_4p5_goals_betting)
goals_4p5_button.grid(row=15, column=0, sticky=W)
# spacer label #3
# spacer_label_3 = Label(market_button_frame, text="", width="16", height="1")
# spacer_label_3.grid(row=16, column=0, sticky=W)

# enter 2.5 Goals down to 4.5 Goals button (9 markets in total)
# last_three_markets_text = "Match Betting\nthen\n2.5 Goals\ndown to\n4.5 Goals\n(last 9\nmarkets)"
# last_three_markets_button = ttk.Button(market_button_frame, text=last_three_markets_text, width=16,
#             command=enter_match_betting_then_2p5_goals_down_to_4p5_goals_markets)
# last_three_markets_button.grid(row=17, column=0, sticky=W)

# spacer label #4
spacer_label_4 = Label(market_button_frame, text="", width="16", height="1")
spacer_label_4.grid(row=18, column=0, sticky=W)
# Checkbutton for optionally entering handicap betting
hcap_checkbutton_value = IntVar()
enter_hcap_betting_checkbutton = Checkbutton(market_button_frame, text="Enter H'cap", variable=hcap_checkbutton_value)
enter_hcap_betting_checkbutton.grid(row=19, column=0, sticky=W)
# Checkbutton for optionally regenerating correct scores
cscores_checkbutton_value = IntVar()
cscores_checkbutton = Checkbutton(market_button_frame, text="Enter c'scores", variable=cscores_checkbutton_value)
cscores_checkbutton.grid(row=20, column=0, sticky=W)
# Checkbutton for optionally regenerating half-time/full-time prices
htft_checkbutton_value = IntVar()
htft_checkbutton = Checkbutton(market_button_frame, text="Enter HT/FT", variable=htft_checkbutton_value)
htft_checkbutton.grid(row=21, column=0, sticky=W)

# grid the market_button_frame into market_button_window
market_button_frame.grid(row=0, column=0, sticky=W)

read_football_webpage()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# build a new window; it's going to hold the full match list, with the current match highlighted
# football_betting[current_line_no]
#
# Each line will be in the following format:
# <match no> <home team> v <away team>
# For example:
# 001 Man Utd v Chelsea
# 002 Wigan v Southend
# 003 Dumbarton v Eastleigh
# etc.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# First, work out max line width for the match list window. This will be used to set the width
# of the match list window
match_list_max_line_width = calculate_match_list_max_line_width() + 1

match_list_window = Toplevel()
match_list_window.wm_title("Match List")

# frame to hold the list of matches
match_list_frame = ttk.Frame(match_list_window)

# grid text widget and frame
match_list_text_widget = Text(match_list_frame, background="black", foreground="yellow",
                                width=match_list_max_line_width, height=45)
match_list_text_widget.grid(row=0, column=0, sticky=W)
match_list_frame.grid(row=0, column=0, sticky=W)

update_match_list_window()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Start 'er up!
root.mainloop()
