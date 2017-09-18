import requests,json,re,chardet,random,pymongo
import urllib,os
from multiprocessing import Pool
#166
class MM():
    def __init__(self):

        client=pymongo.MongoClient()
        db=client.proxies
        self.collection=db.ip
    def ips(self):
        tryconut=3
        d=list()
        for l in self.collection.find():
            d.append(l['ip'])
        i=random.choice(d)
        ip={'http':'%s'%i}
        while tryconut:
            try:
                requests.get('https://www.baidu.com/?tn=90294326_hao_pg',proxies=ip,timeout=1)
            except:
                tryconut-=1
                i = random.choice(self.collection.find())
                ip = {'http': '%s' % i}
                try:
                    requests.get('https://www.baidu.com/?tn=90294326_hao_pg', proxies=ip, timeout=1)
                except:
                    tryconut -= 1
                else:
                    return ip
            else:
                return ip

    def run(self):
        if os.path.exists(r'D:\淘女郎'):
            print('已经存在文件夹')
        else:
            print('不存在，那就创建一个文件夹')
            os.makedirs(r'D:\淘女郎')
        ip=self.ips()
        for i in range(1,167):
            url = ('https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8')
            form = {
                'q': '',
                'viewFlag': 'A',
                'sortType': 'default',
                'searchStyle': '',
                'searchRegion': 'city:',
                'searchFansNum': '',
                'currentPage': '%d'%i,
                'pageSize': 100
            }
            r = requests.post(url,proxies=ip, data=form).text#proxies=ip,
            j = json.loads(r)['data']['searchDOList']
            for l in j:
                phots = ('https://mm.taobao.com/self/album/open_album_list.htm?&user_id =%s' % l['userId'])#相册接口
                realName=l['realName']#姓名
                if os.path.exists(r'D:\淘女郎\%s'%realName):
                    pass
                else:
                    print('不存在，那就创建一个文件夹')
                    os.makedirs(r'D:\淘女郎\%s'%realName)
                file_path=(r'D:\淘女郎\%s'%realName)
                r1 = requests.get(phots)
                r1.encoding = chardet.detect(r1.content)['encoding']
                album_ids = re.findall(
                    r'class="mm-first" href="//mm.taobao.com/self/album_photo.htm\?user_id=(.*?)&album_id=(.*?)"',
                    r1.text)
                try:
                    for userid, albumid in album_ids[::2]:
                        self.getabim(userid, albumid,file_path)
                except Exception as e:
                    print(Exception,e)


    def getabim(self,userid,albumid,file_path):
        url=('https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s'%(userid,albumid))
        r=requests.get(url)
        html=json.loads(r.text)
        a=html['picList']
        print(type(a),'----------------------')
        for i in range(len(a)):
            b=('http:'+a[i]['picUrl'])
            file=a[i]['picUrl'].split('/')
            file_name=file[-1]

            #拼接图片名（包含路径）
            filename = '{}{}{}'.format(file_path,os.sep,file_name)
            self.download(b,filename)

    def download(self,photo_url,filename):
        r=requests.get(photo_url).content
        with open('%s'%filename,'wb')as f:
            f.write(r)
            print('ok')



if __name__ == '__main__':

    a =MM()
    b=a.run()
