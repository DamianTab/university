import random


class Task:
    def __init__(self, start, length):
        self.readyTime = start
        self.length = length

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ' readyTime: ' + str(self.readyTime) + ' length: ' + str(self.length) + '  '


def generate_machines():
    machines = [1.0]
    for i in range(4):
        rand_number = 1 + random.randint(1, 16) / 4
        machines.append(rand_number)
    random.shuffle(machines)
    return machines


def create_task(instance, temp_task_length, start_time, max_length):
    length = random.randint(1, max_length)
    instance.append(Task(start_time, length))
    temp_task_length.append(length)
    return instance, temp_task_length


def generate_instance(instance_size):
    instance = []
    max_length = 20
    time = 0

    for i in range(0, instance_size, 5):
        temp_task_length = []

        # First 5 tasks
        if i == 0:
            for _ in range(5):
                instance, temp_task_length = create_task(instance, temp_task_length, 0, max_length)
        # Rest tasks
        else:
            for _ in range(3):
                instance, temp_task_length = create_task(instance, temp_task_length, time, max_length)
            for _ in range(2):
                rand_time = random.randint(max_length, max_length * 2)
                instance, temp_task_length = create_task(instance, temp_task_length, time + rand_time, max_length)

        random_task_length = random.choice(temp_task_length)
        time += random_task_length
    random.shuffle(instance)
    random.shuffle(instance)
    return instance


def save_to_file(size, machines, instance):
    file = open("136819-instance-" + str(size) + ".txt", "w")

    # Save 2 first lines (size and machine workspeed factor)
    file.write(str(size) + "\n")
    for i in range(5):
        file.write(str(machines[i]))
        if i != 4:
            file.write(" ")
    file.write("\n")
    # Save instance
    for task in instance:
        file.write(
            str(task.length) + " " + str(task.readyTime) + "\n")
    file.close()


if __name__ == '__main__':
    random.seed()
    # instance_sizes = [x for x in range(50, 501, 50)]
    instance_sizes = [x for x in range(15, 16, 50)]
    for size in instance_sizes:
        machines = generate_machines()
        print("Tworzenie instancji: " + str(size))
        print(machines)
        instance = generate_instance(size)
        save_to_file(size, machines, instance)
