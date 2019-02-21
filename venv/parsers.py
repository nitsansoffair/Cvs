
from utility import *

# Parsers

def parseName(Cv):
    lines = string.split(Cv, "\n")
    containName = False
    fullName = ""
    for i in range(len(lines)):
        array = []
        j = 0
        if contains(lines[i], names):
            fullName += lines[i] + "\n"
            containName = True
    if containName:
        fullNameLines = string.split(fullName, "\n")
        if len(fullNameLines) == 1:
            fullName = skipOfAndStartFrom(fullName, names, isLetter, [])
        elif len(fullNameLines) > 1:
            fullName = skipOfAndStartFrom(fullNameLines[0], names + fnames, isLetter, [])
            fullName += " " + skipOfAndStartFrom(fullNameLines[1], names + lnames, isLetter, [])
    else:
        lineIdx = 0
        while not containsOf(lines[lineIdx], isLetter):
            lineIdx += 1
        firstLetterIdx = getFirstOf(lines[lineIdx], isLetter, [])
        firstLetterLine = lines[lineIdx][firstLetterIdx : ]
        fullName = skipOfAndStartFrom(firstLetterLine, prefixes + names, isLetter, [])
    return fullName

def parseDob(Cv):
    lines = string.split(Cv, "\n")
    dob = ""
    for i in range(len(lines)):
        if contains(lines[i], dobs) and hasOneOf(lines[i], dateFormat):
            after = getWordAfter(lines[i], birthes, dateFormat)
            before = getWordBefore(lines[i], birthes, dateFormat)
            if dateFormat(after):
                dob = after
            elif dateFormat(before):
                dob = before
    return dob

def parseId(Cv):
    lines = string.split(Cv, "\n")
    id = ""
    for i in range(len(lines)):
        if contains(lines[i], ids) and containSeqOf(lines[i], 7, digits):
            id = getWordAfter(lines[i], ids, defaultPred)
    return id

def parseEmail(Cv):
    lines = string.split(Cv, "\n")
    email = ""
    for line in lines:
        if contains(line, "@"):
            email = skipOfAndStartFrom(line, emails, isLetter, [])
    return email

def parsePhone(Cv):
    lines = string.split(Cv, "\n")
    phone = ""
    retFlag = False
    for i in range(len(lines)):
        words = string.split(lines[i], " ")
        if contains(lines[i], phones + tells + cells) and hasOneOf(words, phoneFormat):
            after = getWordAfter(lines[i], cells, phoneFormat)
            if not phoneFormat(after):
                before = getWordBefore(lines[i], cells, phoneFormat)
                if not phoneFormat(before):
                    afterNextPriority = getWordAfter(lines[i], phones + tells, phoneFormat)
                    if not phoneFormat(afterNextPriority):
                        beforeNextPriority = getWordBefore(lines[i], phones + tells, phoneFormat)
            if phoneFormat(after):
                chosen = after
                retFlag = True
            elif phoneFormat(before):
                chosen = before
            elif phoneFormat(afterNextPriority):
                chosen = afterNextPriority
            elif phoneFormat(beforeNextPriority):
                chosen = beforeNextPriority
            cleanedAfter = cleanAfter(chosen, [",", ".", " "])
            idxFirstDigit = getFirstOf(cleanedAfter, isDigit, [])
            if idxFirstDigit != -1:
                phone = cleanedAfter[idxFirstDigit : ]
            if retFlag and phone != "":
                return phone
    return phone

def parseCity(Cv):
    lines = string.split(Cv, "\n")
    city = ""
    for line in lines:
        if contains(line, addresses + areas):
            address = string.split(line, ",")
            for subAddress in address:
                if not contains(subAddress, digits + ["st"]):
                    city = skipOfAndStartFrom(subAddress,  ["\n"], isLetter, [])
            if city == "":
                for subAddress in address:
                    if contains(subAddress, ["/"]) and contains(subAddress, digits):
                        subs = string.split(subAddress, "/")
                        for sub in subs:
                            idxLastDigit = getLastOf(sub, isDigit, [])
                            forwardSub = sub[idxLastDigit : ]
                            city = skipOfAndStartFrom(forwardSub, [" "], isLetter, [])
    return city

def parseStatus(Cv):
    lines = string.split(Cv, "\n")
    marital_status = ""
    for line in lines:
        if contains(line, statuses):
            chosenLine = line
            idxSavedWords = -1
            for savedWord in statuses:
                idxSavedWords = indexOf(line, savedWord)
                if idxSavedWords != -1:
                    lenSavedWord = len(savedWord)
                    break
            forwardedLine = chosenLine[idxSavedWords + lenSavedWord : ]
            cleanedLine = skipOfAndStartFrom(forwardedLine, " ", isLetter, [])
            checkedWords = string.split(cleanedLine, " ")
            for checkedWord in checkedWords:
                if not contains(checkedWord, emails + ["@"]):
                    marital_status += checkedWord + " "
    return marital_status

def parseLanguages(Cv):
    lines = string.split(Cv, "\n")
    languages = ""
    for i in range(len(lines)):
        if contains(lines[i], savedLanguages) and not contains(lines[i], progLanguages):
            languages = skipOfAndStartFrom(lines[i], savedLanguages, isLetter, [])
            if not containsOf(languages, isLetter):
                i += 1
                while containsOf(lines[i], isLetter):
                    idxLastChar = indexOf(lines[i], ":")
                    if idxLastChar == -1:
                        idxLastChar = indexOf(lines[i], ",")
                    languages += lines[i][ : idxLastChar] + " "
                    i += 1
                languages = skipOfAndStartFrom(languages, " ", isLetter, [])
    return languages

def parseEducation(Cv):
    lines = string.split(Cv, "\n")
    education = ""
    for i in range(len(lines)):
        if contains(lines[i], educations) and (contains(lines[i], [":", "-"]) or oneWordWithOut(lines[i], [])):
            i += 1
            while i < len(lines) and not containsOf(lines[i], isLetter):
                i += 1
            while i < len(lines) and (containsOf(lines[i], isLetter) and not title(lines[i])) \
                    and not contains(lines[i], statuses + savedLanguages + experiences):
                education += lines[i] + "\n"
                i += 1
                while i < len(lines) and not containsOf(lines[i], isLetter) and not title(lines[i]):
                    i += 1
    return education

def parseExperience(Cv):
    lines = string.split(Cv, "\n")
    experience = ""
    for i in range(len(lines)):
        if firstWordInLineContains(lines[i], experiences) and not contains(lines[i], educations):
            i += 1
            while i < len(lines) and not containsOf(lines[i], isLetter) and not titleOf(lines[i], digits):
                i += 1
            while i < len(lines) and (containsOf(lines[i], isLetter) or titleOf(lines[i], digits)) and \
                    (not title(lines[i]) or titleOf(lines[i], digits) or contains(lines[i], roles)) and not titleOf(lines[i], educations):
                experience += lines[i] + "\n"
                lines[i] = ""
                i += 1
                while i < len(lines) and not containsOf(lines[i], isLetter) and not title(lines[i]):
                    i += 1
    return experience
