# Fork 与 H5 开发环境准备

档位：轻量。纯仓库/环境准备及文档，无新产品规则或登录边界改动。
授权：用户原话“fork一份，本地切换到对应仓库目录继续开发的话，应该怎么做，继续”。飞书应用状态：“还没新建呢”。
目标：把已部署版本移入用户 fork 的开发分支，独立开发环境可复跑 H5 基线。
仓库：nashhu180-netizen/herdr-remote；开发目录 /home/nash/work/herdr-remote-feishu；分支 feat/feishu-h5；目标主干 fork/main。此次只 push 开发分支，不向 main/master push；不创建 tag/发布，不切换运行服务。
验收：GitHub fork 父仓库是 dcolinmorgan/herdr-remote；origin 为用户 fork，upstream 为原项目；开发分支包含 Shift 两个本地提交；web/ 字节与已部署版本完全一致；独立 venv 可跑 H5 相关已有测试；远端开发分支 SHA 与本地一致。
范围：docs/FORK_DEVELOPMENT.md、本任务记录、草案副本及脱敏基线证据；不修改当前 web/ 或 Relay 行为。
步骤：核 remotes/代码来源与 release 触发；创建独立 venv，复用既有依赖缓存；跑 H5 基线、记录字节一致；保存用户 fork 的分支；回读状态。
环境：uv/Python 3.12/Node/Chrome 已可用；原部署依赖清单可复用。现有 release workflow 仅 tag v* 或手动触发，普通分支 push 不触发发布。
测试环境补齐：首次 207 项测试执行中，24 项通过、183 项因缺 Playwright 跳过。仅在独立开发 venv 增加 Playwright 1.63.0（已有浏览器测试需要），复用系统 Chrome；保留开发依赖快照。首次补齐后的运行受工具服务器重启中断，未形成结果，恢复后重新执行。
验证：207 项网页测试通过，0 跳过/失败/错误；20 个网页文件与运行目录一致；11 个 JavaScript 文件通过 node --check，Relay Python 通过语法解析，26 个开发环境依赖通过 uv pip check。运行目录仍保持 clean。
状态：本地 Fork 开发环境准备完成，交付时回读远端开发分支 SHA；H5 布局保持当前版本。飞书 App 尚待新建，真实接入与免登未完成，不宣称 H5 飞书适配已完成。
