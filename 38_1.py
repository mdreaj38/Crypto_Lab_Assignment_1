myfile = open("input.txt", "r")
myfile2 = open("key.txt","r")
key = myfile2.readline()
text = ""
while True:
    cc = myfile.readline()
    if not cc:
        break
    text+=cc

myfile.close()

def format(text):
    text = text.lower()
    cur = ""
    for i in range(0,len(text)):
        if((text[i]>='a' and text[i]<='z') or (text[i]>='A' and text[i]<='Z')):
            cur+=text[i]

    return cur

def encode(text,key):
    ans =""
    t_ln,k_len = len(text),len(key)
    for i in range(0,t_ln):
        n = ord(text[i])-97
        n+=ord(key[i%k_len])-97
        n+=26
        n%=26
        ans+=chr(97+n)
    return ans

text = format(text)
key = format(key)
enc = encode(text,key)
print(enc)