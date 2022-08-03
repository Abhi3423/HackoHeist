from pdf2image import convert_from_bytes
import base64
import os

# pdf = convert_from_path('Pdfs/Trial1.pdf',  poppler_path = r"C:/poppler-22.01.0/Library/bin")


def pdfToImg(pdf_bytes, pdf_name):
  
  decoded = base64.decodebytes(pdf_bytes)
  pdf = convert_from_bytes(decoded)
  
  parent_dir = "./static/images/pdf_images/"
  path = os.path.join(parent_dir, pdf_name)
  os.mkdir(path)
  pages = 0

  for i in range(len(pdf)):
      pages += 1
    
        # Save pages as images in the pdf
      pdf[i].save('./images/page'+ str(i) +'.jpg', 'JPEG')
      pdf[i].save(f'{path}/page'+ str(i) +'.jpg', 'JPEG')
      
  return pages