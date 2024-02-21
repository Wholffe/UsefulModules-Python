from PyPDF2 import PdfMerger
import os

###Settings(optional)###
path:str = r''
pdf_name:str = ''

######
while path == '':
    path = input('Merging PDF files from path: ')
while pdf_name == '':
    pdf_name = input('Merged PDF name: ')
######

###Script###
def main(path, pdf_name):
    if not os.path.exists(path):
        print('Error! Please use a valid path with PDF files.')
        return
    pdf_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        if file_path.endswith('.pdf'):
            pdf_files.append(file_path)
    if len(pdf_files) < 1:
        print('No files to merch')
        return
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    output_file_path = os.path.join(path,pdf_name+'.pdf')
    with open(output_file_path,'wb') as output_file:
        merger.write(output_file)
    print('Files merged')

if __name__=='__main__':
    main(path, pdf_name)