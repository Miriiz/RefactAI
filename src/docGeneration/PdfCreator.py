from fpdf import FPDF


class PDF(FPDF):
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
        func_lines = func[0].split("\n")
        for func_line in func_lines:
            if len(func_line) != 0:
                self.cell(0, 10, func_line, 0, 1)
        self.cell(0, 10, "-> " + func[1][0]['summary_text'], 0, 1)
        self.ln()

    def save(self, filename):
        self.output('output/' + filename + '.pdf', 'F')