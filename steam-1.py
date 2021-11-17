import json

save_dict = {'keyvalue': 'shooting', 'languages': 'English', 'types': 'Action'}
with open('options.json', 'w') as result_file:
    json.dump(save_dict, result_file)

with open('options.json', 'r') as result_file:
    save_dict = json.load(result_file)

dir = "C:/Users/86136/Downloads"


keyvalue=save_dict['keyvalue']
langueges=save_dict['languages']
types=save_dict['types']


import rpa as r

r.init()


r.url('https://store.steampowered.com/')

keyvalue=keyvalue
# 参数1：关键词




r.wait(0.5)
r.type('//*[@id="store_nav_search_term"]',keyvalue+'[enter]')


r.click('//*[@id="additional_search_options"]/div[2]/a')
r.click('//*[@id="additional_search_options"]/div[3]/a')



lan_num=r.count('//*[@id="narrow_language"]/div')


for i in range(1,lan_num):
    selector=f'//*[@id="narrow_language"]/div[{i}]'
    text=r.read(selector)
    print (text)



r.click('//*[@id="narrow_language"]//span[contains(text(),"{languages}}")]')



from keywordextraction import key_word_extraction


h=0
result=[]
for i in range(1,3):
    item_selector = f'(//span[@class="title"])[{i}]'
    if r.exist(item_selector):
        r.click(item_selector)
        r.wait(1)
        #年龄问题
        if r.exist('//div[@class="main_content_ctn"]'):
            r.click('//select[@name="ageYear"]')
            r.hover('//select[@name="ageYear"]')
            r.type('//select[@name="ageYear"]','2000')
            r.click('//select[@name="ageYear"]')
            r.click('(//a[@class="btnv6_blue_hoverfade btn_medium"])[1]')
            h=1
        text=r.read('//div[@id="aboutThisGame"]')
        if r.exist('(//div[@class="discount_final_price"])[1]'):
            price=r.read('(//div[@class="discount_final_price"])[1]')
        else:
            price=r.read('(//div[@class="game_purchase_price price"])[1]')
        name=r.read('//div[@id="appHubAppName"]')
        tag=[]
        for j in range(1,4):
            if r.exist(f'(//div[@class="glance_tags popular_tags"]/a)[{j}]'):
                tag1=r.read(f'(//div[@class="glance_tags popular_tags"]/a)[{j}]')
                tag.append(tag1)
        if r.exist(f'//div[contains(. ,"Publisher:")]/div[@class="summary column"]'):
            publisher=r.read(f'//div[contains(. ,"Publisher:")]/div[@class="summary column"]')
        else:
            publisher=""
        review=r.read('(//div[@class="summary column"]/span[@itemprop="description"])[1]')
        text1=key_word_extraction(text)
        #解决编码问题
        r.wait(1)
        #执行js脚本返回上一页
        r.dom("window.history.go(-1)")
        template={"price":price,"name":name,"tag":tag,"review":review,"publisher":publisher,"description":text1}

        result.append(template)

        if(h==1):
            r.dom("window.history.go(-1)")
            h=0
        r.wait(2)
aJson=json.dumps(result)
filepath='output.txt'
f=open(filepath,'w')
f.write(aJson)
f.close()
with open('options.json', 'w') as result_file:
    json.dump(result, result_file)


with open('output.json', 'w') as result_file:
    json.dump(result, result_file)
r.close()

