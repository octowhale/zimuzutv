# Changelog

> 2017-09-05

+ `core/ZimuzuCrawler.py` 中增加 `self.q` 优先级队列。 **today** 节目单中抓取失败的内容放入队尾等待。
+ mongodb 中查询，要使用字符串查询 `db.detail.find({'m_id':'32342'})`

> 2017-09-01

`core/ZimuzuCrawler.py` 中增加 `threading.BoundedSemaphore(1)` 信号量，控制节目详单的并发，避免被 zimuzu.tv 给屏蔽。

