import numpy as np
# import numpy.core._dtype_ctypes

def q1_coeff(cost_list, f_list = (0.5, 0.5, 0.5, 0.5)):

    coeff_list = np.zeros(6)

    coeff_list[0] = -((cost_list[0]*f_list[0]) + (cost_list[1]*f_list[1]))
    coeff_list[1] = -cost_list[0]
    coeff_list[2] = -cost_list[1]
    coeff_list[3] = -((cost_list[2]*f_list[2]) + (cost_list[3]*f_list[3]))
    coeff_list[4] = -cost_list[2]
    coeff_list[5] = -cost_list[3]


    return coeff_list

cost_list = [8, 4, 4, 16]
# print("coeffs:", q1_coeff(cost_list))

def q1(coeff_list):
    q1 = np.zeros((6,6))
    for i in range(len(coeff_list)):
        q1[i][i] = coeff_list[i]

    return q1

coeff_list = q1_coeff(cost_list)

# print(q1(coeff_list))


def q2():
    q2 = np.zeros((6,6))
    for i in range(6):
        for j in range(i, 6):
            if i == j:
                q2[i][j] = -1
            else:
                q2[i][j] = 2

    return 60*q2

# lembda = 18
# # print(q2(lembda))
#
# q1 = q1(coeff_list)
# q2 = q2(lembda)


def q(q1, q2):
    return q1 + q2

# q = q(q1, q2)
# print(q)