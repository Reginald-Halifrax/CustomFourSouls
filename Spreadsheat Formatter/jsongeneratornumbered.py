import os
import json
from requests import get
from openpyxl import load_workbook

def testImg(string):
    if string == "":
        return None
    return string

def testReward(input):
    if input is None:
        return None
    return input.strip()

def testMod(input):
    if input is None:
        return None
    return input.strip()

def processMultiValue(input):
    if input is None:
        return None
    rvalues = input.split(",")
    values = {
        "hp": int(rvalues[0]),
        "rr": int(rvalues[1]),
        "atk": int(rvalues[2]),
        "souls": int(rvalues[3])
    }
    return values

def processEnemies(sheet, data, type, columnstart):
    row = 2
    Enemies = {}
    while True:
        enemyName = sheet[chr(columnstart) + str(row)].value
        if enemyName is not None:
            Enemies[row-1] = {
                "name": enemyName,
                "desc": sheet[chr(columnstart+4) + str(row)].value
            }
            hp = sheet[chr(columnstart+1) + str(row)].value
            rr = sheet[chr(columnstart+2) + str(row)].value
            atk = sheet[chr(columnstart+3) + str(row)].value
            souls = sheet[chr(columnstart+6) + str(row)].value
            reward = testReward(sheet[chr(columnstart+5) + str(row)].value)
            img = testImg(sheet[chr(columnstart+7) + str(row)].value)
            if reward is not None:
                Enemies[row-1]["reward"] = reward
            if hp is not None and hp != 0:
                Enemies[row-1]["hp"] = int(hp)
            if rr is not None and rr != 0:
                Enemies[row-1]["rr"] = int(rr)
            if atk is not None and atk != 0:
                Enemies[row-1]["atk"] = int(atk)
            if souls is not None and souls != 0:
                Enemies[row-1]["souls"] = int(souls)
            if img is not None:
                Enemies[row-1]["img"] = img
        else:
            break
        row += 1
    Enemies["_size"] = len(Enemies)
    data[type] = Enemies
    print("Successfully processed " + type)
    return data

def processPrefixes(sheet, data):
    row = 2
    Prefixes = {}
    while True:
        prefixName = sheet["I" + str(row)].value
        if prefixName is not None:
            values = processMultiValue(sheet["K" + str(row)].value)
            Prefixes[row-1] = {
                "name": prefixName,
                "mod": testMod(sheet["J" + str(row)].value)
            }
            if values is not None:
                if values["hp"] != 0:
                    Prefixes[row-1]["hp"] = values["hp"]
                if values["rr"] != 0:
                    Prefixes[row-1]["rr"] = values["rr"]
                if values["atk"] != 0:
                    Prefixes[row-1]["atk"] = values["atk"]
                if values["souls"] != 0:
                    Prefixes[row-1]["souls"] = values["souls"]
        else:
            break
        row += 1
    Prefixes["_size"] = len(Prefixes)
    data["Prefixes"] = Prefixes
    print("Successfully processed Prefixes")
    return data

def processSuffixes(sheet, data):
    row = 2
    Suffixes = {}
    while True:
        suffixName = sheet["L" + str(row)].value
        if suffixName is not None:
            values = processMultiValue(sheet["N" + str(row)].value)
            Suffixes[row-1] = {
                "name": suffixName,
                "mod": testMod(sheet["M" + str(row)].value)
            }
            if values is not None:
                if values["hp"] != 0:
                    Suffixes[row-1]["hp"] = values["hp"]
                if values["rr"] != 0:
                    Suffixes[row-1]["rr"] = values["rr"]
                if values["atk"] != 0:
                    Suffixes[row-1]["atk"] = values["atk"]
                if values["souls"] != 0:
                    Suffixes[row-1]["souls"] = values["souls"]
        else:
            break
        row += 1
    Suffixes["_size"] = len(Suffixes)
    data["Suffixes"] = Suffixes
    print("Successfully processed Suffixes")
    return data

def processJinxes(sheet, data):
    row = 2
    Jinxes = {}
    while True:
        jinxName = sheet["O" + str(row)].value
        if jinxName is not None:
            Jinxes[row-1] = {
                "name": jinxName,
                "desc": sheet["P" + str(row)].value,
                "img": testImg(sheet["Q" + str(row)].value)
            }
        else:
            break
        row += 1
    Jinxes["_size"] = len(Jinxes)
    data["Jinxes"] = Jinxes
    print("Successfully processed Jinxes")
    return data

def processStages(sheet, data):
    row = 2
    Stages = {}
    while True:
        stageName = sheet["R" + str(row)].value
        if stageName is not None:
            Stages[row-1] = {
                "name": stageName,
                "desc": sheet["S" + str(row)].value,
                "img": testImg(sheet["T" + str(row)].value)
            }
        else:
            break
        row += 1
    Stages["_size"] = len(Stages)
    data["Stages"] = Stages
    print("Successfully processed Stages")
    return data

def processSouls(sheet, data):
    row = 2
    Souls = {}
    while True:
        soulName = sheet["U" + str(row)].value
        if soulName is not None:
            Souls[row-1] = {
                "name": soulName,
                "desc": sheet["V" + str(row)].value,
                "img": testImg(sheet["W" + str(row)].value)
            }
        else:
            break
        row += 1
    Souls["_size"] = len(Souls)
    data["Souls"] = Souls
    print("Successfully processed Souls")
    return data

# Affinities are the same as relics, but with a different name

def processItems(sheet, data, type):
    row = 2
    Items = {}
    while True:
        itemName = sheet["A" + str(row)].value
        if itemName is not None:
            prefixes = {}
            columnStep = 68
            trueCount = 1
            while True:
                prefixName = sheet[chr(columnStep) + str(row)].value
                if prefixName is not None or columnStep == 68:
                    if prefixName is None:
                        prefixName = ""
                    prefixes[trueCount] = {
                        "name": prefixName,
                        "desc": sheet[chr(columnStep+1) + str(row)].value
                        }
                else:
                    break
                columnStep += 2
                trueCount += 1
            prefixes["_size"] = len(prefixes)

            Items[row-1] = {
                "name": itemName,
                "type": sheet["B" + str(row)].value,
                "img": testImg(sheet["C" + str(row)].value),
                "prefixes": prefixes
            }
        else:
            break
        row += 1
    Items["_size"] = len(Items)
    data[type] = Items
    print("Successfully processed "+type)
    return data

# Wares are set up in three categories, HPWare, ATKWare, and BoneWare. They are to be stored in one large table called "Wares".
def processWares(sheet, data):
    Wares = {}
    HPWare = {}
    ATKWare = {}
    BoneWare = {}
    row = 2
    while True:
        wareName = sheet["A" + str(row)].value
        if wareName is not None:
            HPWare[str(row-1)] = {
                "name": wareName,
                "desc": sheet["B" + str(row)].value,
                "img": testImg(sheet["C" + str(row)].value)
            }
        else:
            break
        row += 1
    row = 2
    while True:
        wareName = sheet["D" + str(row)].value
        if wareName is not None:
            ATKWare[str(row-1)] = {
                "name": wareName,
                "desc": sheet["E" + str(row)].value,
                "img": testImg(sheet["F" + str(row)].value)
            }
        else:
            break
        row += 1
    row = 2
    while True:
        wareName = sheet["G" + str(row)].value
        if wareName is not None:
            BoneWare[str(row-1)] = {
                "name": wareName,
                "desc": sheet["H" + str(row)].value,
                "img": testImg(sheet["I" + str(row)].value)
            }
        else:
            break
        row += 1
    HPWare["_size"] = len(HPWare)
    ATKWare["_size"] = len(ATKWare)
    BoneWare["_size"] = len(BoneWare)
    Wares = {
        "HpWares": HPWare,
        "AtkWares": ATKWare,
        "BoneWares": BoneWare
    }
    data["Wares"] = Wares
    print("Successfully processed Wares")
    return data

# Store 4 tables in one dictionary called Trigger, PlayerMutator, EnemyMutator, and Effector.
def processGlitched(sheet, data):
    Trigger = []
    PlayerMutator = []
    EnemyMutator = []
    Effector = []
    row = 2
    while True:
        triggerValue = sheet["A" + str(row)].value
        if triggerValue is not None:
            Trigger.append(triggerValue)
        PlayerMutatorValue = sheet["B" + str(row)].value
        if PlayerMutatorValue is not None:
            PlayerMutator.append(PlayerMutatorValue)
        EnemyMutatorValue = sheet["C" + str(row)].value
        if EnemyMutatorValue is not None:
            EnemyMutator.append(EnemyMutatorValue)
        EffectorValue = sheet["D" + str(row)].value
        if EffectorValue is not None:
            Effector.append(EffectorValue)
        
        if triggerValue is None and PlayerMutatorValue is None and EnemyMutatorValue is None and EffectorValue is None:
            break
        row += 1
    Glitched = {
        "Trigger": Trigger,
        "PlayerMutator": PlayerMutator,
        "EnemyMutator": EnemyMutator,
        "Effector": Effector
    }
    data["Glitched"] = Glitched
    return data

def main():
    data = {}
    Hexsouls = get("https://docs.google.com/spreadsheets/d/1FkBVhP4NlVBvbxMKVMCMk1cs39O_Y-z4KKQyoP6cwBQ/export?format=xlsx&id=1FkBVhP4NlVBvbxMKVMCMk1cs39O_Y-z4KKQyoP6cwBQ")

    HexSheets = open("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/temp.xlsx", "wb")
    HexSheets.write(Hexsouls.content)
    HexSheets.close()

    # load the workbook using the Hexsouls.content
    wb = load_workbook(filename="C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/temp.xlsx", read_only=True)

    data = processEnemies(wb["Enemies"], data, "Enemies", 65)
    data = processPrefixes(wb["Enemies"], data)
    data = processSuffixes(wb["Enemies"], data)
    data = processJinxes(wb["Enemies"], data)
    data = processStages(wb["Enemies"], data)
    data = processSouls(wb["Enemies"], data)
    data = processItems(wb["Relics"], data, "Relics")
    data = processItems(wb["Affinities"], data, "Affinities")
    data = processWares(wb["Wares"], data)
    data = processGlitched(wb["Glitched"], data)

    data["DLC"] = {}
    dlcEnem = {}
    dlcEnem = processEnemies(wb["Enemies_DLC"], dlcEnem, "Demon", 65)
    dlcEnem = processEnemies(wb["Enemies_DLC"], dlcEnem, "Lunar", 73)
    dlcEnem = processEnemies(wb["Enemies_DLC"], dlcEnem, "Angelic", 81)

    data["DLC"]["Enemies"] = dlcEnem

    dlcRelics = {}
    dlcRelics = processItems(wb["Relics_DLC1"], dlcRelics, "Demonic")
    dlcRelics = processItems(wb["Relics_DLC2"], dlcRelics, "Lunar")
    dlcRelics = processItems(wb["Relics_DLC3"], dlcRelics, "Angelic")

    data["DLC"]["Relics"] = dlcRelics
    wb.close()

    finalJson = json.dumps(data, indent=4)

    # print(finalJson)

    with open("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/HexSouls.json", "w") as outfile:
        outfile.write(finalJson)
        outfile.close()

    os.remove("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/temp.xlsx")

main()

#print(chr(68))