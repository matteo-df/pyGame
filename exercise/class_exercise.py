class Monster:
    def __init__(self, health, energy):
        self.health = health
        self.energy = energy

    def attack(self, amount):
        print('The monster has attacked!')
        print(f'A damage of {amount} was dealt.')
        self.energy -= 20

    def get_damage(self, amount):
        self.health -= amount


class Scorpion(Monster):
    def __init__(self, health, energy, poison_damage):
        super().__init__(health, energy)
        self.poison_damage = poison_damage

    def attack(self):
        print('The scorpion has attacked!')
        print(f'A poison damage of {self.poison_damage} was dealt.')
        self.energy -= 20


class Hero:
    def __init__(self, damage, monster):
        self.damage = damage
        self.monster = monster

    def attack(self):
        self.monster.get_damage(self.damage)


if __name__ == '__main__':
    print('\n###\n')

    monster = Monster(health=100, energy=50)
    hero = Hero(damage=20, monster=monster)
    hero.attack()
    monster.attack(amount=20)
    scorpion = Scorpion(health=50, energy=40, poison_damage=30)
    scorpion.attack()

    print('\n###')
