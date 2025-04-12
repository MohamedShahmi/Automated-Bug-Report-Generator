
from fpdf import FPDF
import os

def generate_pdf(bugs, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, bug in enumerate(bugs):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Bug {i + 1}: {bug['title']}", ln=True)

        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"Description:\n{bug['description']}\n")
        pdf.multi_cell(0, 10, f"Logs:\n{bug['log']}\n")

        if bug["screenshot"] and os.path.exists(bug["screenshot"]):
            pdf.image(bug["screenshot"], w=100)

    pdf.output(output_path)
