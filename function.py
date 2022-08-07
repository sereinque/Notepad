import datetime
import json
import PySimpleGUI as sg

#读写数据函数
def readData(readfp):
    with open(readfp,'r',encoding='utf-8') as fp:
        jsondata=fp.read()
        datalist=json.loads(jsondata)
    return datalist

#写入数据函数
def writeData(data,writefp):
    jsondata=json.dumps(data,ensure_ascii=False)
    #ensure_ascii=False,保证不改变编码方式
    with open(writefp,'w',encoding='utf-8') as fp:
        fp.write(jsondata)

    # 弹窗
    sg.popup("写入成功")

#获取数据
def getData(readfp):
    data=readData(readfp)
    datavalues=[]

    for i in data:
        datavalue=[i['时间'],i['事件'],i['内容'],i['标记']]
        datavalues.append(datavalue)

    return datavalues

#添加数据
class Adddata:
    def __init__(self,thing=0,detail=0,star=0):
        self.thing=thing
        self.detail=detail
        self.star=star

def addData(adddata,readfp):
    datalist=readData(readfp)
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data={"时间":time,"事件":adddata.thing,"内容":adddata.detail,"标记":adddata.star}
    datalist.append(data)
    writeData(datalist,readfp)


#界面

def mainShow(readfp):
    datalist=getData(readfp)
    sum=len(readData(readfp))
    print(datalist)
    #表格
    layout=[
        [sg.T("记事本")],
        [sg.Table(datalist,
                  headings=["时间","事件","内容","标记"],
                  key="-show-",
                  justification='c',
                  auto_size_columns=False,
                  size=(120,20),
                  def_col_width=28,
                  )],
        [sg.T("事件数目："+str(sum),key='-text-')],
        [sg.T("输入事件"),sg.In(key='-thing-')],
        [sg.T("输入内容"),sg.In(key='-detail-')],
        [sg.T("标    记"),sg.In(key='-star-')],
        [sg.B("提    交")],
    ]

    windows=sg.Window("记事本",layout,default_element_size=(130,70))

    while True:
        event,values=windows.read()
        if event=="提    交":
            adddata=Adddata(values['-thing-'],values['-detail-'],values['-star-'])
            addData(adddata,readfp)
            newlist=getData(readfp)
            windows['-show-'].update(values=newlist)
            sum+=1
            newtext="事件数目：" + str(sum)
            windows['-text-'].update(value=newtext)
        if event==None:
            break
    windows.close()