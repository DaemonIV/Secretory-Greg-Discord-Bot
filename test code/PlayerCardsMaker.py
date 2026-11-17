import csv
import requests
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import os


img = Image.open('blank.png')
#put image last
draw = ImageDraw.Draw(img)

# ========================== USERNAME AND USER INPUTS ==========================


user_input_font = 0
user_input_colour = ""
user_input_font_size = 99
user_input_username = ""

player_list_uuid = []
player_list_name = []
csv_data = pd.read_csv('playerlist.csv')
player_list_uuid = csv_data['UUID'].tolist()

a = len(player_list_uuid)
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



    
    

user_input_username = input("Enter your username: ")
player_name_case_sens = user_input_username
while user_input_username.lower() not in [name.lower() for name in player_list_name]:
    print("Username not found in the player list. Please enter a valid username.")
    user_input_username = input("Enter your username: ")
    player_name_case_sens = user_input_username
    user_input_username = user_input_username.lower()


player_list_name.reverse()
player_uuid = player_list_uuid[player_list_name.index(user_input_username.lower()) - 1]

pose = 0
pose = int(input("What kind of pose do you want?: \n 1. Default \n 2. Marching \n 3. Walking \n 4. Crouching \n 5. Crossed \n 6. Criss Cross \n 7. Ultimate \n 8. Isometric \n 9. Head \n 10. Cheering \n 11. Relaxing \n 12. Trudging \n 13. Cowering \n 14. Pointing \n 15. Lunging \n 16. Dungeons \n 17. Facepalm \n 18. Sleeping \n 19. Dead \n 20. Archer \n 21. Kicking \n 22. Mojavatar \n 23. Reading \n 24. High Ground \n 25. Clown \n 26. Bitzel \n 27. Pixel \n 28. Ornament \n 29. Profile \n"))
while pose < 1 or pose > 29:
    print("Invalid input. Please enter a number between 1 and 29.")
    pose = int(input("What kind of pose do you want?: \n 1. Default \n 2. Marching \n 3. Walking \n 4. Crouching \n 5. Crossed \n 6. Criss Cross \n 7. Ultimate \n 8. Isometric \n 9. Head \n 10. Cheering \n 11. Relaxing \n 12. Trudging \n 13. Cowering \n 14. Pointing \n 15. Lunging \n 16. Dungeons \n 17. Facepalm \n 18. Sleeping \n 19. Dead \n 20. Archer \n 21. Kicking \n 22. Mojavatar \n 23. Reading \n 24. High Ground \n 25. Clown \n 26. Bitzel \n 27. Pixel \n 28. Ornament \n 29. Profile \n"))

if pose == 1:
    pose = "default"
elif pose == 2: 
    pose = "marching"
elif pose == 3:
    pose = "walking"
elif pose == 4:
    pose = "crouching"
elif pose == 5:
    pose = "crossed"    
elif pose == 6:
    pose = "criss_cross"
elif pose == 7:
    pose = "ultimate"
elif pose == 8:
    pose = "isometric"
elif pose == 9:
    pose = "head"
elif pose == 10:
    pose = "cheering"
elif pose == 11:
    pose = "relaxing"
elif pose == 12:
    pose = "trudging"
elif pose == 13:
    pose = "cowering"
elif pose == 14:
    pose = "pointing"
elif pose == 15:
    pose = "lunging"
elif pose == 16:
    pose = "dungeons"
elif pose == 17: 
    pose = "facepalm"
elif pose == 18:
    pose = "sleeping"
elif pose == 19:
    pose = "dead"
elif pose == 20:
    pose = "archer"
elif pose == 21:
    pose = "kicking"
elif pose == 22:
    pose = "mojavatar"
elif pose == 23:
    pose = "reading"
elif pose == 24:
    pose = "high_ground"
elif pose == 25:
    pose = "clown"
elif pose == 26:
    pose = "bitzel"
elif pose == 27:
    pose = "pixel"
elif pose == 28:
    pose = "ornament"
elif pose == 29:
    pose = "profile"

url = f"https://starlight.lunareclipse.studio/api/v1/render/{pose}/{player_uuid}/full"
response = requests.get(url)
if response.status_code == 200:
    with open("player_skin.png", "wb") as f:
        f.write(response.content)
        print("Player skin downloaded successfully.")
else:
    print(f"Failed to download player skin. Status code: {response.status_code}")
    

for row_idx, row in enumerate(csv_data.itertuples(index=False), start=1):
    if player_uuid == row.UUID:
        player_row = row
        break


while user_input_font not in [1, 2, 3]:
    try:
        user_input_font = int(input("Enter what font you wish: \n1. Minecraft \n2. Minecraft bold \n3. Trashhand (Official life series font) \n"))
        if user_input_font not in [1, 2, 3]:
            print("Invalid input. Please enter a number between 1 and 3.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
while user_input_font_size < 100 or user_input_font_size > 255:
    try:
        user_input_font_size = int(input("Enter the font size you wish (100-255): "))
        if user_input_font_size < 100 or user_input_font_size > 255:
            print("Invalid input. Please enter a number between 100 and 255.")
    except ValueError:
        print("Invalid input. Please enter a number between 100 and 255.")

if user_input_font == 1:
    font = ImageFont.truetype("Minecraft.otf", user_input_font_size)
elif user_input_font == 2:
    font = ImageFont.truetype("MinecraftBold.otf", user_input_font_size)
elif user_input_font == 3:
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
    1: 0, #'Final_Kills',
    2: 1, #'Kills',
    3: 2, #'Average_kills_per_season',
    4: 3, #'Worst_placement',
    5: 4, #'Best_placement',
    6: 5, #'Average_placement',
    7: 6, #'Chaos_Life_placement',
    8: 7, #'Chaos_Life2_placement' 
}

menu_text = (
    "Select a statistic: \n"
    "1. Final kills \n2. Kills \n3. Average kills per season \n"
    "4. Worst placement \n5. Best placement \n6. Average placement \n"
    "7. Chaos Life placement \n8. Chaos Life^2 placement \n"
)

statselection = []
for i in range(1, 4):
    while True:
        try:
            choice = int(input(f"Enter your stat #{i} choice:\n" + menu_text))
            if choice in (stat_mapping):
                statselection.append(choice)
                stat_value = player_row[stat_mapping[choice]]
                globals()[f"stat{i}"] = stat_value
                break
            else:
                print("Please pick a number from 1 to 8.")
        except ValueError:
            print("Please enter a valid integer number.")

#print(player_row)



#print(f"Stat 1: {stat1}")
#print(f"Stat 2: {stat2}")
#print(f"Stat 3: {stat3}")

if statselection[0] == 1:
    stat1 = "Final kills: " + str(stat1)
elif statselection[0] == 2:
    stat1 = "Kills: " + str(stat1)
elif statselection[0] == 3:
    stat1 = "Avg kills: " + str(stat1)
elif statselection[0] == 4:
    stat1 = "Worst placement: " + str(stat1)
elif statselection[0] == 5:
    stat1 = "Best placement: " + str(stat1)
elif statselection[0] == 6:
    stat1 = "Avg placement: " + str(stat1)
elif statselection[0] == 7:
    stat1 = "CHL placement: " + str(stat1)
elif statselection[0] == 8:
    stat1 = "CHL^2 placement: " + str(stat1)

if statselection[1] == 1:
    stat2 = "Final kills: " + str(stat2)
elif statselection[1] == 2:
    stat2 = "Kills: " + str(stat2)
elif statselection[1] == 3:
    stat2 = "Avg kills: " + str(stat2)
elif statselection[1] == 4:
    stat2 = "Worst placement: " + str(stat2)
elif statselection[1] == 5:
    stat2 = "Best placement: " + str(stat2)
elif statselection[1] == 6:
    stat2 = "Avg placement: " + str(stat2)
elif statselection[1] == 7:
    stat2 = "CHL placement: " + str(stat2)
elif statselection[1] == 8:
    stat2 = "CHL^2 placement: " + str(stat2)

if statselection[2] == 1:
    stat3 = "Final kills: " + str(stat3)
elif statselection[2] == 2:
    stat3 = "Kills: " + str(stat3)
elif statselection[2] == 3:
    stat3 = "Avg kills: " + str(stat3)
elif statselection[2] == 4:
    stat3 = "Worst placement: " + str(stat3)
elif statselection[2] == 5:
    stat3 = "Best placement: " + str(stat3)
elif statselection[2] == 6:
    stat3 = "Avg placement: " + str(stat3)
elif statselection[2] == 7:
    stat3 = "CHL placement: " + str(stat3)
elif statselection[2] == 8:
    stat3 = "CHL^2 placement: " + str(stat3)

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
user_input_background = input("Enter the background you wish: \n1. Basalt Delta ")
background = Image.open("background.png")

overlay = Image.open("stats.png")

background.paste(overlay, (0, 0), overlay)

background.save("player card.png")
background.show()


