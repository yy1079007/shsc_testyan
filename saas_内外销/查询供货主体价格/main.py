# @Author : yan1079
# @Time : 2022/9/9 14:45

import sys
import requests
import json

from datetime import datetime
from get_instanceCode import get_hashcode, GetInstanceCode
from searchprice_new_ui import Ui_MainWindow
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

time_new = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
# print(time_new)
class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}

        # 添加查询按钮信号和槽。
        self.radioButton.setChecked(True)
        self.pushButton.clicked.connect(self.shows)
        self.pushButton_2.clicked.connect(self.clearData)


    def printf(self, mes):
        self.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursot.End)
        QApplication.processEvents()

    def shows(self):
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser_4.clear()
        self.textBrowser_5.clear()
        self.textBrowser_6.clear()
        self.textBrowser_7.clear()
        self.textBrowser_8.clear()
        # customer_Id = self.lineEdit.text().strip()
        shop_Id = self.lineEdit_2.text().strip()
        product_Id = self.lineEdit_3.text().strip()
        order_Date = self.lineEdit_4.text().strip()
        city_Code = self.lineEdit_5.text().strip()
        if len(shop_Id) == 0 or len(product_Id) == 0 or len(order_Date)==0:
            QMessageBox.warning(self, "警告", "请检查输入信息不能为空")
        else:
            try:
                if self.comboBox.currentText() == '测试环境':
                    urls = self.get_url('test')
                    num = get_hashcode(shop_Id,'test')
                    sql1 = f'SELECT customer_code,source_code,tenant_code,instance_code,supply_tenant_code,supply_instance_code,unit_code,business_type,status,storage_type FROM t_customer_product_rel_{num} WHERE customer_code = "%s" AND source_code ="%s"' % ( shop_Id, product_Id)
                    sql2 = f'SELECT sap_code,parent_code FROM t_base_organization WHERE code = "%s"' % shop_Id
                    gc = GetInstanceCode().get_data(sql1,'test')
                    gc1 = GetInstanceCode().get_data(sql2,'test')

                elif self.comboBox.currentText() == 'UAT环境':

                    urls = self.get_url('uat')
                    num = get_hashcode(shop_Id,'uat')
                    sql1 = f'SELECT customer_code,source_code,tenant_code,instance_code,supply_tenant_code,supply_instance_code,unit_code,business_type,status,storage_type FROM t_customer_product_rel_{num} WHERE customer_code = "%s" AND source_code ="%s"' % ( shop_Id, product_Id)
                    sql2 = f'SELECT sap_code,parent_code FROM t_base_organization WHERE code = "%s"' % shop_Id
                    gc = GetInstanceCode().get_data(sql1, 'uat')
                    gc1 = GetInstanceCode().get_data(sql2, 'uat')

                elif self.comboBox.currentText() == '生产环境':
                    urls = self.get_url('pro')
                    num = get_hashcode(shop_Id,'pro')
                    sql1 = f'SELECT customer_code,source_code,tenant_code,instance_code,supply_tenant_code,supply_instance_code,unit_code,business_type,status,storage_type FROM t_customer_product_rel_{num} WHERE customer_code = "%s" AND source_code ="%s"' % ( shop_Id, product_Id)
                    sql2 = f'SELECT sap_code,parent_code FROM t_base_organization WHERE code = "%s"' % shop_Id
                    gc = GetInstanceCode().get_data(sql1, 'pro')
                    gc1 = GetInstanceCode().get_data(sql2, 'pro')

                tenantcode = gc[2]
                if tenantcode is None:
                    tenantcode ="无"
                instancecode = gc[3]
                if instancecode is None:
                    instancecode ="无"
                supplytenantcode = gc[4]
                if supplytenantcode is None:
                    supplytenantcode ="无"
                supplyinstancecode = gc[5]
                if supplyinstancecode is None:
                    supplyinstancecode ="无"
                unitCode = gc[6]
                business_type = gc[7]
                status = gc[8]
                storage_type =gc[9]
                factoryCode = gc1[0]
                customer_Id = gc1[1]

                print(tenantcode, instancecode, supplytenantcode, supplyinstancecode,unitCode,business_type)
                self.textBrowser_4.insertPlainText(tenantcode)
                self.textBrowser_5.insertPlainText(instancecode)
                self.textBrowser_6.insertPlainText(supplytenantcode)
                self.textBrowser_7.insertPlainText(supplyinstancecode)
                if status == 1:
                    self.textBrowser_8.insertPlainText("上架"+"----->>"+business_type+"----->>"+storage_type)
                else:
                    self.textBrowser_8.insertPlainText("下架"+"----->>"+business_type+"----->>"+storage_type)

                if self.radioButton.isChecked():
                    self.customerProduct_supplylist(urls[0],order_Date, customer_Id, product_Id, shop_Id, gc[5], gc[4])
                    self.shscSkuPrice(urls[1],city_Code, customer_Id, order_Date, gc[5], product_Id, gc[4])
                else:
                    supplierCode = self.get_supplierSapNum(urls[2],factoryCode, product_Id[:-3], gc[2], unitCode)
                    self.queryPriceByFacAndSku(urls[3],factoryCode, product_Id[:-3], supplierCode, unitCode, order_Date)
            except Exception as e:
                print(str(e))
                self.printf(str(e))

    def customerProduct_supplylist(self,url,orderDate,customerId, productId, shopId, supply_instance_code,supply_tenant_code):
        '''
        根据[客户编码+商品编码+(供货主体编码)]批量查询供货主体信息,支持状态过滤
        :return:
        '''
        # url = 'http://172.22.226.13:8992/shsc-bizcore-customer-datacenter/customerProduct/supplylist?status=0'
        data = '[{"configDate":"%s","customerId":"%s","productId":"%s","shopId":"%s","instanceCode": "%s","tenantCode": "%s"}]' %(orderDate,customerId, productId, shopId, supply_instance_code, supply_tenant_code)
        self.printf(time_new+ "基础数据查询供应商信息入参：\n"+data)
        print("基础数据查询供应商信息入参："+data)
        res = requests.post(url=url, data=data, headers=self.headers).text
        print("基础数据查询供应商信息出参：" + res)
        self.printf(time_new+ "基础数据查询供应商信息出参：\n" + res)
        try:
            cooperateBusinessId = json.loads(res)["data"][0]["cooperateBusinessId"]
            cooperateBusinessName = json.loads(res)["data"][0]["cooperateBusinessName"]
            self.textBrowser_2.insertPlainText(cooperateBusinessId+'/'+cooperateBusinessName)
            print("查询供货主体信息为："+cooperateBusinessId+'/'+cooperateBusinessName)
            # return cooperateBusinessId
        except IndexError as e:
            self.textBrowser_2.insertPlainText("无")


    def shscSkuPrice(self,url,cityCode,customerId,orderDate,instanceCode,productId,tenantCode):
        '''
        获取内销蜀海商品信息
        :return:返回商品价格
        '''
        # url = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/v3/product/price/shscSku/list'
        data = {
                "auditStatus": "1",
                "cityCode": "%s"%cityCode,
                "customerCode": "%s"%customerId,
                "isQueryExistingSupply": "0",
                "orderDate":"%s"%orderDate,
                # "orderDate": "%s"%self.orderDate,
                "productCodes": [
                    {
                        "instanceCode": "%s"%instanceCode,
                        "productCode": "%s"%productId,
                        "tenantCode": "%s"%tenantCode
                    }
                ]
            }
        print("查询基础数据价格入参为：" + json.dumps(data))
        self.printf(time_new+ "查询基础数据价格入参为：\n" + json.dumps(data))
        res = requests.post(url=url, data=json.dumps(data), headers=self.headers).text
        print("查询基础数据价格出参为：" + res)
        self.printf(time_new+ "查询基础数据价格出参为：\n" + res)
        try:
            salePrice = json.loads(res)["data"][0]["salePrice"]
            if salePrice is None:
                salePrice = "无"
            self.textBrowser_3.insertPlainText(salePrice)
        except:
            self.textBrowser_3.insertPlainText("无")

    def get_supplierSapNum(self,url,factoryCode,skuCode,tenantCode,unitCode):
        '''
        根据门店、物料编码、单位查询供应商
        :return:
        '''
        # url = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/supMaterialFacController/querySupByFacAndSku'
        data = '[{"factoryCode": "%s","skuCode": "%s","tenantCode": "%s","unitCode": "%s"}]'%(factoryCode,skuCode,tenantCode,unitCode)
        self.printf(time_new + "获取SRM供应商入参：\n" + data)
        print("获取SRM供应商入参：" + data)
        res = requests.post(url=url, data=data, headers=self.headers).text
        print("获取SRM供应商出参：" + res)
        self.printf(time_new + "获取SRM供应商出参：\n" + res)
        try:
            supplierName = json.loads(res)["data"][0]["supplierName"]
            supplierCode = json.loads(res)["data"][0]["supplierCode"]
            self.textBrowser_2.insertPlainText(supplierCode+'/'+supplierName)
            print("查询供应商信息为："+supplierCode+'/'+supplierName)
            return supplierCode
        except IndexError as e:
            self.textBrowser_2.insertPlainText("无")

    def queryPriceByFacAndSku(self,url,factoryCode,skuCode,supplierCode,unitCode,receiveDate):
        '''
        根据门店、物料编码、单位、收货日期 查询价格
        :return:
        '''
        # url ='http://172.22.226.12:8093/shsc-bizcore-product-datacenter/supMaterialFacController/queryPriceByFacAndSku'
        data = {
                "factoryCode": "%s"%factoryCode,
                "list": [
                    {
                        "skuCode": "%s"%skuCode,
                        "supplierCode": "%s"%supplierCode,
                        "unitCode": "%s"%unitCode
                    }
                ],
                "receiveDate": "%s"%receiveDate
            }
        print("获取SRM物料价格入参：" + json.dumps(data))
        self.printf(time_new + "获取SRM物料价格入参为：\n" + json.dumps(data))
        res = requests.post(url=url, data=json.dumps(data), headers=self.headers).text
        print("获取SRM物料价格出参为：" + res)
        self.printf(time_new + "获取SRM物料价格出参为：\n" + res)
        try:
            price = json.loads(res)["data"][0]["price"]
            if price is None:
                price = "无"
            self.textBrowser_3.insertPlainText(str(round(float(price), 2)))
        except:
            self.textBrowser_3.insertPlainText("无")

    def get_url(self,envir):
        if envir == 'test':
            url = 'http://172.22.226.13:8992/shsc-bizcore-customer-datacenter/customerProduct/supplylist?status=0'
            url1 = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/v3/product/price/shscSku/list'
            url2 = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/supMaterialFacController/querySupByFacAndSku'
            url3 = 'http://172.22.226.12:8093/shsc-bizcore-product-datacenter/supMaterialFacController/queryPriceByFacAndSku'
            return [url, url1, url2, url3]
        elif envir == 'uat':
            url = 'http://172.22.216.21:8992/shsc-bizcore-customer-datacenter/customerProduct/supplylist?status=0'
            url1 = 'http://172.22.216.22:8093/shsc-bizcore-product-datacenter/v3/product/price/shscSku/list'
            url2 = 'http://172.22.216.22:8093/shsc-bizcore-product-datacenter/supMaterialFacController/querySupByFacAndSku'
            url3 = 'http://172.22.216.22:8093/shsc-bizcore-product-datacenter/supMaterialFacController/queryPriceByFacAndSku'
            return [url, url1, url2, url3]
        elif envir == 'pro':
            url = 'http://172.22.197.55:8992/shsc-bizcore-customer-datacenter/customerProduct/supplylist?status=0'
            url1 = 'http://172.22.197.57:8093/shsc-bizcore-product-datacenter/v3/product/price/shscSku/list'
            url2 = 'http://172.22.197.57:8093/shsc-bizcore-product-datacenter/supMaterialFacController/querySupByFacAndSku'
            url3 = 'http://172.22.197.57:8093/shsc-bizcore-product-datacenter/supMaterialFacController/queryPriceByFacAndSku'
            return [url, url1, url2, url3]

    def clearData(self):
            # self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            # self.textBrowser.clear()
            self.textBrowser_2.clear()
            self.textBrowser_3.clear()
            self.textBrowser_4.clear()
            self.textBrowser_5.clear()
            self.textBrowser_6.clear()
            self.textBrowser_7.clear()
            self.textBrowser_8.clear()



if __name__ == '__main__':
    # 适应高DPI设备
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # 解决图片在不同分辨率显示模糊问题
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())