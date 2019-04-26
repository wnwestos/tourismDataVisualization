近一段时间一直在学习运维相关的知识，并且开始接触自动化运维理念，对于很多运维工具都有自己的管理界面，但是这样分开的管理未免有点麻烦，于是自己就想着参考一下众家的成果来搭建一个可以管理多个运维工具的在线管理平台，计划是首先集成SaltStack、Cobbler，后续再继续整合其他的运维工具，第一版代码已经放到[github](https://github.com/LockeyCheng/oms-iooi)，参考了开源的一些个人项目，目前算是搭起来一个框架，欢迎感兴趣的同学们可以参与进来一起搞事情。

本管理平台的最终架构如下图：
![这里写图片描述](http://img.blog.csdn.net/20171022074849184?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**实验环境：**

	OS: Redhat 7.2 x86_64bit
	
	需要安装的软件或者模块：
	Django 1.11.6、Python 2.7.5
	Saltstack
	Salt API
	MariaDB、MySQL-python模块
	Nginx、uwsgi



	
Saltstack安装使用请参阅[自动化运维工具 Saltstack安装配置](http://blog.csdn.net/lockey23/article/details/78221454)
Salt API安装使用请参阅[ 自动化运维工具Saltstack学习笔记](http://blog.csdn.net/lockey23/article/details/78273506)
MariaDB安装使用请参阅[ MariaDB数据库的安装配置及常用操作](http://blog.csdn.net/lockey23/article/details/77103388)
nginx的编译安装以及基本配置请参阅[Nginx配置解读，虚拟主机，https配置，反向代理，https重定向](http://blog.csdn.net/Lockey23/article/details/77985470)

### 1、搭建Django开发环境（pip安装）

**首先安装pip**，本人分享的[百度盘压缩包地址](https://pan.baidu.com/s/1eSLBgDO)

	# tar -xzvf pip-1.5.4.tar.gz
	# cd pip-1.5.4
	# python setup.py install
 
 **安装Django**
 
	pip install django
![这里写图片描述](http://img.blog.csdn.net/20171022000410409?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**测试Django是否安装成功：**
![这里写图片描述](http://img.blog.csdn.net/20171022000352896?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


**对于Python（记得安装MySQL-python模块）操作数据库以下测试通过才算OK：**

	[root@lockey4 oms]# python manage.py shell
	Python 2.7.5 (default, Oct 11 2015, 17:47:16) 
	[GCC 4.8.3 20140911 (Red Hat 4.8.3-9)] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	(InteractiveConsole)
	>>> from django.db import connection
	>>> cursor = connection.cursor()
	>>> 
	
如果MySQL-python模块报错的话可以安装pymysql ，然后在项目的init文件中写入以下两句

	import pymysql 
	pymysql.install_as_MySQLdb()
###2、 创建project和app并进行基本环境测试

	# django-admin startproject oms_iooi
	# cd oms_iooi
	# django-admin startapp assets
    # django-admin startapp deploy
    # django-admin startapp oms
    # django-admin startapp userauth
    # django-admin startapp userperm
	# python manage.py runserver 0.0.0.0:8000
![这里写图片描述](http://img.blog.csdn.net/20171022002210116?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
![这里写图片描述](http://img.blog.csdn.net/20171022000952055?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**如果访问出现如下错误：**
![这里写图片描述](http://img.blog.csdn.net/20171022005805655?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

可以在setting中修改如下内容：

	ALLOWED_HOSTS = ['*']
或者根据提示将你的ip加入到第二个红线画出文件中的以下位置或者直接添加0.0.0.0：

	[root@lockey4 oms_iooi]# vim /usr/lib64/python2.7/site-packages/django/http/request.py
![这里写图片描述](http://img.blog.csdn.net/20171022010110902?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
关于各app内的代码可以直接拿本人提交到[github](https://github.com/LockeyCheng/oms-iooi)的
![这里写图片描述](http://img.blog.csdn.net/20171022002443954?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

###3. 关于Django数据库连接设置：

setting.py文件中书写格式如下：

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'saltDB',#数据库要提前建好
	        'USER': 'root',#数据库用户
	        'PASSWORD': 'redhat',#数据库密码
	        'HOST': '127.0.0.1',
	        'PORT': '3306',
	    }
	}

文件拷贝进去数据库设置好之后，执行以下命令同步数据库：



	# python manage.py makemigrations
	
	# python manage.py migrate

登录MariaDB数据库验证数据库同步成功后创建应用的超级登录用户然后重启服务
![这里写图片描述](http://img.blog.csdn.net/20171022010239392?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

	# python manage.py createsuperuser
	
![这里写图片描述](http://img.blog.csdn.net/20171022003114597?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

	# python manage.py runserver 0.0.0.0:8888
浏览器访问然后用刚才创建的用户登录
![这里写图片描述](http://img.blog.csdn.net/20171022115517001?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![这里写图片描述](http://img.blog.csdn.net/20171022115610816?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

如果是单纯的拷贝了我的文件的话执行到这一步应该是没问题的，有问题一般是因为对于Django框架的理解不够，自补

**到这里单纯的Django下OMS在线运维管理平台搭建就完成了，接下来整合NGINX**

###4、配置Nginx支持Django

**安装uwsgi**

	# pip install uwsgi

如果出现以下错误的话：

	Cleaning up...
	Command /usr/bin/python -c "import setuptools, tokenize;__file__='/tmp/pip_build_root/uwsgi/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-e_ubgI-record/install-record.txt --single-version-externally-managed --compile failed with error code 1 in /tmp/pip_build_root/uwsgi
	Storing debug log for failure in /root/.pip/pip.log

**解决思路如下：**

	wget https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz
	tar -zxvf distribute-0.6.49.tar.gz 
	cd distribute-0.6.49/
	python setup.py install
	yum install python-devel
	pip install uwsgi

![这里写图片描述](http://img.blog.csdn.net/20171022003956378?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
[root@lockey4 ~]# uwsgi --version
2.0.15
[root@lockey4 ~]# 


**接下来做一个uwsgi的可用性测试：**

建 test.py 文件，内容如下：

	def application(env, start_response):
	    start_response('200 OK', [('Content-Type','text/html')])
	    return "Hello World"
	    
然后在终端运行：

uwsgi --http :8989 --wsgi-file test.py
![这里写图片描述](http://img.blog.csdn.net/20171022004114530?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**浏览器访问出现以下结果则uwsgi 安装成功**

![这里写图片描述](http://img.blog.csdn.net/20171022004141177?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



**以下主要讲NGINX支持uwsgi配置**

Django结合了nginx之后就不需要再执行runserver来启动服务了，而且访问端口就是nginx的默认端口80，访问时都不用加的

vim /usr/local/nginx/conf/nginx.conf

	server {
	        listen       80;
	        server_name  localhost;
	        #charset koi8-r;
	        root /root/oms_iooi;
	        access_log  logs/host.access.log;
	        location / {
	            root   /root/oms_iooi;#project目录
	            include uwsgi_params;
	            uwsgi_pass 127.0.0.1:9090;
	            uwsgi_param UWSGI_CHDIR /root/oms_iooi;#project目录
	            uwsgi_param UWSGI_SCRIPT oms_iooi.wsgi;#wsgi文件位置
	        }
	location /static/ {
	        alias /root/oms_iooi/static;#静态文件
	    }
	}

**uwsgi 配置**

	uwsgi支持ini、xml等多种配置方式，本文以 ini 为例， 在/root/oms_iooi/目录下新建uwsgi.ini，添加如下配置


[root@lockey4 oms_iooi]# cat uwsgi.ini 

	[uwsgi]
	chdir=/root/oms_iooi/#project目录
	module=oms_iooi.wsgi:application
	master=True
	pidfile=/var/run/uwsgi9090.pid 
	vacuum=True
	max-requests=5000
	daemonize=/root/oms_iooi/uwsgi9090.log
	socket=0.0.0.0:9090   

启动或者重启nginx然后将uwsgi后台运行

	[root@lockey4 oms_iooi]# uwsgi --ini uwsgi.ini &
	[root@lockey4 oms_iooi]# nginx -s reload

![这里写图片描述](http://img.blog.csdn.net/20171022005625919?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

直接访问http://ip即可
![这里写图片描述](http://img.blog.csdn.net/20171022005712279?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

以上配置完成之后html页面是可以访问的，但是有可能出现静态
资源加载失败的问题，403forbidden，需要修改nginx运行用户为root：

	user root root;

如果修改了执行用户为root还是加载不了静态文件那么一般自己的静态文件路径有问题，请检查以下三个地方：

**1 、项目的setting.py文件**

	STATIC_URL='/static/'
	STATIC_ROOT='/root/oms_iooi/static'
	STATICFILES_DIRS = [
	    os.path.join(BASE_DIR, "static")
	]
**2、nginx的静态资源路径：**

	location /static/ {
	        alias /root/oms_iooi/static;
	    }
**3、页面引用（2标记出的两种引用方式都是OK的）：**

![这里写图片描述](http://img.blog.csdn.net/20171022011143843?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTG9ja2V5MjM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
