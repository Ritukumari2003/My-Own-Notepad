import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import simpledialog   # required for find dialog

# -------------------- FONT SETTINGS --------------------

# Default font size and font style for the text editor

font_size = 12
font_style = "Georgia"

# -------------------- FILE FUNCTIONS --------------------

def saving_file():
    """
    Save the current content of the text editor into a file.
    Opens a 'Save As' dialog and writes the text to the selected file.
    """
    file_location = asksaveasfilename(
        defaultextension=".txt",   # Default extension
        filetypes=[("Text files", "*.txt"), ("All Files", "*.*")]
    )

    # If user cancels the save dialog
    if not file_location:
        return

    # Write text editor content to file
    with open(file_location, "w") as f:
        text = text_edit.get(1.0, tk.END)  # Get all text
        f.write(text)

    # Update window title with file name
    root.title(f"MY OWN NOTEPAD - {file_location}")


def opening_file():
    """
    Open an existing text file and display its content
    inside the text editor.
    """
    file_location = askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All Files", "*.*")]
    )

    # If user cancels open dialog
    if not file_location:
        return

    # Clear existing text before opening new file
    text_edit.delete(1.0, tk.END)

    # Read file content and insert into text editor
    with open(file_location, "r") as f:
        text_edit.insert(tk.END, f.read())

    # Update window title
    root.title(f"MY OWN NOTEPAD - {file_location}")

def new_file():
    """
    Clear the text editor to start a new file.
    """
    text_edit.delete(1.0, tk.END)
    root.title("My Own Notepad - New File")

# -------------------- THEME FUNCTIONS --------------------

def dark_mode():
    """
    Enable dark mode by changing background,
    text color, and cursor color.
    """
    text_edit.config(
        bg="#1e1e1e",        # Dark background
        fg="white",         # White text
        insertbackground="white"  # Cursor color
    )


def light_mode():
    """
    Enable light mode by restoring default colors.
    """
    text_edit.config(
        bg="white",
        fg="black",
        insertbackground="black"
    )


# -------------------- SEARCH FUNCTION --------------------

def find_text():
    """
    Ask the user for a word and highlight
    all occurrences in the text editor.
    """
    word = simpledialog.askstring("Find", "Enter word:")
    if not word:
        return

    # Remove previous highlights
    text_edit.tag_remove("found", "1.0", tk.END)

    idx = "1.0"  # Start searching from beginning

    while True:
        # Search word in text editor
        idx = text_edit.search(word, idx, nocase=1, stopindex=tk.END)
        if not idx:
            break

        lastidx = f"{idx}+{len(word)}c"
        text_edit.tag_add("found", idx, lastidx)
        idx = lastidx

    # Highlight color
    text_edit.tag_config("found", background="yellow")

# -------------------- FONT SIZE FUNCTIONS --------------------

def increase_font():
    """
    Increase font size of the text editor.
    """
    global font_size
    if font_size < 40:
        font_size += 2
        text_edit.config(font=(font_style, font_size))


def decrease_font():
    """
    Decrease font size of the text editor.
    """
    global font_size
    if font_size > 8:
        font_size -= 2
        text_edit.config(font=(font_style, font_size))


# -------------------- MAIN WINDOW --------------------

root = tk.Tk()
root.title("My Own Notepad")

# Configure grid layout for resizing
root.rowconfigure(0, minsize=800)
root.columnconfigure(1, minsize=800)

# -------------------- MENU BAR --------------------

menu_bar = tk.Menu(root, font=(font_style, 10))
root.config(menu=menu_bar)

# View Menu (Theme switching)
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Dark Mode", command=dark_mode)
view_menu.add_command(label="Light Mode", command=light_mode)

# Search Menu
search_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Find", command=find_text)

# -------------------- TEXT EDITOR --------------------
text_edit = tk.Text(root, font=(font_style, font_size))
text_edit.grid(row=0, column=1, sticky="nsew")

# -------------------- BUTTON FRAME --------------------
frame_button = tk.Frame(root, relief=tk.RAISED, bd=3)
frame_button.grid(row=0, column=0, sticky="ns")

# Buttons
button_new = tk.Button(frame_button, text="NEW FILE", command=new_file)
button_new.grid(row=0, column=0, padx=5, pady=5)

button_open = tk.Button(frame_button, text="OPEN FILE", command=opening_file)
button_open.grid(row=1, column=0, padx=5, pady=5)

button_save = tk.Button(frame_button, text="SAVE AS", command=saving_file)
button_save.grid(row=2, column=0, padx=5, pady=5)

# Font size buttons
button_plus = tk.Button(frame_button, text="A +", command=increase_font)
button_plus.grid(row=3, column=0, padx=5, pady=5)

button_minus = tk.Button(frame_button, text="A -", command=decrease_font)
button_minus.grid(row=4, column=0, padx=5)

# -------------------- SCROLLBAR --------------------
scrollbar = tk.Scrollbar(root, command=text_edit.yview)
scrollbar.grid(row=0, column=2, sticky="ns")

text_edit.config(yscrollcommand=scrollbar.set)

# ----------------- START APPLICATION -----------------

root.mainloop()
