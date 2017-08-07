#-*- coding: utf-8 -*-
import re

ALL_ERROR = Exception

class Error(Exception):
    pass

class NotMatchError(Error):
    def __init__(self, index, msg, obj=None):
        super(NotMatchError, self).__init__(msg)
        self._letx = obj
        self._index = index

class ListNotMatchError(NotMatchError):
    def __init__(self, index, msg, tag_list, ex_list, obj=None):
        super(ListNotMatchError, self).__init__(index, msg, obj)
        self.__dict__.update(dict(zip(tag_list, ex_list)))
        self._index = index
        max_item = max(ex_list, key=lambda i:i._index)
        self._ex = {tag_list[i]:item for (i,item) in enumerate(ex_list) if item._index==max_item._index}

    def __str__(self):
        return '%s >> [ %s ]' % (self.message, ','.join(['<%s> :%s'%(key,item) for (key, item) in self._ex.items()]))


def LOG(msg, handle=None):
    print msg
    if handle:
        handle.write(msg+'\n')
        handle.flush()

def E(e):
    try:
        return '%s:%r' % (e.__class__.__name__, e)
    except ALL_ERROR as ex:
        return '%s(%s)' % ('cannot get ex.msg!', E(ex))


#===============================================================
#========================== MAIN LETX ==========================
#===============================================================

def letx(_sdic):
    def add_tag(nk, env, obj):
        assert nk not in env or env[nk] is None, 'comp_letx add_tag:mutil tag %s in %s.' % (nk, env)
        env[nk] = obj

    def comp_letx(s, fdic, env):
        def find_tag(tag_in, env_in=env):
            assert tag_in in env_in, 'comp_letx find_tag:can not find(%s) in %s.' % (tag_in, env_in)

            def _pkg_parse(index_in, str_in, str_len):
                assert env_in[tag_in], 'comp_letx _pkg_parse:empty value (%s) in %s.' % (tag_in, env_in)
                parse_func, pkg, _ = env_in[tag_in]
                index, ret_tmp = parse_func(index_in, str_in, str_len)
                ret = pkg(ret_tmp)
                return index, ret
            _pkg_parse.func_name = 'letx %s' % (tag_in, )
            return _pkg_parse

        assert isinstance(s, dict) and len(s)==1, 'comp_letx item:%s must dict and len==1.' % (s, )
        for k, v in s.items():
            assert IS_TAG(k) and '.' not in k, 'comp_letx tag dict item:%s must tag(`.` not in it).' % (k, )
            assert isinstance(v, tuple) and len(v)==2, 'comp_letx tag dict item:%s must tuple and len==2.' % (v, )
            assert hasattr(v[1], '__call__'), 'comp_letx tag dict item:%s[1] must callable.' % (v, )
            main_tag, letx_list, pkg = k[1:-1], v[0], v[1]
            letx_list = [letx_list,] if not isinstance(letx_list, list) else letx_list
            tag_list = []
            for i,item in enumerate(letx_list):
                fix_tag = '%s.%s' % (main_tag, i)
                tag, parse_func = comp_tag(item, fdic, fix_tag, env, find_tag)
                if tag==fix_tag:
                    add_tag(tag, env, (parse_func, DEFAULT_PKG, item))
                tag_list.append(tag)

            func_obj = base_list((main_tag, tag_list), find_tag)
            add_tag(main_tag, env, (func_obj, pkg, letx_list))
            return find_tag(main_tag)

    def comp_tag(s, fdic, fix_tag, env, find_tag):
        if hasattr(s, '__call__'):
            return fix_tag, s
        elif isinstance(s, (str, unicode, tuple)):
            return comp_tag({'><':s}, fdic, fix_tag, env, find_tag)
        elif isinstance(s, dict):
            assert len(s)==1, 'comp_tag tag|func dict item:%s must len==1.' % (s, )
            for k,v in s.items():
                if IS_FUN(k):
                    assert k in fdic, 'comp_tag func dict item:%s must in fdic:%s.' % (k, fdic)
                    return fix_tag, fdic[k](v, find_tag)
                elif IS_TAG(k):
                    tmp_func = comp_letx(s, fdic, env)
                    return k[1:-1], tmp_func
        else:
            assert False, 'comp_tag item:%s not support.' % (s, )

    def pre_env(s, fix=None):
        def setkey(env, key, val=None):
            if key in env:
                raise TypeError('mutil tag in main_tag:%s' % (s, ))
            else:
                env[key] = val

        env = {}
        if isinstance(s, dict) and len(s)==1:
            for k, ut in s.items():
                if IS_TAG(k):
                    setkey(env, k[1:-1])
                    v, _ = ut
                    v = [v,] if not isinstance(v, list) else v
                    for i,t in enumerate(v):
                        env.update(pre_env(t, '%s_%s_' % (k[1:-1], i)))
                elif fix:
                    setkey(env, fix)
        elif fix:
            setkey(env, fix)
        return env

    assert '<_>' in _sdic and isinstance(_sdic['<_>'], tuple) and \
            len(_sdic['<_>'])==2 and isinstance(_sdic['<_>'][0], list) and \
            hasattr(_sdic['<_>'][1], '__call__'), \
            'input:%s must as {"<_>":([...], lambda x: x)}.' % (_sdic, )
    func_dict = {k:v for k,v in _sdic.items() if IS_FUN(k)}
    main_tag = {'<_>':_sdic['<_>']}
    env = pre_env(main_tag)
    _self = comp_letx(main_tag, func_dict, env)

    return _self

#===============================================================
#========================== HELP FUNC ==========================
#===============================================================

IS_TAG = lambda  k,sa='<',sb='>': len(k)>=3 and k[0]==sa and k[-1]==sb
IS_FUN = lambda  k,sa='>',sb='<': len(k)>=2 and k[0]==sa and k[-1]==sb
IS_REGEXP = lambda  k,sa='</',sb='/>': len(k)>=4 and k[:2]==sa and k[-2:]==sb

def DEFAULT_PKG(x):
    return x

def SKIP_SPACE(si, ss, sslen, B={'\n':1, '\r':1, '\t':1, ' ':1}):
    while si<sslen and ss[si] in B:
        si += 1
    return si

def _SPLIT_REG(s, sa='<', sb='>'):
    assert isinstance(s, basestring) and s, '_SPLIT_REG:`%s` is not basestring.' % (s, )
    ret, ib, ia = [], 0, s.find(sa)
    while ia>=0:
        if ia>ib:
            ret.append(s[ib:ia])
        _ia, ib = ia, s.find(sb, ia)+1
        ia = s.find(sa, ia+1)
        assert ia<0 or ia>=ib>_ia, '_SPLIT_REG:`%s` <> not match.' % (s, )
        ret.append(s[_ia:ib])
        if ia<0 and s[ib:]:
            assert s.find(sb, ib)<0, '_SPLIT_REG:`%s` <> not match at end.' % (s, )
            ret.append(s[ib:])

    if not ret:
        ret.append(s)

    return tuple([i.strip() for i in ret if i.strip()])

def get_mark(str_in, symbol=('<', '>', ' ', '=')):
    T1, T2, SP, KV = symbol
    i_tag = _skip(str_in, 1)
    attr = {}
    i_attr_start, i_attr_end = str_in.find(SP, i_tag), len(str_in) - 1
    if i_tag<i_attr_start<i_attr_end:
        _tag = str_in[i_tag:i_attr_start].strip()
        str_attr = str_in[i_attr_start+1:i_attr_end].strip()
        if str_attr:
            attr = get_attr(str_attr, SP, KV)
    else:
        _tag = str_in[i_tag:i_attr_end].strip()

    return _tag, attr

def get_attr(str_in, SP, KV, index=0):
    ret_obj = {}
    ll = len(str_in)
    while index < ll-1:
        ks_list, vs, index = get_kv(str_in, index, ll, SP, KV)
        for ks in ks_list:
            ret_obj[ks] = vs
    return ret_obj

def get_kv(str_in, index, ll, SP, KV):
    ks_list = []
    ks, index = get_block(str_in, index, ll, SP, KV)
    if ks:
        ks_list.append(ks)
    vs, index = get_block(str_in, index+1, ll, SP, KV) if index<ll and str_in[index] == KV else (ks, index)
    while index<ll and str_in[index] == KV:
        if vs:
            ks_list.append(vs)
        vs, index = get_block(str_in, index+1, ll, SP, KV)
    return (ks_list, vs, index)

def get_block(str_in, index, ll, SP, KV, T="\\", STR={'"':1, "'":1, }):
    index = _skip(str_in, index)
    while str_in[index] == KV and index<ll-1:
        index = _skip(str_in, index+1)
    if index>=ll:
        return (None, ll)
    oi, tc, si, ki = index, str_in[index], str_in.find(SP, index), str_in.find(KV, index)
    if tc in STR:
        while not str_in[index+1] == tc:
            index += 2 if  str_in[index] == T else 1
        ret_str, index = str_in[oi+1:index+1], index+2
    elif index<si and (si<ki or ki<0):
        ret_str, index = str_in[oi:si], si
    elif index<ki and ( si>ki or si<0):
        ret_str, index = str_in[oi:ki], ki
    else:
        ret_str, index = str_in[index:], ll
    return (ret_str, index)

def _skip(str_in, index, B={' ':1, '\r':1, '\n':1, '\t':1, }):
    while str_in[index] in B:
        index += 1
    return index

#===============================================================
#========================= MATCH FUNC ==========================
#===============================================================
class _base(object):
    TestFalse = object()
    debug = False

    def test(self, index, s, sl):
        try:
            index, val = self.__call__(index, s, sl)
            return index, val
        except NotMatchError as ex:
            msg = '%s test NotMatchError:%r @%d<`%s`>' % (self, ex, index, s[index-5:index+5])
            return index, self.TestFalse

    def log(self, msg, handle=None):
        if self.debug and msg:
            print msg
            if handle:
                handle.write(msg+'\n')
                handle.flush()

    def __call__(self, index, s, sl):
        assert index < sl, 'base_list index:%s out of max_len:%s.'% (index, sl)
        return None, index

    def __repr__(self):
        return '<%s at 0x%08x>' % (str(self), id(self))

    def __str__(self):
        return 'callable letx %s:%s' % (str(self.__class__).split("'")[1], getattr(self, '__tag__', 'unknown'))

class base_list(_base):
    def __init__(self, args_tuple, find_tag):
        main_tag, tag_list = args_tuple
        assert main_tag and isinstance(tag_list, (tuple, list)), \
                'base_list `%s` and `%s` must tuple or list.' % (main_tag, tag_list)

        self.func_list = [find_tag(tag) for tag in tag_list]
        self.__tag__ = '<%s>`%s`' % (main_tag, ','.join(tag_list))
        self.main_tag, self.tag_list = main_tag, tag_list

    def __call__(self, index, s, sl):
        _, index = super(self.__class__, self).__call__(index, s, sl)

        if len(self.func_list)==1:
            index, ret = self.func_list[0](index, s, sl)
            return index, ret
        else:
            ex_list = []
            for _, func in enumerate(self.func_list):
                try:
                    index, ret = func(index, s, sl)
                    return index, ret
                except NotMatchError as ex:
                    ex_list.append(ex)
            msg = '%s cannot match @%s<`%s`>.' % (str(self), index, s[index-5:index+5])
            raise ListNotMatchError(index, msg, self.tag_list, ex_list, self)

class base_reg(_base):
    def __init__(self, args_tuple_or_str, find_tag):
        args_tuple = _SPLIT_REG(args_tuple_or_str) if isinstance(args_tuple_or_str, basestring) else \
                            args_tuple_or_str
        assert args_tuple and isinstance(args_tuple, tuple), 'base_reg `%s` must tuple.' % (args_tuple, )
        for idx, item in enumerate(args_tuple):
            assert isinstance(item, (str, unicode)), 'base_reg idx %d:`%s` must str or unicode.' % (idx, item)

        tag_split = lambda i:[tag for tag in i[1:-1].split('|') if tag]
        tag_func = lambda i: \
            (re.compile(i[2:-2]), i[2:-2]) if IS_REGEXP(i) else \
            (base_list((i[1:-1], tag_split(i)), find_tag), None, None) if IS_TAG(i) and '|' in i else \
            (find_tag(i[1:-1]), None, None) if IS_TAG(i) else (i,)

        self.__tag__ = ''.join(args_tuple)
        self.func_list = [tag_func(item) for item in args_tuple if item]
        self.args_tuple = args_tuple

    def __call__(self, index, s, sl):
        _, index = super(self.__class__, self).__call__(index, s, sl)

        ret = []
        for item in self.func_list:
            tmp = None
            index = SKIP_SPACE(index, s, sl)
            f_len = len(item)
            if f_len==1:
                len_i, tmp_i = len(item[0]), item[0]
                tmp_str = s[index:index+len_i]
                if not tmp_str == tmp_i:
                    msg = 'base_reg str %s not math @[%s:%s]<`%s`>.'% (tmp_i, index, index+len_i, tmp_str)
                    raise NotMatchError(index, msg, self)
                else:
                    index += len_i
                    msg = 'base_reg str `%s` >>>%s<<< match @%s<`%s`>.'% (str(self), tmp_str, index, s[index-5:index+5])
                    self.log(msg)
            elif f_len==2:
                reg_tmp, reg_i = item[0].match(s[index:]), item[1]
                tmp = reg_tmp.group() if reg_tmp else None
                if not tmp :
                    msg = 'base_reg reg_exp %s not math @%s<`%s`>.'% (reg_i, index, s[index-5:index+5])
                    raise NotMatchError(index, msg, self)
                else:
                    index += len(tmp)
                    ret.append(tmp)
                    msg = 'base_reg reg_exp `%s` >>>%s<<< match @%s<`%s`>.'% (str(self), tmp, index, s[index-5:index+5])
                    self.log(msg)
            elif f_len==3:
                index, tmp = item[0](index, s, sl)
                ret.append(tmp)
                msg = 'base_reg tag `%s` >>>%s<<< match @%s<`%s`>.'% (str(self), tmp, index, s[index-5:index+5])
                self.log(msg)
        return index, tuple(ret)




class base_join(_base):
    def __init__(self, args_tuple, find_tag):
        assert isinstance(args_tuple, tuple) and len(args_tuple)==4, \
                'base_join %s must tuple(start, match, split, end).' % (args_tuple, )

        self.func_tuple = [base_reg(item, find_tag) for item in args_tuple]
        self.__tag__ = '%s%s%s...%s' % args_tuple

    def __call__(self, index, s, sl):
        _, index = super(self.__class__, self).__call__(index, s, sl)

        start, match, split, end = self.func_tuple
        T = lambda x: x is self.TestFalse
        b2s = lambda t: '>>>%s<<<' % (t,) if not T(t) else 'not'
        def get_msg(tag, item, t):
            msg = 'base_join %s `%s` %s math @%s<`%s`>.'% (tag, str(item), b2s(t), index, s[index-5:index+5])
            self.log(msg) if not T(t) else None
            return msg

        ret = []
        index, is_start = start.test(index, s, sl)
        msg = get_msg('start', start, is_start)
        if T(is_start):
            raise NotMatchError(index, msg, self)

        index, is_end = end.test(index, s, sl)
        while T(is_end):
            index, tmp = match(index, s, sl)
            msg = get_msg('match', match, tmp)
            if T(tmp):
                raise NotMatchError(index, msg, self)

            ret.append(tmp)
            index, is_split = split.test(index, s, sl)
            msg = get_msg('split', split, is_split)
            index, is_end = end.test(index, s, sl)
            msg = get_msg('end', end, is_end)
            if not T(is_end):
                break
            if T(is_split):
                raise NotMatchError(index, msg, self)



        return index, tuple(ret)

#===============================================================
#========================== TEST FUNC ==========================
#===============================================================

README = u"""
语法描述为
{<tag>:([tag_item1, tag_item2,...], pkg=lambda x:...)} 依次尝试tag_item,然后pkg结果，tag_item只有一个时，可简写 {<tag>:(tag_item, pkg)}
example
dict{
    <_>: ##  main_tag为<_>, tag中不允许有`.`
        ( [{<tag1>: (sub_tag_items, lambda x:...)}, ## 每一个tag 都为全局变量 find_tag('<tag‘>') 可获取此tag的解析函数
           {<tag2>: ({>func<:agrs}, lambda x:...)}, ## 表示调用函数`func`获取结果
           {<tag3>: (agrs, lambda x:...)}, ## func为base_func时可以直接写参数 等同于{<tag3>: ({><:agrs}, lambda x:...)}
           {>func<:agrs}, ## tag可以匿名(补全为上级tag_index_)，等同于{<上级tag_index_>: ({>func<:agrs}, lambda x:x)}
           (agrs), ## 等同于 {<上级tag.index>: ({><:agrs}, lambda x:x)}
           callable_obj, ## callable_obj 参数为(_index当前索引, s原字符串, sl原字符串长度)的可调用对象，匹配则返回结果为 (index下一个带解析处索引,ret获取到的结果)，不匹配raise NotMatchError
            ],
          pkg lambda x:...`) ## 处理tag返回结果的函数
    ><:base_func, ##  base_func为><
    >func<:func, ## func 接受两个参数 (args,find_tag)；返回参数为(_index当前索引, s原字符串, sl原字符串长度)的可调用对象，匹配则返回结果为 (index下一个带解析处索引,ret获取到的结果)，不匹配raise NotMatchError
}
"""

def fstr(QUOTES, ESCAPE = '\\'): ##i[si] is " or ', return index of next i[si] without \ before it
    QUOTES = QUOTES.strip()
    def _fstr(index, s, sl):
        if s[index]!=QUOTES:
            msg = 'fstr not start s[%s:]<`%s`>,`%s`.'% (index, s[index], QUOTES)
            raise NotMatchError(index, msg, _fstr)
        _index = index+1
        while _index<sl and s[_index] != QUOTES:
            _index += 2 if s[_index]==ESCAPE else 1
        if s[_index] != QUOTES:
            msg = 'fstr not end s[%s:]<`%s`>,`%s`.'% (index, s[index], QUOTES)
            raise NotMatchError(__index, msg, _fstr)
        return _index+1, s[index+1:_index]

    return _fstr

def ftoken(SPLIT, SPACE):
    def _ftoken(index, s, sl):
        while s[index] in SPACE:
            index += 1
        if s[index] in SPLIT:
            msg = 'ftoken not start s[%s:]<`%s`>,`%s`.'% (index, s[index-5:index+5], s[index])
            raise NotMatchError(index, msg, _ftoken)
        val = []
        while index < sl and s[index] not in SPLIT:
            if s[index] not in SPACE:
                val.append(s[index])
            index += 1
        return index, ''.join(val)
    return _ftoken

sdic_json = {
    '<_>':([
            { '<str>':([fstr('"'),
                        fstr("'"),], lambda x: x) },
            { '<None>':("None", lambda x: None) },
            { '<True>':("True", lambda x: True) },
            { '<False>':("False", lambda x: False) },
            { '<num>':(r"</\d*/>", lambda x: int(x[0]) ) },
            {'<list>':({'>join<':("[", "<_>", ",", "]")}, lambda x: [i[0] for i in x]) },
            {'<list2>':({'>join<':("[", "<_>", ",,", "]")}, lambda x: [i[0] for i in x]) },
            {'<dict>':({'>join<':("{", "<str|num|token>:<_>", ",", "}")}, lambda x: {k:v for k,v in x}) },
            {'<token>':(ftoken(SPLIT={'{': 1, '}': 1, '[': 1, ']': 1, ':': 1, ',': 1}, SPACE={' ':1,'\r':1,'\n':1,'\t':1}), lambda x: x)}
        ], lambda x: x),
    '><':base_reg,
    '>join<':base_join, }

ljson = lambda s: letx(sdic_json)(0, s, len(s))[1]
test = """  {self:this,  1234 :{'adawe':[{9:99,},4  ,"5",6  ,'7']}  ,2:987,3:[1,2,3],4:{9:10}  ,5:6}"""
print 'str--', test
print 'ret--%s' % (ljson(test), )
ljson = ljson

load = ljson
#===========TEST==========
def _test1():
    t0 = "[34,,56]"
    t1 = "{'test':123, [1,2,3]:'error here.'}"
    t2 = "[45,]"
    t3 = "['fgh',7656,None,True,False,123,7472,98,[],{},]"
    _unittest(load,(True, t0),(False, t1),(True,t2),(True,t3))

def _test2():
    t0 = "{76:554}"
    t1 = "{'a':4,'a':[],}"
    t2 = "{}"
    t3 = "{'fg':556,}"
    _unittest(load,(True, t0),(True, t1),(True,t2),(True,t3))

def _test3():
    t0 = "[34,4,]"
    t1 = "[ture,]"
    t2 = "    [4.   5,    [    ],   {'a'   : 'b',    }   ]"
    t3 = "   ['fgh',7656,None,  True,False  ,123,   7472,[]  ,{},]  "
    _unittest(load,(True, t0),(True, t1),(True,t0),(True,t3))

##==========TEST UNIT===========
## you must def your Error from Exception


def main(test_pre='_test'):
    globals_dict = globals()
    for k, v in globals_dict.items():
        if k.startswith(test_pre):
            LOG("\n\n>>%s" % (k,))
            if hasattr(v, '__call__'):
                v()

def _unittest(func, *cases):
    return [_functest(func, *case) for case in cases]

def _functest(func, isPass, *args, **kws):
    result = None
    try:
        LOG('\n%s -> %s(args=%s,kws=%s)' %(isPass, func.func_name, args, kws))
        result = func(*args, **kws)
        LOG('=%s' %(result ))
    except Error as ex:
        LOG("%s -> %s:%s" %(isPass, type(ex), ex))
        if isPass:
            raise ex
    else:
        if not isPass:
            raise AssertionError("isPass:%s but no Exception!!!"%(isPass))
    return result


if __name__ == '__main__':
    main()
    LOG("\n==========END===========")
