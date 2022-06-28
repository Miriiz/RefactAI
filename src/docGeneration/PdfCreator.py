import os

from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super(PDF, self).__init__()
        self.toc = []
        self.numbering = False
        self.numPageNum = 1
        self.my_links = []

    def AddPage(self):
        self.add_page()
        if self.numbering:
            self.numPageNum += 1

    def startPageNums(self):
        self.numbering = True

    def stopPageNums(self):
        self.numbering = False

    def TOC_Entry(self, txt, level=0):
        self.toc += [{'t': txt, 'l': level, 'p': self.numPageNum}]

    def insertTOC(self, location=1, labelSize=20, entrySize=10, tocfont='Times', label='Table of Contents'):
        self.stopPageNums()
        self.AddPage()
        tocstart = self.page

        self.set_font(tocfont, 'B', labelSize)
        self.cell(0, 5, label, 0, 1, 'C')
        self.ln(10)
        it = 0
        for t in self.toc:
            # Offset
            level = t['l']
            if level > 0:
                self.cell(level * 8)
            weight = ''
            if level == 0:
                weight = 'B'
            Str = t['t']
            self.set_font(tocfont, weight, entrySize)
            strsize = self.get_string_width(Str)
            self.cell(strsize + 2, self.font_size + 2, Str, link=self.my_links[it])
            it += 1

            # Filling dots
            self.set_font(tocfont, '', entrySize)
            PageCellSize = self.get_string_width(str(t['p'])) + 2
            w = self.w - self.l_margin - self.r_margin - PageCellSize - (level * 8) - (strsize + 2)
            nb = int(w / self.get_string_width('.'))
            dots = ''.join(['.' for i in range(nb)])
            self.cell(w, self.font_size + 2, dots, 0, 0, 'R')
            self.ln()

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

    def add_error(self, message):
        self.set_text_color(194, 8, 8)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, message, 0, 1)
        self.set_text_color(0, 0, 0)

    def add_path(self, path):
        self.AddPage()
        self.my_links.append(self.add_link())
        self.set_link(self.my_links[len(self.my_links) - 1])
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, path, 0, 1)#, link=self.files_link)
        self.TOC_Entry(path)

    def save(self, path,  filename):
        if os.path.exists(path):
            self.output(path + filename + '.pdf', 'F')
        else:
            os.mkdir(path)
            self.output(path + filename + '.pdf', 'F')
