# -*- coding: UTF-8 -*-
"""
json parse
@author:kl
@since: 2015-8-1
@change:
"""


class Error(Exception):
    pass


class PyjsonError(Error):
    pass


def load(in_str, no_add=True):
    """Json String TO Json Object """
    if not in_str:
        return None


	SYMBOL = ('{', '}', '[', ']', ':', ',', )
    SPLIT = set(SYMBOL)
    SPACE = set(['\n', '\r', '\t', ' ', ])
    QUOTES = set(['"', "'", ])
    ESCAPE = '\\'
    TAG = (SPLIT, SPACE, QUOTES, ESCAPE)

    token_list = tokenize(in_str, TAG, func=None)
    obj, index = parse(in_str, token_list, 0, SYMBOL)
    if no_add and index < len(token_list):
        undo_list = [get_token(in_str, token) for token in token_list[index:]]
        raise PyjsonError('%s undo list:%s' % (obj, undo_list))
    return obj


def tokenize(in_str, TAG, func=None):
    """ return [ SPLIT->(index,), QUOTES->(index1, index2), VAL->(index1, index2, val<no space>), ...] """
    SPLIT, SPACE, QUOTES, ESCAPE = TAG
    ret_list, length = [], len(in_str)
    index = skip(in_str, length, 0, SPACE)
    while index < length:
        c, _index = in_str[index], index
        if c in SPLIT:
            ret_list.append((_index,))  # SPLIT->(index,)
        elif c in QUOTES:
            index = fstr(in_str, length, index, ESCAPE)
            ret_list.append((_index + 1, index))  # QUOTES->(index1, index2)
        else:
            index, val = fval(in_str, length, index, SPLIT, SPACE)
            val = value(val, (_index, index), func)
            ret_list.append((_index, index, val,))  # VAL->(index1, index2, val<no space>)
            ret_list.append((index,))
        index = skip(in_str, length, index + 1, SPACE)

    return tuple(ret_list)


def parse(in_str, token_list, index, SYMBOL):
    DICT_L, DICT_R, LIST_L, LIST_R, KEY_T, JOIN_T = SYMBOL
    token = token_list[index]
    t_len = len(token)
    ret = None
    if t_len == 3:
        ret = token[2]
    elif t_len == 2:
        ret = in_str[token[0]:token[1]]
    elif t_len == 1:
        char = in_str[token[0]]
        if char == DICT_L:  # `{'key':val,...}`
            ret, index = {}, index + 1
            while not _symbol1(in_str, token_list[index], DICT_R):  # end while `}`
                _assert_key(in_str, token_list[index], ret)  # assert next is `'key'`
                key, index = parse(in_str, token_list, index, SYMBOL)
                _assert_s1(in_str, token_list[index], KEY_T)  # assert next is `:`
                val, index = parse(in_str, token_list, index + 1, SYMBOL)
                _assert_s2(in_str, token_list[index], JOIN_T, DICT_R)  # assert next is `,` or `}`
                ret[key] = val
                if _symbol1(in_str, token_list[index], JOIN_T):  # pass next `,`
                    index += 1
        elif char == LIST_L:  # `[val,...]`
            ret, index = [], index + 1
            while not _symbol1(in_str, token_list[index], LIST_R):  # end while `]`
                val, index = parse(in_str, token_list, index, SYMBOL)
                _assert_s2(in_str, token_list[index], JOIN_T, LIST_R)  # assert next is `,` or `]`
                ret.append(val)
                if _symbol1(in_str, token_list[index], JOIN_T):  # pass next `,`
                    index += 1
        else:
            raise PyjsonError("can not match:%s@%s." % (char, token))
    else:
        raise PyjsonError("can not do:%s" % (token))
    return ret, index + 1


def value(x, index, func):

    def _value(x, index, func):
        try:
            return int(x)
        except ValueError, ex1:
            try:
                return float(x)
            except ValueError, ex2:
                if func:
                    return func(x)
                else:
                    msg = "Error value:%s@%s -> %s,%s." % (x, index, ex1, ex2,)
                    raise PyjsonError(msg)

    if x == 'None':
        return None
    elif x == 'True':
        return True
    elif x == 'False':
        return False
    else:
        return _value(x, index, func)


def get_token(in_str, token):
    t_len = len(token)
    return in_str[token[0]] if t_len == 1 else \
            in_str[token[0]:token[1]] if t_len == 2 else \
            token[2] if t_len == 3 else None


def skip(in_str, length, index, SPACE):
    """ return index of next char not space. """
    while index < length and in_str[index] in SPACE:
        index += 1
    return index


def fstr(in_str, length, index, ESCAPE):
    """ in_str[index] is " or ', return index of next in_str[index] without \\ before it. """
    ci, index = in_str[index], index + 1
    while index < length and in_str[index] != ci:
        index += 2 if in_str[index] == ESCAPE else 1
    return index


def fval(in_str, length, index, SPLIT, SPACE):
    """ in_str[index] is not symbol, return (index of next symbol, val without space). """
    val = []
    while index < length and in_str[index] not in SPLIT:
        if in_str[index] not in SPACE:
            val.append(in_str[index])
        index += 1
    return index, ''.join(val)


def _assert_s1(in_str, token, symbol):
    if not _symbol1(in_str, token, symbol):
        raise PyjsonError("assert fails:%s@%s is %s." %
                          (get_token(in_str, token), token, symbol))


def _symbol1(in_str, token, symbol):
    return len(token) == 1 and in_str[token[0]] == symbol


def _assert_s2(in_str, token, symbol1, symbol2):
    if not _symbol2(in_str, token, symbol1, symbol2):
        raise PyjsonError(
            "assert fails:%s@%s is %s." % (get_token(in_str, token), token,
                                           (symbol1, symbol2)))


def _symbol2(in_str, token, symbol1, symbol2):
    return len(token) == 1 and (in_str[token[0]] == symbol1 or
                                in_str[token[0]] == symbol2)


def _assert_key(in_str, token, rd, must_str=True):
    itoken = get_token(in_str, token)
    if len(token) != 2 and must_str:
        raise PyjsonError("assert fails:%s@%s is not str." % (itoken, token))
    if itoken in rd:
        raise PyjsonError(
            "assert fails:%s@%s is repkey in %s." % (itoken, token, rd))


#===========TEST==========
def _test1():
    t0 = "[34,,56]"
    t1 = "[,]"
    t2 = "[45,]"
    t3 = "['fgh',7656,None,True,False,123.0374,7472e-9,98e12,[],{},]"
    _unittest(load, (False, t0), (False, t1), (True, t2), (True, t3))


def _test2():
    t0 = "{76:554}"
    t1 = "{'a':4,'a':[],}"
    t2 = "{}"
    t3 = "{'fg':556,}"
    _unittest(load, (False, t0), (False, t1), (True, t2), (True, t3))


def _test3():
    t0 = "[34,4.56,],:{"
    t1 = "[ture,]"
    t2 = "    [4.   5,    [    ],   {'a'   : 'b',    }   ]"
    t3 = "{'test':['fgh',7  656,N  one,  Tr  ue,False  ,12  3.03  74,   7472e-9,98  e12,[1,2,'daw\"', [None, True,], {'a0':.5346}]  ,{'a':1,'b':2,'c':3,},]  }"
    _unittest(load, (False, t0), (False, t1), (True, t2), (True, t0, False),
              (True, t3))

##==========TEST UNIT===========
## you must def your Error from Exception


def main(test_pre='_test'):
    globals_dict = globals()
    for k, v in globals_dict.items():
        if k.startswith(test_pre):
            LOG("\n>>%s" % (k,))
            if hasattr(v, '__call__'):
                v()


def _unittest(func, *cases):
    return [_functest(func, *case) for case in cases]


def _functest(func, isPass, *args, **kws):
    result = None
    try:
        LOG('\n%s -> %s(args=%s,kws=%s)' % (isPass, func.func_name, args, kws))
        result = func(*args, **kws)
        LOG('=%s' % (result))
    except Error as ex:
        LOG("%s -> %s:%s" % (isPass, type(ex), ex))
        if isPass:
            raise ex
    else:
        if not isPass:
            raise AssertionError("isPass:%s but no Exception!!!" % (isPass))
    return result


def LOG(msg):
    print msg


if __name__ == '__main__':
    main()
    LOG("\n==========END===========")

