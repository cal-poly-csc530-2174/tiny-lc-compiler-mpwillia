from sexpdata import loads, Symbol 
import argparse
from numbers import Number

lambda_strs = {"λ", "λ", "lambda", "lamda"}
keywords = lambda_strs | {"+", "*", "ifleq0", "println" }

parsed_header = ("import sys\n"
                 "sys.setrecursionlimit(10**6)\n\n"
                 "def println(s):\n"
                 "\tprint(s)\n"
                 "\treturn 0\n\n")

def main():
    args = parse_args() 

    with open(args.src_path, 'r') as f:
        contents = f.read()
    sexp = loads(contents)

    parsed = parsed_header
    parsed += parse(sexp)
    
    with open(args.dst_path, 'w') as f:
        f.write(parsed)


def parse(sexp):
    if isinstance(sexp, Number):
        return str(sexp)
    elif type(sexp) == Symbol:
        return str(sexp.value())

    if len(sexp) <= 0:
        return ''
    elif len(sexp) == 1:
        return parse(sexp[0]) 
    elif type(sexp[0]) != list:
        if type(sexp[0]) == Symbol:
            return parse_keywords(sexp)
        else:
            raise Exception("Expected keyword! Got {}".format(sexp[0]))
    elif len(sexp) == 2:
        return "({}({}))".format(parse(sexp[0]), parse(sexp[1]))
    else:
        raise Exception("Syntax Error!")

def parse_keywords(sexp):
    if sexp[0].value() == '+':
        if len(sexp) == 3:
            return "({} + {})".format(parse(sexp[1]), parse(sexp[2]))
        else:
            raise Exception("Expected 2 operands for '+'")
    elif sexp[0].value() == '*':
        if len(sexp) == 3:
            return "({} * {})".format(parse(sexp[1]), parse(sexp[2]))
        else:
            raise Exception("Expected 2 operands for '*'")
    elif sexp[0].value() == 'ifleq0':
        if len(sexp) == 4:
            return "({} if ({} <= 0) else {})".format(parse(sexp[2]), parse(sexp[1]), parse(sexp[3]))
        else:
            raise Exception("Expected 3 operands for 'ifleq0'")
    elif sexp[0].value() == 'println':
        if len(sexp) == 2:
            return "(println({}))".format(parse(sexp[1]))
        else:
            raise Exception("Expected 1 operand for 'println'")
    elif sexp[0].value() in lambda_strs:
        if len(sexp) == 3:
            if type(sexp[1]) != list or len(sexp[1]) != 1 or type(sexp[1][0]) != Symbol:
               raise Exception("Expected identifier for '{}'".format(sexp[0].value()))
            return "(lambda {} : {})".format(parse(sexp[1]), parse(sexp[2]))
        else:
            raise Exception("Expected 2 operand for '{}'".format(sexp[0].value()))
    else:
        return "({}({})) ".format(parse(sexp[0]), parse(sexp[1]))

def parse_args():
    parser = argparse.ArgumentParser(description='Compiles lambda calculus into python')
    parser.add_argument("src_path", metavar = "Source", type = str, help = 
    """the source file containing lambda calculus to compile to python""")
    parser.add_argument("dst_path", metavar = "Destination", type = str, help = 
    """the name of the python file to write to""")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()


