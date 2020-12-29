#import unitest

#class Test1():

def regex_test():
    import re 
    import rstr

    email_strs = [
        'a@hotmail.com',
        'a@outlook.fr',
        'a@hotmail.xor',
        'AAoutlook@hotmail.com',
        'trixa@hotmail#com',
        'trixa#hotmail.com'
    ]

    pwd_strs = [
        'a',
        'A',
        '2',
        'a++4',
        'a++',
        'AA+aZZ',
        'xS$4',
        '000000000000000000000000000000000000000000000000000000000000000000',
        'asd45adaSDsdf__sda6554545452ddd454542____AASsJHGJHG'

    ]


    
    email_regex = r'[a-zA-Z0-9_]+(@)(hotmail|outlook)(\.)(com|fr)'
    pwd_regex = r'(?=.*[0-9]{1}.*)(?=.*[a-z]{1}.*)(?=.*[A-Z]{1}.*)(?=.*[_]{1}.*)([a-zA-Z0-9_+$]{4,60})'
    



    for i in email_strs:
        print(i, " >> " , re.match(email_regex, i))
    for i in range(5):
        print(i, ' : ', rstr.xeger(email_regex))
    
    for i in pwd_strs:
        print(i, " >> " , re.match(pwd_regex, i))
    for i in range(15):
        break
        print(i, ' : ', rstr.xeger(pwd_regex))
    



regex_test()