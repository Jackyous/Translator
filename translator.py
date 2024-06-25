# Jacky Zhou
# Mr. David Park - ICS 4U
# 2024/06/19
# FCE - translator

# This program include these functions:
#   1. Translate the text you type
#   2. Save the translated text
#   3. Translate the file's text and store it into another new file

import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext as sct
from googletrans import Translator # Translate module
import json
import customtkinter as ctk
import threading

# Load the file which contains language names and their shortcuts
with open("language.json" , "r") as file:
    language = json.load(file)
# Translate the text you type
def translate_text(text,to_language):
    # Check if input values are exited
    if to_language == "":
        error_output.config(text="Please select a language you want to translate to")
        return
    # Transfer the language name to the language shortcut in order to make computer recognize what language is it
    to_language_shortcut = name_to_shortcut(to_language)
    # Define a translator class
    translator = Translator()
    # translate the text by using the method
    translation = translator.translate(text=text,dest=to_language_shortcut)
    # Showing the translated text on the GUI
    show_text_line(translation.text)
    error_output.config(bg="white",text="Text translation completed, you can save the translated result")

# Translate the text and return value, I use it in the translate_file function
def translate_text_return(text,to_language):
    to_language_shortcut = name_to_shortcut(to_language)
    translator = Translator()
    translation = translator.translate(text=text.strip(),dest=to_language_shortcut)
    return translation.text
# Translate file text
def translate_file(to_language):
    # Check if input value are exited
    if to_language == "":
        error_output.config(bg="white",text="Please select a language you want to translate to")
        return
    # open file explorer to ask the file path
    file_path = filedialog.askopenfilename()
    if file_path == "":
        return
    # Read the file into lines(list)
    with open(file_path,"r",encoding="utf-8") as file:
        lines = file.readlines()
    # A list to store the translated text
    translations = []
    threads = []

    for line in lines:
        # If one line of text is over 500, it divides the line into different section to translate, which can accelerate the speed of program running
        if len(line) > 500:
            segments = line.split(",")
            for segment in segments:
                # use 'translate_text' function to translate texts, also eliminate all the space
                translation = translate_text_return(segment.strip(),to_language)
                # add the translated texts into the list
                translations.append(translation)
                # Define a new threading to show the result in real time
                thread = threading.Thread(target=show_text_line,args=(translations,))
                # Start the thread
                thread.start()
                # append it in a list in case all the thread can stop after showing the result
                threads.append(thread)

        else:
            # if the entire texts not over 500, then not add the comma
            translation = translate_text_return(line.strip("/n"),to_language)
            translations.append(translation)
            thread = threading.Thread(target=show_text_line, args=(translations,))
            thread.start()
            threads.append(thread)
    # Stop all thread
    for thread in threads:
        thread.join()
    # Define file path
    translated_file_path = "translated_file" + os.path.basename(file_path)
    error_output.config(bg="white",text="File translation completed, you can save the translated result")
# Showing translated result in text box
def show_text_line(translations):
    # Delete the previous output
    translated_text.delete("1.0", "end")
    # Show up the new output
    translated_text.insert("1.0", str(translations).strip('\'[]').replace("', '", " "))

# Transfer the language name which showing in the drop_down into a shortcut in order to make program recognize which language we want to translate to
def name_to_shortcut(lan_name):
    for i in language["language"]:
        if lan_name== i["name"]:
             return i["shortcut"]

# Save the text
def save_translated_text(file_path,text,to_lan):
    # Check if input values are exited
    if  text == "":
        error_output.config(text="Please type the text you want to translate to")
    elif to_lan == "":
        error_output.config(text="Please select a language you want to translate to")
        return
    # If program has already processed translated_file function, then the translated_file_path is True
    if "translated_file" in translated_file_path:
        with open(translated_file_path, "w", encoding="utf-8") as file:
            file.write("/n".join(text))
            error_output.config(bg="white",text="Translated result has written into the file:" + translated_file_path)
            return
    else:
        with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
                error_output.config(bg="white",text="Translated result has written into the file:" + file_path)
# Start the threading
def threading_start(to_lan):
    # Call work function
    t1 = threading.Thread(target=translate_file,args=(to_lan,))
    t1.start()

# Screen initiation
window = tk.Tk()
window.title("Translator")
window.geometry("1200x600")
window.config(bg="light pink")

# Language name list for combobox dropdown
language_name = []
for i in language["language"]:
    language_name.append(i["name"])

# Variable
common_translated_file_path = "translated_text"
global translated_file_path
translated_file_path = ""
# Label widget
title_label = ctk.CTkLabel(window,text="This Is A Translator Program",font=("Times New Roman", 26, "bold"),anchor=tk.CENTER,text_color="black",bg_color="yellow")
Enter_text_label = tk.Label(window,text="Enter Text",bg="white")
output_text_label= tk.Label(window,text="Output",bg="white")
drop_down_label = tk.Label(window,text="Choose the language you want to translate to:")
error_output = tk.Label(window,bg="light pink")

# Button widget
translate_button = ctk.CTkButton(window,
                                 command=lambda:translate_text(text=text_input.get("1.0", "end-1c"),       # The value from input text box
                                                               to_language=want_to_translate_text_dropdown.get()),
                                 text="Translate Text",corner_radius=30,
                                 fg_color=("black", "black"),
                                font=("Times New Roman", 15, "bold"))
translate_file_button = ctk.CTkButton(window,
                                      command=lambda: threading_start(want_to_translate_text_dropdown.get()), # Drop-down variable
                                      text="Translate File's Text",
                                      corner_radius=30,
                                      fg_color=("black", "black"),
                                    font=("Times New Roman", 15, "bold"))
save_text_button = ctk.CTkButton(window,
                                 command=lambda:save_translated_text(file_path=common_translated_file_path,
                                                                     text=translated_text.get("1.0", "end-1c"), # The value  from result text box
                                                                     to_lan=want_to_translate_text_dropdown.get()),
                                 text="Save Translated Text",
                                 corner_radius=30,
                                 fg_color=("black", "black"),
                                    font=("Times New Roman", 15, "bold"))

# Text widget
translated_text = tk.Text(window, wrap=tk.WORD, borderwidth=2, relief="solid", font=("Times New Roman", 15, "bold"),yscrollcommand="True",width=35,height=10)
text_input = tk.Text(window, wrap=tk.WORD, borderwidth=2, relief="solid", font=("Times New Roman", 15, "bold"),yscrollcommand="True",width=35,height=10)

# Combobox - dropdown
want_to_translate_text_dropdown = ttk.Combobox(window, values=language_name)

# Grid layout

# Column 1
Enter_text_label.grid(row=1,column=0)
text_input.grid(row=2,column=0,padx=10)
drop_down_label.grid(row=3,column=0,padx=10)
want_to_translate_text_dropdown.grid(row=4,column=0,padx=5)

# Column 2
title_label.grid(row=0,column=1)
translate_button.grid(row=3,column=1,pady=10)
translate_file_button.grid(row=4,column=1,pady=10)
save_text_button.grid(row=5,column=1,pady=10)
error_output.grid(row=6,column=1)

# Column 3
output_text_label.grid(row=1,column=2,padx=10)
translated_text.grid(row=2,column=2,pady=10)

window.mainloop()