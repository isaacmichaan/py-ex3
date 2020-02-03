import json
from pymongo import MongoClient

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://isaacmichaan1:11Yossef@cluster0-gvxqb.gcp.mongodb.net/test?retryWrites=true&w=majority")
db=client.phoneBook


class PhoneBook:
    def __init__(self):
        self.__id = 0
        try:
            self.__phoneBook = list(db.test.find({}))
        except:
            self.__phoneBook = []
        #TODO: load

    def validation_for_id(self):
        self.__id += 1
        for i in self.__phoneBook:
            if i["id"] == self.__id:
                return self.validation_for_id()
        return self.__id

    def validation_for_string(self, str):
        val = input(f"{str}:\n")
        if any(char.isdigit() for char in val):
            print("Not valid str input, try again :)")
            return self.validation_for_string(str)
        return val.strip()

    def validation_for_digit(self, str):
        val = input(f"{str}:\n")
        if not val.isdigit():
            print("Not valid int input, try again :)")
            return self.validation_for_digit(str)
        return int(val)

    def add_person(self):
        self.__phoneBook.append({
            "id": self.validation_for_id(),
            "name": self.validation_for_string("name"),
            "age": self.validation_for_digit("age"),
            "location": self.validation_for_string("location"),
             "cel": self.validation_for_digit("cel"),
            "family": {}
        })

    def del_person(self):
        id = int(input(f"insert the id to delete:\n"))
        index = 0
        for i in self.__phoneBook:
            if i["id"] == id:
                del self.__phoneBook[index]
                return
            index += 1
        print("No such id")

    def update_person(self):
        id = int(input("insert the id of the person to update:\n"))
        for i in self.__phoneBook:
            if i["id"] == id:
                key = input("insert the field to update:\n")
                if key in i:
                    update = input("insert the value to update:\n")
                    i[key] = update
                    return
        print("No such field")

    def search_person(self):
        key = input("search by: id, name, age, location, tel\n")
        for i in self.__phoneBook:
            if key not in i:
                print("No such field")
                return

        val = input(f"insert the {key}:\n")
        for i in self.__phoneBook:
            if i[key] == val or i[key] == int(val):
                print(i)

    # need to fix (in case father is 1 and son is 2, than after he tries to make the 2 to become the father and 1 the son)
    # unless he removed from the family members 1 as father and 2 as son before.
    def connect(self):
        father = int(input("insert the id of father:\n"))
        while input("connect (more) son(s) - insert: yes or no:\n") == "yes":
            son = int(input("insert the id of son:\n"))
            if son == father:
                print(f"father: {father} and son: {son} can't have same name")
                stop = True
            else:
                stop = False
            for i in self.__phoneBook:
                if stop:
                    break
                if i["id"] == father:
                    for j in self.__phoneBook:
                        if j["id"] == son:
                            i["family"].update({str(son): 'son'})
                            j["family"].update({str(father): 'father'})
                            stop = True
                            break
            if not stop:
                print(f"couldn't find id for {father} or {son}")

    def print_phone_book(self):
        for item in self.__phoneBook:
            print("---------------------------")
            for key, value in item.items():
                print(key, value)

    def save(self):
        db.test.delete_many({})
        db.test.insert_many(self.__phoneBook)

    def menu(self):
        options = {
            '1': self.add_person,
            '2': self.search_person,
            '3': self.del_person,
            '4': self.update_person,
            '5': self.connect,
            '6': self.print_phone_book,
            '7': self.save
        }
        while True:
            print("Phone Book Menu: \n1)add\n2)search\n3)delete\n4)update\n5)connect\n6)print\n7)save")
            opt = input("Option: ")
            try:
                options[opt]()
                if opt == '7':
                    break
            except TypeError as e:
                print("[-] TypeError: ", e)
                break
            except KeyError as e:
                print("[-] KeyError: ", e)
                break


if __name__ == '__main__':
    a = PhoneBook()
    a.menu()