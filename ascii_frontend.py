import tkinter as tk
from tkinter import filedialog, messagebox
from ascii_magic import AsciiArt
from pathlib import Path

# ----- USER CONFIG -----
DEFAULT_COLUMNS = 120
DEFAULT_CHAR_SET = None     # None = default charset
DEFAULT_MONOCHROME = True
# ------------------------

def load_image():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if not filepath:
        return

    try:
        art = AsciiArt.from_image(filepath)
        ascii_text = art.to_ascii(
            columns=DEFAULT_COLUMNS,
            char=DEFAULT_CHAR_SET,
            monochrome=DEFAULT_MONOCHROME
        )

        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, ascii_text)
        text_widget.config(state=tk.DISABLED)

        save_path = Path(filepath).with_suffix(".txt")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(ascii_text)

        messagebox.showinfo("ASCII Converter", f"ASCII saved to: {save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----- GUI -----
root = tk.Tk()
root.title("ASCII Converter")
root.geometry("800x600")
root.configure(bg="black")

btn = tk.Button(root, text="Load Image", command=load_image, bg="gray", fg="white")
btn.pack(pady=10)

text_widget = tk.Text(root, bg="black", fg="white", font=("Courier", 6))
text_widget.pack(expand=True, fill=tk.BOTH)
text_widget.config(state=tk.DISABLED)

root.mainloop()
