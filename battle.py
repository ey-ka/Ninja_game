import random
import pygame
from player import Player
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


alive_fighters = []
new_alive = random.sample(CHARACTERS, 31)

all_survivors = alive_fighters + new_alive
SECOND_MATCH_CHARACTERS = all_survivors

alive_fighters_two = []
second_alive = random.sample(SECOND_MATCH_CHARACTERS, 15)

for player_data in SECOND_MATCH_CHARACTERS:
    learned_techniques = ["Техника Подмены Тела", "Техника Клонирования"]
    extra_weapon = random.choice(["кунай", "сюрикен"])
    break
def select_fighters():
    fighters = random.sample(CHARACTERS, 2)
    return fighters[0], fighters[1]

def setup_second_match_fighters():
    # Выбираем победителя первой схватки
    winner = Player(alive_fighters, is_winner=True)

    # Случайный противник из оставшихся
    opponent_name = random.choice([
        name for name in SECOND_MATCH_CHARACTERS
        if name != alive_fighters
    ])
    opponent = Player(opponent_name)

    # Распределяем оружие для противника: 2 куная + 1 сюрикен ИЛИ 2 сюрикена + 1 кунай
    if random.choice([True, False]):
        opponent.inventory["кунай"]["count"] = 2
        opponent.inventory["сюрикен"]["count"] = 1
    else:
        opponent.inventory["кунай"]["count"] = 1
        opponent.inventory["сюрикен"]["count"] = 2

    return winner, opponent


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

def post_second_battle_reward(winner, loser):
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
    print(f"Выжило: {len(all_survivors)} из 32")
    print("Выжившие:", ", ".join(alive_fighters_two),", ".join(second_alive))
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
        # Проверяем: можно ли использовать кунай И не активен ли сюрикен
        if (player1.can_use_weapon.get("кунай", False) and
                player1.inventory.get("кунай", 0) > 0 and
                player1.active_weapon != "сюрикен"):
            player1.prepared_kunai = True
            print(f"{player1.name} подготовил кунай!")
        else:
            print(f"{player1.name} не может подготовить кунай (нет в инвентаре или уже использует сюрикен).")
            # Заменяем на случайное действие из допустимого диапазона
            a = random.randint(1, 10)
            print(f"{player1.name} вынужден выбрать другое действие: {a}")

        # --- ПРОВЕРКА ДЕЙСТВИЯ 11 ДЛЯ НИНДЗЯ ---
    if b == 11:
        if (player2.can_use_weapon.get("кунай", False) and
                player2.inventory.get("кунай", 0) > 0 and
                player2.active_weapon != "сюрикен"):
            player2.prepared_kunai = True
            print(f"{player2.name} подготовил кунай!")

        else:
            print(f"{player2.name} не может подготовить кунай (нет в инвентаре/запрещено).")
            # Заменяем на случайное действие из допустимого диапазона
            b = random.randint(1, 10)
            print(f"{player2.name} вынужден выбрать другое действие: {b}")

    if a == 12:
        if (player1.can_use_weapon.get("сюрикен", False) and
                player1.inventory.get("сюрикен", 0) > 0 and
                player1.active_weapon != "кунай"):
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
                player2.inventory.get("сюрикен", 0) > 0 and
                player2.active_weapon != "кунай"):
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

def simulate_second_match_round(player1, player2):
    # Сброс эффектов техник в начале раунда
    player1.reset_technique_effect()
    player2.reset_technique_effect()

    print(f"\n=== ВТОРАЯ СХВАТКА ===")
    print(f"Бойцы: {player1.name} vs {player2.name}")
    print("Нажмите Enter, чтобы начать раунд...")
    input()
    print("Вы нажали Enter — начинаем раунд!")

    a = random.randint(1, 12)
    b = random.randint(1, 12)

    print(f"{player1.name} выбрал действие: {a}")
    print(f"{player2.name} выбрал действие: {b}")

    # Обработка действий 11 (подготовка оружия)
    if a == 11:
        weapon = random.choice(["кунай", "сюрикен"])
        if (weapon in player1.inventory and
                player1.inventory[weapon] > 0 and
                player1.can_use_weapon[weapon]):
            player1.active_weapon = weapon
            if weapon == "кунай":
                player1.prepared_kunai = True
            else:
                player1.prepared_shuriken = True
            print(f"{player1.name} подготовил {weapon}!")
        else:
            print(f"{player1.name} не может подготовить {weapon} (нет в инвентаре/запрещено).")
            a = random.randint(1, 10)
            print(f"{player1.name} вынужден выбрать другое действие: {a}")

    if b == 11:
        weapon = random.choice(["кунай", "сюрикен"])
        if (weapon in player2.inventory and
                player2.inventory[weapon] > 0 and
                player2.can_use_weapon[weapon]):
            player2.active_weapon = weapon
            if weapon == "кунай":
                player2.prepared_kunai = True
            else:
                player2.prepared_shuriken = True
            print(f"{player2.name} подготовил {weapon}!")
        else:
            print(f"{player2.name} не может подготовить {weapon} (нет в инвентаре/запрещено).")
            b = random.randint(1, 10)
            print(f"{player2.name} вынужден выбрать другое действие: {b}")

    # Обработка действий 12 (использование техники)
    technique_used_p1 = False
    technique_used_p2 = False

    if a == 12:
        dmg_mod, desc = player1.use_technique()
        if "Все техники использованы" not in desc:
            technique_used_p1 = True

    if b == 12:
        dmg_mod, desc = player2.use_technique()
        if "Все техники использованы" not in desc:
            technique_used_p2 = True

    # РАСЧЁТ УРОНА
    weapon_p1 = player1.active_weapon
    weapon_p2 = player2.active_weapon

    dmg1, dmg2, desc, lose_kunai_p1, lose_kunai_p2, lose_shuriken_p1, lose_shuriken_p2 = get_damage(
        a, b, weapon_p1, weapon_p2
    )

    # АВТОМАТИЧЕСКОЕ ИСПОЛЬЗОВАНИЕ ТЕХНИКИ при низком HP
    for player in [player1, player2]:
        if (player.hp <= 5 and
                player.hp > 0 and
                player.used_techniques_count < 2 and
                not player.has_used_technique_at_low_hp and
                player.learned_techniques):

            print(f"\n⚠️ {player.name} в отчаянной попытке использует технику для выживания!")
            dmg_mod, tech_desc = player.use_technique()
            player.has_used_technique_at_low_hp = True
            print(tech_desc)

    # Применение урона с учётом активных техник
    p1_damage_to_apply = 0 if player1.is_technique_active() else dmg1
    p2_damage_to_apply = 0 if player2.is_technique_active() else dmg2

    player1.hp += p1_damage_to_apply
    player2.hp += p2_damage_to_apply

    # Вывод описания удара
    if desc:
        print(f"Описание: {desc}")
    else:
        print("Описание: Обычный обмен ударами (нет специального эффекта)")

    p1_lost = False
    p2_lost = False

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

    # Сообщение о защите техникой, если применимо
    if player1.is_technique_active():
        print(f"{player1.name} избегает урона благодаря активной технике!")
    if player2.is_technique_active():
        print(f"{player2.name} избегает урона благодаря активной технике!")

def start_second_match():
    player1, player2 = setup_second_match_fighters()
    print(f"Победитель первой схватки: {player1.name}")
    print(f"Противник: {player2.name}")

    # Показываем начальное состояние
    print(f"\nНачальное состояние:")
    print(f"{player1.name}: HP={player1.hp}, оружие={player1.inventory}, техники={player1.available_techniques}")
    print(f"{player2.name}: HP={player2.hp}, оружие={player2.inventory}")


    # Проводим раунд
    simulate_second_match_round(player1, player2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()



    player1_name, player2_name = select_fighters()
    player1 = Player(player1_name)
    player2 = Player(player2_name)
    print("Начало боя!")

    fighter1 = Player("Игрок 1", 200, 300)
    fighter2 = Player("Игрок 2", 700, 300)

    while True:
        if simulate_round(player1, player2):
            break

    for player in [player1, player2]:
        player.hp = 20  # Полное восстановление здоровья
        player.active_weapon = None  # Сброс активированного оружия
        player.prepared_kunai = False
        player.prepared_shuriken = False
    while True:
        if simulate_second_match_round(player1, player2):
            break

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Управление
            keys = pygame.key.get_pressed()
            # Игрок 1: A/D для движения, Q для атаки
            if keys[pygame.K_a]:
                fighter1.x -= 5
            if keys[pygame.K_d]:
                fighter1.x += 5
            if keys[pygame.K_q] and not fighter1.is_attacking:
                fighter1.attack()
                # Проверка попадания по игроку 2
                if abs(fighter1.x - fighter2.x) < 80:  # Дистанция атаки
                    fighter2.take_damage(10)

            # Игрок 2: Стрелки для движения, O для атаки
            if keys[pygame.K_LEFT]:
                fighter2.x -= 5
            if keys[pygame.K_RIGHT]:
                fighter2.x += 5
            if keys[pygame.K_o] and not fighter2.is_attacking:
                fighter2.attack()
                if abs(fighter2.x - fighter1.x) < 80:
                    fighter1.take_damage(10)

        # Обновление состояния бойцов
            fighter1.update()
            fighter2.update()

        # Отрисовка
            screen.fill((50, 50, 100))  # Синий фон
            fighter1.draw(screen)
            fighter2.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

