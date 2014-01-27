def roundStr(s, sigfig):
    padding = len(s) - sigfig - 1
    floatstring = s[:sigfig] + "." + s[sigfig:]
    d = float(floatstring)
    d = float(round(d))
    d = str(d).split(".")[0] + str(d).split(".")[1] + "0" * padding
    return d
print(roundStr("0.1101",1))