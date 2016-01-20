#from __future__ import unicode_literals
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
        return json.loads(response.read())

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
    cat = request.GET.get('cat', '')
    catFactor = request.GET.get('catFactor', '2.5')
    brandBst = request.GET.get('brandBst', '')
    brandFactor = request.GET.get('brandFactor', '2.5')
    priceBst = request.GET.get('priceBst', '')
    priceFactor = request.GET.get('priceFactor', '2.5')
    itemProduct = getItemProduct()
    criteria = {}

    if len(userId) > 0:
        criteria["user"] = userId
        criteria["getHistory"] = True

    if len(itemId) > 0:
        criteria["item"] = itemId
        itemProduct = getItemProduct(itemId)

    addBoostOrFilter("categories", cat, catFactor, criteria)
    addBoostOrFilter("brand", brandBst, brandFactor, criteria)
    addBoostOrFilter("level", priceBst, priceFactor, criteria)

    # if len(brandBst) > 0:
    #     criteria['fields'] = criteria.get('fields', []) + [
    #                      {
    #                          "name":"brand",
    #                          "values":brandBst.split(','),
    #                          "bias":float(brandFactor)
    #                      }
    #     ]
    #
    # if len(priceBst) > 0:
    #     criteria['fields'] = criteria.get('fields', []) + [
    #                      {
    #                          "name":"level",
    #                          "values":priceBst.split(','),
    #                          "bias":float(priceFactor)
    #                      }
    #     ]

    if len(criteria) > 0:
        result = searchPio(criteria)
        items = result['itemScores']
        history = result['historyItems']
    else:
        result = items = history = []

    for item in items:
        item['product'] = getItemProduct(item['item'])

    history = sorted(history, key=lambda h: h['event'])
    for h in history:
        h['product'] = getItemProduct(h['item'])

    if items is not None:
        context = { 'items': items, 'userid': userId, 'itemid': itemId, 'itemProduct': itemProduct,
                    'cat': cat,
                    'catFactor': catFactor,
                    'brandBst': brandBst,
                    'brandFactor': brandFactor,
                    'priceBst': priceBst,
                    'priceFactor': priceFactor,
                    'history': history}
        return render(request, 'price/search.html', context)
    else:
        return HttpResponse("Search is called: user=%s" % userId)


def addBoostOrFilter(fieldName, bstStr, bstFactor, criteria):
    if len(bstStr) > 0:
        criteria['fields'] = criteria.get('fields', []) + [
            {
                "name": fieldName,
                "values": bstStr.split(','),
                "bias": float(bstFactor)
            }
        ]