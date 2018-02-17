import maya.cmds as mc

def rename(name, nodes=None):
    if nodes is None:
        nodes = mc.ls(sl=True, type="transform")
        if not nodes:
            raise RuntimeError("Select a root node to rename.")

    digit_count = name.count("#")
    if digit_count == 0:
        raise RuntimeError("Name has no # sequence.")

    substring = "#" * digit_count
    newsubstrint = "0" * digit_count

    newname = name.replace(substring, newsubstring)

    if newname == name:
        raise RuntimeError("Pound signs must be consecutive.")

    name = name.replace(substring, "%0{0}d".format(digit_count))

    number = 1
    for node in nodes:
        number = rename_chain(node, name, number)

def rename_chain(node, name, number):
    new_name = (name % number)
    node = mc.rename(node, new_name)
    children = mc.listRelatives(node, children=True, type="transform", path=True) or []
    number += 1
    for child in children:
        number = rename_chain(child, name, number)
    return number

#named C_tail01_JNT C_tail02_JNT C_tail03_JNT
rename("C_tail##_JNT")
