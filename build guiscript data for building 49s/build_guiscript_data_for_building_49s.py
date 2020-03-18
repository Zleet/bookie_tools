# ==============================================================================
# Build GUIScript data for building 49s events in the McLeans system
#
# The GUIScript data for a single day looks like this:
#
# # ============================
# 01    	# day
# 07     	# month
# 17     	# hour
# 49     	# minute
# Sun 49s # top market title
#
# Write all the guiscript data to a file named 'guiscript_49s_data.txt'
# ==============================================================================
def main():

    days = ['Wed', 'Thurs', 'Fri', 'Sat', 'Sun', 'Mon', 'Tues']
    # index month no directly, hence zero first element
    month_day_totals = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    data_template = """
# ============================
{{day_no}}     	# day
{{month_no}}     	# month
16     	# hour
49     	# minute
{{day_string}} 49s # top market title
"""

    start_month = 1
    start_day = 1

    data = ''

    for current_month in range(start_month, 13):
        days_in_current_month = month_day_totals[current_month]
        for day_no in range(1, days_in_current_month + 1):
            day_data = data_template
            # add day_no
            day_no = str(day_no)
            if len(day_no) < 2:
                day_no = '0' + day_no
            day_data = day_data.replace('{{day_no}}', day_no)
            # add month_no
            month_no = str(current_month)
            if len(month_no) < 2:
                month_no = '0' + month_no
            day_data = day_data.replace('{{month_no}}', month_no)
            # add day_string
            total_days_elapsed = 0
            for day_calc_month in range(start_month, current_month):
                days_in_day_calc_month = month_day_totals[day_calc_month]
                total_days_elapsed += days_in_day_calc_month
            total_days_elapsed += int(day_no)
            day_string_index = (total_days_elapsed - 1) % 7 # changed
            day_string = days[day_string_index]
            day_data = day_data.replace('{{day_string}}', day_string)
            # add day_data to data
            data += day_data.strip() + "\n"

    # write data to outfile
    outfile = open('guiscript_49s_data.txt', 'w')
    outfile.write(data)
    outfile.close()

    print('***** RUN COMPLETE *****')

    return
# ==============================================================================
main()
