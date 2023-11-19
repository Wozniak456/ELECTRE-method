from electre1 import *


if __name__ == '__main__':
    a_count = 15  # кількість альтернатив
    mx_str = """ 
 1  3  1  3  2  4  3  4  1  6  4  2 
 6  6  3  8  2  7  7  1  2  10  5  7 
 6  10  1  7  5  10  7  3  3  9  5  4 
 2  8  6  7  10  6  3  7  2  4  6  2 
 4  5  6  8  2  3  8  6  10  2  6  10 
 7  7  6  2  8  10  8  8  2  2  2  5 
 9  9  5  10  5  2  9  8  1  6  5  4 
 7  10  3  7  4  10  2  1  10  5  8  3 
 8  6  5  3  9  8  1  3  7  10  6  4 
 6  10  1  5  9  9  4  10  6  10  4  9 
 1  2  8  3  8  8  1  3  4  8  1  2 
 7  10  4  7  3  3  8  1  4  10  9  1 
 7  9  6  2  9  8  3  4  5  10  2  1 
 9  2  6  5  7  9  2  3  10  1  7  2 
 2  10  5  1  10  7  6  2  2  3  3  10 
"""
    matrix = [[int(number) for number in line.split()] for line in mx_str.split('\n') if line.strip()]

    print_matrix(matrix)
    sigma_table = get_sigma_table(matrix)
    print()
    weight = [10, 5, 7, 3, 10, 8, 2, 7, 5, 4, 4, 9]

    valid_c = 0.652
    valid_d = 0.401

    arr, mx_c, mx_d, mx_result = get_result(sigma_table, valid_c, valid_d, matrix)

    print('\nВнутрішня стійкість: ', check_internal_stability(arr, mx_result))
    print('Зовнішня стійкість: ', check_external_stability(arr, a_count, mx_result))

    with open('Var-5-Возняк.txt', 'w') as file:
        file.write('матриця індексів узгодження C\n')
        for row in mx_c:
            row_str = ' '.join(format(elem, ".3f") for elem in row)
            file.write(f'{row_str}\n')

        file.write('матриця індексів неузгодження D\n')
        for row in mx_d:
            row_str = ' '.join(format(elem, ".3f") for elem in row)
            file.write(f'{row_str}\n')

        file.write('Значення порогів для індексів узгодження та неузгодження c, d\n')
        file.write(f'{valid_c} {valid_d}\n')

        file.write('Відношення для порогових значень c, d:\n')
        for row in mx_result:
            row_str = '\t'.join(map(str, row))
            file.write(f'{row_str}\n')

        file.write('Ядро відношення:\n')
        for el in arr:
            file.write(f'{el} ')

    do_research(sigma_table, matrix)

