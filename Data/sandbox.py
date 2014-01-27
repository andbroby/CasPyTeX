<<<<<<< HEAD
def roundStr(s, sigfig):
    padding = len(s) - sigfig - 1
    floatstring = s[:sigfig] + "." + s[sigfig:]
    d = float(floatstring)
    d = float(round(d))
    d = str(d).split(".")[0] + str(d).split(".")[1] + "0" * padding
    return d
print(roundStr("0.1101",1))
=======
f=open(r"C:\Users\Esben\home\CAS-v3\Data\Bestemmelse af stamfunktion med tangent.cpt")
print(f.readlines())
>>>>>>> eeb6c6fd199fa488e63a7b783e17320f42ab50b4
