import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(' | VALIDATOR  |')

file_log_handler = logging.FileHandler('../validator.log')
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s.%(msecs)d %(name)s %(levelname)s | %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)


class Task:
    def __init__(self, file_line):
        words = file_line.split()
        self.length = int(words[0])
        self.readyTime = int(words[1])
        self.dueDate = int(words[2])
        self.weight = int(words[3])

    def __repr__(self):
        # return 'Task nr ' + str(self.startTime)
        return str(self)

    def __str__(self):
        return 'length: ' + str(self.length) + ' readyTime: ' + str(self.readyTime) + ' dueDate:' + str(
            self.dueDate) + ' weight:' + str(self.weight) + '  '

    def is_exceeding_due_date(self, actual_time):
        return actual_time + self.length > self.dueDate


def read_instance(instance_file):
    result = []
    first_line = True
    for line in instance_file:
        if first_line:
            result.append(int(line))
            first_line = False
        else:
            result.append(Task(line))
    return result


def read_result(result_file):
    result = []
    first_line = True
    for line in result_file:
        if first_line:
            result.append(int(line))
            first_line = False
        else:
            words = line.split()
            result += words

    return result


def check_task_amount(instance, result):
    if instance[0] != len(result) - 1:
        logger.error("ERROR ! The task amount in result file is invalid.")
        exit()


def check_uniq_of_tasks(result):
    result = result[1:]
    non_unique_elements = list({x for x in result if result.count(x) > 1})
    if len(non_unique_elements) > 0:
        logger.error("ERROR ! There are non unique tasks in result file.")
        exit()


def check_criteria_value(instance, result):
    iter_result = iter(result)
    next(iter_result)
    actual_time = 0
    criteria_value = 0
    for task_index in iter_result:
        task = instance[int(task_index)]
        if task.readyTime > actual_time:
            actual_time = task.readyTime

        if task.is_exceeding_due_date(actual_time):
            criteria_value += task.weight
        actual_time += task.length

    message_prefix = "The result file is correct." if criteria_value == int(result[0]) \
        else "ERROR ! Invalid criteria value !!!"
    logger.info(
        message_prefix + " Correct criteria value: " + str(criteria_value) + ", actual value: " + str(result[0]))


if __name__ == '__main__':
    instance_file = open(sys.argv[1], "r")
    instance = read_instance(instance_file)
    instance_file.close()
    time = 0

    if ".exe" in sys.argv[2]:
        instance_path = Path(sys.argv[1])
        algorithm_path = Path(sys.argv[2])

        algorithm_index = algorithm_path.name[:6]
        logger.info("Algorytm: " + algorithm_path.name)

        start_time = datetime.now()
        process = subprocess.call([sys.argv[2], sys.argv[1]], shell=True)
        time = (datetime.now() - start_time).microseconds * 1000
        logger.info('---- Czas algorytmu: ' + str(time))

        result_file_path = Path(
            str(instance_path.parents[0]) + "/" + str(algorithm_index) + "-solution-" + str(instance[0]) + ".txt")
        result_file = open(result_file_path, "r")
    else:
        result_file = open(sys.argv[2], "r")

    result = read_result(result_file)
    result_file.close()

    logger.info(sys.argv[1])
    check_task_amount(instance, result)
    check_uniq_of_tasks(result)
    check_criteria_value(instance, result)
    logger.info("------------------------------------------------\n")
