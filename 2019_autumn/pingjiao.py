# coding=utf-8

import requests
from lxml import etree
import execjs
import json
import click

# 参数
some_id = '41'  # 某个不知道干啥用的 id
kkxy = '2302000'  # 某个不知道干啥用的 key
lt = ''
dllt = ''
execution = ''
_eventId = ''
rmShown = ''

# 各种 url
base_addr = 'http://s.ugsq.whu.edu.cn/'
login = 'https://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fs.ugsq.whu.edu.cn%2Fcaslogin%2F'
caslogin = base_addr + 'caslogin/'
loginSSO = base_addr + 'loginSSO'
studentpj = base_addr + 'studentpj'
getkcpmid = base_addr + 'getkcpmid'
evaluate2 = base_addr + 'new/student/rank/evaluate2.jsp'
SCHOOL_ADMIN = base_addr + 'getStudentPjPf/' + some_id + '/' + kkxy + '/SCHOOL_ADMIN'
createStudentPjpf = base_addr + 'createStudentPjpf'

# 使用会话保持 cookie
s = requests.Session()


# 获取课程信息
def get_kc(username, password):

    # 登录
    data = {
        'username': username,
        'password': password,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': _eventId,
        'rmShown': rmShown
    }
    login_response = s.post(login, data=data, allow_redirects=False)  # 重定向请求必须加上 allow_redirects=False

    # 获取 Location，向 CAS 客户端发送请求
    url = login_response.headers['Location']
    s.get(url, allow_redirects=False)

    # 对照浏览器执行相同的请求
    s.get(caslogin)
    s.post(loginSSO, data={'userId': username})
    s.get(studentpj)

    # 进入课程列表界面
    data = {
        'hdid': some_id,
        'xh': username
    }
    s.post(getkcpmid, data=data)
    params = {
        'hdfaid': some_id,
        'overtime': 'timeNO',
        'sfkdcpj': '1',
        'sfqxzdf': '0',
        'zbtx': '267,268,266,265',
        'kkxy': '2302000',
        'roid': 'SCHOOL_ADMIN'
    }
    s.get(evaluate2, params=params)

    # 获取课程列表数据
    data = {
        'sEcho': '1',
        'iColumns': '6',
        'sColumns': '',
        'iDisplayStart': '0',
        'iDisplayLength': '10',
        'mDataProp_0': 'KCMC',
        'mDataProp_1': 'XM',
        'mDataProp_2': 'TJSJ',
        'mDataProp_3': 'YZ',
        'mDataProp_4': 'PJJGID',
        'mDataProp_5': '',
        'iSortCol_0': '0',
        'sSortDir_0': 'asc',
        'iSortingCols': '1',
        'bSortable_0': 'false',
        'bSortable_1': 'false',
        'bSortable_2': 'false',
        'bSortable_3': 'false',
        'bSortable_4': 'false',
        'bSortable_5': 'false'
    }
    SCHOOL_ADMIN_response = s.post(SCHOOL_ADMIN, data=data)
    result = json.loads(SCHOOL_ADMIN_response.text)
    all = result['iTotalRecords']  # 总课程数
    count = 0  # 已评价的课程数
    print('共有 {} 门课需要评价：'.format(all))
    kc_list = result['aaData']
    for kc in kc_list:
        if kc['TJSJ']:
            count += 1
            print('教务系统课程号：{}，课程名称：{}({})，课程类型：{}，教师姓名：{}({})，评价提交时间：{}，一级指标得分：{}，评价结果：{}'.format(
                kc['JXBDM'], kc['KCMC'], kc['KCH'], kc['KCLX'], kc['XM'], kc['GH'], kc['TJSJ'], kc['YZ'], kc['ZPDF']))
        else:
            print('教务系统课程号：{}，课程名称：{}({})，课程类型：{}，教师姓名：{}({})，未评价'.format(
                kc['JXBDM'], kc['KCMC'], kc['KCH'], kc['KCLX'], kc['XM'], kc['GH']))
    print('已评价：{} 门 未评价：{} 门'.format(count, all - count))

    return kc_list


# 进行评价
def pingjia(kc):
    if not kc['TJSJ']:
        data = [
            ('dxid', '908'),
            ('dxid', '909'),
            ('dxid', '910'),
            ('dxid', '911'),
            ('dxid', '912'),
            ('dxid', '913'),
            ('dxid', '914'),
            ('dxid', '915'),
            ('dxid', '916'),
            ('dxid', '917'),
            ('dxid', '918'),
            ('dxid', '919'),
            ('dxid', '920'),
            ('dxid', '921'),
            ('dxid', '922'),
            ('dxid', '923'),
            ('dxid', '924'),
            ('dxid', '925'),
            ('dxid', '926'),
            ('dxid', '927'),
            ('dxid', '928'),
            ('dxid', '929'),
            ('dxvalue', '10'),
            ('dxvalue', '5'),
            ('dxvalue', '5'),
            ('dxvalue', '5'),
            ('dxvalue', '5'),
            ('dxvalue', '5'),
            ('dxvalue', '5'),
            ('dxvalue', '7'),
            ('dxvalue', '7'),
            ('dxvalue', '7'),
            ('dxvalue', '8'),
            ('dxvalue', '8'),
            ('dxvalue', '8'),
            ('dxvalue', '2'),
            ('dxvalue', '3'),
            ('dxvalue', '2'),
            ('dxvalue', '3'),
            ('dxvalue', '3'),
            ('dxvalue', '3'),
            ('dxvalue', '3'),
            ('dxvalue', '3'),
            ('dxvalue', '3'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('sfjft', '1'),
            ('wdid', '930'),
            ('wdid', '931'),
            ('wdid', '932'),
            ('wdid', '933'),
            ('wdvalue', '0'),
            ('wdvalue', '0'),
            ('wdvalue', '0'),
            ('wdvalue', '无'),
            ('rwid', some_id),  # 不知道是啥，41
            ('xqid', kc['XQID']),  # 不知道是啥，12
            ('jsgh', kc['GH']),  # 教师工号
            ('kch', kc['KCH']),  # 课程号
            ('bzxh', kc['BZXH']),  # 不知道是啥，None
            ('jxbdm', kc['JXBDM']),  # 教务系统课程号
            ('xsxh', kc['XH']),  # 学号
            ('zf', '100.00'),
            ('pjjgid', kc['PJJGID'])  # 评价结果 id
        ]
        createStudentPjpf_response = s.post(createStudentPjpf, data=data)
        if createStudentPjpf_response.text == '{}':
            print('{}评价成功'.format(kc['KCMC']))


@click.command()
@click.option('--username', prompt='学号')
@click.option('--password', prompt='信息门户密码（默认身份证后 6 位）')
def pingjiao(username, password):
    global lt
    global dllt
    global execution
    global _eventId
    global rmShown

    # 首次请求，获取隐藏参数
    start_response = s.get(login)
    start_html = etree.HTML(start_response.text, parser=etree.HTMLParser())
    lt = start_html.xpath('//*[@id="casLoginForm"]/input[1]/@value')[0]
    dllt = start_html.xpath('//*[@id="casLoginForm"]/input[2]/@value')[0]
    execution = start_html.xpath('//*[@id="casLoginForm"]/input[3]/@value')[0]
    _eventId = start_html.xpath('//*[@id="casLoginForm"]/input[4]/@value')[0]
    rmShown = start_html.xpath('//*[@id="casLoginForm"]/input[5]/@value')[0]
    pwdDefaultEncryptSalt = start_html.xpath('//*[@id="casLoginForm"]/input[6]/@value')[0]

    # 调用 JavaScript 对密码加密
    with open('encrypt.js', 'r') as f:
        js = f.read()
    ctx = execjs.compile(js)
    password = ctx.call('encryptAES', password, pwdDefaultEncryptSalt)

    kc_list = get_kc(username, password)
    for kc in kc_list:
        pingjia(kc)
    get_kc(username, password)


if __name__ == '__main__':
    pingjiao()
