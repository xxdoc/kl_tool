import random
import time
from functools import wraps

def time_me(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        ret = func(*args, **kwargs)
        used = (time.clock() - start) * 1000
        print "%.4f ms"%(used, )
        return ret
    return wrapper

@time_me
def topN_sort(int_list, num):
    if len(int_list) <= num:
        return sorted(int_list)[::-1]
    int_list.sort()
    return int_list[-num:][::-1]

@time_me
def topN_bubble(int_list, num):
    if len(int_list) <= num:
        return sorted(int_list)[::-1]
    ret = []
    for _ in xrange(num):
        max_v = int_list[0]
        for idx, test_v in enumerate(int_list):
            if test_v > max_v:
                int_list[idx] = max_v
                max_v = test_v
        else:
            ret.append(max_v)
    return ret

@time_me
def topN_bubble_fix(int_list, num):
    if len(int_list) <= num:
        return sorted(int_list)[::-1]
    ret = []
    skip_idx = set()
    for _ in xrange(num):
        max_v = int_list[0]
        max_i = 0
        for idx, test_v in enumerate(int_list):
            if test_v > max_v and idx not in skip_idx:
                max_i = idx
                max_v = test_v
        else:
            skip_idx.add(max_i)
            ret.append(max_v)
    return ret

@time_me
def topN_bitmap(int_list, num, item_range):
    if len(int_list) <= num:
        return sorted(int_list)[::-1]
    bitmap = {i:0 for i in xrange(item_range)}
    for j in int_list:
        bitmap[j] = 1

    ret = []
    for idx in xrange(item_range - 1, 0, -1):
        if bitmap[idx]:
            ret.append(idx)
        if len(ret) >= num:
            break
    return ret

def t(int_list, max_n = 10):
    l_len = len(int_list)
    if l_len < max_n:
        return str(int_list)
    return str(int_list[:max_n])[:-1] + ', ... <len:{0}> ...]'.format(l_len)

def test(func, t_num, _int_list, **kwargs):
    int_list = list(_int_list)
    print '{func}({int_list}, {t_num})'.format(func=func.__name__, int_list=t(int_list, 3), t_num=t_num), t( func(int_list, t_num, **kwargs) )

def main():
    item_range = 1000000
    list_large  = random.sample(range(1, item_range), 555555)
    list_middle = random.sample(range(1, item_range), 55555)
    list_small  = random.sample(range(1, item_range), 10)

    for t_num in [5, 10, 20, 50, 100, 500]:
        print '\n test for t_num:{0}'.format(t_num)
        test(topN_sort, t_num, list_middle)
        test(topN_bubble, t_num, list_middle)
        test(topN_bubble_fix, t_num, list_middle)
        test(topN_bitmap, t_num, list_middle, item_range=item_range)

    for t_num in [5, 10, 20, 50, 100, 500]:
        print '\n test for {0}'.format(t_num)
        test(topN_sort, t_num, list_large)
        test(topN_bubble, t_num, list_large)
        test(topN_bubble_fix, t_num, list_large)
        test(topN_bitmap, t_num, list_large, item_range=item_range)

    print 'topN_sort(list_small, 10)', topN_sort(list(list_small), 10)
    print 'topN_bubble(list_small, 10)', topN_bubble(list(list_small), 10)
    print 'topN_bubble_fix(list_small, 10)', topN_bubble_fix(list(list_small), 10)
    print 'topN_bitmap(list_small, 10)', topN_bitmap(list(list_small), 10, item_range=item_range)

if __name__ == '__main__':
    main()