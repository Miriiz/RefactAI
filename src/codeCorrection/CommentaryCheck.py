import itertools
from src.docGeneration.utils.function import *

if __name__ == '__main__':
    code = getFunctFromFile(os.path.dirname(os.path.abspath(__file__)))
    codeWithCommentary = getCommentaryFromCodeFunct(code)
    codeArray = createCodeAndSummarize(code)
    for cc, ca in zip(codeWithCommentary, codeArray):
        if cc.startswith("#"):
            if SameMeaning(cc, ca):
                print("Same meaning")
            else:
                print("Not same meaning")