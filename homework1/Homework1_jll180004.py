# HW1
# Jackie Le
# NetID: jll180004

import sys
import re
import pickle
import pathlib


# Person class
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Name:", self.last, self.first, self.mi)
        print("ID:", self.id)
        print("Phone", self.phone)


# function to process input file
def process_lines(employeeData):
    # dictionary for storing employee data
    employees = {}
    for line in employeeData:
        data = line.strip().split(',')
        data[0] = data[0].capitalize()
        data[1] = data[1].capitalize()

        # middle initial should be capitalized, if no middle initial, mark as X
        if data[2] == "":
            data[2] = "X"
        else:
            data[2] = data[2].upper()

        # process id - correct format is 2 letters followed by 4 digit
        # prompt user until valid ID is input
        validID = False
        while not validID:
            if re.match(r'[a-zA-Z]{2}\d{4}', data[3]):
                if data[3] in employees:
                    print("ID already exists")
                else:
                    validID = True
            else:
                print("ID invalid: ", data[3])
                print("ID is two letters followed by 4 digits ")
                data[3] = input("Please enter a valid ID: ")

        # check if phone number is in XXX-XXX-XXXX form
        while True:
            phone_match = re.match(r'(\d{3})-(\d{3})-(\d{4})', data[4])
            if phone_match:
                data[4] = phone_match.group()
                break
            else:
                print("Phone number invalid: ", data[4])
                print("Phone number should be in XXX-XXX-XXXX form ")
                data[4] = input("Please enter a valid phone number ")

        # once employee info is processed in correct format, add to employee dict and create
        employees[data[3]] = Person(data[0], data[1], data[2], data[3], data[4])
    return employees


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please specify a filepath as a sysarg ")
        quit()

    path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(path), 'r') as f:
        text_in = f.read().splitlines()

    employees = process_lines(text_in[1:])  # text_in[1:]: individual lines in csv, skipping header

    # pickle employees dict
    pickle.dump(employees, open("employees.pickle", "wb"))

    employees_in = pickle.load(open("employees.pickle", "rb"))

    print("\n\nEmployees list: \n")
    for key in employees_in.keys():
        employees_in[key].display()
