# =============================================================================
# Build a webpage from the "football to build" spreadsheet, formatted in
# the colours I usually format the spreadsheet.
#
# Instructions:
# 1. Save the football spreadsheet as "football_to_build.csv"
# 2. Run this Python 3 script.
# 3. The script will build the football in a webpage named
#    "football_webpage.htm"
# =============================================================================
def main():

    build_webpage_from_spreadsheet_containing_football_fixtures()

    print()
    print('***** RUN COMPLETE *****')

    return
# =============================================================================
def build_webpage_from_spreadsheet_containing_football_fixtures():

    infile = open('football_to_build.csv', 'r')
    lines = infile.readlines()
    infile.close()

    # read euro league identifiers from file; we're going to use these to
    # identify european football leagues
    euro_league_identifiers = read_league_identifiers_from_file('euro_league_identifiers.txt')

    # read domestic league identifiers from file; we're going to use these to
    # identify domestic football leagues
    domestic_league_identifiers = read_league_identifiers_from_file('domestic_league_identifiers.txt')

    # filter lines; get rid of lines that don't contain any information
    lines = get_rid_of_non_information_lines(lines)

    # classify lines
    line_dictionaries = classify_lines(lines, domestic_league_identifiers, euro_league_identifiers)

    # print('Total kept lines =', len(lines))

    # Count unclassified lines
    total_unclassified_lines = 0
    for line_dictionary in line_dictionaries:
        if line_dictionary["line_type"] == 'undetermined':
            total_unclassified_lines += 1
    # If some lines remain unclassified, print them and quit
    if total_unclassified_lines > 0:
        print()
        print('The following league titles have not been successfully classified:')
        print()
        for line_dictionary in line_dictionaries:
            if line_dictionary["line_type"] == 'undetermined':
                elements = line_dictionary["line_text"].split(',')
                league_title = elements[3].strip()
                print(league_title)
        print()
        print('Append them to the appropriate text file')
        print('("domestic_league_identifiers.txt" or "euro_league_identifiers.txt")')
        print('and run this script again.')
        # new - bug fixing!!! (23/2/18)
        print()
        print('unclassified matches:')
        for line_dictionary in line_dictionaries:
            if line_dictionary["line_type"] == 'undetermined':
                print(line_dictionary)
        exit(0)

    # read the html template
    infile = open('webpage_template.htm', 'r')
    html = infile.read()
    infile.close()

    # build a big table with all the football in order, populate the html template with it
    football_table = build_html_football_table(line_dictionaries)
    html = html.replace('{{football_table_goes_here}}', football_table)

    # build two lists: domestic league titles and european league titles; format them in
    # teletext name style (e.g. 'Spa: Spanish La Liga') and place them in a textarea at the bottom
    # of the webpage, ready to copy and paste into Linefeeder
    league_titles_text = build_league_titles_text(line_dictionaries)
    html = html.replace('{{league_titles_text_goes_here}}', league_titles_text)

    # build text containing all home and away team names, one per line
    team_names_text = build_team_names_text(line_dictionaries)
    html = html.replace('{{team_names_text_goes_here}}', team_names_text)

    # build list of teletext names in the format:
    # <teletext_name>,<total_matches>
    # where <teletext_name> is the current teletext name and <total_matches> is the total
    # number of football matches to apply it to.
    # For example:
    # Eng: Championship,5
    # means there are five English Championship matches
    # Place these teletext name lines in a textarea at the bottom of the webpage
    teletext_count_lines = []
    current_teletext_name = ''
    name_count = 0
    for line_dictionary in line_dictionaries:
        if 'league' in line_dictionary["line_type"]:
            if name_count > 0:
                teletext_count_lines.append(current_teletext_name + ',' + str(name_count))
            name_count = 0 # reset name_count
            # set current_teletext_name
            line = line_dictionary["line_text"]
            elements = line.split(',')
            current_teletext_name = elements[3].strip()
            current_teletext_name = current_teletext_name[:3] + ': ' + current_teletext_name
        if line_dictionary["line_type"] == 'match':
            name_count += 1
    big_teletext_name_count_string = "\n".join(teletext_count_lines)
    html = html.replace('{{teletext_name_count_lines_go_here}}', big_teletext_name_count_string)

    # build the text data to copy and paste into GUIScript, in order to build a bunch of
    # trio matches automatically
    big_guiscript_string = build_guiscript_data(line_dictionaries)

    # place the guiscript_data at the bottom of the webpage
    html = html.replace('{{guiscript_data_goes_here}}', big_guiscript_string)

    # build the football coupon strings
    football_coupon_strings = build_football_coupon_strings(line_dictionaries)
    football_coupon_strings_text = "\n".join(football_coupon_strings)

    # stick the football coupon strings in the football coupon strings textarea
    html = html.replace('{{football_coupon_strings_go_here}}', football_coupon_strings_text)

    # write the webpage to the outfile
    outfile = open('football_to_build_.htm', 'w')
    outfile.write(html)
    outfile.close()

    return
# =============================================================================
# Build the text that goes in the "team names textarea" at the bottom of the
# page. It consists of all home and away team names, one per line.
# =============================================================================
def build_team_names_text(line_dictionaries):

    # test print
    # for line_dictionary in line_dictionaries:
        # print(line_dictionary)

    team_names = []

    for line_dictionary in line_dictionaries:
        if line_dictionary["line_type"] == 'match':
            line = line_dictionary["line_text"].strip()
            elements = line.split(',')
            team_names.append(elements[2].strip())
            team_names.append(elements[4].strip())

    text = "\n".join(team_names)

    return text
# =============================================================================
# Build a list of league titles in the form:
# 'Spa: Spanish La Liga' etc., one per line, for placing in a textarea at the
# bottom of the webpage
# =============================================================================
def build_league_titles_text(line_dictionaries):

    euro_leagues = []
    domestic_leagues = []

    for line_dictionary in line_dictionaries:
        # if euro league and not already in euro_leagues list, add it to list
        if line_dictionary["line_type"] == "euro league":
            elements = line_dictionary["line_text"].split(',')
            league_title = elements[3].strip()
            if not league_title in euro_leagues:
                euro_leagues.append(league_title[:3] + ': ' + league_title)
        # if domestic league and not already in domestic_leagues list, add it to list
        if line_dictionary["line_type"] == "domestic league":
            elements = line_dictionary["line_text"].split(',')
            league_title = elements[3].strip()
            if not league_title in domestic_leagues:
                domestic_leagues.append(league_title)

    euro_leagues_joined = "\n".join(euro_leagues)
    domestic_leagues_joined = "\n".join(domestic_leagues)
    league_titles_text = domestic_leagues_joined + "\n\n" + euro_leagues_joined

    # read the teletext name conversions from the local file
    # "teletext_name_conversions.csv"
    infile = open('teletext_name_conversions.csv', 'r')
    lines = infile.readlines()
    infile.close()

    # loop through lines; remove whitespace lines and lines consisting of a
    # sole comma
    kept_lines = []
    for line in lines:
        line = line.strip()
        if (len(line) > 0) and (line != ','):
            kept_lines.append(line)
    lines = kept_lines

    # build a bunch of teletext replacement dictionaries in the form:
    # {
    #   "original_teletext_name"    : "League Cup",
    #   "replacement_teletext_name" : "Eng: League Cup"
    # }
    # Stick all the teletext replacement dictionaries in the list
    # teletext_replacement_dictionaries
    teletext_replacement_dictionaries = []
    for line in lines:
        line = line.strip()
        elements = line.split(',')
        teletext_replacement_dictionary = {
            "original_teletext_name"    : elements[0].strip(),
            "replacement_teletext_name" : elements[1].strip()
                                                }
        teletext_replacement_dictionaries.append(teletext_replacement_dictionary)

    # sort the lines into alphabetical order and write them back to the local
    # file "teletext_name_conversions.csv"
    lines.sort()
    outfile = open('teletext_name_conversions.csv', 'w')
    outfile.write("\n".join(lines))
    outfile.close()

    # get all the lines in league_titles_text
    league_title_lines = league_titles_text.split("\n")

    # loop through league_title_lines and remove whitespace lines
    kept_league_title_lines = []
    for line in league_title_lines:
        line = line.strip()
        if len(line) > 0:
            kept_league_title_lines.append(line)
    league_title_lines = kept_league_title_lines
    
    for line in league_title_lines:
        print(line)

    # loop through league_title_lines; for each league title line, try to find a
    # teletext replacement line with which to replace it. If we can't find a
    # replacement for the league title line, append the league title line to
    # the list non_replaced_league_title_lines
    non_replaced_league_title_lines = []
    # for league_title_line in league_title_lines:
    for count in range(len(league_title_lines)):
        league_title_line = league_title_lines[count]
        replacement_line = ''
        # try to find a teletext replacement for the current league title line
        replacement_has_been_found = 0
        for teletext_replacement_dict in teletext_replacement_dictionaries:
            if teletext_replacement_dict["original_teletext_name"] == league_title_line:
                replacement_has_been_found = 1
                replacement_line = teletext_replacement_dict["replacement_teletext_name"]
                break
        # if we've found a replacement, replace the line, otherwise append the
        # league title line to non_replaced_league_title_lines
        if replacement_has_been_found:
            league_title_line = replacement_line
            league_title_lines[count] = league_title_line
        else:
            non_replaced_league_title_lines.append(league_title_line)

    # remove duplicate non_replaced_league_title_lines
    # (new on 13/1/20 at 0901)
    rebuilt_lines = []
    for title_line in non_replaced_league_title_lines:
        if not title_line in rebuilt_lines:
            rebuilt_lines.append(title_line)
    non_replaced_league_title_lines = rebuilt_lines

    # if there is at least one non-replaced league title line, warn the user,
    # provide a list of all the non-replaced league title lines and exit
    if len(non_replaced_league_title_lines) > 0:
        message = "\n\n"
        message += 'The following teletext names (and their replacements)'
        message += ' should be appended to the local file '
        message += '"teletext_name_conversions.csv":' + "\n"
        # build the list of non replaced league title lines
        for non_replaced_league_title in non_replaced_league_title_lines:
            message += non_replaced_league_title + ',' + non_replaced_league_title + "\n"
        print(message)
        exit(0)

    league_titles_text = "\n".join(league_title_lines)
    # bookmark (17/8/19 at 1504)

    return league_titles_text
# =============================================================================
# Build a html football table for all of the football, in the same order as
# on the supplied spreadsheet (i.e. in the same order as the line dictionaries
# in line_dictionaries
# =============================================================================
def build_html_football_table(line_dictionaries):

    # Find out the league type of the first league title and build the first line
    # of the football table, containing either FOOTBALL EURO or FOOTBALL MASTER
    current_league_type = ''
    for line_dictionary in line_dictionaries:
        # print()
        # print(line_dictionary)
        if ( (line_dictionary["line_type"] == 'domestic league')
             or (line_dictionary["line_type"] == 'euro league') ):
            current_league_type = line_dictionary["line_type"]
            break
    html = '<table>' + "\n"
    html += '<tr><td COLSPAN="5" class="league_separator"><b>'
    if current_league_type == 'euro league':
        html += 'FOOTBALL EURO'
    if current_league_type == 'domestic league':
        html += 'FOOTBALL MASTER'
    html += '</b></td><td></td><td></td><td></td><td></td></tr>'

    # Build the table and return it
    # Format for match rows is:
    # '<tr><td>MATCH NO</td><td>BLANK CELL</td><td>HOME TEAM</td><td></td><td>AWAY TEAM</td><td>BLANK CELL</td>'
    # <td>KICK OFF TIME</td><td>LIVE ON</td><td>F FOR FEATURE MATCH</td></tr>'
    # (9 COLUMNS)
    match_no = 0
    for line_dictionary in line_dictionaries:
        # if line is a league:
        # 1. change current_league_type
        # 2. make a html table row for this league line
        if ( (line_dictionary["line_type"] == 'euro league')
             or (line_dictionary["line_type"] == 'domestic league') ):
            # if different league type to current_league_type, build a league separator line
            # e.g. "FOOTBALL EURO" or "FOOTBALL MASTER"
            if line_dictionary["line_type"] != current_league_type:
                html += '<tr><td COLSPAN="5" class="league_separator"><b>'
                if line_dictionary["line_type"] == 'euro league':
                    html += 'FOOTBALL EURO'
                if line_dictionary["line_type"] == 'domestic league':
                    html += 'FOOTBALL MASTER'
                html += '</b></td><td></td><td></td><td></td><td></td></tr>'
            current_league_type = line_dictionary["line_type"]
            html += '<tr><td COLSPAN="5" class="league_title"><b>'
            elements = line_dictionary["line_text"].split(',')
            html += elements[3].strip()
            html += '</b></td><td></td><td></td><td></td><td></td></tr>'
        # if line is a date or a section divider, build the appropriate html table row
        if (line_dictionary["line_type"] == "date") or (line_dictionary["line_type"] == "section divider"):
            html += '<tr><td COLSPAN="5" class="date_or_section_divider">'
            elements = line_dictionary["line_text"].split(',')
            html += elements[3].strip()
            html += '</td><td></td><td></td><td></td><td></td></tr>'
        # if line is a match, construct the appropriate html table line
        if line_dictionary["line_type"] == "match":
            # print(line_dictionary)
            match_no += 1
            elements = line_dictionary["line_text"].split(',')
            html += '<tr>'
            html += '<td class="match_no">' + str(match_no) + '</td>'    # match no
            html += '<td>' + '' + '</td>'
            html += '<td class="home_team">' + elements[2].strip() + '</td>' # home team
            html += '<td style="width: 15px;">' + '' + '</td>'
            html += '<td class="away_team">' + elements[4].strip() + '</td>' # away team
            html += '<td>' + '' + '</td>'
            # print(elements) # new
            html += '<td class="ko_time">' + elements[6].strip() + '</td>' # kick off time
            html += '<td class="live_on">' + elements[7].strip() + '</td>' # live on...
            html += '<td class="f_for_feature" style="width: 15px;">'
            html += elements[8].strip() + '</td>' # F for Feature Match
            html += '</tr>'
    html += '</table>'

    return html
# =============================================================================
# Get rid of lines that don't contain information in any of cells C,D or E
# (i.e. elements[2], elements[3] or elements[4])
# =============================================================================
def get_rid_of_non_information_lines(lines):

    kept_lines = []
    
    for line in lines:
        elements = line.split(',')
        # flags
        c_col_data = 0
        d_col_data = 0
        e_col_data = 0
        if len(elements[2].strip()) > 1:
            c_col_data = 1
        if len(elements[3].strip()) > 1:
            d_col_data = 1
        if len(elements[4].strip()) > 1:
            e_col_data = 1
        if c_col_data or ( (d_col_data) or (e_col_data) ):
            kept_lines.append(line)

    return kept_lines
# =============================================================================
# 1. Read league identifiers from a text file (may be either european or
#    domestic
# 2. Filter out whitespace lines
# 3. Sort the identifiers into alphabetical order
# 4. Filter out duplicate identifiers
# 5. Write the identifiers back to the file
# 6. Return the list of identifiers
#
# Using this method, we can add new league identifiers to the end of
# the text file by hand, then run this script again and have it automatically
# sort all the league identifiers in the text file into alphabetical
# order, getting rid of duplicates.
# =============================================================================
def read_league_identifiers_from_file(filename):

    # read identifiers from file
    infile = open(filename, 'r')
    lines = infile.readlines()
    infile.close()

    # Filter out whitespace lines
    kept_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            kept_lines.append(line)
    lines = kept_lines

    # sort identifiers into alphabetical order
    lines.sort()

    # Filter out duplicate identifiers
    euro_identifiers = []
    for line in lines:
        if not line in euro_identifiers:
            euro_identifiers.append(line)

    # write the identifiers back to the file
    file_text = "\n".join(euro_identifiers)
    outfile = open(filename, 'w')
    outfile.write(file_text)
    outfile.close()

    return euro_identifiers
# =============================================================================
# Helper function for
# build_webpage_from_spreadsheet_containing_football_fixtures()
# Classify the lines
#
# For each line, create a dictionary in the form:
# {
#   "line_type" : "date",
#   "line_text" : ",,,Saturday 21st & Sunday 22nd January,,,,,,Total Goals,,,Goal Rush,"
# }
#
# or...
# {
#   "line_type" : "euro league",
#   "line_text" : ",,,African Cup of Nations,,,,,,,,,,"
# }
#
# {
#   "line_type" : "domestic league",
#   "line_text" : ",,,Premier League,,,,,,,,,,"
# }
#
# or...
#
# {
#   "line_type" : "match",
#   "line_text" : "46,,Bayer Leverkusen,,Hertha Berlin,,S 14.30,BT,F,,,,,"
# }
#
# or...
#
# {
#   "line_type" : "section divider",
#   "line_text" : ",,,Football Master,,,,,,,,,,"
# }
# and append it to the list line_dictionaries
# =============================================================================
def classify_lines(lines, domestic_league_identifiers, euro_league_identifiers):

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    section_identifiers = ['Football Master', 'Football Euro']

    line_dictionaries = []

    # BOOKMARK - SORT THIS FUNCTION OUT
    # LABEL EACH LINE AS BELONGING TO ONE OF THE FOLLOWING CATEGORIES:
    # 1. match line
    # 2. date line
    # 3. league line
    # 4. section separator (i.e. "Football Master" or "Football Euro"    

    for line in lines:
        line = line.strip()
        line_dictionary = {
                    "line_type" : "undetermined",
                    "line_text" : line.strip()
                            }
        elements = line.split(',')
        # identity flags
        contains_league_title = 0
        contains_date = 0
        contains_teams = 0
        contains_section_divider = 0
        # identify match line
        if len(elements) >= 5:
            if (len(elements[2].strip()) > 0) and (len(elements[4].strip()) > 0):
                contains_teams = 1
                line_dictionary["line_type"] = 'match'
        # identify date line
        if len(elements) >= 4:
            test_string = elements[3].strip()
            # check for day
            for day in days:
                if day.upper() in test_string.upper():
                    contains_date = 1
                    line_dictionary["line_type"] = 'date'
                    break
            # check for month
            for month in months:
                if month.upper() in test_string.upper():
                    contains_date = 1
                    line_dictionary["line_type"] = 'date'
                    break
        # identify euro league line
        if len(elements) >= 4:
            test_string = elements[3].strip()
            for euro_league_identifier in euro_league_identifiers:
                if euro_league_identifier.upper() == test_string.upper(): # changed from in to ==
                    line_dictionary["line_type"] = 'euro league'
                    break
        # identify domestic league line
        if len(elements) >= 4:
            test_string = elements[3].strip()
            for domestic_league_identifier in domestic_league_identifiers:
                if domestic_league_identifier.upper() == test_string.upper(): # changed from in to ==
                    line_dictionary["line_type"] = 'domestic league'
                    break
        # identify section separator
        if len(elements) >= 4:
            test_string = elements[3].strip()
            for section_identifier in section_identifiers:
                if section_identifier in test_string:
                    line_dictionary["line_type"] = 'section divider'
        # append line_dictionary to line_dictionaries
        line_dictionaries.append(line_dictionary)

    return line_dictionaries
# =============================================================================
# Build data for copying and pasting into GUIScript. GUIScript can then
# automatically build the matches.
#
# The GUIScript data returned from this function will be a large string
# containing information for every match. Each match will be represented by a
# substring in the following format:
#
# 25        # day
# 11        # month
# 2017      # year (4 digits)
# 23        # hour
# 59        # minutes
# Man Utd   # home team
# Liverpool # away team
#
# Within the function, match_dictionaries is a list containing a bunch of
# match dictionaries. Each match dictionary will be in the following format:
# match_dictionary = {
#                   "day"           : 25,
#                   "month"         : 11,
#                   "year"          : 2017,
#                   "hour"          : 19,
#                   "minute"        : 45,
#                   "home_team"     : "Man Utd",
#                   "away_team"     : "Liverpool"
#                       }
#
# =============================================================================
def build_guiscript_data(line_dictionaries):

    # default values, before first date line is parsed
    day     = -1
    month   = -1
    year    = 2020 # default
    hour    = -1
    minute  = -1

    match_dictionaries = [] # append match dictionaries to this list
    
    # Loop through lines:
    # if line is a date line, parse it and change the current date information,
    # otherwise parse match line, build a match dictionary for the match and append
    # the match dictionary to the list match_dictionaries
    for line in line_dictionaries:
        line_type = line["line_type"]
        line_text = line["line_text"]
        if line_type == 'date':
            day, month = parse_date_line_for_guiscript(line_text)
        if line_type == 'match':
            match_dictionary = build_match_dictionary_for_guiscript(line_text,
                                                            day, month, year)
            match_dictionaries.append(match_dictionary)

    # build the big text string to return
    big_guiscript_string = ''
    for count in range(len(match_dictionaries)):
        match_dictionary = match_dictionaries[count]
        # if day, month, hour or minute are single digit, a zero must be prepended
        # to them to form a two-digit string suitable for GUIScript to automatically
        # type into match builder; test for this and prepend where required
        # day
        day = str(match_dictionary["day"])
        if len(day) == 1:
            day = '0' + day
        # month
        month = str(match_dictionary["month"])
        if len(month) == 1:
            month = '0' + month
        # year
        year = str(match_dictionary["year"])
        # hour
        hour = str(match_dictionary["hour"])
        if len(hour) == 1:
            hour = '0' + hour
        # minute
        minute = str(match_dictionary["minute"])
        if len(minute) == 1:
            minute = '0' + minute
        # home and awy teams
        home_team = match_dictionary["home_team"]
        away_team = match_dictionary["away_team"]
        # work out length of largest string for this match
        left_col_width = max(4, len(home_team), len(away_team)) + 1
        # build the string for the current match, append it to big_guiscript_string
        # add 'Match # line'
        big_guiscript_string += "\n" + '# Match #' + str(count + 1) + "\n"
        # add day
        big_guiscript_string += day
        for count in range(left_col_width - 2):
            big_guiscript_string += ' '
        big_guiscript_string += "# day\n"
        # add month
        big_guiscript_string += month
        for count in range(left_col_width - 2):
            big_guiscript_string += ' '
        big_guiscript_string += "# month\n"
        # add year
        big_guiscript_string += year
        for count in range(left_col_width - 4):
            big_guiscript_string += ' '
        big_guiscript_string += "# year (4 digits)\n"
        # add hour
        big_guiscript_string += hour
        for count in range(left_col_width - 2):
            big_guiscript_string += ' '
        big_guiscript_string += "# hour\n"
        # add minutes
        big_guiscript_string += minute
        for count in range(left_col_width - 2):
            big_guiscript_string += ' '
        big_guiscript_string += "# minutes\n"
        # add home_team
        big_guiscript_string += home_team
        for count in range(left_col_width - len(home_team)):
            big_guiscript_string += ' '
        big_guiscript_string += "# home team\n"
        # add away_team
        big_guiscript_string += away_team
        for count in range(left_col_width - len(away_team)):
            big_guiscript_string += ' '
        big_guiscript_string += "# away team\n"

    # read file containing good name replacements for bad names (i.e. replace
    # football team names that are not in the McLeans system with football
    # team names that are in the McLeans system)
    infile = open('bad name to good name conversions.txt', 'r')
    lines = infile.readlines()
    infile.close()

    # lose first line (csv header line)
    lines = lines[1:]

    for line in lines:
        line = line.strip()
        if (len(line) > 0) and (',' in line):
            names = line.split(',')
            big_guiscript_string = big_guiscript_string.replace(names[0], names[1])

    return big_guiscript_string
# =============================================================================
# Parse a date line like this:
# ',,,Monday 10th July,,,,,,Total Goals,,,Goal Rush,'
# and return a two item list containing the day and month as integers
# e.g. [9, 11] or [23, 5]
# =============================================================================
def parse_date_line_for_guiscript(date_line):

    date_line = date_line.strip()
    elements = date_line.split(',')
    date_string = elements[3]

    # date_string looks like this:
    # 'Monday 10th July'
    elements = date_string.split()

    # get month
    month = -1 # month to return
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    for count in range(len(months)):
        current_month = months[count]
        if current_month.lower() in date_line.lower():
            month = count + 1
            break

    # get day
    day_string = elements[1]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    kept_digits = []
    for character in day_string:
        if character in numbers:
            kept_digits.append(character)
    day_no_string = ''.join(kept_digits)
    day_no = int(day_no_string)

    return [day_no, month]
# =============================================================================
# From a line in the following format:
# ',,Palmeiras,,Corinthians,,23.59,,,,,,,'
# build a guiscript match dictionary in the format:
# match_dictionary = {
#                   "day"           : 25,
#                   "month"         : 11,
#                   "year"          : 2017,
#                   "hour"          : 19,
#                   "minute"        : 45,
#                   "home_team"     : "Man Utd",
#                   "away_team"     : "Liverpool"
#                       }
# =============================================================================
def build_match_dictionary_for_guiscript(line_text, day, month, year):

    line_text = line_text.strip()
    elements = line_text.split(',')

    # get home team
    home_team = elements[2].strip()

    # get away team
    away_team = elements[4].strip()

    ko_string = elements[6].strip()
    # test for S prefix to time (if found, increment day)
    if (len(ko_string) > 0) and (ko_string[0].upper() == 'S'):
        day += 1
        if day > 31:
            day = 1
    # parse kick off time string to get hour and minute
    acceptable_chars = [':', '.', '0', '1', '2', '3', '4', '5', '6', '7',
                            '8', '9']
    kept_chars = []
    for character in ko_string:
        if character in acceptable_chars:
            kept_chars.append(character)
    ko_string = ''.join(kept_chars)
    # split along '.' or ':'
    if '.' in ko_string:
        elements = ko_string.split('.')
    if ':' in ko_string:
        elements = ko_string.split(':')
    # get hour
    hour = int(elements[0].strip())
    # get minute
    minute = int(elements[1].strip())

    # build match dictionary
    match_dictionary = {
                    "day"           : day,
                    "month"         : month,
                    "year"          : year,
                    "hour"          : hour,
                    "minute"        : minute,
                    "home_team"     : home_team,
                    "away_team"     : away_team
                        }

    return match_dictionary
# =============================================================================
# Build the football coupon strings. For each match, there will be three
# strings:
# 1. The coupon name, followed by "(feature)"
#   (e.g. "Liverpool v Man Utd (feature)"
# 2. same as (1), except without the "(feature)" appended
# 3. The league - date - live on/kick off time string that goes beneath the
#    match title on the football coupon
#    (e.g. "Championship - Saturday 31st August - Live Sky 12:30pm")
# =============================================================================
def build_football_coupon_strings(line_dictionaries):

    live_on_string_conversions = {
                "BT"    : "BT Sport",
                "SKY"   : "Sky",
                "BBCS"  : "BBC Scotland"
                                }

    # build a list of the keys in live_on_string_conversions
    live_on_string_conversions_keys = list(live_on_string_conversions.keys())

    print('live_on_string_conversions_keys:')
    print(live_on_string_conversions_keys)

    football_coupon_strings = []
    current_date_string = ''
    current_league_name = ''

    print()
    print()
    print('line_dictionaries:')
    for line_dict in line_dictionaries:
        print(line_dict)
        line_text = line_dict["line_text"]
        elements = line_text.split(',')
        # if line is a date line, change current_date_string
        if line_dict["line_type"] == 'date':
            current_date_string = elements[3].strip()
            # print('Date line found:', line_dict['line_text'])
            # print('current_date_string changed to', current_date_string)
        # if line is a league line, change current_league_name
        if ((line_dict["line_type"] == 'domestic league')
                or (line_dict["line_type"] == 'euro league')):
            current_league_name = elements[3].strip()
            # print('League line found:', line_dict['line_text'])
            # print('current_league_name changed to', current_league_name)
        # if line is a match AND it includes a 'F' for feature match, build the
        # three football coupon strings for that match and append them to
        # the list football_coupon_strings
        if ((line_dict["line_type"] == 'match') and (elements[8].strip().upper() == 'F')):
            print('Feature match found...')
            # build coupon name, followed by 'feature'
            home_team = elements[2].strip()
            away_team = elements[4].strip()
            coupon_name = home_team + ' v ' + away_team + ' (Feature)'
            football_coupon_strings.append(coupon_name)
            # build match name
            match_name = home_team + ' v ' + away_team
            football_coupon_strings.append(match_name)
            # ++++++++++++++++++++++++++++++++++++++++++++++++++
            # build league - date - live on/kick off time string
            # ++++++++++++++++++++++++++++++++++++++++++++++++++
            league_date_ko_string = current_league_name + ' - '
            league_date_ko_string += current_date_string + ' - '
            live_on_string = elements[7].strip()
            # convert live_on_string if it's available for conversion
            if live_on_string.upper() in live_on_string_conversions_keys:
                live_on_string = live_on_string_conversions[live_on_string.upper()]
            # get kick off time string
            kick_off_time_string = elements[6].strip().replace('.', ':')
            kick_off_time_string = convert_kick_off_time_string(kick_off_time_string)
            # if there's a live on string, the format for last_bit_of_string will be
            # 'Live * 7:45pm' otherwise it'll be 'Kick Off *pm'
            if len(live_on_string) > 0:
                last_bit_of_string = 'Live ' + live_on_string + ' ' + kick_off_time_string
            else:
                last_bit_of_string = 'Kick Off ' + kick_off_time_string
            # add last bit of string to league_date_ko_string
            league_date_ko_string += last_bit_of_string
            football_coupon_strings.append(league_date_ko_string)
            football_coupon_strings.append('')

    # test print
    print()
    print('football_coupon_strings:')
    for line in football_coupon_strings:
        print(line)

    return football_coupon_strings
# =============================================================================
# Convert a time string in the format '17:30' to a time string in the form
# '5:30pm'.
# =============================================================================
def convert_kick_off_time_string(time_string):

    time_string = time_string.strip()

    # remove Sunday prefix, if present
    if time_string[0].upper() == 'S':
        time_string = time_string[1:]
        time_string = time_string.strip()

    am_pm_suffix = 'am'

    colon_pos = time_string.find(':')
    # get hour
    hour_string = time_string[:colon_pos]
    hours = int(hour_string)
    if hours >= 12:
        am_pm_suffix = 'pm'
    if hours > 12:
        hours -= 12
    # get minutes
    minute_string = time_string[colon_pos + 1:]
    minutes = int(minute_string)
    # rebuild time string
    converted_time_string = str(hours)
    if minutes != 0:
        converted_time_string += ':' + str(minutes)
    converted_time_string += am_pm_suffix

    return converted_time_string
# =============================================================================
main()
