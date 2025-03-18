import fitz  # PyMuPDF
from PIL import Image, ImageTk
from tkinter import Label,filedialog,messagebox,Toplevel, Canvas, Scrollbar, Frame, Button, LEFT, RIGHT, BOTTOM, X, Y, BOTH, VERTICAL, HORIZONTAL,PhotoImage
import os 
import io

class PreviewWindow:
    def __init__(self, root, pdf_path):
        """
        Initialize the preview window.
        """
        self.root = root
        self.pdf_path = pdf_path
        self.scale_factor = 1.2  # Initial zoom level
        # Creating new window for preview
        self.preview_window = Toplevel(self.root)
        self.preview_window.title("Preview of TC")
        self.preview_window.state("zoomed")
        icon=PhotoImage(file=r"img\\TC53.png")
        self.preview_window.iconphoto(True,icon)

        # Creating main frame to hold the canvas and button frame
        self.main_frame = Frame(self.preview_window)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Adding canvas with horizontal and vertical scrollbars
        self.canvas = Canvas(self.main_frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Vertical scrollbar
        self.v_scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)

        # Horizontal scrollbar
        self.h_scrollbar = Scrollbar(self.main_frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)

        # Configuring canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Creating a frame to hold the PDF pages inside the canvas
        self.page_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.page_frame, anchor="nw")

        # Load and display the PDF pages
        self.load_pdf_pages()

        # To add buttons for zoom, download, print and back
        self.add_buttons()

    def load_pdf_pages(self):
        """
        Load and display the PDF pages in the preview window.
        """
        # Opening PDF file
        self.pdf_document = fitz.open(self.pdf_path)

        # Clear existing pages
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        # Display each page of the PDF
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))

            # Resize the image based on the current scale factor
            width = int(img.width * self.scale_factor)
            height = int(img.height * self.scale_factor)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            # Display the image in a label
            label = Label(self.page_frame, image=img_tk)
            label.image = img_tk  # Keeping a reference to avoid garbage collection
            label.pack()

            # Adding page break separator (optional)
            if page_num < len(self.pdf_document) - 1:
                separator = Label(self.page_frame, text="-" * 100, fg="gray")
                separator.pack()

    def zoom_in(self):
        """
        Zoom in on the PDF pages.
        """
        self.scale_factor *= 1.2  # Increase scale factor by 20%
        self.load_pdf_pages()

    def zoom_out(self):
        """
        Zoom out on the PDF pages.
        """
        self.scale_factor /= 1.2  # Decrease scale factor by 20%
        self.load_pdf_pages()

    def reset_zoom(self):
        """
        Reset the zoom level to 100%.
        """
        self.scale_factor = 1.2  # Reset scale factor
        self.load_pdf_pages()

    def add_buttons(self):
        """
        Add zoom, download, print, and back buttons at the bottom of the window.
        """
        # Creating button frame at the bottom
        button_frame = Frame(self.preview_window,bg="#ffffff")
        button_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        # buttons
        buttons=[
        ("Zoom in" ,self.zoom_in),
        ("Zoom out" ,self.zoom_out),
        ("Reset zoom" , self.reset_zoom),
        ("Download" ,self.download_file),
        ("Print", self.print_file),
        ("Back",self.preview_window.destroy)]
        
        for i, (button_text, cmd) in enumerate(buttons):
            row = 0 if i < 6 else 1
            col = i % 6
            button = Button(button_frame, text=button_text, font=("Arial", 11,"bold"), bg="#4c3bcf", fg="#ffffff", width=12, command=cmd)
            button.grid(row=row, column=col, padx=30, pady=5)

    def download_file(self):
        """
        Save the PDF file to the user's desired location.
        """
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF Files", "*.pdf")],
                                                 initialfile=".pdf")
        if save_path:
            try:
                import shutil
                shutil.copy(self.pdf_path, save_path)
                messagebox.showinfo("Success", f"File saved as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def print_file(self):
        """
        Print the PDF file using the default printer.
        """
        try:
            os.startfile(self.pdf_path, "print")
            messagebox.showinfo("Success", "Document sent to printer!")
        except Exception as e:
            messagebox.showerror("Exception", f"Failed to print document: {e}")
