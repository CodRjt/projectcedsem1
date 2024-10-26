import tkinter as tk

def process_choice():
    selected_indices = listbox.curselection()  # Get the indices of the selected items
    selected_values = [listbox.get(i) for i in selected_indices]  # Fetch the selected items
    print(f"User selected: {selected_values}")

win = tk.Tk()
win.title("Multi-Choice Selection")

# Create a Listbox with MULTIPLE selection mode
listbox = tk.Listbox(win, selectmode=tk.MULTIPLE, height=5)  # 'height' specifies how many items are visible
options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

# Insert options into Listbox
for option in options:
    listbox.insert(tk.END, option)

listbox.pack(pady=10)

# Create a button to process the choice
btn = tk.Button(win, text="Submit", command=process_choice)
btn.pack(pady=10)

win.mainloop()
