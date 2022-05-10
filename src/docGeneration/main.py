from src.utils.function import *

if __name__ == '__main__':
    code = getFunctFromFile(os.path.dirname(__file__))
    codeArray = createCodeAndSummarize(code)
