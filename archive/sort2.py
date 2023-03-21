#sort_v2 for danish, pastry, kitchen orders
import glob
import pdfplumber
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import PyPDF2

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
        path = ('input.pdf')
#        fname = os.path.splitext(os.path.basename(path))[0]
        pdf2 = PdfFileReader(path)
        pdf2_writer = PdfFileWriter()
        pdf2_writer.addPage(pdf2.getPage(i))
        output_filename = 'input_{}_{}.pdf'.format(
            ordernum, page_id)
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
    merger((f'_{getfile}_output.pdf'), paths)
    print ('Created: _{}_output.pdf'.format(getfile))
for f in glob.glob("input*.pdf"):
    os.remove(f)