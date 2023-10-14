#consolidated picklist by customer sorted by route
#for bread, dd, retail orders

import glob
import pdfplumber
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import PyPDF2
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import red
from reportlab.lib.colors import Color, red

dictroute = {
  "000113": "3",
  "000114": "1",
  "000118": "2",
  "000120": "3",
  "000123": "1",
  "000127": "2",
  "000130": "3",
  "000134": "1",
  "000136": "1",
  "000138": "3",
  "000142": "2",
  "000144": "1",
  "000146": "1",
  "000148": "2",
  "000149": "2",
  "000151": "4",
  "000153": "3",
  "000154": "1",
  "000156": "3",
  "000401": "4",
  "000402": "4",
  "000403": "4",
  "003002": "3",
  "003003": "1",
  "003004": "1",
  "003005": "1",
  "003006": "3",
  "003007": "2",
  "003008": "3",
  "003009": "2",
  "003010": "2",
  "003011": "3",
  "003013": "3"
}

dictCustomer = {
  "000113": "SOHO  ",
  "000114": "MADISON",
  "000118": "FIRST AVE",
  "000120": "  8TH ",
  "000123": "LINCOLN",
  "000127": "BRYANT ",
  "000130": "TRIBECA",
  "000134": "MINERAL",
  "000136": "   88 ",
  "000138": "BLEECKER",
  "000142": " GCW  ",
  "000144": "  E97 ",
  "000146": "  E83 ",
  "000148": "  E65 ",
  "000149": "  W55 ",
  "000151": "ROOSEVELT",
  "000153": "85 BROAD",
  "000154": "SAILBOAT",
  "000156": "SOUTH END",
  "000401": "N.CANAAN",
  "000402": "  RYE ",
  "000403": "GREENWICH",
  "003002": "921 BWAY",
  "003003": "   58 ",
  "003004": "   87 ",
  "003005": "   76 ",
  "003006": "JORALEMON",
  "003007": "   56 ",
  "003008": "   36 ",
  "003009": "   38 ",
  "003010": "   43 ",
  "003011": "   41 ",
  "003013": "   29 "
}

page_id = 1 # fix for orders >1 page long
outputName= ""

getfile = str(input("File name: "))
os.rename(f"{getfile}.pdf","input.pdf")

pdfFileObj = open('input.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
lastpage = pdfReader.numPages

with pdfplumber.open('input.pdf') as pdf:
    # fix blank last page
    if pdf.pages[lastpage-1].extract_text().find('Customer: ') == -1:
        lastpage = lastpage - 1

    for i in range(lastpage):
        curr_page = pdf.pages[i]

        # print(curr_page.extract_text())
        customer_idx = curr_page.extract_text().index('Customer: ') + 10
        # print(customer_idx)
        # print(curr_page.extract_text()[customer_idx:customer_idx+4])
        customer_id = curr_page.extract_text()[customer_idx:customer_idx+4]
        is_mpq = customer_id.isnumeric()
        # print(customer_id)
        # print(is_mpq)
        if (is_mpq == True):
            customer_id = '00' + customer_id
        else:
            customer_id = '000' + customer_id
        customer_id = customer_id[0:6]
        # print(customer_id)
        # print(len(customer_id))

        route = dictroute.get(f"{customer_id}")
        customer = dictCustomer.get(f"{customer_id}")
        path = ('input.pdf')
        pdf2 = PdfFileReader(path)
        pdf2_writer = PdfFileWriter()
        pdf2_writer.addPage(pdf2.getPage(i))
        output_filename = 'input_{}_{}_{}.pdf'.format(
            route, customer_id, page_id)
        with open(output_filename, 'wb') as out:
            pdf2_writer.write(out)
        print('Created: {}'.format(output_filename))

#bottom text start
        redtransparent = Color( 255, 0, 0, alpha=0.4)
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        # can.setFont("Courier-Bold", 42)
        can.setFillColor(redtransparent)
        # can.drawString(12, 15, f'ROUTE {route} - {customer}')
        can.setFont("Helvetica-Bold", 110)
        if (len(customer) == 6):
            can.setFont("Helvetica-Bold", 185)
        if (len(customer) >= 9):
            can.setFont("Helvetica-Bold", 95)
        can.rotate(90)
        can.setPageSize((850, 600))
        can.drawString(12, -770, f'{customer}')
        # can.drawString(12, 18, f'{customer}')
        can.setFont("Helvetica-Bold", 20)
        can.drawString(20, -70, f'{route}')
        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(output_filename, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page2 = existing_pdf.getPage(0)
        page2.mergePage(new_pdf.getPage(0))
        output.addPage(page2)
        outputStream = open(f'footer_{route}_{customer_id}_{page_id}.pdf', "wb")
        output.write(outputStream)
        print(f'Created: footer_{route}_{customer_id}_{page_id}.pdf')
        outputStream.close()
        page_id += 1
# #bottom text end

for f in glob.glob("input*.pdf"):
    os.remove(f)

#merge page with footer start
def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
if __name__ == '__main__':
    paths = glob.glob('footer_*.pdf')
    paths.sort()
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    merger((f'_{getfile}_output_{current_time}.pdf'), paths)
    outputName = (f'_{getfile}_output_{current_time}.pdf')
    print ('Created: _{}_output_{}.pdf'.format(getfile, current_time))
for f in glob.glob("footer*.pdf"):
    os.remove(f)
#merge page with footer end
