__author__ = 'yluo'

"""
Simple SQL parser, inspired a lot by
https://github.com/kmanley/redisql/blob/master/sqlparser.py
"""

import sys
# Build the lexer
import ply.lex as lex

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
    'insert': 'INSERT',
    'into': 'INTO',
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'order': 'ORDER',
    'by': 'BY',
    'values': 'VALUES',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
}


tokens = ['NAME', 'COMMA', 'SEMI', 'EQUAL'] + list(reserved.values())

t_COMMA = r'\,'
t_SEMI = r';'
t_EQUAL = r'='

t_ignore = " \t"

def t_NAME(t):
    r'[a-zA-Z0-9\./\*\$]+'
    t.type = reserved.get(t.value,'NAME') # Check for reserved words
    t.value = t.value.lower()
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

import ply.yacc as yacc


def p_statement_assign(p):
    """
    assign_statement : NAME EQUAL select_statement
                    | select_statement
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])

def p_statement_select(p):
    """
    select_statement : SELECT attrlist FROM tablist opt_where_clause SEMI
    """
    p[0] = ('select', p[2], p[4], p[5])

def p_statement_opt_where(p):
    """
    opt_where_clause : WHERE condition_list
                     |
    """
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = p[2]

def p_statement_condition_list(p):
    """
    condition_list : condition
                   | condition_list COMMA condition
    """
    if len(p) == 2:
       p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[3]]

def p_statement_condition(p):
    """
    condition : NAME EQUAL NAME
    """
    p[0] = (p[1],p[2],p[3])

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


def parse(ssql):
    return yacc.parse(ssql)


if __name__ == "__main__":
    query = 'select $1 from data;'
    # Give the lexer some input
    lexer.input(query)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

    print(yacc.parse(query))