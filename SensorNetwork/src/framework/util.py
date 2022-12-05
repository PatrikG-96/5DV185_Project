
def copy_dict_subset(dictionary, list_of_keys):
    new_dict = {}

    for key in list_of_keys:
        new_dict[key] = dictionary[key]

    return new_dict