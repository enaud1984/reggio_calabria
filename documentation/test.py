import pickle
import sys
from io import StringIO
from store import Data
import os
# Funzione per catturare l'output di print()
def capture_output(func):
    # Crea un oggetto StringIO
    output = StringIO()
    # Sovrascrivi sys.stdout con l'oggetto StringIO
    sys.stdout = output
    # Esegui la funzione
    func()
    # Ripristina sys.stdout
    sys.stdout = sys.__stdout__
    # Restituisci l'output catturato come stringa
    return output.getvalue()

# Codice da eseguire
code_to_execute = """
import sys
from io import StringIO
 # Crea un oggetto StringIO
output = StringIO()
# Sovrascrivi sys.stdout con l'oggetto StringIO
sys.stdout = output
# Esegui la funzione
def my_function():
    print("Hello, world!")
    a=c
    b=12*a
    return a,b
a,b = my_function()
print("risultato ",a,b)
print("comuni ",comuni.columns)
ciccio=comuni
sys.stdout = sys.__stdout__
"""
output = {}
#header ="""


input = Data(["comuni","condotte"]).input
# Esegui il codice con exec()
input.update({"c":12})
""" 
exec(header,{},output)
input=output["input"]
#"""
output = {}
exec(code_to_execute,input,output)

# Cattura l'output della funzione my_function()
captured_output = output["output"].getvalue()

# Stampalo
print("Output catturato:", captured_output)