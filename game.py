import random


class bcolors:
    HEADDER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'


class Person:
    def __init__(self, name, hp, mp, attack, defence, magic, items):
        self.name = name
        self.max_hp = hp
        self.max_mp = mp
        self.mp = mp
        self.hp = hp
        self.attack_low = attack - 10
        self.attack_high = attack + 10
        self.defence = defence
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.attack_low, self.attack_high)

    def take_damage(self, damage):
        while self.hp > 0:
            self.hp -= damage
            if self.hp < 0:
                self.hp = 0
            return self.hp

    def heal(self, damage):
        self.hp += damage
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print("\n" + bcolors.MAGENTA + bcolors.BOLD + "    Actions" + bcolors.ENDC)
        for item in self.actions:
            print("         " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.MAGENTA + bcolors.BOLD + "    Magic" + bcolors.ENDC)
        for spell in self.magic:
            print("         " + str(i) + ".", spell.name, "(Magic cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.MAGENTA + bcolors.BOLD + "    Items" + bcolors.ENDC)
        for item in self.items:
            print("         " + str(i) + ".", item["item"].name, ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.MAGENTA + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose target: ")) - 1
        return choice

    def get_enemy_stat(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.max_hp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""
        if len(hp_string) < 11:
            decreased_hp = 11 - len(hp_string)

            while decreased_hp > 0:
                current_hp += " "
                decreased_hp -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                                 __________________________________________________ ")
        print(bcolors.BOLD + self.name + "             " +
              current_hp + " |" + bcolors.RED + hp_bar + bcolors.ENDC
              + "|     ")

    def get_stats(self):
        hp_bar = ""
        mp_bar = ""
        hp_bar_ticks = (self.hp / self.max_hp) * 100 / 4
        mp_bar_ticks = (self.mp / self.max_mp) * 100 / 10

        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""
        if len(hp_string) < 9:
            decreased_hp = 9 - len(hp_string)

            while decreased_hp > 0:
                current_hp += " "
                decreased_hp -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)

        current_mp = ""
        if len(mp_string) < 7:
            decreased_mp = 7 - len(mp_string)

            while decreased_mp > 0:
                current_mp += " "
                decreased_mp -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print("                                _________________________               __________ ")
        print(bcolors.BOLD + self.name + "              " +
              current_hp + " |" + bcolors.RED + hp_bar + bcolors.ENDC
              + "|     " +
              current_mp + " |" + bcolors.BLUE + mp_bar + bcolors.ENDC + "|     ")

    def choose_enemy_spell(self):

        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_damage = spell.generate_damage()
        return spell, magic_damage
            

