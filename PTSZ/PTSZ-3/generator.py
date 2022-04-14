import random


class Task:
    def __init__(self, subtasks_length, due_time, weight):
        self.subtasks = subtasks_length
        self.length = sum(subtasks_length)
        self.dueTime = due_time
        self.weight = weight

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '(p1: ' + str(self.subtasks[0]) + ' p2: ' + str(self.subtasks[1]) + ' p3: ' + str(
            self.subtasks[2]) + ' length: ' + str(self.length) + ' dueTime: ' + str(self.dueTime) + ' weight: ' + str(
            self.weight) + ')  '


def generate_instance(instance_size):
    instance = []
    max_weight = 10
    max_length = 100
    time = 0

    for i in range(instance_size):
        subtasks_length = [0, 0, 0]
        weight = random.randint(int(0.1 * max_weight), max_weight)
        # choose overall length of work (all 3 subtasks)
        length = random.randint(int(0.2 * max_length), max_length)

        # the longest task are in the middle or the last
        long_subtask_index = random.randint(1, 2)
        subtasks_length[long_subtask_index] = random.randint(int(0.45 * length), int(0.65 * length))

        # choose length of the second (the longest) task
        if long_subtask_index == 1:
            subtasks_length[2] = random.randint(int(0.25 * length), int(0.3 * length))
        else:
            subtasks_length[1] = random.randint(int(0.25 * length), int(0.3 * length))
        # choose length of the first task (shortest)
        subtasks_length[0] = length - subtasks_length[1] - subtasks_length[2]

        # Calculate due_time
        if i % 5 == 2 or i % 5 == 3:
            value = int(0.1 * length)
            time = time + value if random.randint(1, 5) > 1 else time - value
        else:
            time += random.randint(int(0.6 * length), int(1.1 * length))
        due_time = time
        instance.append(Task(subtasks_length, due_time, weight))
        random.shuffle(instance)
    return instance


def save_to_file(size, instance):
    file = open("136819-instance-" + str(size) + ".txt", "w")
    # Save instance size
    file.write(str(size) + "\n")
    # Save instance
    for task in instance:
        file.write(
            str(task.subtasks[0]) + ' ' + str(task.subtasks[1]) + ' ' + str(task.subtasks[2]) + ' ' + str(
                task.dueTime) + ' ' + str(task.weight) + "\n")
    file.close()


if __name__ == '__main__':
    random.seed()
    instance_sizes = [x for x in range(50, 501, 50)]
    for size in instance_sizes:
        print("Tworzenie instancji: " + str(size))
        instance = generate_instance(size)
        save_to_file(size, instance)
