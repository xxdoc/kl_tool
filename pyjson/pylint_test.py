#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Administrator
#
# Created:
# Copyright:   (c) Administrator
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from collections import namedtuple
import sys
import _ast
import tokenize
import astroid
from astroid import nodes, Module

class CONF:
    no_redef_func = False
    no_undoc_func = False

Confidence = namedtuple('Confidence', ['name', 'description'])
# Warning Certainties
HIGH = Confidence('HIGH', 'No false positive possible.')
INFERENCE = Confidence('INFERENCE', 'Warning based on inference result.')
INFERENCE_FAILURE = Confidence('INFERENCE_FAILURE',
                               'Warning based on inference with failures.')
UNDEFINED = Confidence('UNDEFINED',
                       'Warning without any associated confidence level.')
CONFIDENCE_LEVELS = [HIGH, INFERENCE, INFERENCE_FAILURE, UNDEFINED]

GLOBAL_ENV = {'str':str, 'int':int, 'long':long, 'basestring':basestring, 'unicode':unicode, 'float':float, 'bool':bool,
            'buffer':buffer, 'bytearray':bytearray, 'bytes':bytes, 'memoryview':memoryview,'file':file,
            'type':type, 'object':object, 'dict':dict, 'tuple':tuple, 'list':list, 'set':set, 'slice':slice,
             'classmethod':classmethod, 'property':property, 'reversed':reversed, 'staticmethod':staticmethod,
             'super':super, 'enumerate':enumerate, 'complex':complex, 'frozenset':frozenset, 'xrange':xrange,
            }

def MSG(args, info, confidence):
    msg_str = '%s %s %s obj(%s) line:%d col_offset:%d' % args
    msg = '[%s] %s -> %s.' % (confidence.name, msg_str, info)
    print msg

#================parse tool=========================
def parse_atom(str_in, ln, index, start, allow):
    test_char = str_in[index]
    if not (test_char in start or test_char.isalpha()):
        return index, ''
    val = []
    while index<ln and (test_char in allow or test_char.isalpha() or test_char.isdigit()):
        val.append(test_char)
        index += 1
        test_char = str_in[index]
    return index, ''.join(val)

def parse_tmp_env(type_tmp):
    atom_start, atom_allow = {'_'}, {'_'}
    result = {}
    type_tmp = type_tmp.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    if not type_tmp:
        return result
    index, ln = 0, len(type_tmp)
    while index<ln:
        index, atom = parse_atom(type_tmp, ln, index, atom_start, atom_allow)
        assert atom, 'can not get atom from `%s` @%d' % (type_tmp, index)
        assert atom not in result, 'redef atom `%d` from `%s` @%d' % (atom, type_tmp, index)
        assert type_tmp[index]=='=', 'after atom must be `=` but `` @%d' % (type_tmp[index], index)
        index += 1
        tmp = type_tmp[index:]
        type_str = tmp.split(';')[0] if ';' in tmp else tmp
        _type = parse_type(type_str)
        assert _type, 'can not parse_type from `%s` @%d' % (type_str, index)
        index += len(type_str) + 1
        result[atom] = _type
    return result

def parse_type_def(type_str):
    atom_start, atom_allow = {'_'}, {'_', '.'}
    result = {}
    type_tmp = type_tmp.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    if not type_tmp:
        return result
    index, ln = 0, len(type_tmp)
    while index<ln:
        index, atom = parse_atom(type_tmp, ln, index, atom_start, atom_allow)
        assert atom, 'can not get atom from `%s` @%d' % (type_tmp, index)
        assert atom not in result, 'redef atom `%d` from `%s` @%d' % (atom, type_tmp, index)
        assert type_tmp[index]=='=', 'after atom must be `=` but `` @%d' % (type_tmp[index], index)
        index += 1
    return

def parse_target(target_str):
    result = GLOBAL_ENV.get(type_str, None)
    return result

def parse_type(type_str):
    result = GLOBAL_ENV.get(type_str, None)
    return result

def parse_type_assist(type_assist, env=GLOBAL_ENV):
    type_str, type_tmp = type_assist
    tmp_env = parse_tmp_env(type_tmp)
    type_def = parse_type_def(type_str)
    return []

#==================ADD TYPE INFO===================
def parse_assign(type_assist, target):
    result = parse_type_assist(type_assist)
    ret_list = []
    return ret_list

def parse_functiondef(type_assist, ast_arguments):
    args, vararg, kwarg, defaults = ast_arguments.args, ast_arguments.vararg, ast_arguments.kwarg, ast_arguments.defaults
    args = [i.name for i in args]
    defaults = [i.value for i in defaults]
    return FuncType(args, vararg, kwarg, defaults)

test = "a=int;b=str;c=list"
ret = parse_tmp_env(test)
print ret
print 'end!'



class Pyter(object):
    def __init__(self, current_name, current_file):
        self.current_name = current_name
        self.current_file = current_file
        self.msg_info = {}

    def add_message(self, msg_descr, line=None, node=None, args=None, confidence=UNDEFINED):
        if line is None and node is not None:
            line = node.fromlineno
        if hasattr(node, 'col_offset'):
            col_offset = node.col_offset # XXX measured in bytes for utf-8, divide by two for chars?
        else:
            col_offset = None
        # expand message ?
        msg = self.msg_info.get(msg_descr, ','.join(['%s'] *len(args)))
        if args:
            msg %= args
        # get module and object
        if node is None:
            module, obj = self.current_name, ''
            abspath = self.current_file
        else:
            module, obj = self.get_module_and_frameid(node)
            abspath = node.root().file
        path = abspath
        MSG((abspath, path, module, obj, line or 1, col_offset or 0), msg, confidence)



    def get_ast(self):
        """return a ast(roid) representation for a module"""
        def get_type_assist_tuple(str_val, line_no, str_line):
            str_val = str_val.replace(' ', '').replace('\t', '')
            if str_val.startswith('~:') and len(str_val)>2:
                str_list = str_val[2:].split('@')
                if len(str_list)==1:
                    return (str_list[0], '')
                elif (len(str_list)==3 and str_list[2]==''):
                    return (str_list[0], str_list[1])
                else:
                    msg = 'type assist must use like:`a_item = a_list.pop() # ~:type[@...@]`.'
                    raise SyntaxError("line:%d -> %s -> %s" % (line_no, str_line))
            return None

        def get_type_assist_dict(tokens):
            type_assist_dict = {}
            for type_id, str_val, index_start, index_end, str_line in tokens:
                line_no = index_start[0]
                if type_id==53 and str_val[0]=='#' and len(str_val)>3:
                    tmp = get_type_assist_tuple(str_val[1:], line_no, str_line)
                    if tmp:
                        type_assist_dict[line_no] = tmp
            return type_assist_dict

        def fix_ast(ast_node, type_assist_dict):
            body = getattr(ast_node, 'body', [])
            for item in body:
                if isinstance(item, astroid.Assign):
                    target = [i.name for i in item.targets]
                    _type_assist = type_assist_dict.get(item.lineno, None)
                    if _type_assist:
                        type_list = parse_assign(_type_assist, target)
                        for index, sub_item in enumerate(item.targets):
                            sub_item._type = type_list[index]
                elif isinstance(item, astroid.FunctionDef):
                    doc = getattr(item, 'doc', '')
                    str_val  = doc.split('\n')[0]
                    _type_assist = get_type_assist_tuple(str_val, item.lineno, item.as_string())
                    if _type_assist:
                        item._type = parse_functiondef(_type_assist, item.args)
                    fix_ast(item, type_assist_dict)

        filepath, modname = self.current_file, self.current_name
        try:
            ast_node = astroid.MANAGER.ast_from_file(filepath, modname, source=True)
            tokens = self.tokenize_module(ast_node)
            type_assist_dict = get_type_assist_dict(tokens)
            fix_ast(ast_node, type_assist_dict)
            return ast_node
        except astroid.AstroidBuildingException as ex:
            if isinstance(ex.args[0], SyntaxError):
                ex = ex.args[0]
                self.add_message('syntax-error',
                                 line=ex.lineno or 0,
                                 args=ex.msg)
            else:
                self.add_message('parse-error', args=ex)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            self.add_message('astroid-error', args=(ex.__class__, ex))

    def get_module_and_frameid(self, node):
        """return the module name and the frame id in the module"""
        frame = node.frame()
        module, obj = '', []
        while frame:
            if isinstance(frame, Module):
                module = frame.name
            else:
                obj.append(getattr(frame, 'name', '<lambda>'))
            try:
                frame = frame.parent.frame()
            except AttributeError:
                frame = None
        obj.reverse()
        return module, '.'.join(obj)

    def tokenize_module(self, module):
        def _decoding_readline(stream, encoding):
            return lambda: stream.readline().decode(encoding, 'replace')

        with module.stream() as stream:
            readline = stream.readline
            if sys.version_info < (3, 0):
                if module.file_encoding is not None:
                    readline = _decoding_readline(stream, module.file_encoding)

                return list(tokenize.generate_tokens(readline))
            return list(tokenize.tokenize(readline))

def main():
    py_file = r"E:\test_pyt.py"
    py_name = 'test_pyt'
    expr_ast = Pyter(py_name, py_file).get_ast()


    #global_env = check(expr_ast)

def check(expr_ast, outer=None):
    env = Env(outer)
    for item in expr_ast.body:
        ast_func = AST_FUNC_DIST.get(type(item), None)
        if ast_func:
            ast_func(item, env)


class Env(dict):
    def __init__(self, outer=None):
        self.__outer = outer

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            if self.__outer is not None:
                return self.__outer.get(key, default)
            else:
                return default



def FunctionDef_func(item, env):
    name_str = item.name

    decorator_list = item.decorator_list
    args_dict = item.args
    args_type = type_func_args(args_dict)

    raise_error(name_str in env and CONF.no_redef_func, 'redef func:%s(%s)->(%s)' % (name_str, env.get(name_str,''), args_type))

    item_doc = item.body[0].value if isinstance(item.body[0], _ast.Expr) and isinstance(item.body[0].value, _ast.Str) else None
    raise_error(not item_doc and CONF.no_undoc_func, 'undoc func:%s(%s)' % (name_str, args_type))

    type_doc = type_func_doc(item_doc) if item_doc else None
    env[name_str] = cast(args_type, type_doc) if type_doc else args_type


def Assign_func(item, env):
    targets = item.targets
    types = type_assign_value(item.value)
    for index, atom in enumerate(targets):
        if atom.id in env:
            msg = 'redef:%s(%s)->%s(%s)' % (item.name, env[item.name], item.name, get_doc(item))
        else:
            env[item.name] = get_doc(item)





def type_func_doc(ast_str):
    doc_str = ast_str.s.strip()
    lineno = ast_str.lineno
    doc_list =  doc_str.split(':', 1)
    if doc_list[0].strip()=='pyt':
        doc_str = doc_list[1].strip()
        tmp_list = doc_str.split('=>', 1) if '=>' in doc_str else ['', doc_str]
        def_str, type_str = tmp_list[0].strip(), tmp_list[1].strip()
        def_dict = parse_def(def_str, STD_TYPE)
        return type_build(type_str, def_dict, STD_TYPE)
    else:
        return None

def type_assign_value():
    return 'eq'

def type_inline_explain():
    return 'eq'

def parse_def(def_str, STD_TYPE):
    ret_dict = {}
    def_list = [s.strip() for s in def_str.split(';')]
    for item_str in def_list:
        raise_error('`' not in item_str, 'cannot parse_def:%s at %s' % (def_str, item_str))
        tmp_list = item_str.split('`', 1)
        type_str, atom_str = tmp_list[0], tmp_list[1]
        atom_list = parse_atom(atom_str)
        tmp_type = type_build(type_str, {}, STD_TYPE)
        for atom in atom_list:
            ret_dict[atom] = tmp_type
    return ret_dict

def parse_atom(atom_str):
    return [s.strip() for s in atom_str.split(',')]

def type_build(type_str, def_dict, STD_TYPE):
    type_str = type_str.strip()
    if type_str in def_dict:
        return def_dict[type_str]
    elif type_str in STD_TYPE:
        return BaseType(STD_TYPE[type_str])
    else:
        return _type_build(type_str, def_dict, STD_TYPE)

def _type_build(type_str, def_dict, STD_TYPE):
    return type_str

def cast(from_type, to_type):
    return to_type

class Type(object):
    pass

class BaseType(Type):
    def __init__(self, sys_type):
        self.base_type = sys_type if isinstance(sys_type, type) else None

class NoneType(Type):
    pass

class AnyType(Type):
    pass

class FuncType(Type):
    def __init__(self, args, vararg=None, kwarg=None, defaults=[]):
        self.args = args
        self.vararg = vararg
        self.kwarg = kwarg
        self.defaults = defaults


AST_FUNC_DIST = {
_ast.Assign:Assign_func,
_ast.ClassDef:None,
_ast.FunctionDef:FunctionDef_func,}

def raise_error(raise_it, msg, Error=TypeError):
    if raise_it:
        raise Error(msg)

if __name__ =='__main__':
    main()