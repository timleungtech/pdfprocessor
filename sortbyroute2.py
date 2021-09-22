#sortbyroute_v2 for bread, dd, retail orders
import glob
import pdfplumber
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import PyPDF2
from datetime import datetime

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
  "000156": "3",
  "000401": "4",
  "000402": "4",
  "000403": "4",
  "003002": "3",   #3002
  "003003": "2",   #3003
  "003004": "1",   #3004
  "003005": "1",   #3005
  "003006": "3",   #3006
  "003007": "2",   #3007
  "003008": "3",   #3008
  "003009": "2",   #3009
  "003010": "2",   #3010
  "003011": "2",   #3011
  "003013": "3"    #3013
}

page_id = 1 # fix for orders >1 page long

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
        route = dictroute.get(f"{ordernum}")   #z puts unallocated stores on top
        path = ('input.pdf')
#        fname = os.path.splitext(os.path.basename(path))[0]
        pdf2 = PdfFileReader(path)
        pdf2_writer = PdfFileWriter()
        pdf2_writer.addPage(pdf2.getPage(i))
        output_filename = 'input_{}_{}_{}.pdf'.format(
            route, ordernum, page_id)
        page_id += 1
        with open(output_filename, 'wb') as out:
            pdf2_writer.write(out)
        print('Created: {}'.format(output_filename))
if __name__ == '__main__':
    path = ('input.pdf')
    pdf_splitter(path)

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
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    merger((f'_{getfile}_output_{current_time}.pdf'), paths)
    print ('Created: _{}_output_{}.pdf'.format(getfile, current_time))
for f in glob.glob("input*.pdf"):
    os.remove(f)