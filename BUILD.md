# Building and Distributing PDF OCR Desktop Application

This guide covers how to build a standalone executable and create an installer for the PDF OCR Desktop Application.

## Prerequisites

### Required Software

1. **Python 3.8 or higher** - Already installed if you can run the application
2. **PyInstaller** - Will be installed automatically by build script
3. **Inno Setup 6+** (for creating installer) - Download from: https://jrsoftware.org/isdl.php

### Optional
- **UPX** (Ultimate Packer for eXecutables) - For smaller executable size: https://upx.github.io/

## Build Process

### Step 1: Run the Build Script

The easiest way to build the application is to run the automated build script:

```bash
python build.py
```

This script will:
1. Download Tesseract OCR installer (~74 MB)
2. Download Poppler utilities (~16 MB)
3. Install PyInstaller if not present
4. Build the standalone executable
5. Create a portable ZIP package

**Output files:**
- `dist/PDF_OCR/` - Standalone application folder
- `dist/PDF_OCR_Portable.zip` - Portable ZIP package (no installation needed)
- `installer_files/` - Downloaded dependencies for the installer

### Step 2: Test the Standalone Application

Before creating the installer, test the built application:

```bash
cd dist\PDF_OCR
PDF_OCR.exe
```

Verify that:
- The application launches without errors
- You can select PDF files
- Text extraction works
- OCR functionality works (requires Tesseract to be installed on your system)

### Step 3: Create the Installer (Optional)

To create a professional installer with wizard interface:

1. **Install Inno Setup** if you haven't already:
   - Download from: https://jrsoftware.org/isdl.php
   - Run the installer and follow the wizard

2. **Compile the installer script**:
   - Right-click on `installer.iss`
   - Select "Compile" (if you have Inno Setup installed)
   
   OR use the command line:
   ```bash
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

3. **Find your installer**:
   - The installer will be created in the `Output/` folder
   - Filename: `PDF_OCR_Setup_1.0.0.exe`

## Distribution Options

You have two ways to share the application with friends:

### Option 1: Portable ZIP (Quick and Easy)
- **File:** `dist/PDF_OCR_Portable.zip`
- **Pros:** 
  - No installation needed
  - Can run from USB drive or any folder
  - Smaller download size
- **Cons:**
  - Users must install Tesseract OCR separately for OCR functionality
  - No start menu shortcuts

**Instructions for users:**
1. Extract the ZIP to any folder
2. Install Tesseract OCR from: https://github.com/tesseract-ocr/tesseract
3. Run `PDF_OCR.exe`

### Option 2: Installer EXE (Professional)
- **File:** `Output/PDF_OCR_Setup_1.0.0.exe`
- **Pros:**
  - Professional installation wizard
  - Automatically installs Tesseract OCR
  - Creates desktop and start menu shortcuts
  - Easy uninstall
- **Cons:**
  - Larger file size (~100 MB)
  - Requires administrator privileges

**Instructions for users:**
1. Run `PDF_OCR_Setup_1.0.0.exe`
2. Follow the installation wizard
3. Launch from desktop shortcut or start menu

## Manual Build (Advanced)

If you need more control over the build process:

### Build Executable Only

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the spec file
pyinstaller pdf_ocr.spec --clean
```

### Customize the Build

Edit `pdf_ocr.spec` to:
- Change the executable name
- Add/remove bundled files
- Modify the icon
- Adjust compression settings

## Troubleshooting

### Build Fails with "Module not found"

Install missing dependencies:
```bash
pip install -r requirements.txt
```

### Executable is too large

1. Install UPX: https://upx.github.io/
2. UPX will be used automatically by PyInstaller

### Tesseract download fails

Manually download Tesseract:
1. Download from: https://digi.bib.uni-mannheim.de/tesseract/
2. Save as `installer_files/tesseract-installer.exe`
3. Re-run build script

### Poppler download fails

Manually download Poppler:
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract to `poppler/` folder in project root
3. Re-run build script

### Inno Setup compilation errors

Check that:
- You have Inno Setup 6 or higher installed
- The `dist/PDF_OCR/` folder exists and contains the built application
- The `installer_files/tesseract-installer.exe` exists

## File Sizes (Approximate)

- Standalone application folder: ~150 MB
- Portable ZIP: ~80 MB
- Installer EXE: ~100 MB

## System Requirements for Built Application

### Minimum
- Windows 7 or higher (64-bit)
- 2 GB RAM
- 200 MB disk space

### Recommended
- Windows 10/11 (64-bit)
- 4 GB RAM
- 500 MB disk space

## Security Notes

- The application doesn't require internet connection
- No data is sent to external servers
- All processing is done locally
- The installer requires admin rights only for:
  - Installing to Program Files
  - Installing Tesseract system-wide
  - Adding Tesseract to PATH

## Updating the Application

To create a new version:

1. Update version number in:
   - `version_info.txt`
   - `installer.iss` (MyAppVersion)
   
2. Run build script:
   ```bash
   python build.py
   ```
   
3. Recompile installer with Inno Setup

## License

See `LICENSE.txt` for license information and third-party attributions.
