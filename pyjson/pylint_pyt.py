# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        pyt
# Purpose:
#
# Author:      Administrator
#
# Created:     22/12/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import tokenize
import astroid
from astroid import nodes, Module

import six
import collections
import itertools
from collections import namedtuple
from astroid import nodes, Module

Confidence = namedtuple('Confidence', ['name', 'description'])
# Warning Certainties
HIGH = Confidence('HIGH', 'No false positive possible.')
INFERENCE = Confidence('INFERENCE', 'Warning based on inference result.')
INFERENCE_FAILURE = Confidence('INFERENCE_FAILURE',
                               'Warning based on inference with failures.')
UNDEFINED = Confidence('UNDEFINED',
                       'Warning without any associated confidence level.')

CONFIDENCE_LEVELS = [HIGH, INFERENCE, INFERENCE_FAILURE, UNDEFINED]

import sys
from pylint.lint import Run

def run_pylint():
    """run pylint"""
    args = [r"missing_docstring.py"]
    #Run(args)

    PyLinter()._do_check(args)



def tokenize_module(module):
    with module.stream() as stream:
        readline = stream.readline
        if sys.version_info < (3, 0):
            if module.file_encoding is not None:
                readline = _decoding_readline(stream, module.file_encoding)

            return list(tokenize.generate_tokens(readline))
        return list(tokenize.tokenize(readline))





class MessagesStore(object):
    """The messages store knows information about every possible message but has
    no particular state during analysis.
    """

    def __init__(self):
        # Primary registry for all active messages (i.e. all messages
        # that can be emitted by pylint for the underlying Python
        # version). It contains the 1:1 mapping from symbolic names
        # to message definition objects.
        self._messages = {}
        # Maps alternative names (numeric IDs, deprecated names) to
        # message definitions. May contain several names for each definition
        # object.
        self._alternative_names = {}
        self._msgs_by_category = collections.defaultdict(list)

    @property
    def messages(self):
        """The list of all active messages."""
        return six.itervalues(self._messages)

    def add_renamed_message(self, old_id, old_symbol, new_symbol):
        """Register the old ID and symbol for a warning that was renamed.

        This allows users to keep using the old ID/symbol in suppressions.
        """
        msg = self.check_message_id(new_symbol)
        msg.old_names.append((old_id, old_symbol))
        self._alternative_names[old_id] = msg
        self._alternative_names[old_symbol] = msg

    def register_messages(self, checker):
        """register a dictionary of messages

        Keys are message ids, values are a 2-uple with the message type and the
        message itself

        message ids should be a string of len 4, where the two first characters
        are the checker id and the two last the message id in this checker
        """
        chkid = None
        for msgid, msg_tuple in six.iteritems(checker.msgs):
            msg = build_message_def(checker, msgid, msg_tuple)
            assert msg.symbol not in self._messages, \
                    'Message symbol %r is already defined' % msg.symbol
            # avoid duplicate / malformed ids
            assert msg.msgid not in self._alternative_names, \
                   'Message id %r is already defined' % msgid
            assert chkid is None or chkid == msg.msgid[1:3], \
                   'Inconsistent checker part in message id %r' % msgid
            chkid = msg.msgid[1:3]
            self._messages[msg.symbol] = msg
            self._alternative_names[msg.msgid] = msg
            for old_id, old_symbol in msg.old_names:
                self._alternative_names[old_id] = msg
                self._alternative_names[old_symbol] = msg
            self._msgs_by_category[msg.msgid[0]].append(msg.msgid)

    def check_message_id(self, msgid):
        """returns the Message object for this message.

        msgid may be either a numeric or symbolic id.

        Raises UnknownMessage if the message id is not defined.
        """
        if msgid[1:].isdigit():
            msgid = msgid.upper()
        for source in (self._alternative_names, self._messages):
            try:
                return source[msgid]
            except KeyError:
                pass
        raise UnknownMessage('No such message id %s' % msgid)

    def get_msg_display_string(self, msgid):
        """Generates a user-consumable representation of a message.

        Can be just the message ID or the ID and the symbol.
        """
        return repr(self.check_message_id(msgid).symbol)

    def help_message(self, msgids):
        """display help messages for the given message identifiers"""
        for msgid in msgids:
            try:
                print(self.check_message_id(msgid).format_help(checkerref=True))
                print("")
            except UnknownMessage as ex:
                print(ex)
                print("")
                continue

    def list_messages(self):
        """output full messages list documentation in ReST format"""
        msgs = sorted(six.itervalues(self._messages), key=lambda msg: msg.msgid)
        for msg in msgs:
            if not msg.may_be_emitted():
                continue
            print(msg.format_help(checkerref=False))
        print("")


class MessagesHandlerMixIn(object):
    """a mix-in class containing all the messages related methods for the main
    lint class
    """

    def __init__(self):
        self._msgs_state = {}
        self.msg_status = 0

    def _checker_messages(self, checker):
        for checker in self._checkers[checker.lower()]:
            for msgid in checker.msgs:
                yield msgid

    def disable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """don't output message of the given id"""
        assert scope in ('package', 'module')
        # handle disable=all by disabling all categories
        if msgid == 'all':
            for msgid in MSG_TYPES:
                self.disable(msgid, scope, line)
            return
        # msgid is a category?
        catid = category_id(msgid)
        if catid is not None:
            for _msgid in self.msgs_store._msgs_by_category.get(catid):
                self.disable(_msgid, scope, line)
            return
        # msgid is a checker name?
        if msgid.lower() in self._checkers:
            msgs_store = self.msgs_store
            for checker in self._checkers[msgid.lower()]:
                for _msgid in checker.msgs:
                    if _msgid in msgs_store._alternative_names:
                        self.disable(_msgid, scope, line)
            return
        # msgid is report id?
        if msgid.lower().startswith('rp'):
            self.disable_report(msgid)
            return

        try:
            # msgid is a symbolic or numeric msgid.
            msg = self.msgs_store.check_message_id(msgid)
        except UnknownMessage:
            if ignore_unknown:
                return
            raise

        if scope == 'module':
            self.file_state.set_msg_status(msg, line, False)
            if msg.symbol != 'locally-disabled':
                self.add_message('locally-disabled', line=line,
                                 args=(msg.symbol, msg.msgid))

        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = False
            # sync configuration object
            self.config.disable = [self._message_symbol(mid)
                                   for mid, val in six.iteritems(msgs)
                                   if not val]

    def _message_symbol(self, msgid):
        """Get the message symbol of the given message id

        Return the original message id if the message does not
        exist.
        """
        try:
            return self.msgs_store.check_message_id(msgid).symbol
        except UnknownMessage:
            return msgid

    def enable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """reenable message of the given id"""
        assert scope in ('package', 'module')
        if msgid == 'all':
            for msgid_ in MSG_TYPES:
                self.enable(msgid_, scope=scope, line=line)
            if not self._python3_porting_mode:
                # Don't activate the python 3 porting checker if it
                # wasn't activated explicitly.
                self.disable('python3')
            return
        catid = category_id(msgid)
        # msgid is a category?
        if catid is not None:
            for msgid in self.msgs_store._msgs_by_category.get(catid):
                self.enable(msgid, scope, line)
            return
        # msgid is a checker name?
        if msgid.lower() in self._checkers:
            for checker in self._checkers[msgid.lower()]:
                for msgid_ in checker.msgs:
                    self.enable(msgid_, scope, line)
            return
        # msgid is report id?
        if msgid.lower().startswith('rp'):
            self.enable_report(msgid)
            return

        try:
            # msgid is a symbolic or numeric msgid.
            msg = self.msgs_store.check_message_id(msgid)
        except UnknownMessage:
            if ignore_unknown:
                return
            raise

        if scope == 'module':
            self.file_state.set_msg_status(msg, line, True)
            self.add_message('locally-enabled', line=line, args=(msg.symbol, msg.msgid))
        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = True
            # sync configuration object
            self.config.enable = [mid for mid, val in six.iteritems(msgs) if val]

    def get_message_state_scope(self, msgid, line=None, confidence=UNDEFINED):
        """Returns the scope at which a message was enabled/disabled."""
        if self.config.confidence and confidence.name not in self.config.confidence:
            return MSG_STATE_CONFIDENCE
        try:
            if line in self.file_state._module_msgs_state[msgid]:
                return MSG_STATE_SCOPE_MODULE
        except (KeyError, TypeError):
            return MSG_STATE_SCOPE_CONFIG

    def is_message_enabled(self, msg_descr, line=None, confidence=None):
        """return true if the message associated to the given message id is
        enabled

        msgid may be either a numeric or symbolic message id.
        """
        if self.config.confidence and confidence:
            if confidence.name not in self.config.confidence:
                return False
        try:
            msgid = self.msgs_store.check_message_id(msg_descr).msgid
        except UnknownMessage:
            # The linter checks for messages that are not registered
            # due to version mismatch, just treat them as message IDs
            # for now.
            msgid = msg_descr
        if line is None:
            return self._msgs_state.get(msgid, True)
        try:
            return self.file_state._module_msgs_state[msgid][line]
        except KeyError:
            return self._msgs_state.get(msgid, True)

    def add_message(self, msg_descr, line=None, node=None, args=None, confidence=UNDEFINED):
        """Adds a message given by ID or name.

        If provided, the message string is expanded using args

        AST checkers should must the node argument (but may optionally
        provide line if the line number is different), raw and token checkers
        must provide the line argument.
        """
        msg_info = self.msgs_store.check_message_id(msg_descr)
        msgid = msg_info.msgid
        # backward compatibility, message may not have a symbol
        symbol = msg_info.symbol or msgid
        # Fatal messages and reports are special, the node/scope distinction
        # does not apply to them.
        if msgid[0] not in _SCOPE_EXEMPT:
            if msg_info.scope == WarningScope.LINE:
                assert node is None and line is not None, (
                    'Message %s must only provide line, got line=%s, node=%s' % (msgid, line, node))
            elif msg_info.scope == WarningScope.NODE:
                # Node-based warnings may provide an override line.
                assert node is not None, 'Message %s must provide Node, got None'

        if line is None and node is not None:
            line = node.fromlineno
        if hasattr(node, 'col_offset'):
            col_offset = node.col_offset # XXX measured in bytes for utf-8, divide by two for chars?
        else:
            col_offset = None
        # should this message be displayed
        if not self.is_message_enabled(msgid, line, confidence):
            self.file_state.handle_ignored_message(
                self.get_message_state_scope(msgid, line, confidence),
                msgid, line, node, args, confidence)
            return
        # update stats
        msg_cat = MSG_TYPES[msgid[0]]
        self.msg_status |= MSG_TYPES_STATUS[msgid[0]]
        self.stats[msg_cat] += 1
        self.stats['by_module'][self.current_name][msg_cat] += 1
        try:
            self.stats['by_msg'][symbol] += 1
        except KeyError:
            self.stats['by_msg'][symbol] = 1
        # expand message ?
        msg = msg_info.msg
        if args:
            msg %= args
        # get module and object
        if node is None:
            module, obj = self.current_name, ''
            abspath = self.current_file
        else:
            module, obj = get_module_and_frameid(node)
            abspath = node.root().file
        path = abspath.replace(self.reporter.path_strip_prefix, '')
        # add the message
        self.reporter.handle_message(
            Message(msgid, symbol,
                    (abspath, path, module, obj, line or 1, col_offset or 0), msg, confidence))

    def print_full_documentation(self):
        """output a full documentation in ReST format"""
        print("Pylint global options and switches")
        print("----------------------------------")
        print("")
        print("Pylint provides global options and switches.")
        print("")

        by_checker = {}
        for checker in self.get_checkers():
            if checker.name == 'master':
                if checker.options:
                    for section, options in checker.options_by_section():
                        if section is None:
                            title = 'General options'
                        else:
                            title = '%s options' % section.capitalize()
                        print(title)
                        print('~' * len(title))
                        _rest_format_section(sys.stdout, None, options)
                        print("")
            else:
                try:
                    by_checker[checker.name][0] += checker.options_and_values()
                    by_checker[checker.name][1].update(checker.msgs)
                    by_checker[checker.name][2] += checker.reports
                except KeyError:
                    by_checker[checker.name] = [list(checker.options_and_values()),
                                                dict(checker.msgs),
                                                list(checker.reports)]

        print("Pylint checkers' options and switches")
        print("-------------------------------------")
        print("")
        print("Pylint checkers can provide three set of features:")
        print("")
        print("* options that control their execution,")
        print("* messages that they can raise,")
        print("* reports that they can generate.")
        print("")
        print("Below is a list of all checkers and their features.")
        print("")

        for checker, (options, msgs, reports) in six.iteritems(by_checker):
            title = '%s checker' % (checker.replace("_", " ").title())
            print(title)
            print('~' * len(title))
            print("")
            print("Verbatim name of the checker is ``%s``." % checker)
            print("")
            if options:
                title = 'Options'
                print(title)
                print('^' * len(title))
                _rest_format_section(sys.stdout, None, options)
                print("")
            if msgs:
                title = 'Messages'
                print(title)
                print('~' * len(title))
                for msgid, msg in sorted(six.iteritems(msgs),
                                         key=lambda kv: (_MSG_ORDER.index(kv[0][0]), kv[1])):
                    msg = build_message_def(checker, msgid, msg)
                    print(msg.format_help(checkerref=False))
                print("")
            if reports:
                title = 'Reports'
                print(title)
                print('~' * len(title))
                for report in reports:
                    print(':%s: %s' % report[:2])
                print("")
            print("")


class FileState(object):
    """Hold internal state specific to the currently analyzed file"""

    def __init__(self, modname=None):
        self.base_name = modname
        self._module_msgs_state = {}
        self._raw_module_msgs_state = {}
        self._ignored_msgs = collections.defaultdict(set)
        self._suppression_mapping = {}

    def collect_block_lines(self, msgs_store, module_node):
        """Walk the AST to collect block level options line numbers."""
        for msg, lines in six.iteritems(self._module_msgs_state):
            self._raw_module_msgs_state[msg] = lines.copy()
        orig_state = self._module_msgs_state.copy()
        self._module_msgs_state = {}
        self._suppression_mapping = {}
        self._collect_block_lines(msgs_store, module_node, orig_state)

    def _collect_block_lines(self, msgs_store, node, msg_state):
        """Recursivly walk (depth first) AST to collect block level options line
        numbers.
        """
        for child in node.get_children():
            self._collect_block_lines(msgs_store, child, msg_state)
        first = node.fromlineno
        last = node.tolineno
        # first child line number used to distinguish between disable
        # which are the first child of scoped node with those defined later.
        # For instance in the code below:
        #
        # 1.   def meth8(self):
        # 2.        """test late disabling"""
        # 3.        # pylint: disable=E1102
        # 4.        print self.blip
        # 5.        # pylint: disable=E1101
        # 6.        print self.bla
        #
        # E1102 should be disabled from line 1 to 6 while E1101 from line 5 to 6
        #
        # this is necessary to disable locally messages applying to class /
        # function using their fromlineno
        if (isinstance(node, (nodes.Module, nodes.ClassDef, nodes.FunctionDef))
                and node.body):
            firstchildlineno = node.body[0].fromlineno
        else:
            firstchildlineno = last
        for msgid, lines in six.iteritems(msg_state):
            for lineno, state in list(lines.items()):
                original_lineno = lineno
                if first > lineno or last < lineno:
                    continue
                # Set state for all lines for this block, if the
                # warning is applied to nodes.
                if  msgs_store.check_message_id(msgid).scope == WarningScope.NODE:
                    if lineno > firstchildlineno:
                        state = True
                    first_, last_ = node.block_range(lineno)
                else:
                    first_ = lineno
                    last_ = last
                for line in range(first_, last_+1):
                    # do not override existing entries
                    if line in self._module_msgs_state.get(msgid, ()):
                        continue
                    if line in lines: # state change in the same block
                        state = lines[line]
                        original_lineno = line
                    if not state:
                        self._suppression_mapping[(msgid, line)] = original_lineno
                    try:
                        self._module_msgs_state[msgid][line] = state
                    except KeyError:
                        self._module_msgs_state[msgid] = {line: state}
                del lines[lineno]

    def set_msg_status(self, msg, line, status):
        """Set status (enabled/disable) for a given message at a given line"""
        assert line > 0
        try:
            self._module_msgs_state[msg.msgid][line] = status
        except KeyError:
            self._module_msgs_state[msg.msgid] = {line: status}

    def handle_ignored_message(self, state_scope, msgid, line,
                               node, args, confidence): # pylint: disable=unused-argument
        """Report an ignored message.

        state_scope is either MSG_STATE_SCOPE_MODULE or MSG_STATE_SCOPE_CONFIG,
        depending on whether the message was disabled locally in the module,
        or globally. The other arguments are the same as for add_message.
        """
        if state_scope == MSG_STATE_SCOPE_MODULE:
            try:
                orig_line = self._suppression_mapping[(msgid, line)]
                self._ignored_msgs[(msgid, orig_line)].add(line)
            except KeyError:
                pass

    def iter_spurious_suppression_messages(self, msgs_store):
        for warning, lines in six.iteritems(self._raw_module_msgs_state):
            for line, enable in six.iteritems(lines):
                if not enable and (warning, line) not in self._ignored_msgs:
                    yield 'useless-suppression', line, \
                        (msgs_store.get_msg_display_string(warning),)
        # don't use iteritems here, _ignored_msgs may be modified by add_message
        for (warning, from_), lines in list(self._ignored_msgs.items()):
            for line in lines:
                yield 'suppressed-message', line, \
                    (msgs_store.get_msg_display_string(warning), from_)

DEPRECATED_ALIASES = {
    # New name, deprecated name.
    'repr': 'backquote',
    'expr': 'discard',
    'assignname': 'assname',
    'assignattr': 'assattr',
    'attribute': 'getattr',
    'call': 'callfunc',
    'importfrom': 'from',
    'classdef': 'class',
    'functiondef': 'function',
    'generatorexp': 'genexpr',
}

class PyLintASTWalker(object):

    def __init__(self, linter):
        # callbacks per node types
        self.nbstatements = 0
        self.visit_events = collections.defaultdict(list)
        self.leave_events = collections.defaultdict(list)
        self.linter = linter

    def _is_method_enabled(self, method):
        if not hasattr(method, 'checks_msgs'):
            return True
        for msg_desc in method.checks_msgs:
            if self.linter.is_message_enabled(msg_desc):
                return True
        return False

    def add_checker(self, checker):
        """walk to the checker's dir and collect visit and leave methods"""
        # XXX : should be possible to merge needed_checkers and add_checker
        vcids = set()
        lcids = set()
        visits = self.visit_events
        leaves = self.leave_events
        for member in dir(checker):
            cid = member[6:]
            if cid == 'default':
                continue
            if member.startswith('visit_'):
                v_meth = getattr(checker, member)
                # don't use visit_methods with no activated message:
                if self._is_method_enabled(v_meth):
                    visits[cid].append(v_meth)
                    vcids.add(cid)
            elif member.startswith('leave_'):
                l_meth = getattr(checker, member)
                # don't use leave_methods with no activated message:
                if self._is_method_enabled(l_meth):
                    leaves[cid].append(l_meth)
                    lcids.add(cid)
        visit_default = getattr(checker, 'visit_default', None)
        if visit_default:
            for cls in nodes.ALL_NODE_CLASSES:
                cid = cls.__name__.lower()
                if cid not in vcids:
                    visits[cid].append(visit_default)
        # for now we have no "leave_default" method in Pylint

    def walk(self, astroid):
        """call visit events of astroid checkers for the given node, recurse on
        its children, then leave events.
        """
        cid = astroid.__class__.__name__.lower()

        # Detect if the node is a new name for a deprecated alias.
        # In this case, favour the methods for the deprecated
        # alias if any,  in order to maintain backwards
        # compatibility.
        old_cid = DEPRECATED_ALIASES.get(cid)
        visit_events = ()
        leave_events = ()

        if old_cid:
            visit_events = self.visit_events.get(old_cid, ())
            leave_events = self.leave_events.get(old_cid, ())
            if visit_events or leave_events:
                msg = ("Implemented method {meth}_{old} instead of {meth}_{new}. "
                       "This will be supported until Pylint 2.0.")
                if visit_events:
                    warnings.warn(msg.format(meth="visit", old=old_cid, new=cid),
                                  PendingDeprecationWarning)
                if leave_events:
                    warnings.warn(msg.format(meth="leave", old=old_cid, new=cid),
                                  PendingDeprecationWarning)

        visit_events = itertools.chain(visit_events,
                                       self.visit_events.get(cid, ()))
        leave_events = itertools.chain(leave_events,
                                       self.leave_events.get(cid, ()))

        if astroid.is_statement:
            self.nbstatements += 1
        # generate events for this node on each checker
        for cb in visit_events or ():
            cb(astroid)
        # recurse on children
        for child in astroid.get_children():
            self.walk(child)
        for cb in leave_events or ():
            cb(astroid)


class PyLinter(MessagesHandlerMixIn):

    def __init__(self):
        self.file_state = FileState()
        self.msgs_store = MessagesStore()

    def process_tokens(self, tokens):
        """process tokens from the current module to search for module/block
        level options
        """
        pass

    def _do_check(self, files_or_modules):
        walker = PyLintASTWalker(self)
        _checkers = []
        tokencheckers = [c for c in _checkers]
        rawcheckers = [c for c in _checkers]
        # notify global begin
        for checker in _checkers:
            checker.open()
            if interfaces.implements(checker, interfaces.IAstroidChecker):
                walker.add_checker(checker)

        for filepath in files_or_modules:
            modname = filepath.replace('.py', '')
            ast_node = self.get_ast(filepath, modname)

            self.file_state = FileState(modname)
            self.check_astroid_module(ast_node, walker, rawcheckers, tokencheckers)

    def check_astroid_module(self, ast_node, walker, rawcheckers, tokencheckers):
        """Check a module from its astroid representation."""
        try:
            tokens = tokenize_module(ast_node)
        except tokenize.TokenError as ex:
            self.add_message('syntax-error', line=ex.args[1][0], args=ex.args[0])
            return

        if not ast_node.pure_python:
            self.add_message('raw-checker-failed', args=ast_node.name)
        else:
            #assert astroid.file.endswith('.py')
            # invoke ITokenChecker interface on self to fetch module/block
            # level options
            self.process_tokens(tokens)

            # walk ast to collect line numbers
            self.file_state.collect_block_lines(self.msgs_store, ast_node)
            # run raw and tokens checkers
            for checker in rawcheckers:
                checker.process_module(ast_node)
            for checker in tokencheckers:
                checker.process_tokens(tokens)
        # generate events to astroid checkers
        if walker:
            walker.walk(ast_node)
        return True


    def get_ast(self, filepath, modname):
        """return a ast(roid) representation for a module"""
        try:
            return astroid.MANAGER.ast_from_file(filepath, modname, source=True)
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


def main():
    run_pylint()

if __name__ == '__main__':
    main()
