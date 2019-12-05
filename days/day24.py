import re
from typing import Iterator

from days import AOCDay, day


DEBUG = False


class Group:
    SIDE_IMMUNE_SYSTEM = 0
    SIDE_INFECTION = 1

    SIDES = {
        SIDE_IMMUNE_SYSTEM: "Immune System",
        SIDE_INFECTION: "Infection"
    }

    current_target = None
    dead = False

    def __init__(self, identifier, side, unit_count, health, attack_damage, attack_type, initiative, weaknesses=None, immunities=None):
        self.side = side
        self.units = unit_count
        self.health = health
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses[:] if weaknesses else []
        self.immunities = immunities[:] if immunities else []
        self.current_target = None
        self.dead = False
        self.identifier = identifier

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{} units each with {} hit points (immune to {}; weak to {}) with an attack that does {} {} damage at initiative {}".format(
            self.units, self.health,
            ", ".join(self.immunities) if self.immunities else "nothing",
            ", ".join(self.weaknesses) if self.weaknesses else "nothing",
            self.attack_damage, self.attack_type, self.initiative
        )

    @property
    def effective_power(self):
        return self.units * self.attack_damage

    def attack_power(self, target: 'Group'):
        damage = self.effective_power
        if self.attack_type in target.immunities:
            damage = 0
        if self.attack_type in target.weaknesses:
            damage = damage * 2
        return damage

    def select_target(self, other_groups: 'Iterator[Group]'):
        self.current_target = max(other_groups,
                                  key=lambda x: (self.attack_power(x), x.effective_power, x.initiative),
                                  default=None
                                  )
        if self.current_target and self.attack_power(self.current_target) == 0:
            self.current_target = None
        return self.current_target

    @staticmethod
    def inflict_damage(attacker: 'Group', defender: 'Group'):
        damage = attacker.attack_power(defender)
        units_lost = damage // defender.health
        defender.units = max(0, defender.units - units_lost)
        return units_lost

    def attack(self):
        if self.current_target:
            return Group.inflict_damage(self, self.current_target)
        return 0

    def cleanup(self):
        self.current_target = None
        if not self.units:
            self.dead = True

    def boost(self, amount):
        self.attack_damage += amount


@day(24)
class DayTemplate(AOCDay):
    test_input = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""

    GROUP_REGEX = re.compile("(?P<num_units>[0-9]+) units each with (?P<hp>[0-9]+) hit points( \((?P<immuneweakness>.*)\))? with an attack that does (?P<damage>[0-9]+) (?P<damage_type>.*) damage at initiative (?P<initiative>[0-9]+)")
    IMMUNEREGEX = re.compile("immune to (?P<immunities>[^;]*)")
    WEAKNESSREGEX = re.compile("weak to (?P<weaknesses>[^;]*)")

    immune_system_groups = []
    infection_groups = []

    def reset(self):
        self.immune_system_groups = []
        self.infection_groups = []

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        self.immune_system_groups = []
        self.infection_groups = []
        immune = []
        infection = []
        target = immune
        for line in input_data:
            if line == "Immune System:":
                target = immune
            elif line == "Infection:":
                target = infection
            elif line:
                target.append(line)

        self.parse_input(immune, infection)

    def parse_input(self, immune_lines, infection_lines):
        group_id = 1
        for line in immune_lines:
            rx = self.GROUP_REGEX.match(line)

            num_units = int(rx.group("num_units"))
            hp = int(rx.group("hp"))
            damage = int(rx.group("damage"))
            damage_type = rx.group("damage_type")
            initiative = int(rx.group("initiative"))

            immuneweakness = rx.group("immuneweakness")
            immunities, weaknesses = [], []
            if immuneweakness:
                immuneweakness = immuneweakness.split(";")
                for part in immuneweakness:
                    rx_i = self.IMMUNEREGEX.match(part.strip())
                    if rx_i:
                        immunities = rx_i.group("immunities").split(", ")
                    rx_w = self.WEAKNESSREGEX.match(part.strip())
                    if rx_w:
                        weaknesses = rx_w.group("weaknesses").split(", ")
            self.immune_system_groups.append(Group(group_id, Group.SIDE_IMMUNE_SYSTEM, num_units, hp, damage, damage_type, initiative, weaknesses, immunities))
            group_id += 1

        group_id = 1
        for line in infection_lines:
            rx = self.GROUP_REGEX.match(line)

            num_units = int(rx.group("num_units"))
            hp = int(rx.group("hp"))
            damage = int(rx.group("damage"))
            damage_type = rx.group("damage_type")
            initiative = int(rx.group("initiative"))

            immuneweakness = rx.group("immuneweakness")
            immunities, weaknesses = [], []
            if immuneweakness:
                immuneweakness = immuneweakness.split(";")
                for part in immuneweakness:
                    rx_i = self.IMMUNEREGEX.match(part.strip())
                    if rx_i:
                        immunities = rx_i.group("immunities").split(", ")
                    rx_w = self.WEAKNESSREGEX.match(part.strip())
                    if rx_w:
                        weaknesses = rx_w.group("weaknesses").split(", ")
            self.infection_groups.append(Group(group_id, Group.SIDE_INFECTION, num_units, hp, damage, damage_type, initiative, weaknesses, immunities))
            group_id += 1

    def play_round(self):
        # Info
        if DEBUG:
            print("Immune System:")
            for group in self.immune_system_groups:
                print("Group {} contains {} units".format(group.identifier, group.units))
            print("Infection:")
            for group in self.infection_groups:
                print("Group {} contains {} units".format(group.identifier, group.units))
            print("")

        # Target selection phase
        for side in [self.infection_groups, self.immune_system_groups]:
            order = sorted(side, key=lambda x: (x.effective_power, x.initiative), reverse=True)
            chosen_targets = []
            for group in order:
                if group.side == Group.SIDE_INFECTION:
                    chosen_target = group.select_target(
                        filter(lambda x: x not in chosen_targets, self.immune_system_groups))
                else:
                    chosen_target = group.select_target(
                        filter(lambda x: x not in chosen_targets, self.infection_groups))
                if chosen_target:
                    chosen_targets.append(chosen_target)
                if DEBUG and group.current_target:
                    print("{} group {} would deal defending group {} {} damage".format(
                        Group.SIDES[group.side], group.identifier, group.current_target.identifier,
                        group.attack_power(group.current_target)
                    ))

        if DEBUG:
            print("")

        # Attack phase
        damage_done = False
        order = sorted(self.immune_system_groups + self.infection_groups, key=lambda x: x.initiative, reverse=True)
        for group in order:
            res = group.attack()
            if res:
                damage_done = True
            if DEBUG and group.current_target:
                print("{} group {} attacks defending group {}, killing {} units".format(
                    Group.SIDES[group.side], group.identifier, group.current_target.identifier, res
                ))

        if not damage_done:
            raise ValueError("Stalemate!")

        # Cleanup phase
        for group in self.immune_system_groups + self.infection_groups:
            group.cleanup()
        self.immune_system_groups = list(filter(lambda x: not x.dead, self.immune_system_groups))
        self.infection_groups = list(filter(lambda x: not x.dead, self.infection_groups))


    def play_game(self):
        # While both sides still have groups
        while len(self.immune_system_groups) > 0 and len(self.infection_groups) > 0:
            self.play_round()

        # Info
        if DEBUG:
            print("Immune System:")
            if len(self.immune_system_groups):
                for group in self.immune_system_groups:
                    print("Group {} contains {} units".format(group.identifier, group.units))
            else:
                print("No groups remain.")
            print("Infection:")
            if len(self.infection_groups):
                for group in self.infection_groups:
                    print("Group {} contains {} units".format(group.identifier, group.units))
            else:
                print("No groups remain.")

        winning_army = self.immune_system_groups if len(self.immune_system_groups) else self.infection_groups
        units_left = sum(x.units for x in winning_army)
        return units_left, Group.SIDE_IMMUNE_SYSTEM if len(self.immune_system_groups) else Group.SIDE_INFECTION

    def part1(self, input_data):
        yield self.play_game()[0]

    def boost(self, immune_groups, amount):
        for group in immune_groups:
            group.boost(amount)

    def part2(self, input_data):
        boost_amount = 0

        while True:
            # Reset
            self.reset()
            self.common(input_data)

            # Apply boost
            self.boost(self.immune_system_groups, boost_amount)

            if DEBUG:
                print("Boost {}...".format(boost_amount), end="")

            try:
                units_left, army = self.play_game()
                if DEBUG:
                    print(" {} wins".format(army))
                if army == Group.SIDE_IMMUNE_SYSTEM:
                    yield units_left
                    break
                boost_amount += 1
            except ValueError:
                if DEBUG:
                    print(" Stalemate")
                boost_amount += 1
