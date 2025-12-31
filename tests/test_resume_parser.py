import unittest
from tools.resume_parser import resume_parser
import os

class TestResumeParser(unittest.TestCase):

    def test_parse_dummy_resume(self):
        # Create a dummy resume for testing
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        file_path = "dummy_resume_for_test.pdf"

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.drawString(72, height - 72, "John Doe")
        c.drawString(72, height - 84, "Software Engineer")
        c.save()

        with open(file_path, "rb") as f:
            text = resume_parser(f)
        
        self.assertIn("John Doe", text)
        self.assertIn("Software Engineer", text)

        # Clean up the dummy file
        os.remove(file_path)

if __name__ == "__main__":
    unittest.main()
