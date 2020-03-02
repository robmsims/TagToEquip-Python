import dbf
import read_write_project_structure


def read_in_dbf(dbf_file_name, project):
    dbf_list = list()

    table = dbf.Table(dbf_file_name)
    table.open()

    header_list = table.field_names
    for record in table:
        record_dict = dict()
        if not record.__repr__().find('*') == 2:  # is not deleted
            for field in header_list:
                record_dict[field] = [table.field_info(field)[1], record[field].__str__().rstrip()]  # record length to

            record_dict['project'] = [240, project]  # used to track project if table split across multiple project
            record_dict['include_read_in_status'] = [1, 0]  # used to track include project (only used in master dbf)
                        # 0 = unread,  1 = read pending, 2 = read_complete

            project_name = record_dict['name'][1]

            dbf_project_field_value = read_write_project_structure.get_field_value(dbf_list, project_name, 'name')

            if not project_name == dbf_project_field_value:
                dbf_list.append(record_dict)
            else:
                print('warning duplicate found')

    table.close()
    return dbf_list
