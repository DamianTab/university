import logging
import sys

logger = logging.getLogger(' | ALGORYTM-DAMIAN  |')

file_log_handler = logging.FileHandler('algorytmy.log')
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s.%(msecs)d %(name)s %(levelname)s | %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)


class Task:
    def __init__(self, subtasks_length, due_time, weight, index):
        self.subtasks = subtasks_length
        self.length = sum(subtasks_length)
        self.dueTime = due_time
        self.weight = weight
        self.index = index

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n(p1: ' + str(self.subtasks[0]) + ' p2: ' + str(self.subtasks[1]) + ' p3: ' + str(
            self.subtasks[2]) + ' length: ' + str(self.length) + ' dueTime: ' + str(self.dueTime) + ' weight: ' + str(
            self.weight) + ' index: ' + str(self.index) + ')'


class Machine:
    def __init__(self):
        self.times = [0.0, 0.0, 0.0]
        self.delay_value = 0.0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '| times: ' + str(self.times) + ' delay: ' + str(self.delay_value) + ' | '

    def execute_task(self, task):
        self.times[0] = self.times[0] + task.subtasks[0]
        self.times[1] = max(self.times[0], self.times[1]) + task.subtasks[1]
        self.times[2] = max(self.times[1], self.times[2]) + task.subtasks[2]
        self.delay_value += max(0, self.times[2] - task.dueTime) * task.weight


def read_instance(instance_file):
    instance = []
    first_line = True
    index = 1
    for line in instance_file:
        if first_line:
            instance.append(int(line))
            first_line = False
        else:
            split_line = line.split()
            subtasks = [int(x) for x in split_line[:3]]
            instance.append(Task(subtasks, int(split_line[3]), int(split_line[4]), index))
            index += 1
    return instance


def save_to_file(solution, instance_size):
    file = open("136819-solution-" + str(instance_size) + ".txt", "w")
    file.write(str(solution[0]) + "\n")
    for task in solution[1:]:
        file.write(str(task.index) + " ")
    file.write("\n")
    file.close()


def calculate_criteria_value(instance, machine):
    weights_sum = sum([task.weight for task in instance[1:]])
    criteria_value = round(machine.delay_value / weights_sum, 2)
    return criteria_value


def compare_tasks(a, b):
    return -1 if a.readyTime < b.readyTime or (a.readyTime == b.readyTime and a.length < b.length) else 1


def choose_best_task(task):
    return float(task.length) / task.weight


def run_algorithm(instance):
    coefficient = 10 + instance[0]//50

    solution = []
    machine = Machine()
    tasks = instance[1:]
    tasks.sort(key=lambda x: x.dueTime, reverse=False)

    while len(tasks) > 0:
        first_task_part = coefficient if len(tasks) >= coefficient else len(tasks)
        possible_tasks = tasks[:first_task_part]
        chosen_task = min(possible_tasks, key=lambda x: choose_best_task(x))

        machine.execute_task(chosen_task)
        solution.append(chosen_task)
        tasks.remove(chosen_task)

    solution = [calculate_criteria_value(instance, machine)] + solution
    return solution


if __name__ == '__main__':
    index, _, _ = sys.argv[1].split('-')

    # Read instance file
    instance_file = open(sys.argv[1], "r")
    instance = read_instance(instance_file)
    instance_file.close()

    # Algorithm
    solution = run_algorithm(instance)
    logger.info("Wynik algorytmu: " + str(solution[0]))

    # Save to file
    save_to_file(solution, instance[0])
