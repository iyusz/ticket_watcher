# ticket_watcher
bilibili会员购票数监控


```
#首先安装依赖
pip3 install requests
#然后启动即可
python3 bilibili_ticket_watcher.py

```


写本软件是为了监控miYoSummer 2nd的可售时间，其他会员购项目修改project id后应该也可以使用，已大幅降低请求时间，频繁请求会造成服务器压力过大。

使用邮箱作为通知工具，需获取对应邮箱的授权码 注意修改31-35行

78行为判断是否有票的条件，不同项目应该需要修改
