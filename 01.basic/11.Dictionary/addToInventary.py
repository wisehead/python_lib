# inventory.py
stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

def display_inventory(inventory):
    total = 0
    print("Inventory:")
    for k,v in inventory.items():
        print(str(v) + ' ' + str(k))
        total = total + v
    print('Total number of items:' + str(total))


def addToInventory(inventory, addItems):
    for v in addItems:
        inventory.setdefault(v, 0)
        inventory[v] = inventory[v] + 1
    return inventory



inv = {'gold coin':42, 'rope':1} 
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = addToInventory(inv, dragonLoot)
display_inventory(inv)
