import random
import xml.etree.ElementTree as ET
import math
import time


# Classes ------------------------------------------------------------------------------------------------------------

class Oligonucleotide:
    def __init__(self, sequence, occurrence):
        self.sequence = sequence
        self.occurrence = occurrence

    def decrease_occurrence(self):
        self.occurrence -= 1

    def debug(self):
        print("Oligonucleotyde sequence: " + self.sequence + " and occurrence: " + str(self.occurrence))


class Chain:
    # todo by moze dodac ilosc nukleotydow do funkcji uzytecznosci
    def __init__(self, sequence, new_id=-1):
        self.id = new_id
        self.sequence = sequence

    def add_oligonucleotide(self, oligo):
        self.sequence += oligo.sequence[-1:]
        oligo.decrease_occurrence()

    def add_chain(self, chain):
        # print("Podstawa: " + self.sequence + " CALY LANCUCH: " + chain.sequence
        #       + "  to co laczymy: " + chain.sequence[l - 1:])
        self.sequence += chain.sequence[l - 1:]
        chains.remove(chain)

    def debug(self):
        print(" -------- Chain id: " + str(self.id) + " sequence: " + self.sequence)


class Population:
    def __init__(self):
        self.__idList = []
        self.points = 0
        self.sequence = ''
        self.length = 0
        self.usedChainsLength = 0
        self.chainsLength = len(chains)

    def get_list_id(self):
        return self.__idList.copy()

    def set_list_id(self, new_list):
        self.__idList = new_list
        self.evaluate_sequence_and_points()

    def list_append_value(self, value):
        self.__idList.append(value)
        self.evaluate_sequence_and_points()

    def list_delete_last_id(self):
        self.__idList = self.__idList[:-1]
        self.evaluate_sequence_and_points()

    def list_replace_value(self, new_id, value):
        self.__idList[new_id] = value
        self.evaluate_sequence_and_points()

    def evaluate_sequence_and_points(self):
        points = 0
        sequence = ''
        for chain_id in self.get_list_id():
            sequence_to_add = chains[chain_id].sequence
            position = can_merge_strings_different_length(sequence, sequence_to_add)
            if position >= 0:
                points += len(sequence) - position
                sequence = sequence[:position] + sequence_to_add
            else:
                sequence += sequence_to_add
        points -= abs(len(sequence) - n)

        self.points = points
        self.sequence = sequence
        self.length = len(self.sequence)
        self.usedChainsLength = len(self.get_list_id())

    def add_chain_to_pop(self, chain):
        self.list_append_value(chain.id)
        if self.length > n:
            self.list_delete_last_id()
            return False
        return True

    def find_duplicates(self):
        seen = set()
        uniq = set()
        duplicates = set()
        for x in self.get_list_id():
            if x not in seen:
                uniq.add(x)
                seen.add(x)
            else:
                duplicates.add(x)
        return duplicates, uniq

    def replace_duplicates(self, duplicates, uniq):
        possible_values = [x for x in range(1, len(chains))]
        possible_values = set(possible_values)
        possible_values -= uniq
        possible_values = list(possible_values)
        for duplicate in duplicates:
            rand_id = random.choice(possible_values)
            index = self.get_list_id().index(duplicate)
            self.list_replace_value(index, rand_id)

    def mutate(self):
        _, uniq = self.find_duplicates()
        possible_values = [x for x in range(1, len(chains))]
        possible_values = set(possible_values)
        possible_values -= uniq
        possible_values = list(possible_values)
        incorrect_mutation = True
        while incorrect_mutation and len(possible_values) > 0:
            rand_value = random.choice(possible_values)
            possible_values.remove(rand_value)
            possible_indexes = [x for x in range(1, len(self.get_list_id()))]

            while incorrect_mutation and len(possible_indexes) > 0:
                random_index = random.choice(possible_indexes)
                possible_indexes.remove(random_index)
                old_value = self.get_list_id()[random_index]
                self.list_replace_value(random_index, rand_value)
                if self.length > n:
                    self.list_replace_value(random_index, old_value)
                else:
                    incorrect_mutation = False

    def debug(self, show_details=False):
        if show_details:
            print(" -------- Points: " + str(self.points) + " length: " + str(len(self.sequence)) + "/" + str(n)
                  + " chains: " + str(self.usedChainsLength) + "/" + str(self.chainsLength)
                  + "  sequence: " + self.sequence + "\tlist: " + str(self.get_list_id()))
        else:
            print(" -------- Points: " + str(self.points) + " length: " + str(len(self.sequence)) + "/" + str(n)
                  + " chains: " + str(self.usedChainsLength) + "/" + str(self.chainsLength)
                  + "  sequence: " + self.sequence)


# Functions ------------------------------------------------------------------------------------------------------------

def read_from_file():
    root = ET.parse(filename).getroot()
    n = int(root.get('length'))  # poprawna długość wyniku
    start_chain = Chain(root.get('start'))  # startowy oligonukleotyd
    l = len(start_chain.sequence)  # długość oligonukleotydu
    print("n = " + str(n))
    print("start sequence = " + start_chain.sequence)
    print("l = " + str(l))
    for cell in root.iter('cell'):
        occurrence_number = math.floor(int(cell.get('intensity')) / 2)
        occurrence_number = 1 if occurrence_number == 0 else occurrence_number
        oligonucleotides.append(Oligonucleotide(cell.text, occurrence_number))

    return [n, l, start_chain]


def can_merge_strings_fixed_length(str1, str2):
    return str1[-l + 1:] == str2[0:l - 1]


# return position of first string where start merging
def can_merge_strings_different_length(str1, str2):
    # print("---PROBA")
    # print(str1)
    # print(str2)
    if len(str2) > len(str1):
        # print("--- drugi wiekszy")
        for i in range(len(str1)):
            # print(str1[i:])
            # print(str2[0:len(str1)-i])
            if str1[i:] == str2[0:len(str1) - i]:
                return i
    elif len(str2) == len(str1):
        # print("--- drugi równy")
        for i in range(len(str1) - 1):
            # print("teraz i jest: " + str(i))
            # print(str1[i + 1:])
            # print(str2[0:len(str1) - i - 1])
            if str1[i + 1:] == str2[0:len(str1) - i - 1]:
                # print("zwraca: "+ str(i+1))
                return i + 1
    else:
        # print("--- drugi mniejszy")
        iteration_number = 1
        for i in range(len(str1) - len(str2) + 1, len(str1)):
            # print(i)
            # print(str1[i:])
            # print(str2[0:-iteration_number])
            if str1[i:] == str2[0:-iteration_number]:
                return i
            iteration_number += 1
    return -1


def combine_nucleotidies():
    print("\n------------------------------------------------------------------------ Łączenie oligonukleotydów\n")
    for selected in oligonucleotides:
        if selected.occurrence > 0:
            new_chain = Chain(selected.sequence)
            selected.occurrence -= 1
            chain_changed = True
            while chain_changed:
                chain_changed = False
                for tested in oligonucleotides:
                    if tested.occurrence > 0 and tested != selected and can_merge_strings_fixed_length(
                            new_chain.sequence, tested.sequence):
                        # Bierze jeden nukleotyd i łączy z dopasowanym (dodaje tylko ostatnią zasadę azotową)
                        new_chain.add_oligonucleotide(tested)
                        # Zmienił się new_chain więc musimy puścić jeszcze raz od nowa dla wszystkich oligonukleotydów (być może jakiś wcześniejszy się teraz dopasuje)
                        chain_changed = True
            chains.append(new_chain)


def supply_missing_nucleotidies():
    print(
        "\n------------------------------------------------------------------------ Dopisywanie łańcuchów jednego oligonukleotydu (gdy jego wystąpienia są jeszcze > 0 )\n")
    for selected in oligonucleotides:
        while selected.occurrence > 0:
            chains.append(Chain(selected.sequence))
            selected.decrease_occurrence()


def combine_chains():
    print("\n------------------------------------------------------------------------ Łączenie łańcuchów\n")
    for selected in chains:
        for tested in chains:
            if selected != tested and can_merge_strings_fixed_length(selected.sequence, tested.sequence):
                selected.add_chain(tested)


def creat_initial_populations():
    print(
        "\n------------------------------------------------------------------------ Tworzenie populacji początkowych - losowo\n")
    iteration = 0
    while len(populations) < population_size:
        iteration += 1
        population = Population()
        population.list_append_value(start_chain.id)
        possible_chains_id_set = set(list(range(1, len(chains))))
        available_id_list = list(possible_chains_id_set)
        while len(available_id_list) > 0:
            rand_id = random.choice(available_id_list)
            available_id_list.remove(rand_id)
            if population.add_chain_to_pop(chains[rand_id]):
                possible_chains_id_set -= {rand_id}
                available_id_list = list(possible_chains_id_set)
        populations[str(population.get_list_id())] = population
    print("------------------ Wykonano tyle iteracji podczas generowania algorytmem naiwnym (losowym): "
          + str(iteration) + "\n\n")


def creat_initial_populations_greedy_algorithm():
    print(
        "\n------------------------------------------------------------------------ "
        "Tworzenie populacji początkowych - algorytmem zachłannym (zazwyczaj chwile to trwa)\n")
    iteration = 0
    upper_bound_iteration = 400
    while len(populations) < population_size and iteration < upper_bound_iteration:
        iteration += 1
        population = Population()
        population.list_append_value(start_chain.id)
        possible_chains_id = list(range(1, len(chains)))
        population_ready = False
        while not population_ready:
            next_chain_id = max_coverage_chain_id(population, possible_chains_id)
            if next_chain_id is None:
                population_ready = True
            else:
                population.add_chain_to_pop(chains[next_chain_id])
                possible_chains_id.remove(next_chain_id)
        populations[str(population.get_list_id())] = population
    print("------------------ Wykonano tyle iteracji podczas generowania algorytmem zachłannym: " + str(iteration))
    if len(populations) < population_size and iteration == upper_bound_iteration:
        creat_initial_populations()


def max_coverage_chain_id(population, chain_id_list):
    max_coverage = 0
    possible_chain_ids = []
    for chain_id in chain_id_list:
        position = can_merge_strings_different_length(population.sequence, chains[chain_id].sequence)
        # print("+++++++++++")
        # print("position: " + str(position))
        # print("dlugosc sekwencji: " + str(len(population.sequence)))
        # print("coverage points: " + str(len(population.sequence) - position))
        coverage_points = 0 if position == -1 else len(population.sequence) - position
        if coverage_points > max_coverage:
            max_coverage = coverage_points
            possible_chain_ids = [chain_id]
        elif coverage_points == max_coverage:
            possible_chain_ids.append(chain_id)

    # print(max_coverage)
    while len(possible_chain_ids) > 0:
        rand_id = random.choice(possible_chain_ids)
        possible_chain_ids.remove(rand_id)
        test_population = Population()
        test_population.set_list_id(population.get_list_id() + [rand_id])
        if test_population.length <= n:
            return rand_id
    return None


def sort_populations():
    print("------------------ Sortowanie")
    return {k: v for k, v in sorted(populations.items(), key=lambda item: item[1].points, reverse=True)}


def choose_best_solutions():
    print("------------------ Selekcja\n")

    new_dict = {}
    size = 0
    for (k, v) in populations.items():
        if size == population_size:
            break
        new_dict[k] = v
        size += 1
    return new_dict


def add_children_to_dict(children):
    for child in children:
        populations[str(child.get_list_id())] = child


def cross_parents(first, second):
    children = []
    length = min(len(first.get_list_id()), len(second.get_list_id()))
    separators = [random.randrange(length) for _ in range(3)]
    separators.sort()

    first_fragments = [first.get_list_id()[i: j] for i, j in zip([0] + separators, separators + [None])]
    second_fragments = [second.get_list_id()[i: j] for i, j in zip([0] + separators, separators + [None])]
    new_ids_lists = [first_fragments[0] + second_fragments[1] + first_fragments[2] + second_fragments[3],
                     second_fragments[0] + first_fragments[1] + second_fragments[2] + first_fragments[3],
                     first_fragments[0] + first_fragments[1] + second_fragments[2] + second_fragments[3],
                     second_fragments[0] + second_fragments[1] + first_fragments[2] + first_fragments[3]]

    for id_list in new_ids_lists:
        pop = Population()
        pop.set_list_id(id_list)
        # print("PRZED")
        # pop.debug(True)
        duplicates, uniq = pop.find_duplicates()
        pop.replace_duplicates(duplicates, uniq)
        # print("PO")
        # pop.debug(True)
        if pop.length <= n:
            children.append(pop)
        # children.append(pop)
    return children


def crossing():
    print("------------------ Krzyżowanie")
    ten_percent_index = math.ceil(population_size / 10)

    # Krzyzowanie kazdy z kazdym w pierwszych najpelszych 10%
    for first in range(0, ten_percent_index):
        for second in range(first + 1, ten_percent_index):
            children = cross_parents(populations.get(pop_keys[first]), populations.get(pop_keys[first]))
            add_children_to_dict(children)

    # W kazdej dziesiatce krzyzujemy ze soba losowe populacje kilka razy (w zaleznosci od zmiennej)
    for ten in range(0, population_size, 10):
        for _ in range(crossing_frequency):
            possible_indexes = [x for x in range(ten, ten + 10)]
            # Może zostać na końcu np grupa gdzie jest tylko jeden element - wtedy pomijamy i nie krzyżujemy
            if len(possible_indexes) > 1:
                first_parent_index = random.choice(possible_indexes)
                possible_indexes.remove(first_parent_index)
                second_parent_index = random.choice(possible_indexes)
                # print(first_parent_index)
                # print(possible_indexes)
                # print(second_parent_index)
                children = cross_parents(populations.get(pop_keys[first_parent_index]),
                                         populations.get(pop_keys[second_parent_index]))
                add_children_to_dict(children)

    # Krzyzujemy ze sobą populacje z najlepszych 20% z drugą z pozostałej cześci wielokrotnie (8 razy zmienna)
    # print("OSTATNI 20% - 80%")
    for _ in range(crossing_frequency * 8):
        # print("-----------")
        possible_first_indexes = [x for x in range(ten_percent_index * 2)]
        possible_second_indexes = [x for x in range(ten_percent_index * 2, population_size)]
        first_parent_index = random.choice(possible_first_indexes)
        second_parent_index = random.choice(possible_second_indexes)
        children = cross_parents(populations.get(pop_keys[first_parent_index]),
                                 populations.get(pop_keys[second_parent_index]))
        add_children_to_dict(children)


def mutation():
    if iteration >= mutation_iteration_bound and iteration % mutation_frequency == 0:
        print("------------------ Mutacja")
        possible_indexes = [x for x in range(1, population_size)]
        for _ in range(mutation_quantity):
            if len(possible_indexes) == 0:
                break
            rand_index = random.choice(possible_indexes)
            possible_indexes.remove(rand_index)
            population = populations.get(pop_keys[rand_index])
            population.mutate()
            populations[str(population.get_list_id())] = population
        return True
    return False


def debug_chains():
    for e in chains:
        e.debug()


def debug_populations(show_details=False):
    for (k, v) in populations.items():
        v.debug(show_details)
    print("-------- Długosc słownika wszystkich populacji wynosi: " + str(len(populations)))


def print_generation_number(generation=-1):
    print(
        "\n------------------------------------------------------------------------ Pokolenie nr:"
        + str(generation) + "\n")


def pause_algorithm():
    if sleep_mode:
        print("***************************************************************************")
        print("Wstrzymanie programu na 10s ...")
        time.sleep(10)


# Main ------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    debug_mode = True
    sleep_mode = True
    chains = []
    populations = {}

    population_size = 100  # ilosc populacji w pokoleniu
    max_iterations = 100  # ilość pokoleń jaka ma zostać wytworzona
    crossing_frequency = 4  # współczynnik częstości krzyżowań w algorytmie
    mutation_iteration_bound = 30  # po ilu rundach zacznie mutować populację
    mutation_frequency = 6  # co ile rund będzie mutować
    mutation_quantity = math.ceil(population_size * 0.05)  # ile zmutuje populacji podczas jednego cyklu mutowania

    filename = "instance2.xml"
    # variables read from file
    oligonucleotides = []
    n = 0
    l = 0
    start_chain = Chain("")

    from_file = read_from_file()
    n = from_file[0]  # oczekiwana długość wyniku
    l = from_file[1]  # długość oligonukleotydów
    start_chain = from_file[2]  # początkowy oligonukleotyd

    # Dopasowanie oligonukleotydów w łańcuchy
    combine_nucleotidies()
    debug_chains()

    # Tworzenie łańcuchów jednoelementowych z oligonukleotydów jeśli jeszcze mają jakieś wystąpić
    supply_missing_nucleotidies()
    debug_chains()

    # Próba połączenia istniejących już łańcuchów (może się zdarzyć że da się je jeszcze połączyć)
    combine_chains()

    # Dodanie pierwszego elementu startowego (indeks 0)
    chains = [start_chain] + chains
    # Nadanie identyfikatorów
    for i in range(len(chains)):
        chains[i].id = i
    debug_chains()

    # Tworzenie instancji początkowych
    creat_initial_populations_greedy_algorithm()
    # stary sposób ()
    # creat_initial_populations()
    debug_populations()
    pause_algorithm()

    # Sortowanie i selekcja populacji
    populations = sort_populations()

    # Utworzenie listy odwzorującej indeks na klucz w słowniku (mapie)
    pop_keys = list(populations.keys())
    debug_populations()
    pause_algorithm()

    #     GŁÓWNY ALGORYTM
    for iteration in range(max_iterations):
        print_generation_number(iteration)

        # Krzyżowanie
        crossing()

        # Sortowanie i Selekcja
        populations = sort_populations()
        populations = choose_best_solutions()
        pop_keys = list(populations.keys())

        # Mutacja
        if mutation():
            # Sortowanie i Selekcja
            populations = sort_populations()
            populations = choose_best_solutions()
            pop_keys = list(populations.keys())

        if debug_mode:
            debug_populations(True)
            # pause_algorithm()

    if not debug_mode:
        debug_populations(True)

    print("\nNajlepszy wynik:")
    populations[pop_keys[0]].debug(True)
