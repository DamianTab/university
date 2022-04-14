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
    def __init__(self, start, length):
        self.readyTime = int(start)
        self.length = int(length)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ' readyTime: ' + str(self.readyTime) + ' length: ' + str(self.length) + '  '

    def calculate_flow_time(self, time):
        return max(0, time - self.readyTime)


def read_instance(instance_file):
    instance = []
    machines = []
    first_line = True
    second_line = True
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
            instance.append(Task(split_line[1], split_line[0]))
    return instance, machines


def read_result(result_file):
    result = []
    first_line = True
    for line in result_file:
        if first_line:
            result.append(float(line))
            first_line = False
        else:
            one_machine_list = list(line.split())
            one_machine_list = [int(x) for x in one_machine_list]
            result.append(one_machine_list)

    return result


def check_task_amount(instance, result):
    task_amount = 0
    for machine_list in result[1:]:
        task_amount += len(machine_list)

    if instance[0] != task_amount:
        logger.error("ERROR ! The task amount in result file is invalid.")
        exit()


def check_0_length_instance(instance):
    for task in instance[1:]:
        if task.length == 0:
            logger.error("ERROR ! There are non unique tasks in result file.")
            exit()


def check_uniq_of_tasks(result):
    all_elements = [x for sublist in result[1:] for x in sublist]
    non_unique_elements = list({x for x in all_elements if all_elements.count(x) > 1})
    if len(non_unique_elements) > 0:
        logger.error("ERROR ! There are non unique tasks in result file.")
        exit()


def check_criteria_value(instance, machines, result):
    criteria_value = 0
    machine_number = -1
    for tasks_on_machine in result[1:]:
        actual_time = 0
        machine_number += 1
        machine_factor = machines[machine_number]
        for task_id in tasks_on_machine:
            ready_time = instance[task_id].readyTime
            if actual_time < ready_time:
                actual_time = ready_time
            actual_time += machine_factor * instance[task_id].length
            criteria_value += instance[task_id].calculate_flow_time(actual_time)

    criteria_value = round(criteria_value / instance[0], 2)
    message_prefix = "CORRECT " if criteria_value == float(result[0]) \
        else "ERROR ! Invalid criteria value !!! Correct criteria value: " + str(criteria_value) + " ."
    logger.info(
        message_prefix + " Actual value: " + str(result[0]))


if __name__ == '__main__':
    logger.info("------------------------------------------------\n")
    logger.info(sys.argv[1])
    instance_file = open(sys.argv[1], "r")
    instance, machines = read_instance(instance_file)
    instance_file.close()

    if "-algorithm.exe" in sys.argv[2]:
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

    check_0_length_instance(instance)
    check_task_amount(instance, result)
    check_uniq_of_tasks(result)
    check_criteria_value(instance, machines, result)
