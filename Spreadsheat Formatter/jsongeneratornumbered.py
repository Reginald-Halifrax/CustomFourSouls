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
                "desc": sheet[chr(columnstart+4) + str(row)].value,
                "reward": testReward(sheet[chr(columnstart+5) + str(row)].value),
                "hp": int(sheet[chr(columnstart+1) + str(row)].value) or None,
                "rr": int(sheet[chr(columnstart+2) + str(row)].value) or None,
                "atk": int(sheet[chr(columnstart+3) + str(row)].value) or None,
                "souls": int(sheet[chr(columnstart+6) + str(row)].value) or None,
                "img": testImg(sheet[chr(columnstart+7) + str(row)].value)
            }
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
                "mod": testMod(sheet["J" + str(row)].value),
                "hp": values["hp"] or None,
                "rr": values["rr"] or None,
                "atk": values["atk"] or None,
                "souls": values["souls"] or None,
            }
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
                "mod": testMod(sheet["M" + str(row)].value),
                "hp": values["hp"] or None,
                "rr": values["rr"] or None,
                "atk": values["atk"] or None,
                "souls": values["souls"] or None,
            }
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
                "img": testImg(sheet["Q" + str(row)].value),
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
                "img": testImg(sheet["T" + str(row)].value),
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
                "img": testImg(sheet["W" + str(row)].value),
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
                "prefixes": prefixes,
                "img": testImg(sheet["C" + str(row)].value),
            }
        else:
            break
        row += 1
    Items["_size"] = len(Items)
    data[type] = Items
    print("Successfully processed "+type)
    return data

# Wares are pulled from 4 sets of 3 column tables. These must be compiled all into one dictionary called "Wares" and then we must track the number of entries in each table.
def processWares(sheet, data):
    Wares = {}
    AtkWareStart = 0
    BoneWareStart = 0
    UniqueWareStart = 0
    WareNum = 1
    for k in [65, 68, 71, 74]:
        row = 2
        while True:
            wareName = sheet[chr(k) + str(row)].value
            if wareName is not None:
                Wares[WareNum] = {
                    "name": wareName,
                    "desc": sheet[chr(k+1) + str(row)].value,
                    "img": testImg(sheet[chr(k+2) + str(row)].value),
                }
            else:
                break
            row += 1
            WareNum += 1
        if k == 65:
            AtkWareStart = len(Wares)
        elif k == 68:
            BoneWareStart = len(Wares)
        elif k == 71:
            UniqueWareStart = len(Wares)
    
    Wares["_AtkWareStart"] = AtkWareStart
    Wares["_BoneWareStart"] = BoneWareStart
    Wares["_UniqueWareStart"] = UniqueWareStart
    Wares["_size"] = len(Wares)
    data["Wares"] = Wares
    print("Successfully processed Wares")
    return data

# Stores 4 tables in Glitched dictionary called Trigger, PlayerMutator, EnemyMutator, and Effector.
def processGlitched(sheet, data):
    Glitched = {
        "Trigger": {},
        "PlayerMutator": {},
        "EnemyMutator": {},
        "Effector": {},
    }
    for k,v in {"Trigger": 65, "PlayerMutator": 67, "EnemyMutator": 69, "Effector": 71}.items():
        row = 2
        while True:
            curGlitchDesc = sheet[chr(v) + str(row)].value
            if curGlitchDesc is not None:
                Glitched[k][str(row-1)] = {
                    "desc": curGlitchDesc,
                    "weight": sheet[chr(v+1) + str(row)].value,
                }
            else:
                break
            row += 1
    
    for k in ["Trigger", "PlayerMutator", "EnemyMutator", "Effector"]:
        Glitched[k]["_size"] = len(Glitched[k])

    data["Glitched"] = Glitched
    print("Successfully processed Glitched cards")
    return data

def clean_nones(value):
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value

def main():
    data = {}
    Hexsouls = get("https://docs.google.com/spreadsheets/d/1FkBVhP4NlVBvbxMKVMCMk1cs39O_Y-z4KKQyoP6cwBQ/export?format=xlsx&id=1FkBVhP4NlVBvbxMKVMCMk1cs39O_Y-z4KKQyoP6cwBQ")

    with open("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/temp.xlsx", "wb") as HexSheets:
        HexSheets.write(Hexsouls.content)

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

    data = clean_nones(data)

    with open("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/HexSouls.json", "w", encoding="utf8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    os.remove("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/temp.xlsx")

main()
