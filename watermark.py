from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter,A4
Path='watermark.pdf'
c=canvas.Canvas(Path)
c.translate(cm,cm)
c.setFont('Helvetica',20)
c.setFillColorCMYK(0, 0, 0, 0, alpha=0.7)
c.rect(204, 199, 157, 15, stroke=0, fill=1)
c.setFillColorCMYK(0, 0, 0, 100, alpha=0.7)
c.drawString(cm*6.4,cm*0.81,"thejan64go@gmail.com")
c.drawString(cm*6.4,cm*14.81,"thejan64go@gmail.com")
c.drawString(cm*6.4,cm*26.81,"thejan64go@gmail.com")
c.setFont('Helvetica',10)
c.drawString(cm*0,cm*27.81,"thejan64go@gmail.com")
c.showPage()
c.save()