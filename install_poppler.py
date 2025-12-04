"""
Poppler Installation Helper for Windows
Downloads and sets up Poppler for pdf2image
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

POPPLER_VERSION = "24.08.0-0"
POPPLER_URL = f"https://github.com/oschwartz10612/poppler-windows/releases/download/v{POPPLER_VERSION}/Release-{POPPLER_VERSION}.zip"
INSTALL_DIR = Path(__file__).parent / "poppler"


def download_poppler():
    """Download Poppler for Windows."""
    print(f"Downloading Poppler {POPPLER_VERSION}...")
    print(f"URL: {POPPLER_URL}")
    
    zip_path = "poppler.zip"
    
    try:
        urllib.request.urlretrieve(POPPLER_URL, zip_path)
        print("✓ Download complete")
        return zip_path
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None


def extract_poppler(zip_path):
    """Extract Poppler archive."""
    print("Extracting Poppler...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("poppler_temp")
        
        # Move the poppler-XX.XX.X folder contents to our install dir
        temp_dir = Path("poppler_temp")
        poppler_folder = list(temp_dir.glob("poppler-*"))[0]
        
        if INSTALL_DIR.exists():
            shutil.rmtree(INSTALL_DIR)
        
        shutil.move(str(poppler_folder), str(INSTALL_DIR))
        
        # Cleanup
        shutil.rmtree(temp_dir)
        os.remove(zip_path)
        
        print(f"✓ Poppler extracted to: {INSTALL_DIR}")
        return True
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False


def update_pdf_processor():
    """Update pdf_processor.py to use local Poppler."""
    print("Updating pdf_processor.py...")
    
    processor_file = Path(__file__).parent / "pdf_processor.py"
    
    try:
        with open(processor_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add poppler_path parameter to convert_from_path call
        if 'poppler_path=' not in content:
            # Find the convert_from_path line and add poppler_path
            old_line = 'images = convert_from_path(pdf_path, dpi=200)'
            new_line = '''# Set Poppler path for Windows
            poppler_path = None
            if sys.platform == 'win32':
                local_poppler = Path(__file__).parent / "poppler" / "Library" / "bin"
                if local_poppler.exists():
                    poppler_path = str(local_poppler)
            
            images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)'''
            
            content = content.replace(old_line, new_line)
            
            # Add Path import if not present
            if 'from pathlib import Path' not in content:
                content = content.replace('import sys', 'import sys\nfrom pathlib import Path')
            
            with open(processor_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ pdf_processor.py updated")
            return True
    except Exception as e:
        print(f"✗ Update failed: {e}")
        return False


def main():
    """Main installation process."""
    print("=" * 60)
    print("Poppler Installation Helper for Windows")
    print("=" * 60)
    print()
    
    # Check if already installed
    if INSTALL_DIR.exists():
        print(f"Poppler is already installed at: {INSTALL_DIR}")
        response = input("Do you want to reinstall? (y/n): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            return
    
    # Download
    zip_path = download_poppler()
    if not zip_path:
        print("\n✗ Installation failed at download step")
        return
    
    # Extract
    if not extract_poppler(zip_path):
        print("\n✗ Installation failed at extraction step")
        return
    
    # Update pdf_processor.py
    if not update_pdf_processor():
        print("\n✗ Installation failed at update step")
        return
    
    print()
    print("=" * 60)
    print("✓ Poppler installation complete!")
    print("=" * 60)
    print()
    print(f"Poppler installed at: {INSTALL_DIR}")
    print(f"Binaries location: {INSTALL_DIR / 'Library' / 'bin'}")
    print()
    print("You can now use OCR functionality in the PDF OCR application.")
    print()


if __name__ == "__main__":
    main()
