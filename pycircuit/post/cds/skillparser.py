import skill


# Begin -- grammar generated by Yapps
import sys, re
from yapps import runtime

class skillparserScanner(runtime.Scanner):
    patterns = [
        ('r"\\)"', re.compile('\\)')),
        ('r"\\("', re.compile('\\(')),
        ('[ \t\n\r]+', re.compile('[ \t\n\r]+')),
        ('FLOATNUM', re.compile('-?[0-9]+\\.[0-9e+-]*')),
        ('INTNUM', re.compile('-?[0-9]+')),
        ('ID', re.compile('[-+*/!@$%^&=.?a-zA-Z0-9_]+')),
        ('OBJECT', re.compile('[a-z]+:0x[0-9a-f]+')),
        ('STR', re.compile('"([^\\\\"]+|\\\\.)*"')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{'[ \t\n\r]+':None,},str,*args,**kw)

class skillparser(runtime.Parser):
    Context = runtime.Context
    def expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'expr', [])
        _token = self._peek('ID', 'OBJECT', 'STR', 'INTNUM', 'FLOATNUM', 'r"\\("', context=_context)
        if _token == 'ID':
            ID = self._scan('ID', context=_context)
            return skill.Symbol(ID)
        elif _token == 'OBJECT':
            OBJECT = self._scan('OBJECT', context=_context)
            return OBJECT
        elif _token == 'STR':
            STR = self._scan('STR', context=_context)
            return eval(STR)
        elif _token == 'INTNUM':
            INTNUM = self._scan('INTNUM', context=_context)
            return int(INTNUM)
        elif _token == 'FLOATNUM':
            FLOATNUM = self._scan('FLOATNUM', context=_context)
            return float(FLOATNUM)
        else: # == 'r"\\("'
            self._scan('r"\\("', context=_context)
            e = []
            while self._peek( context=_context) != 'r"\\)"':
                expr = self.expr(_context)
                e.append(expr)
            self._scan('r"\\)"', context=_context)
            return e


def parse(rule, text):
    P = skillparser(skillparserScanner(text))
    return runtime.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
