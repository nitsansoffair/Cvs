
import pymysql
import docx
import PyPDF2
import pathlib

from datetime import datetime

from parsers import  *


# SQL
def insert(array):
    """
    :param array: String data, input to DB
    Description: Insert array Data to DB
    :return: closes DB / prints Err
    """
    try:
        db = pymysql.connect(host = "127.0.0.1",
                             user = "root",
                             password = "",
                             db = "CvsDB")
        cursor = db.cursor()
        sql = """
            INSERT INTO users
            (full_name, dob, person_id, email, phone, city, marital_status, languages, education, work_experience)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(sql, array)
    except pymysql.connections.err as error:
        db.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        cursor.close()
        db.close()
        print("MySQL connection is closed")


# Files
def readText(filename):
    text = ""
    if indexOf(filename.lower(), "docx") != -1:
        text = readDocx(filename)
    elif indexOf(filename.lower(), "pdf") != -1:
        text = readPdf(filename)
    return text

def readPdf(filename):
    fileObj = open(filename, 'rb')
    reader = PyPDF2.PdfFileReader(fileObj)
    nPages = reader.numPages
    nPagesCurr = 0
    text = ""
    while nPagesCurr < nPages:
        pageObj = reader.getPage(nPagesCurr)
        nPagesCurr += 1
        text += pageObj.extractText()
    fileObj.close()
    return text

def readDocx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    text = '\n'.join(fullText)
    return text

def traverseFiles(rootDir = "Cvs/eng"):
    Cvs = []
    currentDirectory = pathlib.Path(rootDir)
    for currentFile in currentDirectory.iterdir():
        Cvs.append(readText(rootDir + str(currentFile)[len(rootDir) : ]))
    return Cvs


# Parse
def parseCv(Cv):
    """
    :param Cv: txt of Cv
    Description: Parse relevant fields from Cv, and Insert to DB
    :return: return of "insert" DB function
    """
    full_name = str(parseName(Cv))
    if full_name == "":
        full_name = None

    unformattedDob = str(parseDob(Cv).encode('utf-8'))
    formatDob = getDateFormatStr(unformattedDob)
    dob = None
    if(formatDob != "" and formatDob != None):
        dob = datetime.strptime(unformattedDob, formatDob)

    person_id = str(parseId(Cv).encode('utf-8'))
    if person_id == "":
        person_id = None

    email = str(parseEmail(Cv).encode('utf-8'))
    if email == "":
        email = None

    phone = str(parsePhone(Cv).encode('utf-8'))
    if phone == "":
        phone = None

    city = str(parseCity(Cv).encode('utf-8'))
    if city == "":
        city = None

    marital_status = str(parseStatus(Cv).encode('utf-8'))
    if marital_status == "":
        marital_status = None

    languages = str(parseLanguages(Cv).encode('utf-8'))
    if languages == "":
        languages = None

    education = str(parseEducation(Cv).encode('utf-8'))
    if education == "":
        education = None

    work_experience = str(parseExperience(Cv).encode('utf-8'))
    if work_experience == "":
        work_experience = None

    array = (full_name, dob, person_id, email, phone, city, marital_status, languages, education, work_experience)
    insert(array)

def parseAllCvs(rootDir):
    Cvs = traverseFiles(rootDir)
    for Cv in Cvs:
        parseCv(Cv)


# Print
def printPrevParsed(Cv):
    print "Name: ", parseName(Cv), "\n"
    print "Dob: ", parseDob(Cv), "\n"
    print "Id: ", parseId(Cv), "\n"
    print "Email: ", parseEmail(Cv), "\n"
    print "Phone: ", parsePhone(Cv), "\n"
    print "City: ", parseCity(Cv), "\n"
    print "Status: ", parseStatus(Cv), "\n"
    print "Languages: ", parseLanguages(Cv), "\n"
    print "Education: \n", parseEducation(Cv), "\n"
    print "Experience: \n", parseExperience(Cv), "\n"

def printAll(rootDir):
    Cvs = traverseFiles(rootDir)
    for i in range(len(Cvs)):
        print Cvs[i]


# Prints
print "Pdf:"
Cvs = traverseFiles("Cvs\pdf")
for Cv in Cvs:
    print parseName(Cv)

print "\nDocx:"
Cvs = traverseFiles("Cvs\eng") + traverseFiles("Cvs\docx")
for Cv in Cvs:
    print parseName(Cv)
