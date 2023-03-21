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

page_id = 1                                             # fix for orders >1 page long

getfile = str(input("File name: "))                     # prompt user for file name
os.rename(f"{getfile}.pdf","input.pdf")                 # renames file to input.pdf

def pdf_splitter(path):                                 # splits pdf pages into separate files
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf2 = PdfFileReader(path)

pdfFileObj = open('input.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
lastpage = pdfReader.numPages                           # assign lastpage

with pdfplumber.open('input.pdf') as pdf:               # open and read input pdf
    for i in range(lastpage):                           # iterate to lastpage
        first_page = pdf.pages[i]
        ordernum = first_page.extract_text()[10:16]     # extracts chars 10 to 16 on pdf
        route = dictroute.get(f"{ordernum}")            # assign route via dictroute above
        path = ('input.pdf')
        pdf2 = PdfFileReader(path)
        pdf2_writer = PdfFileWriter()                   # declare write function
        pdf2_writer.addPage(pdf2.getPage(i))            # get page with PdfFileReader
        output_filename = 'input_{}_{}_{}.pdf'.format(  # output file name format; order by route, ordernum, then page_id
            route, ordernum, page_id)
        page_id += 1                                    # iterate page_id to fix overwrite orders >1 page long
        with open(output_filename, 'wb') as out:
            pdf2_writer.write(out)
        print('Created: {}'.format(output_filename))    # displays page creation process in console
if __name__ == '__main__':
    path = ('input.pdf')
    pdf_splitter(path)

def merger(output_path, input_paths):                   # merges the split pages back together
    pdf_merger = PdfFileMerger()
    file_handles = []
    for path in input_paths:
        pdf_merger.append(path)
    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)
if __name__ == '__main__':
    paths = glob.glob('input_*.pdf')                    # merges files with file name input_*
    paths.sort()
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    merger((f'_{getfile}_output_{current_time}.pdf'), paths)                # writes back original file name, with current time to prevent overwrite of bread orders
    print ('Created: _{}_output_{}.pdf'.format(getfile, current_time))      # notify conclusion of script in console
for f in glob.glob("input*.pdf"):                                           # removes all the split pages that were created
    os.remove(f)