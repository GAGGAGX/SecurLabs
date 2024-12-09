import csv
import sys
import os

file_path = os.path.join(os.path.dirname(__file__), "log.csv")

data_list = []

def loadCSV(file_path):
    global data_list
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_list.append({
                    "name":row.get("name", "Unknown"), 
                    "phone":row.get("phone", "Unknown"), 
                    "age":row.get("age", "Unknown"), 
                    "email":row.get("email", "Unknown")
                    })
        print(f"Data loaded.")
    except FileNotFoundError:
        print(f"File not found. Starting with an empty list.")

def saveCSV(file_path):
    with open(file_path, "w", newline="") as file:
        fieldnames = ["name", "phone", "age", "email"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

def printAllList():
    for elem in data_list:
        print("Student name is " + elem["name"] + ",  Phone is " + elem["phone"] + ", Age is " + elem["age"] + ", Email is " + elem["email"])

def addNewElement():
    name = input("Please enter student name: ")
    phone = input("Please enter student phone: ")
    age = input("Please enter student age: ")
    email = input("Please enter student email: ")
    newItem = {"name": name, "phone": phone, "age": age, "email": email}
    insertPosition = 0
    for item in data_list:
        if name > item["name"]:
            insertPosition += 1
        else:
            break
    data_list.insert(insertPosition, newItem)
    print("New element has been added")

def deleteElement():
    name = input("Please enter name to be deleted: ")
    deletePosition = -1
    for item in data_list:
        if name == item["name"]:
            deletePosition = data_list.index(item)
            break
    if deletePosition == -1:
        print("Element was not found")
    else:
        del data_list[deletePosition]
        print(f"Element with name {name} has been deleted.")

def updateElement():
    name = input("Please enter name to be updated: ")
    insertPosition = -1
    for item in data_list:
        if name == item["name"]:
            insertPosition = data_list.index(item)
            break
    if insertPosition == -1:
        print("Name not found")
    else:
        old_element = data_list[insertPosition]
        print(f"Student name is {old_element['name']}, Phone is {old_element['phone']}, Age is {old_element['age']}, Email is {old_element['email']}")

        newname = input("Please enter student new name or skip: ") or old_element['name']
        newphone = input("Please enter student new phone or skip: ") or old_element['phone']
        newage = input("Please enter student new age or skip: ") or old_element['age']
        newemail = input("Please enter student new email or skip: ") or old_element['email']    

        updateElement = {"name": newname, "phone": newphone, "age": newage, "email": newemail}
        del data_list[insertPosition]
        updatePosition = 0
        for item in data_list:
            if newname > item["name"]:
                updatePosition += 1
        data_list.insert(updatePosition, updateElement)
        print("Element has been updated.")

def main():
    global file_path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    loadCSV(file_path)
    print(file_path)

    while True:
        choice = input("Please specify the action [ C create, U update, D delete, P print, S save, X exit and save ] ")
        match choice:
            case "C" | "c":
                print("New element will be created:")
                addNewElement()
            case "U" | "u":
                print("Existing element will be updated:")
                updateElement()
            case "D" | "d":
                print("Element will be deleted:")
                deleteElement()
            case "P" | "p":
                print("List will be printed:")
                printAllList()
            case "S" | "s":
                saveCSV(file_path)
                print("Data saved.")
            case "X" | "x":
                saveCSV(file_path)
                print("Exit. Data saved.")
                exit(0)
            case _:
                print("Wrong choice")

if __name__ == "__main__":
    main()

    