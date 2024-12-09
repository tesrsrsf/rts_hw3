import random
import time

import numpy

import hw1
import hw2
import hw3

hw2_result = []
hw3_result = []


def read_hw2_result():
    result = []
    file_reader = open("output/2022315690_HW2.txt", "r")
    line = file_reader.readline()

    while line != "":
        result.append(int(line.strip()))
        line = file_reader.readline()
    file_reader.close()

    return result


def read_hw3_result():
    result = []
    file_reader = open("output/2022315690_HW3.txt", "r")
    line = file_reader.readline()

    while line != "":
        result.append(line.strip())
        line = file_reader.readline()
    file_reader.close()

    return result


def get_pass_ratio(mode):
    result = -1
    if mode == 2:
        pass_count = 0
        for res in hw2_result:
            if res == 0:
                pass_count += 1
        result = (pass_count / len(hw2_result)) * 100
    elif mode == 3:
        pass_count = 0
        for res in hw3_result:
            if res == "P":
                pass_count += 1
        result = (pass_count / len(hw3_result)) * 100

    return result


def main():
    global hw2_result
    global hw3_result

    print("running hw2")
    hw2.main_call("SJF", "np")
    print("running hw3")
    hw3.main_call("DM", "R")

    hw2_result = read_hw2_result()
    hw3_result = read_hw3_result()

    print(hw2_result)
    print(get_pass_ratio(2))
    print(hw3_result)
    print(get_pass_ratio(3))


def generate_n_list():
    size = 20
    min_v = 1
    max_v = 10
    ttl = 100
    result = []

    while True:
        numbers = numpy.random.multinomial(ttl, [1/size]*size)

        if (numbers >= min_v).all() and (numbers <= max_v).all():
            return list(numbers)


def test_hw2():
    global hw2_result

    print("running hw2")

    u_increment = 0.08
    u = 0
    v = 1  # v switch between 0 and 1

    percentage = 0

    n_list = generate_n_list()
    print(n_list)
    idx = 0

    #while u <= u_max:
    while idx < len(n_list):
        start_time = time.time()
        n = n_list[idx]
        filename = hw1.main_call(n, u, v)
        hw2.main_call("FCFS", "p", "output/" + filename)
        hw2_result = read_hw2_result()

        print("utilization:", u, "ratio:", get_pass_ratio(2))
        end_time = time.time()

        time_cost = end_time - start_time
        print(f"time elapsed: {time_cost:.2f} seconds")

        u += u_increment
        idx += 1


def test_hw3():
    global hw3_result

    print("running hw3")

    u_increment = 0.08
    u = 0
    u_max = 1.6
    v = 0  # v switch between 0 and 1

    percentage = 0
    n_list = generate_n_list()
    print(n_list)
    idx = 0

    while idx < len(n_list):
        start_time = time.time()
        n = n_list[idx]
        filename = hw1.main_call(n, u, v)
        print("utilization:", u)
        hw3.main_call("EDF", "U", "output/" + filename)
        print("analysis complete")
        hw3_result = read_hw3_result()

        print("ratio:", get_pass_ratio(3))
        end_time = time.time()

        time_cost = end_time - start_time
        print(f"time elapsed: {time_cost:.2f} seconds")

        u += u_increment
        idx += 1


if __name__ == '__main__':
    # main()
    test_hw2()
    #test_hw3()
