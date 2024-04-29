
from rpy2 import robjects

def invoke_R(code):
    r = robjects.r
    result = r(code)
    return result,r