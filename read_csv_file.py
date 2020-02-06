

def get_schema(tag, g_tag):
    schema = ''
    type = ''
    g_tag = []

    for chr in tag:
        if chr == "\"":
            continue

        # print('character {}'.format(chr)) - for debugging
        if chr.isalpha():
            if not type == "W":
                type = "W"
                schema = schema + type
                g_tag.append(chr)
            else:
                g_tag[len(g_tag ) -1] = g_tag[len(g_tag ) -1] + chr

        if chr.isnumeric():
            type = "N"
            schema = schema + type
            g_tag.append(chr)

        if not chr.isalnum():
            type = chr # record delineator type
            schema = schema + type
            g_tag.append(chr)

    # print('g_tag = {}'.format(g_tag)) - for debugging
    return schema


def read_in_data(data_loc, line_str):
    record_list = line_str.rsplit(',')
    return record_list[data_loc]