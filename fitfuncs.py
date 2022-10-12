import numpy as np

def x_deg(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * x ** deg
    return ret

def x_deg_sin_x(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * x ** deg * np.sin(x)
    return ret

def x_sin_x(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * x * np.sin(x)
    return ret

def sin_x(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * np.sin(x)
    return ret

def log_x__sin_x(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * np.log(x) ** np.sin(x)
    return ret

def log_x_sin_x(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * np.log(x) * np.sin(x)
    return ret

def x__1_sin_x(x,*a):
    ret = a[0]
    for deg in range(1,len(a)):
        ret += a[deg] * x ** (1/np.sin(x))
    return ret



