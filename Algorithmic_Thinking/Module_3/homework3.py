def mystery(array, left, right):

    if left > right:
        return -1

    m = (right + left) / 2

    if array[m] == m:
        return m
    else:
        if array[m] < m:
            return mystery(array, m+1, right)
        else:
            return mystery(array, left, m-1)

print mystery([-2,0,1,3,7,12,15],0,6)
print mystery([0,1,2,3,4], 0, 4)