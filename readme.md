# Checkin

GitHub Actions 实现 [GLaDOS][glados] 自动签到

([GLaDOS][glados] 可用邀请码: `1TJAU-JLPBN-NLSWV-5QTUF`, 双方都有奖励天数)
1. 直接注册GLaDOS(注册地址在 https://github.com/glados-network/GLaDOS 实时更新)

成功后输入邀请码:1TJAU-JLPBN-NLSWV-5QTUF 激活

2. 通过 https://glados.space/landing/1TJAU-JLPBN-NLSWV-5QTUF 注册, 自动填写激活

3. 通过 https://1tjau-jlpbn-nlswv-5qtuf.glados.space , 自动填写激活


## 使用说明

1. Fork 这个仓库

1. 登录 [GLaDOS][glados] 获取 Cookie

1. 添加 Cookie 到 Secret `GLADOS`

1. 启用 Actions, 每天北京时间 00:10 自动签到

1. 如需推送通知, 可用 [PushPlus][pushplus], 添加 Token 到 Secret `NOTIFY`

[glados]: https://github.com/glados-network/GLaDOS
[pushplus]: https://www.pushplus.plus/
