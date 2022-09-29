# @Author : yan1079
# @Time : 2022/8/12 10:30

import requests
import json

from get_instanceCode import GetInstanceCode


class CustomerOpr:
    def __init__(self, customerId, productId,  shopId, orderDate):
        gc = GetInstanceCode(shopId, productId)
        self.customerId = customerId
        self.productId = productId
        self.shopId = shopId
        self.orderDate = orderDate
        self.instanceCode = gc.get_data()[5]
        self.tenantCode = gc.get_data()[4]
        self.headers = {"Accept": "application/json",
                        "Content-Type": "application/json"}



    def customerProduct_supplylist(self):
        '''
        根据[客户编码+商品编码+(供货主体编码)]批量查询供货主体信息,支持状态过滤
        :return:
        '''
        url = 'http://172.22.226.13:8992/shsc-bizcore-customer-datacenter/customerProduct/supplylist?status=0'
        data = '[{"configDate":"%s","customerId":"%s","productId":"%s","shopId":"%s","instanceCode": "%s","tenantCode": "%s"}]' %(self.orderDate,self.customerId, self.productId, self.shopId, self.instanceCode, self.tenantCode)
        print("基础数据查询供应商信息入参："+data)
        res = requests.post(url=url, data=data, headers=self.headers).text
        print("基础数据查询供应商信息出参：" + res)
        try:
            cooperateBusinessId = json.loads(res)["data"][0]["cooperateBusinessId"]
            cooperateBusinessName = json.loads(res)["data"][0]["cooperateBusinessName"]
            print("查询供货主体信息为："+cooperateBusinessId+'/'+cooperateBusinessName)
            return cooperateBusinessId
        except IndexError as e:
            print(e)


    def shscSkuPrice(self):
        '''
        获取内销蜀海商品信息
        :return:返回商品价格
        '''
        url = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/v3/product/price/shscSku/list'
        data = {
                "auditStatus": "1",
                "cityCode": "100001",
                "customerCode": "%s"%self.customerId,
                "isQueryExistingSupply": "0",
                "orderDate":"%s"%self.orderDate,
                # "orderDate": "%s"%self.orderDate,
                "productCodes": [
                    {
                        "instanceCode": "%s"%self.instanceCode,
                        "productCode": "%s"%self.productId,
                        "tenantCode": "%s"%self.tenantCode
                    }
                ]
            }
        print("查询基础数据价格入参为：" + json.dumps(data))
        res = requests.post(url=url, data=json.dumps(data), headers=self.headers).text
        print("查询基础数据价格出参为：" + res)
        salePrice = json.loads(res)["data"][0]["salePrice"]
        if salePrice != None:
            print("查询基础数据价格为：" + str(salePrice))
        else:
            print("查询基础数据价格为不存在")
        return salePrice
        # print(availableQty)




if __name__ == '__main__':
    c_opr = CustomerOpr("0W30020860", "4210356001", "0W50237321", "2022-09-09")
    c_opr.customerProduct_supplylist()
    c_opr.shscSkuPrice()
