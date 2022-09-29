# @Author : yan1079
# @Time : 2022/8/12 10:30

import requests
import jsonpath
import json


class SearchStock:
    def __init__(self, customerId, productId, spuCode, shopId, unitName):
        self.customerId = customerId
        self.productId = productId
        self.shopId = shopId
        self.spuCode = spuCode
        self.unitName = unitName
        self.headers = {"Accept": "application/json",
                        "Content-Type": "application/json"}


    def customerProduct_supplylist(self):
        '''
        根据[客户编码+商品编码+(供货主体编码)]批量查询供货主体信息,支持状态过滤
        :return:
        '''
        url = 'http://172.22.226.13:8992/shsc-bizcore-customer-datacenter/customerProduct/supplylist?status=0'
        data = '[{"customerId":"%s","productId":"%s","shopId":"%s"}]' %(self.customerId, self.productId, self.shopId)
        # print(data)
        res = requests.post(url=url, data=data, headers=self.headers).text
        print(res)
        cooperateBusinessId = json.loads(res)["data"][0]["cooperateBusinessId"]
        return cooperateBusinessId


    def batchAvailableQty(self):
        '''
        多货主物料查询
        :return:返回进销存中存在的物料的spuCode、单位、可用数量
        '''
        url = 'http://172.22.226.11:9303/external/inventory/batchAvailableQty'
        data = {
                "areaCode": "200001",
                "ownerAndSpuList": [
                    {
                        "goodsOwnerCode": f'{self.customerProduct_supplylist()}',
                        "spuCodes": [
                            f"{self.spuCode}"
                        ]
                    }
                    ]
                }
        # print(data)
        res = requests.post(url=url, data=json.dumps(data), headers=self.headers).text
        # print(res)
        availableQty = json.loads(res)["data"][0]["inventoryQuantity"][0]["availableQty"]
        print("查询交付基本单位库存为："+str(availableQty))
        return availableQty
        # print(availableQty)


    def queryByGroupCodes(self):
        '''
        根据groupCodes 查询sku集合
        :return:
        '''
        url = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/productsku/queryByGroupCodes?tenantCode=00000'
        data = f'["{self.spuCode}"]'
        # print(data)
        res = requests.post(url=url, data=data, headers=self.headers).text
        groupCodes = jsonpath.jsonpath(json.loads(res), f'$.data.[?(@.unitName=="{self.unitName}")]')[0]
        # print(groupCodes)
        conversionNumerator = groupCodes["conversionNumerator"]
        conversionDenominatr = groupCodes["conversionDenominatr"]
        print("查询基础数据换算比为："+ conversionNumerator+':'+conversionDenominatr)
        return int(conversionNumerator)/int(conversionDenominatr)


    def convertStock(self):
        availableQty =self.batchAvailableQty()
        queryByGroupCodes = self.queryByGroupCodes()
        if availableQty <= 0:
            print("%s该物料获取销售库存数量为：0"%self.productId)
        else:
            convert_availableQty = availableQty / queryByGroupCodes
            if convert_availableQty < 0.5:
                print("%s该物料获取销售库存数量为：0" % self.productId)
            elif convert_availableQty >= 1000000:
                convert_availableQty = int(convert_availableQty/10000)
                print("%s该物料获取销售库存数量为：%s万" %(self.productId, convert_availableQty))
            else:
                convert_availableQty = round(convert_availableQty, 2)
                print("%s该物料获取销售库存数量为：%s" %(self.productId, convert_availableQty))





if __name__ == '__main__':
    sea_stock = SearchStock("0W30000102", "4000460001", "4000460", "0W50082448", "公斤")
    # print(sea_stock.customerProduct_supplylist())
    sea_stock.batchAvailableQty()
    # sea_stock.queryByGroupCodes()
    # sea_stock.convertStock()