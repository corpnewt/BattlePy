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

def main(target, output):
    animations = []
    current_animation = ""
    current_time      = 0.50
    with open(target, "r") as f:
        for line in f:
            if line.startswith('set "frame1='):
                # We got the first frame
                current_animation = line.replace('set "frame1=', '')[:-2] + "\n"
            elif line.startswith('set "frame8='):
                # Last frame
                current_animation += line.replace('set "frame8=', "")[:-2]
            elif line.startswith('set "frame'):
                # Some in-between frame
                current_animation += line[len('set "frame1='):-2] + "\n"
            elif line.startswith("call :displayAnimation "):
                if "1000" in line:
                    animations.append({ "frame" : current_animation, "time" : 1.0 })
                elif "2000" in line:
                    animations.append({ "frame" : current_animation, "time" : 2.0 })
                else:
                    animations.append({ "frame" : current_animation, "time" : 0.05 })
    json.dump(animations, open(output, "w"), indent=2)

targets = [ "Miss.txt", "Hit.txt", "Sunk.txt" ]
outputs = [ "Miss.json", "Hit.json", "Sunk.json" ]

for i in range(len(targets)):
    main(targets[i], outputs[i])