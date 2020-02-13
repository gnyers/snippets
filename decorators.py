#!/usr/bin/env python3

'''
Simple decorators
'''

## Markup

def bold(origfunc):
    def bold_wrapper(*args, **kwargs):
        return '<b>{}</b>'.format( origfunc(*args, **kwargs) )
    return bold_wrapper

def italic(origfunc):
    def italic_wrapper(*args, **kwargs):
        return '<i>{}</i>'.format( origfunc(*args, **kwargs) )
    return italic_wrapper

def shout(origfunc):
    def shout_wrapper(*args, **kwargs):
        ret = origfunc(*args, **kwargs)
        return '{}!!!'.format(ret.upper())
    return shout_wrapper

@italic
def say_in_italic(text):
    return text

@bold
@shout
def shout_in_bold(text):
    return text



## Separation of concerns:
persons = [
    ['username', 'full_name', 'show', 'gendergroup', 'agegroup'],
    ['fred', 'Fred Flintstone', 'flintstones', 'm', 'adults'],
    ['wilma', 'Wilma Flintstone', 'flintstones', 'f', 'adults'],
    ['pebbles', 'Pebbles Flintstone', 'flintstones', 'f', 'kids'],
    ['barney', 'Barney Rubble', 'flintstones', 'm', 'adults'],
    ['betty', 'Betty Rubble', 'flintstones', 'f', 'adults']
]

def auth(origfunc):
    '''Decorate any function to require authentication; in this case the
    secret: 'secret'
    '''
    def auth_wrapper(*args, **kwargs):
        if input('Enter secret: ') == 'secret':
            return origfunc(*args, **kwargs)
        else:
            print('Nooo...!')
            return None
    return auth_wrapper

def search(name):
    '''Find record in `persons`, who's `username` field equals `name`.
    '''
    for username, full_name, *rest in persons:
        if name == username: return full_name
    return None

@auth
def search2(name):
    for username, full_name, *rest in persons:
        if name == username: return full_name
    return None

@auth
@bold
def search3(name):
    for username, full_name, *rest in persons:
        if name == username: return full_name
    return None


def lookup0(idx):
    return persons[idx]

import json
def as_json(origfunc):
    '''Decorator function to format a function's return in JSON format
    '''
    def wrapper(*args, **kwargs):
        ret_l = origfunc(*args, **kwargs)
        d = { 'header': persons[0] }
        d['data'] = ret_l
        return json.dumps(d)
    return wrapper

@as_json
def lookup_as_json(idx):
    '''Decorated function to return a record from `persons` as JSON, incl.
    headers.

    Result of decorator: lookup_as_json = as_json(lookup0)
    Equivalent usage   : as_json(lookup0)(idx)
    '''
    return persons[idx]


def as_csv(delim=',', header=False):
    '''Decorator function to format a function's return as a CSV record.
    The to be decorated function's return value assumed to be an interable.

    The decorator arguments:
    - delim: the delimiter charcter (optional, default value: ',')
    - header: output a header row (optional, default is False)
    '''
    def arg_wrapper(origfunc):
        def wrapper(*args, **kwargs):
            ret_l = origfunc(*args, **kwargs)
            ret_s = delim.join(ret_l)
            if header:
                ret_s = delim.join(persons[0]) + '\n' + ret_s
            return ret_s
        return wrapper
    return arg_wrapper


@as_csv
def lookup_as_csv1(idx):
    '''Decorated function to return a record from `persons` as CSV, delimited
    by ','

    Result of decorator: lookup_as_csv1 = as_csv()(lookup0)
    Equivalent usage   : as_csv()(lookup0)(idx)
    '''
    return persons[idx]

@as_csv(delim=';', header=True )
def lookup_as_csv2(idx):
    '''Decorated function to return a record from `persons` as CSV incl.
    header and delimiter char ';'

    Result of decorator: lookup_as_csv2 = as_csv(delim=';', header=True)(lookup0)
    Equivalent usage   : as_csv(delim=';', header=True)(lookup0)(idx)
    '''
    return persons[idx]

@auth
@as_csv(delim=';', header=True )
def lookup_as_csv_auth(idx):
    '''Decorated function to return a record from `persons` as CSV incl.
    header and delimiter char ';'. Authentication is required first though.

    Result of decorator: lookup_as_csv_auth = auth(as_csv)(delim=';', header=True)(lookup0)
    Equivalent usage   : auth(as_csv)(delim=';', header=True)(lookup0)(idx)
    '''
    return persons[idx]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 showbreak=… ruler
# vim: foldmethod=indent foldcolumn=4 wrap linebreak spelllang=en nospell
