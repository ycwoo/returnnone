# RETURNNONE
### 介绍
这是我在学习python时候的一个练手项目，那时GFW完全屏蔽了Google，之前修改hosts的方法也无法奏效，为了方便没有梯子的用户访问Google就有了做这个项目的想法。</br>
RETURNNONE可以实现以下功能：</br>
* 抓取Google的搜索结果</br>
实现很简单，就是用requests获取关键词的搜索结果，然后用beautifulsoup解析再用正则表达式提取出关键信息。
* 抓取知乎的搜索结果</br>
和上面一样的套路，只不过这次是用的搜狗的接口，而不是在知乎的原站抓取。
* 前端呈现</br>
用Flask+Jinja2模板将以上搜索结果呈现出来。
## 部署
以ubuntu为例：
* 下载源码<br>
```shell
git clone https://github.com/ycwoo/returnnone
cd returnnone
```
* 安装依赖<br>
```shell
sudo -H pip install -r requirements.txt
```
* 运行<br>
Flask是一个web框架，他擅长于生成html代码而不是处理和响应HTTP请求，所以我们用WSGI容器把Flask包裹起来，让其有处理HTTP请求的能力。这里我们选择Gunicorn，但是Gunicorn 默认使用同步阻塞的网络模型，对于大并发的访问表现不好，所以用gevent将其变为异步模型，运行以下命令：<br>
```shell
gunicorn -w4 -b127.0.0.1:28000 app:app -k gevent
```
* nginx<br>
Gunicorn对静态文件的支持不太好，所以生产环境下还要用Nginx作为反向代理服务器。将以下内容保存为`returnnone.conf`保存在`/etc/nginx/sites-enabled`目录下。<br>
```
server {
    listen 80;
    server_name returnnone.com www.returnnone.com;
    if ($host = 'returnnone.com'){
        rewrite ^/(.*)$ http://www.returnnone.com/$1 permanent;
    }
    location / {
        proxy_pass http://127.0.0.1:28000;
        proxy_redirect     off;
        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }
```
重启nginx<br>
```commandline
sudo nginx -s reload
```
* Enjoy it<br>
