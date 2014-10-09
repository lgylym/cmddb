# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
# Build the lexer
import ply.lex as lex
#sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
'insert' : 'INSERT',
'into' : 'INTO',
'select' : 'SELECT',
'from' : 'FROM',
'where' : 'WHERE',
'order' : 'ORDER',
'by' : 'BY',
'values' : 'VALUES',
'and' : 'AND',
'or' : 'OR',
'not' : 'NOT',
}


tokens = [
    'NAME', 'COMMA', 'SEMI'
         ] + list(reserved.values())

#literals = [';',',']

t_COMMA = r'\,'
t_SEMI = r';'

t_ignore = " \t"

# Tokens

def t_NAME(t):
    r'[a-zA-Z0-9:/]+'
    t.type = reserved.get(t.value,'NAME') # Check for reserved words
    # redis is case sensitive in hash keys but we want the sql to be case insensitive,
    # so we lowercase identifiers
    t.value = t.value.lower()
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


#names = {}

import ply.yacc as yacc


def p_statement_select(p):
    'statement : SELECT attrlist FROM tablist SEMI'
    p[0] = ('select', p[2],p[4])

def p_statement_attr(p):
    """
    attrlist : NAME
             | attrlist COMMA NAME
    """
    if len(p) == 2:
       p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[3]]

def p_statement_tablist(p):
    """
    tablist : NAME
            | tablist COMMA NAME
    """
    if len(p) == 2:
       p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[3]]

yacc.yacc()

# Test it out
data = '''
select a:1,b:2 from /rrr/data1,data2;
'''

result = yacc.parse(data)

print(result)

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok

# # Parsing rules
#
# precedence = (
#     ('left','+','-'),
#     ('left','*','/'),
#     ('right','UMINUS'),
#     )
#
# # dictionary of names
# names = { }
#
# def p_statement_assign(p):
#     'statement : NAME "=" expression'
#     names[p[1]] = p[3]
#
# def p_statement_expr(p):
#     'statement : expression'
#     print(p[1])
#
# def p_expression_binop(p):
#     '''expression : expression '+' expression
#                   | expression '-' expression
#                   | expression '*' expression
#                   | expression '/' expression'''
#     if p[2] == '+'  : p[0] = p[1] + p[3]
#     elif p[2] == '-': p[0] = p[1] - p[3]
#     elif p[2] == '*': p[0] = p[1] * p[3]
#     elif p[2] == '/': p[0] = p[1] / p[3]
#
# def p_expression_uminus(p):
#     "expression : '-' expression %prec UMINUS"
#     p[0] = -p[2]
#
# def p_expression_group(p):
#     "expression : '(' expression ')'"
#     p[0] = p[2]
#
# def p_expression_number(p):
#     "expression : NUMBER"
#     p[0] = p[1]
#
# def p_expression_name(p):
#     "expression : NAME"
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print("Undefined name '%s'" % p[1])
#         p[0] = 0
#
# def p_error(p):
#     if p:
#         print("Syntax error at '%s'" % p.value)
#     else:
#         print("Syntax error at EOF")
#
# import ply.yacc as yacc
# yacc.yacc()
#
# while 1:
#     try:
#         s = raw_input('calc > ')
#     except EOFError:
#         break
#     if not s: continue
#     yacc.parse(s)
