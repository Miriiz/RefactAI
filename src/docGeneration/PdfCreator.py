import os

from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super(PDF, self).__init__()
        self.files_link = None

    def header(self):
        #self.image('logo_pb.png', 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(45, 10, 'Documentation', 1, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def add_function(self, func):
        self.set_font('Arial', '', 10)
        func_lines = func[0].split("\n")
        for func_line in func_lines:
            if len(func_line) != 0:
                self.cell(0, 10, func_line, 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, "-> " + func[1][0]['summary_text'], 0, 1)
        self.ln()

    def add_summary(self, files):
        self.files_link = self.add_link()
        self.set_font('Arial', 'B', 16)
        #self.set_link(self.files_link)
        self.cell(40, 10, 'Page 2', border=1, ln=0, align='', fill=False)
        return

    def add_path(self, path):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, path, 0, 1, link=self.files_link)

    def save(self, path,  filename):
        if os.path.exists(path):
            self.output(path + filename + '.pdf', 'F')
        else:
            os.mkdir(path)
            self.output(path + filename + '.pdf', 'F')
