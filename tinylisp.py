import traceback
import sys
import math
import operator as op
from string import upper
import lispop as lop

Number = (int, float) # A Scheme Number is implemented as a Python int or float
Symbol = str          # A Scheme Symbol is implemented as a Python str

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self[var]
        elif self.outer is None:
            return var
        else:
            return self.outer.find(var)
def add_globals(self):
    "An environment with some Scheme standard procedures."
    self.update(vars(math)) # sin, cos, sqrt, pi, ...
    self.update({
        '+':lop.addl, '-':lop.subl, '*':lop.mull, '/':lop.divl,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'AND':     lop.andl,'OR':     lop.orl,
        'CAR':     lambda x: x[0],
        'CDR':     lambda x: x[1:],
        'CONS':    lambda x,y: [x] + y,
        'FIRST':   lambda  x:x[1],
        'SECOND':  lambda x: x[2],
        'THIRD':   lambda x: x[3],
        'LIST':    lambda *x: list(x),
        'LISTP':   lambda x: isinstance(x,list),
        'NOT':     op.not_,
        'NULL':    lambda x:x==None
    })
    return self
global_env = add_globals(Env())
class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))
def tolist(tokens):
    if len(tokens)==0:
        return None
    token = tokens.pop(0)
    if '('==token:
        result = []
        while tokens[0]!=')':
            if '('==tokens[0] or "'"==tokens[0]:
                result.append(eval(read_from_tokens(tokens)))
            else:
                result.append(tokens[0])
            tokens.pop(0)
        return result
def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
def listToStr(exp):
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(listToStr, exp)) + ')'
    else:
        return str(exp)
def parse(line):
    tokens = tokenize(line)
    return read_from_tokens(tokens)
def changeres(i):
    if isinstance(i,list):
        return eval(i,global_env)
    else:
        return i
def read_from_tokens(tokens):
    if len(tokens) == 0:
        return None
    token = tokens.pop(0)
    if "'"==token:
        res = []
        res.append("'")
        result = read_from_tokens(tokens)
        #for i in range(len(result)):
        #    if isinstance(result[i],list):
        #        result[i] = eval(result[i],global_env)
        resu = [changeres(i) for i in result]
        res.append(resu)
        return res
    elif '(' == token:
        result = []
        while tokens[0]!=')':
            result.append(read_from_tokens(tokens))
        tokens.pop(0)
        return result
    elif ')'==token:
        raise SyntaxError('Unexpected ")"')
    else:
        return atom(token)
def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            token = upper(token)
            if token == 'NONE' or token == 'NIL':
                return None
            if token[0] == "'":
                return upper(token[1:])
            if token[0] =='"':
                if token[-1]=='"':
                    return token
                else:
                    raise SyntaxError('Miss "')
            if global_env.has_key(token):
                return token
            else:
                return token
                #raise SyntaxError('Undefined function or variable')
def eval(x, env = global_env):
    if isinstance(x, Symbol):
        if env.find(x)!=x:
            return env.find(x)
        else:
            return x
    elif not isinstance(x, list):
        return x
    elif len(x)==0:
        return None
    elif x[0]=="'" or x[0]=='QUOTE':
        for i in range(len(x[1])):
            if isinstance(x[1][i],list):
                x[1][i] = eval(x[1][i],global_env)
        res = x[1]
        return res
    elif x[0] == 'LAMBDA':  # procedure
        if len(x)==4:
            (_, parms, body,var) = x
            lam = Procedure(parms, body, Env(parms, var, env))
            return eval(lam(var), Env(parms, var, env))
        else:
            (_, parms, body) = x
            lam = Procedure(parms, body,env)
            return lam


    elif x[0] == 'DEFINE':  # definition
        (_, var, exp) = x
        env[var] = eval(exp, env)
        return var

    elif x[0] =='IF':
        if len(x)==3:
            (_, conseq, tru) = x
        fal = None
        if len(x)==4:
            (_, conseq, tru,fal) = x

        if eval(conseq,env):
            exp = eval(tru)
        else:
            exp = fal
        return exp

    elif x[0] == 'DEFPARAMETER':
        (_,varname,exp) = x
        global_env[varname] = eval(exp,env)
        return varname
    elif x[0] == 'SETF':
        (_,varname,exp) = x
        if(global_env.has_key(varname)):
            global_env[varname] = eval(exp,env)
        return varname
    else:
        proc = env.find(x[0])
        if isinstance(proc, Number) or isinstance(proc, str):
            return x
        else:
            args = [eval(arg,env) for arg in x[1:]]
        return proc(*args)



while True:
    try:
        line = raw_input("dk> ")
        print listToStr(eval(parse(line),global_env))

    except Exception as e:
        print "".join(traceback.format_exception(*sys.exc_info()))

