import math


myfile = open("output.txt", "r")
cypher_text = ""
while True:
    cc = myfile.readline()
    if not cc:
        break
    cypher_text+=cc

myfile.close()
ic_eng = 0.0686
r,c =100,100
def format(text):
    text = text.lower()
    cur = ""
    for i in range(0,len(text)):
        if((text[i]>='a' and text[i]<='z') or (text[i]>='A' and text[i]<='Z')):
            cur+=text[i]

    return cur

def guess_length(text):
    length,d = 0,0.0
    #guess length using the IC value.Length with high IC value will be more accurate as a key length
    for i in range(2,36):
        now = get_ic(text,i)
        if( now>d):
            d,length = now,i
    return length

def get_ic(text,n):
    #n = length
    s=0
    coset = [ [ '' for x in range(r) ] for y in range(c) ]
    #extract the coset.Find IC for each coset using ic() function
    for i in range(0,n):
        for j in range(i,len(text),n):
            coset[i]+=text[j]
        now = ''.join(map(''.join, coset[i]))
        s+=ic(now)

    return s/n

#retuen IC value 'text'
def ic(text):
    ln = len(text)
    cnt = [0]*30
    for i in range(0 ,len(text)):
        cnt[ord(text[i])-97]+=1
    a = 0.0
    for i in range(0,26):
        a+=(cnt[i]*(cnt[i]-1))

    ret = a/(ln*(ln-1))
    # for i in range(0,26):
    #     print("{}={}".format(chr(97+i),cnt[i]))
    return ret


global_freq=[ 0.082, 0.014, 0.028, 0.038, 0.131, 0.029, 0.020, 0.053, 0.064, 0.001, 0.004, 0.034, 0.025,
             0.071, 0.080, 0.020, 0.001, 0.068, 0.061, 0.105, 0.025, 0.009, 0.015, 0.002, 0.020, 0.001 ]

def guess_key(key_len,text):
    s = 0
    ans = ""
    coset = [ [ '' for x in range(r) ] for y in range(c) ]
    # extract the coset.Find minimum x^2 valure for each coset using get_min_xx() function
    for i in range(0, key_len):
        for j in range(i, len(text), key_len):
            coset [ i ] += text [ j ]
        now = ''.join(map(''.join, coset [ i ]))
        mn_xx = get_min_xx(now)
        ans+=chr(97+mn_xx)

    return ans

def get_min_xx(text):
     ln = len(text)
     cnt = [ 0 ] * 30
     for i in range(0,ln):
         cnt[ord(text[i])-97]+=1
        # print(chr(97+i),cnt[i])
     shift,mn = 0,1000.0
     for i in range(0,26):
         s=0
         temp = [0]*30
         for j in range(0,26):
             d = j-i;
             d%=26;d+=26;d%=26 #multiple line inside one line
             temp[d] = cnt[j]/ln

         for j in range(0,26):
             d = temp[j]-global_freq[j]
             d*=d
             d/=global_freq[j]
             s+=d
            # print(chr(97+j),temp[j],global_freq[j],d,s)
         if(s<mn):
             shift,mn = i,s
     return shift
def Decode(text,key):
    ans =""
    t_ln,k_len = len(text),len(key)
    for i in range(0,t_ln):
        n = (ord(text[i])-97)
        n-=(ord(key[i%k_len])-97)
        n+=26
        n%=26
        ans+=chr(97+n)

    return ans

def divisor(n):
    div = []
    t = int(math.sqrt(n))
    for i in range (1,t+1):
        if(n%i==0):
            if(i!=1):
                div.append(i)
            if(i*i!=n):
                div.append(n//i)
    div.sort()
    return div

def check_accuracy(key,flag):
    file1 = open("input.txt","r")
    actual_text = "";
    while True:
        cc = file1.readline()
        if not cc:
            break
        actual_text+=cc

    actual_text = format(actual_text)
    recovered_text = Decode(cypher_text,key);
    ln = len(actual_text)
    #print(len(actual_text),len(recovered_text))
    if(flag==1):
        print("Actual Text::> \n    {} \n\nPredicted Text::> \n    {}".format(actual_text, recovered_text))
    c = 0

    for i in range(0,ln):
        if(actual_text[i]!=recovered_text[i]):
            c+=1

    if(flag==1):
        print("Accuracy = {}%".format((ln - c) * 100 / ln))
    return (ln-c)*100/ln

#Unnecessary character remove

cypher_text = format(cypher_text)
key_length = guess_length(cypher_text)
arr = divisor(key_length)
cur_key=""
cur_acc=0
for i in range(0,len(arr)):
    predicted_key = guess_key(arr[i], cypher_text)
    acc = check_accuracy(predicted_key,0)
   # print(arr[i],acc,cur_acc,predicted_key)
    if(acc>cur_acc):
        curr_acc,cur_key,cur_length = acc,predicted_key,arr[i]


print("Predicted Key ::> {}\n".format(cur_key))
check_accuracy(cur_key,1)

#check_accuracy(predicted_key)

