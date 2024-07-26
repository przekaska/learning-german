import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os

# Directory to store lists
LISTS_DIR = "lists" 
if not os.path.exists(LISTS_DIR):
    os.makedirs(LISTS_DIR)

# Create an instance of the Tk class
root = tk.Tk()
root.title("German Vocabulary Learning")
root.state("zoomed")
root.configure(bg='#121212')

# Colors and Fonts
BACKGROUND_COLOR = '#121212'
FRAME_COLOR = '#1e1e1e'
BUTTON_COLOR = '#4caf50'
BUTTON_TEXT_COLOR = '#ffffff'
ENTRY_BG_COLOR = '#333333'
ENTRY_FG_COLOR = '#ffffff'
TEXT_BG_COLOR = '#1e1e1e'
TEXT_FG_COLOR = '#ffffff'
FONT = ('Arial', 14)
HIGHLIGHT_COLOR = '#8a0000'

# Create a frame for the mode label
mode_frame = tk.Frame(root, bg=FRAME_COLOR, pady=20)
mode_frame.pack(fill='x')

mode_label = tk.Label(mode_frame, text="Current Mode: Edit Mode", font=(FONT[0], 16, 'bold'), bg=FRAME_COLOR, fg=BUTTON_COLOR)
mode_label.pack()

# Create a frame to hold the list name and entry widgets
top_frame = tk.Frame(root, bg=FRAME_COLOR, pady=10)
top_frame.pack(fill='x')

list_name_label = tk.Label(top_frame, text="List Name:", font=FONT, bg=FRAME_COLOR, fg=BUTTON_TEXT_COLOR)
list_name_label.pack(side='left', padx=10)
list_name_entry = tk.Entry(top_frame, width=30, font=FONT, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
list_name_entry.pack(side='left')

# Create a frame to hold the entry widgets
entry_frame = tk.Frame(root, bg=FRAME_COLOR, pady=10)
entry_frame.pack(fill='x')

entry1_label = tk.Label(entry_frame, text="English Word:", font=FONT, bg=FRAME_COLOR, fg=BUTTON_TEXT_COLOR)
entry1_label.pack(side='left', padx=10)
entry1 = tk.Entry(entry_frame, width=40, font=FONT, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
entry1.pack(side='left', padx=10)

entry2_label = tk.Label(entry_frame, text="German Translation:", font=FONT, bg=FRAME_COLOR, fg=BUTTON_TEXT_COLOR)
entry2_label.pack(side='left', padx=10)
entry2 = tk.Entry(entry_frame, width=40, font=FONT, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
entry2.pack(side='left', padx=10)

entry1.config(disabledbackground="#000000")
entry2.config(disabledbackground="#000000")
list_name_entry.config(disabledbackground="#000000")

# Create a Text widget to display the list of words
words_display = tk.Text(root, wrap='word', font=FONT, height=15, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, state='disabled')
words_display.pack(pady=20, padx=20, fill='both', expand=True)

# Define text tags for different genders
words_display.tag_configure("die", foreground="#e91e63")  # Pink color for "die"
words_display.tag_configure("der", foreground="#2196f3")  # Blue color for "der"
words_display.tag_configure("das", foreground="#4caf50")  # Green color for "das"
words_display.tag_configure("highlight", background=HIGHLIGHT_COLOR)

# Mode variable to track the current mode
mode = tk.StringVar(value="edit")

# Variables to store the current list of words and the order of English words
words_list = []
english_order = []
translations_visible = False  # Track the visibility state of translations
view_mode = tk.StringVar(value="both")  # Track the current view mode (English, German, or both)

# Variable to track the current highlighted line
highlighted_line_index = None

def get_gender_tag(word):
    if word.lower().startswith("die "):
        return "die"
    elif word.lower().startswith("der "):
        return "der"
    elif word.lower().startswith("das "):
        return "das"
    return ""

def add_word(event=None):
    if mode.get() == "edit":
        english_word = entry1.get().strip()
        german_word = entry2.get().strip()
        if english_word and german_word:
            formatted_text = f"{english_word} - {german_word}\n"
            gender_tag = get_gender_tag(german_word)
            words_display.config(state='normal')
            words_display.insert(tk.END, formatted_text, gender_tag)
            words_display.config(state='disabled')
            words_list.append(formatted_text.strip())
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry1.focus_set()
            
            # Scroll to the end of the text widget
            words_display.config(state='normal')
            words_display.see(tk.END)
            words_display.config(state='disabled')
        else:
            messagebox.showwarning("Input Error", "Please enter both English and German words.")
    else:
        messagebox.showwarning("Mode Error", "Cannot add words in View Mode.")


def save_list():
    if mode.get() == "edit":
        list_name = list_name_entry.get().strip()
        if list_name:
            file_path = os.path.join(LISTS_DIR, f"{list_name}.txt")
            if words_list:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write("\n".join(words_list))
                    messagebox.showinfo("Success", f"List '{list_name}' saved successfully!")
                    words_display.config(state='normal')
                    words_display.delete("1.0", tk.END)
                    words_display.config(state='disabled')
                    list_name_entry.delete(0, tk.END)
                    words_list.clear()
                except IOError:
                    messagebox.showerror("File Error", "Unable to save the list. Please check file permissions.")
            else:
                messagebox.showwarning("Save Error", "The list is empty. Add some words before saving.")
        else:
            messagebox.showwarning("Save Error", "Please enter a list name.")
    else:
        messagebox.showwarning("Mode Error", "Cannot save list in View Mode.")

def load_list():
    file_paths = filedialog.askopenfilenames(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_paths:
        words_display.config(state='normal')
        words_display.delete("1.0", tk.END)
        words_list.clear()
        english_order.clear()
        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        words_list.append(line.strip())
                        english_word, german_word = line.split(' - ')
                        english_order.append(english_word)
                        gender_tag = get_gender_tag(german_word)
                        words_display.insert(tk.END, line.strip() + "\n", gender_tag)
                list_name = os.path.basename(file_path).replace(".txt", "")
                list_name_entry.delete(0, tk.END)
                list_name_entry.insert(0, list_name)
            except IOError:
                messagebox.showerror("File Error", f"Unable to load the file: {file_path}. Please check file permissions.")
        words_display.config(state='disabled')

def switch_mode():
    global highlighted_line_index
    if mode.get() == "edit":
        mode.set("view")
        display_english_words()
        toggle_button.config(text="Switch to Edit Mode", bg='#ff5722')
        mode_label.config(text="Current Mode: View Mode")
        add_button.config(state='disabled')
        save_button.config(state='disabled')
        list_name_entry.config(state='disabled')
        entry1.config(state='disabled')
        entry2.config(state='disabled')
        highlighted_line_index = 1
        highlight_line()
        
    else:
        mode.set("edit")
        words_display.config(state='normal')
        words_display.delete("1.0", tk.END)
        for word in words_list:
            english_word, german_word = word.split(' - ')
            gender_tag = get_gender_tag(german_word)
            words_display.insert(tk.END, word + "\n", gender_tag)
        words_display.config(state='disabled')
        toggle_button.config(text="Switch to View Mode", bg=BUTTON_COLOR)
        mode_label.config(text="Current Mode: Edit Mode")
        add_button.config(state='normal')
        save_button.config(state='normal')
        list_name_entry.config(state='normal')
        entry1.config(state='normal')
        entry2.config(state='normal')
        highlighted_line_index = None
        remove_highlight()

def display_english_words():
    words_display.config(state='normal')
    words_display.delete("1.0", tk.END)
    global english_order
    english_order = [word.split(' - ')[0] for word in words_list]
    random.shuffle(english_order)
    for word in english_order:
        words_display.insert(tk.END, word + "\n")
    words_display.config(state='disabled')

def display_english_words_no_shuffle():
    for english_word in english_order:
        for word in words_list:
            word_english, word_german = word.split(' - ')
            if word_english == english_word:
                words_display.insert(tk.END, f"{word_english}\n")
                break

def show_translations():
    global translations_visible
    if mode.get() == "view":
        # Save the current view position
        view_pos = words_display.yview()
        words_display.config(state='normal')
        words_display.delete("1.0", tk.END)
        if view_mode.get() == "english":
            display_english_words_no_shuffle()
        elif view_mode.get() == "german":
            for english_word in english_order:
                for word in words_list:
                    word_english, word_german = word.split(' - ')
                    if word_english == english_word:
                        gender_tag = get_gender_tag(word_german)
                        words_display.insert(tk.END, f"{word_german}\n", gender_tag)
                        break
        elif view_mode.get() == "both":
            for english_word in english_order:
                for word in words_list:
                    word_english, word_german = word.split(' - ')
                    if word_english == english_word:
                        gender_tag = get_gender_tag(word_german)
                        words_display.insert(tk.END, f"{english_word} - {word_german}\n", gender_tag)
                        break
        words_display.config(state='disabled')
        translations_visible = False

        # Restore the view position
        words_display.yview_moveto(view_pos[0])

def handle_enter(event):
    if mode.get() == "edit":
        current_widget = root.focus_get()
        if current_widget == entry2:
            add_word()
        elif current_widget == entry1:
            entry2.focus_set()
        else:
            add_word()

def new_list():
    if mode.get() == "edit":
        # Prompt the user for confirmation before clearing the list
        response = messagebox.askyesno("Confirm New List", "Are you sure you want to start a new list? This will clear the current list.")
        if response:
            # Clear existing entries and reset state
            words_display.config(state='normal')
            words_display.delete("1.0", tk.END)
            list_name_entry.delete(0, tk.END)
            words_list.clear()
            english_order.clear()
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
    else:
        messagebox.showwarning("Mode Error", "Cannot start a new list in View Mode.")

def highlight_line():
    remove_highlight()
    if highlighted_line_index is not None:
        line_start = f"{highlighted_line_index}.0"
        line_end = f"{highlighted_line_index}.end"
        words_display.tag_add("highlight", line_start, line_end)

def remove_highlight():
    words_display.tag_remove("highlight", "1.0", tk.END)

def move_highlight_up(event=None):
    global highlighted_line_index
    if highlighted_line_index is not None and highlighted_line_index > 1:
        highlighted_line_index -= 1
        highlight_line()

def move_highlight_down(event=None):
    global highlighted_line_index
    if highlighted_line_index is not None:
        total_lines = int(words_display.index('end-1c').split('.')[0])
        if highlighted_line_index < total_lines:
            highlighted_line_index += 1
            highlight_line()

# Bind the Enter key to the handle_enter function
entry1.bind("<Return>", handle_enter)
entry2.bind("<Return>", handle_enter)

# Bind the up and down arrow keys to move the highlight
root.bind("<Up>", move_highlight_up)
root.bind("<Down>", move_highlight_down)
root.bind("<space>", move_highlight_down)
root.bind("<Return>", move_highlight_down)

# Create buttons to add words, save the list, and load the list
button_frame = tk.Frame(root, bg=FRAME_COLOR, pady=20)
button_frame.pack()

add_button = tk.Button(button_frame, text="Add Word", command=add_word, font=FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, padx=20, pady=10, relief="flat")
add_button.pack(side='left', padx=10)

save_button = tk.Button(button_frame, text="Save List", command=save_list, font=FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, padx=20, pady=10, relief="flat")
save_button.pack(side='left', padx=10)

load_button = tk.Button(button_frame, text="Load List", command=load_list, font=FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, padx=20, pady=10, relief="flat")
load_button.pack(side='left', padx=10)

new_list_button = tk.Button(button_frame, text="New List", command=new_list, font=FONT, bg='#f44336', fg=BUTTON_TEXT_COLOR, padx=20, pady=10, relief="flat")
new_list_button.pack(side='left', padx=10)

toggle_button = tk.Button(button_frame, text="Switch to View Mode", command=switch_mode, font=FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, padx=20, pady=10, relief="flat")
toggle_button.pack(side='left', padx=10)

# View mode options
view_mode_frame = tk.Frame(root, bg=FRAME_COLOR)
view_mode_frame.pack(pady=10)

tk.Radiobutton(view_mode_frame, text="English Only", command=show_translations, variable=view_mode, value="english", bg=FRAME_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT).pack(side='left', padx=10)
tk.Radiobutton(view_mode_frame, text="German Only", command=show_translations, variable=view_mode, value="german", bg=FRAME_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT).pack(side='left', padx=10)
tk.Radiobutton(view_mode_frame, text="Both", command=show_translations, variable=view_mode, value="both", bg=FRAME_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT).pack(side='left', padx=10)

# Start the main event loop
root.mainloop()