import datetime
# from docxtpl import DocxTemplate
# from docxtpl import InlineImage
from docx.shared import Cm
from docxtpl import DocxTemplate,InlineImage

#Возвращает словарь аргументов
def get_context(company, result_sku_list):
    return {
        'retailer': company,
        'sku_list': result_sku_list,
    }

def from_template(company,result_sku_list,template,signature):
    template=DocxTemplate(template)
    context = get_context(company,result_sku_list)

    img_size = Cm(15)
    acc = InlineImage(template,signature,img_size)
    context['acc']=acc

    template.render(context)
    template.save(company + ' ' + str(datetime.datetime.now().date()) + ' report.docx')

def generate_report(company,result_sku_list):
    template = '../lesson_5/7.2 job_doc/report.docx'
    signature = '../lesson_5/7.2 job_doc/acc.png'
    document = from_template(company,result_sku_list,template,signature)

def toFixed(numObj,digits=0):
    return f"{numObj:.{digits}f}"

generate_report('Ozon',[0.78, 0.12, 0.05, 0.01, 0.01])