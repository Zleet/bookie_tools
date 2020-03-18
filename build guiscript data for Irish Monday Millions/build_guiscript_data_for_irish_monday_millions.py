# Script to build guiscript data for Irish Monday Millions, in the following
# format:
#
# ==========================
# 01     # day
# 03     # month
# 21     # hour
# 00     # minutes
# Thurs Eve Millions
#==========================
# 02     # day
# 03     # month
# 21     # hour
# 00     # minutes
# Fri Eve Millions
#==========================
#
# etc.
# ==============================================================================
def main():

    build_guiscript_data_for_irish_monday_millions()

    print('***** RUN COMPLETE *****')

    return
# ==============================================================================
def build_guiscript_data_for_irish_monday_millions():

    first_month = 1             # start with January
    last_month = 12              # end with December
    first_day_name = 'Wed'    # day_name of first day in first_month

    days_in_each_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_names = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

    day_template = """
{{day_no}}     # day
{{month_no}}     # month
21     # hour
00     # minutes
{{day_name}} Eve Millions
#==========================
"""

    file_text = ''

    for month in range(first_month, last_month + 1):
        for day_no in range(1, days_in_each_month[month - 1] + 1):
            day_text = day_template
            # add day_no
            day_no_string = str(day_no)
            if len(day_no_string) == 1:
                day_no_string = '0' + day_no_string
            day_text = day_text.replace('{{day_no}}', day_no_string)
            # add month_no
            month_no_string = str(month)
            if len(month_no_string) == 1:
                month_no_string = '0' + month_no_string
            day_text = day_text.replace('{{month_no}}', month_no_string)
            # work out day_name, add it
            days_elapsed = 0
            for count in range(first_month, month):
                days_elapsed += days_in_each_month[count - 1]
            days_elapsed += day_no
            day_name = day_names[(days_elapsed + day_names.index(first_day_name) - 1)% 7]
            day_text = day_text.replace('{{day_name}}', day_name)
            file_text += "\n" + day_text

    # clean up text
    while "\n\n" in file_text:
        file_text = file_text.replace("\n\n", "\n")
    file_text = file_text.strip()

    # write file_text to file
    outfile = open('guiscript_data.txt', 'w')
    outfile.write(file_text)
    outfile.close()

    return
# ==============================================================================
main()
