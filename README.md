# PDF OCR Desktop Application

A cross-platform desktop application for extracting text from PDF files with OCR support for scanned documents.

## Features

- 📄 **Text Extraction**: Extract text from regular text-based PDFs
- 🔍 **OCR Support**: Convert scanned PDFs to searchable text using Tesseract OCR
- 📋 **Clipboard Integration**: Copy extracted text to clipboard
- 🎨 **Modern UI**: Clean and intuitive Tkinter interface
- ⚡ **Progress Tracking**: Real-time progress updates during OCR processing
- 🖥️ **Cross-Platform**: Works on Windows and Linux

## Prerequisites

### Python
- Python 3.8 or higher
- pip (Python package installer)

### Tesseract OCR
Tesseract OCR must be installed separately on your system:

#### Windows
1. Download the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer (recommended path: `C:\Program Files\Tesseract-OCR`)
3. The application will automatically detect Tesseract in common installation paths

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install tesseract
```

#### Verify Installation
```bash
tesseract --version
```

### Poppler (Required for OCR on Windows)
Poppler is required to convert PDF pages to images for OCR processing.

#### Automated Installation (Recommended)
Run the provided installer script:
```bash
python install_poppler.py
```

This will:
- Download Poppler for Windows
- Extract it to the project directory
- Configure the application to use it automatically

#### Manual Installation
1. Download Poppler from [oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract the archive
3. Add the `bin` folder to your system PATH, or
4. Place the extracted `poppler-XX.XX.X` folder in the project directory and rename it to `poppler`

#### Linux
Poppler is usually pre-installed. If not:
```bash
sudo apt-get install poppler-utils
```

## Installation

### 1. Clone or Download the Repository
```bash
cd c:\Users\Gustavo\Projects\pdf-ocr
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux:**
```bash
source venv/bin/activate
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

**With virtual environment activated:**
```bash
python main.py
```

**Or directly:**
```bash
python c:\Users\Gustavo\Projects\pdf-ocr\main.py
```

### Using the Application

1. **Select a PDF File**
   - Click the "Browse..." button
   - Select your PDF file from the file dialog

2. **Extract Text**
   - For regular PDFs with selectable text, click **"📄 Extract Text"**
   - For scanned PDFs or images, click **"🔍 OCR (Scanned PDF)"**

3. **View Results**
   - Extracted text will appear in the text area
   - Use **"📋 Copy to Clipboard"** to copy the text
   - Use **"🗑️ Clear"** to clear the text area

### Tips for Best Results

- **Text-based PDFs**: Use "Extract Text" for faster processing
- **Scanned PDFs**: Use "OCR (Scanned PDF)" for image-based documents
- **OCR Quality**: Higher quality scans produce better OCR results
- **Processing Time**: OCR can take several seconds per page depending on PDF size and complexity

## Building a Standalone Executable

To create a standalone executable that doesn't require Python installation:

### Install PyInstaller
```bash
pip install pyinstaller
```

### Build the Executable

**Windows:**
```bash
pyinstaller --onefile --windowed --name="PDF-OCR" --icon=NONE main.py
```

**Linux:**
```bash
pyinstaller --onefile --windowed --name="PDF-OCR" main.py
```

The executable will be created in the `dist` folder.

**Note:** You'll still need to install Tesseract OCR separately on the target system.

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| PyMuPDF | ≥1.23.0 | PDF text extraction |
| pytesseract | ≥0.3.10 | Python wrapper for Tesseract OCR |
| pdf2image | ≥1.16.3 | Convert PDF pages to images |
| Pillow | ≥10.0.0 | Image processing |

## Troubleshooting

### "Tesseract is not installed or not found in PATH"

**Solution:**
1. Install Tesseract OCR (see Prerequisites section)
2. Ensure Tesseract is in your system PATH, or
3. The application will automatically check common Windows installation paths

### "No text found - This might be a scanned PDF"

**Solution:**
- The PDF contains images rather than text
- Use the "OCR (Scanned PDF)" button instead

### OCR is very slow

**Solution:**
- OCR processing is CPU-intensive and can take time for large PDFs
- The progress bar shows the current page being processed
- Consider reducing the DPI in `pdf_processor.py` (line 109) for faster processing at the cost of accuracy

### Import errors or missing modules

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### pdf2image errors on Windows

**Solution:**
- pdf2image requires Poppler for Windows
- Download Poppler for Windows from [oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
- Extract and add the `bin` folder to your system PATH

## License

This project uses the following open-source libraries:
- **PyMuPDF**: AGPL v3 (free for non-commercial use)
- **Tesseract OCR**: Apache 2.0
- **pytesseract**: Apache 2.0
- **pdf2image**: MIT
- **Pillow**: HPND License

All libraries are free for non-commercial use.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed correctly
3. Ensure you're using compatible Python and library versions

## Project Structure

```
pdf-ocr/
├── main.py              # Main application with GUI
├── pdf_processor.py     # PDF processing and OCR logic
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Future Enhancements

Potential improvements for future versions:
- Support for multiple file formats (images, DOCX, etc.)
- Batch processing multiple PDFs
- Language selection for OCR
- Text editing capabilities
- Export to different formats (TXT, DOCX, etc.)
- Image preprocessing options for better OCR accuracy
