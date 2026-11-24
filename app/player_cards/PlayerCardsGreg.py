import csv
import requests
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import os

def generate_player_card(user_input_username, user_input_font, user_input_colour, user_input_font_size, pose, statselection1, statselection2, statselection3, background_choice):
    img = Image.open('blank.png')
    draw = ImageDraw.Draw(img)
    # ========================== USERNAME AND USER INPUTS ==========================

    player_list_uuid = []
    player_list_name = []
    csv_data = pd.read_csv('playerlist.csv')
    player_list_uuid = csv_data['UUID'].tolist()

    a = len(player_list_uuid)
    b = 0
    while a != -1:
        a -= 1
        uuid = player_list_uuid[a]
        #print(f"Attempting to fetch URL: https://api.mojang.com/user/profile/{uuid}")
        data = requests.get(f"https://api.mojang.com/user/profile/{uuid}", timeout = 10)
        if data.status_code != 200:
            print(f"Failed to fetch profile. Status code: {data.status_code}")
            while data.status_code == 429:
                print("Rate limit exceeded, trying again after 2 seconds...")
                print(f"Attempting to fetch URL: https://api.mojang.com/user/profile/{uuid}")
                time.sleep(2)
                data = requests.get(f"https://api.mojang.com/user/profile/{uuid}", timeout = 10)
        

        if not data.text.strip():
            print("Received empty response from server.")
            continue

        data = data.json()
        data['name'] = data['name'].lower()
        player_list_name.append(data['name'])
        time.sleep(1)

        if player_list_name[b] == user_input_username.lower():
            player_uuid = uuid
            break
        b = b + 1
        print(b)


        
        


    player_name_case_sens = user_input_username
    while user_input_username.lower() not in [name.lower() for name in player_list_name]:
        print("Username not found in the player list. Please enter a valid username.")
        user_input_username = input("Enter your username: ")
        player_name_case_sens = user_input_username
        user_input_username = user_input_username.lower()



   

    url = f"https://starlight.lunareclipse.studio/api/v1/render/{pose}/{player_uuid}/full"
    response = requests.get(url)
    if response.status_code == 200:
        with open("player_skin.png", "wb") as f:
            f.write(response.content)
            print("Player skin downloaded successfully.")
    else:
        print(f"Failed to download player skin. Status code: {response.status_code}")
        print(url)
        

    for row_idx, row in enumerate(csv_data.itertuples(index=False), start=1):
        if player_uuid == row.UUID:
            player_row = row
            break


    

    if user_input_font == "Minecraft":
        font = ImageFont.truetype("Minecraft.otf", user_input_font_size)
    elif user_input_font == "Minecraft Bold":
        font = ImageFont.truetype("MinecraftBold.otf", user_input_font_size)
    elif user_input_font == "Trashhand":
        font = ImageFont.truetype("TrashHand.ttf", user_input_font_size)


    while len(user_input_colour) != 6 or not all(c in '0123456789ABCDEFabcdef' for c in user_input_colour):
        user_input_colour = input("Enter the hex colour you wish for the text (e.g. FF0000): ")
        if user_input_colour.startswith('#'):
            user_input_colour = user_input_colour[1:]
        if len(user_input_colour) != 6 or not all(c in '0123456789ABCDEFabcdef' for c in user_input_colour):
            print("Invalid input. Please enter a valid hex colour code.")

    R_value = int(user_input_colour[0:2], 16)
    G_value = int(user_input_colour[2:4], 16)
    B_value = int(user_input_colour[4:6], 16)


    #========================= ADDING PLAYER SKIN ==========================
    img = Image.open("blank.png").convert("RGBA")

    skin = Image.open("player_skin.png")

    x = 1920 - skin.width - 10
    y = (1080 - skin.height) - 63

    x0 = x - 10
    y0 = y - 10
    x1 = x + skin.width + 10
    y1 = y + skin.height + 10

    IMG_Name_Rec = ImageDraw.Draw(img)
    IMG_Name_Rec.rounded_rectangle([(x0, y0), (x1, y1)], radius=15, fill=(0, 0, 0, 100), outline=None, width=1, corners=None)

    img.paste(skin, (x, y), skin)


    #========================= ADDING PLAYER NAME ==========================   
    
    text_length = draw.textlength(player_name_case_sens, font)
    x = ((img.width - text_length) / 2) - 5
    y = img.height / 1.1 - user_input_font_size / 2

    x0 = x - 10
    y0 = y
    x1 = x + text_length + 5
    y1 = y + user_input_font_size + 5

    IMG_Name_Rec = ImageDraw.Draw(img)
    IMG_Name_Rec.rounded_rectangle([(x0, y0), (x1, y1)], radius=15, fill=(0, 0, 0, 100), outline=None, width=1, corners=None)

    IMG_username = ImageDraw.Draw(img)
    IMG_username.text((x, y), player_name_case_sens, fill=(R_value, G_value, B_value, 255), font=font)

    #========================= STATISTICS ==========================



    stat_mapping = {
        1: 0,  # Final_Kills
        2: 1,  # Kills
        3: 2,  # Average_kills_per_season
        4: 3,  # Worst_placement
        5: 4,  # Best_placement
        6: 5,  # Average_placement
        7: 6,  # Chaos_Life_placement
        8: 7   # Chaos_Life2_placement 
    }

    stat_name_mapping = {
        1: "Final kills: ",
        2: "Kills: ",
        3: "Avg kills: ",
        4: "Worst placement: ",
        5: "Best placement: ",
        6: "Avg placement: ",
        7: "CHL placement: ",
        8: "CHL^2 placement: "
    }

    stat_string_to_id = {
        "Final Kills": 1,
        "Kills": 2,
        "Average Kills per season": 3,
        "Worst placement": 4,
        "Best placement": 5,
        "Average placement": 6,
        "Chaos Life": 7,
        "Chaos Life^2": 8
    }

    statselection = [
        stat_string_to_id.get(statselection1, 1),
        stat_string_to_id.get(statselection2, 2),
        stat_string_to_id.get(statselection3, 3)
    ]

    # Fixed bug: correctly index each stat using its respective selection value
    stat1 = stat_name_mapping[statselection[0]] + str(player_row[stat_mapping[statselection[0]]])
    stat2 = stat_name_mapping[statselection[1]] + str(player_row[stat_mapping[statselection[1]]])
    stat3 = stat_name_mapping[statselection[2]] + str(player_row[stat_mapping[statselection[2]]])

    text_length1 = draw.textlength(stat1, font)
    text_length2 = draw.textlength(stat2, font)
    text_length3 = draw.textlength(stat3, font)

    largest_text_length = max(text_length1, text_length2, text_length3)

    x0 = 0
    y0 = 140
    x1 = largest_text_length + 30
    y1 = 855

    IMG_Name_Rec = ImageDraw.Draw(img)
    IMG_Name_Rec.rounded_rectangle([(x0, y0), (x1, y1)], radius=15, fill=(0, 0, 0, 100), outline=None, width=1, corners=None)


    x = 12
    y = 150


    IMG_stat1 = ImageDraw.Draw(img)
    IMG_stat1.text((x, y), f"{stat1}", fill=(R_value, G_value, B_value, 255), font=font)



    x = 12
    y = 425

    IMG_stat2 = ImageDraw.Draw(img)
    IMG_stat2.text((x, y), f"{stat2}", fill=(R_value, G_value, B_value, 255), font=font)



    x = 12
    y = 700

    IMG_stat3 = ImageDraw.Draw(img)
    IMG_stat3.text((x,y), f"{stat3}", fill=(R_value, G_value, B_value, 255), font=font)


    img.save("stats.png")

    #========================= FINAL IMAGE ==========================


    if background_choice == "Enchanted Warped Forest":
        background_choice = "1"
    elif background_choice == "Bloody Crimson":
        background_choice = "2"
    elif background_choice == "Mooshroom Isles":
        background_choice = "3"
    elif background_choice == "Grand Canyon":
        background_choice = "4"
    elif background_choice == "Distant Horizons":
        background_choice = "5"
    elif background_choice == "Dappled Hills":
        background_choice = "6"
    elif background_choice == "Mountain's Peak":
        background_choice = "7"
    elif background_choice == "Cherry Mountains":
        background_choice = "8"
    elif background_choice == "Skeleton Meadows":
        background_choice = "9"
    elif background_choice == "Pale Highlands":
        background_choice = "10"
    

    
    background_choice = background_choice + ".png"

    background = Image.open(background_choice)

    overlay = Image.open("stats.png")

    background.paste(overlay, (0, 0), overlay)

    background.save("player card.png")
    print("Player card generated successfully as 'player card.png'.")

        



