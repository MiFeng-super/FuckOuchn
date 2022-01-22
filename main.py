import requests
import json
import time
import os
from datetime import datetime

g_url = 'http://guangzhou.ouchn.cn/'
g_cookie = 'UserName=2144101422158; MoodleSession=e9raib1ueqsut2rhe4dliqnusr'
g_section = 83413
g_course = 1946
g_type = ['url', 'page', 'resource']

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Cookie': g_cookie,
}


def getSection(id):
    time.sleep(4)
    data = {'sectionid': id, 'courseid': g_course}
    res = requests.post(url=g_url + 'theme/blueonionres/sectionInfo.php', data=data, headers=headers)
    try:
        return json.loads(res.text)
    except Exception:
        return None


def getJobHtml(sectionid, mid):
    time.sleep(10)
    try:
        data = '?id=' + str(g_course) + '&sectionid=' + str(sectionid) + '&mid=' + str(mid)
        r = requests.get(url=g_url + 'course/view.php' + data, headers=headers)
        return r.status_code
    except Exception:
        return 0


def setJobState(id, secId):
    try:
        data = '?cmid=' + str(id) + '&id=' + str(g_course) + '&sectionid=' + str(secId)
        print('\t' + str(getJobHtml(secId, id)), end='')
        time.sleep(4)
        r = requests.get(url=g_url + 'theme/blueonionres/modulesCompletion.php' + data, headers=headers)
        if r.status_code == 200:
            return '1'
        else:
            return '0'
    except Exception:
        return '0'


def parseSection(id, section):
    try:
        if section.__contains__('sequence'):
            for i in section['sequence']:
                try:
                    JobType = section[i]['type']
                    print('\t\t' + section[i]['name'], end='')
                    if JobType in g_type:
                        print('\t\t' + setJobState(section[i]['id'], id))
                    else:
                        print('\t\t' + '不支持一键完成\t' + JobType)
                except Exception:
                    pass

        if section.__contains__('ssec'):
            ssec = section['ssec']
            if type(ssec) == dict:
                for i in ssec.values():
                    print('\t\t' + i['name'])
                    sInfo = getSection(i['sectionid'])
                    if sInfo is not None:
                        for j in sInfo['sequence']:
                            JobType = sInfo[j]['type']
                            print('\t\t\t\t' + sInfo[j]['name'], end='')
                            if JobType in g_type:
                                print('\t\t\t\t' + setJobState(sInfo[j]['id'], i['sectionid']))
                            else:
                                print('\t\t\t\t' + '不支持一键完成\t' + JobType)
    except Exception:
        return


def main():
    while True:
        MSection = getSection(g_section)
        if MSection is not None:
            secinfo = MSection['secinfo']
            for sec in secinfo:
                if sec != 'fsec':
                    print(secinfo[sec]['name'])
                    child_section = getSection(secinfo[sec]['id'])
                    if child_section is not None:
                        parseSection(secinfo[sec]['id'], child_section)
            break

        else:
            print('封号时间：' + str(datetime.now()))
            time.sleep(60 * 10)


if __name__ == '__main__':
    for i in range(1000):
        os.system('cls')
        print('第%d次开始' % (i + 1))
        print('*' * 100)
        main()
