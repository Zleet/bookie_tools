# ==============================================================================
# Script to build the GUIScript data to build Daily Millions events
# ==============================================================================
def main():

    build_guiscript_data_for_daily_millions()

    print('***** RUN COMPLETE! *****')

    return
# ==============================================================================
# ==============================================================================
def build_guiscript_data_for_daily_millions():

    # read template for single day data
    infile = open('day_data_template.txt', 'r')
    day_template = infile.read()
    infile.close()

    # total days in months
    month_day_totals = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # day strings
    day_strings = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

    # set month range and initial day
    start_month = 1
    end_month = 12
    start_day_string = "Wed"

    # build output data here
    data = ''

    for current_month in range(start_month, end_month + 1):
        # get total days in current month
        total_days_in_current_month = month_day_totals[current_month - 1]
        # loop through days in month
        for current_day in range(1, total_days_in_current_month + 1):
            # get current day string by firstly calculating the total
            # number of days that have elapsed since the start of the
            # first month
            total_elapsed_days = 0
            # loop through all the months before the current month and
            # add their total days to total_elapsed_days
            for earlier_month in range(start_month - 1, current_month - 1):
                total_elapsed_days += month_day_totals[earlier_month]
            # add current_day to total_elapsed_days
            total_elapsed_days += current_day
            start_day_string_index = day_strings.index(start_day_string)
            # work out current day string
            current_day_string = day_strings[
                    (total_elapsed_days + start_day_string_index - 1) % 7]
            # test print
            # print()
            # print('total_elapsed_days =', total_elapsed_days)
            # print('month =', current_month, ', day =', current_day,
            #           ', current_day_string =', current_day_string)
            # get day template, populate it
            day_data = day_template
            # populate day template with day integer
            day_integer_string = str(current_day)
            if len(day_integer_string) == 1:
                day_integer_string = '0' + day_integer_string
            day_data = day_data.replace(
                                '{{day_integer}}', day_integer_string)
            # populate day template with month integer
            month_integer_string = str(current_month)
            if len(month_integer_string) == 1:
                month_integer_string = '0' + month_integer_string
            day_data = day_data.replace(
                                '{{month_integer}}', month_integer_string)
            # populate day template with day string
            day_data = day_data.replace('{{day_name}}', current_day_string)
            # append day data to data
            data += day_data

    # write data to outfile
    outfile = open('guiscript_data.txt', 'w')
    outfile.write(data)
    outfile.close()

    return
# ==============================================================================
# ==============================================================================
# ==============================================================================
main()
