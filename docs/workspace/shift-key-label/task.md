# Keys Shift 标识优化

档位：轻量；仅既有按钮标签/辅助说明，不改变按键协议或布局。
授权原话：“这个项目还需要加个优化，keys 里面需要加上shift 键”。源码已有 Shift modifier（⇧），本卡保留已有实现并把入口明确为 Shift。
目标仓库：/home/nash/work/herdr-remote；任务分支 fix/shift-key-label；本地交付主干 main；不向第三方上游 push/创建 PR。
范围：web/index.html 的既有 modShift 按钮；本任务记录及截图验证材料。
验收：手机 Keys 按钮显示 Shift，不溢出；Shift→Tab→Send 仍组成 shift+Tab，验证仅拦截浏览器发送，不操作真实 agent。
步骤：只改标签和辅助说明；运行相关既有测试；真实 Chrome 核手机布局与组合键；检查源树无并行修改，再把已验证提交合入本地运行版本。
环境：已有 Python venv、Chrome、Node，测试无需安装依赖。当前源树 clean，live 页面每次读取 index.html，不需重启服务。
状态：候选验证通过，待本地合入与运行页面回读。网址公网响应正常，但未验证用户手机关闭梯子后的网络可达性。

验证：11 项既有 web assets 测试通过；真实 Chrome 在 360/390 宽度无横向溢出、Shift 文字未裁切；Shift→Tab→Send 捕获 shift+Tab。发送边界为 fake sendKeys，无真实 Agent 输入。截图 keys-360.png/keys-390.png，结构证据 browser-verification.json。
