"""
PDF Processing Module
Handles text extraction from PDFs and OCR for scanned documents.
"""

import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import sys


class PDFProcessor:
    """Handles PDF text extraction and OCR operations."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.check_tesseract_installation()
    
    def check_tesseract_installation(self):
        """
        Check if Tesseract is installed and accessible.
        Raises an exception if not found.
        """
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            # Try to find common Tesseract installation paths on Windows
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            
            tesseract_found = False
            for path in common_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    tesseract_found = True
                    break
            
            if not tesseract_found:
                raise RuntimeError(
                    "Tesseract OCR is not installed or not found in PATH.\n\n"
                    "Please install Tesseract OCR:\n"
                    "- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "- Linux: sudo apt-get install tesseract-ocr\n\n"
                    f"Original error: {str(e)}"
                )
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a text-based PDF using PyMuPDF.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: For other PDF processing errors
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Open the PDF
            doc = fitz.open(pdf_path)
            text_content = []
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
            
            doc.close()
            
            full_text = "\n".join(text_content)
            
            if not full_text.strip():
                return "[No text found - This might be a scanned PDF. Try using OCR instead.]"
            
            return full_text
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_with_ocr(self, pdf_path, progress_callback=None):
        """
        Extract text from a scanned PDF using OCR.
        Converts each page to an image and performs OCR.
        
        Args:
            pdf_path (str): Path to the PDF file
            progress_callback (callable): Optional callback function to report progress
                                        Called with (current_page, total_pages)
            
        Returns:
            str: OCR-extracted text from all pages
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: For other OCR processing errors
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Convert PDF pages to images
            # Using a lower DPI for faster processing, increase to 300 for better quality
            
            # Set Poppler path for Windows
            poppler_path = None
            if sys.platform == 'win32':
                from pathlib import Path
                local_poppler = Path(__file__).parent / "poppler" / "Library" / "bin"
                if local_poppler.exists():
                    poppler_path = str(local_poppler)
            
            images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)
            
            text_content = []
            total_pages = len(images)
            
            # Perform OCR on each page
            for page_num, image in enumerate(images, start=1):
                if progress_callback:
                    progress_callback(page_num, total_pages)
                
                # Perform OCR on the image
                text = pytesseract.image_to_string(image)
                text_content.append(f"--- Page {page_num} ---\n{text}\n")
            
            full_text = "\n".join(text_content)
            
            if not full_text.strip():
                return "[No text could be extracted via OCR. The PDF might be empty or the image quality is too poor.]"
            
            return full_text
            
        except Exception as e:
            raise Exception(f"Error performing OCR on PDF: {str(e)}")


# Simple test function
if __name__ == "__main__":
    processor = PDFProcessor()
    print("PDF Processor initialized successfully!")
    print("Tesseract version:", pytesseract.get_tesseract_version())
