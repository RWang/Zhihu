# -*- coding:utf-8 -*-

import urllib.request
import re
import HTMLParser
import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')



def getHtml(url):
    header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36', 'Referer': '*****'}
    request = urllib.request.Request(url,headers=header)
    response = urllib.request.urlopen(request)
    text = response.read()
    return text

def getUrls(html):
    pattern = re.compile('http://daily.zhihu.com/story/(.*?)',re.S)
    items = re.findall(pattern,html)
    urls = []
    for item in items:
        urls.append('http://daily.zhihu.com/story/' +item)
    return urls



def getContent(url):
    html = getHtml(url)
    pattern = re.compile('<h1 class= "headline-title">(.*?)</h1>')
    items = re.findall(pattern,html)
    print('***************************************************')
    print('********************' + items[0] + '*******************************')
    print('***************************************************')

    pattern = re.compile('<div class="content">\\n<p></div>',re.S) 
    items_withtag = re.findall(pattern,html)
    for item in items_withtag:
        for content in characterProcessing(item):
            print(content)



def characterProcessing(html):
    htmlParser = HTMLParser.HTMLParser()
    pattern = re.compile('<p>(.*?)</p>|<li>(.*?)</li>.*?',re.S)
    items = re.findall(pattern.html)
    result = []
    for index in items:
        if index != '':
            for content in index:
                tag = re.search('<.*?>',content)
                http = re.search('<.*?http.*?',content)
                html_tag = re.search('&',content)
                if html_tag:
                    content = htmlParser.unescape(content)
                if http:
                    continue
                elif tag:
                    pattern = re.comppile('(.*?)<.*?>(.*?)</.*?>(.*)')
                    items = re.findall(pattern.content)
                    content_tags = ''
                    if len(items) > 0:
                        for item in items:
                            if len(item) > 0:
                                for item_s in item:
                                    content_tags = content_tags + item_s
                            else:
                                content_tags = content_tags + item_s
                        content_tags = re.sub('<.*?>','',content_tags)
                        result.append(content_tags)
                    else:
                        continue
                else:
                    result.append(content)
    return result


def main():
    for i in range(1,5):
        print('page%s'%i)
        url = "http://zhihudaily.ahorn.me/page/&s"%i
        html = getHtml(url)
        urls = getUrls(html)
        for url in urls:
            try:
                getContent(url)
            except Exception as e:
                print(e)

main()