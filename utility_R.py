
from rpy2 import robjects

def invoke_R(code_input):
    result = robjects.r(code_input.code)
    return result