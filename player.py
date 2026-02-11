import random

class Player:
    def __init__(self, name, is_winner=False):
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

        # НОВЫЕ ПОЛЯ ДЛЯ ВТОРОЙ СХВАТКИ
        self.used_techniques_count = 0  # счётчик использованных техник (максимум 2)
        self.has_used_technique_at_low_hp = False  # флаг: использована ли техника при низком HP
        self.technique_active_this_round = False  # техника активна в текущем раунде

    def get_weapon_status(self):
        return self.active_weapon if self.active_weapon else "нет оружия"

    # Метод для подготовки оружия (действие 11)
    def prepare_weapon(self, weapon_name):
        """Подготовить оружие (кунай или сюрикен) по действию 11"""
        if (weapon_name in self.inventory
                and self.inventory[weapon_name] > 0
                and self.can_use_weapon[weapon_name]):
            self.active_weapon = weapon_name
            if weapon_name == "кунай":
                self.prepared_kunai = True
            else:
                self.prepared_shuriken = True
            print(f"{self.name} подготовил {weapon_name}!")
            return True
        else:
            print(f"{self.name} не может подготовить {weapon_name} (нет в инвентаре/запрещено).")
            return False

    # Метод для использования техники (действие 12)
    def use_technique(self):
        """Использовать технику по действию 12 (максимум 2 раза за бой)"""
        if self.used_techniques_count >= 2:
            print(f"{self.name} уже использовал все доступные техники!")
            return 0, "Все техники использованы"

        if not self.learned_techniques:
            print(f"{self.name} не знает техник!")
            return 0, "Нет доступных техник"

        # Случайный выбор техники из выученных
        technique = random.choice(self.learned_techniques)
        self.used_techniques_count += 1
        self.technique_active_this_round = True  # активируем эффект на текущий раунд

        print(f"{self.name} использует технику: {technique}!")
        print(f"→ Эффект: {self.get_technique_effect_description(technique)}")

        return 0, f"{technique}: полное избежание урона в этом раунде"

    # Вспомогательный метод для описания эффекта техники
    def get_technique_effect_description(self, technique):
        if technique == "Техника Подмены Тела":
            return "Игрок мгновенно перемещается в безопасное место, избегая атаки"
        elif technique == "Техника Клонирования":
            return "Клон принимает удар на себя, защищая настоящего ниндзя"
        else:
            return "Неизвестный эффект техники"

    # Метод для автоматического использования техники при низком HP (≤5 и >0)
    def auto_use_technique_if_low_hp(self):
        """Автоматически использует технику, если HP ≤5 и техники ещё остались"""
        if (self.hp <= 5
                and self.hp > 0
                and self.used_techniques_count < 2
                and not self.has_used_technique_at_low_hp
                and self.learned_techniques):

            print(f"\n⚠️ {self.name} в отчаянной попытке использует технику для выживания!")
            damage_mod, desc = self.use_technique()
            self.has_used_technique_at_low_hp = True
            return damage_mod, desc

        return 0, "Автоматическое использование техники не требуется"

    # Метод для сброса эффекта техники в начале нового раунда
    def reset_technique_effect(self):
        """Сбрасывает эффект техники в начале нового раунда"""
        self.technique_active_this_round = False

    # Метод для проверки, активна ли техника в текущем раунде
    def is_technique_active(self):
        """Проверяет, активна ли защитная техника в текущем раунде"""
        return self.technique_active_this_round

    # Метод для добавления бонусного оружия (для победителя первой схватки)
    def add_bonus_weapon(self, weapon_type):
        """Добавляет +1 к указанному оружию (для победителя)"""
        if weapon_type in self.inventory:
            self.inventory[weapon_type] += 1
            print(f"{self.name} получил дополнительное оружие: {weapon_type} (+1)")

    # Метод для добавления техник (для победителя первой схватки)
    def learn_techniques(self, techniques_list):
        """Обучает игрока новым техникам (для победителя)"""
        for technique in techniques_list:
            if technique not in self.learned_techniques:
                self.learned_techniques.append(technique)
        print(f"{self.name} освоил техники: {', '.join(techniques_list)}")