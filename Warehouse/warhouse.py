from menu import print_menu
from item import Item
import pickle
import datetime
import os
"""
Program: Warhouse inventory control system
Functionality:
    -Register new items
        id(auto generated)
        title
        category
        price
        stock
    -print all the items

    -print different categories
    -print stock value sum(price * stock)
    -register purchase
    -register sale

    -log of events  
    
        time | action | itemid
        1 - generate log string inside important function
        2 - add that string to logs array
        3 - save logs array
        4 - load logs array when system starts

"""
logs = []
items = []
id_count = 1
items_file = "item.data"
logs_file = "logs.data"
def clear():
    return os.system("cls")





def get_time():
    current_date = datetime.datetime.now()
    time = current_date.strftime("%X on %a-%b-%y")
    return time

def log_event(): 
    writer = open(logs_file, "wb")
    pickle.dump(logs, writer)
    writer.close()



def read_items():
    global id_count #import variable into fn scope
    try:
        reader = open(items_file,"rb") # rb = read binary
        temp_list = pickle.load(reader) #read the binary and convery it the the original object

        for item in temp_list:
            items.append(item)
        last = items[-1]
        id_count = last.id + 1
        print("Loaded " + str(len(temp_list)) + " items")
    except:
        #you get here if try block crashes
        print("Error: Data could not be loaded!")


def save_items():
    # open creates/opens a file
    writer = open(items_file, "wb") #wb = write binary info
    pickle.dump(items, writer) # pickle.dump converts the object into binary and writes it on the file
    writer.close() #closes the file stream (to release the file
    print("Data saved!")
    log_event()

def print_header(text):
    print("\n\n")
    print("*" * 40)
    print((" "*10)+text)
    print("*"*40)
def print_stock_value():
    clear()
    print_header("Overall Stock Value: ")
    total = 0.0
    for item in items:
        total += (item.price * item.stock)
    print("Total Stock Value: " + str(total))
    input("\n Press Enter To Return To Main Menu...")
def read_log():
    try:
        reader = open(logs_file, "rb")
        temp_list = pickle.load(reader)
        
        for item in temp_list:
            logs.append(item)
            print("Loaded " + str(len(temp_list)) + " items")
    except:
        print("Error: data could not be located!")

def list_log():
    clear()
    print_header("LIST OF LOGS")
    print("TIME  | ACTION   |  ID")
    for item in logs:
        print("\n" + str(item))
    input("\n Press Enter To Return To Main Menu...")

def list_item(header_text):
        clear()
        print_header(header_text)
        print("ID  | Title                     | Category        | Price    | Stock ")
        for item in items:
            print(str(item.id).ljust(3)+ " | " +item.title.ljust(25) + " | " + item.category.ljust(15) + " | " +str(item.price).ljust(8)+ " | " +str(item.stock).ljust(6))
       
def remove_item():
    clear()
    print_header("REMOVE AN ITEM FROM STOCK")
    list_item("Choose an Item from the list to remove: ")
    id = input("\n Select an ID to remove: ")
    
    for item in items:
        if (str(item.id) == id):
            items.remove(item)
            print( "Item has been removed!")
            log_line = str(get_time()) + " | REMOVE ITEM | " + str(id)
            logs.append(str(log_line))
    input("\n Press Enter To Return To Main Menu...")
def print_cat():
    clear()
    print_header("LIST OF CATEGORIES")
    temp_list = []

    for item in items:
       
        if(item.category not in temp_list):
            temp_list.append(item.category)
    for item in temp_list:
        print(item)
    input("\n Press Enter To Return To Main Menu...")

id_count = 0

read_items() #read previous data from the file to items array
read_log()
def register_item():

    #import global variable into function
    clear()
   
    global id_count
    print_header("REGISTER NEW ITEM")
    #ask users for object values
    title = input("Please input the Title: ")
    category = input("Please input the Category: ")
    price = float(input("Please input the Price: "))
    stock = int(input("Please input the Stock: "))

    #assign those values to Item object
    new_item = Item()
    new_item.id = id_count
    new_item.title = title
    new_item.category = category
    new_item.price = price
    new_item.stock = stock

    id_count += 1
    items.append(new_item)
    print(" Item Created!! ")
    log_line = str(get_time()) + " | REGISTER ITEM | " + str(id)
    logs.append(str(log_line))
    input("\n Press Enter To Return To Main Menu...")

def update_stock():
    clear()
    list_item("UPDATE EXISTING STOCK")
    id = input("\n Select an ID to update its stock: ")
    found = False
    for item in items:
        if (str(item.id) == id):
            stock = input("\n Please input new stock value: ")
            item.stock = int(stock)
            found = True
            log_line = str(get_time()) + " | UPDATE | " + str(id)
            logs.append(str(log_line))
            print(str(item.title) + " stock is updated to " + str(item.stock))
           
    if(not found):
        print("Error: ID Doesn't exist, try again")
    input("\n Press Enter To Return To Main Menu...")

def register_purchase():
        """
        Show the items
        ask the user to select 1
        ask for the quantity in the order
        update the stock of the selected item
        
        
        """
        clear()
        list_item("SELECT AN ID TO PURCHASE")
        id = input("\n Select an ID: ")
        found = False

        for item in items:
            if (str(item.id) == id):
                found = True
                stock = int(input("\n How many would you like to purchase? : "))
                quanitity = False
                if(int(stock) <= int(item.stock)):
                    quanitity = True
                    print("\n The Total cost is: " + str(item.price * stock))
                    item.stock = item.stock - int(stock)
                    log_line = str(get_time()) + " | PURCHASE | " + str(id)
                    logs.append(str(log_line))
                    
                if(not quanitity):
                    print("Error: We do not have that much product in stock.")
                        
        if(not found):
            print("Error: ID Doesn't exist, try again")
        input("\n Press Enter To Return To Main Menu...")

def register_sale():
    clear()
    list_item("SELECT AN ID TO SELL TO US")
    id = int(input("\n Select an ID: "))
    found = False

    for item in items:
        if (item.id == id):
            found = True
            stock = int(input("\n How many would you like to sell? : "))
            print("\n The amount we owe you is: " + str(item.price * stock))
            item.stock = item.stock + int(stock)     
            log_line = str(get_time()) + " | SALE | " + str(id)
            logs.append(str(log_line))
                
    if(not found):
        print("Error: ID Doesn't exist, try again")
    input("\n Press Enter To Return To Main Menu...")

def list_no_stock():
    clear()
    print("ID  | Title                     | Category        | Price    | Stock ")
    for item in items:
        if(item.stock == 0):
            print(str(item.id).ljust(3)+ " | " +item.title.ljust(25) + " | " + item.category.ljust(15) + " | " +str(item.price).ljust(8)+ " | " +str(item.stock).ljust(6))
    input("\n Press Enter To Return To Main Menu...")
opc = ''
while(opc != 'x'):
    clear()
    print_menu()

    opc = input("Please select an option: ")

    #actions based on selected option
    if(opc == "1"):
        register_item()
        save_items()
    elif(opc == "2"):
        list_item("LIST ALL ITEMS")
        input("\n Press Enter To Return To Main Menu...")
    elif(opc =="3"):
        update_stock()
        save_items()
    elif(opc == "4"):
        list_no_stock()
    elif(opc == "5"):
        remove_item()
        save_items()
    elif(opc == "6"):
        print_cat()
    elif(opc == "7"):
        print_stock_value()
    elif(opc == "8"):
        register_purchase()
        save_items()
    elif(opc == "9"):
        register_sale()
        save_items()
    elif(opc == "10"):
        list_log()
    if(opc =="x"):
        input("\n Press Enter To Continue...")