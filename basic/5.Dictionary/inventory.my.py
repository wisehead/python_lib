# inventory.py
stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

def display_inventory(inventory):
    total = 0
    print("Inventory:")
    for k,v in inventory.items():
        print(str(v) + ' ' + str(k))
        total = total + v
    print('Total number of items:' + str(total))

display_inventory(stuff)
