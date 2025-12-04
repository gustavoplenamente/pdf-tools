# Quick Start Guide for Sharing Your PDF OCR Application

This guide shows you the easiest way to share the PDF OCR application with your friends.

## 📦 Option 1: Professional Installer (Recommended)

This creates a Windows installer that includes everything your friends need.

### Steps:

1. **Run the build script** (in your project folder):
   ```
   python build.py
   ```
   
   This will:
   - Download Tesseract OCR (~74 MB)
   - Download Poppler utilities (~16 MB)
   - Create a portable ZIP
   - Prepare files for the installer

2. **Install Inno Setup** (one-time setup):
   - Download from: https://jrsoftware.org/isdl.php
   - Install it (use default settings)

3. **Create the installer**:
   - Right-click `installer.iss`
   - Select "Compile"
   - Wait for completion

4. **Share the installer**:
   - Find `Output/PDF_OCR_Setup_1.0.0.exe`
   - Upload to Google Drive, Dropbox, or USB drive
   - Share with friends!

### What your friends get:
✅ Professional installation wizard (in Portuguese or English)
✅ All dependencies installed automatically
✅ Desktop and Start Menu shortcuts
✅ Easy uninstaller

---

## 📂 Option 2: Portable ZIP (Simpler, but requires Tesseract)

This creates a ZIP file that works without installation.

### Steps:

1. **Run the build script**:
   ```
   python build.py
   ```

2. **Share the ZIP**:
   - Find `dist/PDF_OCR_Portable.zip`
   - Upload to Google Drive, Dropbox, or USB drive
   - Share with friends!

### What your friends need to do:
1. Extract the ZIP to any folder
2. Install Tesseract OCR from: https://github.com/tesseract-ocr/tesseract
3. Run `PDF_OCR.exe`

### Benefits:
✅ No installation needed
✅ Can run from USB drive
✅ Smaller file size (~80 MB vs ~100 MB)

---

## 🚀 Which Option Should You Choose?

| Feature | Installer | Portable ZIP |
|---------|-----------|--------------|
| Easy for friends | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| File size | ~100 MB | ~80 MB |
| Includes Tesseract | ✅ Yes | ❌ No |
| Shortcuts | ✅ Yes | ❌ No |
| Uninstaller | ✅ Yes | ❌ No |
| Build complexity | Medium (needs Inno Setup) | Easy |

**Recommendation**: Use the **Installer** if you want the best experience for your friends. Use **Portable ZIP** if you want something quick and simple.

---

## 📋 System Requirements for Your Friends

- Windows 7 or higher (64-bit)
- 2 GB RAM (4 GB recommended)
- 200 MB disk space (500 MB recommended)
- No Python required! ✅

---

## ❓ Troubleshooting

### Build script fails to download files

**Solution**: Check your internet connection or download manually:
- Tesseract: https://digi.bib.uni-mannheim.de/tesseract/
- Poppler: https://github.com/oschwartz10612/poppler-windows/releases

### "PyInstaller not found"

**Solution**: 
```
pip install pyinstaller
```

### Inno Setup errors

**Solution**: Make sure you ran `python build.py` first to create the `dist/PDF_OCR` folder.

---

## 💡 Tips

1. **Test before sharing**: Run the installer on your own computer first
2. **Virus scanners**: Some antivirus software may flag PyInstaller executables as suspicious. This is a false positive.
3. **File size**: You can use file compression tools like 7-Zip to further reduce the size
4. **Updates**: To create a new version, just run the build script again and recompile the installer

---

## 📞 Need More Help?

See the full documentation in [BUILD.md](BUILD.md) for:
- Advanced build options
- Customization
- Detailed troubleshooting
- Version management

---

**Happy sharing! 🎉**
