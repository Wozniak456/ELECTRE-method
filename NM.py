a_count = 15


def get_NM(matrix, size):
    is_relation_cyclic = check_acyclic(matrix)
    if not is_relation_cyclic:
        print('\nS')
        s = get_S_NM(matrix, size)
        print('\nQ')
        q = get_Q_NM(s, matrix, size)
        print('\nЯдро:')
        print(q[len(q)-1])
        return q[len(q)-1]
    else:
        print('not acyclic')


def get_upper_contour_set(matrix, size, node):
    up_set = set()
    for i in range(size):
        if matrix[i][node] == 1:
            up_set.add(i)
    return up_set


def get_S_NM(matrix, size):
    S = []
    up_sets = []
    for i in range(size):
        s = get_upper_contour_set(matrix, size, i)
        up_sets.append(s)
    S0 = []
    for i in range(size):
        if len(up_sets[i]) == 0:
            S0.append(i)
    print('S0:', S0)
    S.append(S0)
    count_s = 1
    while S[-1] != list(range(size)):
        Si = []
        for i in range(size):
            if up_sets[i].issubset(S[-1]):
                Si.append(i)
        print('S{}: {}'.format(count_s, Si))
        S.append(Si)
        count_s += 1
    return S


def get_Q_NM(S, matrix, size):
    Q = [S[0]]
    print('Q0: {}'.format(Q[0]))
    up_sets = []
    for i in range(size):
        s = get_upper_contour_set(matrix, size, i)
        up_sets.append(s)
    for i in range(1, len(S)):
        Q.append(Q[-1].copy())

        dif = list(set(S[i]) - set(S[i - 1]))
        for j in dif:
            if len(set(up_sets[j]).intersection(Q[i - 1])) == 0:
                Q[i].append(j)
        print('Q{}: {}'.format(i, Q[i]))

    return Q


def check_internal_stability(arr, matrix):
    for row in arr:
        for col in arr:
            if matrix[row][col] == 1:
                return False
    return True


def check_external_stability(arr, size, matrix):
    for col in range(size):
        if (col in arr):
            continue
        res = False
        for row in arr:
            if matrix[row][col] == 1:
                res = True
                break
        if not res:
            return False
    return True


def check_acyclic(matrix):
    used = []
    for node in range(a_count):
        if used.count(node) == 0:
            if dfs(used, [], node, matrix):
                return True
    return False


def dfs(used, checked, row, matrix):
    checked.append(row)
    for col in range(a_count):
        if matrix[row][col] == 0:
            continue
        if matrix[row][col] == 1 and checked.count(col) == 0:
            if dfs(used, checked, col, matrix):
                return True
        else:
            return True
    checked.remove(row)
    used.append(row)
    return False
