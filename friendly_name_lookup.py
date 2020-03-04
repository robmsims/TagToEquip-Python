def build_field_friendly_name_lookup(file_path):
    root_file_path = file_path[0:file_path.rfind('\\', 2)]
    citect_ini_file_path = root_file_path + '\\citect.ini'

    dbf_csv_lookup_dict = dict()
    dbf_csv_lookup_dict['variable.dbf'] = dict()
    dbf_csv_lookup_dict['variable.dbf']['name'] = 'Tag Name'
    dbf_csv_lookup_dict['variable.dbf']['equip'] = 'Equipment'
    dbf_csv_lookup_dict['variable.dbf']['item'] = 'Item Name'
    dbf_csv_lookup_dict['variable.dbf']['unit'] = 'I/O Device'
    dbf_csv_lookup_dict['variable.dbf']['cluster'] = 'Cluster Name'

    dbf_csv_lookup_dict['trend.dbf'] = dbf_csv_lookup_dict['variable.dbf']

    dbf_csv_lookup_dict['spc.dbf'] = dict()
    dbf_csv_lookup_dict['spc.dbf']['equip'] = 'Equipment'
    dbf_csv_lookup_dict['spc.dbf']['item'] = 'Item Name'
    dbf_csv_lookup_dict['spc.dbf']['name'] = 'Spc Tag Name'
    dbf_csv_lookup_dict['spc.dbf']['cluster'] = 'Cluster Name'

    dbf_csv_lookup_dict['accums.dbf'] = dict()
    dbf_csv_lookup_dict['accums.dbf']['equip'] = 'Equipment'
    dbf_csv_lookup_dict['accums.dbf']['item'] = 'Item Name'
    dbf_csv_lookup_dict['accums.dbf']['name'] = 'Name'
    dbf_csv_lookup_dict['accums.dbf']['cluster'] = 'Cluster Name'

    dbf_csv_lookup_dict['advalm.dbf'] = dbf_csv_lookup_dict['accums.dbf']
    dbf_csv_lookup_dict['advalm.dbf']['tag'] = 'Alarm Tag'

    dbf_csv_lookup_dict['anaalm.dbf'] = dbf_csv_lookup_dict['advalm.dbf']

    dbf_csv_lookup_dict['argdig.dbf'] = dbf_csv_lookup_dict['advalm.dbf']

    dbf_csv_lookup_dict['digalm.dbf'] = dbf_csv_lookup_dict['advalm.dbf']

    dbf_csv_lookup_dict['hresalm.dbf'] = dbf_csv_lookup_dict['advalm.dbf']

    dbf_csv_lookup_dict['tsana.dbf'] = dbf_csv_lookup_dict['advalm.dbf']

    dbf_csv_lookup_dict['tsdig.dbf'] = dbf_csv_lookup_dict['advalm.dbf']

    dbf_csv_lookup_dict['equip.dbf'] = dbf_csv_lookup_dict['advalm.dbf']
    dbf_csv_lookup_dict['equip.dbf']['iodevice'] = 'I/O Device'

    return dbf_csv_lookup_dict


def get_table_friendly_names(dbf_file_name, dbf_header_list, dbf_csv_lookup_dict):
    csv_header_list = list()
    for field in dbf_header_list:
        column = ''
        if dbf_file_name in dbf_csv_lookup_dict:
            if field in dbf_csv_lookup_dict[dbf_file_name]:
                column = dbf_csv_lookup_dict[dbf_file_name][field]

        if column == '':
            column = field.upper()

        csv_header_list.append(column)

    return csv_header_list
