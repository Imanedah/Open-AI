from fpdf import FPDF
import io
import pandas as pd

def convert_text_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def convert_text_to_csv(text):
    lines = text.split("\n")
    data = {"Résumé": lines}
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')
