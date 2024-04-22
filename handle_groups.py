import argparse
import os
import requests
import sys


def get_arguments():
    token = ""
    arg_parser = argparse.ArgumentParser(description="The program gets the group members for a course and logs them"
                                                     " in a file.")
    arg_parser.add_argument("-c", "--course_id", type=int, required=True, help="The ID associated with the"
                                                                               " course in Canvas")
    arg_parser.add_argument("-t", "--token_path", type=str, required=True, help="The address to the file"
                                                                                " containing the token for Canvas")
    arg_parser.add_argument("-o", "--output_file", type=str, required=True, help="The name for the output file "
                                                                                 "containing the name of the group "
                                                                                 "members")
    args = arg_parser.parse_args()

    if not (os.path.isfile(args.token_path)):
        print("Invalid path for the token file")
        sys.exit(2)

    with open(os.path.abspath(args.token_path)) as f:
        token = f.readline().strip()

    return args.course_id, token, args.output_file


def get_groups(course_id, num_of_elements, token):
    headers = {'Authorization': 'Bearer ' + str(token)}
    parameters = dict()
    parameters["per_page"] = num_of_elements
    url = f"https://uppsala.instructure.com:443/api/v1/courses/{course_id}/groups"
    response = requests.get(url, headers=headers, params=parameters)
    ans1 = response.json()
    response2 = requests.get(response.links.get('next')['url'], headers=headers, params=parameters)
    ans2 = response2.json()
    ans = ans1 + ans2
    Lab1_ids = []
    for group in ans:
        if str(group["name"]).startswith("L1"):
            Lab1_ids.append(group["id"])

    return Lab1_ids


def get_groups_members(group_ids, num_of_elements, token, outputfile_name):
    headers = {'Authorization': 'Bearer ' + str(token)}
    parameters = dict()
    parameters["per_page"] = num_of_elements
    for group_id in group_ids:
        url = f"https://uppsala.instructure.com:443/api/v1/groups/{group_id}/users"
        response = requests.get(url, headers=headers, params=parameters)
        ans = response.json()
        users = []
        users.append(group_id)
        for user in ans:
            temp = str(user['name']).replace(" ", "").lower()
            temp = temp.replace("ö", "o")
            temp = temp.replace("ä", "a")
            temp = temp.replace("å", "a")
            temp = temp.replace("é", "e")
            temp = temp.replace("ü", "u")
            temp = temp.replace("ó", "o")
            users.append(temp)
        write_to_file(outputfile_name, users)


def write_to_file(file_name, arr_to_write):
    f = open(file_name, "a")
    for elem in arr_to_write:
        f.write(str(elem) + "\n")
    f.close()

def main():
    course_id, token, output_file_name = get_arguments()
    ids = get_groups(course_id, 500, token)
    get_groups_members(ids, 500, token, output_file_name)


if __name__ == '__main__':
    main()