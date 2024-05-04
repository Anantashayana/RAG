# To read the PDF
import PyPDF2
# To extract the images from the PDFs
from PIL import Image
import pdf2image
from pdf2image import convert_from_path
# To perform OCR to extract text from images 
import pytesseract 
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class PdfOcrCorpus:
    def __init__(self):#, folder_path):
        # self.folder_path = folder_path
        text_data_file = ""
        
    def process(self)->None:
        print("Processing Started.")
        # Check whether folder is valid or not
        if self.__is_dir_exists():        
            print("Directory exists.")
            text_data_file = os.path.join(self.folder_path, 
                            "text_data_ocr_corpus.txt")
            text_data_file = os.path.abspath(text_data_file)
            pdf_files = self.__get_pdf_files()
            no_files = len(pdf_files)
            print("No. pdf files = ", no_files)
            #print(pdf_files)
            #text_data = ["File 1", "File 2"]
            with open(text_data_file, 'w') as txt_file:    
                for index in range(0, no_files):
                    file = pdf_files[index]
                    print("Processing started for ",file)
                    self.__process_pdffile(file, txt_file)                    
                    print("Processing completed for ",file)
                    #txt_file.write(text_data[index])
                    if (index != (no_files -1)):
                        txt_file.write("\n")
                txt_file.close()
                
            print("Text Data Written in file, ", text_data_file)        
        else:
            print("Directory Path does not exists.")
            
        return 
    

    
    def __process_pdffile(self, file_name):#, txt_file)->None:
        doc = convert_from_path(file_name, poppler_path=r'C:\Release-24.02.0-0\poppler-24.02.0\Library\bin')
        # Convert PDF to images and create searchable PDF
        # doc = pdf2image.convert_from_path(file_name)        
        pages_data = []
        for page_number, page_data in enumerate(doc):            
            txt = pytesseract.image_to_string(page_data)
            #print(txt)
            txt_lines = txt.split("\n")            
            pages_data.append(txt_lines)
            #txt_lines = ''.join(txt_lines)
            #print(txt_lines)
            
            #print("Page # {} - {}".format(str(page_number),txt)) 
            
        text_data = ""
        for page_data in pages_data: 
            txt_lines = ''.join(page_data)           
            text_data = text_data + " " + txt_lines
            
        #print(text_data)
        # txt_file.write(text_data)

        return text_data
            

    def __is_dir_exists(self)->bool:
        is_valid_dir = False
        # Convert the path to Asbolute Path
        dir_path = os.path.abspath(self.folder_path)
        print("Directory = ", self.folder_path)
        print("Asbolute Directory = ", dir_path)

        # Check whether folder exists or not
        if os.path.isdir(dir_path):
            is_valid_dir = True
        
        return is_valid_dir
    

    def __get_pdf_files(self)->list:
        dir_path = os.path.abspath(self.folder_path)
        files = []
        for f in os.listdir(dir_path):            
            file = os.path.join(dir_path,f)
            #print(file)            
            if os.path.isfile(file): 
                name, extn = os.path.splitext(file) 
                #print(extn)              
                if  ((extn == ".PDF") or (extn == ".pdf")):
                    files.append(file)    

        #print(files)
        return files
    

    def simplePdftoText(self, path):
        return self.__process_pdffile(path)


