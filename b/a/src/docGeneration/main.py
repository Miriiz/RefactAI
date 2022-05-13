from b.a.src.utils.function import *
from b.a.src.docGeneration.PdfCreator import PDF

if __name__ == '__main__':
    code = getFunctFromFile(os.path.dirname(__file__))
    codeArray = createCodeAndSummarize(code)
    print(codeArray)

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for func in codeArray:
        pdf.add_function(func)
    pdf.save("test")

