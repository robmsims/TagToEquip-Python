import read_in_tree_structure


def build_field_friendly_name_lookup(file_path):
    root_file_path = file_path[0:file_path.rfind('\\')]
    root_file_path = file_path[0:root_file_path.rfind('\\')]
    citect_ini_file_path = root_file_path + '\\config\\citect.ini'  # this assumes standard project position
    file_list = read_in_tree_structure.get_file_list()

    with open(citect_ini_file_path, mode='rt', encoding='utf-8') as f:
        for read_line in f:
            if 'BIN=' in read_line:
                break

    citect_frm_path = read_line[4:].rstrip('\n') + '\\citect.frm'
    citect_frm_extensions_path = read_line[4:].rstrip('\n') + '\\CitectFrmExtensions.xml'

    dbf_csv_lookup_dict = dict()
    with open(citect_frm_extensions_path, mode='rt', encoding='utf-8') as frmext:
        for read_line in frmext:
            if '<Entity' in read_line:
                ref = read_line[read_line.find('"') + 1:]
                ref = ref[0:ref.find('"')]
                ref_csv = ref + '.csv'
                ref_dbf = ref + '.dbf'
                if ref_csv in file_list:
                    dbf_csv_lookup_dict[ref_dbf] = dict()
                    for read_field in frmext:
                        if '<Field name' in read_field:
                            dbf_field = read_field[read_field.find('"') + 1:]
                            dbf_field = dbf_field[0:dbf_field.find('"')]
                            if dbf_field == 'PROJECTNAME':
                                dbf_csv_lookup_dict[ref_dbf][dbf_field] = 'Project'
                            else:
                                dbf_csv_lookup_dict[ref_dbf][dbf_field] = ''

                        if 'Entity' in read_field:
                            break

    with open(citect_frm_path, mode='rt', encoding='utf-8') as frm:
        for read_line in frm:
            if read_line.find('FORM') == 0:
                line = read_line.rsplit(',')
                ref_dbf = line[2].strip().replace('"', '') + '.dbf'
                if ref_dbf in dbf_csv_lookup_dict:
                    line = line
                    for read_field in frm:
                        if read_field.find('NORMAL') == 0:
                            break

                        if ':' in read_field:
                            number = read_field[0:read_field.find(':')]
                            field = read_field[read_field.find('"') + 1:]
                            field = field[0:field.find('"')]

                            if field not in dbf_csv_lookup_dict[ref_dbf]:
                                dbf_csv_lookup_dict[ref_dbf][field] = field
                            else:
                                dbf_csv_lookup_dict[ref_dbf][field] = number

                    for read_friendly_field in frm:
                        if read_friendly_field.find('PRINT') == 0:
                            break

                        friendly_field_list = read_friendly_field.rsplit('}')
                        for friendly_field in friendly_field_list:
                            pos = friendly_field.find('{')
                            if pos > 0:
                                number = friendly_field[pos + 1:].strip()
                                friendly_name = friendly_field[0:pos].strip().strip('"')
                                for field in dbf_csv_lookup_dict[ref_dbf]:
                                    if dbf_csv_lookup_dict[ref_dbf][field] == number:
                                        if not friendly_name == '':
                                            dbf_csv_lookup_dict[ref_dbf][field] = friendly_name
                                        else:
                                            if field == 'ALMSTAT0':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger 000'
                                            elif field == 'ALMSTAT1':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger 00A'
                                            elif field == 'ALMSTAT2':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger 0B0'
                                            elif field == 'ALMSTAT3':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger 0BA'
                                            elif field == 'ALMSTAT4':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger C00'
                                            elif field == 'ALMSTAT5':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger C0A'
                                            elif field == 'ALMSTAT6':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger CB0'
                                            elif field == 'ALMSTAT7':
                                                dbf_csv_lookup_dict[ref_dbf][field] = 'Trigger CBA'
                                            else:
                                                dbf_csv_lookup_dict[ref_dbf][field] ='unknown key:' + field

    return dbf_csv_lookup_dict


def get_table_friendly_names(dbf_file_name, dbf_csv_lookup_dict):
    csv_header_list = list()
    dbf_header_name = list()
    for field in dbf_csv_lookup_dict[dbf_file_name]:
        column = ''
        if dbf_file_name in dbf_csv_lookup_dict:
            if field in dbf_csv_lookup_dict[dbf_file_name]:
                column = dbf_csv_lookup_dict[dbf_file_name][field]

        if column == '':
            column = field.upper()

        csv_header_list.append(column)
        dbf_header_name.append(field)

    return csv_header_list, dbf_header_name
