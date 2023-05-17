import importlib
import subprocess
def install_pillow_if_needed():
    try:
        importlib.import_module('PIL')
    except ImportError:
        subprocess.call(['pip', 'install', 'Pillow'])
        print("Pillow installed successfully!")
install_pillow_if_needed()
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from PIL import Image, ImageTk

root = tk.Tk()
root.title("HP Calculator for D&D")
window_width = 1344
window_height = 195

def save_data(name_vars, max_hp_vars, current_hp_vars, status_vars, class_vars, subclass_vars, ac_vars):
    # Update the player_data dictionary with the values from the StringVar objects
    for i, player in enumerate(players):
        name = name_vars[i].get()
        player_data[player]["name"] = name.encode('utf-8').decode('unicode_escape')

        if isinstance(max_hp_vars[i], tk.StringVar):
            player_data[player]["max_hp"] = max_hp_vars[i].get()
        else:
            player_data[player]["max_hp"] = max_hp_vars[i]

        if isinstance(current_hp_vars[i], tk.StringVar):
            player_data[player]["current_hp"] = current_hp_vars[i].get()
        else:
            player_data[player]["current_hp"] = current_hp_vars[i]

        if isinstance(status_vars[i], tk.StringVar):
            player_data[player]["status"] = status_vars[i].get()
        else:
            player_data[player]["status"] = status_vars[i]

        if isinstance(class_vars[i], tk.StringVar):
            player_data[player]["class"] = class_vars[i].get()
        else:
            player_data[player]["class"] = class_vars[i]

        if isinstance(subclass_vars[i], tk.StringVar):
            player_data[player]["subclass"] = subclass_vars[i].get()
        else:
            player_data[player]["subclass"] = subclass_vars[i]

        if isinstance(ac_vars[i], tk.StringVar):
            player_data[player]["ac"] = ac_vars[i].get()
        else:
            player_data[player]["ac"] = ac_vars[i]

    # Save the data to the file
    try:
        with open("player_data.json", "w") as f:
            json.dump(player_data, f, indent=4, default=str)
    except Exception as e:
        print(f"Error saving data: {e}")

    # Extract the names from the name_vars list
    names = [name_var.get() for name_var in name_vars]

    # Save the names to a separate file
    try:
        with open("names.json", "w") as f:
            json.dump(names, f, indent=4)
    except Exception as e:
        print(f"Error saving names: {e}")

    # Print a success message
    print("Data saved successfully.")

# create a list of player names
players = ["Player 1", "Player 2", "Player 3", "Player 4"]
player_data = {}

# load player data from JSON file
def load_data():
    global player_data
    with open("player_data.json", "r") as file:
        player_data = json.load(file)
        for player in player_data:
            name_var = tk.StringVar()
            name_var.set(player_data[player]["name"])
            max_hp_var = tk.StringVar()
            max_hp_var.set(player_data[player]["max_hp"])
            current_hp_var = tk.StringVar()
            current_hp_var.set(player_data[player]["current_hp"])
            status_var = tk.StringVar()
            status_var.set(player_data[player]["status"])
            class_var = tk.StringVar()
            class_var.set(player_data[player]["class"])
            subclass_var = tk.StringVar()
            subclass_var.set(player_data[player]["subclass"])
            ac_var = tk.StringVar()
            ac_var.set(player_data[player].get("ac", ""))
            player_data[player]["name_var"] = name_var
            player_data[player]["max_hp_var"] = max_hp_var
            player_data[player]["current_hp_var"] = current_hp_var
            player_data[player]["status_var"] = status_var
            player_data[player]["class_var"] = class_var
            player_data[player]["subclass_var"] = subclass_var
            player_data[player]["ac_var"] = ac_var
            
    return player_data

# Load player data from JSON file
load_data()

if not player_data:
    # Handle the case when player_data is empty
    # For example, display a message or initialize the player_data dictionary
    player_data = {}  # Initialize an empty dictionary if player_data is empty

# create player data for any missing players
for player in players:
    if player not in player_data:
        player_data[player] = {
            "name_var": tk.StringVar(),
            "max_hp_var": tk.StringVar(),
            "current_hp_var": tk.StringVar(),
            "status_var": tk.StringVar(),
        }

# function to update the player data file
def update_player_data(event, player, max_hp_var, current_hp_var, status_var, name_var):
    player_data[player]["name"] = name_var.get()
    player_data[player]["current_hp"] = current_hp_var
    
    # Check if max_hp_var is a StringVar or a string
    if isinstance(max_hp_var, tk.StringVar):
        player_data[player]["max_hp"] = max_hp_var.get()
    else:
        player_data[player]["max_hp"] = max_hp_var
    
    player_data[player]["status"] = status_var
    player_data[player]["class"] = class_var.get()
    player_data[player]["subclass"] = subclass_var.get()
    player_data[player]["ac"] = ac_var.get()

# function to calculate the status of a player based on their current hp
def get_status(player):
    current_hp = int(player_data[player]["current_hp_entry"].get())
    max_hp = player_data[player]["max_hp"]
    if current_hp <= 0:
        return "Unconscious"
    elif current_hp <= max_hp / 2:
        return "Injured"
    else:
        return "Healthy"

# function to apply healing to a player
def apply_healing(player, healing_entry):
    current_hp_var = player_data[player]["current_hp_entry"]
    current_hp = int(player_data[player]["current_hp_entry"].get())
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
    max_hp = player_data[player]["max_hp"]
    if new_hp > max_hp:
        new_hp = max_hp
    
    # update the current_hp variable and the entry widget
    current_hp_var.set(new_hp)
    player_data[player]["current_hp_entry"].delete(0, tk.END)
    player_data[player]["current_hp_entry"].insert(0, new_hp)
    
    update_player_data(player)

# function to apply damage to a player
def apply_damage(player, damage_entry):
    try:
        current_hp_var = player_data[player]["current_hp_entry"]
        current_hp = int(current_hp_var.get())
        damage = int(damage_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid damage value.")
        return

    # Check if the damage value is non-negative
    if damage < 0:
        messagebox.showerror("Error", "Damage value cannot be negative.")
        return

    new_hp = current_hp - damage

    # make sure new_hp does not exceed max_hp
    max_hp = player_data[player]["max_hp"]
    if new_hp > max_hp:
        new_hp = max_hp
    
    # update the current_hp variable and the entry widget
    current_hp_var.set(new_hp)
    player_data[player]["current_hp_entry"].delete(0, tk.END)
    player_data[player]["current_hp_entry"].insert(0, new_hp)
    
    update_player_data(player)

def load_background_image():
    try:
        # Load the background image
        background_image = Image.open('backgrounds/background_image.jpg')

        # Calculate the window size
        window_width = 1344
        window_height = 195

        # Resize the background image to fit the window resolution
        resized_image = background_image.resize((window_width, window_height), Image.LANCZOS)

        # Convert the resized image to a format compatible with Tkinter
        tk_image = ImageTk.PhotoImage(resized_image)

        # Create a label and set the background image
        background_label = tk.Label(root, image=tk_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        return tk_image

    except Exception as e:
        print("Error loading background image:", e)
        return None
        
tk_image = load_background_image()

# add widgets to the window
def create_widgets():
    max_hp_vars = []
    current_hp_vars = []
    status_vars = []
    tk_image = load_background_image()
    
    for row, player in enumerate(players):
        player_label = tk.Label(root, text=f"{player}")
        player_label.grid(row=row+1, column=0)

        name_var = tk.StringVar(value=player_data[player].get("name", player))
        player_data[player]["name_var"] = name_var

        player_entry = tk.Entry(root, textvariable=name_var)
        player_entry.grid(row=row+1, column=1)

        # add current hp label and entry
        current_hp_label = tk.Label(root, text="Current HP")
        current_hp_label.grid(row=row+1, column=2)

        # create a separate current_hp_var for each player
        current_hp_var = tk.StringVar(value=player_data[player].get("current_hp", "10"))
        current_hp_entry = tk.Entry(root, textvariable=current_hp_var)
        current_hp_entry.grid(row=row+1, column=3)
        player_data[player]["current_hp_var"] = current_hp_var
        player_data[player]["current_hp_entry"] = current_hp_entry  # add current_hp_entry to player_data
        current_hp_vars.append(current_hp_var)  # add current_hp_var to current_hp_vars list

        # add max hp label and entry
        max_hp_label = tk.Label(root, text="Max HP")
        max_hp_label.grid(row=row+1, column=4)

        max_hp_var = tk.StringVar(value=player_data[player].get("max_hp", "10"))
        max_hp_entry = tk.Entry(root, textvariable=max_hp_var)
        max_hp_entry.grid(row=row+1, column=5)
        player_data[player]["max_hp_var"] = max_hp_var
        player_data[player]["max_hp_entry"] = max_hp_entry  # add max_hp_entry to player_data
        max_hp_vars.append(max_hp_var)  # add max_hp_var to max_hp_vars list

        # add AC label and entry
        ac_label = tk.Label(root, text="AC")
        ac_label.grid(row=row+1, column=6)

        ac_var = tk.StringVar(value=player_data[player].get("ac", "10"))
        ac_entry = tk.Entry(root, textvariable=ac_var)
        ac_entry.grid(row=row+1, column=7)
        player_data[player]["ac_var"] = ac_var
        player_data[player]["ac_entry"] = ac_entry  # add ac_entry to player_data

        # create a label for the dropdown menu
        dropdown_var = tk.StringVar(value=player_data[player].get("status", "None"))
        dropdown = tk.OptionMenu(root, dropdown_var, "None", "Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious", "Exhaustion")
        dropdown.grid(row=row+1, column=10, sticky="W", padx=0, pady=0)  # Set padx and pady to zero
        player_data[player]["status_var"] = dropdown_var
        
        class_dropdown_var = tk.StringVar(value=player_data[player].get("class", "None"))
        class_dropdown = tk.OptionMenu(root, class_dropdown_var, "Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard")
        class_dropdown.grid(row=row+1, column=8, sticky="W", padx=(0, 5), pady=0)  # Adjust padx value as needed
        player_data[player]["class_var"] = class_dropdown_var
    
        # Create the subclass dropdown menu
        subclass_dropdown_var = tk.StringVar(value="None")
        subclass_dropdown_menu = tk.Menu(root, tearoff=0)
        subclasses = (
                                "None",
                                 "Armorer (Artificer)",
                                 "Alchemist (Artificer)",
                                 "Artillerist (Artificer)",
                                 "Battle Smith (Artificer)",
                                 "Berserker (Barbarian)",
                                 "Totem Warrior (Barbarian)",
                                 "Ancestral Guardian (Barbarian)",
                                 "Storm Herald (Barbarian)",
                                 "Zealot (Barbarian)",
                                 "Beast (Barbarian)",
                                 "Wild Soul (Barbarian)",
                                 "Battlerager (Barbarian)",
                                 "College of Lore (Bard)",
                                 "College of Valor (Bard)",
                                 "College of Creation (Bard)",
                                 "College of Glamor (Bard)",
                                 "College of Swords (Bard)",
                                 "College of Whispers (Bard)",
                                 "College of Eloquence (Bard)",
                                 "College of Spirits (Bard)",
                                 "Knowledge Domain (Cleric)",
                                 "Life Domain (Cleric)",
                                 "Light Domain (Cleric)",
                                 "Nature Domain (Cleric)",
                                 "Tempest Domain (Cleric)",
                                 "Trickery Domain (Cleric)",
                                 "War Domain (Cleric)",
                                 "Death Domain (Cleric)",
                                 "Twilight Domain (Cleric)",
                                 "Order Domain (Cleric)",
                                 "Forge Domain (Cleric)",
                                 "Grave Domain (Cleric)",
                                 "Peace Domain (Cleric)",
                                 "Arcane Domain (Cleric)",
                                 "Circle of the Land (Druid)",
                                 "Circle of the Moon (Druid)",
                                 "Circle of Dreams (Druid)",
                                 "Circle of the Shepherd (Druid)",
                                 "Circle of Spores (Druid)",
                                 "Circle of Stars (Druid)",
                                 "Circle of Wildfire (Druid)",
                                 "Champion (Fighter)",
                                 "Battle Master (Fighter)",
                                 "Eldritch Knight (Fighter)",
                                 "Arcane Archer (Fighter)",
                                 "Cavalier (Fighter)",
                                 "Samurai (Fighter)",
                                 "Psi Warrior (Fighter)",
                                 "Rune Knight (Fighter)",
                                 "Echo Fighter (Fighter)",
                                 "Purple Dragon Knight (Fighter)",
                                 "Way of the Open Hand (Monk)",
                                 "Way of the Shadow (Monk)",
                                 "Way of the Four Elements (Monk)",
                                 "Way of Mercy (Monk)",
                                 "Way of the Astral Self (Monk)",
                                 "Way of the Drunken Master (Monk)",
                                 "Way of the Kensei (Monk)",
                                 "Way of the Sun Soul (Monk)",
                                 "Way of Long Death (Monk)",
                                 "Way of the Ascendant Dragon (Monk)",
                                 "Oath of Devotion (Paladin)",
                                 "Oath of the Ancients (Paladin)",
                                 "Oath of Vengeance (Paladin)",
                                 "Oathbreaker (Paladin)",
                                 "Oath of Conquest (Paladin)",
                                 "Oath of Redemption (Paladin)",
                                 "Oath of Glory (Paladin)",
                                 "Oath of the Watchers (Paladin)",
                                 "Oath of the Crown (Paladin)",
                                 "Fey Wanderer (Ranger)",
                                 "Swarmkeeper (Ranger)",
                                 "Gloom Stalker (Ranger)",
                                 "Horizon Walker (Ranger)",
                                 "Monster Slayer (Ranger)",
                                 "Hunter (Ranger)",
                                 "Beast Master (Ranger)",
                                 "Drakewarden (Ranger)",
                                 "Thief (Rogue)",
                                 "Assassin (Rogue)",
                                 "Arcane Trickster (Rogue)",
                                 "Inquisitive (Rogue)",
                                 "Mastermind (Rogue)",
                                 "Scout (Rogue)",
                                 "Swashbuckler (Rogue)",
                                 "Phantom (Rogue)",
                                 "Soulknife (Rogue)",
                                 "Abberant Mind(Sorcerer)",
                                 "Clockwork Soul(Sorcerer)",
                                 "Divine Soul(Sorcerer)",
                                 "Shadow Magic (Sorcerer)",
                                 "Storm Sorcery (Sorcerer)",
                                 "Draconic Bloodline (Sorcerer)",
                                 "Wild Magic (Sorcerer)",
                                 "The Archfey (Warlock)",
                                 "The Fiend (Warlock)",
                                 "The Great Old One (Warlock)",
                                 "The Celestial (Warlock)",
                                 "Undying (Warlock)",
                                 "The Hexblade (Warlock)",
                                 "The Fathomless (Warlock)",
                                 "The Genie (Warlock)",
                                 "The Undead (Warlock)",
                                 "School of Abjuration (Wizard)",
                                 "School of Conjuration (Wizard)",
                                 "School of Divination (Wizard)",
                                 "School of Enchantment (Wizard)",
                                 "School of Evocation (Wizard)",
                                 "School of Illusion (Wizard)",
                                 "School of Necromancy (Wizard)",
                                 "School of Transmutation (Wizard)",
                                 "School of Graviturgy (Wizard)",
                                 "School of Chonurgy (Wizard)",
                                 "War Magic (Wizard)",
                                 "Bladesinging (Wizard)",
                                 "Order of Scribes (Wizard)")
        subclass_dropdown = tk.OptionMenu(root, subclass_dropdown_var, *subclasses)
        subclass_dropdown.grid(row=row+1, column=9, sticky="W", padx=5, pady=5)

        # Set the width of the subclass button
        max_subclass_length = max(len(subclass) for subclass in subclasses)
        subclass_dropdown.config(width=max_subclass_length + 2)  # Add some padding
        pass

# Associate the dropdown menu with the variable
        subclass_dropdown_var.set(subclasses[0])  # Set the initial value

    #save_button = tk.Button(root, text="Save Names", command=save_names)
    #save_button.grid(row=len(players)+1, column=0)

    return max_hp_vars, current_hp_vars, status_vars

create_widgets()
def save_names():
    names = [player_data[player]["name_var"].get() for player in players]
    print("Saved Names:", names)

max_hp_vars, current_hp_vars, status_vars = create_widgets()

def apply_damage_to_player(player, damage_entry):
    try:
        damage = int(damage_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for damage.")
        return
    current_hp_entry = player_data[player]["current_hp_entry"]
    current_hp = int(current_hp_entry.get())
    new_hp = current_hp - damage
    player_data[player]["current_hp"] = new_hp
    current_hp_var = player_data[player]["current_hp_var"]
    current_hp_var.set(new_hp)

def apply_healing(player, healing_entry):
    try:
        healing = int(healing_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for healing.")
        return
    current_hp_entry = player_data[player]["current_hp_entry"]
    current_hp = int(current_hp_entry.get())
    max_hp_entry = player_data[player]["max_hp_entry"]
    max_hp = int(max_hp_entry.get())
    new_hp = min(current_hp + healing, max_hp)
    player_data[player]["current_hp"] = new_hp
    current_hp_var = player_data[player]["current_hp_var"]
    current_hp_var.set(new_hp)

# add dropdown menu to select player for damage/healing
player_choice = tk.StringVar()
player_choice.set(players[0])
player_dropdown = tk.OptionMenu(root, player_choice, *players)
player_dropdown.grid(row=0, column=0)

# add entry for damage
damage_label = tk.Label(root, text="Damage")
damage_label.grid(row=0, column=2)

damage_entry = tk.Entry(root)
damage_entry.grid(row=0, column=3)
damage_button = tk.Button(root, text="Apply Damage", command=lambda: apply_damage_to_player(player_choice.get(), damage_entry))
damage_button.grid(row=0, column=4)

# add entry for healing
healing_label = tk.Label(root, text="Healing")
healing_label.grid(row=0, column=5)

healing_entry = tk.Entry(root)
healing_entry.grid(row=0, column=6)

# add button to apply healing
healing_button = tk.Button(root, text="Apply Healing", command=lambda: apply_healing(player_choice.get(), healing_entry), textvariable=healing_label)
healing_button.grid(row=0, column=7)

def print_window_resolution():
    # Function to be called after a delay
    def get_window_resolution():
        width = root.winfo_width()
        height = root.winfo_height()
        print(f"Window resolution: {width}x{height}")
        root.destroy()

    # Delay the function call by 100ms to ensure the window is displayed
    root.after(100, get_window_resolution)
#print_window_resolution()

# create a function to handle the window closing event
def on_closing():
    # Retrieve the values from the entries and store them in lists
    name_vars = [player_data[player]["name_var"] for player in players]
    max_hp_vars = [player_data[player]["max_hp_var"] for player in players]
    current_hp_vars = [player_data[player]["current_hp_var"] for player in players]
    status_vars = [player_data[player]["status_var"] for player in players]
    class_vars = [player_data[player]["class_var"] for player in players]
    subclass_vars = [player_data[player]["subclass_var"] for player in players]
    ac_vars = [player_data[player]["ac_var"] for player in players]

    # Extract the string values from max_hp_vars, current_hp_vars, and status_vars
    max_hp_values = [var.get() if isinstance(var, tk.StringVar) else var for var in max_hp_vars]
    current_hp_values = [var.get() if isinstance(var, tk.StringVar) else var for var in current_hp_vars]
    status_values = [var.get() if isinstance(var, tk.StringVar) else var for var in status_vars]

    save_data(name_vars, max_hp_values, current_hp_values, status_values, class_vars, subclass_vars, ac_vars)

    # Destroy the window
    root.destroy()

# start the main event loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
# used this to determine the original window resolution
#print_window_resolution()