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
from price import productDf

# Create your views here.
def index(request):
    context = {'irange': range(5)}
    return render(request, 'price/index.html', context)

def getPriceProductInfofromWeb(productId):
    url = 'http://www.price.com.hk/product.php?p=' + str(productId)
    page = requests.get(url, timeout=10)
    parsedUrl = urlparse(url)
    basePath = parsedUrl.scheme + "://" + parsedUrl.hostname

    tree = html.fromstring(page.content)

    node = tree.xpath('//*[contains(@class, "product-name")]')
    productName = '!! Not found !!' if node is None or len(node) == 0 else node[0].text

    node = tree.xpath('//*[contains(@id, "product-image-img")]')
    imgPath = '' if node is None or len(node) == 0 else basePath + node[0].attrib['src']

    return productName, imgPath

def searchPio(critera):
        url = 'http://localhost:8000/queries.json'
        headers = { 'Content-Type' : 'application/json' }
        jsonStr = JSONEncoder().encode(critera)
        req = urllib2.Request(url, data=jsonStr, headers=headers)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())

        return result['itemScores']

def getItemProduct(productId = None):
        itemProduct = {'brand':'', 'name':'', 'cat':''}

        if productId is not None:
            try:
                product = productDf.loc[int(productId)]
                itemProduct = product.to_dict()
                itemProduct['cat'] = product['c0'] + " / " + product['c1'] + " / " + product['c2']
            except:
                pass

        return itemProduct

def search(request):

    userId = request.GET.get('u', '')
    itemId = request.GET.get('i', '')
    itemProduct = getItemProduct()

    if len(userId) > 0:
        criteria = { "user": userId }
    elif len(itemId) > 0:
        criteria = { "item": itemId}
        itemProduct = getItemProduct(itemId)

    items = searchPio(criteria)

    for item in items:
        productId = int(item['item'])
        item['product'] = getItemProduct(productId)

    if items is not None:
        context = { 'items': items, 'userid': userId, 'itemid': itemId, 'itemProduct': itemProduct}
        return render(request, 'price/search.html', context)
    else:
        return HttpResponse("Search is called: user=%s" % userId)