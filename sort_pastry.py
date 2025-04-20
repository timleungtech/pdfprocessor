#consolidated picklist by customer sorted by quantity
#for pastry orders

import glob
import pdfplumber
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import PyPDF2

routes = {
  "000113": "9",
  "000114": "9",
  "000118": "9",
  "000120": "9",
  "000123": "9",
  "000127": "9",
  "000130": "9",
  "000134": "9",
  "000136": "9",
  "000138": "9",
  "000142": "9",
  "000144": "9",
  "000146": "9",
  "000148": "9",
  "000149": "9",
  "000151": "0",
  "000153": "9",
  "000154": "9",
  "000156": "9",
  "000401": "1",
  "000402": "2",
  "000403": "3",
  "003002": "9",
  "003003": "9",
  "003004": "9",
  "003005": "9",
  "003006": "9",
  "003007": "9",
  "003008": "9",
  "003009": "9",
  "003010": "9",
  "003011": "9",
  "003013": "9"
}

page_id = 1 # fix for orders >1 page long
output_file_name= ""

get_file = str(input("File name: "))
os.rename(f"{get_file}.pdf","input.pdf")

pdfFileObj = open('input.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
last_page = pdfReader.numPages

with pdfplumber.open('input.pdf') as pdf:
    # fix blank last page
    if pdf.pages[last_page - 1].extract_text().find('Customer: ') == -1:
        last_page = last_page - 1

    for i in range(last_page):
        curr_page = pdf.pages[i]

        # get quantities
        idx_last_period = curr_page.extract_text().rfind('.')
        idx_penultimate_period = curr_page.extract_text().rfind('.', 0, curr_page.extract_text().rfind('.'))
        quantity = curr_page.extract_text()[idx_penultimate_period + 4:idx_last_period]
        quantity = quantity.rjust(6, '0')
        # print(quantity)

        customer_idx = curr_page.extract_text().index('Customer: ') + 10
        customer_id = curr_page.extract_text()[customer_idx:customer_idx + 4]
        is_mpq = customer_id.isnumeric()

        if (is_mpq == True):
            customer_id = '00' + customer_id
        else:
            customer_id = '000' + customer_id
        customer_id = customer_id[0:6]

        route = routes.get(customer_id)
        # customer_name = customer_names.get(customer_id)
        path = ('input.pdf')
        pdf_reader = PdfFileReader(path)
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(i))
        output_page_name = 'input_{}_{}_{}_{}.pdf'.format(
            route, quantity, customer_id, page_id)
        with open(output_page_name, 'wb') as out:
            pdf_writer.write(out)
        print(f'Created: {output_page_name}')
        page_id += 1

def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
if __name__ == '__main__':
    paths = glob.glob('input_*.pdf')
    paths.sort()
    merger((f'_{get_file}_output.pdf'), paths)
    print ('Created: _{}_output.pdf'.format(get_file))
for f in glob.glob("input*.pdf"):
    os.remove(f)
