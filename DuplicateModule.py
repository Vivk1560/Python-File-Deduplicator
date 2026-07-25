import hashlib
from os import walk, path, makedirs, remove
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

def checkSum(dirPath):
    starttObj = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    filesRemoved = 0
    duplicateFiles = 0
    totalFiles = 0
    makedirs("Marvellous",exist_ok= True)
    sObj = f"DuplicateRemovalLog {starttObj}.log"
    sObj = sObj.replace(" ","_")
    sObj = sObj.replace(":","_")
    sObj = sObj.replace("-","_")
    logName = path.join("Marvellous",sObj)
    border = "-"*50

    if not (path.isdir(dirPath)):
        logObj = open(logName,"w")
        logObj.write(border+"\n")
        logObj.write(f"Directory Path: {dirPath} is Invalid\n")
        logObj.write(border+"\n")
        endTime = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        return {"DirectoryName":dirPath, "TotalFiles":totalFiles,"DuplicateFiles":duplicateFiles, "filesRemoved":filesRemoved, "startTime":starttObj,"endTime":endTime, "logFile":logName}
    else:
        with open(logName,"w") as logObj:
            try:
                logObj.write(border+"\n")
                logObj.write("Marvellous Automation Script \n")
                logObj.write(f"Starting Time Of Scanning: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')} \n")
                logObj.write(f"Name Of The Directory Scanned: {dirPath} \n")
                logObj.write(border+"\n")

                for folders,subfolders,files in walk(dirPath):
                    totalFiles += len(files)
                    for i in range(len(files)):
                        file1 = path.join(folders,files[i])
                        for j in range(i+1,len(files)):
                            file2 = path.join(folders,files[j])
                            hex1 = hashing(file1)
                            hex2 = hashing(file2)
                            if(hex1==hex2):
                                duplicateFiles += 1
                                try:
                                    remove(file2)
                                    filesRemoved += 1
                                    logObj.write(border+"\n")
                                    logObj.write(f"Duplicate File Pair Found! \n")
                                    logObj.write(border+"\n")
                                    logObj.write(f"Duplicate File 1: {file1} \n")
                                    logObj.write(f"Duplicate File 2: {file2} \n")
                                    logObj.write(f"CheckSum Value Of The File1: {hex1} \n")
                                    logObj.write(f"CheckSum Value Of The File2: {hex2} \n")
                                    logObj.write(border+"\n")

                                except Exception as e1Obj:
                                    logObj.write(f"Exception Occurred In Deleting DuplicateFiles {file1} and {file2}, the exception is {e1Obj}")

                logObj.write(border+"\n")
                logObj.write(f"Total number of files scanned: {totalFiles} \n")
                logObj.write(f"Total number of duplicate files found: {duplicateFiles} \n")
                logObj.write(f"Total number of duplicates removed: {filesRemoved} \n")
                logObj.write(f"Ending Time Of Scanning: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')} \n")
                endTime = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
                return {"DirectoryName":dirPath, "TotalFiles":totalFiles,"DuplicateFiles":duplicateFiles, "filesRemoved":filesRemoved, "startTime":starttObj,"endTime":endTime, "logFile":logName}
            except Exception as e2Obj:
                logObj.write(f"Exception Occurred In Scanning the given directory {dirPath}, exception is: {e2Obj} at time {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')} \n")
                endTime = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
                return {"DirectoryName":dirPath, "TotalFiles":totalFiles,"DuplicateFiles":duplicateFiles, "filesRemoved":filesRemoved, "startTime":starttObj,"endTime":endTime, "logFile":logName}
        
        



def sendEmail(receiverMail,dirPath):
    senderMail = os.getenv("SENDER_EMAIL")
    appPassword = os.getenv("APP_PASSWORD")
    mailObj = EmailMessage()
    mailObj["From"] = senderMail
    mailObj["To"] = receiverMail
    mailObj["Subject"] = "Sending Scheduled Duplicate Task Report"
    report = checkSum(dirPath)
    body = f"""
    Jai Ganesh!,
    The Duplicate File Removal Operation Has Been Done Sucessfully.
    Operation Statistics:
    Starting Time Of Scanning: {report['startTime']}
    Completion Time Of Scanning: {report['endTime']}
    Directory Scanned: {report['DirectoryName']}
    Total Number Of Files Scanned: {report['TotalFiles']}
    Total Number Of Duplicate Files Found: {report['DuplicateFiles']}
    Total Number Of Duplicate Files Deleted: {report['filesRemoved']}

    Please Find Detailed LogFile Attached To This Mail.

    Regards,
    Marvellous Automation System
    """
    mailObj.set_content(body)
    aObj = open(report['logFile'],"rb")
    attachment = aObj.read()
    mailObj.add_attachment(attachment,maintype="text",subtype="plain",filename=path.basename(report["logFile"]))
    aObj.close()
    try:
        smtpObj = smtplib.SMTP("smtp.gmail.com",587)
        smtpObj.starttls()
        if not senderMail or not appPassword:
            raise ValueError("Missing SENDER_EMAIL or APP_PASSWORD. Please configure your .env file.")
        smtpObj.login(senderMail, appPassword)
        smtpObj.send_message(mailObj)
        smtpObj.quit()
    except Exception as eObj:
        print("Failed To Send Email Because Of:",eObj)



def hashing(fileName):
    hObj = hashlib.md5()
    fObj = open(fileName,"rb")
    buffer = fObj.read(1000)
    while(len(buffer)>0):
        hObj.update(buffer)
        buffer = fObj.read(1000)

    fObj.close()
    return hObj.hexdigest()

    
