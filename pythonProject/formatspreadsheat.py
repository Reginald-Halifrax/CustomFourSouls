from openpyxl import load_workbook

workbook = load_workbook(filename="Hex Souls.xlsx")


def enemy_process():
    sheet = workbook["Enemies"]
    columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
    row = 2

    eof = 0

    enemies_file = open("enemies.txt", "w", encoding="utf-8")

    enemies_file.write("Enemies = {")

    while not eof:
        for k in columns:
            if k == "A":
                enemies_file.write("\n{")
            cell = sheet[k + str(row)]
            if cell.value is None:
                data = ""
            else:
                data = str(cell.value)
            if sheet["A" + str(row + 1)].value is None:
                eof = 1
            if k in "AEFH":
                data = '"' + data + '"'
            else:
                data = str(int(cell.value))
            enemies_file.write(data)
            if k != "H":
                enemies_file.write(",")
        if eof:
            enemies_file.write("}")
        else:
            enemies_file.write("},")
        row += 1

    enemies_file.write("\n}")
    enemies_file.close()


def enemy_modifier_process(filename, json, columns):
    sheet = workbook["Enemies"]
    row = 2

    eof = 0

    mod_file = open(filename, "w", encoding="utf-8")
    mod_file.write(json)

    while not eof:
        for k in columns:
            if k == columns[0]:
                mod_file.write("\n{")
            cell = sheet[k + str(row)]
            if sheet[columns[0] + str(row + 1)].value is None:
                eof = 1
            if cell.value is None:
                data = ""
            else:
                data = cell.value
            if k in columns[0] + columns[1]:
                data = '"' + data + '",'
            else:
                data = '{' + cell.value + '}'
            mod_file.write(data)
        if eof:
            mod_file.write("}")
        else:
            mod_file.write("},")
        row += 1
    mod_file.write("\n}")
    mod_file.close()


def stage_modifier(filename, json, columns):
    sheet = workbook["Enemies"]
    row = 2

    eof = 0

    mod_file = open(filename, "w", encoding="utf-8")
    mod_file.write(json)

    while not eof:
        for k in columns:
            if k == columns[0]:
                mod_file.write("\n{")
            cell = sheet[k + str(row)]
            if sheet[columns[0] + str(row + 1)].value is None:
                eof = 1
            if cell.value is None:
                data = ""
            else:
                data = cell.value
            data = '"' + data + '"'
            mod_file.write(data)
            if k in columns[0] + columns[1]:
                mod_file.write(",")
        if eof:
            mod_file.write("}")
        else:
            mod_file.write("},")
        row += 1
    mod_file.write("\n}")
    mod_file.close()


def usable_process(filename, json, sheet):
    row = 2
    columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    eof = 0

    item_file = open(filename, "w", encoding="utf-8")

    item_file.write(json)

    while not eof:
        for k in columns:
            if k == "A":
                item_file.write("\n{")
            cell = sheet[k + str(row)]
            if k == "D":
                item_file.write("{")
            if cell.value is None:
                data = '""'
            else:
                data = '"' + cell.value + '"'
            if sheet["A" + str(row + 1)].value is None:
                eof = 1
            if k not in "ABCDE" and data == '""':
                item_file.write("}")
                break
            elif k in "M":
                item_file.write("}")
            elif k not in "ABCD":
                item_file.write("," + data)
            elif k == "D":
                item_file.write(data)
            elif k in "ABC":
                item_file.write(data + ",")
        if eof:
            item_file.write("}")
        else:
            item_file.write("},")

        row += 1
    item_file.write("\n}")
    item_file.close()


def ware_process():
    sheet = workbook["Wares"]

    ware_file = open("wares.txt", "w", encoding="utf-8")
    ware_file.write("Wares = {\n")

    for columns in [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]:
        row = 2
        eof = 0
        while not eof:
            ware_file.write("{")
            for k in columns:
                cell = sheet[k + str(row)]
                data = '"' + cell.value + '"'
                ware_file.write(data)
                if k not in "CFI":
                    ware_file.write(",")
            if sheet[columns[0] + str(row + 1)].value is None:
                eof = 1
            row += 1
            ware_file.write("}")
            if columns[0] in "AD" or not eof:
                ware_file.write(",\n")
    ware_file.write("\n}")
    ware_file.close()


def glitched_process():
    sheet = workbook["Glitched"]

    glitch_file = open("glitched.txt", "w", encoding="utf-8")
    for columns in ["A", "B", "C", "D"]:
        if columns == "A":
            glitch_file.write("Trigger = {")
        elif columns == "B":
            glitch_file.write("Player_Mutator = {")
        elif columns == "C":
            glitch_file.write("Enemy_Mutator = {")
        else:
            glitch_file.write("Effector = {")

        row = 2
        eof = 0

        while not eof:
            cell = sheet[columns + str(row)]
            data = '"' + cell.value + '"'
            glitch_file.write(data)
            if sheet[columns + str(row + 1)].value is None:
                eof = 1
            else:
                glitch_file.write(", ")
                if row % 2 == 0:
                    glitch_file.write("\n")
            row += 1
        glitch_file.write("}\n\n")

    glitch_file.write("")
    glitch_file.close()


enemy_process()

stage_modifier("jinxes.txt", "Jinxes = {", ["O", "P", "Q"])
stage_modifier("stages.txt", "Stages = {", ["R", "S", "T"])
stage_modifier("bonus_souls.txt", "Souls = {", ["U", "V", "W"])

enemy_modifier_process("enemy_prefixes.txt", "EnemyPrefixes = {", ["I", "J", "K"])
enemy_modifier_process("enemy_suffixes.txt", "EnemySuffixes = {", ["L", "M", "N"])

usable_process("relics.txt", "Relics = {", workbook["Relics"])
usable_process("affinities.txt", "Affinities = {", workbook["Affinities"])

ware_process()

glitched_process()
