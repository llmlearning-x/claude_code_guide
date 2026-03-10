import argparse
import os
from pathlib import Path

import requests
from openai import OpenAI


ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
MODEL_NAME = "doubao-seedream-5-0-260128"


IMAGE_SPECS = {
    "preface-city-skyline": {
        "prompt": "黄昏城市天际线，远景，高楼灯光刚刚亮起，略带未来感但真实写实风格，暖色调，无文字，适合作为技术书前言封面背景。",
        "filename": "preface-city-skyline.png",
    },
    "cc-intro-cover-pro": {
        "prompt": (
            "中文计算机技术书籍封面海报设计，纵向 2K 分辨率，风格参考京东上常见的大模型/AI 技术书。"
            "画面左侧为竖向主色块，印有大标题“Claude Code 工程实践”和副标题“小字：从 Agent 到 Skill 与 MCP 的系统指南”，"
            "右下角排版作者署名“小字：晓云 著”；"
            "画面右侧为抽象的几何图形、代码方块和流程线条，表现 Claude Code 连接代码库、Skill 与 MCP 的概念，"
            "整体色调以青绿色和深蓝为主，搭配少量金色或橙色强调色，构图简洁、有留白，具有专业技术书的质感。"
        ),
        "filename": "cc-intro-cover-pro.png",
        "width": 1664,
        "height": 2432,  # 2:3 竖版
    },
    "preface-cover": {
        "prompt": "俯瞰一个巨大而精密复杂的机械迷宫或钟表内部结构，象征现代软件工程的复杂性。在混沌的机械结构中心，有一束明亮的光或一条清晰的路径正在显现，穿透迷雾。整体色调偏冷峻、严肃，具有宏大的工业感和神秘感，高分辨率，写实风格。",
        "filename": "preface-cover.png",
    },
    "cc-intro-cover": {
        "prompt": "夜晚的现代化办公室，一位开发者专注地坐在多屏工位前。屏幕上显示着代码编辑器和与 Claude 的聊天界面。屏幕发出柔和的蓝紫色光芒照亮开发者的脸庞。画面中隐约可见发光的数据流或神经元连接线条，连接着开发者的大脑与屏幕，象征人机协作与思维共振。赛博朋克轻科技风，但基于现实，高清晰度，电影质感。",
        "filename": "cc-intro-cover.png",
    },
    "cc-modes-cover": {
        "prompt": "一个充满未来感的全息控制面板或仪表盘，上面有四个明显的通过发光图标区分的功能区：Ask（问号/气泡）、Plan（指南针/地图）、Agent（机械臂/齿轮）、Debug（放大镜/虫子）。仪表盘采用玻璃拟态设计，精致通透。背景是模糊的数字工作空间。科技感强，UI设计风格。",
        "filename": "cc-modes-cover.png",
    },
    "cc-workflow-cover": {
        "prompt": "3D 等轴测视角的流水线可视化。左侧是杂乱的便签和草图（需求）进入一台流线型的未来机器（Claude Code）；机器内部可见代码语法和逻辑门构成的精密齿轮在转动；右侧输出整齐、发光的几何方块（交付的软件），并自动部署到云端结构中。风格极简、专业、工程化，白色或浅灰背景。",
        "filename": "cc-workflow-cover.png",
    },
    "cc-prompts-cover": {
        "prompt": "一张数字蓝图或制图桌的特写。桌面上，“Prompt”被描绘成模块化的、可互锁的拼图块或积木。积木上标记着“Context”、“Instruction”、“Output”等技术术语。一只发光的手（AI）和一只真人的手正在共同拼装这些积木，构建一个复杂的结构。建筑蓝图风格，蓝白线条，精确、结构化。",
        "filename": "cc-prompts-cover.png",
    },
    "skill-intro-cover": {
        "prompt": "清晨雾气缭绕的山谷中，一间温馨的木屋旁有一个井井有条的工具棚。工具棚的墙上挂满了各种未来派工具，它们融合了传统工具（锤子、扳手）的形态和发光的数字科技元素。氛围宁静、充满创造力，象征“数字工匠精神”。",
        "filename": "skill-intro-cover.png",
    },
    "skill-patterns-cover": {
        "prompt": "软件设计模式的抽象可视化。各种几何体（球体、立方体、金字塔）在虚空中组成优雅、对称的重复结构和阵列。细线连接着这些形状，展示它们之间的逻辑关系。数学可视化风格，数据艺术，冷色调（青、蓝、银），强调秩序与和谐。",
        "filename": "skill-patterns-cover.png",
    },
    "skill-team-cover": {
        "prompt": "一个繁忙的未来指挥中心或数字图书馆。一个多元化的团队围绕着中央巨大的发光光柱或全息知识树。人们从这个中央库中获取“技能球”（发光的球体）并带回自己的工位使用。场景强调共享、协作和中心化资源。暖色调照明，社区氛围。",
        "filename": "skill-team-cover.png",
    },
    "mcp-intro-cover": {
        "prompt": "一座宏伟、坚固的桥梁连接着两个截然不同的世界。左侧是纯粹的数字代码世界（0和1，矩阵风格），右侧是真实的物理世界（服务器、文档、地球仪）。发光的数据包顺滑地在桥梁上双向流动。桥梁本身充满高科技感，由光纤和能量束构成。主题：连接、融合。",
        "filename": "mcp-intro-cover.png",
    },
    "mcp-server-cover": {
        "prompt": "一个极简的白色工作台。台上放着一个刚刚启动的小型机器人或装置（代表第一个 MCP Server），它正发出友好的绿色光芒，并向空中投射出“Hello World”的全息字符。背景干净无杂物，聚焦于这个新生的创造物。主题：诞生、简洁、开始。",
        "filename": "mcp-server-cover.png",
    },
    "mcp-deep-cover": {
        "prompt": "潜入深海数据中心。无尽延伸的服务器机柜如同海底峡谷。抽象的潜水员（数字探索者）正在深处探索，采集发光的数据晶体。场景深邃、神秘，信息密度高，由数据本身的光芒照亮。主题：深度、企业级规模。",
        "filename": "mcp-deep-cover.png",
    },
    "mcp-security-cover": {
        "prompt": "一个高科技的六边形能量护盾或保险库大门，正在保护核心系统。护盾发出蓝光，坚不可摧。护盾外，红色的火花（威胁）被弹开。护盾内，数据井然有序地运行。画面突出一把发光的数字锁或盾牌徽章。主题：安全、防御、可靠。",
        "filename": "mcp-security-cover.png",
    },
    "practices-web-app-cover": {
        "prompt": "现代响应式 Web 应用的展示图。画面中心是笔记本电脑、平板和手机，屏幕上都显示着同一个精美的“图书追踪”应用界面，布局自适应。设备旁放着一杯咖啡和一本实体笔记本。背景明亮、通透，展现现代 Web 开发的高效与优雅。",
        "filename": "practices-web-app-cover.png",
    },
    "practices-backend-ops-cover": {
        "prompt": "服务器集群或云基础设施的抽象图。无数个节点通过高速移动的光束（API 请求）连接。视角为等轴测或俯视。一个控制塔或仪表盘正在监控流量。强调速度、效率和庞大的基础设施网络。",
        "filename": "practices-backend-ops-cover.png",
    },
    "practices-legacy-cover": {
        "prompt": "蜕变与重生。一台巨大的、生锈的蒸汽朋克风格旧机器，正在被转化为流线型的未来赛博机械。纳米机器人或光束正在进行改造工作，一半是旧齿轮，一半是新金属。主题：重构、进化、现代化。",
        "filename": "practices-legacy-cover.png",
    },
    "practices-team-adoption-cover": {
        "prompt": "一群职业人士（工程师、经理、设计师）在一个现代化的开放式办公区围成一圈，注视着中央全息投影展示的项目成功图表。大家面带微笑，正在交流。背景明亮，充满活力。主题：团队合作、成功、以人为本。",
        "filename": "practices-team-adoption-cover.png",
    },
    "practices-overview-cover": {
        "prompt": "一张巨大的战役地图或战略规划图铺在桌面上。地图上标记着不同的领地（Web、后端、遗留系统、团队）。几枚棋子或标记物放置在关键位置。光线聚焦在地图上，象征从理论到实践的全局视野。",
        "filename": "practices-overview-cover.png",
    },
    "appendix-prompt-cover": {
        "prompt": "一个整洁的档案室或药房。抽屉或格子上贴着“Prompts”标签。一个目录卡片或平板电脑显示着模板列表。光线温暖，充满书卷气。主题：索引、查阅、知识库。",
        "filename": "appendix-prompt-cover.png",
    },
    "appendix-code-cover": {
        "prompt": "文件目录树的 3D 可视化。文件夹和文件表现为发光的树状节点结构。根系深扎，枝繁叶茂。节点之间有清晰的层级关系。主题：结构、组织、逻辑。",
        "filename": "appendix-code-cover.png",
    },
    "appendix-glossary-cover": {
        "prompt": "一本打开的魔法书或全息百科全书，发光的定义和概念从页面上浮现出来。背景中有艺术化的字母表。主题：定义、清晰、语言。",
        "filename": "appendix-glossary-cover.png",
    },
    "appendix-faq-cover": {
        "prompt": "一个亲切的咨询台或信息站。一个巨大的问号标志发着光。一个机器人助手递出一把发光的钥匙（解决方案）。主题：帮助、解答、支持。",
        "filename": "appendix-faq-cover.png",
    },
}


def download_to_file(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    out_path.write_bytes(resp.content)


def generate_images(image_names: list[str], force: bool = False) -> None:
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise RuntimeError("环境变量 ARK_API_KEY 未设置，无法调用豆包图像模型。")

    client = OpenAI(base_url=ARK_BASE_URL, api_key=api_key)

    project_root = Path(__file__).resolve().parent.parent
    images_dir = project_root / "docs" / "images"

    for name in image_names:
        spec = IMAGE_SPECS.get(name)
        if spec is None:
            print(f"[warn] 未找到名为 {name!r} 的图片配置，跳过。")
            continue

        prompt = spec["prompt"]
        filename = spec["filename"]
        out_path = images_dir / filename

        # 获取特定尺寸，如果未设置则默认生成 16:9 横版章节图
        # 注意：需要确保使用的模型支持该分辨率比例
        # Doubao-Seedream-5 要求像素数至少为 3,686,400 (约 3.7MP)
        # 16:9 比例推荐 2560x1440 (3.68MP) 或更大，这里使用 2688x1512 (约 4MP) 以确保安全
        width = spec.get("width", 2688)
        height = spec.get("height", 1512)

        if out_path.exists() and not force:
            print(f"[info] 检测到已存在图片 {out_path}，未使用 --force，本次不重复生成。")
            continue

        print(f"[info] 生成图片 {name} -> {filename} ({width}x{height})")

        resp = client.images.generate(
            model=MODEL_NAME,
            prompt=prompt,
            size=f"{width}x{height}",
            response_format="url",
            extra_body={"watermark": False},
        )

        url = resp.data[0].url

        print(f"[info] 下载 {url} 到 {out_path}")
        download_to_file(url, out_path)

    print("[info] 所选图片生成完成。")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="使用豆包 Seedream 模型批量为本书生成插图，并保存到 docs/images/。"
    )
    parser.add_argument(
        "--names",
        nargs="*",
        help=f"要生成的图片名称，可选值：{', '.join(IMAGE_SPECS.keys())}。",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="生成配置中的所有图片（配合默认的跳过已存在逻辑，可用于批量补全）。",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="如已存在同名图片，是否强制重新生成并覆盖。",
    )
    args = parser.parse_args()

    if args.all:
        names = list(IMAGE_SPECS.keys())
    elif args.names:
        names = args.names
    else:
        # 默认只生成专业封面图
        names = ["cc-intro-cover-pro"]

    generate_images(names, force=args.force)


if __name__ == "__main__":
    main()
