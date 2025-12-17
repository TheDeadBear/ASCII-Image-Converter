import tkinter as tk                          # Tkinter for GUI (windows, buttons, text box)
from tkinter import filedialog, messagebox    # filedialog: select files; messagebox: pop-up messages
from ascii_magic import AsciiArt             # ascii_magic: converts images to ASCII art
from pathlib import Path                      # pathlib: handle file paths in an OS-independent way

#  USER CONFIG 
# These are settings we can tweak to change output

DEFAULT_COLUMNS = 600  # Number of characters per row in ASCII output; higher = more detail
DEFAULT_CHAR_SET = " .'`^\",:;Il!i~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# The character set is used to map brightness levels to characters
# Longer/more varied char sets = more subtle shading/detail
DEFAULT_MONOCHROME = False  # True = plain ASCII (no colour) False = coloured output though I don't think our gui supports it


def load_image():
    """
    This function runs when the 'Load Image' button is clicked.
    It:
    1. Opens a file picker to select an image
    2. Converts the image to ASCII art
    3. Displays the ASCII in the GUI
    4. Saves both TXT and HTML versions of the ASCII
    """

    # Open a file dialog to let user pick an image
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    
    # If user cancels file selection, just return (do nothing)
    if not filepath:
        return

    try:
        # Step 1 — generate ASCII from the image
        # AsciiArt.from_image reads the image and creates an object representing the ASCII art
        art = AsciiArt.from_image(filepath)

        # Step 2 — convert the AsciiArt object to a string with our settings
        ascii_text = art.to_ascii(
            columns=DEFAULT_COLUMNS,        # width of ASCII output
            char=DEFAULT_CHAR_SET,          # which characters to use for shading
            monochrome=DEFAULT_MONOCHROME   # color or plain
        )

        # Step 3 — display ASCII in the GUI
        text_widget.config(state=tk.NORMAL)   # Enable editing temporarily
        text_widget.delete("1.0", tk.END)    # Clear any previous ASCII
        text_widget.insert(tk.END, ascii_text)  # Insert new ASCII
        text_widget.config(state=tk.DISABLED)  # Disable editing again to prevent user typing

        # Step 4 — save ASCII to a plain text file
        txt_path = Path(filepath).with_suffix(".txt")  # same filename, but .txt extension
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(ascii_text)

        # Step 5 — save ASCII to an HTML file for better display with dark background
        html_path = Path(filepath).with_suffix(".html")  # same filename, but .html extension
        with open(html_path, "w", encoding="utf-8") as f:
            # Wrap ASCII in <pre> to preserve spacing; set background black and text white
            f.write("<html><body style='background:black;color:white;'><pre>\n")
            f.write(ascii_text)
            f.write("\n</pre></body></html>")

        # Step 6 — notify the user that files are saved
        messagebox.showinfo(
            "ASCII Converter",
            f"ASCII saved to:\nTXT: {txt_path}\nHTML: {html_path}"
        )

    except Exception as e:
        # If anything goes wrong (file not found, invalid image, etc.), show an error message
        messagebox.showerror("Error", str(e))


# GUI SETUP 
# Create the main window
root = tk.Tk()
root.title("ASCII Converter")       # Window title
root.geometry("800x600")            # Window size in pixels (width x height)
root.configure(bg="black")          # Set background color to black

# Create a button to load images
btn = tk.Button(
    root, 
    text="Load Image",               # Button label
    command=load_image,              # Function to run when clicked
    bg="gray",                       # Button background color
    fg="white"                       # Button text color
)
btn.pack(pady=10)                   # Add some vertical padding around the button

# Create a text widget to display ASCII
text_widget = tk.Text(
    root,
    bg="black",                       # Text widget background
    fg="white",                       # Text color
    font=("Courier", 4)               # Monospaced font, very small for high-resolution ASCII
)
text_widget.pack(expand=True, fill=tk.BOTH)  # Make text widget expand to fill window
text_widget.config(state=tk.DISABLED)        # Start as read-only

# Start the Tkinter event loop
root.mainloop()  # Keeps the window open and responsive
