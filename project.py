# Michael Langford
import sys

tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR",\
        "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

tagsLevel = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1,\
            "FAM":0, "MARR":1,"HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2,\
            "HEAD":0, "TRLR":0, "NOTE":0}

def parseFile(filename):
    with open(filename, 'r') as file:
        level = -1;
        tag = ''
        valid = ''
        args = ''
        for line in file:
            print('--> {}'.format(line.strip()))
            words = line.strip().split(' ')
            level = words[0]
            tag = words[1];
            if tag not in tags:
                if len(words) < 3:
                    valid = 'N'
                    args = ''
                elif words[2] in {"INDI" , "FAM"}:
                    tag = words[2]
                    args = words[1]
                    valid = isValidLevel(int(level), tag)
                else:
                    args = ' '.join(words[2:])
                    valid = 'N'
            else:
                if tag in {"INDI" , "FAM"}:
                    valid = 'N'
                    args = ' '.join(words[2:])
                else:
                    valid = isValidLevel(int(level), tag)
                    args = ' '.join(words[2:])
            print('<-- {}|{}|{}|{}'.format(level, tag, valid, args))


def isValidLevel(level, tag):
    if level == tagsLevel[tag]:
        return 'Y'
    return 'N'

parseFile(sys.argv[1])
