from prettytable import PrettyTable
import matplotlib.pyplot as plt
from NM import *

weight = [10, 5, 7, 3, 10, 8, 2, 7, 5, 4, 4, 9]
a_count = 15


def do_research(sigma_table, matrix):
    constant_c(sigma_table, matrix)
    constant_d(sigma_table, matrix)
    changing_c_d(sigma_table, matrix)


def changing_c_d(sigma_table, matrix):
    c = 0.5
    d = 0.5
    c_values = []
    d_values = []
    arr_values = []
    while c < 1:
        print(f'c = {c}, d = {d}')
        d_values.append(round(d, 2))
        c_values.append(round(c, 2))
        arr, _, _, _ = get_result(sigma_table, c, d, matrix)
        arr_values.append(arr)
        d -= 0.05
        c += 0.05

    show_graph(c_values, arr_values, 'Значення c')


def constant_c(sigma_table, matrix):
    valid_c = 0.5
    d = 0.05
    d_values = []
    arr_values = []

    while d < 0.5:
        print(f'c = {valid_c}, d = {d}')
        d_values.append(round(d, 2))
        arr, _, _, _ = get_result(sigma_table, valid_c, d, matrix)
        arr_values.append(arr)
        d += 0.05

    show_graph(d_values, arr_values, 'Значення d')


def constant_d(sigma_table, matrix):
    valid_d = 0.49
    c = 0.5
    c_values = []
    arr_values = []

    while c <= 1:
        print(f'c = {c}, d = {valid_d}')
        c_values.append(round(c, 2))
        arr, _, _, _ = get_result(sigma_table, c, valid_d, matrix)
        arr_values.append(arr)
        c += 0.05

    show_graph(c_values, arr_values, 'Значення с')


def show_graph(x_points, y_values, xlabel):
    flattened_values = [item for sublist in y_values if sublist is not None for item in sublist]

    for i, y_points in enumerate(y_values):
        if y_points is not None:
            plt.scatter([x_points[i]] * len(y_points), y_points, color='green')

    plt.xticks(x_points)
    plt.yticks(range(0, max(flattened_values, default=1) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Аналіз впливу параметрів c, d')
    plt.xlabel(xlabel)
    plt.ylabel('Склад ядра')
    plt.show()


def print_matrix(matrix):
    table = PrettyTable()
    table.field_names = [f'{i+1}' for i in range(len(matrix[0]))]

    for row in matrix:
        table.add_row(row)
    print(table)


def get_result(sigma_table, valid_c, valid_d, matrix):
    mx_c, binary_c = get_c(sigma_table, valid_c)
    mx_d, binary_d = get_d(sigma_table, matrix, valid_d)
    mx_result = find_intersection(binary_c, binary_d)
    arr = get_NM(mx_result, a_count)
    return arr, mx_c, mx_d, mx_result


def get_c(sigma_table, valid_c):
    c_matrix = [[0] * a_count for _ in range(a_count)]

    general_w = sum(weight)

    for row_index, row in enumerate(sigma_table):
        for group_index, group in enumerate(row):
            if row_index != group_index:
                w = sum(weight[el] for el in range(len(group)) if group[el] >= 0)
                c = w / general_w
                c_matrix[row_index][group_index] = round(c, 3)
    print('\nМатриця ступеней переваги\n')
    print_matrix(c_matrix)
    binary_c = get_binary_relation(c_matrix, valid_c, 'C')
    return c_matrix, binary_c


def get_d(sigma_table, mx, valid_d):
    d_matrix = [[1] * a_count for _ in range(a_count)]

    for row_index, row in enumerate(sigma_table):
        for group_index, group in enumerate(row):
            first_max = 0
            second_max = 0
            for el in range(len(group)):
                if group[el] < 0:
                    first = weight[el] * (mx[group_index][el]-mx[row_index][el])
                    second = weight[el] * find_delta(el, mx)
                    if first > first_max:
                        first_max = first
                    if second > second_max:
                        second_max = second
            if group_index != row_index:
                if first_max != 0:
                    d = first_max / second_max
                    d_matrix[row_index][group_index] = round(d, 3)
                else:
                    d_matrix[row_index][group_index] = 0

    print('\nМатриця ступеней погіршення\n')
    print_matrix(d_matrix)
    binary_d = get_binary_relation(d_matrix, valid_d, 'D')
    return d_matrix, binary_d


def find_intersection(matrix1, matrix2):
    intersection_matrix = [[0] * len(matrix1[0]) for _ in range(len(matrix1))]

    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            if matrix1[i][j] == 1 and matrix2[i][j] == 1:
                intersection_matrix[i][j] = 1
    print("\nЕлементи, для яких виконуються дві умови:\n")
    print_matrix(intersection_matrix)
    return intersection_matrix


def get_binary_relation(c_matrix, valid_value, relation_type):
    print('\nБінарне відношення\n')
    binary_matrix = [[0] * a_count for _ in range(a_count)]

    for row_index, row in enumerate(c_matrix):
        for group_index, group in enumerate(row):
            if (relation_type == 'C' and c_matrix[row_index][group_index] >= valid_value) or \
                    (relation_type == 'D' and c_matrix[row_index][group_index] <= valid_value):
                binary_matrix[row_index][group_index] = 1

    print_matrix(binary_matrix)

    return binary_matrix


def find_delta(column_index, mx):
    column_values = [row[column_index] for row in mx]
    max_value = max(column_values)
    min_value = min(column_values)
    return max_value - min_value


def get_delta(x, y):
    result = []
    for i in range(len(x)):
        result.append(x[i] - y[i])
    return result


def get_sigma_table(mx):
    sigma_table = []
    # print('\nВектори різниць:\n')
    for i in range(len(mx)):
        row = []
        for j in range(len(mx)):
            delta = get_delta(mx[i], mx[j])
            # print(f'{i+1}-{j+1}:{delta}')
            row.append(get_sigma(delta))
        sigma_table.append(row)

    # print('\nВектори знаків різниць:\n')
    # for i in range(len(sigma_table)):
    #     for j in range(len(sigma_table)):
    #         print(f'{i+1}-{j+1}:{sigma_table[i][j]}')
    return sigma_table


def get_sigma(delta):
    result = []
    for i in range(len(delta)):
        if delta[i] > 0:
            result.append(1)
        elif delta[i] < 0:
            result.append(-1)
        else:
            result.append(0)
    return result
