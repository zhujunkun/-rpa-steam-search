
from keywordextraction import key_word_extraction
import tagui as t
import json
t.init(visual_automation = True)

# goto the page
t.url('https://store.steampowered.com/search/?term=action')
t.wait(1)
h=0
result=[]
for i in range(1,11):
    item_selector = f'(//span[@class="title"])[{i}]'
    t.click(item_selector)
    t.wait(1)
    #年龄问题
    if t.exist('//div[@class="main_content_ctn"]'):
        t.click('//select[@name="ageYear"]')
        t.hover('//select[@name="ageYear"]')
        t.type('//select[@name="ageYear"]','2000')
        t.click('//select[@name="ageYear"]')
        t.click('(//a[@class="btnv6_blue_hoverfade btn_medium"])[1]')
        h=1
    text=t.read('//div[@id="aboutThisGame"]')
    if t.exist('(//div[@class="discount_final_price"])[1]'):
        price=t.read('(//div[@class="discount_final_price"])[1]')
    else:
        price=t.read('(//div[@class="game_purchase_price price"])[1]')
    name=t.read('//div[@id="appHubAppName"]')
    tag=[]
    for j in range(1,4):
        tag1=t.read(f'(//div[@class="glance_tags popular_tags"]/a)[{j}]')
        tag.append(tag1)
    if t.exist(f'//div[contains(. ,"Publisher:")]/div[@class="summary column"]'):
        publisher=t.read(f'//div[contains(. ,"Publisher:")]/div[@class="summary column"]')
    else:
        publisher=""
    review=t.read('(//div[@class="summary column"]/span[@itemprop="description"])[1]')
    text1=key_word_extraction(text)
    #解决编码问题
    text1 = text1.encode("gbk", 'ignore')
    text1 = text1.decode("gbk", "ignore")
    t.wait(1)
    #执行js脚本返回上一页
    t.dom("window.history.go(-1)")
    template={"description":text1,"price":price,"name":name,"tag":tag,"review":review,"publisher":publisher}
    
    result.append(template)
    
    if(h==1):
        t.dom("window.history.go(-1)")
        h=0
    t.wait(2)
aJson=json.dumps(result)
filepath=f'output.txt'
f=open(filepath,'w')
f.write(aJson)
f.close()
t.close()
