import schedule 
import re
from sys import argv
from os import path
from DuplicateModule import sendEmail
from time import sleep

def validateEmail(email):

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if re.fullmatch(pattern, email):
        return True

    return False

def help():
    print("-"*60)
    print("Duplicate File Removal Automation")
    print("-"*60)
    print("This script scans a directory, identifies duplicate files using checksums, deletes duplicate files, creates a log file, and sends the log file through email.")
    print("Usage:")
    print("python DuplicateFileRemoval.py <DirectoryPath> <TimeIntervalInMinutes> <ReceiverEmail>")
    print("Example:")
    print("python DuplicateFileRemoval.py E:\\Data\\Demo 50 vivaankukreja@gmail.com")
    print("-"*60)

def usage():
    print("-"*60)
    print("Usage")
    print("-"*60)

    print("python DuplicateFileRemoval.py <AbsoluteDirectoryPath> <TimeIntervalInMinutes> <ReceiverEmailAddress>\n")

    print("Arguments:")
    print("1. AbsoluteDirectoryPath  : Directory to scan recursively.")
    print("2. TimeIntervalInMinutes : Time interval after which  the operation will repeat.")
    print("3. ReceiverEmailAddress  : Email address to receive the operation report.")
   

    print("-"*60)

def main():

    if len(argv)==2:
        if argv[1]=="--h" or argv[1]=="--H" or argv[1]=="--help" or argv[1]=="--Help":
            help()
        elif argv[1]=="--u" or argv[1]=="--U"or argv[1]=="--usage" or argv[1]=="--Usage":
            usage()
        else:
            print("Invalid Option")
            print("Use --h or --u for more info")

    elif len(argv)==4:
        directory = argv[1]
        try:
            interval = int(argv[2])
        except ValueError:
            print("Time Interval Should Be Numeric")
            return
        receiverMail = argv[3]
        if not path.isdir(directory):
            print("Invalid Directory Name")
            print("Provide Correct Path")
            return

        elif(interval<=0):
            print("Invalid Time Interval")
            return

        elif not validateEmail(receiverMail):
            print("Provide Valid Email Id")
            return

        elif not path.isabs(directory):
            print("Please Provide Absolute Path!")
            return
        else:
            schedule.every(interval).minutes.do(sendEmail,receiverMail,directory)
            while(True):
                schedule.run_pending()
                sleep(20)
    else:
        print("Invalid Number Of Arguments")
        print("Check --h or --u for more info")
        return

if __name__ == "__main__":
    main()
