有句话叫**所有的乐趣都在部署之前**，也许这个小应用还有很多缺陷，也许它还不够完美，但是，仔细想想，其实没有什么能比自己的网站在互联网中上线更令人满足的了，但是满足的背后，总是存在着很多的风险，以至于几乎所有的开发人员都说过这样的话：“在我这里运行是正常的呀！”，所以这章，会让这个应用在实际的互联网中跑起来。

部署一个网站的大概步骤如下：

1. 注册一个域名（备案）  
2. 购买一个服务器  
3. 安装万维网服务  
4. 使用git将代码上传到服务器  
5. 使用virtualenv管理项目的python依赖  
6. 使用Gunicorn配置网站  

## 安装及配置服务器 ##
首先，我们要注册一个域名，这方面我想做开发的都应该很熟悉，在万网或新网以及各种小的代理商都可以，就不展开了。

然后，还需要一个服务器，这个选择也有很多，并且由于跑一个Python的站点需要的资源不是太多，所以，无论是阿里云，腾讯云，Amazon的AWS，微软的azure，甚至你箱子底下的一台多年不用的BT服务器都行，只要能满足以下条件：

- 可以安装Ubuntu(控制台版本即可，需要资源极少)
- 自己有Ubuntu的root权限
- 外网可访问
- 可以使用ssh控制

好吧，我推荐使用Ubuntu的原因是我只会用这个，现在这些都很简单，举个例子，但并不是广告，去阿里云官网，购买一个ecs实例，之后选择安装操作系统，可以选择Ubuntu1604版本，输入用户名密码，他就会自动安装操作系统，稍等一会，在阿里云的控制台显示"运行中"，即可使用：

![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask14/201705122245.PNG)

这时候可以使用远程的ssh工具，输入他的公网ip，以及之前输入的用户名密码， 即可连接：

![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask14/201705122249.PNG)

当出现这些内容，即表示已经使用root账户联通远程服务器，为了安全起见，可以自己配置一个非root账户，当必须使用root权限的时候，使用sudo前缀即可：

	useradd -m -s /bin/bash niufennan #添加niufennan账户
	# m 表示创建home目录，s表示默认可以使用bash（shell）
	usermod -a -G sudo niufennan #将niufennan添加至sudo用户组
	passwd niufennan #设置密码
	su - niufennan #切换到niufennan用户
![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask14/201705152311.PNG)
![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask01/201705152314.PNG)
![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask14/201705152315.PNG)


当然，其实最好的方式其实是使用私钥认证，关于这方面的内容网上也有很多，就不在展开。

## 安装Nginx ##

在安装软件之前，最好先升级一下apt-get

	sudo apt-get update

然后安装并启动Nginx

	sudo apt-get install nginx
	sudo service nginx start

经过一个安装列表 并且启动服务后，即可在浏览器中通过ip地址访问到nginx的欢迎页：

![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask14/201705152321.PNG)
Nginx可用了

接下来按照同样的步骤安装剩余所需的软件(Python git pip)

	sudo apt-get install git python3 python-pip


## 解析域名 ##

总是使用ip访问当然是不行的，所以需要对域名进行dns解析，这点不同的注册商网站的解析界面都有所不同，但是我相信四处点击几次总会找到正确的方法。

## 安装Gunicorn ##

Gunicorn是一个Python的http服务器，使用起来非常简单，安装也很方便，，直接使勇pip即可

	sudo pip install gunicorn

准备工作终于已经完成，开始上传代码

##安装MySql
在Ubuntu上安装mysql同样非常简单，只需要几个命令就可以完成：

	sudo apt-get install mysql-server 
	sudo apt-get install mysql-client
	sudo apt-get install libmysqlclient-dev
其中安装mysql-server的时候会出现让输入root密码的界面，将焦点放置到ok按钮上边，回车后输入密码即可。

然后在mysql中创建数据库：

	create database cblog default character set utf8 collate utf8_general_ci;

创建此数据库的管理用户

	http://www.cnblogs.com/janken/p/5500320.html

此用户可公网访问，root数据库则只能localhost访问

## 上传代码

>这里假设你已经拥有github账户并且熟悉简单的git操作，并且已经通过ssh公钥方式与github库关联

首先，到[github](https://github.com/)中 创建一个库，我的库名字叫**nblog** 

然后将文件push至远程库（假设本地以及提交完成）：

	git remote add nblog 远程库git地址
	git push -u nblog master 

## 虚拟环境使用
到了这里，突然发现之前的blog中，或者说开发中犯了一个严重的错误，即没有使用virtualenv，这个将导致在服务器上配置运行环境将变成了一件非常繁琐，困难，甚至变成挑战自己极限的事情，不过好在还可以不就，那么，首先在**服务端**安装virtualenv吧：

	sudo pip install virtualenv

然后自己的环境，只能不考虑其他，先打一个比较臃肿的包（全环境）

	pip freeze > requirements.txt

这里会将本机所有的库记录，到服务器端可以直接复原，若有virtualenv，则会只记录虚拟环境下的库，将非常的方便，下面看一下记录中的内容：

![](http://ojzct6bcl.bkt.clouddn.com/cblog/pflask14/201705172241.PNG)

可以看到，虽然没有细看，但至少画红线的部分是本项目肯定没有用到的，可以手动删除。

将此文件添加至git库中并推送到远程库

	git add requirements.txt
	git commit -m "增加迁移文件"
	
	git push -u nblog master

然后通过ssh链接到服务器，到用户的home文件夹，创建nblog文件夹

	mkdir nblog

然后将git远程库中的代码复制到nblog文件夹中

	git clone https://github.com/niufennan/nblog.git nblog/nblog.niufennan.com/source
	

>注意，Linux下，目录层级关系必须使用/

创建虚拟环境(此时在nblog.niufennan.com文件夹下)

	sudo virtualenv  --python=python3 ../virtualenv

>前一个为命令，后一个为目录名

>virtualenv的使用方式有两种，一种是执行activete进行环境切换，一种是直接指定virtualenv文件夹下的python和/或pip，一般来讲开发时可以切换，服务器直接指定路径即可

在虚拟环境中安装项目所用的库：

	sudo ../virtualenv/bin/pip3.5 install -r source/requirements.txt

这样，就会将原本在开发机上记录在requirements.txt上所有的库都安装在virtualenv的site-packages文件夹中
	
## 配置环境变量

这时候先别着急运行，别忘了有些值是配置在环境变量中的，主要有三个：

	access_key=os.environ.get("qn_access_key")
	secret_key=os.environ.get("qn_secret_key")

	SQLALCHEMY_DATABASE_URI=os.environ.get("nblog_mysql_str") 
	
>其中七牛的都是公共的，以后即使有其他的应用，这两个依然不会变，sql链接字符串则是项目私有的，所有使用nblog前缀。

vi /etc/profile







  