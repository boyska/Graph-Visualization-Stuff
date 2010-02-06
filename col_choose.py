#PRE: receives a list of column
#Each column is a tuple (col, node)
#POST: return an "assignment": (col, node), (col, node), (col, node)

def column_choose(avail_col):
    avail_col.sort()
    incoming = set()
    for col in avail_col:
        incoming.add(col[1])
    n_incoming = len(incoming)
    del incoming

    print avail_col
    node1 = avail_col[0][1]
    center = None
    
    res = [avail_col[0]]
    for i in range(1, len(avail_col)):
        if avail_col[i][1] in (x[1] for x in res):
            continue
        res.append(avail_col[i])
        if n_incoming == len(res):
            return res
    else:
        raise ValueError('%s is not a valid column list' % str(avail_col))

    return (avail_col[0], avail_col[center], avail_col[third])

def test_column_choose(avail_col):
    try:
        res = column_choose(avail_col)
    except Exception, e:
        print 'Error calculating'
        print e
        return False
    print avail_col, '=>', res
    if not (res[0][0] < res[1][0] < res[2][0]):
        return False
    if res[0][1] == res[1][1] or res[1][1] == res[2][1] or res[0][1] == res[2][1]:
        return False
    return True

if __name__ == '__main__':
    test1 = [(2,'c'), (3, 'f'), (-2, 'f'), (0, 'e'), (-1, 'e')]
    print test_column_choose(test1)


