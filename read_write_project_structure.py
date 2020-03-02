import read_write_dbf


def get_field_value(dbf_list, project_name, field):
    dbf_project_field_value = ''
    for record in dbf_list:
        if record['name'][1] == project_name:
            dbf_project_field_value = record[field][1]
            break

    return dbf_project_field_value


def write_field_value(dbf_list, project_name, field, value):
    for record in dbf_list:
        if record['name'][1] == project_name:
            record[field][1] = value
            break

    return dbf_list


def find_name_for_path(dbf_list, file_path):
    project_name = ''
    for record in dbf_list:
        project = record['name'][1]
        project_path = record['path'][1].rstrip('\\')
        # print(project, project_path)
        if file_path == project_path:
            project_name = project
            break

    return project_name


def read_through_include_files(master_list):
    project_black_list = ['System', 'Include', 'CSV_Include', 'Library_Controls', 'Library_Equipment',
                          'SxW_Style_Include', 'Tab_Style_Include', 'SA_Include', 'SA_Library', 'SA_Controls']

    for count in range(20):  # limit to 20 levels deep
        found = 0
        for master_index in range(len(master_list)):
            project = master_list[master_index]['name'][1]
            if project not in project_black_list:
                if master_list[master_index]['include_read_in_status'][1] == 1:
                    found = 1
                    master_list[master_index]['include_read_in_status'][1] = 2
                    include_file_path = master_list[master_index]['path'][1].rstrip('\\') + '\\' + 'include.dbf'
                    include_list = read_write_dbf.read_in_dbf(include_file_path, project)
                    for include_index in range(len(include_list)):
                        project = include_list[include_index]['name'][1]
                        if project not in project_black_list:
                            if get_field_value(master_list, project, 'include_read_in_status') == 0:
                                write_field_value(master_list, project, 'include_read_in_status', 1)

        if not found:
            break

    return master_list

