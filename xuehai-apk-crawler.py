from datetime import date
import urllib.request as urllib2
import re,json
l=['595d9d4af099e42a9255b777','595d9db6f099e42a9255b77a','595d9f89f099e42a9255b77d','595d9fe1f099e42a9255b780','595da0cdf099e42a9255b78c','595da0f8f099e42a9255b78f','595da1bef099e42a9255b792','595da231f099e42a9255b795','595da254f099e42a9255b798','595da297f099e42a9255b79b','595da2c1f099e42a9255b79e','595da3b2f099e42a9255b7a4','595da419f099e42a9255b7a7','595da43df099e42a9255b7aa','595da49df099e42a9255b7ad','595da5bef099e40ed92c5641','595da5fbf099e40ed92c5644','595da65ef099e40ed92c5647','595da685f099e40ed92c564a','595da7c1f099e40ed92c564d','595da7e6f099e40ed92c5651','597fe8c9f099e469ecc58cda','598004ecf099e469ecc58cdd','59ae6bcef099e435f3366f13']
dic={}
def enc(s):
    t=map(int,bin(date.today().day-1)[2:].rjust(len(s),'0'))
    return ''.join('%'+hex(ord(c))[2:] if f else c for f,c in zip(t,s))
base='https://xhoffice.yunzuoye.net/excelView.php?url=http://app.yunzuoye.cloud/api/v1/'+enc('applications')+'/'
def extr(h):
    return re.sub('\\s+',' ',re.sub('<.*?>','',re.sub('<style.*?</style>','',re.sub('<script.*?</script>','',re.sub('<head.*?</head>','',h,flags=re.S),flags=re.S),flags=re.S),flags=re.S).replace('\n','')).replace('&quot;','"')
url='?page=1&size=1000'
print('Loading index...')
try:
    with urllib2.urlopen(base+url) as r:
        s=extr(r.read().decode('utf-8'))
        try:
            o=json.loads(s)
            if 'code' in dir(o) and int(o.code)==500:raise Exception
            o=o['content']
            def chk(x):
                if not len(x['appVersions']):return False
                if not len(x['appVersions'][0]['url']):return False
                if x['appVersions'][0]['status']==4:dic[x['appId']]=x['appVersions'][0]
                s = x['packageName']
                if 'com.xuehai.third.' in s:return False
                if s=='com.zhitongyun.netcheck':return False
                if s=='cn.mdict':return False
                if 'com.xuehai.' in s:return True
                if 'com.xh.' in s:return True
                if 'com.zhitongyun.' in s:return True
                return False
            o=[x for x in o if chk(x)]
            o2=o
            o=[a['appId'] for a in o]+l
            o.sort(key=lambda x:-int(x,16))
            def req(i):
                print('Loading %s...'%i)
                r=urllib2.urlopen(base+enc(i))
                s=extr(r.read().decode('utf-8'))
                t=json.loads(s)
                if 'code' in dir(t) and int(t.code)==500:raise Exception
                if t['packageName']=='com.xh.mis':
                    t['appVersions'].pop()
                return t
            o=[req(i) for i in o]
            for x in o:
                if x['appId'] in dic:x['appVersions'].insert(0,dic[x['appId']])
            with open('xuehai.%d.json'%date.today().toordinal(),'w') as f:json.dump(o,f,indent=4,ensure_ascii=False)
        except Exception as e:print('Invalid response!');print(e)
except:print('Invalid response!')