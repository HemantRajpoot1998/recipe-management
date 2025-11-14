from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


from django.http import FileResponse


from .models import Recipe


def recipe_to_pdf_response(recipe: Recipe):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter


    margin = 40
    y = height - margin
    c.setFont('Helvetica-Bold', 18)
    c.drawString(margin, y, recipe.title)
    y -= 24


    c.setFont('Helvetica', 10)
    c.drawString(margin, y, f"Prep: {recipe.prep_duration_minutes} mins Cook: {recipe.cook_duration_minutes} mins")
    y -= 20


    # Description
    textobj = c.beginText(margin, y)
    textobj.setFont('Helvetica', 10)
    for line in recipe.description.splitlines():
        textobj.textLine(line)
    c.drawText(textobj)
    y = textobj.getY() - 10


    # Ingredients
    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin, y, 'Ingredients:')
    y -= 16
    c.setFont('Helvetica', 10)
    for ing in recipe.ingredients.all():
        c.drawString(margin + 10, y, f"- {ing.name} {('('+ing.quantity+')') if ing.quantity else ''}")
        y -= 14
        if y < 72:
            c.showPage()
            y = height - margin


    # Steps
    c.setFont('Helvetica-Bold', 12)
    c.drawString(margin, y, 'Steps:')
    y -= 16
    c.setFont('Helvetica', 10)
    for step in recipe.steps.all():
        c.drawString(margin + 10, y, f"{step.order}. {step.description[:180]}")
        y -= 14
        if y < 72:
            c.showPage()
            y = height - margin


    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{recipe.title}.pdf")