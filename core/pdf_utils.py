"""
core/pdf_utils.py
-----------------
Shared helpers for reading and writing PDFs, extracted from main.ipynb.
"""

import os
import re
from fpdf import FPDF
from PyPDF2 import PdfReader
from core.config import OUTPUT_DIR


def read_pdf(file_path: str) -> str:
    """Extract text from all pages of a PDF file."""
    reader = PdfReader(file_path)
    return "\n".join(
        page.extract_text()
        for page in reader.pages
        if page.extract_text()
    )


def save_output(text: str, filename: str, table: bool = False, output_dir: str = OUTPUT_DIR) -> str:
    """
    Save text content as a PDF file.

    Args:
        text:       Raw text (or pipe-delimited table rows) to render.
        filename:   Output filename, e.g. "summary.pdf".
        table:      If True, render as a table (Day|Time Slot|Task|Duration|Priority).
        output_dir: Directory to write the file into.

    Returns:
        Absolute path of the written PDF.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    if table:
        lines = [line.strip() for line in text.split("\n") if line.strip() and "|" in line]

        headers = ["Day", "Time Slot", "Task", "Duration", "Priority"]
        col_widths = [30, 40, 70, 25, 25]

        pdf.set_fill_color(200, 200, 200)
        pdf.set_font("Helvetica", "B", 11)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align="C", fill=True)
        pdf.ln()

        pdf.set_font("Helvetica", size=10)
        for line in lines:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 5:
                for i, val in enumerate(parts):
                    val_clean = val.encode("latin-1", "replace").decode("latin-1")
                    pdf.cell(col_widths[i], 8, val_clean, border=1, align="C")
                pdf.ln()
    else:
        # Strip markdown formatting
        clean_text = text
        clean_text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", clean_text)
        clean_text = re.sub(r"\*\*(.+?)\*\*", r"\1", clean_text)
        clean_text = re.sub(r"\*(.+?)\*", r"\1", clean_text)
        clean_text = re.sub(r"__(.+?)__", r"\1", clean_text)
        clean_text = re.sub(r"_(.+?)_", r"\1", clean_text)

        clean_text = (
            clean_text
            .replace("\u2022", "- ")
            .replace("\u2013", "-")
            .replace("\u2014", "-")
            .replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2026", "...")
            .replace("\u2605", "*")
        )

        max_chars = 72  # approx chars per line at font size 11

        for line in clean_text.split("\n"):
            line_clean = line.encode("latin-1", "ignore").decode("latin-1").strip()

            if not line_clean:
                pdf.ln(5)
                continue

            if line_clean.isupper() or (len(line_clean) < 100 and line == line.strip() and not line.startswith("-")):
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 10, line_clean, new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", size=11)
            else:
                if len(line_clean) <= max_chars:
                    pdf.cell(0, 6, line_clean, new_x="LMARGIN", new_y="NEXT")
                else:
                    words = line_clean.split()
                    current_line = ""
                    for word in words:
                        test_line = current_line + (" " if current_line else "") + word
                        if len(test_line) <= max_chars:
                            current_line = test_line
                        else:
                            if current_line:
                                pdf.cell(0, 6, current_line, new_x="LMARGIN", new_y="NEXT")
                            current_line = word
                    if current_line:
                        pdf.cell(0, 6, current_line, new_x="LMARGIN", new_y="NEXT")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    pdf.output(output_path)
    return os.path.abspath(output_path)
