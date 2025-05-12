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
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

### 注意！！！0.1.6版本进行了重构以适配nonebot2新版本，pydantic升级到v2（v0.1.9已兼容 pydantic v1），存在破坏性改动：
### 将不兼容历史的记录，所有群配置需要重新设置；
### python版本从3.8升级到3.9，和nonebot2保持同步，虽然本插件仍采用了兼容3.8的写法，但不保证能正常运行。

一个能每天随机抓取群友作为老婆的插件

每天会重置记录（根据本地时间判断）

已经是别人老婆的成员就不会再成为别人的老婆了哦 【NTR禁止】

如果剩余成员列表为空则默认机器人本身为老婆

适配多平台，依赖[nonebot_plugin_alconna](https://github.com/nonebot/plugin-alconna)、
[nonebot_plugin_uninfo](https://github.com/RF-Tar-Railt/nonebot-plugin-uninfo)，具体参考对应插件文档。【0.1.6版本新增】

#### \>>换老婆功能

如果对抽到的老婆不满意可以换老婆  
可以指定换老婆次数上限，超过次数上限的话就没老婆了哦~
该功能可以开启或关闭

#### \>>支持不同抽取模式【0.1.6版本新增】

目前支持两种模式：

- 随机模式：随机抽取一个人作为老婆，随机模式作为默认模式，可以在配置中修改为活跃模式或者在群里使用命令修改
- 活跃模式：优先从最近n天发言过的群友中抽取，n可自定义，默认为3天。可以解决大群总是抽到死人的情况（如果剩余活跃成员少于5则进行随机选择）

#### \>>支持定时自动撤回功能【0.1.6版本新增】

可以设置n秒后自动撤回刚刚发送的老婆信息，防止刷屏，默认关闭，n可自定义，

#### \>>支持自动设置对方老婆功能【0.1.6版本新增】

可以配置抽到老婆，是否自动给对方的老婆设置为自己（前提是对方当前没有老婆，并且即使给对方设置，对方也可也继续换老婆）<br/>
默认关闭，可以在配置文件中开启或者在群里使用命令开启

#### \>>分群记录信息

每个群单独记录，包括老婆记录以及换老婆次数（不包括禁止作为老婆的id列表，那个是全局的）<br/>
并且支持命令实时查看【0.1.6版本新增】

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

在 nonebot2 项目的`.env`文件中添加下表中的配置，实际上**都可以不填写**

### 全局配置项：

|              配置项               | 必填 | 类型        |  默认值  |                    说明                    |
|:------------------------------:|:--:|-----------|:-----:|:----------------------------------------:|
|    TODAY_WAIFU_BAN_ID_LIST     | 否  | List[int] |  []   |               列表内的id不会被抽到                |
|      TODAY_WAIFU_ALIASES       | 否  | List[str] |  []   |  今日老婆插件的别名，允许设置多个即除了"今日老婆"外，也可以用别名触发指令   |
|     TODAY_WAIFU_RECORD_DIR     | 否  | str       |       |      记录保存路径，默认在插件目录下新建record_v2文件夹       |
|   TODAY_WAIFU_SUPERUSER_OPT    | 否  | bool      | false |               是否仅主人可设置换老婆                |
| TODAY_WAIFU_GROUP_MEMBER_CACHE | 否  | bool      | false | 是否缓存群成员信息，默认关闭，当前仅支持OneBot V11协议，其余协议请关闭 |

### 群组配置项（默认）：

|               配置项                | 必填 | 类型   |  默认值   |                                说明                                |
|:--------------------------------:|:--:|------|:------:|:----------------------------------------------------------------:|
| TODAY_WAIFU_DEFAULT_CHANGE_WAIFU | 否  | bool |  true  |                         是否默认开启换老婆功能，默认开启                         |
| TODAY_WAIFU_DEFAULT_LIMIT_TIMES  | 否  | int  |   2    |                             允许换老婆次数                              |
|    TODAY_WAIFU_AUTO_WITHDRAW     | 否  | bool | false  |                         是否开启自动撤回功能，默认关闭                          |
| TODAY_WAIFU_AUTO_WITHDRAW_DELAY  | 否  | int  |   5    |                        自动撤回延迟时间，单位为秒，默认5秒                        |
| TODAY_WAIFU_AUTO_SET_OTHER_HALF  | 否  | bool | false  | 如果抽到老婆，是否自动给对方设置<br/>（前提是对方当前没有老婆，并且即使给对方设置，对方也可也继续换老婆）<br/>默认关闭 |
|     TODAY_WAIFU_SELECT_MODE      | 否  | str  | random |       抽取模式，random为随机模式，随机抽取<br/>active为活跃模式，优先选择最近x天发言过的用户       |
|     TODAY_WAIFU_ACTIVE_DAYS      | 否  | int  |   3    |                     活跃天数，默认3天，当选择active模式时生效                     |

    # today-waifu 配置样例

    TODAY_WAIFU_BAN_ID_LIST = [2854196310,123456]
    TODAY_WAIFU_ALIASES = ["每日老婆","我的老婆"]
    # TODAY_WAIFU_RECORD_DIR= "" # 一般不需要填写，如果需要请填写绝对路径
    TODAY_WAIFU_SUPERUSER_OPT = false
    # TODAY_WAIFU_GROUP_MEMBER_CACHE = false  # 注意：当前仅支持OneBot V11协议，其余协议请关闭

    TODAY_WAIFU_DEFAULT_CHANGE_WAIFU = true
    TODAY_WAIFU_DEFAULT_LIMIT_TIMES = 2
    TODAY_WAIFU_AUTO_WITHDRAW = false
    TODAY_WAIFU_AUTO_WITHDRAW_DELAY = 5
    TODAY_WAIFU_AUTO_SET_OTHER_HALF = false
    TODAY_WAIFU_SELECT_MODE = "active"
    TODAY_WAIFU_ACTIVE_DAYS = 3

## 🎉 使用

### 指令表

|        指令         |    权限     | 需要@ | 范围 |                    说明                    |
|:-----------------:|:---------:|:---:|:--:|:----------------------------------------:|
|      今日老婆帮助       |    群员     |  否  | 群聊 |              显示今日老婆插件的帮助信息               |
|      今日老婆信息       |    群员     |  否  | 群聊 |              显示当前插件在本群的配置信息              |
|       今日老婆        |    群员     |  否  | 群聊 |     随机抽取群友作为老婆，返回头像和昵称。当天已经抽取过回复相同老婆     |
|        换老婆        |    群员     |  否  | 群聊 |                  重新抽取老婆                  |
|    (刷新/重置)今日老婆    |    主人     |  否  | 群聊 |                清空今日本群老婆数据                |
|    (开启/关闭)换老婆     | 主人/群主/管理员 |  否  | 群聊 |               开启/关闭本群换老婆功能               |
|     设置换老婆次数n      | 主人/群主/管理员 |  否  | 群聊 |           设置本群换老婆最大次数，n为整数，默认2           |
|    (开启/关闭)自动撤回    | 主人/群主/管理员 |  否  | 群聊 |       开启/关闭本群换老婆功能后，是否自动撤回原消息，默认关闭       |
|     设置自动撤回延迟n     | 主人/群主/管理员 |  否  | 群聊 |        设置本群自动撤回延迟，单位为秒，n为整数，默认5秒         |
|  (开启/关闭)自动设置对方老婆  | 主人/群主/管理员 |  否  | 群聊 |      开启/关闭本群换老婆功能后，是否自动给对方设置老婆，默认关闭      |
| 设置抽取模式(随机模式/活跃模式) | 主人/群主/管理员 |  否  | 群聊 | 设置本群抽取老婆模式，随机模式为随机选择，活跃模式为优先选择最近x天发言过的用户 |
|      设置活跃天数n      | 主人/群主/管理员 |  否  | 群聊 |           设置本群活跃模式下的活跃天数，n为整数            |

### 效果图

暂无

## ✨其他

- [Nonebot](https://github.com/nonebot/nonebot2): 本项目的基础，非常好用的聊天机器人框架。
- [dailywife](https://github.com/SonderXiaoming/dailywife): 本项目的灵感及思路来源。
- [petpet](https://github.com/noneplugin/nonebot-plugin-petpet): 本项目获取群友头像的功能代码来源。
- [nonebot_plugin_alconna](https://github.com/nonebot/plugin-alconna): 本项目的多平台适配依赖插件。
- [nonebot_plugin_uninfo](https://github.com/RF-Tar-Railt/nonebot-plugin-uninfo): 本项目多平台的会话信息获取依赖插件。

## 📋版本历史

- 0.1.0 初始版本
- 0.1.1 更新metadata及修复一些bug
- 0.1.2 修复每次关闭换老婆状态无法保存bug
- 0.1.3 修改换老婆次数以及是否开启指令允许群主管理员执行。如果想保持原状仅允许主人执行换老婆相关执行则在配置文件中增加项
  `TODAY_WAIFU_SUPERUSER_OPT = true`
- 0.1.4 指定换老婆次数命令与次数间可以存在空格
- 0.1.5 修改TODAY_WAIFU_BAN_ID_LIST的验证条件以适应py3.8以下版本
- 0.1.6 <br/>
  (1) 重构代码以适配nonebot2新版本，注意该版本有破坏性改动，将不兼容历史的记录，所有群配置需要重新设置。<br/>
  (2) [nonebot_plugin_alconna](https://github.com/nonebot/plugin-alconna)、
  [nonebot_plugin_uninfo](https://github.com/RF-Tar-Railt/nonebot-plugin-uninfo)，适配多平台，具体参考对应插件文档。<br/>
  (3) 增加撤回功能、自动设置对方老婆功能、设置抽取模式功能、今日老婆信息等功能。<br/>
  (4) python版本从3.8升级到3.9，和nonebot2保持同步，虽然本插件仍采用了兼容3.8的写法，但不保证正常运行。
- 0.1.7 更新PluginMetadata信息
- 0.1.8 修复bug
- 0.1.9 兼容pydantic v1
        