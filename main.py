"""
PDF OCR Desktop Application
A simple desktop application to extract text from PDFs with OCR support.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import os
from pdf_processor import PDFProcessor


class PDFOCRApp:
    """Main application class for PDF OCR."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("PDF OCR - Text Extractor")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Initialize PDF processor
        try:
            self.processor = PDFProcessor()
        except RuntimeError as e:
            messagebox.showerror("Tesseract Not Found", str(e))
            self.root.destroy()
            return
        
        self.current_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="PDF OCR Text Extractor",
            font=("Segoe UI", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF File", padding="10")
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(0, weight=1)
        
        # File path display
        self.file_path_var = tk.StringVar(value="No file selected")
        file_path_label = ttk.Label(
            file_frame, 
            textvariable=self.file_path_var,
            foreground="gray",
            wraplength=700
        )
        file_path_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(
            file_frame,
            text="Browse...",
            command=self.browse_file,
            width=15
        )
        browse_btn.grid(row=0, column=1)
        
        # Action buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 15), sticky=tk.W)
        
        # Extract text button
        self.extract_btn = ttk.Button(
            button_frame,
            text="📄 Extract Text",
            command=self.extract_text,
            state=tk.DISABLED,
            width=20
        )
        self.extract_btn.grid(row=0, column=0, padx=(0, 10))
        
        # OCR button
        self.ocr_btn = ttk.Button(
            button_frame,
            text="🔍 OCR (Scanned PDF)",
            command=self.extract_with_ocr,
            state=tk.DISABLED,
            width=20
        )
        self.ocr_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Copy button
        self.copy_btn = ttk.Button(
            button_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
            width=20
        )
        self.copy_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Clear button
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_text,
            state=tk.DISABLED,
            width=15
        )
        self.clear_btn.grid(row=0, column=3)
        
        # Text output frame
        output_frame = ttk.LabelFrame(main_frame, text="Extracted Text", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Scrolled text widget
        self.text_output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            padx=10,
            pady=10
        )
        self.text_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Progress bar (initially hidden)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        # Don't grid it yet, will show when needed
    
    def browse_file(self):
        """Open file dialog to select a PDF file."""
        filename = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            self.current_file = filename
            self.file_path_var.set(filename)
            self.extract_btn.config(state=tk.NORMAL)
            self.ocr_btn.config(state=tk.NORMAL)
            self.status_var.set(f"File selected: {os.path.basename(filename)}")
    
    def extract_text(self):
        """Extract text from the selected PDF."""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return
        
        # Disable buttons during processing
        self.set_buttons_state(tk.DISABLED)
        self.status_var.set("Extracting text...")
        
        # Run in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._extract_text_thread)
        thread.daemon = True
        thread.start()
    
    def _extract_text_thread(self):
        """Thread function for text extraction."""
        try:
            text = self.processor.extract_text_from_pdf(self.current_file)
            self.root.after(0, self._display_text, text)
            self.root.after(0, self.status_var.set, "Text extraction completed")
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
            self.root.after(0, self.status_var.set, "Error during text extraction")
        finally:
            self.root.after(0, self.set_buttons_state, tk.NORMAL)
    
    def extract_with_ocr(self):
        """Extract text using OCR from the selected PDF."""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return
        
        # Disable buttons during processing
        self.set_buttons_state(tk.DISABLED)
        self.status_var.set("Performing OCR... This may take a while.")
        
        # Show progress bar
        self.progress_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.progress_var.set(0)
        
        # Run in a separate thread
        thread = threading.Thread(target=self._extract_ocr_thread)
        thread.daemon = True
        thread.start()
    
    def _extract_ocr_thread(self):
        """Thread function for OCR extraction."""
        try:
            def progress_callback(current, total):
                progress = (current / total) * 100
                self.root.after(0, self.progress_var.set, progress)
                self.root.after(0, self.status_var.set, f"Processing page {current} of {total}...")
            
            text = self.processor.extract_text_with_ocr(
                self.current_file,
                progress_callback=progress_callback
            )
            self.root.after(0, self._display_text, text)
            self.root.after(0, self.status_var.set, "OCR completed")
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
            self.root.after(0, self.status_var.set, "Error during OCR")
        finally:
            self.root.after(0, self.set_buttons_state, tk.NORMAL)
            self.root.after(0, self.progress_bar.grid_remove)
    
    def _display_text(self, text):
        """Display extracted text in the text widget."""
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(1.0, text)
        self.copy_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)
    
    def copy_to_clipboard(self):
        """Copy the extracted text to clipboard."""
        text = self.text_output.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status_var.set("Text copied to clipboard")
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("No Text", "No text to copy.")
    
    def clear_text(self):
        """Clear the text output area."""
        self.text_output.delete(1.0, tk.END)
        self.copy_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.status_var.set("Text cleared")
    
    def set_buttons_state(self, state):
        """Enable or disable all action buttons."""
        self.extract_btn.config(state=state if self.current_file else tk.DISABLED)
        self.ocr_btn.config(state=state if self.current_file else tk.DISABLED)
        if state == tk.DISABLED:
            self.copy_btn.config(state=state)
            self.clear_btn.config(state=state)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = PDFOCRApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
