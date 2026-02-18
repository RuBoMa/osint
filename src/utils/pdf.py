def save_as_pdf(filename: str, content: str):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Courier", 10)
    y = 750
    
    for line in content.split("\n"):
        if y < 50:  # Start new page if running out of space
            c.showPage()
            c.setFont("Courier", 10)
            y = 750
        c.drawString(50, y, line)
        y -= 15
    
    c.save()