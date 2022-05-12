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
    for i in range(1, 41):
        pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
    pdf.output('output/tuto2.pdf', 'F')

