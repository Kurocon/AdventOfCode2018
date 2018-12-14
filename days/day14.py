from typing import Optional

from days import AOCDay, day


class Recipe:
    next: Optional['Recipe'] = None
    prev: Optional['Recipe'] = None
    score: int = 0

    def __init__(self, score: int, previous_entry: Optional['Recipe'] = None, next_entry: Optional['Recipe'] = None):
        self.score = score
        self.prev = previous_entry
        self.next = next_entry


@day(14)
class DayFourteen(AOCDay):
    test_input = "59414"

    first_recipe: Recipe = None
    last_recipe: Recipe = None
    current_recipe1: Recipe = None
    current_recipe2: Recipe = None
    final_recipe: Recipe = None

    num_recipes: int = None
    current_amount_of_recipes: int = 0
    recipe_to_find: str = None

    def common(self, input_data):
        # input_data = self.test_input
        self.first_recipe = Recipe(3, None, None)
        self.last_recipe = Recipe(7, self.first_recipe, None)
        self.first_recipe.next = self.last_recipe
        self.num_recipes = int(input_data)
        self.recipe_to_find = input_data
        self.current_recipe1 = self.first_recipe
        self.current_recipe2 = self.last_recipe
        self.current_amount_of_recipes = 2
        self.final_recipe = None

    def part1(self, input_data):
        while self.current_amount_of_recipes < (self.num_recipes + 10):
            # Get the sum of the two current recipes
            recipe_sum = str(self.current_recipe1.score + self.current_recipe2.score)

            if self.current_amount_of_recipes == self.num_recipes:
                self.final_recipe = self.last_recipe
            elif (self.current_amount_of_recipes-1) == self.num_recipes:
                self.final_recipe = self.last_recipe.prev

            # Add new recipes to the end
            if len(recipe_sum) == 2:
                self.last_recipe.next = Recipe(int(recipe_sum[0]), self.last_recipe, None)
                self.last_recipe = self.last_recipe.next
                self.last_recipe.next = Recipe(int(recipe_sum[1]), self.last_recipe, None)
                self.last_recipe = self.last_recipe.next
                self.current_amount_of_recipes += 2
            else:
                self.last_recipe.next = Recipe(int(recipe_sum[0]), self.last_recipe, None)
                self.last_recipe = self.last_recipe.next
                self.current_amount_of_recipes += 1

            # Get the new recipes of the elves
            elf_1_offset = 1 + self.current_recipe1.score
            for _ in range(elf_1_offset):
                new_recipe_1 = self.current_recipe1.next
                if new_recipe_1 is None:
                    new_recipe_1 = self.first_recipe
                self.current_recipe1 = new_recipe_1

            elf_2_offset = 1 + self.current_recipe2.score
            for _ in range(elf_2_offset):
                new_recipe_2 = self.current_recipe2.next
                if new_recipe_2 is None:
                    new_recipe_2 = self.first_recipe
                self.current_recipe2 = new_recipe_2

            # recipe = self.first_recipe
            # string = ""
            # while recipe is not None:
            #     if recipe == self.current_recipe1:
            #         string += "({})".format(recipe.score)
            #     elif recipe == self.current_recipe2:
            #         string += "[{}]".format(recipe.score)
            #     else:
            #         string += " {} ".format(recipe.score)
            #     recipe = recipe.next
            # yield string

        yield "Last 10 recipes: {}".format(self.last_n(10))

    def part2(self, input_data):
        input_data = self.recipe_to_find
        yield "Finding '{}'".format(input_data)
        last_n_numbers = "37"
        num_iterations = 0
        for recipe in self.recipes():
            # yield recipe.score, last_n_numbers
            num_iterations += 1
            last_n_numbers += str(recipe.score)
            if len(last_n_numbers) >= len(input_data):
                if len(last_n_numbers) > len(input_data):
                    last_n_numbers = last_n_numbers[-len(input_data):]
                if last_n_numbers == input_data:
                    # yield recipe.score, last_n_numbers
                    yield "input found after {} iterations".format(num_iterations - len(input_data) + 2)
                    break

    def recipes(self):
        while True:
            # Get the sum of the two current recipes
            recipe_sum = str(self.current_recipe1.score + self.current_recipe2.score)

            # Add new recipes to the end
            if len(recipe_sum) == 2:
                self.last_recipe.next = Recipe(int(recipe_sum[0]), self.last_recipe, None)
                self.last_recipe = self.last_recipe.next
                yield self.last_recipe
                self.last_recipe.next = Recipe(int(recipe_sum[1]), self.last_recipe, None)
                self.last_recipe = self.last_recipe.next
                yield self.last_recipe
            else:
                self.last_recipe.next = Recipe(int(recipe_sum[0]), self.last_recipe, None)
                self.last_recipe = self.last_recipe.next
                yield self.last_recipe

            # Get the new recipes of the elves
            elf_1_offset = 1 + self.current_recipe1.score
            for _ in range(elf_1_offset):
                new_recipe_1 = self.current_recipe1.next
                if new_recipe_1 is None:
                    new_recipe_1 = self.first_recipe
                self.current_recipe1 = new_recipe_1

            elf_2_offset = 1 + self.current_recipe2.score
            for _ in range(elf_2_offset):
                new_recipe_2 = self.current_recipe2.next
                if new_recipe_2 is None:
                    new_recipe_2 = self.first_recipe
                self.current_recipe2 = new_recipe_2

    def last_n(self, n: int):
        recipe = self.final_recipe.next
        string = ""
        for _ in range(n):
            string += "{}".format(recipe.score)
            recipe = recipe.next
        return string
