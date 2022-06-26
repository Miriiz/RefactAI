import os.path

from utils.function import *
from PdfCreator import PDF

if __name__ == '__main__':
    code, files_paths = getFunctFromFile(os.path.dirname(os.path.abspath(__file__)))
    codeArray = createCodeAndSummarize(code)
    function_index = 0

    pdf = PDF()
    pdf.alias_nb_pages()
    #pdf.add_page()
    # pdf.add_summary(None)

    for file_path in files_paths:
        pdf.add_path(file_path[0])
        for i in range(function_index, function_index + file_path[1]):
            pdf.add_error("error")
            pdf.add_function(codeArray[function_index])
            function_index += 1

    pdf_path = ''.join(os.path.dirname(os.path.abspath(__file__)).split(IGNORE_DIR_NAME)[0]) + 'output/'
    pdf.save(pdf_path, "test")