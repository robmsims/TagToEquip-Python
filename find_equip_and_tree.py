import read_csv_file

def read_first_line(file_name):
    with open(file_name, mode='rt', encoding='utf-8') as f:
        return f.readline().strip().lower().rsplit(',')


def read_in_schema(file_name, loc_tagname, max_count):
    data_block = []
    with open(file_name, mode='rt', encoding='utf-8') as f:
        read_count = 0
        for read_line in f:
            if read_count > 0:
                tag = read_csv_file.read_in_data(loc_tagname, read_line.strip())
                # g_tag not used here but required by function get_schema
                current_schema, g_tag = read_csv_file.get_schema(tag)
                data_block.append(current_schema)

            read_count += 1
            if read_count > max_count:
                break

    last_schema = ''
    top_count = 0
    data_block.sort()
    for current_schema in data_block:
        if not last_schema == current_schema:
            count = 0 # reset count on change of schema

        last_schema = current_schema
        count += 1
        if count > top_count:
            top_count = count
            schema = current_schema

    return schema


def find_equip_type_position_and_import_data(file_name, loc_tagname, max_count, schema):
    count = 0
    for chr in schema:
        if chr == "W":
            count += 1

    matrix0 = []
    matrix = []
    equip_type_count_matrix = []
    equip_matrix = []
    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]

    mode = -1 # switch to record equipment
    search_digit = 0

    Percent_Filter = 92
    #count = 1
    for equip_postion in range(1,count+1):
        data_base = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                    max_count, schema,
                                                    equip_postion, data_base, mode)

        # print('equip count = {}'.format(data_base[2][0])) # position 0 equip
        # print('eqpipment {}, count {}'.format(data_base[1][0], data_base[0][0]))

    return
