import os
import json
from requests import get
from openpyxl import load_workbook

def testImg(string):
    if string == "":
        return None

def testReward(input):
    if input is None:
        return None
    return input.strip()

def testMod(input):
    if input is None:
        return None
    return input.strip()

def processMultiValue(input):
    rvalues = input.split(",")
    values = {
        "hp": int(rvalues[0]),
        "rr": int(rvalues[1]),
        "atk": int(rvalues[2]),
        "souls": int(rvalues[3])
    }
    return values

def processEnemies(sheet, data):
    row = 2
    Enemies = {}
    while True:
        enemyName = sheet["A" + str(row)].value
        if enemyName is not None:
            Enemies[row-1] = {
                "name": enemyName,
                "desc": sheet["E" + str(row)].value,
                "hp": int(sheet["B" + str(row)].value),
                "rr": int(sheet["C" + str(row)].value),
                "atk": int(sheet["D" + str(row)].value),
                "reward": testReward(sheet["F" + str(row)].value),
                "souls": int(sheet["G" + str(row)].value),
                "img": testImg(sheet["H" + str(row)].value)
            }
        else:
            break
        row += 1
    Enemies["_size"] = len(Enemies)
    data["Enemies"] = Enemies
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
                "hp": values["hp"],
                "rr": values["rr"],
                "atk": values["atk"],
                "souls": values["souls"]
            }
        else:
            break
        row += 1
    Prefixes["_size"] = len(Prefixes)
    data["Prefixes"] = Prefixes
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
                "hp": values["hp"],
                "rr": values["rr"],
                "atk": values["atk"],
                "souls": values["souls"]
            }
        else:
            break
        row += 1
    Suffixes["_size"] = len(Suffixes)
    data["Suffixes"] = Suffixes
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
    return data

def processRelics(sheet, data):
    row = 2
    Relics = {}
    while True:
        relicName = sheet["A" + str(row)].value
        if relicName is not None:
            # create a tuple of columns containing the letters D through M
            columns = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
            prefixes = {}
            columnStep = 0
            while True:
                prefixName = sheet[columns[columnStep] + str(row)].value
                if prefixName is not None or columnStep == 0:
                    if prefixName is None:
                        prefixName = ""
                    prefixes[columnStep+1] = {
                        "name": prefixName,
                        "desc": sheet[columns[columnStep + 1] + str(row)].value
                        }
                    if columns[columnStep] == "L":
                        break
                else:
                    break
                columnStep += 2
            prefixes["_size"] = len(prefixes)

            Relics[row-1] = {
                "name": relicName,
                "type": sheet["B" + str(row)].value,
                "img": testImg(sheet["C" + str(row)].value),
                "prefixes": prefixes
            }
        else:
            break
        row += 1
    Relics["_size"] = len(Relics)
    data["Relics"] = Relics
    return data

# Affinities are the same as relics, but with a different name

def processAffinities(sheet, data):
    row = 2
    Affinities = {}
    while True:
        affinityName = sheet["A" + str(row)].value
        if affinityName is not None:
            # create a tuple of columns containing the letters D through M
            columns = ["D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
            prefixes = {}
            columnStep = 0
            while True:
                prefixName = sheet[columns[columnStep] + str(row)].value
                if prefixName is not None or columnStep == 0:
                    if prefixName is None:
                        prefixName = ""
                    prefixes[columnStep+1] = {
                        "name": prefixName,
                        "desc": sheet[columns[columnStep + 1] + str(row)].value
                        }
                    if columns[columnStep] == "L":
                        break
                else:
                    break
                columnStep += 2
            prefixes["_size"] = len(prefixes)

            Affinities[row-1] = {
                "name": affinityName,
                "type": sheet["B" + str(row)].value,
                "img": testImg(sheet["C" + str(row)].value),
                "prefixes": prefixes
            }
        else:
            break
        row += 1
    Affinities["_size"] = len(Affinities)
    data["Affinities"] = Affinities
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
            HPWare[wareName] = {
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
            ATKWare[wareName] = {
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
            BoneWare[wareName] = {
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

    data = processEnemies(wb["Enemies"], data)
    data = processPrefixes(wb["Enemies"], data)
    data = processSuffixes(wb["Enemies"], data)
    data = processJinxes(wb["Enemies"], data)
    data = processStages(wb["Enemies"], data)
    data = processSouls(wb["Enemies"], data)
    data = processRelics(wb["Relics"], data)
    data = processAffinities(wb["Affinities"], data)
    data = processWares(wb["Wares"], data)
    data = processGlitched(wb["Glitched"], data)
    wb.close()

    finalJson = json.dumps(data, indent=4)

    # print(finalJson)

    with open("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/HexSouls.json", "w") as outfile:
        outfile.write(finalJson)
        outfile.close()

    os.remove("C:/Users/iamtr/Desktop/Git Content/Four Souls/CustomFourSouls/Spreadsheat Formatter/temp.xlsx")

main()