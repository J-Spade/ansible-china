import argparse
import csv
import json
import os


JSON_OUT = "users.json"


_GROUPS_BY_ROLE = {
    "IT": [
        "Chief of IT",
        "IT Staff",
    ],
    "intel": [
        "Intelligence Deputy",
        "Intelligence Officer",
    ],
    "telecom": [
        "Telecommunications Deputy",
        "Telecommunications Officer",
    ],
    "robotics": [
        "Robotics Deputy",
        "Robotics Officer"
    ],
    "energy": [
        "Energy Deputy",
        "Energy Officer",
    ],
    "AI": [
        "Artificial Intelligence Deputy",
        "Artificial Intelligence Officer",
    ],
    "hyrdoponics": [
        "Hydroponics Deputy",
        "Hydroponics Officer",
    ],
    "HR": [
        "Human Resources Head",
        "Human Resources Representative",
    ],
    "accounting": [
        "Accountant Lead",
        "Accountant",
    ],
    "engineering": [
        "Engineer Chief",
        "Engineer"
    ],
    "research": [
        "Researcher Head",
        "Researcher"
    ],
    "logistics": [
        "Logistics Chief",
        "Logistics Head",
        "Logistics Officer",
    ],
}


def _get_role_group(role):
    for group in _GROUPS_BY_ROLE.keys():
        if role in _GROUPS_BY_ROLE[group]:
            return group
    return ""


def _convert_csv(csv_path):

    with open(csv_path, encoding="utf-8") as csvfile:
        # handle invalid first line and weird unicode characters
        if not "China" in csvfile.readline():
            csvfile.seek(0)
        fp = csvfile.tell()
        if "\ufeff" != csvfile.read(1):
            csvfile.seek(fp)

        # read in the users
        users = [
            {
                "username": row["Account Name"],
                "role_group": _get_role_group(row["Role"]),
                "password": row["Password"],
            }
            for row in csv.DictReader(csvfile)
        ]

    with open(JSON_OUT, "w") as jsonfile:
        json.dump(users, jsonfile, indent=4)


if __name__  == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=os.path.realpath)
    args = parser.parse_args()

    _convert_csv(args.csv_file)

