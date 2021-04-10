#pdfparser.py

import pdfplumber

#file = input("PDF file: ")
z = int(3) #int(input("How many pages? "))
with pdfplumber.open("input.pdf") as pdf:
    for i in range(z):
        first_page = pdf.pages[i]
        ordernum = first_page.extract_text()[10:25]
        print (ordernum)