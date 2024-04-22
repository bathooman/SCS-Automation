import argparse
import os
import requests
import sys


def get_registered_users(course_id, num_of_elements, token):
    headers = {'Authorization': 'Bearer ' + str(token)}
    parameters = dict()
    parameters["per_page"] = num_of_elements
    url = f"https://uppsala.instructure.com:443/api/v1/courses/{course_id}/enrollments"
    response = requests.get(url, headers=headers, params=parameters)
    json_response = response.json()
    latest_json_response = json_response

    while True:
        new_response = requests.get(response.links.get('next')['url'], headers=headers, params=parameters)
        if new_response.json() == latest_json_response:
            break
        else:
            json_response.extend(new_response.json())
            latest_json_response = new_response.json()

    num = 0
    users = []
    for user in json_response:
        if user['role'] == "Student registrerad":
            temp = str(user['user']['name']).replace(" ", "").lower()
            temp = temp.replace("ö", "o")
            temp = temp.replace("ä", "a")
            temp = temp.replace("å", "a")
            temp = temp.replace("é", "e")
            temp = temp.replace("ü", "u")
            temp = temp.replace("ó", "o")
            users.append(temp)
            num += 1
    return num, users


def write_to_file(file_name, arr_to_write):
    f = open(file_name, "a")
    for elem in arr_to_write:
        f.write(str(elem) + "\n")
    f.close()


def get_arguments():
    token = ""
    arg_parser = argparse.ArgumentParser(description="The program gets the registered users for a course and logs them"
                                                     " in a file.")
    arg_parser.add_argument("-c", "--course_id", type=int, required=True, help="The ID associated with the"
                                                                               " course in Canvas")
    arg_parser.add_argument("-t", "--token_path", type=str, required=True, help="The address to the file"
                                                                                " containing the token for Canvas")
    arg_parser.add_argument("-o", "--output_file", type=str, required=True, help="The name for the output file "
                                                                                 "containing the name of students")
    args = arg_parser.parse_args()

    if not (os.path.isfile(args.token_path)):
        print("Invalid path for the token file")
        sys.exit(2)

    with open(os.path.abspath(args.token_path)) as f:
        token = f.readline().strip()

    return args.course_id, token, args.output_file


def main():
    course_id, token, output_file_name = get_arguments()
    num, users = get_registered_users(course_id, 500, token)
    print(f"Number of registered students: {num}")
    write_to_file(output_file_name, users)


if __name__ == '__main__':
    main()
