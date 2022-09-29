# @Author : yan1079
# @Time : 2022/9/8 10:04
import pymysql


def convert_n_bytes(n, b):
    bits = b * 8
    return (n + 2 ** (bits - 1)) % 2 ** bits - 2 ** (bits - 1)

def convert_4_bytes(n):
    return convert_n_bytes(n, 4)

def hashCode(str):
    h = 0
    n = len(str)
    for i, c in enumerate(str):
        h = h + ord(c) * 31 ** (n - 1 - i)
    return convert_4_bytes(h)

def get_hashcode(code,envir):
    if envir=='test':
        num=35
    elif envir=='uat':
        num=35
    elif envir == 'pro':
        num=50
    js_str = hashCode(code)
    if '0N5' in code or '0W5'in code or '0N3'in code:
        result = num-js_str % num
        if result ==num:
            return 0
        else:
            return result
    else:
        result = js_str % num
        if result == num:
            return 0
        else:
            return result

class GetInstanceCode:
    # def __init__(self, customer_code, source_code):
    #     self.customer_code = customer_code
    #     self.source_code = source_code
    #     self.num = get_hashcode(customer_code)

    def get_data(self,sql,envir):

        db = self.get_envir(envir)
        cursor = db.cursor()
        cursor.execute(sql)
        goods_data = cursor.fetchone()
        db.close()
        return goods_data

    def get_envir(self,envir):
        if envir=='test':
            return pymysql.connect(host='172.22.227.134', port=8066, user='root', password='shuhaisc.com', db='athena_db')
        elif envir=='uat':
            return pymysql.connect(host='172.22.216.107', port=8066, user='root', password='root', db='athena_db')
        elif envir=='pro':
            return pymysql.connect(host='172.22.197.176', port=8066, user='read_user', password='PdkWslSkl540ZIcB7_j', db='athena_db')


if __name__ == '__main__':
    num = get_hashcode('0N50001196','uat')
    sql = f"SELECT customer_code,source_code,tenant_code,instance_code,supply_tenant_code,supply_instance_code,unit_code FROM t_customer_product_rel_{num} WHERE customer_code = '0N50001196' AND source_code ='4006298011'"
    gc = GetInstanceCode()
    print(gc.get_data(sql,'uat'))


