import pymysql
#创建数据库
# db=pymysql.connect(host='localhost',port=3306,user='root')
# cursor=db.cursor()
# cursor.execute('select version()')
# data=cursor.fetchone()
# print(data)
# cursor.execute('create database spiders default character set utf8')
# db.close()

#创建table
# db=pymysql.connect(host='localhost',port=3306,user='root',db='spiders')
# cursor=db.cursor()
# sql='create table if not exists students(id varchar(255) not null,name varchar(255) not null,' \
#     'age int not null,primary key(id))'
# cursor.execute(sql)
# db.close()

#插入数据,主键不存在便插入数据，存在则更新数据
db=pymysql.connect(host='localhost',port=3306,user='root',db='spiders')
cursor=db.cursor()
data={
    'id':'125',
    'name':'lee123',
    'age':19
}
table='students'
k=','.join(data.keys())
v=','.join(['%s']*len(data))
sql='insert into {table}({k}) values({v}) on duplicate key update'.format(table=table,k=k,v=v)
update=','.join([' {k}=%s'.format(k=key) for key in data])
sql+=update
print(sql)
try:
    if cursor.execute(sql,tuple(data.values())*2):
        print('success')
        db.commit()
except:
    print('failed')
    db.rollback()

#查询
sql = 'SELECT * FROM students WHERE age >= 20'
try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    row = cursor.fetchone()
    while row:
        print('Row:', row)
        row = cursor.fetchone()
except:
    print('Error')
db.close()