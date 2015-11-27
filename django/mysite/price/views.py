from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import urllib
import urllib2
from json import JSONEncoder
import json
from lxml import html
import requests
from urlparse import urlparse


# Create your views here.
def index(request):
    context = {'irange': range(5)}
    return render(request, 'price/index.html', context)

def getPriceProductInfo(productId):
    url = 'http://www.price.com.hk/product.php?p=' + str(productId)
    page = requests.get(url)
    parsedUrl = urlparse(url)
    basePath = parsedUrl.scheme + "://" + parsedUrl.hostname

    tree = html.fromstring(page.content)

    productName = tree.xpath('//*[contains(@class, "product-name")]')[0].text
    img = tree.xpath('//*[contains(@id, "product-image-img")]')[0].attrib['src']
    imgPath = basePath + img

    return productName, imgPath

def searchPio(critera):
        url = 'http://localhost:8000/queries.json'
        headers = { 'Content-Type' : 'application/json' }
        jsonStr = JSONEncoder().encode(critera)
        req = urllib2.Request(url, data=jsonStr, headers=headers)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())

        return result['itemScores']

def search(request):
    userid = request.GET.get('u', '')
    if len(userid) > 0:
        criteria = { "user": userid }
        items = searchPio(criteria)

        # Add price product name and photos
        for item in items:
            productId = item['item']
            productId = 215606

            productName, imgPath = getPriceProductInfo(productId)

            item['productName'] = productName
            item['img'] = imgPath

        context = { 'items': items, 'userid': userid}
        return render(request, 'price/search.html', context)
    else:
        return HttpResponse("Search is called: user=%s" % userid)