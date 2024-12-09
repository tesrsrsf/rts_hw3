import os
import random
import sys

import numpy as np

output_list = []
student_id = ""
n = -1
U = -1
v = -1


def initialize_output_folder():
    dir_name = "output"
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass


def list2str(res):
    result = ""
    for j in res:
        result += str(j)
        result += " "

    return result


def output_to_file(res_list):
    filename_idx = "_" + str(n) + "_" + str(U) + "_" + str(v)
    filename = student_id + filename_idx + ".txt"
    filewriter = open("output/" + filename, "w")
    for j in range(0, len(res_list)):
        line = list2str(res_list[j])
        filewriter.write(line + "\n")
    #print("output finished")
    filewriter.close()
    return filename


def uunifast(n, U):
    vectU = []
    sumU = U
    for i in range(1, n):
        nextSumU = sumU * np.random.rand()**(1 / (n - i))
        vectU.append(sumU - nextSumU)
        sumU = nextSumU
    vectU.append(sumU)  # Assign the remaining utilization to the last task
    return vectU


# For testing
def generate_T():
    T = random.randint(100, 1001)

    return T


def generate_T_C(U):
    T = random.randint(100, 1000)       # correct
    C = int(U * T)                      # correct

    return T, C


def generate_task(n, U, v):
    result = [n, U, v]
    utilities = uunifast(n, U)
    #print(utilities, "sum: ", sum(utilities))
    T = 0
    D = 0   # randomly choose between C and T, no need to consider extreme cases
    C = 0

    for uti in utilities:
        T, C = generate_T_C(uti)
        if v == 0:
            D = T
        elif v == 1:
            if C >= T:
                #print(C, T, "WTF")
                pass
            D = random.randint(min(C, T), T)

        result.append(T)
        result.append(C)
        result.append(D)

    return result


def verify_quickly(res):
    uti = 0
    c = 0
    t = 0
    for i in range(3, len(res) - 2, 3):
        TC = res[i:(i + 2)]
        t = TC[0]
        c = TC[1]
        uti += c / t

    return uti


def main_call(In, IU, Iv):
    global student_id
    global n
    global U
    global v
    global output_list

    student_id = "2022315690"
    n = In
    U = IU
    v = Iv

    initialize_output_folder()
    output_list = []
    for i in range(0, 100):
        output_list.append(generate_task(n, U, v))

    filename = output_to_file(output_list)

    print("task generation completed")
    return filename


'''
if __name__ == '__main__':
    args = sys.argv
    #student_id = args[1]
    #n = int(args[2])
    #U = float(args[3])
    #v = int(args[4])

    
    student_id = "2022315690"
    n = 3
    U = 0.5
    v = 1
    

    initialize_output_folder()
    for i in range(0, 100):
        output_list.append(generate_task(n, U, v))

    output_to_file(output_list)
    
    print(output_list)
    print(verify_quickly(output_list))
'''
