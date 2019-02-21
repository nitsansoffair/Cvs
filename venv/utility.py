
import string

# "Saved words"
names = ["Name", "name"]
fnames = ["First Name", "First name", "first name"]
lnames = ["Last Name", "Last name", "last name"]
prefixes = ["CV", "Cv", "cv"
            "Personal Details", "Personal details", "personal details"]

dobs = ["Date Of Birth", "Date Of birth", "Date of Birth", "Date of birth", "date of birth"]
birthes = ["Birth", "birth",
           "Birth:", "birth:",
           "Birth-", "birth-"]

ids = ["ID", "Id", "id",
       "I.D", "I.d", "i.d"]

emails = ["E-mail", "e-mail",
          "Email", "email"]

phones = ["Phone", "phone",
          "Phone:", "phone:",
          "Phone-", "phone-"]
cells = ["Cell", "cell",
         "Cell:", "cell:",
         "Cell-", "cell-",
         "Cell.", "cell.",
         "Cell,", "cell,",
         "Cel", "cel",
         "Cel:", "cel:",
         "Cel-", "cel-",
         "Cel.", "cel.",
         "Cel,", "cel,",
         "Cellular", "cellular",
         "Cellular:", "cellular:",
         "Cellular-", "cellular-",
         "Mobile", "mobile",
         "Mobile:", "mobile:",
         "Mobile-", "mobile-"]
tells = ["Tell", "tell",
         "Tell:", "tell:",
         "Tell-", "tell-",
         "Tell.", "tell.",
         "Tell,", "tell,",
         "Tel", "tel",
         "Tel:", "tel:",
         "Tel-", "tel-",
         "Tel.", "tel."
         "Tel,", "tel,"]

areas = ["Galilee", "galilee",
         "Tel Aviv", "Tel aviv", "tel aviv",
         "Tel-Aviv", "Tel-aviv", "tel-aviv",
         "Darom", "darom",
         "HaDarom", "Hadarom",
         "Tzafon", "tzafon",
         "HaTzafon", "Hatzafon",
         "Merkaz", "merkaz",
         "HaMerkaz", "Hamerkaz"]
addresses = ["Address", "address",
             "Residence", "residence"]

statuses = ["Marital status", "marital status",
            "Status", "status"]

savedLanguages = ["Languages", "languages"]
progLanguages = ["Programming Languages", "Programming languages", "programming languages"]

educations = ["EDUCATION", "Education", "education",
              "Courses", "courses", "COURSES"]

experiences = ["EXPERIENCE", "Experience", "experience",
               "Employment", "employment"]
roles = ["Role", "role",
         "CEO", "Ceo",
         "CTO", "Cto"]

digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
empties = [' ', '-', ':', '=', '+', '.', "#"]


# Types
def isDigit(char):
    return char <= '9' and char >= '0'

def isNumber(str):
    for char in str:
        if not isDigit(char):
            return False
    return True

def isLetter(char):
    return (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z')


# contains
def contains(str, stockArr):
    for i in range(len(stockArr)):
        idxStr = indexOf(str, stockArr[i])
        if idxStr != -1:
            return True
    return False

def containsOf(str, pred):
    for char in str:
        if pred(char):
            return True
    return False


# Titles
def title(str):
    words = string.split(str, " ")
    length = getRealLen(words)
    return length <= 3 and contains(str, ["-", ":"])

def titleOf(str, stockArr):
    return contains(str, stockArr) and (title(str) or oneWordWithOut(str, empties))


# Sub Groups
def indexOf(str, subStr):
    if str == None:
        return -1
    for i in range(len(str)):
        j = 0
        strIdx = i
        while j < len(subStr) and strIdx < len(str) and str[strIdx] == subStr[j]:
            j += 1
            strIdx += 1
        if j == len(subStr):
            return i
    return -1

def oneOf(checkedElem, stockArr):
    for elem in stockArr:
        if checkedElem == elem:
            return True
    return False


# First/Last
def getFirstOf(str, pred, extendArr):
    i = 0
    while i < len(str) and not pred(str[i]) and not oneOf(str[i], extendArr):
        i += 1
    if i != len(str):
        return i
    else:
        return -1

def getLastOf(str, pred, extendArr):
    i = 0
    while i < len(str) and (pred(str[i]) or oneOf(str[i], extendArr)):
        i += 1
    if i != 0:
        return i
    else:
        return -1


# Cleaning
def getCleanedOf(str, pred, extendArr):
    cleanedWord = str
    idxFirstOf = getFirstOf(str, pred, extendArr)
    idxLastOf = getLastOf(str, pred, extendArr)
    if idxFirstOf == -1:
        idxFirstOf = 0
    if idxLastOf == -1:
        idxLastOf = len(str)
    cleanedWord = str[idxFirstOf : idxLastOf]
    return cleanedWord

def cleanAfter(str, stockArr):
    newStr = str
    for i in range(len(stockArr)):
        idxClean = indexOf(str, stockArr[i])
        if idxClean != -1:
            newStr = str[ : idxClean]
    return newStr

def skipOfAndStartFrom(str, skipArr, pred, extendArr):
    newStr = str
    for i in range(len(skipArr)):
        idxSkip = indexOf(str, skipArr[i])
        if idxSkip != -1:
            startIdx = idxSkip + len(skipArr[i])
            newStr = str[startIdx : ]
            idxFirstOf = getFirstOf(newStr, pred, extendArr)
            newStr = newStr[idxFirstOf : ]
    return newStr


# get Next/Prev Word
def getWordAfter(line, stockArr, pred):
    words = string.split(line, " ")
    nextWord = ""
    for i in range(len(words)):
        cleanedLetterdWord = getCleanedOf(words[i], isLetter, ["."])
        if oneOf(cleanedLetterdWord, stockArr):
            nextWord = getNextWord(words, i)
            while i < len(words) and not pred(nextWord):
                i += 1
                nextWord = getNextWord(words, i)
    return nextWord

def getNextWord(words, i):
    i += 1
    while i < len(words) and oneOf(words[i], empties + ["#:"]):
        i += 1
    if i >= len(words):
        return ""
    return words[i]

def getWordBefore(line, stockArr, pred):
    words = string.split(line, " ")
    prevWord = ""
    for i in range(len(words)):
        cleanedLetterdWord = getCleanedOf(words[i], isLetter, ["."])
        if oneOf(cleanedLetterdWord, stockArr):
            prevWord = getPrevWord(words, i)
            while i >= 0 and not pred(prevWord):
                i -= 1
                prevWord = getPrevWord(words, i)
    return prevWord

def getPrevWord(words, i):
    i -= 1
    while i >= 0 and oneOf(words[i], empties + ["#:"]):
        i -= 1
    return words[i]


# Formatting
def dateFormat(word):
    dotSplit = string.split(word, ".")
    backSlashSplit = string.split(word, "/")
    if dateFormatHelper(dotSplit) or dateFormatHelper(backSlashSplit):
        return True
    return False

def dateFormatHelper(split):
    checkLen = len(split) >=1 and len(split) <= 4
    nSatisfy = 0
    for part in split:
        if isNumber(part):
            nSatisfy += 1
        if nSatisfy >= 2:
            return True
    return False

def getDateFormatStr(unformattedDob):
    if contains(unformattedDob, ["-"]):
        splittedDob = string.split(unformattedDob, "-")
        return getDateFormatStrHelper(splittedDob, "-")
    elif contains(unformattedDob, ["/"]):
        splittedDob = string.split(unformattedDob, "/")
        return getDateFormatStrHelper(splittedDob, "/")
    elif contains(unformattedDob, ["."]):
        splittedDob = string.split(unformattedDob, ".")
        return getDateFormatStrHelper(splittedDob, ".")

def getDateFormatStrHelper(splittedDob, delimiter):
    if len(splittedDob[0]) > 3 or int(splittedDob[0]) > 31 or (int(splittedDob[1]) <= 31 and int(splittedDob[2]) <= 31):
        if (int(splittedDob[1] > 12)):
            return '%Y' + delimiter + '%d' + delimiter +'%m'
        else:
            return '%Y' + delimiter + '%m' + delimiter + '%d'
    elif len(splittedDob[2]) > 3 or (int(splittedDob[0]) <= 31 and int(splittedDob[1]) <= 31):
        if (int(splittedDob[0] > 12)):
            return '%d' + delimiter + '%m' + delimiter + '%Y'
        else:
            return '%m' + delimiter + '%d' + delimiter + '%Y'
    else:
        if int(splittedDob[2]) > 12:
            return '%m' + delimiter + '%Y' + delimiter + '%d'
        else:
            return '%d' + delimiter + '%Y' + delimiter + '%m'

def phoneFormat(word):
    splittedWord = string.split(word, "-")
    nValidPlus = 0
    nValidNumGroups = 0
    maxNumLen = 0
    for part in splittedWord:
        cleanedNumber = getCleanedOf(part, isDigit, [])
        if isNumber(cleanedNumber):
            nValidNumGroups += 1
            if maxNumLen < len(cleanedNumber):
                maxNumLen = len(cleanedNumber)
        if oneOf(part, '+'):
            nValidPlus += 1
    ans = (nValidNumGroups >= 1 and maxNumLen >= 4) or (nValidNumGroups >= 1 and nValidPlus >= 1)
    return ans


# Sequence
def isSeqOf(str, requiredNum, stockArr):
    nSeq = 0
    for char in str:
        if oneOf(char, stockArr):
            nSeq += 1
            if nSeq >= requiredNum:
                return True
        else:
            nSeq = 0
    return False

def containSeqOf(str, requiredNum, stockArr):
    words = string.split(str, " ")
    for word in words:
        if isSeqOf(word, requiredNum, stockArr):
            return True
    return False


# Others
def hasOneOf(elems, pred):
    for elem in elems:
        if pred(elem):
            return True
    return False

def getRealLen(words):
    realLen = len(words)
    for word in words:
        if word == " " or (not containsOf(word, isLetter) and not contains(word, digits)):
            realLen -= 1
    return realLen

def oneWordWithOut(line, stockArr):
    words = string.split(line, " ")
    nWords = 0
    for word in words:
        if not oneOf(word, stockArr):
            nWords += 1
    return nWords <= 2

def firstWordInLineContains(line, stockArr):
    words = string.split(line, " ")
    for i in range(min(3, len(words))):
        if contains(words[i], stockArr):
            return True
    return False

def defaultPred(word):
    return True
