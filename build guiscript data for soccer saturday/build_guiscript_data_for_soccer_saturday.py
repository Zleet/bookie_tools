# ===========================================================================
# Build the guiscript data for soccer saturday
# Reads csv and builds guiscript data text file.
#
# Data for each pair of soccer saturday markets will be output as follows:
# # HOME TEAM
# # AWAY TEAM
# yes price
# no price
# yes price
# no price
#
# e.g.
# # Liverpool
# # Man Utd
# 1/2
# 6/4
# 1/2
# 6/4
#
# with a blank line between each match
# ===========================================================================
def main():

    # read csv spreadsheet
    infile = open('soccer_saturday_csv.csv', 'r')
    lines = infile.readlines()
    infile.close()

    # remove first line (header line)
    lines = lines[1:]

    csv_text = ''

    # loop through remaining lines; for each line, extract home team,
    # away team, yes price and no price
    for line in lines:
        line = line.strip()
        elements = line.split(',')
        print(elements)
        home_team = elements[1].strip()
        away_team = elements[3].strip()
        yes_price = elements[12].strip()
        no_price  = elements[13].strip()
        # build guiscript data for current match, add it to csv_text
        csv_text += '# ' + home_team + "\n"
        csv_text += '# ' + away_team + "\n"
        csv_text += yes_price + "\n"
        csv_text += no_price + "\n"
        csv_text += yes_price + "\n"
        csv_text += no_price + "\n\n"

    # write csv_text to outfile
    outfile = open('soccer_saturday_guiscript_data.txt', 'w')
    outfile.write(csv_text)
    outfile.close()

    print()
    print('***** RUN COMPLETE *****')

    return

main()
