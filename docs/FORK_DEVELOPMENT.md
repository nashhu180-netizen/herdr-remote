# Herdr H5 fork 开发入口

## 仓库与目录

- Fork：https://github.com/nashhu180-netizen/herdr-remote
- 原项目：https://github.com/dcolinmorgan/herdr-remote
- 开发目录：`/home/nash/work/herdr-remote-feishu`
- 当前开发分支：`feat/feishu-h5`
- 原运行目录：`/home/nash/work/herdr-remote`，当前服务仍从这里运行；开发代码不会自动上线。
- `origin` 用于本人的 fork；`upstream` 用于原项目同步。原项目 AGPL 许可证保留。

进入开发目录：

```bash
cd /home/nash/work/herdr-remote-feishu
git switch feat/feishu-h5
git status
```

本分支基于实际部署提交 `dd1f49346cb377491a9fee25acaaea9d30254632`，包含既有 Shift 标签改动与部署验证记录。当前 `web/` 与运行版本保持一致。

## 已确认方向

用户要求“完全搬运当前网页版的布局”。现有应用已经是 HTML/CSS/JS H5/PWA，复用 `web/` 与 Python Relay，保持工作区列表、终端、历史、Keys 和确认操作。飞书作为可选访问入口，普通浏览器也能使用；飞书 SDK/身份服务不能成为所有浏览器的硬依赖。

上一版重排界面的工作台原型已被用户否决，不作为规格。本次只准备仓库，不把兼容或认证设想写成已实现功能。

## 开发环境与基线

独立 `.venv` 使用 Python 3.12 与现有 Relay 的固定依赖版本，无 live 配置/凭据。Playwright 1.63.0 仅供已有浏览器测试使用，复用本机 Chrome，不添加生产依赖。重建环境和运行 H5 基线：

```bash
uv venv --python /usr/bin/python3 .venv
uv pip install --python .venv/bin/python \
  -r docs/workspace/fork-bootstrap/development-requirements.txt
PYTHONPATH=tests HERDR_TEST_CHROME=/usr/bin/google-chrome .venv/bin/python -m unittest \
  test_web_assets test_web_pwa test_web_connection test_web_keys \
  test_web_spaces test_web_theme test_web_history test_web_selection
```

开发 Relay 应使用隔离端口、fake 数据或获准的验收 Agent，不能复制 live token/配置进仓库、不能并行启动消费者操纵 live 会话。网页截图与模拟发送不替代手机飞书实证。

本次基线：207 项网页测试全部通过，0 跳过、0 失败；20 个 `web/` 文件与运行目录逐字节一致；11 个网页 JavaScript 文件语法检查通过，Relay Python 语法及开发依赖兼容检查通过。证据见 `docs/workspace/fork-bootstrap/`。

## 飞书配置前置与下一步

用户尚未新建应用。前往 https://open.feishu.cn/app 创建企业自建应用「Herdr」，添加网页应用能力，取得 App ID。

网页入口使用现有 HTTPS 域名；配置主页并不自动提供飞书免登。现有浏览器 Cookie 不保证与飞书 WebView 共享，首次进入可能需要认证。第一版免登是否启用、与独立浏览器认证如何共存、账号范围和回调地址，需依据实际应用信息定稿后再开发。

应用密钥仅放仓库外指定私有配置，0600；不放文档、commit、测试或日志。应用发布、真实账号/Agent 验收、服务切换均按明确范围推进。

接下来：收齐 App ID，针对现有布局确认飞书内兼容/可选登录的具体交付范围，再创建对应开发任务；不实施被否决的工作台重排。
