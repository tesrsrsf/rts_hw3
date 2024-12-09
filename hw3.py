import os
import sys
import math

'''
 
                                 _oo8oo_
                                o8888888o
                                88" . "88
                                (| -_- |)
                                0\  =  /0
                              ___/'==='\___
                            .' \\|     |// '.
                           / \\|||  :  |||// \
                          / _||||| -:- |||||_ \
                         |   | \\\  -  /// |   |
                         | \_|  ''\---/''  |_/ |
                         \  .-\__  '-'  __/-.  /
                       ___'. .'  /--.--\  '. .'___
                    ."" '<  '.___\_<|>_/___.'  >' "".
                   | | :  `- \`.:`\ _ /`:.`/ -`  : | |
                   \  \ `-.   \_ __\ /__ _/   .-` /  /
               =====`-.____`.___ \_____/ ___.`____.-`=====
                                 `=---=`
                   佛祖保佑                      永无bug
          Buddha bless us                       let there no bugs
'''

next_index = 1


class task:
    def __init__(self, t, c, d, next_index):
        self.t = t
        self.c = c
        self.d = d
        self.idx = next_index


file_input_data = []
output_results = []

total_time_units = 100000

n = 0
u = 0
v = 0

# true is preemptive, false is non-preemptive
p = True


def initialize_output_folder():  # from hw2
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
    if u > 1:
        pass
    v = int(line_data[2])
    temp = []

    for i in range(3, len(line_data), 3):
        new_task = task(int(line_data[i]), int(line_data[i + 1]), int(line_data[i + 2]), next_index)
        next_index += 1
        temp.append(new_task)
    next_index = 1
    return temp


def get_file_input(filename):  # from hw2
    global file_input_data
    file_input_data = []
    file_reader = open(filename, "r")
    line = file_reader.readline()
    while line != "":
        file_input_data.append(file_process_line(line))
        line = file_reader.readline()

    file_reader.close()


def output_result():  # from hw2, modified
    file_writer = open("./output/2022315690_HW3.txt", "w")
    for idx in output_results:
        file_writer.write(str(idx) + "\n")
    file_writer.close()


# Little tools
# not used
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# not used
def lcm(a, b):
    return a * b // gcd(a, b)


def lcm_t(taskset):
    t_list = [task.t for task in taskset]
    # print(t_list)
    result = t_list[0]
    j = 1
    for temp in t_list[1:]:
        # print(j)
        j += 1
        # print("lcm:", result, "-", temp)
        # result = math.lcm(t_list)
        result = math.lcm(result, temp)

    # print(j)
    return result


# Analysis algorithms
# return 'P'/'F'/'U*'. 'P' and 'F' stands for pass and fail, any response should not include letter 'U'
def EDF_U(taskset):
    result = 'U1'
    total_U = 0

    for single_task in taskset:
        total_U += (single_task.c / single_task.t)

    if total_U <= 1:
        result = 'P'  # + ' ' + str(total_U)
    else:
        result = 'F'  # + ' ' + str(total_U)

    return result


def RM_R(taskset):
    # '''
    taskset_sorted = sorted(taskset, key=lambda task: task.t)

    c_list = []
    t_list = []

    # old_r = -1

    for i in range(len(taskset_sorted)):
        task_item = taskset_sorted[i]
        # calc_list = [task_item.c]

        old_r = task_item.c
        c_list.append(task_item.c)
        t_list.append(task_item.t)

        while True:
            calc_list = [task_item.c]
            for k in range(len(c_list) - 1):
                t = t_list[k]
                c = c_list[k]
                calc_list.append(math.ceil(old_r / t) * c)

            new_r = sum(calc_list)

            if new_r > task_item.t:
                return 'F'

            if new_r == old_r:
                break

            old_r = new_r

    return 'P'
    # '''
    '''
    taskset_sorted = sorted(taskset, key=lambda task: task.t)
    c_list = []
    t_list = []

    old_r = -1

    for i in range(0, len(taskset_sorted)):
        task_item = taskset_sorted[i]
        #calc_list = [task_item.c]
        #c_list.append(task_item.c)
        #t_list.append(task_item.t)
        for j in range(0, i + 1):
            if i == 0:
                r1 = task_item.c
                if r1 > task_item.t:
                    return 'F'
                c_list.append(task_item.c)
                t_list.append(task_item.t)
                break

            if j == 0:
                old_r = task_item.c
                c_list.append(task_item.c)
                t_list.append(task_item.t)
            else:
                calc_list = [task_item.c]
                for k in range(0, len(c_list) - 1):
                    t = t_list[k]
                    c = c_list[k]
                    calc_list.append(math.ceil(old_r/t) * c)
                old_r = sum(calc_list)
                if old_r > task_item.t:
                    return 'F'

    return 'P'
    '''


def DM_R(taskset):
    taskset_sorted = sorted(taskset, key=lambda task: task.d)

    c_list = []
    t_list = []

    # old_r = -1

    for i in range(len(taskset_sorted)):
        task_item = taskset_sorted[i]
        # calc_list = [task_item.c]

        old_r = task_item.c
        c_list.append(task_item.c)
        t_list.append(task_item.t)

        while True:
            calc_list = [task_item.c]
            for k in range(len(c_list) - 1):
                t = t_list[k]
                c = c_list[k]
                calc_list.append(math.ceil(old_r / t) * c)

            new_r = sum(calc_list)

            if new_r > task_item.d:
                return 'F'

            if new_r == old_r:
                break

            old_r = new_r

    return 'P'

    '''
    taskset_sorted = sorted(taskset, key=lambda task: task.d)
    c_list = []
    t_list = []

    old_r = -1

    for i in range(0, len(taskset_sorted)):
        task_item = taskset_sorted[i]
        # calc_list = [task_item.c]
        # c_list.append(task_item.c)
        # t_list.append(task_item.t)
        for j in range(0, i + 1):
            if i == 0:
                r1 = task_item.c
                if r1 > task_item.d:
                    return 'F'
                c_list.append(task_item.c)
                t_list.append(task_item.t)
                break

            if j == 0:
                old_r = task_item.c
                c_list.append(task_item.c)
                t_list.append(task_item.t)
            else:
                calc_list = [task_item.c]
                for k in range(0, len(c_list) - 1):
                    t = t_list[k]
                    c = c_list[k]
                    calc_list.append(math.ceil(old_r / t) * c)
                old_r = sum(calc_list)
                if old_r > task_item.d:
                    return 'F'

    return 'P'
    '''


# not used
def tp_generator(taskset, total_lcm):
    time_points = set()
    l = 1

    for task in taskset:
        # the time points for each task are {Di + k * Ti}
        k = 0
        while True:
            t = task.d + k * task.t
            print("i:", l, "k:", k, "total:", total_lcm)
            if t > total_lcm:  # no need to check further than lcm (since the movements will start repeating)
                break
            time_points.add(t)
            k += 1
        l += 1

    return time_points


# not used
def EDF_D(taskset):
    # find time points
    total_lcm = lcm_t(taskset)
    # print(total_lcm)
    time_points = set()
    # print("----- calculating time points -----")
    l = 1

    '''

    for task in taskset:
        if bp >= task.d:
            max_k = (bp - task.d) // task.t
            for k in range(max_k + 1):
                time_points.add(task.d + k * task.t)
    '''

    #'''
    if u > 1:   # not schedulable
        return 'F'
    for task in taskset:
        # the time points for each task are {Di + k * Ti}
        k = 0
        while True:
            t = task.d + k * task.t
            print("i:", l, "k:", k, "total:", total_lcm)
            if t > total_lcm:  # no need to check further than lcm (since the movements will start repeating)
                break
            time_points.add(t)
            k += 1
        l += 1
    #'''

    # remove duplicated time points and sort
    time_points = sorted(time_points)

    # calculate h(t) for every time point
    # print("----- calculating h(t) -----")
    for t in time_points:
        ht = 0

        # the sigma operation for h(t)
        ht_calc_list = []

        for task in taskset:
            if t >= task.d:
                ht_calc_list.append(task.c * math.ceil((t - task.d) / task.t))

        ht = sum(ht_calc_list)

        # if any h(t) > t happens, return 'F'
        if ht > t:
            return 'F'

    # passed all h(t) <= t
    return 'P'


def EDF_D2(taskset):
    def calc_demand(intv):
        total_demand = 0
        for task in taskset:
            total_demand += (intv // task.t) * task.c
            if (intv % task.t) >= task.d:
                total_demand += task.c
        return total_demand

    crit_pts = set()
    for task in taskset:
        for k in range(1, (max(task.d for task in taskset) // task.t) + 2):
            crit_pts.add(k * task.t + task.d)

    crit_pts = sorted(crit_pts)

    for L in crit_pts:
        if L > 0:
            demand = calc_demand(L)
            if demand > L:
                return 'F'

    return 'P'



# main
def run_analysis(policy, mode):
    global output_results
    global file_input_data
    count = 1
    output_results = []
    for taskset in file_input_data:
        # print(count)
        if u == 0:
            output_results.append('P')
            continue

        '''
        if u > 1:
            output_results.append('F')
            continue
        '''

        # debugging
        if count == 5:
            pass
        if count == 6:
            pass

        if policy == "EDF" and mode == "U":
            output_results.append(EDF_U(taskset))
        elif policy == "RM" and mode == "R":
            output_results.append(RM_R(taskset))
        elif policy == "DM" and mode == "R":
            output_results.append(DM_R(taskset))
        elif policy == "EDF" and mode == "D":
            output_results.append(EDF_D2(taskset))
        count += 1


def main():
    args = sys.argv
    '''
    input_file = args[1]
    policy = args[2]
    mode = args[3]
    '''

    input_file = 'hw3_test.txt'
    policy = 'EDF'
    mode = 'U'

    initialize_output_folder()
    get_file_input(input_file)

    '''
    Note: 
        上有佛祖
        Buddha above
    '''

    run_analysis(policy, mode)
    output_result()


# used when writing reports
def main_call(policy, preemptive, filename):
    args = sys.argv
    # input_file = args[1]
    # policy = args[2]
    # preemptive = args[3]

    input_file = filename
    # policy = "EDF"
    # preemptive = "p"

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

    run_analysis(policy, preemptive)
    output_result()


'''
if __name__ == '__main__':
    main()
'''
