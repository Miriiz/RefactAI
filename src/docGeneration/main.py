from src.utils.function import *
from src.docGeneration.PdfCreator import PDF

if __name__ == '__main__':
    code = getFunctFromFile(os.path.dirname(__file__))
    codeArray = createCodeAndSummarize(code)

    print(codeArray)
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for func in codeArray:
        pdf.cell(0, 10, func[0], 0, 1)
        pdf.cell(0, 10, func[1][0]['summary_text'], 0, 1)
    pdf.save("test")

