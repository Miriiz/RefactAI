import io
import os
import tokenize
from os.path import join

from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline

IGNORE_DIR_NAME = ".github"
IGNORE_DIR_NAME_2 = ".git"
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
    currentPath = ''.join(currentPath.split(IGNORE_DIR_NAME)[0])
    tmp = [f for f in os.listdir(currentPath) if os.path.isdir(join(currentPath, f))]
    rep = []
    for rm in tmp:
        if rm != IGNORE_DIR_NAME and rm != IGNORE_DIR_NAME_2:
            rep.append(rm)
    newCurrentRep = []
    newCurrentRep.append(currentPath)
    for r in rep:
        if r != currentPath:
            newCurrentRep.append(currentPath + "\\" + r)
    file = []
    for r in newCurrentRep:
        files = os.listdir(r)
        for name in files:
            if os.path.splitext(name)[1] == '.py':
                file.append(name)
    return newCurrentRep, file, currentPath


'''
@currentPath : Current path from file 
:return Function from file
'''


def getFunctFromFile(currentPath):
    files = getFileFromDir(currentPath)
    path = files[0]
    func = []
    val = ""
    for r in files[0]:
        if os.listdir(r) != 0:
            path = r
            for f in files[1]:
                if path != files[2]:
                    filepath = path + "/" + f
                else:
                    filepath = path + f
                if os.path.exists(filepath):
                    with open(filepath) as fil:
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
        # print(tokenized_code)
        x.append((c, pipeline([tokenized_code])))
    return x
