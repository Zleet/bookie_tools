# ============================================================================
# Line Feeder
# Paste a bunch of text
# Every time the Paste Line button is pressed, the next line is copied to
# the system clipboard, ready for pasting elsewhere
# ============================================================================
# Imports
from tkinter import *
from tkinter import ttk
import random

current_line_no = 0 # keep a record of the current line index (from zero upwards)
# ============================================================================
# Get the text from the text widget
def get_lines():

    text = all_text_box.get("1.0", END)
    text = text.strip()

    lines = text.split("\n")

    return lines
# ============================================================================
# Start line feeder
def start_line_feeder():

    global current_line_no
    current_line_no = 0 # reset to first line of text

    # remove 'highlighted_line' tag
    all_text_box.tag_remove('highlighted_line', 1.0, END)

    lines = get_lines()
    total_lines = len(lines)

    # Delete current contents of current_line_text_box, then insert first line
    # into it
    current_line_text_box.delete('1.0', END)
    current_line_text = lines[0] + '   (' + str(current_line_no + 1) + '/'
    current_line_text += str(total_lines) + ')'
    current_line_text_box.insert('1.0', current_line_text)

    # add a tag to the current line in all_text_box (remembering that lines
    # in tkinter Text widgets begin at 1.0!)
    # Then highlight the line
    start_index = str(current_line_no + 1) + '.0'
    end_index = str(current_line_no + 1) + '.end'
    all_text_box.tag_add('highlighted_line', start_index, end_index)
    all_text_box.tag_configure('highlighted_line', background='yellow', foreground='black')
    
    # Copy current line to system clipboard
    new_window = Tk()
    new_window.withdraw()
    new_window.clipboard_clear()
    new_window.clipboard_append(lines[0])
    new_window.destroy()

    return
# ============================================================================
def move_up_a_line():

    global current_line_no

    lines = get_lines()
    total_lines = len(lines)

    current_line_no -= 1
    if current_line_no < 0:
        current_line_no = total_lines - 1

    # Delete current contents of current_line_text_box, then insert current line
    # into it
    current_line_text_box.delete('1.0', END)
    current_line_text = lines[current_line_no] + '   (' + str(current_line_no + 1) + '/'
    current_line_text += str(total_lines) + ')'
    current_line_text_box.insert('1.0', current_line_text)

    # remove 'highlighted_line' tag
    all_text_box.tag_remove('highlighted_line', 1.0, END)

    # add a tag to the current line in all_text_box (remembering that lines
    # in tkinter Text widgets begin at 1.0!)
    # Then highlight the line
    start_index = str(current_line_no + 1) + '.0'
    end_index = str(current_line_no + 1) + '.end'
    all_text_box.tag_add('highlighted_line', start_index, end_index)
    all_text_box.tag_configure('highlighted_line', background='yellow', foreground='black')
    
    # Copy current line to system clipboard
    new_window = Tk()
    new_window.withdraw()
    new_window.clipboard_clear()
    new_window.clipboard_append(lines[current_line_no])
    new_window.destroy()

    return
# ============================================================================
def move_down_a_line():
    
    global current_line_no

    lines = get_lines()
    total_lines = len(lines)

    current_line_no += 1
    if current_line_no > total_lines - 1:
        current_line_no = 0

    # Delete current contents of current_line_text_box, then insert current line
    # into it
    current_line_text_box.delete('1.0', END)
    current_line_text = lines[current_line_no] + '   (' + str(current_line_no + 1) + '/'
    current_line_text += str(total_lines) + ')'
    current_line_text_box.insert('1.0', current_line_text)

    # remove 'highlighted_line' tag
    all_text_box.tag_remove('highlighted_line', 1.0, END)

    # add a tag to the current line in all_text_box (remembering that lines
    # in tkinter Text widgets begin at 1.0!)
    # Then highlight the line
    start_index = str(current_line_no + 1) + '.0'
    end_index = str(current_line_no + 1) + '.end'
    all_text_box.tag_add('highlighted_line', start_index, end_index)
    all_text_box.tag_configure('highlighted_line', background='yellow', foreground='black')
    
    # Copy current line to system clipboard
    new_window = Tk()
    new_window.withdraw()
    new_window.clipboard_clear()
    new_window.clipboard_append(lines[current_line_no])
    new_window.destroy()

    return
# ============================================================================
# Set up the interface
# Basic window
root = Tk()
root.wm_title("LineFeeder (Amelyn Technologies 2016)")

# Frame to hold the four buttons. We're going to grid the buttons in the button_frame,
# then grid the button_frame in the root
button_frame = ttk.Frame(root)

# Set up buttons, grid them into button_frame
down_button = ttk.Button(button_frame, text='Down', command=move_down_a_line)
down_button.grid(row=0, column=0)

up_button = ttk.Button(button_frame, text='Up', command=move_up_a_line)
up_button.grid(row=0, column=1)

start_button = ttk.Button(button_frame, text='Start', command=start_line_feeder)
start_button.grid(row=0, column=2)

# Grid button_frame into root
button_frame.grid(row=0, column=0, sticky=W, rowspan=2)

# Create a label and text box to display the current line and grid them onto root
# in rows 1 and 2 respectively
# current_line_label = Label(root, text="Current Line")
# current_line_label.grid(row=2, column=0, sticky=W)
current_line_text_box = Text(root, width=70, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
# current_line_text_box.grid(row=3, column=0, sticky=W)

# Create a text box for the user to paste all the text into
all_text_label = Label(root, text="Write or paste text here")
all_text_label.grid(row=2, column=0, sticky=W)
all_text_box = Text(root, width=70, height=40, background='#000000', foreground='#FFFF00',
                    insertbackground='#FFFFFF', font=('Courier', 10))
all_text_box.grid(row=3, column=0, columnspan=4)

# Start 'er up!
root.mainloop()
