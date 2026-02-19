def save_as_pdf(filename: str, content: str):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from textwrap import wrap

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Courier", 10)
    y = 750
    max_chars = 80  # Approximate max characters per line at 10pt Courier
    
    for line in content.split("\n"):
        # Wrap long lines to fit on page
        wrapped_lines = wrap(line, width=max_chars) if line else [""]
        
        for wrapped_line in wrapped_lines:
            if y < 50:  # Start new page if running out of space
                c.showPage()
                c.setFont("Courier", 10)
                y = 750
            c.drawString(50, y, wrapped_line)
            y -= 15
    
    c.save()