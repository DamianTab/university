import logging
import subprocess
import sys
import time as timelib

logger = logging.getLogger(' | VALIDATOR  |')

file_log_handler = logging.FileHandler('validator.log')
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s.%(msecs)d %(name)s %(levelname)s | %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)


class Task:
    def __init__(self, subtasks_length, due_time, weight):
        self.subtasks = subtasks_length
        self.length = sum(subtasks_length)
        self.dueTime = due_time
        self.weight = weight

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n(p1: ' + str(self.subtasks[0]) + ' p2: ' + str(self.subtasks[1]) + ' p3: ' + str(
            self.subtasks[2]) + ' length: ' + str(self.length) + ' dueTime: ' + str(self.dueTime) + ' weight: ' + str(
            self.weight) + ')'


def read_instance(instance_file):
    instance = []
    first_line = True
    for line in instance_file:
        if first_line:
            instance.append(int(line))
            first_line = False
        else:
            split_line = line.split()
            subtasks = [int(x) for x in split_line[:3]]
            instance.append(Task(subtasks, int(split_line[3]), int(split_line[4])))
    return instance


def read_result(result_file):
    result = []
    first_line = True
    for line in result_file:
        if first_line:
            result.append(float(line))
            first_line = False
        else:
            task_order = line.split()
            task_order = [int(x) for x in task_order]
            result += task_order
    return result


def check_task_amount(instance, result):
    if instance[0] != len(result[1:]):
        logger.error("ERROR ! The task amount in result file is invalid.")
        exit()


def check_0_attribute_instance(instance):
    for task in instance[1:]:
        if 0 in task.subtasks:
            logger.error("ERROR ! One of task's length is 0 !!!")
            exit()
        elif task.weight == 0:
            logger.error("ERROR ! Task WEIGHT is 0 !!!")
            exit()


def check_uniq_of_tasks(result):
    non_unique_elements = list({x for x in result[1:] if result[1:].count(x) > 1})

    if len(non_unique_elements) > 0:
        logger.error("ERROR ! There are non unique tasks in result file. Non-unique: {}", non_unique_elements)
        exit()


def check_criteria_value(instance, result):
    criteria_value = 0
    machine_times = [0, 0, 0]

    for task_id in result[1:]:
        task = instance[task_id]
        machine_times[0] = machine_times[0] + task.subtasks[0]
        machine_times[1] = max(machine_times[0], machine_times[1]) + task.subtasks[1]
        machine_times[2] = max(machine_times[1], machine_times[2]) + task.subtasks[2]
        criteria_value += max(0, machine_times[2] - task.dueTime) * task.weight

    weights_sum = sum([task.weight for task in instance[1:]])
    criteria_value = round(criteria_value / weights_sum, 2)
    message_prefix = "CORRECT " if criteria_value == result[
        0] else "ERROR ! Invalid criteria value !!! Correct criteria value: " + str(criteria_value) + " ."
    logger.info(message_prefix + " Actual value: " + str(result[0]))


if __name__ == '__main__':
    logger.info("------------------------------------------------\n")
    logger.info(sys.argv[1])
    instance_file = open(sys.argv[1], "r")
    instance = read_instance(instance_file)
    instance_file.close()

    if "-algorithm.exe" in sys.argv[2]:
        result_file = open(sys.argv[2], "r")

        algorithm_name = sys.argv[2]
        algorithm_index = algorithm_name[:6]
        logger.info(algorithm_name)

        start_time = timelib.time_ns()
        process = subprocess.call([algorithm_name, sys.argv[1]], shell=True)
        time = round((timelib.time_ns() - start_time) / 1000)
        logger.info('--------------- Czas algorytmu: ' + str(time))

        result_file_path = str(algorithm_index) + "-solution-" + str(int(instance[0])) + ".txt"
        result_file = open(result_file_path, "r")
    else:
        result_file = open(sys.argv[2], "r")

    result = read_result(result_file)
    result_file.close()

    check_0_attribute_instance(instance)
    check_task_amount(instance, result)
    check_uniq_of_tasks(result)
    check_criteria_value(instance, result)
