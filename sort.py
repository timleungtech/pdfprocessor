#final.py
import glob
import pdfplumber
import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

z = int(input("How many pages? "))

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf2 = PdfFileReader(path)

with pdfplumber.open('input.pdf') as pdf:
    for i in range(z):
        first_page = pdf.pages[i]
        ordernum = first_page.extract_text()[10:25]
        path = ('input.pdf')
        fname = os.path.splitext(os.path.basename(path))[0]
        pdf2 = PdfFileReader(path)

        pdf2_writer = PdfFileWriter()
        pdf2_writer.addPage(pdf2.getPage(i))
        output_filename = '{}_{}.pdf'.format(
            fname, ordernum)
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
    merger('output.pdf', paths)
#    now = datetime.now()
#    current_time = now.strftime("%H_%M_%S")
#    merger((f'{current_time}.pdf'), paths)



