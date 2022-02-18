import datetime
from docx.shared import Cm
from docxtpl import DocxTemplate,InlineImage

def get_context(brand,model,fuel_cons,price):
    return {
        'brand':brand,
        'model':model,
        'fuel_cons':fuel_cons,
        'price':price,
    }
def from_car(brand,model,fuel_cons,price,template):
    template =DocxTemplate(template)
    context = get_context(brand,model,fuel_cons,price)

    template.render(context)
    template.save()