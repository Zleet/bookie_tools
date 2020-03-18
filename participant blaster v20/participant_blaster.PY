# ====================================================================================================
# Participant Blaster
#
# A program that finds participants in the mcleans system and enters them, one by one.
# Also types participants into blank cells.
#
# Requires Python 3 and the pyautogui GUI automation library to be installed on the computer
#
# Written by Michael McLarnon (bigbadmick2000@hotmail.com) 28/10/16
# ====================================================================================================
# Thursday 27th October 2016 - Stuff To Add:
# 1. A status text line that displays:
#    1. the participant currently being entered
#    2. what number the current participant is in the list of participants (e.g. 15/28 or 3/7 etc.)
#    3. Percentage of participants that have been successfully entered, to a single decimal place
#       (e.g. 53.2%)
#    *** DONE ***
# 2. A Letter Delay text entry box for the user to enter the delay (in seconds) between the program
#    typing successive letters
#    *** DONE ***
# 3. Scroll bar for the big text space that holds the list of participants
#    *** DONE ***
# 4. Highlight the participant being currently entered in the big list of participants
#
# 5. Ensure that the big list of participants scrolls down to always keep the participant being
#    currently entered in view
#
# ====================================================================================================
# imports
import pyautogui, time
from tkinter import *
from tkinter import ttk
# ====================================================================================================
# global variables
current_line_no = 0 # keep a record of the current line index (from zero upwards)

# coordinate information for:
# (1) the save button
# (2) the plus at the top left of the grid area where participants and prices are displayed
#     in the McLeans system
# (3) the input line where you search for participants in the McLeans computer system
# (4) the Q button on the top left of the onscreen accessibility keyboard
# (5) the NEXT MARKET button
save_x = -1
save_y = -1
plus_x = -1
plus_y = -1
input_x = -1
input_y = -1
keyboard_q_x = -1
keyboard_q_y = -1
next_market_x = -1
next_market_y = -1
letter_delay = 0.2

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

    # read and set the values of the global variables:
    # keyboard_q_x (the x coordinate of the q key on the onscreen keyboard)
    # keyboard_q_y (the y coordinate of the q key on the onscreen keyboard)
    keyboard_q_x = keyboard_q_key_x_text_box.get("1.0", END)
    keyboard_q_x = int(keyboard_q_x.strip())
    print('keyboard_q_x =', keyboard_q_x)

    keyboard_q_y = keyboard_q_key_y_text_box.get("1.0", END)
    keyboard_q_y = int(keyboard_q_y.strip())
    print('keyboard_q_y =', keyboard_q_y)

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
    global next_market_x
    global next_market_y

    # next_market_x_text_box

    save_x = save_x_text_box.get("1.0", END)
    save_x = int(save_x.strip())
    print('save_x =', save_x)
    save_y = save_y_text_box.get("1.0", END)
    save_y = int(save_y.strip())
    print('save_y =', save_y)

    plus_x = plus_x_text_box.get("1.0", END)
    plus_x = int(plus_x.strip())
    print('plus_x =', plus_x)

    plus_y = plus_y_text_box.get("1.0", END)
    plus_y = int(plus_y.strip())
    print('plus_y =', plus_y)

    input_x = input_x_text_box.get("1.0", END)
    input_x = int(input_x.strip())
    print('input_x =', input_x)

    input_y = input_y_text_box.get("1.0", END)
    input_y = int(input_y.strip())
    print('input_y =', input_y)

    keyboard_q_x = keyboard_q_key_x_text_box.get("1.0", END)
    keyboard_q_x = int(keyboard_q_x.strip())
    print('keyboard_q_x =', keyboard_q_x)

    keyboard_q_y = keyboard_q_key_y_text_box.get("1.0", END)
    keyboard_q_y = int(keyboard_q_y.strip())
    print('keyboard_q_y =', keyboard_q_y)

    next_market_x = next_market_x_text_box.get("1.0", END)
    next_market_x = int(next_market_x.strip())
    print('next_market_x =', next_market_x)

    next_market_y = next_market_y_text_box.get("1.0", END)
    next_market_y = int(next_market_y.strip())
    print('next_market_y =', next_market_y)

    letter_delay = letter_delay_text_box.get("1.0", END)
    letter_delay = float(letter_delay.strip())
    print('letter_delay =', letter_delay)

    return
# ====================================================================================================
# Type text by using pyautogui to click on the windows accessibility onscreen
# keyboard. In between each character, pause pause_between_letters seconds
def kb_type(text):

    if dont_type_to_one and (text[-2:] == '/1'):
        text = text[:-2]

    for character in text:
        if character.upper() in keys.keys():
            x = keys[character.upper()]["x"]
            y = keys[character.upper()]["y"]
            # if uppercase character, press shift first
            if (character.upper() == character) and character.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                kb_press("shift")
            pyautogui.click(x, y)
            time.sleep(letter_delay)

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
# Loop through the lines in csv_data_text_box
# Swop first and last names along commas
# e.g. Change "Woods,Tiger" to "Tiger,Woods" etc.
# ====================================================================================================
def swop_names_along_commas():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the participants from the csv_data_text_box
    text = csv_data_text_box.get("1.0", END)

    # test print
    print(text)

    text = text.strip()
    lines = text.split("\n")

    swopped_lines = []
    for line in lines:
        line = line.strip()
        if ',' in line:
            comma_loc = line.find(',')
            first_bit = line[:comma_loc].strip()
            second_bit = line[comma_loc + 1:].strip()
            rebuilt_line = second_bit + ', ' + first_bit
            rebuilt_line = rebuilt_line.strip()
            swopped_lines.append(rebuilt_line)
    lines = swopped_lines

    new_text = "\n".join(lines)

    # delete old text, insert new text
    csv_data_text_box.delete(1.0, END)
    csv_data_text_box.insert(END, new_text)

    return
# ====================================================================================================
# Loop through participants. For each participant, search for it in the participant search area in
# the mcleans system, then press down, then enter to enter it. After processing all participants,
# press the save button in the mcleans system.
# ====================================================================================================
def find_and_enter_participants():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the participants from the csv_data_text_box
    text = csv_data_text_box.get("1.0", END)
    text = text.strip()
    lines = text.split("\n")

    # click on the participant search box
    pyautogui.click(input_x, input_y)
    time.sleep(5)

    # 1. Loop through participants. For each:
    #    1. Type the name into the participant search box
    #    2. Press down
    #    3. Press enter
    # 2. Finally, click the save button
    total_participants = len(lines)
    for count in range(total_participants):
        line = lines[count]
        line = line.strip()
        kb_type(line)
        time.sleep(0.2)
        kb_press('down')
        time.sleep(0.2)
        kb_press('enter')
        time.sleep(0.2)
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Copy some text to the windows clipboard so that's it's ready to paste later, using:
# kb_press('control')
# kb_type('v')
# ====================================================================================================
def copy_text_to_windows_clipboard(text):

    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

    return
# ====================================================================================================
# Click the top left blank cell, then loop through participants.
# For each participant, type it in, then press down.
# If we're at the final participant, press up instead of down after typing it in.
# Then press the save button. Job done.
# ====================================================================================================
def type_participants_in():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the participants from the csv_data_text_box
    text = csv_data_text_box.get("1.0", END)
    text = text.strip()
    lines = text.split("\n")

    # click on the top left empty cell, which is located at
    # (plus_x + 32, plus_y + 18)
    # pyautogui.click(plus_x + 32, plus_y + 18)

    # type a bunch of test lines to get the focus on the target window
    type_test_lines() # NEW 6/2/17 AT 19:06

    # 1. Loop through participants; for each:
    #     1. Type the participant name
    #     2. If we're NOT at the last participant, press down, else press up
    # 2. Finally, click the save button
    total_participants = len(lines)
    for count in range(total_participants):
        line = lines[count]
        line = line.strip()
        # build the status text for the two line status Text widget
        # It will be in the form:
        # Woods, Tiger
        # 15/23 - 63.2% complete
        status_text = line + "\n" + str(count + 1) + '/' + str(total_participants) + ' - '
        if count + 1 < total_participants:
            percentage = float(count) / (float(total_participants) / 100.0)
            percentage = str(round(percentage, 1))
        else:
            percentage = "100"
        status_text += percentage + "%"
        # set text in status_text_box to status_text
        status_text_box.delete('1.0', END)
        status_text_box.insert('1.0', status_text)
        kb_type(line)
        root.update_idletasks()
        if count + 1 != total_participants:
            kb_press('down')
        else:
            kb_press('up')
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Type a bunch of test lines; used to get the focus onto the remote desktop window as there is
# sometimes a delay before the remote window reacts to actions initiated by the pyautogui library
# ====================================================================================================
def type_test_lines():

    direction = 0
    for count in range(4):
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
# Parse the data the user enters and get the forecast info.
# Type the forecast strings and prices into blank cells.
# First, type the names in, going down.
# Then move across and type the prices in going up.
# Then click save.
# ====================================================================================================
def enter_first_goal_forecasts_and_prices():

    # get the wincast strings and prices information
    forecast_information = extract_forecast_information()

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # type a bunch of test lines to get the focus on the target window
    type_test_lines() # NEW 6/2/17 AT 19:06

    # Loop through forecast objects and type the forecast strings in
    for count in range(len(forecast_information)):
        forecast_object = forecast_information[count]
        kb_type(forecast_object["fc_string"])
        if (count < (len(forecast_information) - 1)):
            kb_press('down')
    # move right to the bottom of the price column
    for count in range(3):
        kb_press('right')
    # loop through forecast objects backwards and type the forecast prices in going up the column
    # from bottom to top
    
    for count in range(len(forecast_information) - 1, -1, -1):
        forecast_object = forecast_information[count]
        kb_type(forecast_object['first_goal_fc_price_string'])
        if count > 0:
            kb_press('up')
        else:
            kb_press('down')
    # click save
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Enter anytime forecast strings and prices
# ====================================================================================================
def enter_anytime_forecasts_and_prices():

    # get the wincast strings and prices information
    forecast_information = extract_forecast_information()

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # type a bunch of test lines to get the focus on the target window
    type_test_lines()

    # Loop through forecast objects and type the forecast strings in
    for count in range(len(forecast_information)):
        forecast_object = forecast_information[count]
        kb_type(forecast_object["fc_string"])
        if (count < (len(forecast_information) - 1)):
            kb_press('down')
    # move right to the bottom of the price column
    for count in range(3):
        kb_press('right')
    # loop through forecast objects backwards and type the anytime forecast prices in going up the
    # column from bottom to top
    for count in range(len(forecast_information) - 1, -1, -1):
        forecast_object = forecast_information[count]
        kb_type(forecast_object['anytime_fc_price_string'])
        if count > 0:
            kb_press('up')
        else:
            kb_press('down')
    # click save
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Helper function for enter_first_goal_forecasts_and_prices()
# Build a list of forecast objects and append them to a container list named forecast_information
# Each forecast object will be in the form:
# {
#   "fc_string"                     : "A.Cornelius/Atalanta",
#   "first_goal_fc_price_string"    : "28/1",
#   "anytime_fc_price_string"       : "19/2"
# }
# ====================================================================================================
def extract_forecast_information():

    forecast_information = []

    # get text from csv_data_text_box
    text = csv_data_text_box.get("1.0", END)
    text = text.strip()
    lines = text.split("\n")

    # find start of forecast lines
    first_forecast_line_index = -1
    for count in range(len(lines)):
        line = lines[count].strip()
        if line == '=== WINCASTS ===':
            first_forecast_line_index = count + 1
            break

    # get forecast lines
    forecast_lines = []
    for count in range(first_forecast_line_index, len(lines)):
        line = lines[count]
        forecast_lines.append(line)

    # process forecast lines; for each line, create a forecast object and append it to
    # forecast_information
    for line in forecast_lines:
        line = line.strip()
        elements = line.split(',')
        forecast_object = {
                "fc_string"                     : elements[0].strip(),
                "first_goal_fc_price_string"    : elements[1].strip(),
                "anytime_fc_price_string"       : elements[2].strip()
                            }
        forecast_information.append(forecast_object)
    
    return forecast_information
# ====================================================================================================
# Extract the scorer information from csv data. For each scorer, build a dictionary in the form:
# {
#   "home_or_away"              : "h",
#   "team_name"                 : "Venezuela",
#   "first_name"                : "Rondon",
#   "last_name"                 : "Salomon",
#   "first_scorer_price"        : "11/2",
#   "anytime_scorer_price"      : "13/8"
#   "first_goal_wincast_price"  : "20/1",
#   "anytime_wincast_price"     : "13/2",
#   "brace_price"               : "5/1",
#   "hat_trick_price"           : "8/1"
# }
# Append all the scorer objects onto a list named scorer_information and return it.
# ====================================================================================================
def extract_scorer_information_from_csv_data(text=''):

    scorer_information = []

    # get lines from csv_data_text_box if the text hasn't been passed as a parameter to the function
    if text == '':
        text = csv_data_text_box.get("1.0", END)
        text = text.strip()

    lines = text.split("\n")

    # get home scorer lines
    team_name_line_index = -1
    for count in range(len(lines)):
        line = lines[count]
        if '=== HOME TEAM ===' in line:
            team_name_line_index = count
            break

    # get away scorer lines
    # find index of first home scorer line, first away scorer line and the line that terminates
    # the away scorers (wincasts_header_line_index)
    home_scorer_header_line_index = -1
    away_scorer_header_line_index = -1
    wincasts_header_line_index = -1
    for count in range(len(lines)):
        line = lines[count]
        if line[:17] == '=== HOME TEAM ===':
            home_scorer_header_line_index = count
        if line[:17] == '=== AWAY TEAM ===':
            away_scorer_header_line_index = count
        if line[:16] == '=== WINCASTS ===':
            wincasts_header_line_index = count
            break

    # get home team name
    home_team_name = lines[home_scorer_header_line_index + 1].replace('team name,', '').strip()

    # process home scorer lines
    for count in range(home_scorer_header_line_index + 2, away_scorer_header_line_index - 1):
        line = lines[count].strip()
        elements = line.split(',')
        first_name = elements[0].strip()
        last_name = elements[1].strip()
        first_scorer_price = elements[2].strip()
        anytime_scorer_price = elements[3].strip()
        first_goal_wincast_price = elements[4].strip()
        anytime_wincast_price = elements[5].strip()
        brace_price = ''
        if len(elements) >= 7:
            brace_price = elements[6].strip()
        hat_trick_price = ''
        if len(elements) >= 8:
            hat_trick_price = elements[7].strip()
        # build scorer dictionary, append it to scorer_information
        scorer_dictionary = {
                    "home_or_away"              : "h",
                    "team_name"                 : home_team_name,
                    "first_name"                : first_name,
                    "last_name"                 : last_name,
                    "first_scorer_price"        : first_scorer_price,
                    "anytime_scorer_price"      : anytime_scorer_price,
                    "first_goal_wincast_price"  : first_goal_wincast_price,
                    "anytime_wincast_price"     : anytime_wincast_price,
                    "brace_price"               : brace_price,
                    "hat_trick_price"           : hat_trick_price
                            }
        scorer_information.append(scorer_dictionary)

    # get away team name
    away_team_name = lines[away_scorer_header_line_index + 1].replace('team name,', '').strip()

    # process away scorer lines
    for count in range(away_scorer_header_line_index + 2, wincasts_header_line_index - 1):
        line = lines[count].strip()
        elements = line.split(',')
        first_name = elements[0].strip()
        last_name = elements[1].strip()
        first_scorer_price = elements[2].strip()
        anytime_scorer_price = elements[3].strip()
        first_goal_wincast_price = elements[4].strip()
        anytime_wincast_price = elements[5].strip()
        brace_price = ''
        if len(elements) >= 7:
            brace_price = elements[6].strip()
        hat_trick_price = ''
        if len(elements) >= 8:
            hat_trick_price = elements[7].strip()
        # build scorer dictionary, append it to scorer_information
        scorer_dictionary = {
                    "home_or_away"              : "a",
                    "team_name"                 : away_team_name,
                    "first_name"                : first_name,
                    "last_name"                 : last_name,
                    "first_scorer_price"        : first_scorer_price,
                    "anytime_scorer_price"      : anytime_scorer_price,
                    "first_goal_wincast_price"  : first_goal_wincast_price,
                    "anytime_wincast_price"     : anytime_wincast_price,
                    "brace_price"               : brace_price,
                    "hat_trick_price"           : hat_trick_price
                            }
        scorer_information.append(scorer_dictionary)

    return scorer_information
# ====================================================================================================
# In the ALL tab, enter all players and prices for both home and away teams.
# ====================================================================================================
def enter_first_scorer_all_names_and_prices():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get all data, extract home_player_names, away_player_names, home_first_scorer_prices
    # and away_first_scorer_prices
    all_data = get_scorer_names_and_scorer_prices()

    home_player_names = all_data["home_players"]
    away_player_names = all_data["away_players"]
    home_first_scorer_prices = all_data["home_1st_scorer_prices"]
    away_first_scorer_prices = all_data["away_1st_scorer_prices"]

    # click on the participant search box
    pyautogui.click(input_x, input_y)
    time.sleep(5)

    # build big list of all home and away names, with "Own, Goal" as the first item
    big_list_of_names = ["Own, Goal"]
    big_list_of_names.extend(home_player_names)
    big_list_of_names.extend(away_player_names)

    # build big list of prices
    big_list_of_prices = ["20/1"]
    big_list_of_prices.extend(home_first_scorer_prices)
    big_list_of_prices.extend(away_first_scorer_prices)

    # 1. Loop through big list of names. For each:
    #    1. Swop the name along the comma
    #    2. Type the name into the participant search box
    #    3. Press down
    #    4. Press enter
    # 2. Finally, click the save button
    total_participants = len(big_list_of_names)
    for count in range(total_participants):
        player_name = big_list_of_names[count]
        player_name = player_name.strip()
        # swop name along comma
        player_name = swop_name_along_comma(player_name)
        kb_type(player_name)
        time.sleep(0.2)
        kb_press('down')
        time.sleep(0.2)
        kb_press('enter')
        time.sleep(0.2)
    pyautogui.click(save_x, save_y)

    # Enter all the prices
    # click top left cell
    time.sleep(1)
    pyautogui.click(plus_x + 17, plus_y + 14)
    time.sleep(0.2)
    # press right four times
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    # press down
    kb_press('down')
    time.sleep(0.2)
    # type prices
    for count in range(len(big_list_of_prices)):
        price_string = big_list_of_prices[count]
        if price_string == "":
            kb_type("n")
        else:
            kb_type(price_string)
        time.sleep(0.03)
        if count < (len(big_list_of_prices) - 1):
            kb_press('down')
        else:
            kb_press('up')
        time.sleep(0.2)
    # click save button
    pyautogui.click(save_x, save_y)    
    time.sleep(1)

    # enter all the 'D', 'H' and 'A' for (1) no goal, (2) home players, and (3) away players
    # click top left cell
    pyautogui.click(plus_x + 17, plus_y + 14)
    time.sleep(0.2)
    # press right twice
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    # type 'D' for the 'No Goalscorer' row
    kb_type('D')
    time.sleep(0.2)
    kb_press('enter')
    time.sleep(0.2)
    # press down
    kb_press('down')
    time.sleep(0.2)
    # type a 'H' for "Own, Goal" plus each home player
    for count in range(len(home_player_names) + 1):
        kb_type('H')
        time.sleep(0.2)
        kb_press('down')
        time.sleep(0.2)
    # type a 'A' for each away player
    for count in range(len(away_player_names)):
        kb_type('A')
        time.sleep(0.2)
        if count < (len(away_player_names) - 1):
            kb_press('down')
        else:
            kb_press('up')
        time.sleep(0.2)
    # click save button
    pyautogui.click(save_x, save_y)    
    time.sleep(1)

    return
# ====================================================================================================
# In the ALL tab, enter all the prices for "Own Goal" and all home and away players
# ====================================================================================================
def enter_all_anytime_scorer_prices():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get all data, home_first_scorer_prices and away_first_scorer_prices
    all_data = get_scorer_names_and_scorer_prices()
    home_anytime_scorer_prices = all_data["home_anytime_scorer_prices"]
    away_anytime_scorer_prices = all_data["away_anytime_scorer_prices"]

    # build big list of prices with "11/2" for anytime own goal, then home anytime scorer prices,
    # then away anytime scorer prices
    big_list_of_prices = ["11/2"]
    big_list_of_prices.extend(home_anytime_scorer_prices)
    big_list_of_prices.extend(away_anytime_scorer_prices)

    # Enter all the prices
    # click top left cell
    time.sleep(1)
    pyautogui.click(plus_x + 17, plus_y + 14)
    time.sleep(0.2)
    # press right four times
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    kb_press('right')
    time.sleep(0.2)
    # press down
    kb_press('down')
    time.sleep(0.2)
    # type prices
    for count in range(len(big_list_of_prices)):
        price_string = big_list_of_prices[count]
        if price_string == "":
            kb_type("n")
        else:
            kb_type(price_string)
        time.sleep(0.03)
        if count < (len(big_list_of_prices) - 1):
            kb_press('down')
        else:
            kb_press('up')
        time.sleep(0.2)
    # click save button
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Get home_names, away_names, home_1st_scorer_prices, away_1st_scorer_prices,
# home_anytime_scorer_prices and away_anytime_scorer_prices from the big text data block
# the user has pasted into the csv_data_text_box
# ====================================================================================================
def get_scorer_names_and_scorer_prices():

    # get the big block of text data from the csv_data_text_box
    text_data = csv_data_text_box.get("1.0", END)
    lines = text_data.split("\n")

    # first, get the home and away players
    # loop through lines and find the first two lines that contain the string "PLAYERS:"
    # also find the index of the line that contains the substring "WINCAST STRINGS" as this will
    # indicate the end of the away player names
    indices_of_players_lines = []
    index_of_wincast_header_line = -1
    for count in range(len(lines)):
        line = lines[count].strip()
        if "PLAYERS:" in line:
            indices_of_players_lines.append(count)
        if "WINCAST STRINGS" in line:
            index_of_wincast_header_line = count

    # get home and away player names
    home_players = []
    away_players = []
    first_player_header_index = indices_of_players_lines[0]
    second_player_header_index = indices_of_players_lines[1]
    for line_no in range(first_player_header_index, index_of_wincast_header_line):
        current_line = lines[line_no].strip()
        # check for home player
        if ((line_no > first_player_header_index) and (line_no < second_player_header_index)):
            if len(current_line) > 0:
                home_players.append(current_line)
        # check for away player
        if ((line_no > second_player_header_index) and (line_no < index_of_wincast_header_line)):
            if len(current_line) > 0:
                away_players.append(current_line)

    # loop through lines and get the indices of the lines containing:
    # 1. the string "=== HOME TEAM ===" at the top of the home team csv data lines
    # 2. the string "=== AWAY TEAM ===" at the top of the away team csv data lines
    # 3. the string "=== WINCASTS ===" at the end of the away team csv data lines
    home_team_header_index = -1
    away_team_header_index = -1
    wincast_header_index = -1
    for line_no in range(len(lines)):
        line = lines[line_no].strip()
        if line == "=== HOME TEAM ===":
            home_team_header_index = line_no
        if line == "=== AWAY TEAM ===":
            away_team_header_index = line_no
        if line == "=== WINCASTS ===":
            wincast_header_index = line_no

    # get home_csv_lines
    home_csv_lines = []
    for line_no in range(home_team_header_index + 2, away_team_header_index):
        line = lines[line_no].strip()
        if len(line) > 0:
            home_csv_lines.append(line)
        
    # get away_csv_lines
    away_csv_lines = []
    for line_no in range(away_team_header_index + 2, wincast_header_index):
        line = lines[line_no].strip()
        if len(line) > 0:
            away_csv_lines.append(line)

    # loop through home_csv_lines and build home_1st_scorer_prices
    # and home_anytime_scorer_prices
    home_1st_scorer_prices = []
    home_anytime_scorer_prices = []
    for line in home_csv_lines:
        line = line.strip()
        elements = line.split(',')
        index_of_last_element = len(elements) - 1
        # get 1st scorer price
        first_scorer_price = elements[2] # changed
        home_1st_scorer_prices.append(first_scorer_price)
        # get anytime scorer price
        anytime_scorer_price = elements[3] # changed
        home_anytime_scorer_prices.append(anytime_scorer_price)
    # remove trailing empty strings from home_1st_scorer_prices
    # and home_anytime_scorer_prices
    while home_1st_scorer_prices[-1] == '':
        home_1st_scorer_prices.pop()
    while home_anytime_scorer_prices[-1] == '':
        home_anytime_scorer_prices.pop()

    # loop through away_csv_lines and build away_1st_scorer_prices
    # and away_anytime_scorer_prices
    away_1st_scorer_prices = []
    away_anytime_scorer_prices = []
    for line in away_csv_lines:
        line = line.strip()
        elements = line.split(',')
        index_of_last_element = len(elements) - 1
        # get 1st scorer price
        first_scorer_price = elements[2] # changed
        away_1st_scorer_prices.append(first_scorer_price)
        # get anytime scorer price
        anytime_scorer_price = elements[3] # changed
        away_anytime_scorer_prices.append(anytime_scorer_price)
    # remove trailing empty strings from away_1st_scorer_prices
    # and away_anytime_scorer_prices
    while away_1st_scorer_prices[-1] == '':
        away_1st_scorer_prices.pop()
    while away_anytime_scorer_prices[-1] == '':
        away_anytime_scorer_prices.pop()

    # build a dictionary to hold all the data we're returning
    names_and_prices = {
            "home_players"                  : home_players,
            "away_players"                  : away_players,
            "home_1st_scorer_prices"        : home_1st_scorer_prices,
            "away_1st_scorer_prices"        : away_1st_scorer_prices,
            "home_anytime_scorer_prices"    : home_anytime_scorer_prices,
            "away_anytime_scorer_prices"    : away_anytime_scorer_prices
                    }

    return names_and_prices
# ====================================================================================================
# If a name contains a comma, swop the names sections around the comma
# e.g. "Tiger,Woods" will become "Woods,Tiger"
# ====================================================================================================
def swop_name_along_comma(name):

    if ',' in name:
        comma_loc = name.find(',')
        first_bit = name[:comma_loc].strip()
        second_bit = name[comma_loc + 1:].strip()
        rebuilt_name = second_bit + ', ' + first_bit
        rebuilt_name = rebuilt_name.strip()

    return rebuilt_name
# ====================================================================================================
# Enter names and betting for both wincast markets.
# This function assumes that the focus is already on the top left cell of the
# "first goal wincast cell"
# ====================================================================================================
def enter_both_wincast_markets():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the wincast strings and prices information
    forecast_information = extract_forecast_information()

    total_wincasts = len(forecast_information)

    # press up and down a few times to get focus on the window
    for count in range(5):
        kb_press('down')
        time.sleep(0.2)
        kb_press('up')
        time.sleep(0.2)
        kb_press('up')
        time.sleep(0.2)

    # There are usually 6 blank lines already built into the "first scorer wincasts" market.
    # So we will need to add (total_wincasts - 6) more lines.
    # Add another two to ensure we get enough lines to hold all the wincasts (these can be
    # deleted by hand by the user after this program enters all the wincasts)
    for count in range(total_wincasts - 4):
        pyautogui.click(plus_x, plus_y)
        time.sleep(0.5)
    # move down eight times to get to the bottom cell
    for count in range(8):
        time.sleep(0.2)
        kb_press('down')
    # type total_wincasts + 2 dots into the blank cells, from bottom to top
    for count in range(total_wincasts + 2):
        time.sleep(0.2)
        kb_type('.')
        time.sleep(0.2)
        if count < (total_wincasts + 1):
            kb_press('up')
        else:
            kb_press('down')
    time.sleep(0.5)
    # click the save button
    pyautogui.click(save_x, save_y)
    time.sleep(1)

    # click the top left cell
    pyautogui.click(plus_x + 17, plus_y + 14)
    time.sleep(1)

    enter_first_goal_forecasts_and_prices()

    # move to next market
    time.sleep(1)
    pyautogui.click(next_market_x, next_market_y)
    time.sleep(1)

    # the anytime forecast market usually contains zero lines, so we need to add
    # total_wincasts lines
    # Add another two for good measure.
    for count in range(total_wincasts + 2):
        pyautogui.click(plus_x, plus_y)
        time.sleep(0.5)
    # move down eight times to get to the bottom cell
    for count in range(8):
        time.sleep(0.2)
        kb_press('down')
    # type total_wincasts + 2 dots into the blank cells, from bottom to top
    for count in range(total_wincasts + 2):
        time.sleep(0.2)
        kb_type('.')
        time.sleep(0.2)
        if count < (total_wincasts + 1):
            kb_press('up')
        else:
            kb_press('down')
    time.sleep(0.5)
    # click the save button
    pyautogui.click(save_x, save_y)
    time.sleep(1)

    # click the top left cell
    pyautogui.click(plus_x + 17, plus_y + 14)
    time.sleep(1)

    enter_anytime_forecasts_and_prices()

    return
# ====================================================================================================
# Copy the text in the paste_all_football_data_text_box in the football_match_data_window to the
# csv_data_text_box in the main window
# ====================================================================================================
def put_all_data_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', text)

    return
# ====================================================================================================
# Extract the home scorer names from all the football data in the
# paste_all_football_data_text_box and reverse them (i.e. transform the line "Paul,Scholes" into
# "Scholes,Paul" etc.
# Place the list of reversed names in the csv_data_text_box in the main window
# ====================================================================================================
def put_home_scorer_names_reversed_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all home scorers
    home_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'h':
            home_scorers.append(scorer)

    # build the text for the list of reversed names
    text = ''
    for scorer in home_scorers:
        text += scorer["last_name"] + ', ' + scorer["first_name"] + "\n"
    text = text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', text)

    return
# ====================================================================================================
# Extract all scorer information from the football data in the
# paste_all_football_data_text_box and build a list containing '20/1' and all the home first scorer
# prices. Place this list in the csv_data_text_box in the main window.
# ====================================================================================================
def put_twenty_to_one_and_home_first_scorer_prices_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all home scorers
    home_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'h':
            home_scorers.append(scorer)

    # build the text for the list containing '20/1' followed by all the first scorer prices
    output_text = '20/1' + "\n"
    for scorer in home_scorers:
        output_text += scorer["first_scorer_price"] + "\n"
    output_text = output_text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the output_text in the csv_data_text_box
    csv_data_text_box.insert('1.0', output_text)

    return
# ====================================================================================================
# Extract the away scorer names from all the football data in the
# paste_all_football_data_text_box and reverse them (i.e. transform the line "Paul,Scholes" into
# "Scholes,Paul" etc.
# Place the list of reversed names in the csv_data_text_box in the main window
# ====================================================================================================
def put_away_scorer_names_reversed_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all away scorers
    away_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'a':
            away_scorers.append(scorer)

    # build the text for the list of reversed names
    text = ''
    for scorer in away_scorers:
        text += scorer["last_name"] + ', ' + scorer["first_name"] + "\n"
    text = text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', text)

    return
# ====================================================================================================
# Extract all scorer information from the football data in the
# paste_all_football_data_text_box and build a list containing all the away first scorer
# prices. Place this list in the csv_data_text_box in the main window.
# ====================================================================================================
def put_away_first_scorer_prices_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all away scorers
    away_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'a':
            away_scorers.append(scorer)

    # build the text for the list containing the away first scorer prices
    output_text = ''
    for scorer in away_scorers:
        output_text += scorer["first_scorer_price"] + "\n"
    output_text = output_text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the output_text in the csv_data_text_box
    csv_data_text_box.insert('1.0', output_text)

    return
# ====================================================================================================
# Extract all scorer information from the football data in the
# paste_all_football_data_text_box and build a list containing all the home brace prices.
# Place this list in the csv_data_text_box in the main window.
# ====================================================================================================
def put_home_brace_prices_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all the home scorers
    home_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'h':
            home_scorers.append(scorer)

    # build the list of home brace prices
    output_text = ''

    for scorer in home_scorers:
        # if brace price is empty, enter 'n' for the price, otherwise enter the price string
        if scorer["brace_price"] == '':
            output_text += "n\n"
        else:
            output_text += scorer["brace_price"] + "\n"
    output_text = output_text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', output_text)

    return
# ====================================================================================================
# Extract all scorer information from the football data in the
# paste_all_football_data_text_box and build a list containing all the away brace prices.
# Place this list in the csv_data_text_box in the main window.
# ====================================================================================================
def put_away_brace_prices_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all the away scorers
    away_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'a':
            away_scorers.append(scorer)

    # build the list of away brace prices
    output_text = ''

    for scorer in away_scorers:
        # if brace price is empty, enter 'n' for the price, otherwise enter the price string
        if scorer["brace_price"] == '':
            output_text += "n\n"
        else:
            output_text += scorer["brace_price"] + "\n"
    output_text = output_text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', output_text)

    return
# ====================================================================================================
# Extract all scorer information from the football data in the
# paste_all_football_data_text_box and build a list containing all the home hat-trick prices.
# Place this list in the csv_data_text_box in the main window.
# ====================================================================================================
def put_home_hat_trick_prices_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all the home scorers
    home_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'h':
            home_scorers.append(scorer)

    # build the list of home hat-trick prices
    output_text = ''

    for scorer in home_scorers:
        # if hat-trick price is empty, enter 'n' for the price, otherwise enter the price string
        if scorer["hat_trick_price"] == '':
            output_text += "n\n"
        else:
            output_text += scorer["hat_trick_price"] + "\n"
    output_text = output_text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', output_text)

    return
# ====================================================================================================
# Extract all scorer information from the football data in the
# paste_all_football_data_text_box and build a list containing all the away hat-trick prices.
# Place this list in the csv_data_text_box in the main window.
# ====================================================================================================
def put_away_hat_trick_prices_in_main_window_text_widget():

    # get text from paste_all_football_data_text_box
    text = paste_all_football_data_text_box.get("1.0", END)
    text = text.strip()

    # get all the scorer information
    scorer_data = extract_scorer_information_from_csv_data(text)

    # get all the away scorers
    away_scorers = []
    for scorer in scorer_data:
        if scorer["home_or_away"] == 'a':
            away_scorers.append(scorer)

    # build the list of away hat-trick prices
    output_text = ''

    for scorer in away_scorers:
        # if hat-trick price is empty, enter 'n' for the price, otherwise enter the price string
        if scorer["hat_trick_price"] == '':
            output_text += "n\n"
        else:
            output_text += scorer["hat_trick_price"] + "\n"
    output_text = output_text.strip()

    # delete text from csv_data_text_box
    csv_data_text_box.delete('1.0', END)

    # stick the text in the csv_data_text_box
    csv_data_text_box.insert('1.0', output_text)

    return
# ====================================================================================================
# Set up the interface
# Basic window
root = Tk()
root.wm_title("Participant Blaster (Amelyn Technologies 2016)")

# Frame to hold the four X and Y coordinates the program requires.
# We're going to grid the six coordinates and their labels into the xy_frame,
# then grid the xy_frame in the root
xy_frame = ttk.Frame(root)

# Set up x and y coordinate Text boxes and their labels, grid them into xy_frame
save_x_label = Label(xy_frame, text="Save X")
save_x_label.grid(row=0, column=0, sticky=E)
save_x_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
save_x_text_box.grid(row=0, column=1)

save_y_label = Label(xy_frame, text="Save Y")
save_y_label.grid(row=0, column=2, sticky=E)
save_y_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
save_y_text_box.grid(row=0, column=3)

input_x_label = Label(xy_frame, text="Input X")
input_x_label.grid(row=1, column=0, sticky=E)
input_x_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
input_x_text_box.grid(row=1, column=1)

input_y_label = Label(xy_frame, text="Input Y")
input_y_label.grid(row=1, column=2, sticky=E)
input_y_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
input_y_text_box.grid(row=1, column=3)

plus_x_label = Label(xy_frame, text="+ X")
plus_x_label.grid(row=2, column=0, sticky=E)
plus_x_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
plus_x_text_box.grid(row=2, column=1)

plus_y_label = Label(xy_frame, text="+ Y")
plus_y_label.grid(row=2, column=2, sticky=E)
plus_y_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
plus_y_text_box.grid(row=2, column=3)

keyboard_q_key_x_label = Label(xy_frame, text="kb Q X")
keyboard_q_key_x_label.grid(row=3, column=0, sticky=E)
keyboard_q_key_x_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
keyboard_q_key_x_text_box.grid(row=3, column=1)

keyboard_q_key_y_label = Label(xy_frame, text="kb Q Y")
keyboard_q_key_y_label.grid(row=3, column=2, sticky=E)
keyboard_q_key_y_text_box = Text(xy_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
keyboard_q_key_y_text_box.grid(row=3, column=3)

# Set up Swop Names Along Comma button, grid it into xy_frame
comma_swop_button = ttk.Button(xy_frame, text='Swop Text Along Commas',
                                    command=swop_names_along_commas)
comma_swop_button.grid(row=0, column=4, sticky=EW)

# NEW (30/9/16):
# REMOVED (12/6/18)
# Set up "Enter Home 1st Scorers & Prices" button, grid it onto xy_frame
# enter_home_1st_scorers_and_prices_button = ttk.Button(xy_frame, text='Home 1st Scorers & Prices',
                                    # command=enter_home_1st_scorers_and_prices)
# enter_home_1st_scorers_and_prices_button.grid(row=0, column=5, sticky=EW)

# NEW (26/9/16):
# Set up "Enter 1st Goal FC and Prices" button, grid it onto xy_frame
enter_fc_and_prices_button = ttk.Button(xy_frame, text='1st Goal WC & Prices',
                                    command=enter_first_goal_forecasts_and_prices)
enter_fc_and_prices_button.grid(row=2, column=5, sticky=EW)

# Set up Find and Enter button for finding and entering participants
button_text = 'Find & Enter Participants'
find_and_enter_participants_button = ttk.Button(xy_frame, text=button_text,
                                                    command=find_and_enter_participants)
find_and_enter_participants_button.grid(row=1, column=4, sticky=EW)

# NEW (27/9/16):
# Set up "Enter Anytime FC and Prices" button, grid it onto xy_frame
anytime_fc_and_prices_button = ttk.Button(xy_frame, text='Anytime WC & Prices',
                                    command=enter_anytime_forecasts_and_prices)
anytime_fc_and_prices_button.grid(row=3, column=5, sticky=EW)

# NEW (12/6/18) +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# "Enter home and away scorer names and all prices" button
enter_all_first_scorer_names_and_prices_button = ttk.Button(xy_frame,
            text='All 1st Scorers & Prices', command=enter_first_scorer_all_names_and_prices)
enter_all_first_scorer_names_and_prices_button.grid(row=0, column=5, sticky=EW)

# "Enter all anytime scorer prices" button
enter_all_anytime_scorer_prices_button = ttk.Button(xy_frame,
            text='All Anytime Scorer Prices', command=enter_all_anytime_scorer_prices)
enter_all_anytime_scorer_prices_button.grid(row=1, column=5, sticky=EW)
# END OF NEW (12/6/18) ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Set up Type In button for typing all the participants into blank cells
button_text = 'Type Lines Into Cells'
type_participants_in_button = ttk.Button(xy_frame, text=button_text,
                                                    command=type_participants_in)
type_participants_in_button.grid(row=2, column=4, sticky=EW)

# Create frame to hold the Letter Delay label and the Text widget for the user to enter the
# Letter Delay
letter_delay_frame = ttk.Frame(xy_frame)
# Create letter delay label and letter delay text widget and grid them into the letter_delay_frame
letter_delay_label = Label(letter_delay_frame, text="_")
letter_delay_label.grid(row=0, column=0, sticky=E)
letter_delay_text_box = Text(letter_delay_frame, width=4, height=1, background='#000000',
                             foreground='#FFFF00', font=('Courier', 12, 'bold'))
letter_delay_text_box.grid(row=0, column=1, sticky=E)
# Grid the letter_delay_frame onto root
letter_delay_frame.grid(row=3, column=4, sticky=E)

# Grid xy_frame into root
xy_frame.grid(row=0, column=0, sticky=W)

# Create status label and single line Text widget to display information about the participant
# currently beining entered (participant, X of Y for the participant in the current list and
# percentage of list entered so far
status_label = Label(root, text="Status")
# status_label.grid(row=1, column=0, sticky=W)
status_text_box = Text(root, width=34, height=2, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
# status_text_box.grid(row=2, column=0, sticky=W)

# NEW 16/6/18 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create frame to hold the "Paste CSV data here" label and the "Don't type /1 suffixes" label
two_labels_and_tickbox_frame = ttk.Frame(root)

# Label and textbox for next_market_x
next_market_x_label = Label(two_labels_and_tickbox_frame, text="Next Market X")
next_market_x_label.grid(row=0, column=0, sticky=W)
next_market_x_text_box = Text(two_labels_and_tickbox_frame, width=4, height=1,
                              background='#000000', foreground='#FFFF00',
                                font=('Courier', 12, 'bold'))
next_market_x_text_box.grid(row=0, column=1)

# Label and textbox for next_market_y
next_market_y_label = Label(two_labels_and_tickbox_frame, text="Next Market Y")
next_market_y_label.grid(row=0, column=2, sticky=W)
next_market_y_text_box = Text(two_labels_and_tickbox_frame, width=4, height=1,
                              background='#000000', foreground='#FFFF00',
                                font=('Courier', 12, 'bold'))
next_market_y_text_box.grid(row=0, column=3)

# Variable linked to "don't type /1 suffixes checkbox"
dont_type_to_one = IntVar()

# Tickbox for not typing '/1' suffixes in prices
dont_type_to_one_checkbox = Checkbutton(two_labels_and_tickbox_frame,
                                text="Don't type /1 suffixes", variable=dont_type_to_one)
dont_type_to_one_checkbox.grid(row=0, column=4, sticky=W)

# both wincasts button
both_wincasts_button = ttk.Button(two_labels_and_tickbox_frame, text='Both WC',
                                    command=enter_both_wincast_markets)
both_wincasts_button.grid(row=0, column=5, sticky=W)

# grid it
two_labels_and_tickbox_frame.grid(row=1, column=0, sticky=W)
# END OF NEW 16/6/18 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Create frame to hold the csv_data_text_box
csv_data_frame = ttk.Frame(root)

# create csv_data_text_box
csv_data_text_box = Text(csv_data_frame, width=53, height=3, background='#000000', foreground='#FFFF00',
                         insertbackground="#FFFFFF", font=('Courier', 10), wrap='word')
csv_data_text_box.pack(side=LEFT)
# create scrollbar, pack it into csv_data_text_box
scrollbar = Scrollbar(csv_data_frame)
scrollbar.pack(side=RIGHT, fill=Y)
# attach scrollbar to csv_data_text_box to each other
csv_data_text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=csv_data_text_box.yview)

# grid the csv_data_frame
csv_data_frame.grid(row=4, column=0, sticky=W)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# football_match_data_window for manipulating football scorer data.
# Set out like this:
#
# TEXT WIDGET
# <Text widget to paste all the football data for a single match into>
#
# BUTTONS:
# <All data>
# <Home scorers (reversed)>
# <20/1 + home first scorer prices>
# <Away scorers (reversed)>
# <Away first scorer prices>
# <Brace home prices>
# <Brace away prices>
# <Hat-trick home prices>
# <Hat-trick away prices>
#
# How it works:
# The user pastes all the data for a single football match into the text widget in the
# football_data_window. When one of the buttons in the football_data_window is pressed,
# the relevant data appears in the text widget in the main window.
# This will save the continual copying and pasting of different data from the
# football feature match webpage into the main page. All the data for a single football
# match can now be copied and pasted once and quickly and easily manipulated using the
# buttons in this new window.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
football_match_data_window = Tk()
football_match_data_window.wm_title("Football match data window (Amelyn Technologies 2016)")

# Frame to hold all the buttons and the text widget
football_data_frame = ttk.Frame(football_match_data_window)

# label above text widget which says "Paste All Football Data Here"
paste_all_football_data_here_label = Label(football_data_frame,
                                            text="Paste All Football Data Here")
paste_all_football_data_here_label.grid(row=0, column=0, sticky=E)

# text widget
paste_all_football_data_text_box = Text(football_data_frame, width=15, height=3,
                                        background='#000000', foreground='#FFFF00',
                                        font=('Courier', 12, 'bold'))
paste_all_football_data_text_box.grid(row=1, column=0)

# "all data" button
all_data_button = ttk.Button(football_data_frame, text='All data',
                                    command=put_all_data_in_main_window_text_widget)
all_data_button.grid(row=2, column=0, sticky=W)

# "home scorers (reversed)" button
home_scorers_reversed_button = ttk.Button(football_data_frame,
                                        text='Home scorer names (reversed)',
                        command=put_home_scorer_names_reversed_in_main_window_text_widget)
home_scorers_reversed_button.grid(row=3, column=0, sticky=W)

# "20/1 + home first scorer prices" button
home_first_scorer_prices_button = ttk.Button(football_data_frame,
                                        text='20/1 & home first scorer prices',
        command=put_twenty_to_one_and_home_first_scorer_prices_in_main_window_text_widget)
home_first_scorer_prices_button.grid(row=4, column=0, sticky=W)

# "away scorers (reversed)" button
away_scorers_reversed_button = ttk.Button(football_data_frame,
                                        text='Away scorer names (reversed)',
                        command=put_away_scorer_names_reversed_in_main_window_text_widget)
away_scorers_reversed_button.grid(row=5, column=0, sticky=W)

# "away first scorer prices" button
away_first_scorer_prices_button = ttk.Button(football_data_frame,
                                        text='Away first scorer prices',
        command=put_away_first_scorer_prices_in_main_window_text_widget)
away_first_scorer_prices_button.grid(row=6, column=0, sticky=W)

# "brace home prices" button
home_brace_prices_button = ttk.Button(football_data_frame,
                                        text='Home brace prices',
        command=put_home_brace_prices_in_main_window_text_widget)
home_brace_prices_button.grid(row=7, column=0, sticky=W)

# "brace away prices" button
away_brace_prices_button = ttk.Button(football_data_frame,
                                        text='Away brace prices',
        command=put_away_brace_prices_in_main_window_text_widget)
away_brace_prices_button.grid(row=8, column=0, sticky=W)

# "hat-trick home prices" button
home_hat_trick_prices_button = ttk.Button(football_data_frame,
                                        text='Home hat-trick prices',
        command=put_home_hat_trick_prices_in_main_window_text_widget)
home_hat_trick_prices_button.grid(row=9, column=0, sticky=W)

# "hat-trick away prices" button
away_hat_trick_prices_button = ttk.Button(football_data_frame,
                                        text='Away hat-trick prices',
        command=put_away_hat_trick_prices_in_main_window_text_widget)
away_hat_trick_prices_button.grid(row=10, column=0, sticky=W)

# grid the football_data_frame
football_data_frame.grid(row=0, column=0, sticky=W)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Start 'er up!
root.mainloop()
