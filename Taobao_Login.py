# -*- coding: utf-8 -*-
"""
输入： 淘宝用户名，UA，RSA后的密码（后两者，每次登陆都不一样，拥有复杂的算法，我们需要通过
       firefox捕捉一次合法的（UA,RSA后的密码））
       
输出： COOKIE，用于后续登陆后的操作

"""

import requests
import re
import webbrowser

url = 'https://login.taobao.com/member/login.jhtml'
username = '554128639@qq.com'
password = '911010com'
#ua是淘宝根据复杂的算法算得的，每次都不同
ua = """076UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5OcktyTnVKcE52SHxBfCo=|U2xMHDJ
        +H2QJZwBxX39Rb1t1VXsnRiBMK1UvAVcB|VGhXd1llXGVZYl1nWWFfa1ZrXGFDe0d5Q3tCeE
        x2SHxGeEN5TGI0|VWldfS0SMg01Di4SLAwiBiIfbldqXisWKhAsCSdxJw==|VmNDbUMV|V2N
        DbUMV|WGRYeCgGZhtmH2VScVI2UT5fORtmD2gCawwuRSJHZAFsCWMOdVYyVTpbPR99HWAFYV
        MoRSlIM141SBZPCTlZJFkgWnNMdEoBKBcvEFx1SnJNAWBCP1YxWzJVdxx7HjcIMA9DJlYCfx
        ZxG3IVN1cqT2ZZYV8TdRh7HGFId09xP1IWXz9BBG49AH5XaFBvV2knDjEJNg4wfkJ7Qn5Fek
        B9QnlEeUZoSGZIHkg=|WWdHFyMZOQQkGCYfKws+CjMTLxEqETELMAUlGSccJwc9AjdhNw==|
        WmZYeCgGWjtdMVYoUn5EakpkOHs/Ey8aOgcnGjoFOwQqfCo=|W2FBET9gO30pUDlDOUcgWzd
        jX3FRbU1zSR9J|XGBdfVMDPAI7ADUVQmxQaVBsV2hUblZjXGhdKBU3DjUPMgwxDjEEOQE1AD
        UINQxbdVVpPxFH|XWdHFzlmPXsvVj9FP0EmXTFlWXdXakp2Q3lGEEY=|XmREFDoUNAkpFSAa
        Lngu|X2dHFzlmPXsvVj9FP0EmXTFlWXdXBzMPOhokGSRyUm9PYU9vUG5Vb1MFUw==|QHpaCi
        QKKhY2CTcMNgJUAg==|QXtbCyV6IWczSiNZI106QS15RWtLd1doVm1ZZjBm|QnhYCCZ5ImQw
        SSBaIF45Qi56RmhIdVVqUWtTbjhu|Q3lZCScJKRQ0CzAKMQ5YDg==|RH1dDSN8J2E1TCVfJV
        s8Ryt/Q21NeU14WGdSa0t0TnBKdCJ0|RX1dDSN8J2E1TCVfJVs8Ryt/Q21NHSkSKQk2AjxqS
        ndXeVd3SHJKcEkfSQ==|RnxcDCIMLBAwDzUNOAZQBg==|R31dDSN8J2E1TCVfJVs8Ryt/Q21
        NcVFuVGxYZTNl|SHBQAC5uOmIedBFwDVUoQTxdNhg4aFxnWXlHckYQMA0tAy0NMww4AT1rPQ
        ==|SXNTAy1yKW87QitRK1UySSVxTWNDfl5gX2tTbDps|SnBQAC5uOmIedBFwDVUoQTxdNhg4
        BCQaJREqFEIU|S3JPclJvT3BQbFVpSXdPdVVtWXlDe1tnW2JCfl5iWWREek5uW29PcUtrVW5
        Ock5uUGlJd0lpV2hIdkpqS3VVbU1yR2dYYkJ9XWJaekV8Kg==
      """
#RSA后的密码，实际被提交到服务器的也是这个密码，加密的key和ua相关，所以每次都不同
encrypted_password = """
        8fbf8c5438808118e6896a352730468a8bd8bb350f6ca14dd9a27bb
        121bc838fa6b28f69c49967946d7480391ea7f6914d69313e4fc2388e710527478c69eda5bccf6a
        b9fc2857d52c0042ccbe7c26ad354af57c275f8a3e3b854c5863045de83f6e3079053da7e986feb
        72a7c3079b601b0f0fd2125128ae5edff1db6dc34aa"""

def format_long_str(_str):
    """
        格式化 ua 和加密后的密码
        
    """
    return ''.join(_str.split('\n')).strip().replace(' ','')

ua = format_long_str(ua)
encrypted_password = format_long_str(encrypted_password)

#主类
class Taobao:
    headers ={
                'Host':'login.taobao.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding':'gzip, deflate',
                'Referer':'https://login.taobao.com/member/login.jhtml',
                }

    #post的参数
    params = {
            'ua':ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username':username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':encrypted_password,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
                
             }

     
    def setHeaders(self,params):
        """
            更新header
        """
        self.headers = dict(self.headers,**params)

    def setParams(self,params):
        """
            更新post过去的参数
        """
        self.params = dict(self.params,**params)


    def _judge_checkcode(self,content):
        """
            判断输入的验证码是否正确
        """
        wrong_checkcode_pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef',re.S)
        if re.search(wrong_checkcode_pattern,content):
            print u'验证码错误'
            exit(-1)

    def _check_Jtoken(self,content):
        """
            判断JToken是否存在
        """
        tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
        tokenMatch = re.search(tokenPattern,content)
        #如果匹配成功，找到了J_HToken
        try:
            self.Jtoken = tokenMatch.group(1)
            print u"JTOKEN 获取成功"
        except:
            #匹配失败，J_Token获取失败
            print u"J_Token获取失败"
            exit(-1)

    def _get_ST(self):
        """
            通过JTOKEN 来获取ST
        """
        tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % self.Jtoken
        st_response = requests.get(tokenURL,headers=self.headers)
        #处理st，获得用户淘宝主页的登录地址
        pattern = re.compile('{"st":"(.*?)"}',re.S)
        result = re.search(pattern,st_response.text)
        try:
            #获取st的值
            st = result.group(1)
            self.st = st
            print u"成功获取st码"
            
        except:
            print u"未匹配到st"
            exit(1)
            
    def _login(self):
        #第一次登陆
        first_response = requests.post(url,data=self.params,headers=self.headers)
        #判断是否登陆被拒绝 并被要求提交邀请码
        need_checkcode_pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
        needCheckcode = re.search(need_checkcode_pattern,first_response.text)
        #如果被要求提交邀请码，则通过getCheckcode 来获取图片，在浏览器打开，手工填入后
        #再次提交请求
        if needCheckcode:
            checkCode = self.getCheckcode(first_response.text)
            webbrowser.open_new_tab(checkCode)
            #更新params，再次提交请求
            self.setParams({'TPL_checkcode':raw_input(u'请输入验证码:')})
            #获得第二次请求的内容后，判断是否验证码输入正确
            content = requests.post(url,data=self.params,headers = self.headers,cookies=first_response.cookies).text 
            self._judge_checkcode(content)
        #无需验证码 就直接获取JToken
        else:
            content = first_response.text
            
        #判断返回结果是否带有J_HToken字样
        self._check_Jtoken(content)
        #通过JTOKEN 来获取ST
        self._get_ST()
        return self.st

    def _is_login_successfully(self,content):
        """
            检测是否登陆成功 如果成功就设置cookies
        """
        pattern = re.compile('top.location = "(.*?)"',re.S)
        match = re.search(pattern,content)
        try:
            location = match.group(1) 
            print u"登录网址成功"
            return True
        except:
            print "登录失败"
            exit(-1)
            
    def login(self):
        """
            通过_login 来获取 ST， 然后直接在这个函数里面登陆,并设定登陆后的self.cookie
            用来备用
        """
        self._login()
        stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (self.st,username)
        #更新header
        self.setHeaders({'Connection':'Keep-Alive'})
        login_response = requests.get(stURL,headers=self.headers)
        #检测结果，看是否登录成功
        if self._is_login_successfully(login_response.text):
                self.cookies = login_response.cookies     
        
            
    def getCheckcode(self,page):
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1): 
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容,登陆失败"
            exit(-1)

if __name__ == '__main__':
    t = Taobao()
    t.login()
    _cookies = t.cookies
    _headers = t.headers
    goodsURL = 'http://buyer.trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1' + '&pageNum=1'
    response = requests.get(goodsURL,cookies=_cookies)
    print response.text
