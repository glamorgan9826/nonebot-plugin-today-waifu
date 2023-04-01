<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-today-waifu

_✨ 随机抽取群友作为老婆吧！ ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/glamorgan9826/nonebot-plugin-today-waifu.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-today-waifu">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-today-waifu.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

一个能每天随机抓取群友作为老婆的插件

每天会重置记录（根据本地时间判断）

已经是别人老婆的成员就不会再成为别人的老婆了哦 【NTR禁止】

如果剩余成员列表为空则默认机器人本身为老婆

#### \>>换老婆功能

如果对抽到的老婆不满意可以换老婆  
可以指定换老婆次数上限，超过次数上限的话就没老婆了哦~
该功能可以开启或关闭

#### \>>分群记录信息

每个群单独记录，包括老婆记录以及换老婆次数（不包括禁止作为老婆的id列表，那个是全局的）

#### \>>可以禁止某些id被抽到

全局生效，主要是为了防止Q群管家之类的机器人被抽到

#### \>>支持自定义插件别名

可以使用自定义名称触发抽取老婆的指令

#### \>>重置群记录信息

可以手动重置该群当天老婆及换老婆记录

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-today-waifu

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-today-waifu

</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-today-waifu

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-today-waifu

</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-today-waifu

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_today_waifu"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置，实际上可以都不填写

|               配置项                | 必填  | 类型        |                 默认值                 |                   说明                   |
|:--------------------------------:|:---:|-----------|:-----------------------------------:|:--------------------------------------:|
|     TODAY_WAIFU_BAN_ID_LIST      |  否  | List[int] |                 []                  |              列表内的id不会被抽到               |
| TODAY_WAIFU_DEFAULT_CHANGE_WAIFU |  否  | bool      |                true                 |            是否默认开启换老婆功能，默认开启            |
| TODAY_WAIFU_DEFAULT_LIMIT_TIMES  |  否  | int       |                  3                  |                允许换老婆次数                 |
|       TODAY_WAIFU_ALIASES        |  否  | List[str] |              ["每日老婆"]               | 今日老婆插件的别名，允许设置多个，即除了"今日老婆"外，也可以用别名触发指令 |
|      TODAY_WAIFU_RECORD_DIR      |  否  | str       | "nonebot_plugin_today_waifu/record" |       记录保存路径，默认在插件目录下新建record文件夹       |

    # today-waifu 配置样例
    TODAY_WAIFU_BAN_ID_LIST = [2854196310,123456]
    TODAY_WAIFU_DEFAULT_CHANGE_WAIFU = true
    TODAY_WAIFU_DEFAULT_LIMIT_TIMES = 3
    TODAY_WAIFU_ALIASES = ["每日老婆","我的老婆"]
    # TODAY_WAIFU_RECORD_DIR= "" 一般不需要填写，如果需要请填写绝对路径

## 🎉 使用

### 指令表

|            指令            | 权限  | 需要@ | 范围  |                说明                |
|:------------------------:|:---:|:---:|:---:|:--------------------------------:|
|        今日老婆/自定义别名        | 群员  |  否  | 群聊  | 随机抽取群友作为老婆，返回头像和昵称。当天已经抽取过回复相同老婆 |
|           换老婆            | 群员  |  否  | 群聊  |              重新抽取老婆              |
| (刷新/重置)今日老婆/(刷新/重置)自定义别名 | 主人  |  否  | 群聊  |            清空今日本群老婆数据            |
|        (开启/关闭)换老婆        | 主人  |  否  | 群聊  |           开启/关闭本群换老婆功能           |
|         设置换老婆次数n         | 主人  |  否  | 群聊  |         设置本群换老婆最大次数，n为整数         |

### 效果图

暂无

## ✨其他

- [Nonebot](https://github.com/nonebot/nonebot2): 本项目的基础，非常好用的聊天机器人框架。
- [dailywife](https://github.com/SonderXiaoming/dailywife): 本项目的灵感及思路来源。
- [petpet](https://github.com/noneplugin/nonebot-plugin-petpet): 本项目获取群友头像的功能代码来源。