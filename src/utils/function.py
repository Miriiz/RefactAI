import os, sys
import tokenize
import io
from os.path import join

from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline

pipeline = SummarizationPipeline(
    model=AutoModelWithLMHead.from_pretrained("SEBIS/code_trans_t5_base_code_documentation_generation_python"),
    tokenizer=AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_code_documentation_generation_python",
                                            skip_special_tokens=True))


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


'''
Function to get file from directory
@Return new current path from file and files 
'''


def getFileFromDir(currentPath):
    rep = [f for f in os.listdir(currentPath) if os.path.isdir(join(currentPath, f))]
    newCurrentRep = currentPath + "\\" + rep[0]
    file = [f for f in os.listdir(currentPath) if os.path.isfile(join(currentPath, f))]
    return newCurrentRep, file


'''
@currentPath : Current path from file 
:return Function from file
'''


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


'''
Fonction to generate summarize from function 
@code : Array with extract code from file
:return Array with code and summarize
'''


def createCodeAndSummarize(code):
    x = []
    for c in code:
        tokenized_code = pythonTokenizer(c)
        print(tokenized_code)
        x.append((c, pipeline([tokenized_code])))
    return x
