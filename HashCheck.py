'''
Brendan Clayton Donahue
ccd3048
Blue Team Delta tool


Hashes critical files of the user's choice and then periodically checks the hashes, overwriting any mismatched files. 

Run with --init to build the hash list based on passed configuration files

Crontab runs with --ct to check hashes periodically

To update the hashlist pass --u and then the file name modified in the script directory

'''

import os
import argparse
import time


HASHDICT = {}
CONFDICT = {}
FILEDICT = {}

def HashFile(filepath):
    command = os.popen(f"md5sum " + filepath).read()
    return command.split()
    

def initialize():
    '''
    HashCheckConf file format should be as follows:

    path/to/file/in/system filenameInScriptDirectory
    path/to/file/in/system filenameInScriptDirectory
    path/to/file/in/system filenameInScriptDirectory
    path/to/file/in/system filenameInScriptDirectory

    initialize takes the path and makes it the key, then makes the hash of the script directory compliment the value
    '''
    with open("HashCheckConf.txt", "r") as file:
        for line in file:
            sl = line.split()
            #helpful for future references. searching by name FTW!
            FILEDICT[sl[0]] = sl[1] #filepath key 
            CONFDICT[sl[1]] = sl[0] #custom name key

            HASHDICT[sl[0]] = HashFile(sl[1]) #filepath key with custom hash

def update(filenameInScriptDirectory):
    with open("HCLog.txt", "a") as log:
        ''' 
        Update takes the updated filename as the argument following the option. 

        this will update the real system file and copy over it.
        '''

        os.popen(f"mv " + filenameInScriptDirectory + " " + str(CONFDICT[filenameInScriptDirectory]))
        HASHDICT[filenameInScriptDirectory] = HashFile(filenameInScriptDirectory)
        message = filenameInScriptDirectory + " updated at: " + os.popen("date").read() + f"\n"
        print(message)

        log.write(message)

def ct():
    with open("HCLog.txt", "a") as log:
        while True:
            for key, value in HASHDICT:
                if HashFile(key) != value:
                    message = f"File: \"" + key + "\" has been edited. Updating now.\n"
                    date = os.popen("date").read()
                    print(message + " " + date)
                    log.write(message + " " + date + f"\n")
                    update(FILEDICT[key])
            time.sleep(15.0)
        

################################################################################################################
def main():
    parse = argparse.ArgumentParser(description = "Hashes Critical files and checks em or something.")

    parse.add_argument("--init", type=str, help='Initializes, concatenates HashCheckConf.txt')
    parse.add_argument("--u", type=str, help="Updates critical files with changes made in HashCheckConf.txt")
    parse.add_argument("--ct", type=str, help="for self-designed crontab only, automated checks and replacements")

    args = parse.parse_args()

    if args.init == "init":
        initialize()
        exit()
    elif args.u:
        update(args.u)
    elif args.ct == "ct":
        ct()

main()
