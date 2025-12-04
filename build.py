"""
Build Script for PDF OCR Desktop Application
This script automates the build process and downloads necessary dependencies.
"""

import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
from pathlib import Path

# Configuration
TESSERACT_URL = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
POPPLER_URL = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
TESSERACT_INSTALLER = "tesseract-installer.exe"
POPPLER_ZIP = "poppler.zip"

class Builder:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.installer_dir = self.project_dir / "installer_files"
        
    def download_file(self, url, filename):
        """Download a file with progress indication."""
        print(f"\nDownloading {filename}...")
        filepath = self.installer_dir / filename
        
        if filepath.exists():
            print(f"{filename} already exists, skipping download.")
            return filepath
            
        try:
            def progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(100, (downloaded / total_size) * 100) if total_size > 0 else 0
                print(f"\rProgress: {percent:.1f}%", end='', flush=True)
            
            urllib.request.urlretrieve(url, filepath, progress)
            print("\nDownload complete!")
            return filepath
        except Exception as e:
            print(f"\nError downloading {filename}: {e}")
            return None
    
    def download_dependencies(self):
        """Download Tesseract and Poppler if not present."""
        print("\n" + "="*60)
        print("STEP 1: Downloading Dependencies")
        print("="*60)
        
        # Create installer files directory
        self.installer_dir.mkdir(exist_ok=True)
        
        # Download Tesseract installer
        tesseract_path = self.download_file(TESSERACT_URL, TESSERACT_INSTALLER)
        if not tesseract_path:
            print("WARNING: Failed to download Tesseract. You'll need to download it manually.")
        
        # Download and extract Poppler
        poppler_path = self.download_file(POPPLER_URL, POPPLER_ZIP)
        if poppler_path:
            print("\nExtracting Poppler...")
            poppler_dir = self.project_dir / "poppler"
            if not poppler_dir.exists():
                with zipfile.ZipFile(poppler_path, 'r') as zip_ref:
                    zip_ref.extractall(self.project_dir)
                # The zip contains a folder, move its contents up
                extracted = list(self.project_dir.glob("poppler-*"))
                if extracted:
                    shutil.move(str(extracted[0]), str(poppler_dir))
                print("Poppler extracted successfully!")
            else:
                print("Poppler already exists, skipping extraction.")
    
    def install_pyinstaller(self):
        """Install PyInstaller if not already installed."""
        print("\n" + "="*60)
        print("STEP 2: Installing PyInstaller")
        print("="*60)
        
        try:
            import PyInstaller
            print("PyInstaller is already installed.")
        except ImportError:
            print("Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully!")
    
    def build_executable(self):
        """Build the executable using PyInstaller."""
        print("\n" + "="*60)
        print("STEP 3: Building Executable")
        print("="*60)
        
        spec_file = self.project_dir / "pdf_ocr.spec"
        if not spec_file.exists():
            print("ERROR: pdf_ocr.spec not found!")
            return False
        
        print("Running PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "PyInstaller", str(spec_file), "--clean"])
            print("\nExecutable built successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\nERROR: Build failed: {e}")
            return False
    
    def prepare_distribution(self):
        """Prepare the final distribution folder."""
        print("\n" + "="*60)
        print("STEP 4: Preparing Distribution")
        print("="*60)
        
        app_dist = self.dist_dir / "PDF_OCR"
        if not app_dist.exists():
            print("ERROR: Build output not found!")
            return False
        
        # Copy README
        readme_src = self.project_dir / "README.md"
        if readme_src.exists():
            shutil.copy(readme_src, app_dist / "README.txt")
        
        # Copy LICENSE
        license_src = self.project_dir / "LICENSE.txt"
        if license_src.exists():
            shutil.copy(license_src, app_dist / "LICENSE.txt")
        
        print(f"\nDistribution ready at: {app_dist}")
        return True
    
    def create_portable_zip(self):
        """Create a portable ZIP file."""
        print("\n" + "="*60)
        print("STEP 5: Creating Portable ZIP")
        print("="*60)
        
        app_dist = self.dist_dir / "PDF_OCR"
        zip_path = self.dist_dir / "PDF_OCR_Portable.zip"
        
        if zip_path.exists():
            zip_path.unlink()
        
        print("Creating ZIP archive...")
        shutil.make_archive(
            str(zip_path.with_suffix('')),
            'zip',
            self.dist_dir,
            'PDF_OCR'
        )
        
        print(f"\nPortable ZIP created: {zip_path}")
        print(f"Size: {zip_path.stat().st_size / (1024*1024):.2f} MB")
    
    def build(self):
        """Run the complete build process."""
        print("\n" + "="*60)
        print("PDF OCR Desktop Application - Build Script")
        print("="*60)
        
        steps = [
            ("Downloading dependencies", self.download_dependencies),
            ("Installing PyInstaller", self.install_pyinstaller),
            ("Building executable", self.build_executable),
            ("Preparing distribution", self.prepare_distribution),
            ("Creating portable ZIP", self.create_portable_zip),
        ]
        
        for step_name, step_func in steps:
            result = step_func()
            if result is False:
                print(f"\n❌ Build failed at: {step_name}")
                return False
        
        print("\n" + "="*60)
        print("✅ BUILD SUCCESSFUL!")
        print("="*60)
        print(f"\nOutput files:")
        print(f"  - Application folder: {self.dist_dir / 'PDF_OCR'}")
        print(f"  - Portable ZIP: {self.dist_dir / 'PDF_OCR_Portable.zip'}")
        print(f"  - Installer files: {self.installer_dir}")
        print("\nNext steps:")
        print("  1. Test the application in dist/PDF_OCR/")
        print("  2. To create installer, run Inno Setup with installer.iss")
        print("  3. The installer will be created in Output/")
        
        return True

if __name__ == "__main__":
    builder = Builder()
    success = builder.build()
    sys.exit(0 if success else 1)
