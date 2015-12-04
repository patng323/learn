import pandas as pd

productDf = None

def initProductInfo():
    global productDf
    dataPath = '/Users/patrickng/Documents/nw/data/products.csv'
    imgBase = "http://www.price.com.hk/space/product/"
    if productDf is None:
        print "productDf inited"
        productDf = pd.read_csv(dataPath,
                names=['id', 'brand', 'name', 'c0_id', 'c0', 'c1_id', 'c1', 'c2_id', 'c2', 'priceType', 'price', 'img' ])
        productDf.set_index('id', inplace=True)
        productDf.ix[:,'img'] = imgBase + productDf.ix[:, 'img']

print "calling initProductInfo..."
initProductInfo()
print type(productDf)