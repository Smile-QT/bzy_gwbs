## 部署

- 安装依赖包

   ```
   pip install -r requirement.txt
   ```

- 安装 uwsgi

  > 配置文件 uwsgi.ini

- 安装 nginx

  > 配置文件 GWWeb\nginx.conf

- 数据库

   ```
   'NAME': 'cc_gwbs',
   'USER': 'root',
   'PASSWORD': '090301',
   'HOST': '127.0.0.1',
   ```

## 运行

python manage.py runserver 0.0.0.0:80

## TODO

> 1. Docker 运行
> 2. docker-compose.yml
> 