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
day     = '01'
month   = '01'
year    = '2017'
hour    = '23'
minutes = '59'
# ==============================================================================
def main():

    # create match dictionaries from information in "football_betting_webpage.htm"
    match_dictionaries = build_match_dictionaries_from_webpage()

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
def build_match_dictionaries_from_webpage():

    infile = open('football_betting_webpage.htm', 'r')
    html = infile.read()
    infile.close()
    
    # split html up into blocks
    code_blocks = html.split('<table')
    code_blocks = code_blocks[1:]
    print('Total code blocks =', str(len(code_blocks)))
    # print()
    # print(code_blocks[0])
    # print()
    # print(code_blocks[1])

    match_dictionaries = []

    # each pair of code blocks represents a single match
    # extract all the data for each match
    for count in range(0, len(code_blocks) - 2, 3):
        code_block = code_blocks[count] + code_blocks[count + 1]
        # get time string, hour, minutes
        start = code_block.find('Kick off: ') + 10
        end = start
        while code_block[end] != '<':
            end += 1
        time_string = code_block[start:end]
        hour, minutes = parse_time_string(time_string)
        print('time_string =', time_string)
        print('hour =', hour)
        print('minutes =', minutes)
        # get home_price
        start = code_block.find('big_price')
        while code_block[start] != '>':
            start += 1
        start += 1
        end = start
        while code_block[end] != '<':
            end += 1
        home_price = code_block[start:end]
        print('home_price =', home_price)
        code_block = code_block[end:]
        # get home_team
        start = code_block.find('<h1>') + 4
        end = start
        while code_block[end] != '<':
            end += 1
        home_team = code_block[start:end]
        print('home_team =', home_team)
        code_block = code_block[end:]
        # draw_price
        start = code_block.find('text-align: center')
        while code_block[start] != '>':
            start += 1
        start += 1
        end = start
        while code_block[end] != '<':
            end += 1
        draw_price = code_block[start:end]
        print('draw_price =', draw_price)
        code_block = code_block[end:]
        # get away_team
        start = code_block.find('<h1>') + 4
        end = start
        while code_block[end] != '<':
            end += 1
        away_team = code_block[start:end]
        print('away_team =', away_team)
        code_block = code_block[end:]
        # get away_price
        start = code_block.find('big_price')
        while code_block[start] != '>':
            start += 1
        start += 1
        end = start
        while code_block[end] != '<':
            end += 1
        away_price = code_block[start:end]
        print('away_price =', away_price)
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
