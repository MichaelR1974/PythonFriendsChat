import tkinter as tk
from tkinter import END, StringVar


root = tk.Tk()
root.title("Friendschat")
icon_img = tk.PhotoImage(file="PeopleFriends.64.png")
root.iconphoto(False, icon_img)
root.geometry("400x600")
root.config(bg="#005657")

# Farben
input_color = "#4f646f"
output_color = "#dee7e7"
menu_bg_normal = "#4f646f"
menu_bg_hover  = "#6f848f"

# --- Scrollbarer Output-Bereich ---
output_frame = tk.Frame(root, bg=output_color)
output_frame.pack(padx=10, pady=(10,0), fill="both", expand=True)

canvas = tk.Canvas(output_frame, bg=output_color, highlightthickness=0)
scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=output_color)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0,0), window=scrollable_frame, anchor="nw",width=360)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Eingabe unten ---
input_frame = tk.LabelFrame(root, bg=input_color)
input_frame.pack(pady=10, fill="x")

message_entry = tk.Entry(input_frame, width=25)
message_entry.grid(row=0, column=0, padx=10, pady=10)

send_button = tk.Button(input_frame, text="Send")
send_button.grid(row=0, column=1, padx=10, pady=10)

# --- Smiley-Bilder laden ---
happy = tk.PhotoImage(file="Messenger.64.png")
sad   = tk.PhotoImage(file="Messenger.64.png")
love  = tk.PhotoImage(file="Messenger.64.png")
arrow = tk.PhotoImage(file="arrow_down.png")

selected_smiley = tk.StringVar()
selected_smiley.set("---")

# Events zum Öffnen des Menüs
def open_dropdown(event=None):
    dropdown_menu.tk_popup(dropdown_frame.winfo_rootx(),
                           dropdown_frame.winfo_rooty() + dropdown_frame.winfo_height())

dropdown_frame = tk.Frame(input_frame, bg=input_color)
dropdown_frame.grid(row=0, column=2, padx=5)

# Anzeige der aktuellen Auswahl
selected_label = tk.Label(
    dropdown_frame,
    textvariable=selected_smiley,
    bg=input_color,
    
)
selected_label.pack(side="left", padx=(5, 0))

# Pfeil rechts daneben
arrow_button = tk.Label(
    dropdown_frame,
    image=arrow,
    bg=input_color,
)
arrow_button.pack(side="left",padx=5)

arrow_button.bind("<Button-1>",open_dropdown)
selected_label.bind("<Button-1>",open_dropdown)



def apply_hover_effects():
    # über alle Menüeinträge iterieren
    for i in range(dropdown_menu.index("end") + 1):
        # jedes Menü-Entry bekommt eigene Bindings
        dropdown_menu.entryconfig(i, background=menu_bg_normal)

        # Hover-Effekt erzeugen
        def on_enter(e, index=i):
            dropdown_menu.entryconfig(index, background=menu_bg_hover)

        def on_leave(e, index=i):
            dropdown_menu.entryconfig(index, background=menu_bg_normal)

        dropdown_menu.bind_class("Menu", "<Enter>", on_enter)
        dropdown_menu.bind_class("Menu", "<Leave>", on_leave)



dropdown_menu = tk.Menu(root, tearoff = 0, postcommand = apply_hover_effects)
dropdown_menu.add_command(
    image="",
    command=None)
dropdown_menu.add_command(
    image=happy,
    command=lambda: selected_smiley.set("Happy")
)

dropdown_menu.add_command(
    image=sad,
    command=lambda: selected_smiley.set("Sad")
)

dropdown_menu.add_command(
    image=love,
    command=lambda: selected_smiley.set("Love")
)

# --- Nachrichten senden ---
def send_message():
    text = message_entry.get()
    choice = selected_smiley.get()

    #Image Smiley Auswahl
    if choice == "Happy":
        img = happy
    elif choice == "Sad":
        img = sad
    elif choice == "Love":
        img = love
    else:
        img = None  # keine Auswahl

    msg_label = tk.Label(scrollable_frame,
                        text= text, 
                        image=img,
                        compound="left",
                        bg=output_color, 
                        font=("Helvetica",12))
    msg_label.pack(anchor="w", padx=10, pady=2)

    message_entry.delete(0, END)

    canvas.update_idletasks()
    canvas.yview_moveto(1)

send_button.config(command=send_message)

# Überschrift im scrollbaren Bereich
output_label = tk.Label(scrollable_frame, text="--- Welcome to privat chat ---",
                        fg=input_color, bg=output_color,
                        font=('Helvetica bold',18))
output_label.pack(pady=15)

root.mainloop()

###########################################################################################
# Menü erstellen
# dropdown_menu = tk.Menu(root, tearoff=0)
# dropdown_menu.add_command(label="Happy", command=lambda: selected_smiley.set("Happy"))
# dropdown_menu.add_command(label="Sad", command=lambda: selected_smiley.set("Sad"))
# dropdown_menu.add_command(label="Love", command=lambda: selected_smiley.set("Love"))
############################################################################################
# dropdown = tk.OptionMenu(input_frame, selected_smiley, "Happy", "Sad", "Love")
# dropdown.grid(row=0, column=2, columnspan=2, pady=10)


#Menü mit Bildern befüllen
#menu = dropdown["menu"]
# menu.delete(0, "end")
# menu.add_command(label="---", command=lambda: selected_smiley.set("---"))
# menu.add_command(label="Happy", image=happy_img, compound="left",
#                  command=lambda: selected_smiley.set("Happy"))
# menu.add_command(label="Sad", image=sad_img, compound="left",
#                  command=lambda: selected_smiley.set("Sad"))
# menu.add_command(label="Love", image=love_img, compound="left",
#                  command=lambda: selected_smiley.set("Love"))

# --- Mini Dropdown (eigene Auswahl) ---
