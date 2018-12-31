# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import urllib, zipfile, re, os, json


# Create your views here.
def init(request):
    results = []
    img_list = json.loads(request.body)
    mkdir('downloadImg')

    for img in img_list:
        imgUrl = img['url']
        imgPath = 'downloadImg' + '/' + img['title']
        fileName = re.findall(r"\/([^/]+\.\w+$)", imgUrl)[0]
        mkdir(imgPath)
        urllib.urlretrieve(imgUrl, imgPath + '/' + fileName)

    compress('downloadImg', 'images.zip')
    return returnFile('images.zip')


def mkdir(path):
    if not os.access(path, os.R_OK):
        os.mkdir(path)


def compress(get_files_path, set_files_path):
    f = zipfile.ZipFile(set_files_path , 'w', zipfile.ZIP_DEFLATED )
    for dirpath, dirnames, filenames in os.walk( get_files_path ):
        fpath = dirpath.replace(get_files_path,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            f.write(os.path.join(dirpath,filename), fpath+filename)
    f.close()


def returnFile(fileUri):
    file = open(fileUri, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="images.zip"'
    return response