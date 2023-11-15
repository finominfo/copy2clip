import tkinter as tk
from tkinter import StringVar
import pyperclip
import yaml

class TableApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.selected_payment = StringVar()
        self.selected_payment.set(list(self.data.keys())[0])  # Set the default selected payment
        self.create_dropdown()
        self.create_table()

        # Make the window draggable
        self.root.bind('<B1-Motion>', self.drag_window)
        self.root.bind('<Button-1>', self.click_window)

    def create_dropdown(self):
        # Create a dropdown menu to select the payment
        payment_menu = tk.OptionMenu(self.root, self.selected_payment, *self.data.keys())
        payment_menu.grid(row=0, column=0, pady=10)

        # Bind a function to update the table when the selected payment changes
        self.selected_payment.trace_add('write', self.update_table)

    def create_table(self):
        # Create a table with 1 column and 7 rows for the selected payment
        font_size = 14  # Set the desired font size
        font = ("Arial", font_size)

        for i, text in enumerate(self.data[self.selected_payment.get()]):
            row_label = tk.Label(self.root, text=text, padx=10, pady=5, font=font)
            row_label.grid(row=i + 1, column=0)  # Start from row 1 to leave space for the dropdown

            # Bind the click event to a function that copies the text to the clipboard
            row_label.bind('<Button-1>', lambda event, t=text: self.copy_to_clipboard(t))

    def update_table(self, *args):
        # Update the table when the selected payment changes
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_dropdown()
        self.create_table()

    def copy_to_clipboard(self, text):
        # Copy the clicked text to the clipboard
        pyperclip.copy(text)
        print(f'Copied to clipboard: {text}')

    def click_window(self, event):
        # Store the initial position of the mouse click for window dragging
        self.x = event.x
        self.y = event.y

    def drag_window(self, event):
        # Move the window based on the mouse movement
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f'+{x}+{y}')

def read_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

if __name__ == "__main__":
    # Specify the path to your YAML file
    yaml_file_path = 'copy2clip.yaml'

    # Read data from the YAML file
    payment_data = read_yaml_file(yaml_file_path)

    # Create the main window
    root = tk.Tk()
    root.title("Copy2Clip")

    # Create an instance of the TableApp class
    app = TableApp(root, payment_data)

    # Start the main loop
    root.mainloop()
