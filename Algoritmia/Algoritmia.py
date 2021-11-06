def canSplit(matrix):
    size = len(matrix[0])
    if size < 2:
        return 0
    for column in range(0,size-1):
        print(f'division in the column: {column}')
        left, right = 0, 0
        for f in matrix:
            if f:
                left += sum(f[:column+1])
                print(f'L:{f[:column+1]}', end=',')
                print(f'R:{f[column+1:]}')
                right += sum(f[column+1:])
            else:
                return 0
        print(f'Left:{left} Right:{right}')
        if left == right:
            return 1
    return 0