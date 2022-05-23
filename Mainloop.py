import os
import sys
from columnar import columnar
import json
import time
from cmd import Cmd
from time import sleep
from tqdm import tqdm


class Item:

    def __init__(self, id_num, type, location, status):
        self.id_num = id_num
        self.status = status
        self.location = location
        self.type = type

    @classmethod
    def add(cls, id_num, type, location, status):
        return cls(id_num, type, location, status)


class MyPrompt(Cmd):
    item_list = []
    prompt = "\n \\\\Root\\ >  "
    intro = "- - - - - - - - - - - - - - - - - - - - - - -\n\TERMINAL 05 0.47\n- - - - - - - - - - - - - - - - - - - " \
            "- - - -\nPress [EXIT] to exit\nType 'HELP' to get help using the terminal.\nType 'COMMANDS' to get a " \
            "list of all available commands. "
    try:
        metadata = json.load(open("database_items.json"))
        for k, v in metadata.items():
            item_list.append(Item(v['id'], v['type'], v['zone'], v['status']))

    except Exception as e:
        print(f"\n{e}\n\n")
        print("\n- - - - - - - - - - - - - - - - - - - - - - -")
        sys.exit()

    def do_clear(self, inp):
        os.system("cls")

    def do_exit(self, inp):
        print("\n- - - - - - - - - - - - - - - - - - - - - - -")
        return True

    def do_query(self, inp):
        queried = inp
        found = False
        target = None
        for i in tqdm(range(len(MyPrompt.item_list))):
            sleep(0.04)
            if str(queried).upper() == str(MyPrompt.item_list[i].id_num).upper():
                found = True
                target = MyPrompt.item_list[i]

        if found:
            id = str(target.id_num)
            status = str(target.status)
            zone = str(target.location)
            print("\n- - - - - - - - - - - - - - - - - - - - - - -")
            print("SECURITY CLEARANCE")
            print("- - - - - - - - - - - - - - - - - - - - - - -")
            time.sleep(0.3)
            print(f"ID:           {id.upper()}")
            print(f"ITEM STATUS:  {status.upper()}")
            print(f"ZONE:         {zone.upper()}")
            time.sleep(0.2)
        else:
            print(f"\nQUERY ERROR: Item not found in floor plan with {queried} designation.")

    def do_list(self, inp):
        switch = inp.upper()
        zone_no = switch[-2:]
        headers = ['ID', 'OBJECT_TYPE', 'STATUS']
        if 'ZONE' in switch:
            data = []
            if MyPrompt.item_list:
                for i in tqdm(range(len(MyPrompt.item_list))):
                    sleep(0.04)
                    if str(MyPrompt.item_list[i].location) == str(zone_no):
                        data.append([MyPrompt.item_list[i].id_num.upper(),
                                     MyPrompt.item_list[i].type.upper(),
                                     MyPrompt.item_list[i].status.upper()])
            if data:
                print(f"\nListing filtered floor inventory using filter: {switch}")
                print(columnar(data, headers, no_borders=True))
            else:
                print(f"\nLIST ERROR: No zone in floor plan with {switch} designation.")

        elif ("RESOURCE" in switch) or ("KEY" in switch) or ("ITEM" in switch):
            data = []
            if MyPrompt.item_list:
                for i in tqdm(range(len(MyPrompt.item_list))):
                    sleep(0.04)
                    if str(MyPrompt.item_list[i].type).upper() == str(switch):
                        data.append([MyPrompt.item_list[i].id_num.upper(),
                                     MyPrompt.item_list[i].type.upper(),
                                     MyPrompt.item_list[i].status.upper()])
            if data:
                print(f"\nListing filtered floor inventory using filter: {switch}, Progress : 100%\n ")
                print(columnar(data, headers, no_borders=True))
            else:
                print(f"\nLIST ERROR: No zone in floor plan with {switch} designation.")

        else:
            data = []
            if MyPrompt.item_list:
                for i in tqdm(range(len(MyPrompt.item_list))):
                    sleep(0.04)
                    data.append([MyPrompt.item_list[i].id_num.upper(),
                                 MyPrompt.item_list[i].type.upper(),
                                 MyPrompt.item_list[i].status.upper()])
            if data:
                print(f"\nListing filtered floor inventory using filter: {switch}")
                print(columnar(data, headers, no_borders=True))
            else:
                print(f"\nLIST ERROR: No zone in floor plan with {switch} designation.")

    def do_commands(self, inp):
        print("\nAvailable Commands:")
        print("\nHELP\t\t\t\tShow the documented commands")
        print("\nPING\t\t\t\tTries to ping an item inside the CURRENT security zone to get its location")
        print("\nLIST\t\t\t\tShow the full floor inventory, displaying all essential equipment available on the floor")
        print("\nQUERY\t\t\t\tQuery for detailed information about an object in the floor inventory")

    def do_new(self, inp):
        print("- - - - - - - - - - - - - - - - - - - - - - -\n")
        time.sleep(0.8)
        id_num = input('ID > ')
        type = input('TYPE > ').upper()
        locationNum = input('ZONE NUM > ').upper()
        status = input('STATUS > ').upper()
        print("- - - - - - - - - - - - - - - - - - - - - - -\n")

        MyPrompt.item_list.append(Item.add(id_num, type, locationNum, status))
        print("Established. Item Saved: progress COMPLETE")

    def help_new(self):
        print("\nCreate a new item to be added into the inventory.\n")

    def help_list(self):
        print("Shows a list of items.")

    def help_query(self):
        print("Shows item information.")

    def help_ping(self):
        print("Pinpoints the location of an Item.")

    def help_exit(self):
        print('Exit the application. Shorthand: x q Ctrl-D.')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print(f"'{inp}' is not a recognized command.")

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    MyPrompt().cmdloop()
