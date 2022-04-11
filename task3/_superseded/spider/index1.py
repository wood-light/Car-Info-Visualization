import requests,time,xlwt,openpyxl,datetime,emoji,re
from bs4 import BeautifulSoup
import pymysql

#建立数据库连接
db = pymysql.connect(user='root', password='', database='car-sys', charset='utf8')  # 打开数据库连接
#获取游标对象
cursor = db.cursor()

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'sheet'

payload={}
headers = {
  'authority': 'www.sgcarmart.com',
  'cache-control': 'max-age=0',
  'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'referer': 'https://www.sgcarmart.com/new_cars/newcars_listing.php?BRSR=30&RPG=15',
  'accept-language': 'zh-CN,zh;q=0.9',
  'cookie': 'newcar_rpg=15; SGCMSESSID=firki2lrpq1sr672jr7ta2kt13; SignUpGift=1635162735; _dy_csc_ses=t; _dy_c_exps=; OAID=07b62f938276acfe95ad1eec22c73bc6; _ga=GA1.2.2083035924.1635162736; _gid=GA1.2.1283401735.1635162736; _gcl_au=1.1.410657297.1635162736; __gads=ID=f0b6911370251911:T=1635162737:S=ALNI_MYzDXUzDpKlXajfEcG3at2TSNDnQw; 227b44aa2cb7cf63d7c4806347639187=2; 2ab4e5a525a2cbac5a6e3045325ed1f1=2; _dy_c_att_exps=; _dycnst=dg; _dyid=5426837818904582769; _dyjsession=a1ff4fed1785c83bcddfc86d91fab44a; dy_fs_page=www.sgcarmart.com%2Fnew_cars%2Fnewcars_listing.php%3Fbrsr%3D0%26rpg%3D15; _dy_geo=CN.AS.CN_HI.CN_HI_Haikou; _dy_df_geo=China..Haikou; _dyid_server=5426837818904582769; _dycst=dk.w.c.ss.; _dyfs=1635164392235; _dy_lu_ses=a1ff4fed1785c83bcddfc86d91fab44a%3A1635164392240; _dy_toffset=-14; viewednewcars=12946; _dy_ses_load_seq=79504%3A1635166348790; _dy_soct=506685.941480.1635166348*297777.467401.1635166348*348687.569501.1635166352; OACBLOCK=1158.1635166362; OASCCAP=1158.1; OAVARS[default]=a%3A2%3A%7Bs%3A8%3A%22bannerid%22%3Bs%3A4%3A%223687%22%3Bs%3A6%3A%22oadest%22%3Bs%3A38%3A%22https%3A%2F%2Fwww.facebook.com%2Fyhisingapore%2F%22%3B%7D; __atuvc=1%7C43; newcar_rpg=15; _dyid_server=5426837818904582769'
}

a=0
def SpCharReplace(char):
  temp = str(char)
  for i in temp:
    if '<' == i:
      char = char.replace('<', '《')
    if '>' == i:
      char = char.replace('>', '》')
    if '\'' == i:
      char = char.replace('\'', '')  # 处理单引号
    if '\\' == i:
      char = char.replace('\\', '')  # 处理反斜杠\
    if '\"' == i:
      char = char.replace('\"', '`')  # 处理双引号"
    if '&' == i:
      char = char.replace('&', '-')  # 处理&号"
    if '|' == i:
      char = char.replace('|', '')  # 处理|号
    if '@' == i:
      char = char.replace('@', '.')  # 处理@号
    if '%' == i:
      char = char.replace('%', "`")  # 处理百分号
    if '*' == i:
      char = char.replace('*', '`')  # 处理星号
    if '("' == i:
      char = char.replace('(', '`')  # 处理括号（
    if ')"' == i:
      char = char.replace(')"', '`')  # 处理括号）
    if '-' == i:
      char = char.replace('-', '`')  # 处理-号"
    # 在后面扩展其他特殊字符
  return char

for i in range(0, 44, 1):
  print(i)
  page=i*15;
  url = f"https://www.sgcarmart.com/new_cars/newcars_listing.php?BRSR={page}&RPG=15"
  response = requests.request("GET", url, headers=headers, data=payload)
  soup = response.textsoup = BeautifulSoup(response.text, 'lxml')
  data1 = soup.select('#listingcorner > form > table')
  for item in data1:
    # print(item)
    data2 = item.select('div.floatleft > a > strong')  # 名称
    data3 = item.select('div.floatleft > label')  # 规格
    data4 = item.select('td.font_bold.font_red.syndep')  # 价格
    # print(len(data3))
    print(len(data2),len(data4),data4)

    list1 = []
    list2 = []

    for item1 in data3:
      list1.append(item1.get_text().strip())

    for item2 in data4:
      list2.append(item2.get_text().strip())

    for k in range(len(list1)):
      name = data2[0].get_text()
      mode = list1[k]
      # mode = item3
      price = list2[k]
      # price = list2[i]
      print(f"{name},{mode},{price}")
      print("-----")
      sql2 = "INSERT INTO info(name,mode,price)VALUES('{}','{}','{}')"  # sql语句
      sql = sql2.format(SpCharReplace(name), SpCharReplace(mode), SpCharReplace(price))  # 转化后的sql语句
      cursor.execute(sql)
      db.commit()

