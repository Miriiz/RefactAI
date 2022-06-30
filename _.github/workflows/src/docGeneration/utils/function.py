import io
import os
import tokenize
from os.path import join
from difflib import SequenceMatcher
from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import spacy

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
            newCurrentRep.append(currentPath + '/' + r)
            for it in os.scandir(currentPath + '/' + r):
                if it.is_dir():
                    newCurrentRep.append(it.path)
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
    files_paths = []
    it_paths = 0
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
                        it_paths = 0
                        strr = fil.readline()
                        while strr != "":
                            if "def" in strr:
                                if it_paths != 0:
                                    func.append(val)
                                val = strr
                                it_paths += 1
                            else:
                                val += str(strr)
                            nextline = fil.readline()
                            strr = nextline
                        if it_paths != 0:
                            # filepath.replace(r, "")
                            func.append(val)
                            files_paths.append((filepath, it_paths))
    # func.pop(0)
    return func, files_paths


'''
Fonction to generate summarize from function 
@code : Array with extract code from file
:return Array with code and summarize
'''


def createCodeAndSummarize(code):
    x = []
    for c in code:
        tokenized_code = pythonTokenizer(c)
        x.append((c, pipeline([tokenized_code])))
    return x


def getCountLineComment(funct):
    count = 0
    stop = False
    for c in reversed(funct):
        if c.startswith('#') and stop is False:
            count += 1
        else:
            stop = True
    return count


def getCommentLine(split_c, count):
    i = 0
    allCommentary = []
    for c in reversed(split_c):
        if i != count:
            i += 1
            allCommentary.append(c)
    return '\n'.join(allCommentary)


def getCommentaryFromCodeFunct(code):
    newCode = []
    nextcomm = ''
    for c in code:
        split_c = c.split('\n')
        split_c.insert(0, nextcomm)
        while split_c.count('') > 0:
            split_c.remove('')
        count = getCountLineComment(split_c)
        nextcomm = getCommentLine(split_c, count)
        if split_c[-1].startswith('#'):
            nextcomm = getCommentLine(split_c, count)
            for i in range(count):
                split_c.pop()
        else:
            nextcomm = '\n'
        c = '\n'.join(split_c)
        count = 0
        newCode.append(c)
    return newCode


def ReformateStr(str, str2):
    str_low = str.lower()
    str2_low = str2[1][0]["summary_text"].lower()
    X_list = word_tokenize(str_low)
    Y_list = word_tokenize(str2_low)
    return X_list, Y_list


def SameMeaning(str, str2):
    X_list, Y_list = ReformateStr(str, str2)
    sw = stopwords.words('english')
    l1, l2 = [], []
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0
    # cosine formule
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    cosine = round(cosine * 100, 2)
    write_cosine(getFunctionName(str2[0]), cosine)
    return cosine > 40


def getFunctionName(funct):
    for c in funct.split('\n'):
        if c.startswith('def'):
            return c.replace(':', '')


def SameMeaning_nlp(cc, ca):
    nltk.download('all')
    nlp = spacy.load('en_core_web_lg')
    str_nlp = nlp(cc)
    str2_nlp = nlp(ca[1][0]["summary_text"])
    str_nlp_nostop = nlp(' '.join([str(t) for t in str_nlp if not t.is_stop]))
    str2_nlp_nostop = nlp(' '.join([str(t) for t in str2_nlp if not t.is_stop]))
    write_cosine(getFunctionName(ca[0]), round(str_nlp_nostop.similarity(str2_nlp_nostop) * 100, 2))
    return str_nlp_nostop.similarity(str2_nlp_nostop) > 0.5


def SameMeaning_Seq(str, str2):
    X_list, Y_list = ReformateStr(str, str2)
    return SequenceMatcher(None, str, str2[1][0]["summary_text"]).ratio() > 0.5


def write_cosine(functionName, consineValue):
    path = os.path.dirname(os.path.abspath(__file__)).split(IGNORE_DIR_NAME)[0] + 'output/'
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path + 'commentarySimilarity.txt'):
        with open(path + 'commentarySimilarity.txt', 'a') as f:
            f.write("Commentary Similarity for function :  " + functionName + ' : \t' + str(consineValue) + '% \n')
            print("Commentary Similarity for function :  " + functionName + ' : \t' + str(consineValue) + '% \n')

    else:
        print(path)
        with open(path + 'commentarySimilarity.txt', 'w+') as f:
            f.write("Commentary Similarity for function :  " + functionName + ' : \t' + str(consineValue) + '% \n')
            print("Commentary Similarity for function :  " + functionName + ' : \t' + str(consineValue) + '% \n')
