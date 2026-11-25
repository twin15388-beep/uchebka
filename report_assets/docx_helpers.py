# -*- coding: utf-8 -*-
"""Вспомогательные классы для сборки отчёта в формате .docx."""
import math
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

TEXT_WIDTH_CM = 16.5
PAGE_H_PT = 842.0 - 2 * 56.7          # A4 без верхнего и нижнего поля
LINE_PT = 24.2                        # строка 14 пт при полуторном интервале
CHARS_PER_LINE = 71


def _set_run_font(run, name="Times New Roman", size=14, bold=None,
                  italic=None, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def _set_paragraph_border(paragraph, color="BFBFBF", sz="4"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "4")
        el.set(qn("w:color"), color)
        pBdr.append(el)
    pPr.append(pBdr)


def _shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


class Builder:
    def __init__(self, toc_pages=None, track=True):
        self.doc = Document()
        self.toc_pages = toc_pages if toc_pages is not None else {}
        self.track = track
        self.page = 1
        self.y = 0.0
        self.heading_pages = {}
        self.total_h = 0.0
        self.table_no = 0
        self.fig_no = 0
        self._setup()

    # ------------------------------------------------------------------ setup
    def _setup(self):
        doc = self.doc
        sec = doc.sections[0]
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin = Cm(3.0)
        sec.right_margin = Cm(1.5)
        sec.header_distance = Cm(1.25)
        sec.footer_distance = Cm(1.25)

        styles = doc.styles
        normal = styles["Normal"]
        normal.font.name = "Times New Roman"
        normal.font.size = Pt(14)
        rpr = normal.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.insert(0, rfonts)
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(attr), "Times New Roman")
        pf = normal.paragraph_format
        pf.line_spacing = 1.5
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.first_line_indent = Cm(1.25)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        for name, size, bold, caps, align in (
                ("Heading 1", 14, True, True, WD_ALIGN_PARAGRAPH.CENTER),
                ("Heading 2", 14, True, False, WD_ALIGN_PARAGRAPH.LEFT),
        ):
            st = styles[name]
            st.font.name = "Times New Roman"
            st.font.size = Pt(size)
            st.font.bold = bold
            st.font.color.rgb = RGBColor(0, 0, 0)
            st.font.all_caps = caps
            rpr = st.element.get_or_add_rPr()
            rfonts = rpr.find(qn("w:rFonts"))
            if rfonts is None:
                rfonts = OxmlElement("w:rFonts")
                rpr.insert(0, rfonts)
            for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rfonts.set(qn(attr), "Times New Roman")
            pf = st.paragraph_format
            pf.first_line_indent = Cm(1.25) if name == "Heading 2" else Cm(0)
            pf.alignment = align
            pf.line_spacing = 1.5
            pf.space_before = Pt(12)
            pf.space_after = Pt(6)
            pf.keep_with_next = True

        # титульный лист без номера страницы
        sec.different_first_page_header_footer = True

        # нижний колонтитул с номером страницы
        footer = sec.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.paragraph_format.first_line_indent = Cm(0)
        fp.paragraph_format.line_spacing = 1.0
        run = fp.add_run()
        _set_run_font(run, size=12)
        fld1 = OxmlElement("w:fldChar"); fld1.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve")
        instr.text = " PAGE  \\* MERGEFORMAT "
        fld2 = OxmlElement("w:fldChar"); fld2.set(qn("w:fldCharType"), "separate")
        txt = OxmlElement("w:t"); txt.text = "1"
        fld3 = OxmlElement("w:fldChar"); fld3.set(qn("w:fldCharType"), "end")
        run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
        run._r.append(txt); run._r.append(fld3)

        # обновление полей при открытии, запрет переносов, язык ru-RU
        settings = doc.settings.element
        upd = OxmlElement("w:updateFields"); upd.set(qn("w:val"), "true")
        settings.append(upd)
        hyph = OxmlElement("w:autoHyphenation"); hyph.set(qn("w:val"), "false")
        settings.append(hyph)
        lang = OxmlElement("w:themeFontLang")
        lang.set(qn("w:val"), "ru-RU")
        settings.append(lang)

    # ------------------------------------------------------------ pagination
    def _need(self, h, atomic=True):
        if not self.track:
            return
        self.total_h += h
        if atomic:
            if self.y + h > PAGE_H_PT and self.y > 0:
                self.page += 1
                self.y = 0.0
            self.y += h
        else:
            while h > 0.5:
                remaining = PAGE_H_PT - self.y
                if remaining <= 1:
                    self.page += 1
                    self.y = 0.0
                    remaining = PAGE_H_PT
                used = min(h, remaining)
                h -= used
                self.y += used

    def page_break(self):
        self.doc.add_page_break()
        if self.track:
            self.page += 1
            self.y = 0.0

    # --------------------------------------------------------------- headings
    def h1(self, text, page_break=True):
        if page_break and self.track:
            self.page += 1
            self.y = 0.0
        p = self.doc.add_paragraph(style="Heading 1")
        p.paragraph_format.page_break_before = page_break
        run = p.add_run(text.upper())
        _set_run_font(run, size=14, bold=True, color="000000")
        self.heading_pages[text] = self.page
        self._need(LINE_PT + 18)

    def h2(self, text):
        p = self.doc.add_paragraph(style="Heading 2")
        run = p.add_run(text)
        _set_run_font(run, size=14, bold=True, color="000000")
        self.heading_pages[text] = self.page
        self._need(LINE_PT + 18)

    # ------------------------------------------------------------------- text
    def p(self, text="", first=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
          size=14, bold=False, italic=False, space_after=0, space_before=0,
          keep=False):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = align
        pf.first_line_indent = Cm(1.25) if first else Cm(0)
        pf.space_after = Pt(space_after)
        pf.space_before = Pt(space_before)
        pf.line_spacing = 1.5
        pf.keep_with_next = keep
        run = p.add_run(text)
        _set_run_font(run, size=size, bold=bold, italic=italic, color="000000")
        lines = max(1, math.ceil(len(text) / CHARS_PER_LINE)) if text else 1
        self._need(lines * LINE_PT + space_before + space_after)
        return p

    def bullet(self, text):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.left_indent = Cm(1.25)
        pf.first_line_indent = Cm(-0.6)
        pf.line_spacing = 1.5
        run = p.add_run("– " + text)
        _set_run_font(run, size=14, color="000000")
        lines = max(1, math.ceil((len(text) + 2) / CHARS_PER_LINE))
        self._need(lines * LINE_PT)

    def num(self, number, text):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.left_indent = Cm(1.25)
        pf.first_line_indent = Cm(-0.6)
        pf.line_spacing = 1.5
        run = p.add_run(f"{number}) " + text)
        _set_run_font(run, size=14, color="000000")
        lines = max(1, math.ceil((len(text) + 4) / CHARS_PER_LINE))
        self._need(lines * LINE_PT)

    def caption(self, text, before=6, after=12):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(before)
        pf.space_after = Pt(after)
        pf.keep_with_next = False
        run = p.add_run(text)
        _set_run_font(run, size=12, color="000000")
        self._need(14 + before + after)

    def table_caption(self, text):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(10)
        pf.space_after = Pt(4)
        pf.keep_with_next = True
        run = p.add_run(text)
        _set_run_font(run, size=12, color="000000")
        self._need(14 + 14)

    # ------------------------------------------------------------------ table
    def table(self, data, widths, header=True, size=12, align_center=None,
              row_height=None, first_col_center=False):
        rows, cols = len(data), len(data[0])
        t = self.doc.add_table(rows=rows, cols=cols)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        tblPr = t._tbl.tblPr
        layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed")
        tblPr.append(layout)
        mar = OxmlElement("w:tblCellMar")
        for side, val in (("top", "28"), ("bottom", "28"),
                          ("left", "85"), ("right", "85")):
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:w"), val); el.set(qn("w:type"), "dxa")
            mar.append(el)
        tblPr.append(mar)

        total = sum(widths)
        scale = TEXT_WIDTH_CM / total
        widths = [w * scale for w in widths]
        for i, w in enumerate(widths):
            t.columns[i].width = Cm(w)
        no_split = rows <= 6
        for row in t.rows:
            trPr = row._tr.get_or_add_trPr()
            if no_split:
                cant = OxmlElement("w:cantSplit"); trPr.append(cant)
            for i, cell in enumerate(row.cells):
                cell.width = Cm(widths[i])
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        est = 0.0
        for ri, row in enumerate(data):
            max_lines = 1
            for ci, val in enumerate(row):
                cell = t.cell(ri, ci)
                cell.paragraphs[0].text = ""
                p = cell.paragraphs[0]
                pf = p.paragraph_format
                pf.first_line_indent = Cm(0)
                pf.line_spacing = 1.0
                pf.space_before = Pt(0)
                pf.space_after = Pt(0)
                center = (header and ri == 0) or \
                    (align_center is not None and ci in align_center) or \
                    (first_col_center and ci == 0)
                pf.alignment = WD_ALIGN_PARAGRAPH.CENTER if center \
                    else WD_ALIGN_PARAGRAPH.LEFT
                run = p.add_run(str(val))
                _set_run_font(run, size=size, bold=(header and ri == 0),
                              color="000000")
                if header and ri == 0:
                    _shade_cell(cell, "F2F2F2")
                chars_per_line = max(6, widths[ci] * 28.35 / (size * 0.47))
                max_lines = max(max_lines,
                                math.ceil(len(str(val)) / chars_per_line))
            est += max_lines * (size * 1.17) + 6

        if header:
            trPr = t.rows[0]._tr.get_or_add_trPr()
            th = OxmlElement("w:tblHeader"); trPr.append(th)
        self._need(est + 4, atomic=False)
        return t

    # ----------------------------------------------------------------- figure
    def figure(self, path, caption, width_cm=15.0):
        with Image.open(path) as im:
            w, h = im.size
        height_cm = width_cm * h / w
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(6)
        pf.space_after = Pt(2)
        pf.keep_with_next = True
        run = p.add_run()
        run.add_picture(path, width=Cm(width_cm))
        self.fig_no += 1
        self.caption(f"Рисунок {self.fig_no} – {caption}")
        self._need((height_cm + 0.9) * 28.35)

    # ------------------------------------------------------------------- code
    def code(self, text, size=11):
        lines = text.split("\n")
        for i, line in enumerate(lines):
            p = self.doc.add_paragraph()
            pf = p.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.first_line_indent = Cm(0)
            pf.left_indent = Cm(0.3)
            pf.right_indent = Cm(0.1)
            pf.line_spacing = 1.0
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.keep_with_next = False
            _set_paragraph_border(p)
            run = p.add_run(line if line else " ")
            _set_run_font(run, name="Consolas", size=size, color="000000")
        self._need(len(lines) * size * 1.25 + 10, atomic=False)

    def code_caption(self, text):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(10)
        pf.space_after = Pt(4)
        pf.keep_with_next = True
        run = p.add_run(text)
        _set_run_font(run, size=12, color="000000")
        self._need(14 + 14)

    # -------------------------------------------------------------------- toc
    def toc(self, entries):
        """entries: list of (level, text, page)"""
        first = True
        for level, text, page in entries:
            p = self.doc.add_paragraph()
            pf = p.paragraph_format
            pf.first_line_indent = Cm(0)
            pf.left_indent = Cm(0 if level == 1 else 0.75)
            pf.line_spacing = 1.15
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.tab_stops.add_tab_stop(Cm(TEXT_WIDTH_CM),
                                      WD_TAB_ALIGNMENT.RIGHT,
                                      WD_TAB_LEADER.DOTS)
            if first:
                r = p.add_run()
                f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
                f1.set(qn("w:dirty"), "true")
                it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
                it.text = ' TOC \\o "1-2" \\h \\z \\u '
                f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "separate")
                r._r.append(f1); r._r.append(it); r._r.append(f2)
                first = False
            run = p.add_run(text)
            _set_run_font(run, size=14, bold=(level == 1), color="000000")
            run2 = p.add_run("\t" + str(page))
            _set_run_font(run2, size=14, color="000000")
        # закрытие поля
        p = self.doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        r = p.add_run()
        f3 = OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"), "end")
        r._r.append(f3)

    def save(self, path):
        self.doc.save(path)


def _extra_methods(cls):
    """Дополнительные методы оформления под структуру отчёта-образца."""

    def p_right(self, text, bold=True, size=14, space_before=0, space_after=0):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(space_before)
        pf.space_after = Pt(space_after)
        run = p.add_run(text)
        _set_run_font(run, size=size, bold=bold, color="000000")
        self._need(LINE_PT)
        return p

    def fig(self, path, caption, width_cm=15.0, sep=". "):
        """Рисунок с подписью вида «Рисунок N. Подпись»."""
        with Image.open(path) as im:
            w, h = im.size
        height_cm = width_cm * h / w
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(6)
        pf.space_after = Pt(2)
        pf.keep_with_next = True
        run = p.add_run()
        run.add_picture(path, width=Cm(width_cm))
        if caption is None:
            self._need((height_cm + 0.5) * 28.35)
            return p
        self.fig_no += 1
        cap = self.doc.add_paragraph()
        cpf = cap.paragraph_format
        cpf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cpf.first_line_indent = Cm(0)
        cpf.line_spacing = 1.0
        cpf.space_before = Pt(0)
        cpf.space_after = Pt(10)
        r = cap.add_run(f"Рисунок {self.fig_no}{sep}{caption}")
        _set_run_font(r, size=14, color="000000")
        self._need((height_cm + 0.9) * 28.35)
        return p

    def bullet_item(self, text, style="List Bullet", size=14, spacing=1.0):
        p = self.doc.add_paragraph(style=style)
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.line_spacing = spacing
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        run = p.add_run(text)
        _set_run_font(run, size=size, color="000000")
        lines = max(1, math.ceil(len(text) / CHARS_PER_LINE))
        self._need(lines * LINE_PT * spacing)
        return p

    def sub(self, text, size=14, spacing=1.5):
        """Подзаголовок внутри приложения — полужирный, с отступом."""
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.first_line_indent = Cm(1.25)
        pf.line_spacing = spacing
        pf.space_before = Pt(6)
        pf.space_after = Pt(0)
        pf.keep_with_next = True
        run = p.add_run(text)
        _set_run_font(run, size=size, bold=True, color="000000")
        self._need(LINE_PT * spacing + 8)
        return p

    def bold_line(self, text, size=14, spacing=1.5):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.first_line_indent = Cm(0)
        pf.line_spacing = spacing
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        run = p.add_run(text)
        _set_run_font(run, size=size, bold=True, color="000000")
        self._need(LINE_PT * spacing)
        return p

    def appendix_head(self, number, title):
        self.page_break()
        self.p_right(f"Приложение {number}")
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(0)
        pf.space_after = Pt(12)
        pf.keep_with_next = True
        run = p.add_run(title)
        _set_run_font(run, size=14, bold=True, color="000000")
        self._need(LINE_PT + 14)

    cls.p_right = p_right
    cls.fig = fig
    cls.bullet_item = bullet_item
    cls.sub = sub
    cls.bold_line = bold_line
    cls.appendix_head = appendix_head
    return cls


_extra_methods(Builder)
