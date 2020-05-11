# STEP 1
import os
import json


def create_a_json_file_containing_errors(file_name):
    json_file_name = file_name + '.json'
    os.system('flow --json > ' + json_file_name)

    return json_file_name


def convert_the_json_file_to_a_dictionary(file_to_convert):
    with open(file_to_convert) as json_file:
        converted_file = json.load(json_file)

    return converted_file


# STEP 2
def group_errors_by_file(errors):
    errors_grouped_by_file = []

    for error in errors:
        path_of_error = error['message'][0]['path']
        error_line = error['message'][0]['line']
        length_of_errors_grouped_by_file = len(errors_grouped_by_file)
        different_errors_counter = 0

        errors_grouped_by_file, different_errors_counter = compare_error_path_with_paths_of_files_with_errors(path_of_error, errors_grouped_by_file, error_line, different_errors_counter)

        error_path_is_not_in_the_list = different_errors_counter == length_of_errors_grouped_by_file

        if error_path_is_not_in_the_list:
            errors_grouped_by_file = add_new_file_with_errors_to_list(errors_grouped_by_file, path_of_error, error_line)

    return remove_duplicate_errors(errors_grouped_by_file)


def compare_error_path_with_paths_of_files_with_errors(path_of_error, errors_grouped_by_file, error_line, different_errors_counter):
    for file_with_errors in errors_grouped_by_file:
        path_of_file_with_errors = file_with_errors['path']
        paths_are_different = path_of_error != path_of_file_with_errors
        paths_are_the_same = path_of_error == path_of_file_with_errors
    
        if paths_are_different:
            different_errors_counter += 1

        if paths_are_the_same:
            file_with_errors['lines'] = update_list_of_lines_with_errors(file_with_errors['lines'], error_line)
            
    return errors_grouped_by_file, different_errors_counter


def add_new_file_with_errors_to_list(list_of_files_with_errors, file_path, error_line):
    list_of_files_with_errors = [*list_of_files_with_errors, {'path': file_path, 'lines': [error_line]}]

    return list_of_files_with_errors


def update_list_of_lines_with_errors(list_of_lines, line_to_add):
    list_of_lines = [*list_of_lines, line_to_add]

    return list_of_lines


def remove_duplicate_errors(errors_grouped_by_file):
    for file_with_errors in errors_grouped_by_file:
        list_of_lines_with_an_error_without_duplicates = remove_duplicates_from_list(file_with_errors['lines'])
        file_with_errors['lines'] = list_of_lines_with_an_error_without_duplicates

    return errors_grouped_by_file


def remove_duplicates_from_list(list_with_duplicates):
    #The list is converted into a dictionary which has only unique keys then it is converted back into a list.
    error_list_without_duplicates = list(dict.fromkeys(list_with_duplicates))

    return error_list_without_duplicates


# STEP 3
def ignore_errors_in_file(file_with_errors):
    errors_in_file_counter = 0
    list_of_lines_with_an_error = file_with_errors['lines']

    for line_with_an_error in list_of_lines_with_an_error:
        line_before_the_error = (line_with_an_error - 1) + errors_in_file_counter

        add_ignore_comments_in_file(line_before_the_error, file_with_errors)
        errors_in_file_counter += 1


def add_ignore_comments_in_file(line, file):
    ignore_comment = "//$FlowFixMe\n"

    with open(file['path'], "r+") as file_reading:
        file_contents = file_reading.readlines()
        file_contents.insert(line, ignore_comment)
        file_reading.seek(0)
        file_reading.writelines(file_contents)
        file_reading.truncate()


# MAIN FUNCTION
def ignore_errors():
    json_file_name = 'flow-logs'
    json_file_containing_errors = create_a_json_file_containing_errors(json_file_name)
    dict_containing_errors = convert_the_json_file_to_a_dictionary(json_file_containing_errors)
    errors = dict_containing_errors['errors']

    errors_grouped_by_file = group_errors_by_file(errors)

    for file_with_errors in errors_grouped_by_file:
        ignore_errors_in_file(file_with_errors)


ignore_errors()
