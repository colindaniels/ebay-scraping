import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

def get_average(lst):
    sum = 0
    length = len(lst)
    for price in lst:
        sum = sum + price
    return round(sum/length, 2)

def reject_outliers(data):
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    return filtered

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '__uzma=153d2ce7-2b56-4b07-a0f9-67dbd700f16a; __uzmb=1609641196; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=00a67e99-3384-4391-989d-3bd46024cd6f; __uzmbj2=1609641197; cid=RJQzkFk3wdXkM8EF%23888252336; __uzme=3519; QuantumMetricUserID=2bd37bb459955dee3cf4da60f27929d1; D_HID=756BB114-57A3-3061-9DF8-BDE71FE4579A; D_IID=D8F94D47-FBE9-34C8-9D37-BE7AA4124D07; D_ZID=BEDBB469-A805-39DD-87F7-634DFF9A3194; D_SID=136.30.186.46; D_UID=4BFB31BA-2532-3460-A20F-1A9104230D68; D_ZUID=7B7F1DE0-B642-302C-BA02-30B06D47C299; ak_bmsc=05B873EEA3EC2E0FCC5AD979ED2FF8BA173724741125000055D65A60606AB377~plY8+D6y5MoM3R8P4k3rIkHhgZTwB6DHjmKNA9RfRzXOH8JVrgfg7lGMpuQMASL/Mv1Zf2hGeH6ArNBGH4xWyMxvW/LCzO7Nkgizv7uAzBMJ5KspliO0yms13tfM1mOtYHVBo+1y6bzfUUApb8pm077ZAmelktHJDzdm/Zc7ZjxFK/Il34xrfZ2Hh8Vth3sRHQ3760j8sSW2P4i4WrrM6PeFvaT0c+2xExwImGm3Ox+HY; bm_sv=7F49B02EB16C4F246E8CBC24E0F2A4B5~BrK4enLXyR9vj2/pMRhgqvGEo+mjVfeuWQn03eP3BbQSb2Nev9qGXiRZyP91KLdPDN2NCWEUc2oPPeqOCrtAbncuuwsYUpK6VYcUbP4JnK51w9BbgotIpvhkKSyDPQxLYsWfbC19cDELFowJlwCJYfR9d7V3mC4jqlmQlgiWpeM; __gads=ID=22a669b96385a75d:T=1616567106:S=ALNI_MadiVhftMTIvAvcXovRsBu8G4-8CQ; DG_SID=136.30.186.46:utVROTmCHo4YRg89JHs+rC7NlJwWgNCJuoTJJuDXh70; AMCVS_A71B5B5B54F607AB0A4C98A2%40AdobeOrg=1; DG_ZID=56B436DA-6F29-3177-87DB-B52CF327B536; DG_ZUID=27D8E81D-04A5-3F2F-9036-2307F98DEE0B; DG_HID=B14F6E97-3A4C-36C6-AEA2-99DCEB4B2D81; DG_IID=2D00D6C1-2C26-3F20-8DE9-4036412BD4E5; DG_UID=AE0E6545-E25C-3256-B9F1-CAA41368A6DD; ds1=ats/1616801548863; cssg=dfbb17c41760aad90773076cffad71d1; JSESSIONID=5A868D4C5BB649455FD5596A25131490; shs=BAQAAAXiVB3iwAAaAAVUAD2I/oowyMDQxMzMxNTMyMDA1LDI3EqX+YbI9WwO9P6xTQw6Mc3wkhg**; AMCV_A71B5B5B54F607AB0A4C98A2%40AdobeOrg=-408604571%7CMCMID%7C18721502967304683392404039235057215343%7CMCAAMLH-1618020143%7C7%7CMCAAMB-1618020143%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCCIDH%7C-682630538%7CMCOPTOUT-1617422543s%7CNONE%7CvVersion%7C4.6.0; __uzmc=5240174832516; __uzmd=1617417269; ds2=; __uzmcj2=8245639490559; __uzmdj2=1617417270; npii=btguid/dfbb17c41760aad90773076cffad71d1642a3b37^cguid/fd53d9ec1760aadc3ca082ddfbee5a4a642a3b37^; ebay=%5EsfLMD%3D0%5Esin%3Din%5Edv%3D6067ce56%5Esbf%3D%2320000000000010008000044%5Ecos%3D2%5Elrtjs%3D0.1%5Ecv%3D15555%5Ejs%3D1%5E; cpt=%5Ecpt_prvd%3Drecaptcha_v2%5Ecpt_guid%3D831b42ed-cf49-4217-9582-7d8535bbbbad%5E; ns1=BAQAAAXiVB3iwAAaAAKUADWJJCgwxODU3MzA5MzczLzA7ANgASmJJCgxjNjl8NjAxXjE2MTY4MDMzMjMzMDZeXjFeM3wyfDV8NHw3fDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NXVwsOIz73sZeZqvmhqshkxzOLjP; dp1=bkms/in642a3d8c^u1f/Colin642a3d8c^tzo/12c6067e49c^exc/0%3A0%3A1%3A1608f638c^pcid/88825233662490a0c^mpc/0%7C06075058c^u1p/ZWNvbW1ldF9sbGM*642a3d8c^bl/USen-US642a3d8c^expt/0001616801549533614f08cd^pbf/%232030040a000200050819c0200000462490a0c^; s=BAQAAAXiVB3iwAAWAAPgAIGBpKAxkZmJiMTdjNDE3NjBhYWQ5MDc3MzA3NmNmZmFkNzFkMQFFAAhiSQoMNjA1MWMwNzKSZPoCNcjaAWm9I3KSd4dQd7idKQ**; nonsession=BAQAAAXiVB3iwAAaAAJ0ACGJJCgwwMDAwMDAwMQFkAAdkKj2MIzAwMDAwYQAIABxgj2OMMTYxNzMyMjEwNHgyMzM5MTI5MjgwMTN4MHgyWQAzAA5iSQoMNjAwOTMtMTYyOSxVU0EAywACYGfdlDkyAEAAC2JJCgxlY29tbWV0X2xsYwAQAAtiSQoMZWNvbW1ldF9sbGMAygAgZCo9jGRmYmIxN2M0MTc2MGFhZDkwNzczMDc2Y2ZmYWQ3MWQxAAQAC2I/ooxlY29tbWV0X2xsYwCcADhiSQoMblkrc0haMlByQm1kajZ3Vm5ZK3NFWjJQckEyZGo2QU1sWVdpQ0ptQnBnK2RqNng5blkrc2VRPT3VPd9ALEJvAHeyfBDAJZXsOGrzvQ**',
    'referer': 'https://www.ebay.com/splashui/captcha?ap=1&appName=orch&ru=https%3A%2F%2Fwww.ebay.com%2Fsch%2Fi.html%3F_from%3DR40%26_nkw%3DiPhone%2Bexcellent%26_sacat%3D0%26Model%3DApple%252520iPhone%2525206%26Network%3DUnlocked%26Storage%252520Capacity%3D16%252520GB%26_dcat%3D9355%26LH_ItemCondition%3D3000%26rt%3Dnc%26LH_Sold%3D1%26LH_Complete%3D1%26_ipg%3D200%26_pgn%3D1%26_ipg%3D200%26LH_BIN%3D1&iid=f29fb032-450e-4e52-a94b-13a1c74fd6a7'
}

def requestPage(keyword, added_word, model, network, storage, condition, buying_format):
    raw_model = model.replace(' ', '%2520').replace('(', '%2528').replace(')', '%2529')
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={keyword}+{added_word}&_sacat=0&Model={raw_model}&Network={network}&Storage%2520Capacity={storage}%2520GB&_dcat=9355&LH_ItemCondition={condition}&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200&_pgn=1&_ipg=200&LH_{buying_format}=1&{lock_status}'
    print(url)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def getUnfilteredPrices(soup):
    title_list = [value.text.strip().lower() for value in soup.find_all(class_='s-item__title s-item__title--has-tags')]
    price_list = [value.text.strip().lower() for value in soup.find(class_='srp-river-main').find_all(class_='s-item__price')]
    zipped = list(zip(title_list, price_list))

    return zipped


def getFilteredPrices(title_price_list):
    all_title_and_price = []
    all_prices = []
    for tp in title_price_list:
        if 'to' not in tp[1] and all([w not in tp[0] for w in excludedPhrases]):
            all_title_and_price.append(tp)
            all_prices.append(float(tp[1][1:].replace(',', '')))

    for i in all_title_and_price:
        print(i)
    filtered_result_number = len(all_title_and_price)

    return all_title_and_price, all_prices, filtered_result_number

def getAveragePrice(prices):
    average_price = get_average(reject_outliers(prices))
    return average_price


def plot(all_prices, average_price, result):
    plt.hist(reject_outliers(all_prices), bins=30)
    plt.axvline(x=average_price, color='r', linestyle='dashed', linewidth=2)
    plt.title(f'{model} - ({carrierName}) - ({storage}GB) - ({conditionName}) - ({result} results)')
    plt.xlabel(f'Sold Price ($) - Average Price: ({average_price})')
    plt.ylabel('Volume')
    plt.show()


networks = {
    'Unlocked': {
        'url': 'Unlocked',
        'Lock Status': 'Lock%2520Status=Network%2520Unlocked%7CFactory%2520Unlocked',
        'excludedPhrases': ''
    },
    'Verizon': {
        'url': 'Verizon',
        'Lock Status': 'Lock%2520Status=Network%2520Locked',
    },
    'AT&T': {
        'url': 'AT%256T',
        'Lock Status': 'Lock%2520Status=Network%2520Locked',
    },
    'T-Mobile': {
        'url': 'T%252DMobile',
        'Lock Status': 'Lock%2520Status=Network%2520Locked',
    },
    'Sprint': {
        'url': 'Sprint',
        'Lock Status': 'Lock%2520Status=Network%2520Locked',
    },
    'Other': {
        'url': 'Bell%2520Mobility%7CConsumer%2520Cellular%7CBoost%2520Mobile%7CCricket%2520Wireless%7CC%2520Spire%7Ch2o%7CGoogle%2520Fi%7CMetro%7CMint%2520Mobile%7CNET10%2520Wireless%7CRogers%2520Wireless%7CSIMPLE%2520Mobile%7CXfinity%7CWest%2520Central%2520Wireless%7CWalmart%2520Family%2520Mobile%7CVirgin%2520Mobile%7CUltra%2520Mobile%7CTracFone%7CU%252ES%252E%2520Cellular%7CTing%7CStraight%2520Talk',
        'Lock Status': 'Lock%2520Status=Network%2520Locked',

    }
}

buying_format_dict = {'Buy It Now': 'BIN', 'Auction': 'Auction'}


conditions = {

    'Like New': {
        'conditionID': '3000',
        'excludedPhrases': ['read', 'face', 'see', 'not', 'lot', 'protector', 'case', 'bad', 'touch', 'fair', 'ic', 'poor', 'lcd', 'watch'],
        'addedWord': 'excellent'
    },
    'Good': {
        'conditionID': '3000',
        'excludedPhrases': ['read', 'face', 'see', 'not', 'lot', 'protector', 'case', 'bad', 'touch', 'fair', 'ic', 'poor', 'lcd', 'watch', 'box'],
        'addedWord': ''
    },
    'Fair': {
        'conditionID': '3000',
        'excludedPhrases': ['face', 'lot', 'protector', 'case', 'touch', 'ic', 'watch', 'box'],
        'addedWord': ''
    },
    'Broken': {
        'conditionID': '7000',
        'excludedPhrases': ['lot', 'protector', 'case', 'ic', 'watch', 'box'],
        'addedWord': ''
    }
}



keyword = 'iPhone'
model = 'Apple iPhone X'
storage = '256'
carrierName = 'Unlocked'
conditionName = 'Good'


buying_format = buying_format_dict['Buy It Now']
carrierID = networks[carrierName]['url']
lock_status = networks[carrierName]['Lock Status']
conditionID = conditions[conditionName]['conditionID']
excludedPhrases = conditions[conditionName]['excludedPhrases']

includedPhrase = conditions[conditionName]['addedWord']




soup = requestPage(keyword, includedPhrase, model, carrierID, storage, conditionID, buying_format)

title_and_prices = getUnfilteredPrices(soup)
filtered_prices = getFilteredPrices(title_and_prices)
results = filtered_prices[2]

if results >= 10:
    try:

        average_price = getAveragePrice(filtered_prices[1])
        plot(filtered_prices[1], average_price, results)
        print((model, storage, carrierName, conditionName, average_price))
    except Exception as e:
        print((model, storage, carrierName, conditionName, e))
else:
    print((model, storage, carrierName, conditionName, "**NOT ENOUGH RESULTS**"))

