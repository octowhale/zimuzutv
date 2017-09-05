# zimuzutv
字幕组爬虫

## 项目介绍

爬虫练手项目，每小时爬去 [字幕组tv](http://www.zimuzu.tv/today) 当日更新的内容。
点击剧名后，可以查看该剧的所有资源信息。

## 软件要求

+ python >= 3.6.1
+ mongodb >= 3.4.7
+ redis >= 2.4

### python 库

+ beautifulsoup4==4.6.0
+ bs4==0.0.1
+ Flask==0.12.2
+ Jinja2==2.9.6
+ lxml==3.8.0
+ pymongo==3.5.1
+ requests==2.18.4
+ redis==2.10.5

可以通过 `pip install -r requirements` 安装


## 配置

在 setting 目录下，将所有模板文件保存为同名 json 文件。填入基本信息即可



## 启动

```bash
python3 main.py

# 或

/bin/bash main.sh

```

## TODO LIST

### 改问题

- [ ] 由于字段过长写入 mongodb 失败后，会重新进入 queue 队列的死循环。
- [ ] 修改现在mongodb 的短连接为长连接


### 新功能

- [ ] 增加 flask log
- [ ] 增加 flask flush



### 重构

- [ ] 将数据写入 reids 与 mongodb
- [ ] 查询时，先查询 reids，再查询 mongodb， 在查询 字幕组.tv
- [ ] 重新设计下载链接数据库，mongodb 有最大字符串长度限制。比如[《权利游戏》](http://www.zimuzu.tv/resource/10733) 下载地址就报表了。


## License

GUN General Public License v3.0



