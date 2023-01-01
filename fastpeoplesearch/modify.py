f = open("proxy.txt", "r")
val = f.read().split('\n')
out = ""
print(len(val))
for i in val:
    out+="http://"+i+"\n"
print(out)
f.close()

f = open("proxy_mod.txt", "a")
f.write(out)
f.close()