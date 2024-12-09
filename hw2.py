import os
import sys

next_index = 1


class task:
    def __init__(self, t, c, d, next_index):
        self.t = t
        self.c = c
        self.d = d
        self.idx = next_index
        self.active_time = 0
        self.runtime = 0
        self.abs_ddl = 100000
        self.active = True


file_input_data = []
output_results = []

total_time_units = 100000

n = 0
u = 0
v = 0

# true is preemptive, false is non-preemptive
p = True


def initialize_output_folder():
    dir_name = "output"
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass


def file_process_line(line):
    global n
    global u
    global v
    global next_index
    line_data = line.split()
    n = int(line_data[0])
    u = float(line_data[1])
    v = int(line_data[2])
    temp = []

    for i in range(3, len(line_data), 3):
        new_task = task(int(line_data[i]), int(line_data[i + 1]), int(line_data[i + 2]), next_index)
        next_index += 1
        temp.append(new_task)
    next_index = 1
    return temp


def get_file_input(filename):
    file_reader = open(filename, "r")
    line = file_reader.readline()
    while line != "":
        file_input_data.append(file_process_line(line))
        line = file_reader.readline()

    file_reader.close()


def output_result():
    file_writer = open("./output/2022315690_HW2.txt", "w")
    #print("dllm")
    for idx in output_results:
        file_writer.write(str(idx) + "\n")
    file_writer.close()


# Little tools
def get_task(taskset, idx):
    for task in taskset:
        if task.idx == idx:
            return task


# Schedulers
# return the idx of the process to run for next time unit
def fcfs(tasks, cur_id):
    available_tasks = [task for task in tasks if task.active and task.runtime < task.c]
    if not available_tasks:
        return -1
    available_tasks.sort(key=lambda task: (task.active_time, task.idx))
    return available_tasks[0].idx


def sjf(tasks, cur_id, p):
    # shortest job first
    if p == False and cur_id != -1:
        tsk = get_task(tasks, cur_id)
        if (tsk.runtime < tsk.c):
            return cur_id
    available_tasks = [task for task in tasks if task.active and task.runtime < task.c]
    if not available_tasks:
        return -1
    available_tasks.sort(key=lambda task: ((task.c - task.runtime), task.idx))
    return available_tasks[0].idx


def rm(tasks, cur_id, p):
    # it's based on priority, right?
    # priority is decided by t
    # job with shortest t first
    if p == False and cur_id != -1:
        if get_task(tasks, cur_id).runtime < get_task(tasks, cur_id).c:
            return cur_id
    available_tasks = [task for task in tasks if task.active and task.runtime < task.c]
    if not available_tasks:
        return -1
    available_tasks.sort(key=lambda task: (task.t, task.idx))
    return available_tasks[0].idx


def edf(tasks, cur_id, p):
    # Earlest abs ddl
    if p == False and cur_id != -1:
        if get_task(tasks, cur_id).runtime < get_task(tasks, cur_id).c:
            return cur_id

    available_tasks = [task for task in tasks if task.active and task.runtime < task.c]
    if not available_tasks:
        return -1
    available_tasks.sort(key=lambda task: (task.abs_ddl, task.idx))
    return available_tasks[0].idx


# Processor (single processor)
def check_ddl_miss(tasks, time):
    for task in tasks:
        if time >= task.abs_ddl:
            if task.runtime < task.c:
                return task.idx  # return the idx of the task that missed the ddl

        if time % task.t == 0 and time > 0:  # activate the task
            task.runtime = 0
            task.abs_ddl = time + task.d
            task.active = True
            task.active_time = time
    return -1


# not used
def activate_tasks(tasks, time):
    for task in tasks:
        if time % task.t == 0 and task.active == False:
            task.runtime = 0
            task.abs_ddl = time + task.d
            task.active = True
            task.active_time = time


def run_proc(task_set, policy, p):
    tasks = task_set[:]  # copy the task set just in case

    # initlize the tasks
    for task in tasks:
        task.abs_ddl = task.d
        task.active = True
        task.active_time = 0
        task.runtime = 0

    # initialize next_id
    next_id = -1
    if policy == "FCFS":
        next_id = fcfs(tasks, next_id)
    elif policy == "SJF":
        next_id = sjf(tasks, next_id, p)
    elif policy == "EDF":
        next_id = edf(tasks, next_id, p)
    elif policy == "RM":
        next_id = rm(tasks, next_id, p)
    else:
        print("huh?")


    for timeunit in range(0, total_time_units):
        # update runtime
        if timeunit == 78 or timeunit == 354:
            pass
        for task in tasks:
            if task.idx == next_id:
                task.runtime += 1
                if task.runtime == task.c:
                    task.active = False

        # choose the next task to run
        if policy == "FCFS":
            next_id = fcfs(tasks, next_id)
        elif policy == "SJF":
            next_id = sjf(tasks, next_id, p)
        elif policy == "EDF":
            next_id = edf(tasks, next_id, p)
        elif policy == "RM":
            next_id = rm(tasks, next_id, p)
        else:
            print("huh?")
        #print("now running", next_id)
        '''
        match policy:
            case "FCFS":
                next_id = fcfs(tasks, next_id)
            case "SJF":
                next_id = sjf(tasks, next_id, p)
            case "EDF":
                next_id = edf(tasks, next_id, p)
            case "RM":
                next_id = rm(tasks, next_id, p)
            case _:
                print("huh?")
        '''

        # check ddl miss
        missed_idx = check_ddl_miss(tasks, timeunit)
        if missed_idx != -1:
            return missed_idx

        # activate_tasks(tasks, timeunit)

        # if no task to run
        if next_id == -1:
            continue

    return -1


# main
def run_simulation(policy, p):
    # Convert the string to boolean (preemptive or not)
    p_b = True
    if p == "np":
        p_b = False

    # debugging statement
    # check howmany task sets are done
    count = 0

    for task_set in file_input_data:
        count += 1

        # debugging statement
        if count == 3:
            pass

        line_result = run_proc(task_set, policy, p_b)
        if line_result == -1:
            output_results.append(0)
        else:
            output_results.append(line_result)
        # print(count)


def main():
    args = sys.argv
    #input_file = args[1]
    #policy = args[2]
    #preemptive = args[3]

    input_file = "hw3_test.txt"
    policy = "EDF"
    preemptive = "p"


    initialize_output_folder()
    get_file_input(input_file)

    '''
    Note: 
        the first line in hw2_test.txt is the ddl miss case for fcfs (no matter the p or np)
        the second line is to test the SJF in np
        the third line is to test the EDF in np
        the fourth line is to test RM in p and np
        the fifth line is to test RM in np and p
        the sixth line is to test EDF in p
    '''

    run_simulation(policy, preemptive)
    output_result()


def main_call(policy, preemptive, filename):
    args = sys.argv
    #input_file = args[1]
    #policy = args[2]
    #preemptive = args[3]

    input_file = filename
    #policy = "EDF"
    #preemptive = "p"

    initialize_output_folder()
    get_file_input(input_file)

    run_simulation(policy, preemptive)
    output_result()


'''
if __name__ == '__main__':
    main()
'''
