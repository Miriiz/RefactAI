import os, sys
import tokenize
import io
from os.path import join

from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline


def pythonTokenizer(line):
    result = []
    line = io.StringIO(line)

    for toktype, tok, start, end, line in tokenize.generate_tokens(line.readline):
        if not toktype == tokenize.COMMENT:
            if toktype == tokenize.STRING:
                result.append("CODE_STRING")
            elif toktype == tokenize.NUMBER:
                result.append("CODE_INTEGER")
            elif (not tok == "\n") and (not tok == "    "):
                result.append(str(tok))
    return ' '.join(result)


def getFileFromDir(currentPath):
    rep = [f for f in os.listdir(currentPath) if os.path.isdir(join(currentPath, f))]
    newCurrentRep = currentPath + "\\" + rep[0]
    file = [f for f in os.listdir(currentPath) if os.path.isfile(join(currentPath, f))]
    return newCurrentRep, file


def getFunctFromFile(currentPath):
    files = getFileFromDir(currentPath)
    path = files[0]
    func = []
    val = ""
    for f in files[1]:
        with open(path + "\\" + f) as fil:

            strr = fil.readline()
            while strr != "":
                if "def" in strr:
                    func.append(val)
                    val = strr

                else:
                    val += str(strr)
                nextline = fil.readline()
                strr = nextline
            func.append(val)
    func.pop(0)
    func = sorted(func, key=len, reverse=True)
    return func

