import tag_utils


def find_num_of_areas_used(data_base, tag_part, count_area):
    equip_count = 0
    matrix = data_base[1]
    equip_matrix = data_base[3]
    equip_type_total = len(equip_matrix)  # number of equipment types
    for index in range(equip_type_total):
        if index not in matrix:
            continue

        if tag_part not in matrix[index]:
            continue

        if count_area in matrix[index][tag_part]:
            equip_count += 1

    return equip_count


def get_highest_count_of_stored_tree_part(tag_part, index, data_base):
    dict_matrix = data_base[1][index][tag_part]  # matrix
    count_area = 0
    count = 0
    for c_a, c in dict_matrix.items():
        if c > count:
            count = c
            count_area = c_a

    return count, count_area


def add_highest_count_of_stored_tree_parts(tag_part, data_base, score_total_prev, current_filter, schema, mode):
    score_total = 0
    score_total_count = 0
    score_total_num_stored = 0
    score_total_num_of_areas_used = 0

    matrix = data_base[1]
    equip_type_count_matrix = data_base[2]

    matrix0 = data_base[0]
    if not tag_utils.is_tag_part_used(tag_part, schema, matrix0, mode):
        equip_matrix = data_base[3]
        equip_type_total = len(equip_matrix)  # number of equipment types
        for index in range(equip_type_total):
            if index not in matrix:
                continue

            if tag_part not in matrix[index]:
                continue

            num_tree = len(matrix[index][tag_part])  # number of tree branches
            if num_tree > 0:
                count, count_area = get_highest_count_of_stored_tree_part(tag_part, index, data_base)
                if score_total_prev < count and score_total < count:  # optimization
                    num_stored = equip_type_count_matrix[index]
                    percent = count / num_stored
                    if percent >= current_filter / 100:
                        num_of_areas_used = find_num_of_areas_used(data_base, tag_part, count_area)
                        score = percent * count / num_of_areas_used
                        if score_total < score:
                            score_total = score
                            score_total_count = count
                            score_total_num_stored = num_stored
                            score_total_num_of_areas_used = num_of_areas_used

    return score_total, score_total_count, score_total_num_stored, score_total_num_of_areas_used


def filter_equipment(data_base, tag_part, percent_filter):
    matrix = data_base[1]
    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]
    equip_type_total = len(equip_matrix)  # number of equipment types
    for index in range(equip_type_total):
        if index not in matrix:
            continue

        if tag_part not in matrix[index]:
            continue

        num_tree = len(matrix[index][tag_part])  # number of tree branches
        if num_tree > 0:
            count, count_area = get_highest_count_of_stored_tree_part(tag_part, index, data_base)
            num_stored = equip_type_count_matrix[index]
            percent = count / num_stored
            if percent >= percent_filter / 100:
                equip_matrix[index] += "." + count_area
            else:
                equip_matrix[index] = ""

    return data_base
