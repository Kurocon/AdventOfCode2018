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
        self.units = [health for x in range(unit_count)]
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
            len(self.units), self.health,
            ", ".join(self.immunities) if self.immunities else "nothing",
            ", ".join(self.weaknesses) if self.weaknesses else "nothing",
            self.attack_damage, self.attack_type, self.initiative
        )

    @property
    def effective_power(self):
        return len(self.units) * self.attack_damage

    def attack_power(self, target: 'Group'):
        damage = self.effective_power
        if self.attack_type in target.immunities:
            damage = 0
        if self.attack_type in target.weaknesses:
            damage *= 2
        return damage

    def select_target(self, other_groups: 'Iterator[Group]'):
        max_damage = 0
        max_groups = []

        for target in other_groups:
            damage = self.attack_power(target)
            if damage > max_damage:
                max_damage = damage
                max_groups = [target]
            if damage == max_damage:
                max_groups.append(target)

        possible_targets = sorted(max_groups, key=lambda x: (x.effective_power, x.initiative), reverse=True)
        self.current_target = possible_targets[0] if possible_targets else None
        return possible_targets[0] if possible_targets else None

    @staticmethod
    def inflict_damage(attacker: 'Group', defender: 'Group'):
        damage = attacker.attack_power(defender)
        units_lost = damage // defender.health

        units_left = len(defender.units)
        defender.units = defender.units[units_lost:]
        return min(units_lost, units_left)

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

    def part1(self, input_data):
        # While both sides still have groups
        while len(self.immune_system_groups) > 0 and len(self.infection_groups) > 0:
            # Info
            if DEBUG:
                print("Immune System:")
                for group in self.immune_system_groups:
                    print("Group {} contains {} units".format(group.identifier, len(group.units)))
                print("Infection:")
                for group in self.infection_groups:
                    print("Group {} contains {} units".format(group.identifier, len(group.units)))
                print("")

            # Target selection phase
            for side in [self.infection_groups, self.immune_system_groups]:
                order = sorted(side, key=lambda x: (x.effective_power, x.initiative), reverse=True)
                chosen_targets = []
                for group in order:
                    if group.side == Group.SIDE_INFECTION:
                        chosen_target = group.select_target(filter(lambda x: x not in chosen_targets,self.immune_system_groups))
                    else:
                        chosen_target = group.select_target(filter(lambda x: x not in chosen_targets, self.infection_groups))
                    if chosen_target:
                        chosen_targets.append(chosen_target)
                    if DEBUG and group.current_target:
                        print("{} group {} would deal defending group {} {} damage".format(
                            Group.SIDES[group.side], group.identifier, group.current_target.identifier, group.attack_power(group.current_target)
                        ))

            if DEBUG:
                print("")

            # Attack phase
            order = sorted(self.immune_system_groups + self.infection_groups, key=lambda x: x.initiative, reverse=True)
            for group in order:
                res = group.attack()
                if DEBUG and group.current_target:
                    print("{} group {} attacks defending group {}, killing {} units".format(
                        Group.SIDES[group.side], group.identifier, group.current_target.identifier, res
                    ))

            # Cleanup phase
            for group in self.immune_system_groups + self.infection_groups:
                group.cleanup()
            self.immune_system_groups = list(filter(lambda x: not x.dead, self.immune_system_groups))
            self.infection_groups = list(filter(lambda x: not x.dead, self.infection_groups))

        # Info
        if DEBUG:
            print("Immune System:")
            if len(self.immune_system_groups):
                for group in self.immune_system_groups:
                    print("Group {} contains {} units".format(group.identifier, len(group.units)))
            else:
                print("No groups remain.")
            print("Infection:")
            if len(self.infection_groups):
                for group in self.infection_groups:
                    print("Group {} contains {} units".format(group.identifier, len(group.units)))
            else:
                print("No groups remain.")

        winning_army = self.immune_system_groups if len(self.immune_system_groups) else self.infection_groups
        units_left = sum(len(x.units) for x in winning_army)
        yield units_left

    def boost(self, immune_groups, amount):
        for group in immune_groups:
            group.boost(amount)

    def get_new_boost(self, boost_amount, phase):
        if phase == 0:
            return boost_amount + 1000
        if phase == 1:
            return boost_amount + 100
        if phase == 2:
            return boost_amount + 10
        if phase == 3:
            return boost_amount + 1
        raise ValueError("Invalid phase {}".format(phase))

    def part2(self, input_data):
        boost_amount = 0
        phase = 0
        min_boost_that_still_fails = 0
        while True:
            # Reset
            self.reset()
            self.common(input_data)

            # Apply boost
            self.boost(self.immune_system_groups, boost_amount)

            stalemate = False

            # While both sides still have groups
            turn = 0
            while len(self.immune_system_groups) > 0 and len(self.infection_groups) > 0:
                turn += 1
                # Info
                if DEBUG:
                    print("Immune System:")
                    for group in self.immune_system_groups:
                        print("Group {} contains {} units".format(group.identifier, len(group.units)))
                    print("Infection:")
                    for group in self.infection_groups:
                        print("Group {} contains {} units".format(group.identifier, len(group.units)))
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
                order = sorted(self.immune_system_groups + self.infection_groups, key=lambda x: x.initiative, reverse=True)
                damage_done = False
                for group in order:
                    res = group.attack()
                    if res > 0:
                        damage_done = True
                    if DEBUG and group.current_target:
                        print("{} group {} attacks defending group {}, killing {} units".format(
                            Group.SIDES[group.side], group.identifier, group.current_target.identifier, res
                        ))

                if not damage_done:
                    print("Stalemate detected! Resetting and going to higher boost")
                    stalemate = True
                    break

                # Cleanup phase
                for group in self.immune_system_groups + self.infection_groups:
                    group.cleanup()
                self.immune_system_groups = list(filter(lambda x: not x.dead, self.immune_system_groups))
                self.infection_groups = list(filter(lambda x: not x.dead, self.infection_groups))

            # Info
            if DEBUG:
                print("Immune System:")
                if len(self.immune_system_groups):
                    for group in self.immune_system_groups:
                        print("Group {} contains {} units".format(group.identifier, len(group.units)))
                else:
                    print("No groups remain.")
                print("Infection:")
                if len(self.infection_groups):
                    for group in self.infection_groups:
                        print("Group {} contains {} units".format(group.identifier, len(group.units)))
                else:
                    print("No groups remain.")

            winning_army = self.immune_system_groups if len(self.immune_system_groups) else self.infection_groups
            units_left = sum(len(x.units) for x in winning_army)

            if stalemate:
                print("Stalemate detected! Resetting and going to higher boost")
                print("Skipping boost {}".format(boost_amount))
                boost_amount += 1
            elif len(self.immune_system_groups):
                if(min_boost_that_still_fails + 1 == boost_amount):
                    break
                phase += 1
                print("We won!")
                print("Current boost: {}".format(boost_amount))
                print("Units left: {}".format(sum(len(x.units) for x in self.immune_system_groups)))
                boost_amount = min_boost_that_still_fails
                print("Entering new phase {}".format(phase))
            else:
                min_boost_that_still_fails = boost_amount
                boost_amount = boost_amount + 1 # self.get_new_boost(boost_amount, phase)
                print("Failed! New boost is {}".format(boost_amount))

        print("Minimum boost necessary is {} # {}".format(min_boost_that_still_fails + 1, boost_amount))
        yield units_left

