import requests
pose = 0
pose = int(input("What kind of pose do you want?: \n 1. Default \n 2. Marching \n 3. Walking \n 4. Crouching \n 5. Crossed \n 6. Criss Cross \n 7. Ultimate \n 8. Isometric \n 9. Head \n 10. Cheering \n 11. Relaxing \n 12. Trudging \n 13. Cowering \n 14. Pointing \n 15. Lunging \n 16. Dungeons \n 17. Facepalm \n 18. Sleeping \n 19. Dead \n 20. Archer \n 21. Kicking \n 22. Mojavatar \n 23. Reading \n 24. High Ground \n 25. Clown \n 26. Bitzel \n 27 Pixel \n 28. Ornament \n 29. Profile \n"))
while pose < 1 or pose > 29:
    print("Invalid input. Please enter a number between 1 and 29.")
    pose = int(input("What kind of pose do you want?: \n 1. Default \n 2. Marching \n 3. Walking \n 4. Crouching \n 5. Crossed \n 6. Criss Cross \n 7. Ultimate \n 8. Isometric \n 9. Head \n 10. Cheering \n 11. Relaxing \n 12. Trudging \n 13. Cowering \n 14. Pointing \n 15. Lunging \n 16. Dungeons \n 17. Facepalm \n 18. Sleeping \n 19. Dead \n 20. Archer \n 21. Kicking \n 22. Mojavatar \n 23. Reading \n 24. High Ground \n 25. Clown \n 26. Bitzel \n 27 Pixel \n 28. Ornament \n 29. Profile \n"))

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

url = f"https://starlight.lunareclipse.studio/api/v1/render/{pose}/Bloody_daemonIV/full"
response = requests.get(url)
if response.status_code == 200:
    with open("player_skin.png", "wb") as f:
        f.write(response.content)
        print("Player skin downloaded successfully.")
        print(url)
else:
    print(f"Failed to download player skin. Status code: {response.status_code}")
    print(url)