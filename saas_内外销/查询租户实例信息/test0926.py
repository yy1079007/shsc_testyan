# @Author : yan1079
# @Time : 2022/9/26 20:39
import csv
from get_instanceCode import get_hashcode, GetInstanceCode


def search_data(shop_id, product_Id, envir):
    try:
        num = get_hashcode(shop_id, envir)
        sql1 = f'SELECT customer_code,source_code,tenant_code,instance_code,supply_tenant_code,supply_instance_code,unit_code,business_type FROM t_customer_product_rel_{num} WHERE customer_code = "%s" AND source_code ="%s"' % (shop_id, product_Id)
        grt_datas = GetInstanceCode().get_data(sql1, envir)
        if None in grt_datas:
            print(grt_datas)

    except Exception as e:
        print(str(e))


def execute_SQL(fileName):
    # 读取数据
    list_data = []
    with open(fileName +'.csv', encoding='utf-8-sig') as f:
        f_csv = csv.reader(f)
        f_csv.__next__()
        for row in f_csv:
            list_data.append(row)
    return list_data


if __name__ == '__main__':
    n=1
    for i in execute_SQL("下单模板 (5)"):
        search_data(i[0], i[1], 'pro')
        n+=1
    print(f"共查询{n}条数据")


