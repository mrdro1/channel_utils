

def read_token():
    with open('token.ctl', 'r') as f:
        token = f.readline()
    return token

def read_login_pwd():
    with open('login_pwd.ctl', 'r') as f:
        login, pwd = f.readline().split(':')
    return login, pwd

#a = read_login_pwd()
#print(a)