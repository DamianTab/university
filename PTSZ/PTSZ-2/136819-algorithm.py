import functools
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
    def __init__(self, start, length, index):
        self.readyTime = int(start)
        self.length = int(length)
        self.index = int(index)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ' readyTime: ' + str(self.readyTime) + ' length: ' + str(self.length) + '  '

    def calculate_flow_time(self, time):
        return max(0, time - self.readyTime)


class Machine:
    def __init__(self, index, ratio):
        self.index = index
        self.ratio = ratio
        self.time = 0.0
        self.task_list = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '|index: ' + str(self.index) + ' ratio: ' + str(self.ratio) + '| '

    def execute_task(self, task):
        time_to_add = self.calculate_time(task)
        if self.time < task.readyTime:
            self.time = task.readyTime
        self.time += time_to_add
        self.task_list.append(task)

    def calculate_time(self, task):
        return task.length * self.ratio


def read_instance(instance_file):
    instance = []
    machines = []
    first_line = True
    second_line = True
    index = 1
    for line in instance_file:
        if first_line:
            instance.append(int(line))
            first_line = False
        elif second_line:
            machines = line.split()
            machines = [float(x) for x in machines]
            second_line = False
        else:
            split_line = line.split()
            instance.append(Task(split_line[1], split_line[0], index))
            index += 1
    return instance, machines


# Solution 0 - criterion result, 1 - first machine tasks list, 2 - second ...
def save_to_file(solution, instance_size):
    file = open("136819-solution-" + str(instance_size) + ".txt", "w")
    file.write(str(solution[0]) + "\n")
    for task_list in solution[1:]:
        for task in task_list:
            file.write(str(task.index) + " ")
        file.write("\n")
    file.close()


def calculate_criteria_value(result):
    criteria_value = 0
    machine_number = -1
    for tasks_on_machine in result:
        actual_time = 0
        machine_number += 1
        machine_factor = machines[machine_number]
        for task in tasks_on_machine:
            ready_time = instance[task.index].readyTime
            if actual_time < ready_time:
                actual_time = ready_time
            actual_time += machine_factor * instance[task.index].length
            criteria_value += instance[task.index].calculate_flow_time(actual_time)

    return round(criteria_value / instance[0], 2)


def compare_machines(a, b):
    return -1 if a.time < b.time or (a.time == b.time and a.ratio < b.ratio) else 1


def compare_tasks(a, b):
    return -1 if a.readyTime < b.readyTime or (a.readyTime == b.readyTime and a.length < b.length) else 1


def run_algorithm(instance, machines):
    machines = [Machine(index, val) for index, val in enumerate(machines)]

    # available tasks
    sort_tasks = instance[1:]
    sort_tasks.sort(key=functools.cmp_to_key(compare_tasks), reverse=False)

    while len(sort_tasks) > 0:
        # Take first for the smallest machine (no idle time)
        max_task_ready_time = min(machines, key=lambda x: x.time).time
        available_tasks = [task for task in sort_tasks if float(task.readyTime) <= max_task_ready_time]

        chosen_task = sort_tasks[0]
        if len(available_tasks) > 0:
            chosen_task = min(available_tasks, key=lambda x: x.length)
        # Take first available machine to not generate idle time
        best_machine = sorted(machines, key=functools.cmp_to_key(compare_machines))[0]
        best_machine.execute_task(chosen_task)
        sort_tasks.remove(chosen_task)

    solution = [[] for _ in range(5)]
    for machine in machines:
        solution[machine.index] = machine.task_list

    solution = [calculate_criteria_value(solution)] + solution
    return solution


if __name__ == '__main__':
    index, _, _ = sys.argv[1].split('-')

    # Read instance file
    instance_file = open(sys.argv[1], "r")
    instance, machines = read_instance(instance_file)
    instance_file.close()

    # Algorithm
    solution = run_algorithm(instance, machines)
    logger.info("Wynik algorytmu: " + str(solution[0]))

    # Save to file
    save_to_file(solution, instance[0])
