import random


class Task:
    def __init__(self, start, length):
        self.startTime = start
        self.endTime = start + length
        self.length = length
        self.readyTime = self.startTime
        self.dueDate = self.endTime
        self.weight = random.randint(1, 10)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'length: ' + str(self.length) + ' startTime: ' + str(self.startTime) + ' readyTime: ' + str(
            self.readyTime) + ' dueDate:' + str(
            self.dueDate) + ' weight:' + str(self.weight) + '  '

    def ready_time_lengthen(self):
        difference_time = random.randint(0, self.startTime)
        self.readyTime -= difference_time

    def due_date_lengthen(self, instance_time):
        difference_time = random.randint(0, instance_time - self.endTime) // 2
        self.dueDate += difference_time


def draw_task_weight(amount, task_length, available_time):
    weights_list = []
    for i in range(amount):
        if task_length == 1:
            random_value = random.randint(1, 5)
        elif task_length == 2:
            random_value = random.randint(6, 15)
        else:
            random_value = round(available_time / (amount - i))
        available_time -= random_value
        weights_list += [random_value]

    return weights_list, available_time


def generate_instance(instance_size):
    group_size = 10
    result = []
    # Divide into subgroups
    for first_group_index in range(0, instance_size, group_size):
        available_time = group_size * 10
        available_task_length = []
        short_task_amount = round(group_size * 0.4)
        long_task_amount = round(group_size * 0.2)
        medium_task_amount = group_size - short_task_amount - long_task_amount

        # Draw task length
        temp_list, available_time = draw_task_weight(short_task_amount, 1, available_time)
        available_task_length += temp_list
        temp_list, available_time = draw_task_weight(medium_task_amount, 2, available_time)
        available_task_length += temp_list
        temp_list, available_time = draw_task_weight(long_task_amount, 3, available_time)
        available_task_length += temp_list

        # Shuffle task lengths and create tasks
        random.shuffle(available_task_length)
        actual_time = first_group_index * 10
        for length in available_task_length:
            result.append(Task(actual_time, length))
            actual_time += length

    # Draw which tasks should be before readyTime
    ready_time_coefficient = 1
    ready_time_task = random.sample(result, round(instance_size * ready_time_coefficient))
    for task in ready_time_task:
        task.ready_time_lengthen()

    # Draw which tasks should have longer dueDate
    due_date_coefficient = 0.5
    due_date_task = random.sample(result, round(instance_size * due_date_coefficient))
    for task in due_date_task:
        task.due_date_lengthen(instance_size * 10)
    random.shuffle(result)
    return result


def save_to_file(instance, size):
    file = open("136819-instance-" + str(size) + ".txt", "w")
    file.write(str(size) + "\n")
    for task in instance:
        file.write(
            str(task.length) + " " + str(task.readyTime) + " " + str(task.dueDate) + " " + str(task.weight) + "\n")
    file.close()


if __name__ == '__main__':
    random.seed()
    instance_sizes = [x for x in range(50, 501, 50)]
    for size in instance_sizes:
        instance = generate_instance(size)
        print(instance)
        save_to_file(instance, size)
