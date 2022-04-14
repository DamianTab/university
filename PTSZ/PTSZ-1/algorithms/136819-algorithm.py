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
    def __init__(self, file_line, index):
        words = file_line.split()
        self.index = index
        self.length = int(words[0])
        self.readyTime = int(words[1])
        self.dueDate = int(words[2])
        self.weight = int(words[3])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'index: ' + str(self.index) + ' length: ' + str(self.length) + ' readyTime: ' + str(
            self.readyTime) + ' dueDate:' + str(self.dueDate) + ' weight:' + str(
            self.weight) + '  '

    def is_ready(self, actual_time):
        return actual_time >= self.readyTime

    def calculate_tardiness(self, actual_time):
        delay_time = actual_time + self.length - self.dueDate
        return self.weight if delay_time > 0 else 0

    def is_delayed(self, actual_time):
        return actual_time + self.length > self.dueDate


def read_instance(instance_file):
    result = []
    first_line = True
    index = 1
    for line in instance_file:
        if first_line:
            result.append(int(line))
            first_line = False
        else:
            result.append(Task(line, index))
            index += 1
    return result


def save_to_file(solution, file_prefix):
    file = open(str(file_prefix) + "136819-solution-" + str(len(solution) - 1) + ".txt", "w")
    file.write(str(solution[0]) + "\n")
    for task in solution[1:]:
        file.write(str(task.index) + ' ')
    file.write("\n")
    file.close()


def run_algorithm(instance, due_date_method):
    solution = []
    score = 0
    current_time = 0

    available_tasks = instance[1:]
    delayed_tasks = []

    if due_date_method:
        available_tasks.sort(key=lambda x: x.dueDate, reverse=False)
    else:
        available_tasks.sort(key=lambda x: x.weight / x.length, reverse=True)

    while len(available_tasks) > 0:
        ready_tasks = []
        to_delete = []
        # Catch ready tasks
        for task in available_tasks:
            if task.is_ready(current_time):
                # Delayd tasks
                if task.is_delayed(current_time):
                    delayed_tasks.append(task)
                    to_delete.append(task)
                else:
                    ready_tasks.append(task)
                    # One task is sufficient
                    break

        available_tasks = [x for x in available_tasks if x not in to_delete]

        if len(ready_tasks) > 0:
            # There is only 1 ready task (look above why only 1)
            best_task = ready_tasks[0]
            solution.append(best_task)
            available_tasks.remove(best_task)
            current_time = current_time + best_task.length
        else:
            # No ready task
            current_time += 1

    for task in delayed_tasks:
        score += task.calculate_tardiness(current_time)
        current_time = current_time + task.length
        solution.append(task)

    solution = [score] + solution
    return solution


if __name__ == '__main__':
    logger.info(sys.argv[1])
    file_prefix, _, instance_size = sys.argv[1].split('-')
    file_prefix_without_index = file_prefix[:-6]

    # Read instance file
    instance_file = open(sys.argv[1], "r")
    instance = read_instance(instance_file)
    instance_file.close()

    # Algorithm
    solution_due = run_algorithm(instance, True)
    logger.info("Wynik algorytmu duedate: " + str(solution_due[0]))

    solution_len_wei = run_algorithm(instance, False)
    logger.info("Wynik algorytmu length/weight: " + str(solution_len_wei[0]))

    solution = solution_due if solution_due[0] < solution_len_wei[0] else solution_len_wei

    # Save to file
    save_to_file(solution, file_prefix_without_index)
