

def read_token():
    with open('token.ctl', 'r') as f:
        token = f.readline()
    return token

a = read_token()
print(a)