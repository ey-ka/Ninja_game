import random
from damage_table import DAMAGE_TABLE
from damage_table_weapon import WEARON_P1_ATTACKS, WEARON_P2_ATTACKS, WEARON_EFFECTS_DUAL_KUNAI
from damage_table_suriken import SHURIKEN_P1_ATTACKS, SHURIKEN_P2_ATTACKS, SHURIKEN_DUAL_ATTACKS
from mixed_table import SHURIKEN_P1_KUNAI_P2_ATTACKS, SHURIKEN_P2_KUNAI_P1_ATTACKS



CHARACTERS = [
    "Наруто Удзумаки",
    "Саскэ Утиха",
    "Сакура Харуно",
    "Какаси Хатакэ",
    "Дзирайя",
    "Цунадэ",
    "Орочимару",
    "Итати Утиха",
    "Кисамэ Хосигаки",
    "Хидан",
    "Какудзу",
    "Дейдара",
    "Сасори",
    "Конан",
    "Пэйн (Нагато)",
    "Киллер Би",
    "Гаара",
    "Канкуро",
    "Тэмари",
    "Рок Ли",
    "Майто Гай",
    "Нэдзи Хюга",
    "Хината Хюга",
    "Сино Абурамэ",
    "Киба Инудзука",
    "Акамару",
    "Тёдзи Акимити",
    "Ино Яманака",
    "Сикамару Нара",
    "Асума Сарутоби",
    "Курэнай Юхи",
    "Ирука Умино",
    "Анко Митараси",
    "Ибики Морино",
    "Мифунэ",
    "Тиё",
    "Сасори (в детстве)",
    "Эй (Райкагэ)",
    "Мэй Тэруми",
    "Ооноки",
    "Цучикагэ",
    "Данзо Симура",
    "Конохамару Сарутоби",
    "Моэги",
    "Удон",
    "Сидзунэ",
    "Торифу Абураме",
    "Сино Абурамэ (отец)",
    "Курэнай (в юности)",
    "Аоба Ямасиро",
    "Гэнма Сирануи",
    "Райдо Намиаси",
    "Каси",
    "Хана Инудзука",
    "Тэн‑Тэн",
    "Хаку",
    "Дзабудза Момоти",
    "Югито Нии",
    "Роси",
    "Хан",
    "Фу",
    "Утаката",
    "Чоудзи Акимити (младший, из следующего поколения)"
]
#CHARACTERS = [f"Персонаж_{i}" for i in range(1, 64)]
alive_fighters = []
new_alive = random.sample(CHARACTERS, 31)
def select_fighters():
    fighters = random.sample(CHARACTERS, 2)
    return fighters[0], fighters[1]

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 20
        self.inventory = {"кунай": 1, "сюрикен": 1}
        self.active_weapon = None  # "кунай"/"сюрикен"/None — используется в бою
        self.prepared_kunai = False  # подготовлен ли кунай (действие 11)
        self.prepared_shuriken = False  # подготовлен ли сюрикен (действие 12)
        self.can_use_weapon = {
            "кунай": True,
            "сюрикен": True
        }
        self.learned_techniques = []

    def switch_weapon(self, new_weapon):
        """Переключает активное оружие, если оно доступно."""
        if (new_weapon in self.inventory
                and self.inventory[new_weapon] > 0
                and self.can_use_weapon[new_weapon]):
            self.active_weapon = new_weapon
            print(f"{self.name} переключился на {new_weapon}.")
            return True
        else:
            print(f"{self.name} не может переключиться на {new_weapon} (нет в инвентаре/сломано).")
            return False

    def get_weapon_status(self):
        return self.active_weapon if self.active_weapon else "нет оружия"
def get_damage(a, b, weapon_p1, weapon_p2):
    """Рассчитывает урон и эффект для раунда."""
    if weapon_p1 is None and weapon_p2 is None:
         table = DAMAGE_TABLE
    elif weapon_p1 == "кунай" and weapon_p2 is None:
       table = WEARON_P1_ATTACKS
    elif weapon_p1 is None and weapon_p2 == "кунай":
        table = WEARON_P2_ATTACKS
    elif weapon_p1 == "кунай" and weapon_p2 == "кунай":
        table = WEARON_EFFECTS_DUAL_KUNAI
    elif weapon_p1 == "сюрикен" and weapon_p2 is None:
        table = SHURIKEN_P1_ATTACKS
    elif weapon_p1 is None and weapon_p2 == "сюрикен":
        table = SHURIKEN_P2_ATTACKS
    elif weapon_p1 == "сюрикен" and weapon_p2 == "сюрикен":
        table =  SHURIKEN_DUAL_ATTACKS
    elif weapon_p1 == "кунай" and weapon_p2 == "сюрикен":
        table = SHURIKEN_P2_KUNAI_P1_ATTACKS
    elif weapon_p1 == "сюрикен" and weapon_p2 == "кунай":
        table = SHURIKEN_P1_KUNAI_P2_ATTACKS
    else:
        table = DAMAGE_TABLE

    result = table.get((a, b), (0, 0, None, False, False, False, False))

    return result

#round_counter = 0

def post_battle_reward(winner, loser):
    # Награждаем победителя
    weapon = random.choice(["кунай", "сюрикен"])
    winner.inventory[weapon] += 1
    print(f"{winner.name} изучил новую технику и получил {weapon}!")

    techniques_to_learn = ["Техника Подмены Тела", "Техника Клонирования"]
    if not hasattr(winner, "learned_techniques"):
        winner.learned_techniques = []

    for technique in techniques_to_learn:
        if technique not in winner.learned_techniques:
            winner.learned_techniques.append(technique)
            print(f"{winner.name} освоил технику: {technique}!")

    if winner.name not in alive_fighters:
        alive_fighters.append(winner.name)





    # Выводим статистику
    print(f"\n=== Итоги раунда ===")
    print(f"Выжило: {len(new_alive)} из 64")
    print("Выжившие:", ", ".join(alive_fighters),", ".join(new_alive))
    print("Освоенные техники:", ", ".join(winner.learned_techniques))
def simulate_round(player1, player2):
    #global round_counter  # Говорим, что используем глобальную переменную
    #round_counter += 1  # Теперь это работает: переменная существует

     #Фиксируем a и b по номеру раунда
    #if round_counter == 1:
     #   a, b = 12, 3
    #elif round_counter == 2:
     #   a, b = 10, 7
    #elif round_counter == 3:
     #   a, b = 12, 10
    #else:
     #  raise ValueError("Больше двух раундов не поддерживается")
    print(f"\n=== РАУНД ===")
    print("Нажмите Enter, чтобы начать раунд...")
    input()
    print("Вы нажали Enter — начинаем раунд!")


    a = random.randint(1, 12)
    b = random.randint(1, 12)

    print(f"{player1.name} выбрал действие: {a}")
    print(f"{player2.name} выбрал действие: {b}")

    # Подготовка оружия (не активация!)
    if a == 11:
        if (player1.can_use_weapon.get("кунай", False) and
                player1.inventory.get("кунай", 0) > 0):
            player1.prepared_kunai = True
            print(f"{player1.name} подготовил кунай!")
            desired = "кунай" if player1.active_weapon == "сюрикен" else "сюрикен"
            player1.switch_weapon(desired)
        else:
            print(f"{player1.name} не может подготовить кунай (нет в инвентаре/запрещено).")
            # Заменяем на случайное действие из допустимого диапазона
            a = random.randint(1, 10)
            print(f"{player1.name} вынужден выбрать другое действие: {a}")

        # --- ПРОВЕРКА ДЕЙСТВИЯ 11 ДЛЯ НИНДЗЯ ---
    if b == 11:
        if (player2.can_use_weapon.get("кунай", False) and
                player2.inventory.get("кунай", 0) > 0):
            player2.prepared_kunai = True
            print(f"{player2.name} подготовил кунай!")
            desired = "кунай" if player2.active_weapon == "сюрикен" else "сюрикен"
            player2.switch_weapon(desired)
        else:
            print(f"{player2.name} не может подготовить кунай (нет в инвентаре/запрещено).")
            # Заменяем на случайное действие из допустимого диапазона
            b = random.randint(1, 10)
            print(f"{player2.name} вынужден выбрать другое действие: {b}")

    if a == 12:
        if (player1.can_use_weapon.get("сюрикен", False) and
                player1.inventory.get("сюрикен", 0) > 0):
            player1.prepared_shuriken = True
            print(f"{player1.name} подготовил сюрикен!")
        else:
            print(f"{player1.name} не может подготовить сюрикен (нет в инвентаре/запрещено).")
            # Заменяем на случайное действие из допустимого диапазона
            a = random.randint(1, 10)
            print(f"{player1.name} вынужден выбрать другое действие: {a}")

        # --- ПРОВЕРКА ДЕЙСТВИЯ 11 ДЛЯ НИНДЗЯ ---
    if b == 12:
        if (player2.can_use_weapon.get("сюрикен", False) and
                player2.inventory.get("сюрикен", 0) > 0):
            player2.prepared_shuriken = True
            print(f"{player2.name} подготовил сюрикен!")
        else:
            print(f"{player2.name} не может подготовить сюрикен (нет в инвентаре/запрещено).")
            # Заменяем на случайное действие из допустимого диапазона
            b = random.randint(1, 10)
            print(f"{player2.name} вынужден выбрать другое действие: {b}")




    # РАСЧЁТ УРОНА: используем ТОЛЬКО активное оружие (из прошлого раунда!)
    weapon_p1 = player1.active_weapon
    weapon_p2 = player2.active_weapon



    dmg1, dmg2, desc, lose_kunai_p1, lose_kunai_p2, lose_shuriken_p1, lose_shuriken_p2 = get_damage(a, b, weapon_p1, weapon_p2)


    # Применение урона
    player1.hp += dmg1
    player2.hp += dmg2


    # Вывод описания удара
    if desc:
        print(f"Описание: {desc}")
    else:
        print("Описание: Обычный обмен ударами (нет специального эффекта)")

    p1_lost = False
    p2_lost = False

    #lost = lose_kunai_p1 or lose_kunai_p2 or lose_shuriken_p1 or lose_shuriken_p2

    # ОБРАБОТКА ПОТЕРИ ОРУЖИЯ (из таблицы урона)
    # P1: проверяем только флаги P1
    if lose_kunai_p1 and weapon_p1 == "кунай":
        player1.active_weapon = None
        player1.can_use_weapon["кунай"] = False
        player1.inventory["кунай"] -= 1
        p1_lost = True
        print(f"{player1.name} потерял кунай!")

    if lose_shuriken_p1 and weapon_p1 == "сюрикен":
        player1.active_weapon = None
        player1.can_use_weapon["сюрикен"] = False
        player1.inventory["сюрикен"] -= 1
        p1_lost = True
        print(f"{player1.name} потерял сюрикен!")

    # P2: проверяем только флаги P2
    if lose_kunai_p2 and weapon_p2 == "кунай":
        player2.active_weapon = None
        player2.can_use_weapon["кунай"] = False
        player2.inventory["кунай"] -= 1
        p2_lost = True
        print(f"{player2.name} потерял кунай!")

    if lose_shuriken_p2 and weapon_p2 == "сюрикен":
        player2.active_weapon = None
        player2.can_use_weapon["сюрикен"] = False
        player2.inventory["сюрикен"] -= 1
        p2_lost = True
        print(f"{player2.name} потерял сюрикен!")

    # АКТИВАЦИЯ ОРУЖИЯ: подготовленное оружие становится активным В СЛЕДУЮЩЕМ РАУНДЕ
    if not p1_lost:
        if player1.prepared_kunai and player1.inventory.get("кунай", 0) > 0:
            player1.active_weapon = "кунай"
        elif player1.prepared_shuriken and player1.inventory.get("сюрикен", 0) > 0:
            player1.active_weapon = "сюрикен"


    if not p2_lost:
        if player2.prepared_kunai and player2.inventory.get("кунай", 0) > 0:
            player2.active_weapon = "кунай"
        elif player2.prepared_shuriken and player2.inventory.get("сюрикен", 0) > 0:
            player2.active_weapon = "сюрикен"


    # Сброс флагов подготовки (оружие теперь активно; для новой подготовки нужно снова выбрать 11/12)
    player1.prepared_kunai = False
    player1.prepared_shuriken = False
    player2.prepared_kunai = False
    player2.prepared_shuriken = False

    print(f"{player1.name}: {player1.get_weapon_status()}")
    print(f"{player2.name}: {player2.get_weapon_status()}")

    # Проверка HP и вывод результата раунда
    if player1.hp <= 0 and player2.hp <= 0:
        print(f"\nОба игрока погибли одновременно! Ничья!")
        return True
    elif player1.hp <= 0:
        print(f"\n{player2.name} победил! {player1.name} повержен.")
        post_battle_reward(player2, player1)
        return True
    elif player2.hp <= 0:
        print(f"\n{player1.name} победил! {player2.name} повержен.")
        post_battle_reward(player1, player2)
        return True

    print(f"Урон: {player1.name}={dmg1}, {player2.name}={dmg2}")
    print(f"\nТекущее HP: {player1.name} = {player1.hp}, {player2.name} = {player2.hp}")

    return False

def main():
    player1_name, player2_name = select_fighters()
    player1 = Player(player1_name)
    player2 = Player(player2_name)
    print("Начало боя!")
    while True:
        if simulate_round(player1, player2):
            break

if __name__ == "__main__":
    main()


