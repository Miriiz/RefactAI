import itertools
from src.docGeneration.utils.function import *

if __name__ == '__main__':
    code, file = getFunctFromFile(os.path.dirname(os.path.abspath(__file__)))
    codeWithCommentary = getCommentaryFromCodeFunct(code)
    codeArray = createCodeAndSummarize(code)
    nltk.download('all')
    nlp = spacy.load('en_core_web_lg')
    for cc, ca in zip(codeWithCommentary, codeArray):
        if cc.startswith("#"):
            if SameMeaning_nlp(cc, ca):
                print("Same Meaning")
            else:
                print("Not same meaning")
