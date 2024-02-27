import re 
txt = "The rain in Spain"
x = re.search(r"\bs\w+", txt)
print(x.group())
