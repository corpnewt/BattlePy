import os
import sys
import time
import json

script_path = os.path.dirname(os.path.realpath(__file__))

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# OS Independent clear method
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def check_path(path):
    # Add os checks for path escaping/quote stripping
    if os.name == 'nt':
        # Windows - remove quotes
        path = path.replace('"', "")
    else:
        # Unix - remove quotes and space-escapes
        path = path.replace("\\", "").replace('"', "")
    # Remove trailing space if drag and dropped
    if path[len(path)-1:] == " ":
        path = path[:-1]
    # Expand tilde
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        print("That file doesn't exist!")
        return None
    return path

def main():
    
    cls()
    new_file = ""
    with open("Miss.txt", "r") as f:
        for line in f:
            if line.startswith('set "frame1='):
                line = line.replace('set "frame1=', '"""')[:-2] + "\n"
            elif line.startswith('set "frame8='):
                line = line.replace('set "frame8=', "")[:-2] + '"""\n'
            else:
                line = line[len('set "frame1='):-2] + "\n"
            new_file += line
    with open("Miss-edit.txt", "w") as f:
        f.write(new_file)

main()