import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter App")
        self.geometry("400x300")
        # Creating the first multi-select field
        self.first_field()
        # Creating the second multi-select field
        self.second_field()

    def first_field(self):
        label = ttk.Label(self, text="First Field:")
        label.grid(column=0, row=0, padx=10, pady=10)

        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        listbox.grid(column=1, row=0, padx=10, pady=10)

        def on_select(event=None):
            selection = ', '.join(map(str, listbox.curselection()))

        listbox.bind("<<ListboxSelect>>", on_select)

        values = ['Option 1', 'Option 2', 'Option 3']
        for item in values:
            listbox.insert(tk.END, item)

    def second_field(self):
        label = ttk.Label(self, text="Second Field:")
        label.grid(column=0, row=1, padx=10, pady=10)

        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        listbox.grid(column=1, row=1, padx=10, pady=10)

        def on_select(event=None):
            selection = ', '.join(map(str, listbox.curselection()))

        listbox.bind("<<ListboxSelect>>", on_select)

        values = ['Option A', 'Option B', 'Option C']
        for item in values:
            listbox.insert(tk.END, item)

if __name__ == "__main__":
    app = App()
    app.mainloop()
