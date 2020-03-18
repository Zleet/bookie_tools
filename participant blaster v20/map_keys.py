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
