import read_csv_file
import encode_decode_map_schema


def get_equipment_tree(file_name, loc_tagname, loc_cluster, max_count, map_schema):
    matrix0, mode, schema = encode_decode_map_schema.decode_mapping_schema(map_schema)
    data_base = []
    data_base.append(matrix0)
    data_base.append(dict())  # matrix - use for equipment tree
    data_base.append(list())  # equip_type_count_matrix - dummy place marker
    data_base.append(list())  # equip_matrix - dummy place marker

    search_digit = 2  # read in csv and make flat equip list with no equipment
    data_base,_ = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                            loc_cluster, max_count, schema,data_base, mode)

    return data_base


def read_first_line(file_name):
    with open(file_name, mode='rt', encoding='utf-8') as f:
        return f.readline().strip().lower().rsplit(',')


def get_file_paths(file_path):
    equipmnt_file_name = file_path + "\\equip.csv"
    variables_file_name = file_path + "\\variable.csv"
    trends_file_name = file_path + "\\trend.csv"
    spc_file_name = file_path + "\\spc.csv"
    accums_file_name = file_path + "\\accums.csv"

    advalm_file_name = file_path + "\\advalm.csv"
    anaalm_file_name = file_path + "\\anaalm.csv"
    argdig_file_name = file_path + "\\argdig.csv"
    digalm_file_name = file_path + "\\digalm.csv"
    hresalm_file_name = file_path + "\\hresalm.csv"
    tsana_file_name = file_path + "\\tsana.csv"
    tsdig_file_name = file_path + "\\tsdig.csv"

    return [equipmnt_file_name, variables_file_name, trends_file_name, spc_file_name, accums_file_name,
            advalm_file_name, anaalm_file_name, argdig_file_name, digalm_file_name,
            hresalm_file_name, tsana_file_name, tsdig_file_name]


def update_equipment_csv(map_schema, area_map, equipment_map_list, file_path):
    file_list = get_file_paths(file_path)

    for file_name in file_list:
        # get header file
        header = read_first_line(file_name)
        print(header)

        loc_equip = header.index('equipment')
        loc_item = header.index('item name')
        loc_cluster = header.index('cluster name')
        print('Equipment loation {}'.format(loc_equip))
        print('Equipment Item location {}'.format(loc_item))
        print('Equipment Cluster {}'.format(loc_cluster))
