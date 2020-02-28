def get_schema(tag):
    schema = ''
    schema_char_type = ''
    g_tag = []

    for char in tag:
        if char.isalpha():
            if not schema_char_type == "W":
                schema_char_type = "W"
                schema += schema_char_type
                g_tag.append(char)
            else:
                g_tag[len(g_tag) - 1] += char

        if char.isnumeric():
            schema_char_type = "N"
            schema += schema_char_type
            g_tag.append(char)

        if not char.isalnum():
            schema_char_type = char  # record delineator schema_char_type
            schema += schema_char_type
            g_tag.append(char)

    return schema, g_tag


def read_in_data(data_loc, line_str):
    record_list = line_str.rsplit(',')
    return record_list[data_loc]
