# AI News Daily · 每日 AI 新闻边角料短视频自动化流水线

> **Automated daily AI news briefing video generator.** 一套可复用的「每日资讯播报短视频」生产流水线：自动搜集全球 AI 热点 → 按热度筛选 → 撰写口播稿 → 生成铅笔速写插画 → 分段配音 → 合成竖屏短视频，产出可直接用于抖音 / 视频号 / 小红书 / YouTube Shorts 的 9:16 内容。

**Keywords:** AI news daily, automated news briefing, daily short video generator, content automation pipeline, vertical video 9:16, Python, Pillow, ffmpeg, text-to-speech, pencil sketch illustration, social media content creation, scheduled cron workflow.

## ✨ Features / 特性

- **每日热点聚合**：按周报、社区热度、产品发布、融资商业、研究突破、监管政策六个维度检索，多源交叉验证后按热度排序取前 5 条。
- **固定栏目模板**：开场 + 5 条播报 + 结尾的卡片流结构，每条必带一句争议 / 风险提示，避免单向吹捧。
- **手绘视觉风格**：黑白铅笔速写新闻插画 + 米白纸底 + 衬线标题，竖屏 1080×1920、30fps；卡片文字由模板后期叠字，保证清晰可控。
- **分段配音**：开场 / 5 条 / 结尾共 7 段独立音频，按音频实测时长对齐卡片，支持单段重配而不重跑全片。
- **可复用、可换主题**：栏目名、领域、条数、画幅、音色、插画风格、口播口吻都收敛在 `config.json` 与规则手册中，改配置即可迁移到财经、科技、游戏等其他日更栏目。
- **产出质检清单**：语音内容（数字、专有名词、漏条、争议口径）与画面逐项复核，错误只重配对应段。

## 📋 Pipeline / 工作流程

```text
搜集热点 (6 维度检索)
   ↓
热度筛选 + 去重 + 保留原文链接
   ↓
撰写口播稿 / 卡片摘要 (script.md)
   ↓
生成铅笔速写插画 (assets/news1~5.jpg)
   ↓
分段 TTS 配音 (assets/intro, n1~n5, outro.wav)
   ↓
build_cards.py  →  7 张竖屏卡片 PNG
   ↓
build_video.sh  →  ffmpeg 分段 + concat 合成成片
   ↓
质检复核 (语音内容 + 画面 + 来源)  →  交付人工终审发布
```

## 🚀 Quick Start / 快速开始

### 依赖

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/)（合成与音频探测）
- 图像依赖：`Pillow`
- 配音与插画由对应生成工具产出（本仓库内置卡片模板与合成脚本）

### 安装

```bash
git clone https://github.com/okeya24/ai-news-daily-video.git
cd ai-news-daily-video
pip install -r requirements.txt
```

### 生成卡片

```bash
python3 build_cards.py
```

### 合成成片

```bash
bash build_video.sh
# 输出：output/ai-news-briefing_YYYY-MM-DD.mp4
```

> `assets/` 下的配音与插画、`output/` 下的卡片与成片均为运行时生成产物，已在 `.gitignore` 中排除，不进入版本库。

## 📁 Structure / 目录结构

```text
ai-news-daily-video/
├── README.md              # 项目说明（本文件）
├── config.json            # 可改变量：栏目名、领域、条数、画幅、音色、口吻、质检项
├── requirements.txt        # Python 依赖
├── build_cards.py         # PIL 卡片模板生成（片头 + 5 条 + 结尾）
├── build_video.sh         # ffmpeg 分段 + concat 合成脚本
├── docs/
│   └── AGENT_RULES.md     # 完整规则手册：选题、口径、视觉、配音、合成、质检、复用指南
├── examples/
│   └── script-sample.md   # 当日口播稿 + 卡片摘要 + 新闻来源示例
├── assets/                 # 运行时素材（wav / jpg，不入库）
└── output/                 # 运行时产物（cards / seg / mp4，不入库）
```

## ⚙️ Configuration / 配置

`config.json` 集中管理可复用变量：

| 字段 | 说明 |
|---|---|
| `channel_name` | 栏目名（如「AI 新闻边角料」） |
| `domain` | 内容领域关键词（如 全球 AI） |
| `items_per_day` | 每日条数 |
| `resolution` / `fps` | 画幅分辨率与帧率 |
| `voice` | 音色、语速、口吻描述 |
| `opening_template` / `closing_template` | 开场、结尾话术模板 |
| `quality_check` | 产出质检清单 |
| `publish` | 发布方式（默认人工终审后手动发布） |

## 🧩 Customize / 换到其他主题

把同一套流程迁移到每日财经、科技、游戏等栏目时，只需改动：

1. `config.json` 中的栏目名、领域、条数；
2. 检索维度关键词（见 `docs/AGENT_RULES.md` 第 4 节）；
3. 出图 prompt 中的插画场景；
4. 配音 prompt 中的音色与口吻。

卡片模板、合成脚本、质检清单均可原样复用。完整对照表与步骤见 [docs/AGENT_RULES.md](docs/AGENT_RULES.md)。

## 📌 Notes / 说明与限制

- 当前版本为**静态卡片流**；旁白逐句跟随字幕条、背景音乐、动态镜头 / 数字人属于后续可扩展项。
- 成片默认交付人工终审后手动发布；未接入任何自媒体平台的自动发布通道。
- 新闻需保留可溯源原文链接，不把预测或传闻写成既定事实。
- 本仓库未指定开源许可证；二次使用前请确认素材、字体与配音的授权合规。

## 📄 Sample / 示例稿件

见 [examples/script-sample.md](examples/script-sample.md)，包含开场、5 条播报、卡片摘要与来源链接的成稿样例。
