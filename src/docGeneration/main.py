import os.path

from utils.function import *
from PdfCreator import PDF
from ModelFunctions import *

if __name__ == '__main__':
    code, files_paths = getFunctFromFile(os.path.dirname(os.path.abspath(__file__)))
    codeArray = createCodeAndSummarize(code)
    function_index = 0
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.startPageNums()
    # pdf.add_page()
    model = create_base_model(add_mlp_layers2, encoder)
    model.load_weights('model\\mlp2')

    for file_path in files_paths:
        pdf.add_path(file_path[0])
        for i in range(function_index, function_index + file_path[1]):
            pdf.add_error("error")
            print(model.predict(codeArray[function_index]))
            pdf.add_function(codeArray[function_index])
            function_index += 1

    pdf.insertTOC()
    pdf_path = ''.join(os.path.dirname(os.path.abspath(__file__)).split(IGNORE_DIR_NAME)[0]) + 'output/'
    pdf.save(pdf_path, "test")