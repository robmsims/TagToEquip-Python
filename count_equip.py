def find_num_of_areas_used(data_base, tag_part, count_area):
    equip_count = 0
    matrix = data_base[1]
    equip_matrix = data_base[3]
    equip_type_total = len(equip_matrix) # number of equipment types
    for index in range(equip_type_total):
        if count_area in matrix[index][tag_part]:
            equip_count += 1

    return equip_count


def get_highest_count_of_stored_tree_part(tag_part, index, data_base):
    dict_matrix = data_base[1][index][tag_part] # matrix
    count_area = 0
    count = 0
    # print(dict_matrix)
    for c_a, c in dict_matrix.items():
        # print('tag part {} areas {}, count {}'.format(tag_part, areas, c))
        if c > count:
            count = c
            count_area = c_a

    return count, count_area


def add_highest_count_of_stored_tree_parts(tag_part, data_base, score_total_max, current_filter):
    score_total = 0
    matrix = data_base[1]
    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]
    equip_type_total = len(equip_matrix) # number of equipment types
    for index in range(equip_type_total):
        num_tree = len(matrix[index][tag_part]) # number of tree branches
        #print('num_tree {} equip {}'.format(num_tree, equip_matrix[index]))
        if num_tree > 0:
            count, count_area = get_highest_count_of_stored_tree_part(tag_part, index, data_base)
            if score_total_max < count * 1000: # oprimization
                num_stored = equip_type_count_matrix[index]
                percent = 1000 * count / num_stored
                if percent >= 10 * current_filter:
                    num_of_areas_used = find_num_of_areas_used(data_base, tag_part, count_area)
                    #print(num_of_areas_used)
                    score = count * percent / num_of_areas_used
                    if score_total < score:
                        score_total = score

    return score_total