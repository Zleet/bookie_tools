import math
# ==============================================================================
# Build GUIScript data for Euro Millions.
# Write data to the local file "guiscript_data_for_euro_millions.txt"
# ==============================================================================
def main():

    build_guiscript_data_for_euro_millions()

    print('***** RUN COMPLETE! *****')
# ==============================================================================
# ==============================================================================
def build_guiscript_data_for_euro_millions():

    # the day number and month number for the first Wednesday from which
    # we're going to build all the Euro Millions GUIScript data for the
    # rest of the year
    FIRST_WEDNESDAY_DAY = 2
    FIRST_WEDNESDAY_MONTH = 1

    # read template
    infile = open('euro_millions_template.txt', 'r')
    template = infile.read()
    infile.close()

    month_day_totals = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # build a large list containing two item sublists in the format
    # [<day number>, <month number>]
    # e.g. [3, 5] for 3rd May
    day_and_month_pairs = []
    # loop through months
    for count in range(len(month_day_totals)):
        month_no = count + 1
        days_in_current_month = month_day_totals[count]
        # loop through days in current month
        for day_no in range(1, days_in_current_month + 1):
            day_and_month = [day_no, month_no]
            day_and_month_pairs.append(day_and_month)

    # find the index of the day and month pair that correspond to
    # [FIRST_WEDNESDAY_DAY, FIRST_WEDNESDAY_MONTH]
    truncated_day_and_month_pairs = []
    for count in range(len(day_and_month_pairs)):
        day_and_month = day_and_month_pairs[count]
        day = day_and_month[0]
        month = day_and_month[1]
        if (day == FIRST_WEDNESDAY_DAY) and (month == FIRST_WEDNESDAY_MONTH):
            truncated_day_and_month_pairs = day_and_month_pairs[count:]

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # the indices of the first day and month pair we're going to use will be 1
    # and 4. The indices of each succeeding day and month pair will take the
    # form 7n + 1 and 7n + 4
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    first_wednesday_index = 0
    last_wednesday_index = math.floor(len(truncated_day_and_month_pairs) - 2)
    # test print
    print('first_wednesday_index =', str(first_wednesday_index))
    print('last_wednesday_index =', str(last_wednesday_index))

    # build the big data string
    big_data_string = ''
    for wednesday_index in range(first_wednesday_index,
                                     last_wednesday_index + 1, 7):
        saturday_index = wednesday_index + 3
        # get Wednesday day and Wednesday month
        wednesday_day_and_month = truncated_day_and_month_pairs[wednesday_index]
        wednesday_day = str(wednesday_day_and_month[0])
        if len(wednesday_day) == 1:
            wednesday_day = '0' + wednesday_day
        wednesday_month = str(wednesday_day_and_month[1])
        if len(wednesday_month) == 1:
            wednesday_month = '0' + wednesday_month
        # get Saturday day and Saturday month
        saturday_day_and_month = truncated_day_and_month_pairs[saturday_index]
        saturday_day = str(saturday_day_and_month[0])
        if len(saturday_day) == 1:
            saturday_day = '0' + saturday_day
        saturday_month = str(saturday_day_and_month[1])
        if len(saturday_month) == 1:
            saturday_month = '0' + saturday_month
        week_string = template
        week_string = week_string.replace('{{wednesday_day_number}}',
                                              wednesday_day)
        week_string = week_string.replace('{{wednesday_month_number}}',
                                              wednesday_month)
        week_string = week_string.replace('{{saturday_day_number}}',
                                              saturday_day)
        week_string = week_string.replace('{{saturday_month_number}}',
                                              saturday_month)
        big_data_string += "\n" + week_string

    big_data_string = big_data_string.strip()

    # write big data string to outfile
    outfile = open('guiscript_data_for_euro_millions.txt', 'w')
    outfile.write(big_data_string)
    outfile.close()

    return
# ==============================================================================
# ==============================================================================
main()
