## Summary
Python script that sorts pages of an inputted PDF file by extracting text from each page of the original document. 

## How it works 
Using the PyPDF library, the script splits the inputted PDF file by pages and extracts the text on each page. Then, it takes the customer_id value based on string position and renames the file based on the customer_id, customer_name, and customer_route in hash tables provided in the top of the document. page_number is also included to prevent overwriting of invoices from the same customer. The newly renamed PDF files get merged back together to one sorted PDF file. Lastly, inputted PDF and all originally created split pages and are removed. 

Using the ReportLab library, watermarks are added behind each PDF page. A hash map was created to reference what the watermarks will print behind the pages. 

## Time complexity 
This script runs at O(n) time complexity. Hash tables are included in the beginning of the document to help shorten time. The watermark runs as a different instance from the PyPDF processes, which doubles the time and space required. This is the reason why it is included only in scripts that need it (e.g. sortbyroute).

## Room for improvement
* Optimize the space complexity by compressing the outputted PDF files. The new PDF created after both the PyPDF merger process and inserting the ReportLab watermark process is almost 10x in size.
* ~~Connect the script to a more user-friendly front end interface.~~ View full app here: https://github.com/timleungtech/pdf-processor-react-flask

![sample](https://github.com/timleungtech/pdfprocessor/blob/master/sample.jpg)
![sample2](https://github.com/timleungtech/pdfprocessor/blob/master/sample2.jpg)
