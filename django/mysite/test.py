import json
from json import JSONDecoder

v = '{ \
	"itemScores": [{ \
		"item": "Galaxy", \
		"score": 0.8880454897880554 \
	}, { \
		"item": "Nexus", \
		"score": 0.288095086812973 \
	}, { \
		"item": "Surface", \
		"score": 0.05261862277984619 \
	}] \
}'

j = json.loads(v)

for item in j['itemScores']:
    print "Item:%s, Score:%f" % (item['item'], item['score'])


from lxml import html
import requests
from urlparse import urlparse

url = 'http://www.price.com.hk/product.php?p=215606'
page = requests.get(url)
parsedUrl = urlparse(url)
basePath = parsedUrl.scheme + "://" + parsedUrl.hostname

tree = html.fromstring(page.content)

product = tree.xpath('//*[contains(@class, "product-name")]')[0].text
img = tree.xpath('//*[contains(@id, "product-image-img")]')[0].attrib['src']
imgPath = basePath + img