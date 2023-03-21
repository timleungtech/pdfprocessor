#sortbyroute_v3 for bread, dd, retail orders
#added string of overlay
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

dictroute = {
  "000113": "3",
  "000114": "1",
  "000118": "1",
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
  "003003": "2",
  "003004": "1",
  "003005": "1",
  "003006": "3",
  "003007": "2",
  "003008": "3",
  "003009": "2",
  "003010": "2",
  "003011": "2",
  "003013": "3"
}

dictCustomer = {
  "000113": "SOHO",
  "000114": "MADISON",
  "000118": "FIRST AVE",
  "000120": "8TH ST",
  "000123": "LINCOLN",
  "000127": "BRYANT",
  "000130": "TRIBECA",
  "000134": "MINERAL",
  "000136": "CARNEGIE",
  "000138": "BLEECKER",
  "000142": "GCW",
  "000144": "E 97TH ST",
  "000146": "E 83RD ST",
  "000148": "E 65TH ST",
  "000149": "W 55TH ST",
  "000151": "ROOSEVELT",
  "000153": "85 BROAD",
  "000154": "SAILBOAT",
  "000156": "SOUTH END",
  "000401": "NEW CANAAN",
  "000402": "RYE",
  "000403": "GREENWICH",
  "003002": "921 BWAY",
  "003003": "1800 BWAY",
  "003004": "1535 3RD AVE",
  "003005": "2161 BWAY",
  "003006": "210 JORALEMON",
  "003007": "1377 6TH AVE",
  "003008": "400 5TH AVE",
  "003009": "1400 BWAY",
  "003010": "685 3RD AVE",
  "003011": "370 LEX",
  "003013": "339 7TH AVE"
}

page_id = 1 # fix for orders >1 page long
outputName= ""

getfile = str(input("File name: "))
os.rename(f"{getfile}.pdf","input.pdf")

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf2 = PdfFileReader(path)

pdfFileObj = open('input.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
lastpage = pdfReader.numPages

with pdfplumber.open('input.pdf') as pdf:
    for i in range(lastpage):
        first_page = pdf.pages[i]
        ordernum = first_page.extract_text()[10:16]
        route = dictroute.get(f"{ordernum}")
        customer = dictCustomer.get(f"{ordernum}")
        path = ('input.pdf')
        pdf2 = PdfFileReader(path)
        pdf2_writer = PdfFileWriter()
        pdf2_writer.addPage(pdf2.getPage(i))
        output_filename = 'input_{}_{}_{}.pdf'.format(
            route, ordernum, page_id)
        with open(output_filename, 'wb') as out:
            pdf2_writer.write(out)
        print('Created: {}'.format(output_filename))
#bottom text start
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Courier", 42)
        can.setFillColor(red)
        can.drawString(10, 15, f'{customer} - ROUTE {route}')
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
        outputStream = open(f'footer_{route}_{ordernum}_{page_id}.pdf', "wb")
        output.write(outputStream)
        print(f'Created: footer_{route}_{ordernum}_{page_id}.pdf')
        outputStream.close()
#bottom text end
        page_id += 1

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
