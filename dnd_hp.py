import tkinter as tk
from tkinter import messagebox

# create the main window
root = tk.Tk()
root.title("HP Calculator for D&D")

# create a list of player names
players = ["Player 1", "Player 2", "Player 3", "Player 4"]

# create a dictionary to store the player data
player_data = {}

for player in players:
    # create a dictionary for each player's data
    player_data[player] = {
        "current_hp": tk.IntVar(),
        "max_hp": tk.IntVar(),
        "status": tk.StringVar(),
    }

# create a function to update a player's data
# create a function to update a player's data
def update_player_data(player):
    current_hp = player_data[player]["current_hp"].get()
    max_hp = player_data[player]["max_hp"].get()
    status = player_data[player]["status"].get()
    current_hp_entry = player_data[player]["current_hp_entry"]
    max_hp_entry = player_data[player]["max_hp_entry"]
    status_dropdown = player_data[player]["status_dropdown"]
    current_hp_entry.delete(0, tk.END)
    current_hp_entry.insert(0, current_hp)
    max_hp_entry.delete(0, tk.END)
    max_hp_entry.insert(0, max_hp)
    status_dropdown.set(status)
    
# create a function to apply damage
def apply_damage():
    player = player_choice.get()
    current_hp_var = player_data[player]["current_hp"]
    current_hp = current_hp_var.get()
    damage = damage_entry.get()

    # Check if the entry is empty
    if damage == '':
        messagebox.showerror("Error", "Please enter a valid damage value.")
        return

    # Convert the damage value to an integer
    try:
        damage = int(damage)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid damage value.")
        return
    
    new_hp = current_hp - damage
    
    # update the current_hp variable and the entry widget
    current_hp_var.set(new_hp)
    player_data[player]["current_hp_entry"].delete(0, tk.END)
    player_data[player]["current_hp_entry"].insert(0, new_hp)
    
    update_player_data(player)


# create a function to apply healing
# create a function to apply healing
def apply_healing():
    player = player_choice.get()
    current_hp_var = player_data[player]["current_hp"]
    current_hp = current_hp_var.get()
    healing = healing_entry.get()

    # Check if the entry is empty
    if healing == '':
        messagebox.showerror("Error", "Please enter a valid healing value.")
        return

    # Convert the healing value to an integer
    try:
        healing = int(healing)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid healing value.")
        return
    
    new_hp = current_hp + healing
    
    # make sure new_hp does not exceed max_hp
    max_hp = player_data[player]["max_hp"].get()
    if new_hp > max_hp:
        new_hp = max_hp
    
    # update the current_hp variable and the entry widget
    current_hp_var.set(new_hp)
    player_data[player]["current_hp_entry"].delete(0, tk.END)
    player_data[player]["current_hp_entry"].insert(0, new_hp)
    
    update_player_data(player)


# add widgets to the window
for row, player in enumerate(players):
    # add player name label and entry
    player_label = tk.Label(root, text=f"{player}")
    player_label.grid(row=row+1, column=0)

    player_entry = tk.Entry(root)
    player_entry.insert(0, player)
    player_entry.grid(row=row+1, column=1)

    # add current hp label and entry
    current_hp_label = tk.Label(root, text="Current HP")
    current_hp_label.grid(row=row+1, column=2)

    player_data[player]["current_hp"].set(10)  # set default value
    current_hp_var = player_data[player]["current_hp"]
    current_hp_entry = tk.Entry(root, textvariable=current_hp_var)
    current_hp_entry.grid(row=row+1, column=3)

    # add max hp label and entry
    max_hp_label = tk.Label(root, text="Max HP")
    max_hp_label.grid(row=row+1, column=4)

    player_data[player]["max_hp"].set(10)  # set default value
    max_hp_var = player_data[player]["max_hp"]
    max_hp_entry = tk.Entry(root, textvariable=max_hp_var)
    max_hp_entry.grid(row=row+1, column=5)

    # add status dropdown menu
    dropdown_var = tk.StringVar()
    dropdown = tk.OptionMenu(root, dropdown_var, "None", "Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious", "Exhaustion")
    dropdown.grid(row=row+1, column=6)

    # store the player data in the dictionary
    player_data[player]["current_hp_entry"] = current_hp_entry
    player_data[player]["max_hp_entry"] = max_hp_entry
    player_data[player]["status_dropdown"] = dropdown_var


# add dropdown menu to select player for damage/healing
player_choice = tk.StringVar()
player_choice.set(players[0])
player_dropdown = tk.OptionMenu(root, player_choice, *players)
player_dropdown.grid(row=0, column=0)

# add entry for damage
damage_label = tk.Label(root, text="Damage")
damage_label.grid(row=0, column=1)

damage_entry = tk.Entry(root)
damage_entry.grid(row=0, column=2)

# add button to apply damage
damage_button = tk.Button(root, text="Apply Damage", command=apply_damage)
damage_button.grid(row=0, column=3)

# add entry for healing
healing_label = tk.Label(root, text="Healing")
healing_label.grid(row=0, column=4)

healing_entry = tk.Entry(root)
healing_entry.grid(row=0, column=5)

# add button to apply healing
healing_button = tk.Button(root, text="Apply Healing", command=apply_healing, textvariable=healing_label)
healing_button.grid(row=0, column=6)

# start the main loop
root.mainloop()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if root:
            root.destroy()
        sys.exit()

# add functions to update the total HP and total damage values
def update_total_hp():
        global total_hp
        total_hp = sum(player_data[player]["max_hp"].get() for player in players)
        total_hp_value_label.config(text=total_hp)

def update_total_damage():
    global total_damage
    total_damage = sum(player_data[player]["max_hp"].get() - player_data[player]["current_hp"].get() for player in players)
    total_damage_value_label.config(text=total_damage)

# bind the update functions to changes in the max hp and current hp values
for player in players:
    player_data[player]["max_hp"].trace_add("write", lambda *args: (update_player_data(player), update_total_hp(), update_total_damage()))
    player_data[player]["current_hp"].trace_add("write", lambda *args: (update_player_data(player), update_total_damage()))

# start the main event loop
root.mainloop()