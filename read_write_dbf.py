import dbf
import read_in_tree_structure
import read_write_project_structure
import friendly_name_lookup


def read_in_dbf(dbf_file_name):
    dbf_list = list()

    table = dbf.Table(dbf_file_name)
    header_list = table.field_names

    table.open()
    for record in table:
        record_dict = dict()
        if not record.__repr__().find('*') == 2:  # is not deleted
            for field in header_list:
                record_dict[field] = [table.field_info(field)[1], record[field].__str__().rstrip()]  # record length to

            record_dict['include_read_in_status'] = [1, '0']  # used to track include project (only used in master dbf)
            # 0 = unread,  1 = read pending, 2 = read_complete
            dbf_list.append(record_dict)

    table.close()
    return dbf_list, header_list


def convert_dbf_to_csv_in_project_list(master_list, project_list, file_path, dbf_csv_lookup_dict):
    csv_list = read_in_tree_structure.get_file_list()
    for csv_file_name in csv_list:
        dbf_file_name = csv_file_name[0:csv_file_name.rfind('.')] + '.dbf'
        with open(file_path + '\\' + csv_file_name, mode='wt', encoding='utf-8') as sf:
            count = 0
            for project_name in project_list:
                project_path = read_write_project_structure.get_field_value(
                    master_list, project_name, 'path').rstrip('\\')
                dbf_file, dbf_header_list = read_in_dbf(project_path + '\\' + dbf_file_name)
                if count == 0:  # write header
                    count = 1
                    line = friendly_name_lookup.get_table_friendly_names(
                        dbf_file_name, dbf_header_list, dbf_csv_lookup_dict)
                    line = str(line).strip('[').strip(']').replace('\'', '').replace(', ', ',') + ',Project'

                    if len(dbf_file) > 0:
                        line += '\n'
                    sf.write(line)

                for index in range(len(dbf_file)):
                    record = dbf_file[index]
                    line = ''
                    for field in record:
                        if field == 'include_read_in_status':
                            line += '\"' + project_name + '\"'
                            if not index == len(dbf_file) - 1:
                                line += '\n'
                        else:
                            line += '\"' + record[field][1].replace('"', '""') + '\",'

                    sf.write(line)
