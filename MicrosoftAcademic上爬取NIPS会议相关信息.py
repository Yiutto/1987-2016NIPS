# https://academic.microsoft.com/api/search/GetEntityResults?query=And(Composite(C.CN%3D%3D%27nips%27)%2CY%3D2006)&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=9648675f-3548109d-a11f-bd223ff8
# https://academic.microsoft.com/api/search/GetEntityResults?query=%40nips%202005%40&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=9648675f-3548109d-a11f-bd223ff8
# https://academic.microsoft.com/api/search/GetEntityResults?query=%40nips%202005%40&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=9648675f-3548109d-a11f-bd223ff8
# https://academic.microsoft.com/api/search/GetEntityResults?query=%40NIPS%201995%40&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=77764f9a-9bb742e2-19d6-63bc3a15
# https://academic.microsoft.com/api/search/GetEntityResults?query=%40NIPS%201996%40&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=77764f9a-9bb742e2-19d6-63bc3a15
# https://academic.microsoft.com/api/search/GetEntityResults?query=And(Composite(C.CN%3D%3D%27nips%27)%2CY%3D2004)&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=77764f9a-9bb742e2-19d6-63bc3a15
# https://academic.microsoft.com/api/search/GetEntityResults?query=And(Composite(C.CN%3D%3D%27nips%27)%2CY%3D2001)&filters=&offset=8&limit=8&orderBy=D&sortAscending=false&correlationId=d45f26df-9ad9a58a-577d-469a22ca

from pandas import DataFrame
import pandas as pd
import numpy as np
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}

table = DataFrame(np.array(['aa', 'c', 'extended', 'e', 'd', 'f', 'cc', 'ci', 'ty', 'l', 'w', 'ti', 'y', 'ecc', 'rId', 'id']).reshape(1,16), columns=['aa', 'c', 'extended', 'e', 'd', 'f', 'cc', 'ci', 'ty', 'l', 'w', 'ti', 'y', 'ecc', 'rId', 'id'])
i = 0
while i <= 4:
    url = "https://academic.microsoft.com/api/search/GetEntityResults?query=And(Composite(C.CN%3D%3D%27nips%27)%2CY%3D2000)&filters=&offset=" + str(50*i) + "&limit=50&correlationId=d45f26df-9ad9a58a-577d-469a22ca"
    resp=requests.get(url,headers=headers)
    html=resp.text
    data_dic = json.loads(html)
    data=DataFrame(data_dic['results'])
    table=pd.concat([table,data])
    i += 1

table.to_csv('2000.csv',header=False)
