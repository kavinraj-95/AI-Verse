from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_resume():
    c = canvas.Canvas("dummy_resume.pdf", pagesize=letter)
    width, height = letter

    c.drawString(72, height - 72, "John Doe")
    c.drawString(72, height - 84, "Software Engineer")

    c.drawString(72, height - 120, "Skills:")
    c.drawString(90, height - 132, "- Python")
    c.drawString(90, height - 144, "- LangChain")
    c.drawString(90, height - 156, "- Streamlit")

    c.drawString(72, height - 192, "Experience:")
    c.drawString(90, height - 204, "Software Engineer at Acme Inc. (2022-Present)")
    
    c.drawString(72, height - 240, "Implied Interests:")
    c.drawString(90, height - 252, "AI, Machine Learning, Agentic Systems")

    c.save()

if __name__ == "__main__":
    create_dummy_resume()
