import requests
import parsel
import time

#定义一个检测爬取到的IP的质量的方法
def check_IP(proxies_list):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    #定义一个列表来选出高质量的ip
    can_use=[]
    #使用代理IP访问服务器从而检查IP质量
    for proxy in proxies_list:
        try:
            #使用代理IP访问某站并要求0.1秒内给出响应（若超过0.1秒则会异常报错）
            response=requests.get('https://baidu.com',headers=headers,proxies=proxy,timeout=0.1)
            #高质量的代理IP
            if response.status_code==200:
                    can_use.append(proxy)
        except Exception as e:
            print(e)
    return can_use


# 一个空列表用来存储所有的代理IP
proxies_list = []
for page in range(1,5):

    #用{}预留一个接口，通过.format将页数进行传递
    base_url="https://www.kuaidaili.com/free/inha/{}/".format(page)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    response=requests.get(base_url,headers=headers)
    #接收数据
    data=response.text
    data.encode("UTF-8")

    #解析数据
    #将data数据转换成一个selector对象
    html_data=parsel.Selector(data)

    XpathSelect='//table[@class="table table-bordered table-striped"]/tbody/tr'
    parse_list=html_data.xpath(XpathSelect)
    for tr in parse_list:
        #代理IP的形式是一个类字典
        proxies_dict={}
        #提取协议类型
        http_type=tr.xpath("./td[4]/text()").extract_first()
        IP = tr.xpath("./td[1]/text()").extract_first()
        IP_Port = tr.xpath("./td[2]/text()").extract_first()
        #将数据加入字典
        proxies_dict[http_type]=IP+":"+IP_Port
        proxies_list.append(proxies_dict)
        print(proxies_dict)
        time.sleep(0.5)

print("获取到的代理IP数量是",len(proxies_list),"个")
#检测代理IP可用性
can_use=check_IP(proxies_list)
print("能用的IP数量",len(can_use))