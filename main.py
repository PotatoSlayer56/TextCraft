import json
import random
import math

inventory = {
    "axe": "wood",
    "pickaxe": "wood",
    "forge": "none",
    "wood": 0,
    "stone": 0,
    "coal": 0,
    "ironOre": 0,
    "ironIngot": 0
}

affirmitiveResponses = ["yes", "y"]
saveResponses = ["save", "s"]
loadResponses = ["load", "l"]
mineResponses = ["mine", "m"]
chopResponses = ["chop", "c"]
craftResponses = ["craft", "cr"]
inventoryResponses = ["inventory", "i"]
forgeResponses = ["forge", "f"]
oneResponses = ["one", "1"]
maxResponses = ["maximum", "max"]

def _Load():
    global inventory
    try:
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        print("Inventory loaded!")
    except(FileNotFoundError):
        print("Error loading stats.json")

def _Save():
    global inventory
    json_object = json.dumps(inventory, indent=4)
    with open("inventory.json", "w") as f:
        f.write(json_object)
    print("Inventory saved!")

def _Help():
    print("'save': saves progress")
    print("'load': loads progress")
    print("'help': shows this text")
    print("'mine': mines some blocks")
    print("'chop': chops some blocks")
    print("'craft': craft new item")

def _Mine():
    global inventory
    match inventory["pickaxe"]:
        case "wood":
            stone = random.randint(1,3)
            inventory["stone"] += stone
            print(f"You got {stone} stone!\nYou now have {inventory["stone"]} stone")
        case "stone":
            stone = random.randint(2,4)
            coal = random.randint(1,2)
            ironOre = random.randint(0,1)
            inventory["stone"] += stone
            inventory["coal"] += coal
            inventory["ironOre"] += ironOre
            if ironOre != 0:
                print(f"You got {stone} stone, {coal} coal and {ironOre} iron ore!\nYou now have {inventory["stone"]} stone, {inventory["coal"]} coal and {inventory["ironOre"]} iron ore")
            else:
                print(f"You got {stone} stone and {coal} coal!\nYou now have {inventory["stone"]} stone and {inventory["coal"]} coal")
        case "iron":
            stone = random.randint(3,5)
            coal = random.randint(1,2)
            ironOre = random.randint(1,2)
            inventory["stone"] += stone
            inventory["coal"] += coal
            inventory["ironOre"] += ironOre
            print(f"You got {stone} stone, {coal} coal and {ironOre} iron ore!\nYou now have {inventory["stone"]} stone, {inventory["coal"]} coal and {inventory["ironOre"]} iron ore")

def _Chop():
    global inventory
    match inventory["axe"]:
        case "wood":
            wood = random.randint(1,3)
            inventory["wood"] += wood
            print(f"You got {wood} wood!\nYou now have {inventory["wood"]} wood")
        case "stone":
            wood = random.randint(2,4)
            inventory["wood"] += wood
            print(f"You got {wood} wood!\nYou now have {inventory["wood"]} wood")

def _Craft():
    global inventory
    avaliableCrafts = []
    avaliableCraftsText = ""
    if inventory["axe"] == "wood" and inventory["wood"] >= 10 and inventory["stone"] >= 15:
        avaliableCrafts.append("Stone Axe")
    if inventory["pickaxe"] == "wood" and inventory["wood"] >= 10 and inventory["stone"] >= 15:
        avaliableCrafts.append("Stone Pickaxe")
    if inventory["forge"] == "none" and inventory["wood"] >= 25 and inventory["stone"] >= 50:
        avaliableCrafts.append("Stone Forge")
    match inventory["forge"]:
        case "stone":
            if inventory["axe"] == "stone" and inventory["wood"] >= 25 and inventory["ironIngot"] >= 15:
                avaliableCrafts.append("Iron Axe")
            if inventory["pickaxe"] == "stone" and inventory["wood"] >= 25 and inventory["ironIngot"] >= 15:
                avaliableCrafts.append("Iron Pickaxe")
            if inventory["forge"] == "stone" and inventory["ironIngot"] >= 35:
                avaliableCrafts.append("Iron Forge")
    for avaliableCraft in avaliableCrafts:
        avaliableCraftsText += avaliableCraft
        avaliableCraftsText += ", "
    print(f"Avaliable Crafts: {avaliableCraftsText}")
    craftInput = input("What would you like to craft? ")
    if craftInput in avaliableCrafts:
        match craftInput:
            case "Stone Axe":
                craftInput = input("Would you like to craft a Stone Axe for 10 wood and 15 stone? ")
                if craftInput.lower() in affirmitiveResponses:
                    inventory["wood"] -= 10
                    inventory["stone"] -= 15
                    inventory["axe"] = "stone"
                    print("You crafted a Stone Axe!")
            case "Stone Pickaxe":
                craftInput = input("Would you like to craft a Stone Pickaxe for 10 wood and 15 stone? ")
                if craftInput.lower() in affirmitiveResponses:
                    inventory["wood"] -= 10
                    inventory["stone"] -= 15
                    inventory["pickaxe"] = "stone"
                    print("You crafted a Stone Pickaxe!")
            case "Stone Forge":
                craftInput = input("Would you like to craft a Stone Forge for 25 wood and 50 stone? ")
                if craftInput.lower() in affirmitiveResponses:
                    inventory["wood"] -= 25
                    inventory["stone"] -= 50
                    inventory["forge"] = "stone"
                    print("You crafted a Stone Forge!")
            case "Iron Axe":
                craftInput = input("Would you like to craft an Iron Axe for 25 wood and 15 iron ingots? ")

def _Forge():
    global inventory
    avaliableForges = []
    avaliableForgesText = ""
    if inventory["forge"] == "stone":
        if inventory["ironOre"] >= 3 and inventory["coal"] >= 1:
            avaliableForges.append("Iron Ingot")
    for avaliableForge in avaliableForges:
        avaliableForgesText += avaliableForge
        avaliableForgesText += ", "
    print(f"Avaliable Forges: {avaliableForgesText}")
    forgeInput = input("What would you like to forge? ")
    if forgeInput in avaliableForges:
        match forgeInput:
            case "Iron Ingot":
                craftInput = input("Would you like to forge 1 ingot or maximum ingots? ")
                if craftInput.lower() in oneResponses:
                    inventory["coal"] -= 1
                    inventory["ironOre"] -= 3
                    inventory["ironIngot"] += 1
                    print("You forged 1 Iron Ingot")
                elif craftInput.lower() in maxResponses:
                    possibleIronIngots = math.floor(inventory["ironOre"] / 3)
                    if inventory["coal"] >= possibleIronIngots:
                        craftInput = input(f"Would you like to forge {possibleIronIngots} iron ingots? ")
                        if craftInput.lower() in affirmitiveResponses:
                            inventory["ironOre"] -= possibleIronIngots * 3
                            inventory["coal"] -= possibleIronIngots
                            inventory["ironIngot"] += possibleIronIngots
                            print(f"You forged {possibleIronIngots} iron ingots!")

def _Inventory():
    global inventory
    print(f"\nTools:\nPickaxe: {inventory["pickaxe"]}\nAxe: {inventory["axe"]}\nForge: {inventory["forge"]}\n")
    print(f"Resources:\nWood: {inventory["wood"]}\nStone: {inventory["stone"]}\nCoal: {inventory["coal"]}\nIron Ore: {inventory["ironOre"]}\nIron Ingots: {inventory["ironIngot"]}\n")

print("Textcraft\nBy PotatoSlayer56")
print("Remember to save/load your progress when you start or finish")
print("Type 'help' for a list of commands!")

while True:
    x = input("Action: ")
    if x in saveResponses:
        _Save()
    elif x in loadResponses:
        _Load()
    elif x == "help":
        _Help()
    elif x in mineResponses:
        _Mine()
    elif x in chopResponses:
        _Chop()
    elif x in craftResponses:
        _Craft()
    elif x in inventoryResponses:
        _Inventory()
    elif x in forgeResponses:
        _Forge()