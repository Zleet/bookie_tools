        # identify date line or league title line
        if (len(elements) >= 4) and (len(elements[3].strip())):
            contains_title_or_date = 1
        # identify match line
        if len(elements) >= 5:
            if (len(elements[2].strip()) > 0) and (len(elements[4].strip()) > 0):
                contains_teams = 1
        if contains_title_or_date:
            line_dictionary = {
                    "line_type" : "date_or_league",
                    "line_text" : line.strip()
                                }
            kept_lines.append(line_dictionary)
        if contains_teams:
            line_dictionary = {
                    "line_type" : "match",
                    "line_text" : line.strip()
                                }
            kept_lines.append(line_dictionary)
