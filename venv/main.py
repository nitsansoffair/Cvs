
import pymysql
import docx
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
def readtxt(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def traverseFiles():
    Cvs = []
    rootDir = "Cvs/eng"
    currentDirectory = pathlib.Path(rootDir)
    for currentFile in currentDirectory.iterdir():
        Cvs.append(readtxt(rootDir + str(currentFile)[len(rootDir) : ]))
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

def parseAllCvs():
    Cvs = traverseFiles()
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

def printAll():
    Cvs = traverseFiles()
    for i in range(len(Cvs)):
        print Cvs[i]
