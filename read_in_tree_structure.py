import read_csv_file
import update_csv_file
import shutil


def get_equipment_tree(file_name, loc_tagname, loc_cluster, max_count, map_schema, data_base, mode):
    search_digit = 2  # read in csv and make flat equip list with no equipment
    data_base,_ = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                            loc_cluster, max_count, map_schema, data_base, mode)

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


def get_loc_of_header_columns(file_name):
    # get header file
    header = read_first_line(file_name)

    loc_item = -1
    loc_tagname = -1
    loc_iodev = -1  # only applicable to variable csv and equip csv
    loc_project_mame = -1
    if file_name.find('equip.csv') >= 0:
        loc_equip = header.index('name')
        loc_iodev = header.index('i/o device')
    else:
        loc_equip = header.index('equipment')
        loc_item = header.index('item name')
        if file_name.find('variable.csv') >= 0:
            loc_tagname = header.index('tag name')
            loc_iodev = header.index('i/o device')
        elif file_name.find('trend.csv') >= 0:
            loc_tagname = header.index('tag name')
        elif file_name.find('spc.csv') >= 0:
            loc_tagname = header.index('spc tag name')
        elif file_name.find('accums.csv') >= 0:
            loc_tagname = header.index('name')
        else:
            loc_tagname = header.index('alarm tag')

    loc_cluster = header.index('cluster name')
    loc_project_name = header.index('project')
    return loc_equip, loc_item, loc_tagname, loc_cluster, loc_iodev, loc_project_name


def update_tag_csvs(map_schema, area_map, file_path, equipment_map_dict):
    file_list = get_file_paths(file_path)
    equip_list = dict()

    for file_name in file_list:
        if not file_name.find('equip.csv') >= 0:  # skip equipment file
            loc_equip, loc_item, loc_tagname, loc_cluster, loc_iodev, loc_project_name = \
                get_loc_of_header_columns(file_name)
            equip_list = update_csv_file.update_csv(map_schema, area_map, loc_equip, loc_item, loc_tagname,
                                                    loc_cluster, loc_iodev, loc_project_name, file_name,
                                                    equip_list, equipment_map_dict)

    return equip_list


def update_equipment_csv(file_path, equip_list):
    file_list = get_file_paths(file_path)

    for file_name in file_list:
        if file_name.find('equip.csv') >= 0:
            loc_equip, _, _, loc_cluster, loc_iodev, loc_project_name = get_loc_of_header_columns(file_name)
            update_csv_file.update_equipment_csv(
                loc_equip, loc_cluster, loc_iodev, loc_project_name, file_name, equip_list)


def replace_original_csv(file_path):
    file_list = get_file_paths(file_path)
    for file_name in file_list:
        scratch_file = file_name.replace('.csv', '-working.csv')
        backup_file = file_name.replace('.csv', '.bak')

        # copy .csv to .bak
        shutil.move(file_name, backup_file)
        # copy scratch file to .csv
        shutil.move(scratch_file, file_name)
