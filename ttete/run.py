# -----------------------------------------------------------------------------
# @author globit
# This is template code of markdown generating by ply
# @update 2014-12-16
# @lience MIT
# -----------------------------------------------------------------------------
import sys

tokens = (
    'H1','H2','H3', 'CR', 'TEXT','STRONG','SYMBOL','EM','HR','H','CODE','LBRAC','RBRAC','LBOXBRAC','RBOXBRAC','LANGLEBRAC','RANGLEBRAC'
    )

# Tokens
t_H1 = r'\# '
t_H2 = r'\#\# '
t_H3 = r'\#\#\# '

t_STRONG = r'\*\* |\_\_'

t_SYMBOL = r'[\,\.\!\?\:\;\/]'

t_EM = r'\* |\_'

t_HR = r'\-\-\- '

t_H = r'\=\=\='

t_CODE = r'\`'

t_LBRAC = r'\('

t_RBRAC = r'\)'

t_LBOXBRAC = r'\['

t_RBOXBRAC = r'\]'

t_LANGLEBRAC = r'\<'

t_RANGLEBRAC = r'\>'

def t_TEXT(t):
    r'[a-zA-Z0-9\'\ ]+'
    t.value = str(t.value)
    return t

t_ignore = " \t"

def t_CR(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# ------------------------------------
# definitions of parsing rules by yacc
# ------------------------------------
precedence = (
    )
names = {}

def p_body(p):
    '''body : statement'''
    print '<body>' + p[1] + '</body>'

def p_state(p):
    '''statement : expression
            | statement CR expression'''
    if (len(p)==2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = str(p[1]) + str(p[3])

def p_exp_cr(p):
    '''expression : phrase
                | H1 phrase
                | H2 phrase
                | H3 phrase
                | HR
                | H
                | hr'''
    if p[1] == '#':
        p[0] = '<h1>' + str(p[2]) + '</h1>'
    elif p[1] == '##':
        p[0] = '<h2>' + str(p[2]) + '</h2>'
    elif p[1] == '###': 
        p[0] = '<h3>' + str(p[2]) + '</h3>'
    elif p[1] == '---':
        p[0] = '<hr/>'
    elif p[1] == '===': 
        p[0] = '<h1></h1>'
    elif p[1] == '***':
        p[0] = '<hr/>'
    elif (len(p) == 2):
        p[0] = '<p>' + str(p[1]) + '</p>'

def p_phrase(p):
    '''phrase : factor
                | phrase factor
                | phrase SYMBOL
                | phrase phrase
                | strong_fact STRONG
                | em_fact EM
                | code_fact CODE
                | anglebrac_fact RANGLEBRAC'''
    if (len(p) == 2):
        p[0] = str(p[1])
    elif p[2] == '**' or p[2] == '__':
        p[0] = '<strong>' + str(p[1]) + '</strong>'
    elif p[2] == '*' or p[2] == '_':
        p[0] = '<em>' + str(p[1]) + '</em>'
    elif p[2] == '`':
        p[0] = '<code>' + str(p[1]) + '</code>'
    elif p[2] == '>':
        p[0] = '<a href="' + str(p[1]) + '">' + str(p[1]) + '</a>'
    elif (len(p) == 3):
        p[0] = str(p[1]) + str(p[2])

def p_strong_fact(p):
    '''strong_fact :  strong_fact factor
                    | STRONG factor'''
    if p[1] == '**' or p[1] == '__':
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + str(p[2])

def p_em_fact(p):
    '''em_fact :  em_fact factor
                | EM factor'''
    if p[1] == '*' or p[1] == '_':
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + str(p[2])

def p_hr(p):
    ''' hr : EM EM
           | hr EM'''
    p[0] = str(p[1]) + str(p[2])

def p_code_fact(p):
    '''code_fact :  code_fact factor
                | CODE factor'''
    if p[1] == '`':
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + str(p[2])

def p_anglebrac_fact(p):
    '''anglebrac_fact :  anglebrac_fact factor
                | LANGLEBRAC factor'''
    if p[1] == '<':
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + str(p[2])

#def p_name_fact(p):
 #   '''name_fact :  name_fact factor
  #              | LBOXBRAC factor'''
#    if p[1] == '[':
  #      p[0] = str(p[2])
#    else:
  #     p[0] = str(p[1]) + str(p[2])

#def p_name(p):
 #   '''name :  name_fact RBOXBRAC'''
  #      p[0] = str(p[1])

def p_factor_text(p):
    "factor : TEXT"
    p[0] = p[1]

def p_error(p):
    if p:
        print("error at '%s' line '%d'" % (p.value, p.lineno))
    else:
        print("error at EOF")

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    filename = 'test233.md'
    yacc.parse(open(filename).read())