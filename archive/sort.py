#sort_v2 for danish, pastry, kitchen orders

import glob
import pdfplumber
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import PyPDF2

page_id = 1                                             # fix overwrites for orders >1 page long

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
        path = ('input.pdf')
        pdf2 = PdfFileReader(path)
        pdf2_writer = PdfFileWriter()                   # declare write function
        pdf2_writer.addPage(pdf2.getPage(i))            # get page with PdfFileReader
        output_filename = 'input_{}_{}.pdf'.format(     # output file name format; order by ordernum and then page_id
            ordernum, page_id)
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
    merger((f'_{getfile}_output.pdf'), paths)           # writes back original file name
    print ('Created: _{}_output.pdf'.format(getfile))   # notify conclusion of script in console
for f in glob.glob("input*.pdf"):                       # removes all the split pages that were created
    os.remove(f)