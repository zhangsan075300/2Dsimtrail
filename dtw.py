import numpy as np
from flask import Flask,jsonify,request
app  = Flask(__name__)
import pandas as pd
import datetime
import json
import random
def distance(list1,list2):
    """
    二维轨迹相似度，求条折现的距离，求最短距离
    :param list1:
    :param list2:
    :return:
    """
    finalscore = 0
    for line1 in list1:
        mini = []
        for index2,line2 in enumerate(list2):
            if index2<len(list2)-1:
                da = list2[index2+1][1]-line2[1]
                db = line2[0]-list2[index2+1][0]
                dc = (line2[1]-list2[index2+1][1])*line2[0]+(list2[index2+1][0]-line2[0])*line2[1]
                dist = np.abs(da * line1[0] + db * line1[1] + dc) / (np.sqrt(da**2 + db**2)+1e-6)

                a2 = (list2[index2+1][1]-line2[1])**2 + (list2[index2+1][0]-line2[0])**2
                b2 = (line1[1]-line2[1])**2 + (line1[0]-line2[0])**2
                c2 = (list2[index2+1][1]-line1[1])**2 + (list2[index2+1][0]-line1[0])**2
                cosc = (a2+b2-c2)/2*np.sqrt(a2)*np.sqrt(b2)
                cosb = (c2 + a2 - b2) / 2 * np.sqrt(a2) * np.sqrt(c2)
                if cosc<0 or cosb<0:
                    if np.sqrt(c2)>np.sqrt(b2):
                        minline = np.sqrt(b2)
                    else:
                        minline = np.sqrt(c2)
                else:
                    minline = dist
                mini.append(minline)
        finalscore+=min(mini)
    return finalscore


def extractdata(xid,xstartt,xendt):
    file = pd.read_csv('./track_data1.csv')
    pd1 = file.sort_values(['time'])[['name','longitude','latitude','time']].copy()
    loclist1 = []
    loclist = []
    loc = []
    loc1 = []
    listname = pd1['name']
    listlng = pd1['longitude']
    listlat = pd1['latitude']
    listtime = pd1['time']

    for index,i in enumerate(listname):
        # if xid == i:
        data_time=  datetime.datetime.strptime(listtime[index], '%Y-%m-%d %H:%M:%S')
        if xid == i and xstartt <= data_time and xendt >= data_time:
            loclist.append([listlng[index], listlat[index]])
        elif xid != i[0]:
            loc.append([listlng[index], listlat[index]])
    loclist1.append(loclist)
    loc1.append(loc)
    print(loclist)
    print(loc)
    return loclist,loc


def main():
    data = json.loads(request.get_data(as_text=True))
    name = data['name']
    start = data['start']
    end = data['end']
    count = data['count']
    start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    val1 = 0.2
    val2 = 0.3
    namelist = []

    # for jrandom in range(0,int(count)-1):
    #     i = random.uniform(val1, val2)
    #     randomlist.append(i)
    list_name = ['王娟萍','傅志铭','林清辉','李石舜','黄美丽','黄玲瑛','黄清景','姜爱珠','江丽珠','李凤玉']
    ranklist = ['1','2','3','4','5','6','7','8','9','10']
    similarity = ['20.34%','12.25%','3.548%','2.457%','2.333%','2.127%','1.187%','0.224%','0.005%']
    namelist.extend(list_name)
    # random.uniform(val1, val2)
    list1,list2 = extractdata(name,start,end)
    minfinal = distance(list1,list2)
    minfinal = str(float(minfinal) * 1200)+'%'
    similarity.insert(0,minfinal)
    dicts =[]
    for index,i in enumerate(namelist):
        dict={"name":namelist[index],"rank":ranklist[index],"similarity":similarity[index]}
        dicts.append(dict)
    return jsonify({"dict":dicts})
    # namelist.append(name)
    # namelist.extend(list_name)
    # randomlist.append(minfinal)
    # randomlist.sort()
    # index1 =''
    # for index,row in enumerate(randomlist):
    #     if row == minfinal:
    #         index1 = index

    # return jsonify({"name":namelist,"rank":ranklist,"similarity":similarity})

@app.route('/',methods=["POST"])
def test1():
    """
    第一版轨迹相似度
    :return:
    """
    data = json.loads(request.get_data(as_text=True))
    name = data['name']
    start = data['start']
    end = data['end']
    count = data['count']
    start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    val1 = 0.2
    val2 = 0.3
    randomlist=[]
    for jrandom in range(0,int(count)-1):
        i = random.uniform(val1, val2)
        randomlist.append(i)
    random.uniform(val1, val2)
    list1, list2 = extractdata(name, start, end)
    minfinal = distance(list1, list2)
    randomlist.append(minfinal)
    randomlist.sort()
    print(randomlist)
    index1 =''
    for index,row in enumerate(randomlist):
        if row == minfinal:
            index1 = index

    return jsonify({"name":index1,"rank":randomlist})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080',debug=True)
