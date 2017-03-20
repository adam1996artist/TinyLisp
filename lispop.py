def addl(*args):
    ans = 0
    for i in args:
        if isinstance(i, list):
            ans += i[0]
        else:
            ans+=i
    return ans


def subl(*args):
    if (len(args) != 0):
        ans = args[0]
        for i in args[1:]:
            ans -= i
        return ans
    else:
        raise SyntaxError('Too few Parameter')

def mull(*args):
    if (len(args) != 0):
        ans = 1
        for i in args:
            ans *= i
        return ans
    else:
        raise SyntaxError('Too few Parameter')

def divl(*args):
    if (len(args) != 0):
        ans = args[0]
        for i in args[1:]:
            if i==0:
                raise ZeroDivisionError( 'division by zero')
            else:
                ans /= i
        return ans
    else:
        raise SyntaxError('Less Parameter')

def andl(*args):
    if (len(args) != 0):
        for i in args[1:]:
            if i==None:
                return None
        return args[-1]
    else:
        raise SyntaxError('Too few Parameter')

def orl(*args):
    if (len(args) != 0):
        for i in args[1:]:
            if i!=None:
                return i
        return None
    else:
        raise SyntaxError('Too few Parameter')