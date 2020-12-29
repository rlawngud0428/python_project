import requests

res = requests.get("https://www.google.co.kr/")
res.raise_for_status() # 문제가 있으면 탈출 하는 아래의 if-else문과 같은 기능
#print("response code : ", res.status_code) # 200 이면 정상

#if res.status_code == requests.codes.ok:
#    pass
#else:
#    print("problem,  [error code ", res.status_code, "]")

print(len(res.text))
print(res.text)

with open("mygoogle.html", "w", encoding="utf8") as f:
    f.write(res.text)