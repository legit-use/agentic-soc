import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def markdown_to_docx(md_path, docx_path):
    print(f"Reading markdown: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = docx.Document()
    
    # Page setup: Standard A4 with 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    in_code_block = False
    code_lines = []
    in_table = False
    table_lines = []

    def flush_table():
        nonlocal table_lines, in_table
        if not table_lines:
            return
        
        # Parse markdown table
        rows_data = []
        for line in table_lines:
            clean = line.strip()
            if not clean or clean.startswith('|---') or clean.startswith('| :---') or clean.startswith('|:---') or '---' in clean.replace('|', '').replace(':', '').replace(' ', ''):
                continue
            cells = [c.strip() for c in clean.split('|')[1:-1]]
            if cells:
                rows_data.append(cells)
        
        if rows_data:
            num_rows = len(rows_data)
            num_cols = max(len(r) for r in rows_data)
            tbl = doc.add_table(rows=num_rows, cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl.autofit = True

            for r_idx, row in enumerate(rows_data):
                is_header = (r_idx == 0)
                for c_idx, cell_value in enumerate(row):
                    if c_idx < num_cols:
                        cell = tbl.cell(r_idx, c_idx)
                        cell.text = cell_value.replace('**', '').replace('`', '')
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.space_before = Pt(2)
                        run = p.runs[0]
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(10)

                        if is_header:
                            set_cell_background(cell, "1E293B")
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                        else:
                            if r_idx % 2 == 1:
                                set_cell_background(cell, "F8FAFC")
                            else:
                                set_cell_background(cell, "FFFFFF")
                            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                        
                        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            doc.add_paragraph() # Spacing
        table_lines = []
        in_table = False

    def flush_code():
        nonlocal code_lines, in_code_block
        if not code_lines:
            return
        code_text = "".join(code_lines)
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.right_indent = Inches(0.4)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        code_lines = []
        in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Handle Code Block Fences
        if stripped.startswith("```"):
            if in_code_block:
                flush_code()
            else:
                if in_table:
                    flush_table()
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Handle Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            flush_table()

        # Handle Horizontal Rules
        if stripped == "---":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run("―" * 45)
            run.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
            continue

        # Handle Headings
        if stripped.startswith("# "):
            h_text = stripped[2:].strip().replace("**", "")
            h = doc.add_heading(h_text, level=1)
            h.paragraph_format.space_before = Pt(18)
            h.paragraph_format.space_after = Pt(8)
            run = h.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
            continue

        if stripped.startswith("## "):
            h_text = stripped[3:].strip().replace("**", "")
            h = doc.add_heading(h_text, level=2)
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(6)
            run = h.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
            continue

        if stripped.startswith("### "):
            h_text = stripped[4:].strip().replace("**", "")
            h = doc.add_heading(h_text, level=3)
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
            run = h.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
            continue

        # Empty line
        if not stripped:
            continue

        # Bullet lists
        if stripped.startswith("* ") or stripped.startswith("- "):
            bullet_text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
            # Add runs with basic bold support
            parts = re.split(r'(\*\*.*?\*\*)', bullet_text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.font.bold = True
                else:
                    p.add_run(part.replace('`', ''))
            continue

        # Numbered lists
        match_num = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if match_num:
            num_text = match_num.group(2).strip()
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_after = Pt(2)
            parts = re.split(r'(\*\*.*?\*\*)', num_text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.font.bold = True
                else:
                    p.add_run(part.replace('`', ''))
            continue

        # Standard Paragraph
        p = doc.add_paragraph()
        parts = re.split(r'(\*\*.*?\*\*)', stripped)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                r = p.add_run(part[2:-2])
                r.font.bold = True
            else:
                p.add_run(part.replace('`', ''))

    if in_table:
        flush_table()
    if in_code_block:
        flush_code()

    print(f"Saving to DOCX: {docx_path}")
    doc.save(docx_path)
    print("Done! File generated successfully.")

if __name__ == "__main__":
    src = r"C:\Users\harsh\.gemini\antigravity\brain\bffe4271-730c-43de-bbbd-aa8a3e71fbdd\AEGIS_SOC_70_Page_Final_Thesis_Report.md"
    dst = r"c:\Users\harsh\OneDrive\Desktop\anti gravity  soc\AEGIS_SOC_Final_Project_Report.docx"
    markdown_to_docx(src, dst)
