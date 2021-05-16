import requests
import json
import time

g_Url = 'http://x.ouchn.cn/'
g_Cookie = 'UserName=XXXXXXXXX; MoodleSession=XXXXXXXXXXX'
g_Sectionid = 0
g_Courseid = 0
g_SectionList = []

RequestHeadres = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Cookie' : g_Cookie,
}


def GetSectionInfo(Sectionid, t=0.5):
    # 延迟
    time.sleep(t)
    data = {'sectionid': Sectionid, 'courseid': g_Courseid}
    r = requests.post(url= g_Url+'theme/blueonionres/sectionInfo.php', data=data, headers=RequestHeadres)
    try:
        return json.loads(r.text)
    except Exception:
        return {}


def GetSectionJob(Sectionid):
    Info = []
    SectionInfo = GetSectionInfo(Sectionid, 1)
    if type(SectionInfo) == dict:
        for var in SectionInfo.values():
            if var.__contains__('type') and var.__contains__('id'):
                Info.append(var)

    return Info


def Fuck(Sectionid, mid, t=0.5):
    # 延迟
    time.sleep(t)
    try:
        # data = {'id': g_Courseid, 'sectionid': Sectionid, 'cmid': mid}
        data = '?cmid='+ str(mid) + '&id=' + str(g_Courseid) + '&sectionid=' + str(Sectionid)
        r = requests.get(url=g_Url+'theme/blueonionres/modulesCompletion.php'+data, headers=RequestHeadres)
        if r.status_code == 200:
            return 1
        else:
            return 0

    except Exception:
        return 0


def InitSectionList():
    SectionInfo = GetSectionInfo(g_Sectionid)
    if type(SectionInfo) == dict:
        if SectionInfo.__contains__('secinfo') :
           for Info in SectionInfo['secinfo'].values():
               if Info.__contains__('sequence') :
                    Section = GetSectionInfo(Info['id'])
                    if type(Section) == dict:
                        if Section.__contains__('secinfo') :
                            for var in Section['secinfo'].values():
                                InsertSectionList(var['id'], var['name'])

                            if type(Section['ssec']) == dict:
                                for var in Section['ssec'].values():
                                    InsertSectionList(var['sectionid'], var['name'])


def InsertSectionList(id, name):
    IsExist = False
    data = {'id': id, 'name': name}
    for var in g_SectionList:
        if var['id'] == id:
            IsExist = True

    if IsExist == False:
         g_SectionList.append(data)

def FuckOuchn():
    for var in g_SectionList:
        print(var)

    for var in g_SectionList:
        List = GetSectionJob(var['id'])
        print(var['name'])
        for i in List:
            if i['type'] == 'url' and int(i['is_com']) == 0:
                print('\t' + i['name'], end='')
                IsSuccess = Fuck(var['id'], i['id'], 1)
                if IsSuccess == 1:
                    print('  success', end='')
                else:
                    print('  fail', end='')

                print('\n')

        print('\n')

InitSectionList()
FuckOuchn()
