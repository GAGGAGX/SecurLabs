import unittest
import unittest.mock
import os
import tempfile
import csv
from .lab_02 import data_list, loadCSV, saveCSV, addNewElement, deleteElement, updateElement

class TestStudenList(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile('w', encoding='utf-8',  newline='', delete=False)
        self.test_file_name = self.test_file.name
        self.test_file.close()
        data_list.clear()

    def tearDown(self):
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_addNewElement(self):
        input_data = ["Test student", "0631234567", "18", "example@exmp.com"]

        with unittest.mock.patch('builtins.input', side_effect=input_data):
            addNewElement()

        self.assertEqual(len(data_list), 1)
        self.assertEqual(data_list[0]['name'], "Test Student")
        self.assertEqual(data_list[0]['phone'], "0631234567")
        self.assertEqual(data_list[0]['age'], "18")
        self.assertEqual(data_list[0]['email'], "example@exmp.com")

    def test_deleteElement(self):
        data_list.append({"name": "Test student", "phone": "0631234567", "age": "18", "email": "example@exmp.com"})

        with unittest.mock.patch('builtins.input', return_value="Test student"):
            deleteElement()

        self.assertEqual(len(data_list), 0)

    def test_updateElement(self):
        data_list.append({"name": "Test student", "phone": "0631234567", "age": "18", "email": "example@exmp.com"})

        input_data = ["Test student", "Updated Student", "0660000000", "20", "example@exmp.com"]
        print(data_list[0])
        with unittest.mock.patch('builtins.input', side_effect=input_data):
            updateElement()
        
        self.assertEqual(len(data_list), 1)
        self.assertEqual(data_list[0]['name'], "Updated student")
        self.assertEqual(data_list[0]['phone'], "0660000000")
        self.assertEqual(data_list[0]['age'], "20")
        self.assertEqual(data_list[0]['email'], "example@exmp.com")

    def test_importCSV(self):
        data = [
            {"name": "Emma", "phone": "0664762726", "age": "23", "email": "example@exmp.com"},
            {"name": "Zak", "phone": "0664945504", "age": "22", "email": "example@exmp.com"}
        ]

        with open(self.test_file_name, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "age", "email"])
            writer.writeheader()
            writer.writerows(data)

        loadCSV(self.test_file_name)
        
        self.assertEqual(len(data_list), 2)
        self.assertEqual(data_list[0]['name'], "Emma")
        self.assertEqual(data_list[1]['name'], "Zak")
        self.assertEqual(data_list[0]['age'], "23")
        self.assertEqual(data_list[1]['age'], "22")

    def test_saveCSV(self):
        data_list.append({"name": "Jon", "phone": "0667283939", "age": "26", "email": "example@exmp.com"})
        saveCSV(self.test_file_name)

        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["name"], "Chris")
            self.assertEqual(rows[0]['phone'], "0667283939")
            self.assertEqual(rows[0]['age'], "26")
            self.assertEqual(rows[0]['email'], "example@exmp.com")



if __name__ == '__main__':
    unittest.main()
