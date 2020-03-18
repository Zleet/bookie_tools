# ==============================================================================
# For the friendly football matches in 'friendly_football_matches_CSV.csv'
# build GUIScript data in the format:
#
# ===============================
# Match #1:
#               # day
#               # month
#               # year (4 digits)
#               # hour
#               # minutes
#               # home_team
#               # away_team
#               # home_price
#               # draw_price
#               # away_price
# etc.
# ==============================================================================
# globals (bad!); set these date settings as required
day     = '29'
month   = '07'
year    = '2017'
hour    = '23'
minutes = '59'
# ==============================================================================
def main():

    # create match dictionaries from lines in "friendly_football_matches_CSV.csv"
    match_dictionaries = build_match_dictionaries_from_csv_file()

    # build big guiscript data string from match_dictionaries
    big_data_string = build_guiscript_data_string(match_dictionaries)

    # write big_data_string to outfile
    outfile = open('guiscript_data.txt', 'w')
    outfile.write(big_data_string)
    outfile.close()

    print()
    print('***** RUN COMPLETE *****')

    return
# ==============================================================================
# Build a bunch of match dictionaries in the form
# ==============================================================================
def build_match_dictionaries_from_csv_file():

    infile = open('friendly football matches_CSV.csv', 'r')
    lines = infile.readlines()
    infile.close()

    # remove first line (doesn't contain match data)
    lines = lines[1:]
    
    # loop through lines; only keep lines that contain characters other that commas
    kept_lines = []
    for line in lines:
        line = line.strip()
        for character in line:
            if character != ',':
                kept_lines.append(line)
                break
    lines = kept_lines

    # loop through lines; for each line, create a match dictionary in the form:
    # match_dictionary = {
    #           "day"           : "01",
    #           "month"         : "01",
    #           "year"          : "2017",
    #           "hour"          : "23",
    #           "minutes"       : "59"
    #           "home_team"     : "Liverpool",
    #           "away_team"     : "Man Utd",
    #           "home_price"    : "16/5",
    #           "draw_price"    : "12/5",
    #           "away_price"    : "10/11"
    #                       }
    # Append all the match dictionaries onto the list match_dictionaries
    match_dictionaries = []
    for line in lines:
        # day, month, year are globals; we don't need to extract them
        line = line.strip()
        elements = line.split(',')
        # get time_string, parse into hour and minutes
        time_string = elements[6].strip()
        hour, minutes = parse_time_string(time_string)
        # get home_team
        home_team = elements[1].strip()
        # get away_team
        away_team = elements[3].strip()
        # get home_price
        home_price = elements[0].replace("'", "").strip()
        # get draw_price
        draw_price = elements[2].replace("'", "").strip()
        # get away_price
        away_price = elements[4].replace("'", "").strip()
        # build match_dictionary, append it to match_dictionaries
        match_dictionary = {
                "day"           : day,
                "month"         : month,
                "year"          : year,
                "hour"          : hour,
                "minutes"       : minutes,
                "home_team"     : home_team,
                "away_team"     : away_team,
                "home_price"    : home_price,
                "draw_price"    : draw_price,
                "away_price"    : away_price
                            }
        match_dictionaries.append(match_dictionary)

    return match_dictionaries
# ==============================================================================
# Parse a time string such as 'S00.30' or '20.3' into a two item dictionary of
# hour and minute, both in two character string format
# e.g. ['00', '30'] or ['20', '30']
# ==============================================================================
def parse_time_string(time_string):

    # lose all characters other than 0-9, '.' and ':'
    permissable_characters = '0123456789:.'

    sanitised_time_string = ''
    for character in time_string:
        if character in permissable_characters:
            sanitised_time_string += character
    time_string = sanitised_time_string

    # parse time_string
    # sample time strings: '11.3', '15', '20.3', '00.30'
    if ('.' in time_string) or (':' in time_string):
        if '.' in time_string:
            split_char = '.'
        if ':' in time_string:
            split_char = ':'
        split_pos = time_string.find(split_char)
        hour = time_string[:split_pos].strip()
        minutes = time_string[split_pos + 1:].strip()
        if len(hour) == 1:
            hour = '0' + hour
        if len(minutes) == 0:
            minutes = '00'
        elif len(minutes) == 1:
            minutes = minutes + '0'
    else: # no ':' or '.' in time_string so it's just an hour
        hour = time_string
        if len(hour) == 1:
            hour = '0' + hour
        minutes = '00'

    return [hour, minutes]
# ==============================================================================
# Build a big GUIScript data string in the format:
#
# ===============================
# Match #1:
# 19            # day
# 08            # month
# 2017          # year (4 digits)
# 23            # hour
# 59            # minutes
# Liverpool     # home_team
# Man Utd       # away_team
# 16/5          # home_price
# 10/11         # draw_price
# 2/5           # away_price
# etc.
# for all the match dictionaries in match_dictionaries
# ==============================================================================
def build_guiscript_data_string(match_dictionaries):

    big_data_string = ''

    match_no = 1
    for match_dictionary in match_dictionaries:
        big_data_string += "# ==================\n# Match #"
        big_data_string += str(match_no) + "\n"
        big_data_string += build_data_string_for_single_match(match_dictionary)
        match_no += 1

    return big_data_string
# ==============================================================================
# Helper function for build_guiscript_data_string(match_dictionaries)
# ==============================================================================
def build_data_string_for_single_match(match_dictionary):

    # determine target string length
    target_length = max(
                        len(match_dictionary["day"]),
                        len(match_dictionary["month"]),
                        len(match_dictionary["year"]),
                        len(match_dictionary["hour"]),
                        len(match_dictionary["minutes"]),
                        len(match_dictionary["home_team"]),
                        len(match_dictionary["away_team"]),
                        len(match_dictionary["home_price"]),
                        len(match_dictionary["draw_price"]),
                        len(match_dictionary["away_price"])
                        )
    target_length += 1

    data_string = match_dictionary["day"]
    data_string += (' ' * (target_length - len(match_dictionary["day"])))
    data_string += "# day\n"

    data_string += match_dictionary["month"]
    data_string += (' ' * (target_length - len(match_dictionary["month"])))
    data_string += "# month\n"

    data_string += match_dictionary["year"]
    data_string += (' ' * (target_length - len(match_dictionary["year"])))
    data_string += "# year\n"

    data_string += match_dictionary["hour"]
    data_string += (' ' * (target_length - len(match_dictionary["hour"])))
    data_string += "# hour\n"

    data_string += match_dictionary["minutes"]
    data_string += (' ' * (target_length - len(match_dictionary["minutes"])))
    data_string += "# minutes\n"

    data_string += match_dictionary["home_team"]
    data_string += (' ' * (target_length - len(match_dictionary["home_team"])))
    data_string += "# home_team\n"

    data_string += match_dictionary["away_team"]
    data_string += (' ' * (target_length - len(match_dictionary["away_team"])))
    data_string += "# away_team\n"

    data_string += match_dictionary["home_price"]
    data_string += (' ' * (target_length - len(match_dictionary["home_price"])))
    data_string += "# home_price\n"

    data_string += match_dictionary["draw_price"]
    data_string += (' ' * (target_length - len(match_dictionary["draw_price"])))
    data_string += "# draw_price\n"

    data_string += match_dictionary["away_price"]
    data_string += (' ' * (target_length - len(match_dictionary["away_price"])))
    data_string += "# away_price\n"
    
    return data_string
# ==============================================================================
main()
