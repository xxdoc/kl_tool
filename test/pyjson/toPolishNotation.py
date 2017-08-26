#-------------------------------------------------------------------------------
# Name:        Ä£¿é1
# Purpose:
#
# Author:      Hasee
#
# Created:     09/11/2015
# Copyright:   (c) Hasee 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class IllegalArgumentException(Exception):
    pass

def toPolishNotation(in_list, priority_dict):
    """
    parse the expression.
    param input string list
    throws IllegalArgumentException
    """
    def priorityCompare(op1, op2):
        return priority_dict.get(op1, 1) - priority_dict.get(op2, 1)

    s1, expression = [], []
    lastIndex = -1
    for i in in_list[::-1]:
        if i == ')':
            s1.append(i)
        elif i == '(':
            tempChar = s1.pop()
            while tempChar!=')':
                  expression.push(tempChar)
                  if not s1:
                    raise IllegalArgumentException("bracket dosen't match, missing right bracket ')'.")
        elif i in priority_dict:
            while s1 and s1[-1] != ')' and priorityCompare(i, s1[-1]) < 0:
                  expression.append(s1.pop())
            s1.append(i)
        elif isinstance(i, str):
            expression.append(i)
        else:
            raise IllegalArgumentException("wrong character `%s`" % (i, ))
    while s1:
        expression.append(s1.pop())
    return expression[::-1]

def toCalcExpression(expression, priority_dict, index=0):
    if expression[index] not in priority_dict:
        return index+1, int(expression[index])
    else:
        op = expression[index]
        if op=='*':
            pass
        func = priority_dict[op]
        index += 1
        index, arg1 = toCalcExpression(expression, priority_dict, index)
        index, arg2 = toCalcExpression(expression, priority_dict, index)
        ret = func(arg1, arg2)
        return index, ret

def main():
    priority_dict = {'+':1, '-':1, '*':2, '/':2}
    in_list = ['1','+','2','*','3','-','20','/','4']
    expression = toPolishNotation(in_list, priority_dict)
    print expression
    priority_func = {'+':lambda a,b:a+b, '-':lambda a,b:a-b, '*':lambda a,b:a*b, '/':lambda a,b:a/b}
    print toCalcExpression(expression, priority_func)

if __name__ == '__main__':
    main()
