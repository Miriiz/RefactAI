import os

from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super(PDF, self).__init__()
        self.files_link = None

        self.toc = []
        self.numbering = 0
        self.numPageNum = 1

    def AddPage(self):
        FPDF.AddPage(self)
        if self.numbering:
            self.numPageNum += 1

    def startPageNums(self):
        self.numbering = 1

    def stopPageNums(self):
        self.numbering = 0

    def numPageNo(self):
        return self.numPageNum

    def TOC_Entry(self, txt, level=0):
        self.toc += [{'t': txt, 'l': level, 'p': self.numPageNo()}]

    def insertTOC(self, location=1, labelSize=20, entrySize=10, tocfont='Times', label='Table of Contents'):
        self.stopPageNums()
        self.AddPage()
        tocstart = self.page

        self.SetFont(tocfont, 'B', labelSize)
        self.Cell(0, 5, label, 0, 1, 'C')
        self.Ln(10)

        for t in self.toc:
            # Offset
            level = t['l']
            if level > 0:
                self.Cell(level * 8)
            weight = ''
            if level == 0:
                weight = 'B'
            Str = t['t']
            self.SetFont(tocfont, weight, entrySize)
            strsize = self.GetStringWidth(Str)
            self.Cell(strsize + 2, self.FontSize + 2, Str)

            # Filling dots
            self.SetFont(tocfont, '', entrySize)
            PageCellSize = self.GetStringWidth(str(t['p'])) + 2
            w = self.w - self.lMargin - self.rMargin - PageCellSize - (level * 8) - (strsize + 2)
            nb = w / self.GetStringWidth('.')
            dots = ['.' for i in range(nb)]
            self.Cell(w, self.FontSize + 2, dots, 0, 0, 'R')

            # Page number
            self.Cell(PageCellSize, self.FontSize + 2, str(t['p']), 0, 1, 'R')

        # grab it and move to selected location
        n = self.page
        n_toc = n - tocstart + 1
        last = []

        # store toc pages
        for i in range(tocstart, n + 1):
            last += [self.pages[i]]

        # move pages
        for i in range(tocstart - 1, location - 1, -1):
            # ~ for(i=tocstart - 1;i>=location-1;i--)
            self.pages[i + n_toc] = self.pages[i]

        # Put toc pages at insert point
        for i in range(0, n_toc):
            self.pages[location + i] = last[i]

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

    def add_error(self, message):
        self.set_text_color(194, 8, 8)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, message, 0, 1)
        self.set_text_color(0, 0, 0)

    def add_path(self, path):
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, path, 0, 1)#, link=self.files_link)

    def save(self, path,  filename):
        if os.path.exists(path):
            self.output(path + filename + '.pdf', 'F')
        else:
            os.mkdir(path)
            self.output(path + filename + '.pdf', 'F')
