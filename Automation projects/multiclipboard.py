import sys
import clipboard
import json

SAVED_DATA = "clipboard.json"

def save_items(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_items(filepath):
    try: 
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except:
        return {}

if len(sys.argv) == 2:
    command = sys.argv[1]
    data = load_items(SAVED_DATA)
    
    if command == "save".lower():
        key = input("Enter a key:")
        data[key] = clipboard.paste()
        save_items(SAVED_DATA, data)
        print("data saved!")
    elif command == "load".lower():
        key = input("Enter a key:")
        if key in data:
            clipboard.copy(data[key])
            print("data copied to clipboard!")
        else:
            print("Key doesn't excist.")
    elif command == "list".lower():
        print(data)
    else:
        print("Unkown command")
else:
    print("Please pass exactly two commands.")
