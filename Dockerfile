MAINTAINER nikozhang
FROM python:3.7

#代码添加到code文件夹
ADD ./* /data/chengyuspider
WORKDIR /data/chengyuspider

# 设置时区
RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

# 安装依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
&& pip install -r requirements.txt

# 运行
CMD ['scrapy', 'crawl', 'chengyu']