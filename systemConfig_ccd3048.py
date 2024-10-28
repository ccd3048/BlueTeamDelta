import os
#Brendan Clayton Donahue Blue team delta ccd3048
def main():
    with open("commands.txt", "r") as file:
        lines = file.readlines()

        for line in lines:
            os.popen(line)
main()