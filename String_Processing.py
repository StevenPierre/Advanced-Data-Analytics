text = "sgtEEEr2020.0"
text.isalpha()
text.isdigit()
text.isalpha()
text.isspace()
text.islower()
text.isupper()
text.isnumeric()

def is_ssn (s):
    parts = s.split('-')
    correct_lengths = [3, 2, 4]
    if len(parts) != len(correct_lengths):
        return False
    for p, n in zip(parts, correct_lengths):
        if not (p.isdigit() and len(p) == n):
            return False
    return True

assert is_ssn ('832-38-1847')
assert not is_ssn ('832 -38 -  1847')
assert not is_ssn ('832-bc-3847')
assert not is_ssn ('832381847')
assert not is_ssn ('8323-8-1847')
assert not is_ssn ('abc-de-ghij')
print("\n(Passed!)")

import re
pattern = 'fox'
pattern_matcher = re.compile (pattern)

input = 'The quick brown fox jumps over the lazy dog'
matches = pattern_matcher.search (input)
print (matches)

print (matches.group ())
print (matches.start ())
print (matches.end ())
print (matches.span ())

matches_2 = re.search ('jump', input)
assert matches_2 is not None
print ("Found", matches_2.group (), "@", matches_2.span ())

# Make the above more readable with a re.VERBOSE pattern
re_names2 = re.compile ('''^              # Beginning of string
                           ([a-zA-Z]+)    # First name
                           \s             # At least one space
                           ([a-zA-Z]+\s)? # Optional middle name
                           ([a-zA-Z]+)    # Last name
                           $              # End of string
                        ''',
                        re.VERBOSE)
print (re_names2.match ('Rich Vuduc').groups ())
print (re_names2.match ('Rich S Vuduc').groups ())
print (re_names2.match ('Rich Salamander Vuduc').groups ())

# Named groups
re_names3 = re.compile ('''^
                           (?P<first>[a-zA-Z]+)
                           \s
                           (?P<middle>[a-zA-Z]+\s)?
                           \s*
                           (?P<last>[a-zA-Z]+)
                           $
                        ''',
                        re.VERBOSE)
print (re_names3.match ('Rich Vuduc').group ('first'))
print (re_names3.match ('Rich S Vuduc').group ('middle'))
print (re_names3.match ('Rich Salamander Vuduc').group ('last'))

def parse_email (s):
    """Parses a string as an email address, returning an (id, domain) pair."""
    pattern = '''
       ^
       (?P<user>[a-zA-Z][\w.\-+]*)
       @
       (?P<domain>[\w.\-]*[a-zA-Z])
       $
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches:
        return (matches.group('user'), matches.group('domain'))
    raise ValueError("Bad email address")

def pass_case(u, d):
    s = u + '@' + d
    msg = "Testing valid email: '{}'".format(s)
    print(msg)
    assert parse_email(s) == (u, d), msg
    
pass_case('richie', 'cc.gatech.edu')
pass_case('bertha_hugely', 'sampson.edu')
pass_case('JKRowling', 'Huge-Books.org')

def fail_case(s):
    msg = "Testing invalid email: '{}'".format(s)
    print(msg)
    try:
        parse_email(s)
    except ValueError:
        print("==> Correctly throws an exception!")
    else:
        raise AssertionError("Should have, but did not, throw an exception!")
        
fail_case('x @hpcgarage.org')
fail_case('   quiggy.smith38x@gmail.com')
fail_case('richie@cc.gatech.edu  ')

def parse_phone1 (s):
    pattern = '''
       \s*
       \((?P<area>\d{3})\) # Area code
       \s*
       (?P<local3>\d{3}) # Local prefix (3 digits)
       -
       (?P<local4>\d{4}) # Local suffix (4 digits)
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches:
        return (matches.group('area'), matches.group('local3'), matches.group('local4'))
    raise ValueError("Invalid phone number? '{}'".format(s))
def rand_spaces(m=5):
    from random import randint
    return ' ' * randint(0, m)

def asm_phone(a, l, r):
    return rand_spaces() + '(' + a + ')' + rand_spaces() + l + '-' + r + rand_spaces()

def gen_digits(k):
    from random import choice # 3.5 compatible; 3.6 has `choices()`
    DIGITS = '0123456789'
    return ''.join([choice(DIGITS) for _ in range(k)])

def pass_phone(p=None, a=None, l=None, r=None):
    if p is None:
        a = gen_digits(3)
        l = gen_digits(3)
        r = gen_digits(4)
        p = asm_phone(a, l, r)
    else:
        assert a is not None and l is not None and r is not None, "Need to supply sample solution."
    msg = "Should pass: '{}'".format(p)
    print(msg)
    p_you = parse_phone1(p)
    assert p_you == (a, l, r), "Got {} instead of ('{}', '{}', '{}')".format(p_you, a, l, r)
    
def fail_phone(s):
    msg = "Should fail: '{}'".format(s)
    print(msg)
    try:
        p_you = parse_phone1(s)
    except ValueError:
        print("==> Correctly throws an exception.")
    else:
        raise AssertionError("Failed to throw a `ValueError` exception!")


# Cases that should definitely pass:
pass_phone('(404) 121-2121', '404', '121', '2121')
pass_phone('(404)121-2121', '404', '121', '2121')
for _ in range(5):
    pass_phone()
    
fail_phone("404-121-2121")
fail_phone(" ( 404)121-2121")
fail_phone("(abc) def-ghij")

def parse_phone2(s):
    pattern = '''
        ^\s*               # Leading spaces
        (?P<areacode>
           \d{3}-?         # "xxx" or "xxx-"
           | \(\d{3}\)\s*  # OR "(xxx) "
        )
        (?P<prefix>\d{3})  # xxx
        -?                 # Dash (optional)
        (?P<suffix>\d{4})  # xxxx
        \s*$               # Trailing spaces
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches is None:
        raise ValueError("'{}' is not in the right format.".format (s))
    areacode = re.search('\d{3}', matches.group ('areacode')).group()
    prefix = matches.group ('prefix')
    suffix = matches.group ('suffix')
    return (areacode, prefix, suffix)

# Test cell: `parse_phone2_test`

def asm_phone2(a, l, r):
    from random import random
    x = random()
    if x < 0.33:
        a2 = '(' + a + ')' + rand_spaces()
    elif x < 0.67:
        a2 = a + '-'
    else:
        a2 = a
    y = random()
    if y < 0.5:
        l2 = l + '-'
    else:
        l2 = l
    return rand_spaces() + a2 + l2 + r + rand_spaces()

def pass_phone2(p=None, a=None, l=None, r=None):
    if p is None:
        a = gen_digits(3)
        l = gen_digits(3)
        r = gen_digits(4)
        p = asm_phone2(a, l, r)
    else:
        assert a is not None and l is not None and r is not None, "Need to supply sample solution."
    msg = "Should pass: '{}'".format(p)
    print(msg)
    p_you = parse_phone2(p)
    assert p_you == (a, l, r), "Got {} instead of ('{}', '{}', '{}')".format(p_you, a, l, r)
    
pass_phone2("  (404)   555-1212  ", '404', '555', '1212')
pass_phone2("(404)555-1212  ", '404', '555', '1212')
pass_phone2("  404-555-1212 ", '404', '555', '1212')
pass_phone2("  404-5551212 ", '404', '555', '1212')
pass_phone2(" 4045551212", '404', '555', '1212')
    
for _ in range(5):
    pass_phone2()
    
    
def fail_phone2(s):
    msg = "Should fail: '{}'".format(s)
    print(msg)
    try:
        parse_phone2 (s)
    except ValueError:
        print ("==> Function correctly raised an exception.")
    else:
        raise AssertionError ("Function did *not* raise an exception as expected!")
        
failure_cases = ['+1 (404) 555-3355',
                 '404.555.3355',
                 '404 555-3355',
                 '404 555 3355'                 
                ]
for s in failure_cases:
    fail_phone2(s)
    
print("\n(Passed!)")


