from game import Person, bcolors
from magic import Spell
from inventory import Item
import random



# Create Black Magic
fire = Spell("Fire", 25, 600, "Black")
thunder = Spell("Thunder", 25, 600, "Black")
blizzard = Spell("Blizzard", 25, 600, "Black")
meteor = Spell("Meteor", 40, 1200, "Black")
quake = Spell("Quake", 14, 140, "Black")
atomic_bomb = Spell("Atomic-Bomb", 100, 1000, "Black")


# Create White Magic
cure = Spell("Cure", 25, 620, "White")
cura = Spell("Cura", 32, 1200, "White")
cura_special = Spell("Cura-Special", 50, 6000, "White")


# Create some Items

# Heal
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores party's HP/MP", 9999)
hielixer = Item("Mega-Elixer", "elixer", "Fully restores party's HP/MP", 9999)

# Attack
grande = Item("Grande", "attack", "Deals 500 damage", 500)
knife = Item("Knife", "attack", "Deals 200 damage", 200)


player_spells = [fire, thunder, blizzard, meteor, cure, cura, atomic_bomb]
enemy_spells = [atomic_bomb, meteor, cura_special]


player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5} , {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5}, {"item": hielixer, "quantity": 2}, {"item": grande, "quantity": 2},
                {"item": knife, "quantity": 5}]


player1 = Person("Shain ", 2160, 132, 300, 34, player_spells, player_items)
player2 = Person("Chris ", 1610, 188, 312, 34, player_spells, player_items)
player3 = Person("Robot ", 2060, 174, 283, 34, player_spells, player_items)

enemy1 = Person("Enemy1 ", 1250, 13000, 560, 325, enemy_spells, [])
enemy2 = Person("Enemy2 ", 1200, 7630, 525, 25, enemy_spells, [])
enemy3 = Person("Enemy3 ", 2500, 13000, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]



running = True
print(bcolors.CYAN + bcolors.BOLD + "Welcome to Battle Game" + bcolors.ENDC)
counter_enemies = []
while running:

    print("\n")
    print(bcolors.BOLD + "NAMES:                           HP                                      MP")

    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stat()
    for player in players:
        if player.get_hp() > 0:
            player.choose_action()
            choice = input("    Choose action: ")
            index = int(choice) - 1

            if index == 0:
                damage = player.generate_damage()
                enemy = player.choose_target(enemies)
                if enemies[enemy].get_hp() > 0:
                    enemies[enemy].take_damage(damage)
                print(f'You attacked {enemies[enemy].name.replace(" ", "")} for {damage} points of damage.')

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.RED + enemies[enemy].name.replace(" ", "") + " Has died.", bcolors.ENDC)
                    counter_enemies.append(enemies[enemy])
                    del enemies[enemy]
            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("    Choose magic: ")) - 1

                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                magic_damage = spell.generate_damage()
                current_mp = player.get_mp()

                if spell.cost > current_mp:
                    print(bcolors.OKBLUE + "\nNot enough MP \n" "Do you have just " + str(current_mp) + " MP \nNext turn." + bcolors.ENDC)
                    continue
                player.reduce_mp(spell.cost)

                if spell.type == "White":
                    player.heal(magic_damage)
                    print(bcolors.OKGREEN + "\n" + spell.name + " heals for " + str(magic_damage) + " HP." + bcolors.ENDC)

                elif spell.type == "Black":
                    if player.get_hp() > 0:
                        enemy = player.choose_target(enemies)
                        enemies[enemy].take_damage(magic_damage)
                        print(bcolors.CYAN + "\n" + spell.name + " deals " + str(magic_damage) + " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(bcolors.RED + enemies[enemy].name.replace(" ", "") + " Has died.", bcolors.ENDC)
                        counter_enemies.append(enemies[enemy])
                        del enemies[enemy]

            elif index == 2:
                player.choose_item()
                item_choice = int(input("    Choose Item: ")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]
                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                    continue
                player.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " Heals for", str(item.prop), "HP", bcolors.ENDC)

                elif item.type == "elixer":
                    if item.name == "Mega-Elixer":
                        for i in players:
                            i.hp = i.max_hp
                            i.mp = i.max_mp
                    else:
                        player.hp = player.max_hp
                        player.mp = player.max_mp
                    print(bcolors.OKGREEN + "\n" + item.name + " Fully restored HP/MP ", bcolors.ENDC)

                elif item.type == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.CYAN + "\n" + item.name + " Deals", str(item.prop), "points of damage to" + enemies[enemy].name + bcolors.ENDC)
                    if enemies[enemy].get_hp() == 0:
                        print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " Has died.", bcolors.ENDC)
                        counter_enemies.append(enemies[enemy])
                        del enemies[enemy]

            defeated_enemies = 0
            defeated_players = 0
            for enemy in counter_enemies:
                if enemy.get_hp() == 0:
                    defeated_enemies += 1

            for player in players:
                if player.get_hp() == 0:
                    defeated_players += 1

            if defeated_enemies == 2:
                print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                running = False
                break

            elif defeated_players == 2:
                print(bcolors.RED + "Your enemies have defeated you!" + bcolors.ENDC)
                running = False
                break

            print("\n")

            for enemy in enemies:
                if running == True and enemy.get_hp() > 0:
                    enemy_choice = random.randrange(0, 2)
                    if enemy_choice == 0:
                        target = random.randrange(0, 3)
                        enemy_damage = enemy.generate_damage()
                        players[target].take_damage(enemy_damage)
                        print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for " + str(enemy_damage))

                    elif enemy_choice == 1:
                        spell, magic_damage = enemy.choose_enemy_spell()
                        enemy.reduce_mp(spell.cost)

                        if spell.type == "White":
                            enemy.heal(magic_damage)
                            print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + "for " + str(magic_damage) + " HP." + bcolors.ENDC)

                        elif spell.type == "Black":
                            target = random.randrange(0, 3)
                            players[target].take_damage(magic_damage)

                            print(bcolors.CYAN + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(magic_damage) + " points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                            if players[target].get_hp() == 0:
                                print(bcolors.RED + players[target].name.replace(" ", "") + " Has died.", bcolors.ENDC)





