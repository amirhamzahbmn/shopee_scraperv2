import httpx
import asyncio
import pandas as pd

my_headers = {
    "cookie": "SPC_R_T_ID=bBhqfx%2FUGA71Crgq3xiJYiI7%2Fi2DLrSZdfarZkss8wHmeL021OIHw3QDXEhYnimNGU06YeLaOlmi8Ynco3VlLbW8W9EY505S9ZN0Hx4yz9%2BGpEFImxlfzhgsiVydByN3YjNagTYLDuPHIgsKefCVV1tZYOuCXuGsQtHthkR%2BETM%3D; SPC_R_T_IV=NTZSVU91ZVZOMExMVHoxMA%3D%3D; SPC_T_ID=bBhqfx%2FUGA71Crgq3xiJYiI7%2Fi2DLrSZdfarZkss8wHmeL021OIHw3QDXEhYnimNGU06YeLaOlmi8Ynco3VlLbW8W9EY505S9ZN0Hx4yz9%2BGpEFImxlfzhgsiVydByN3YjNagTYLDuPHIgsKefCVV1tZYOuCXuGsQtHthkR%2BETM%3D; SPC_T_IV=NTZSVU91ZVZOMExMVHoxMA%3D%3D; SPC_SI=dcN1ZAAAAABhTXJOa0tUWL7XdQAAAAAAV2VYNlZDMGo%3D; SPC_ST=.VUMyS0JQeFRCN0VKT1pneV7NlAqc%2BDknM42GnsbxN955GiRH47PwICJAoy0m6SsD8RX7dprFwdvlH742bZd%2FOqcU4m6x0Jj0FdZuAMOxSP%2BebbHeDr3mdtHdTgawHjN944%2F8UXLQ%2Bmmf83W%2FkGjcysPYeuZ%2BddXRp8J9NJjyiulQ1Bc4q1ELPuUjZIJA9KUvfOl994DPTsDcYMN%2BRaiZrw%3D%3D; SPC_U=1010837601; SPC_EC=ZnBTZVZ3cW01QU82OUhPY3OK31dCXWcArw7u7moh1QqeW8lplJroDS1zz0snAAsm41lmJJpACvb%2FzmPHd%2BSONEbKPwDBqztR6ZMtnTeMv95XR8nxsQqLJUyQy%2FR0FmML4ltEJkT7nLYoeSaRtLjiHNlD7S1bhBse8lNbXx4RsYc%3D",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://shopee.com.my/Ready-Stock*Added-New-Design-Air-Force-One-Inspired-Gold-TIck-Shoes-Unisex-Sneakers-Kasut-i.325896901.9637408483?sp_atk=d05d579d-6e67-4096-b49b-b58d7ac699bc&xptdk=d05d579d-6e67-4096-b49b-b58d7ac699bc",
    "Content-Type": "application/json",
    "X-Shopee-Language": "en",
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRFToken": "LNJpFXT5D9zvF77hLioVwEId93qFXBxH",
    "X-API-SOURCE": "pc",
    "af-ac-enc-dat": "AAcyLjguMS0yAAABiHu/3BcAAA6bAsAAAAAAAAAAAlkZhtf7pEceq32saQqA3lseui2aV02tC8ezc74AmWOzHRMB8Ik4+ERj22ILMYz0Kg4taH3a/ZuAmaWXDlPerw1CJnYnFKipLSKevyS5IfkiJmYaXxcJdhb4/uV0SP1xNfvLlvTQwPf/ZRmHUX+PMCqtET+H+HxlNmpkWQZgeFHZL6YtHnmTG0FAfkkwZR50dvWS/1SKs/55E89SjTHqpQyPZepR+zJpMhAks1JVB6ma0WDCzBq3aqGSLC56rwm58jQuQZcNzzAdvrv+J9bh7nrwctkSZZrP9rhYAhnvXTsGZZ6gQaHxc0CILFQHX1IFHeWrYWCX/zYTJ8PH9tVFw9ppG9ibKVfibIqudCanr1dNXpn4nf30YKvRFJLaLQheesCU7TJlY93RkmaRFGufHppkmgWs8XkKvZyf6PMSeqaiu+UhSFcFfU2o6Vn8iYxHWk3NX+CVL6NKiA9e1Jo1H8wjLl9c8kJZb/sGC2yFoUaV2OTH4yJEwg8yu+rg54PrmwsULfmUEXCc2FBelMOoShMOcm244JVbJGvCZ9rEXQAZa9q3IC5tBmCB3tv3kCPBTq0vKeYLDV7bORsgIyPL5xiLbtjT5rk4xCLUS8sAu7aF/GKClcLFzTWE8itx0swhqFf+AV1HJH5/2qmdhFATAtz74Bv1vttRNmxj+JZ2UESU7690suLSelFhA39V1/1uX3yYo2dHJH5/2qmdhFATAtz74Bv10tHSJWlKdVtCR9ZczasByKM8WzXdLAcdBp566Yci+sJcqjywJ/hF/zOo/59kkDOYIlilDLyUbl+R4QOURfZZ0PBlr9OCKxkcww2cVgPUV1YFrJXBLIZp804PiVP/mqdW9hR4awAOseHq2fNMH4TMxZTUhTLGwEKkFK8EG6CVow6aPMZxtLXsI3RlekA1Mg3+QTRh6XCTaMrRR8fW+OBTYg==",
    "sz-token": "6ZaBjp2qgg//yWO4EZnFbw==|GK8oK/JJZQP5dgNdWWFVqdhe+zU686zNR5TTBAbyUOjpAGFcde+GC8iABVa0JxFM4MLmSVT2oCuPJGwZv3x3h7dsTgoNbystEgU=|81oPLombFCW5LTrl|06|3",
    "x-sz-sdk-version": "2.8.1-2@1.2.1",
    "af-ac-enc-sz-token": "6ZaBjp2qgg//yWO4EZnFbw==|GK8oK/JJZQP5dgNdWWFVqdhe+zU686zNR5TTBAbyUOjpAGFcde+GC8iABVa0JxFM4MLmSVT2oCuPJGwZv3x3h7dsTgoNbystEgU=|81oPLombFCW5LTrl|06|3",
    "5b657584": ";6e7b%HjP#&r!fi<j)<://YBV",
    "daaf8c8c": "O:NfV!McKI6YikSB&6FQIg1Ga",
    "x-sap-ri": "b8ca79646d9f6a8a5ade163d556d987f75fb5d78f83b8f51",
    "b7705446": """CSW9Eb*`IphO"N.N:%GI3X(VJWAMcdUL>G?W"9[-n\\n>(W^`32Vs,/SQo``t4dU=:M\041V%4:s\\RDF?[j:a'&>37V)#c+@\\oD`EMPFPj22BgKQ*I\\,r,iMC_C&I`FcV/\\%+ZJa5LOg#_4IFLV@)%or"^jr9;8H5sVY"7#)NQjA#eO_t4;\0414C9@\041QNVAdiH2X0`j@]NaY"H,uuHBQb=&0h2bdR*G;K#-E_YA'rPVXrKl\041@+;o/*ZnNUFIp+G?JI#\\.h4h`HXR1\\1s$mF>KV>6eAa:-V(o@[9\041K0ElQN$*\\2p'-`9FFpIb2,Sca#'+kQm9b"`8KP6`l\041Y"(oLM_1=.<%"8p@@I&1FFgA@Hd^d[\\3""",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": "__LOCALE__null=MY; csrftoken=LNJpFXT5D9zvF77hLioVwEId93qFXBxH; SPC_SI=dcN1ZAAAAABhTXJOa0tUWL7XdQAAAAAAV2VYNlZDMGo=; SPC_T_IV=NTZSVU91ZVZOMExMVHoxMA==; SPC_F=nzudzhvZhHDGtP2LkYLORMO1daX8QS6J; REC_T_ID=fb0f300d-0132-11ee-bc99-c2348b454c36; SPC_R_T_ID=bBhqfx/UGA71Crgq3xiJYiI7/i2DLrSZdfarZkss8wHmeL021OIHw3QDXEhYnimNGU06YeLaOlmi8Ynco3VlLbW8W9EY505S9ZN0Hx4yz9+GpEFImxlfzhgsiVydByN3YjNagTYLDuPHIgsKefCVV1tZYOuCXuGsQtHthkR+ETM=; SPC_R_T_IV=NTZSVU91ZVZOMExMVHoxMA==; SPC_T_ID=bBhqfx/UGA71Crgq3xiJYiI7/i2DLrSZdfarZkss8wHmeL021OIHw3QDXEhYnimNGU06YeLaOlmi8Ynco3VlLbW8W9EY505S9ZN0Hx4yz9+GpEFImxlfzhgsiVydByN3YjNagTYLDuPHIgsKefCVV1tZYOuCXuGsQtHthkR+ETM=; _QPWSDCXHZQA=4b77acce-dcc3-481d-ac52-1fdc0a20782a; language=en; shopee_webUnique_ccd=6ZaBjp2qgg%2F%2FyWO4EZnFbw%3D%3D%7CGK8oK%2FJJZQP5dgNdWWFVqdhe%2BzU686zNR5TTBAbyUOjpAGFcde%2BGC8iABVa0JxFM4MLmSVT2oCuPJGwZv3x3h7dsTgoNbystEgU%3D%7C81oPLombFCW5LTrl%7C06%7C3; ds=1709229d5de99e052e10e7aa2a0517cf; SPC_ST=.VUMyS0JQeFRCN0VKT1pneV7NlAqc+DknM42GnsbxN955GiRH47PwICJAoy0m6SsD8RX7dprFwdvlH742bZd/OqcU4m6x0Jj0FdZuAMOxSP+ebbHeDr3mdtHdTgawHjN944/8UXLQ+mmf83W/kGjcysPYeuZ+ddXRp8J9NJjyiulQ1Bc4q1ELPuUjZIJA9KUvfOl994DPTsDcYMN+RaiZrw==; SPC_CLIENTID=bnp1ZHpodlpoSERHrloudnqrydnrrxus; SPC_EC=dXl4OWpzb01LOXZEbmQzVo+ZKtA1ueErb3wu6O8jrZKy2ROKOc63uTpwoYSgLzMebelwxxBV7TgjSwJWIXX05jrGFlkpq/gp4+CeYsl0WI6M+xCDYPxAhGgCxft8uJZ2rpDHUV7Bh1bxH9LqfsiQTpBjOLRsMkc3E5srRU4qYnc=; SPC_U=1010837601",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

df = pd.read_csv("products.csv", usecols=['itemid','shopid'])
ids = df.values.tolist()

writecount = 10
doneids = []
try:
    donedf = pd.read_csv("productsv2test.csv", usecols=['itemid'])
    doneids = donedf['itemid'].tolist()
except:
    print('No file found')

print(f"Found {len(doneids)} products in csv file.")
task_count = len(doneids)

def write_to_csv(product_list):
    print(f"Writing into csv..")
    product_list_out = pd.json_normalize(product_list)
    if task_count == writecount:
        product_list_out.to_csv('productsv2test.csv', mode='a', index=False) 
    else:
        product_list_out.to_csv('productsv2test.csv', mode='a', header=False, index=False)

async def fetch_itemdata(count, product_list, url, client):
    while True:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                global task_count
                task_count += 1
                print(f'{task_count}. getting {url} product {count+1}/{df.shape[0]}')
                data = response.json()
                product_list.append(data['data'])
                if task_count % writecount == 0:
                    write_to_csv(product_list)
                    product_list.clear()
                break
        except Exception as e:
            print(f"Error occurred: {e}")


async def main():

    async with httpx.AsyncClient(headers = my_headers, limits=httpx.Limits(max_connections=500)) as client:
        tasks = []
        for count, id in enumerate(ids):
            if id[0] in doneids:
                continue 
            else:
                if count == len(doneids) + 500:
                    break
                url = f"https://shopee.com.my/api/v4/item/get?shopid={id[1]}&itemid={id[0]}"
                task = asyncio.ensure_future(fetch_itemdata(count, product_list, url, client))
                tasks.append(task)

        await asyncio.gather(*tasks)

product_list = []
asyncio.run(main())
