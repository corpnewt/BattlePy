import os

def cls():
	os.system('cls' if os.name=='nt' else 'clear')
    
def head(text = "BattlePy", width = 50):
	print("  {}".format("#"*width))
	mid_len = int(round(width/2-len(text)/2)-2)
	middle = " #{}{}{}#".format(" "*mid_len, text, " "*((width - mid_len - len(text))-2))
	print(middle)
	print("#"*width)
    
def get(text = "Please select an option:  ", **kwargs):
    quit = kwargs.get("quit", True)
    prnt = kwargs.get("print", False) # auto print M. Menu, Q. Quit, etc

    if quit and prnt:
        print("Q. Quit")
        print(" ")
        
    i = input(text)
    
    if quit and i.lower() == "q" or i.lower() == "quit":
        os._exit(0)
        
    return i