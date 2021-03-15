from django.http import HttpResponse
from django.shortcuts import render
import requests
import re

class Info(object):
    def __init__(self,name,allbugs,passbugs,passpercent,rank,low,mid,high,critical):
        self.name=name
        self.allbugs=allbugs
        self.passbugs=passbugs
        self.passpercent=passpercent
        self.rank=rank
        self.low=low
        self.mid=mid
        self.high=high
        self.critical=critical

def hello(request):
    return HttpResponse('Hello,welcome to MXPY\'s Django project.')

def error(request,exception=404):#Django新版本需要加上exception
    return render(request,'hack.html',status=404)
def whitehat(request):
    id=str(request.GET.get("id"))
    user=getWhitehatInfo(id)
    return render(request,'whitehat.html',{'user':user})

def getWhitehatInfo(id):
    low=0
    mid=0
    high=0
    critical=0
    name=''
    percent=0.0
    #id=input('请输入用户ID：')
    for i in range(1,999):#此处设置为999为了不用控制页数，使用try进行中断
        userHomeUrl='https://src.sjtu.edu.cn/profile/'+id+'/?page='+str(i)
        backInfo=requests.get(userHomeUrl)
        #print(backInfo.text)
        try:
            #终止循环
            break_str='?page='+str(i)
            #if backInfo.text.find(break_str)==-1:
            if backInfo.text.find(break_str)==-1 and i!=1:#完成后修改，防止页数不足一页而跳出循环
                #print('第'+str(i)+'页，不存在，循环终止！')
                break
            #正则规则中保留尖括号为了提高准确率，防止匹配到用户昵称和用户签名
            r_name=r'<title>.+ 的个人中心'
            r_total=r'总提交漏洞数量：.+'
            r_valid=r'已审核通过漏洞数量：.+'
            r_rank=r'Rank： \d+'
            r_low=r'>低危<'
            r_mid=r'>中危<'
            r_high=r'>高危<'
            r_critical=r'>严重<'
            if name=='':
                name=re.search(r_name,backInfo.text).group().replace('<title>','')
                name=name.replace(' 的个人中心','')
            total=re.search(r_total,backInfo.text).group().replace('总提交漏洞数量： ','')
            valid=re.search(r_valid,backInfo.text).group().replace('已审核通过漏洞数量： ','')#此处采用偷懒式写法，偷懒但有效,注意冒号后有一个空格
            rank=re.search(r_rank,backInfo.text).group().replace('Rank： ','')
            low_result=re.findall(r_low,backInfo.text)
            mid_result=re.findall(r_mid,backInfo.text)
            high_result=re.findall(r_high,backInfo.text)
            critical_result=re.findall(r_critical,backInfo.text)
            #开始计算总通过率
            #print(total)
            if percent==0.0:
                percent='%.4f'%(float(valid)/float(total))
                percent_str='%.2f'%(float(percent)*100.00)+'%'
                #percent_str=str(float(percent)*100.00)+'%'
                #修改写法，解决输出精度问题-2021-02-19
                #percent_str='%.2f'%(float(percent)*100.00)+'%'
            #计算完毕
            #计算各等级漏洞数
            low=low+len(low_result)
            mid=mid+len(mid_result)
            high=high+len(high_result)
            critical=critical+len(critical_result)
            #状态报告
            #print('第'+str(i)+'页，已处理！') 开发web页面注释此行
            #开始计算等级占比
            #开发中途废弃，原因为：各个用户可能存在不同等级漏洞为0的情况。
            '''
            low_percent='%.4f'%(float(low)/float(total))
            low_percent_str=str(float(low_percent)*100.00)+'%'
            mid_percent='%.4f'%(float(mid)/float(total))
            mid_percent_str=str(float(mid_percent)*100.00)+'%'
            high_percent='%.4f'%(float(high)/float(total))
            high_percent_str=str(float(high_percent)*100.00)+'%'
            critical_percent='%.4f'%(float(critical)/float(total))
            critical_percent_str=str(float(critical_percent)*100.00)+'%'
            '''
            #print(percent_str)
        except:
            #print('出现异常，中断进程')
            break
    #打印空行
    #print('')
    #print('计算完毕\n用户昵称：'+name+'\n总漏洞：'+str(total)+'\t总Rank：'+rank+'\t已通过：'+str(valid)+'\t通过率：'+percent_str+'\n低危：'+str(low)+'\t中危：'+str(mid)+'\t高危：'+str(high)+'\t严重：'+str(critical))
    return Info(name,total,valid,percent_str,rank,low,mid,high,critical)
