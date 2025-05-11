import re
from typing import Dict, Any

import nonebot
from nonebot import require, on_regex, on_message, on_notice
from nonebot.params import RegexDict
from nonebot.permission import SUPERUSER
from nonebot.drivers.websockets import logger
from nonebot.plugin import PluginMetadata, get_plugin_config

require("nonebot_plugin_alconna")
require("nonebot_plugin_uninfo")

from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_uninfo import Uninfo, QryItrface, SupportAdapterModule, ADMIN, GROUP

from .config import Config
from .record import SceneManager, SceneRecord

__plugin_name__ = "今日老婆"

__plugin_usage__ = (
    "指令表：\n"
    "[今日老婆] 随机抽取群友作为老婆\n"
    "[换老婆] 重新抽取老婆\n"
    "[今日老婆信息] 查看本群今日老婆信息\n"
    "[开启 | 关闭换老婆] 开启/关闭本群换老婆功能[仅管理]\n"
    "[设置换老婆次数 <N>] 自定义本群换老婆最大次数[仅管理]\n"
    "[开启 | 关闭自动撤回] 开启/关闭本群自动撤回[仅管理]\n"
    "[设置自动撤回延迟 <N>] 设置本群自动撤回延迟[仅管理]\n"
    "[开启 | 关闭自动设置对方老婆] 抽到的老婆如果还没有老婆时，自动给对方设置老婆[仅管理]\n"
    "[设置抽取模式 <随机模式/活跃模式>] 设置本群抽取模式[仅管理]\n"
    "[设置活跃天数 <N>] 设置本群活跃天数[仅管理]\n"
    "[刷新 | 重置今日老婆] 刷新本群记录[仅超管]"
)

__plugin_meta__ = PluginMetadata(
    name=__plugin_name__,
    description="随机抽取群友作为老婆吧！",
    usage=__plugin_usage__,
    type="library",
    config=Config,
    homepage="https://github.com/glamorgan9826/nonebot-plugin-today-waifu",
    supported_adapters=set(SupportAdapterModule.__members__.values()),
)

driver = nonebot.get_driver()
plugin_config = get_plugin_config(Config)

if plugin_config.today_waifu_superuser_opt:
    permission_opt = SUPERUSER
else:
    permission_opt = SUPERUSER | ADMIN()

# 正则匹配插件名与别名的字符串
PatternStr = '|'.join([__plugin_name__, ] + plugin_config.today_waifu_aliases)

# 响应器主体
today_waifu = on_regex(
    pattern=rf'^\s*({PatternStr})\s*$',
    flags=re.S,
    permission=GROUP | SUPERUSER,
    priority=7,
    block=True,
)

# 刷新所在群全部记录
today_waifu_refresh = on_regex(
    rf"^\s*(刷新|重置)(?P<name>{PatternStr})\s*$",
    permission=SUPERUSER,
    priority=7,
    block=True
)

# 换老婆
today_waifu_change = on_regex(
    pattern=r'^\s*换老婆\s*$',
    flags=re.S,
    permission=GROUP | SUPERUSER,
    priority=7,
    block=True,
)

# 设置所在群换老婆最大次数
today_waifu_set_limit_times = on_regex(
    pattern=rf"^\s*设置换老婆次数\s*(?P<times>\d+)\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_set_allow_change = on_regex(
    pattern=rf"^\s*(?P<val>开启换老婆|关闭换老婆)\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_set_withdraw_delay = on_regex(
    pattern=rf"^\s*设置自动撤回延迟\s*(?P<times>\d+)\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_set_auto_withdraw = on_regex(
    pattern=rf"^\s*(?P<val>开启自动撤回|关闭自动撤回)\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_set_auto_set_other_half = on_regex(
    pattern=rf"^\s*(?P<val>开启自动设置对方老婆|关闭自动设置对方老婆)\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_set_select_mode = on_regex(
    pattern=rf"^\s*设置抽取模式\s*(?P<val>.+)$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_set_active_days = on_regex(
    pattern=rf"^\s*设置活跃天数\s*(?P<times>\d+)\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_info = on_regex(
    pattern=rf"^\s*({PatternStr})信息\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)

today_waifu_active_member = on_message(
    permission=GROUP,
    priority=1,
    block=False,
)

today_waifu_usage = on_regex(
    pattern=rf"^\s*({PatternStr})帮助\s*$",
    permission=permission_opt,
    priority=7,
    block=True,
)


@driver.on_startup
async def init() -> None:
    SceneManager().load()


if plugin_config.today_waifu_group_member_cache:
    logger.warning("今日老婆缓存已开启，注意：当前仅支持OneBot V11协议，其余协议请关闭today_waifu_group_member_cache选项")

    from typing import Union
    from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
    from nonebot.adapters.onebot.v11.permission import GROUP

    group_member_handle = on_notice()


    @group_member_handle.handle()
    async def _(session: Uninfo, interface: QryItrface,
                event: Union[GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent]):
        scene_record: SceneRecord = SceneManager().get_scene(session.scene)  # 获取场景记录
        if isinstance(event, GroupIncreaseNoticeEvent):
            await scene_record.add_member(session.user.id, session, interface)
        elif isinstance(event, GroupDecreaseNoticeEvent):
            await scene_record.remove_member(session.user.id, session, interface)
        await group_member_handle.finish()


@today_waifu_active_member.handle()
async def _(session: Uninfo):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)  # 获取场景记录
    scene_record.log_speak_record(session.user.id)  # 记录群友发言
    await today_waifu_active_member.finish()


@today_waifu_info.handle()
async def _(session: Uninfo):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    await today_waifu_info.finish(scene_record.get_info())


@today_waifu_set_withdraw_delay.handle()
async def _(session: Uninfo, times: Dict[str, Any] = RegexDict()):
    delay: str = times.get("times", str(plugin_config.today_waifu_auto_withdraw_delay)).strip()
    try:
        delay_num = max(1, int(delay))
    except ValueError:
        await today_waifu_set_withdraw_delay.finish("延迟时间应为整数")
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    scene_record.set_auto_withdraw_delay(delay_num)
    await today_waifu_set_withdraw_delay.finish(f"已将本群自动撤回延迟设置为{delay_num}秒")


@today_waifu_set_active_days.handle()
async def _(session: Uninfo, times: Dict[str, Any] = RegexDict()):
    active_days: str = times.get("times", str(plugin_config.today_waifu_active_days)).strip()
    try:
        active_days_num = int(active_days)
    except ValueError:
        await today_waifu_set_active_days.finish("活跃天数应为整数")
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    scene_record.set_active_days(active_days_num)
    await today_waifu_set_active_days.finish(f"已将本群活跃天数设置为{active_days_num}天")


@today_waifu_set_select_mode.handle()
async def _(session: Uninfo, val: Dict[str, Any] = RegexDict()):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    val: str = val.get("val", "").strip()
    if "随机" in val:
        val = "随机模式"
        scene_record.set_select_mode("random")
    elif "活跃" in val:
        val = "随机模式"
        scene_record.set_select_mode("active")
    await today_waifu_set_select_mode.finish(f"本群设置为{val}模式")


@today_waifu_set_allow_change.handle()
async def _(session: Uninfo, val: Dict[str, Any] = RegexDict()):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    val: str = val.get("val", "").strip()
    if val == "开启换老婆":
        scene_record.set_allow_change_waifu(True)
    elif val == "关闭换老婆":
        scene_record.set_allow_change_waifu(False)
    else:
        await today_waifu_set_allow_change.finish()
    await today_waifu_set_allow_change.finish(f"本群设置为{val}")


@today_waifu_set_auto_withdraw.handle()
async def _(session: Uninfo, val: Dict[str, Any] = RegexDict()):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    val: str = val.get("val", "").strip()
    if val == "开启自动撤回":
        scene_record.set_auto_withdraw(True)
    elif val == "关闭自动撤回":
        scene_record.set_auto_withdraw(False)
    else:
        await today_waifu_set_auto_withdraw.finish()
    await today_waifu_set_auto_withdraw.finish(f"本群设置为{val}")


@today_waifu_set_auto_set_other_half.handle()
async def _(session: Uninfo, val: Dict[str, Any] = RegexDict()):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    val: str = val.get("val", "").strip()
    if val == "开启自动设置对方老婆":
        scene_record.set_auto_set_other_half(True)
    elif val == "关闭自动设置对方老婆":
        scene_record.set_auto_set_other_half(False)
    else:
        await today_waifu_set_auto_set_other_half.finish()
    await today_waifu_set_auto_set_other_half.finish(f"本群设置为{val}")


@today_waifu_set_limit_times.handle()
async def _(session: Uninfo, times: Dict[str, Any] = RegexDict()):
    limit_times: str = times.get("times", str(plugin_config.today_waifu_default_limit_times)).strip()
    try:
        limit_times_num = int(limit_times)
    except ValueError:
        await today_waifu_set_limit_times.finish("换老婆次数应为整数")
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    scene_record.set_limit_times(limit_times_num)
    await today_waifu_set_limit_times.finish(f"已将本群换老婆次数设置为{limit_times_num}次")


@today_waifu_change.handle()
async def _(session: Uninfo, interface: QryItrface):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    msg: UniMessage = await scene_record.change_waifu(session, interface)
    receipt = await msg.send(at_sender=True, reply_to=True)
    if scene_record.auto_withdraw:
        await receipt.recall(delay=max(1, scene_record.auto_withdraw_delay))


@today_waifu.handle()
async def _(session: Uninfo, interface: QryItrface):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    msg: UniMessage = await scene_record.get_waifu(session, interface)
    receipt = await msg.send(at_sender=True, reply_to=True)
    if scene_record.auto_withdraw:
        await receipt.recall(delay=max(1, scene_record.auto_withdraw_delay))


@today_waifu_refresh.handle()
async def _(session: Uninfo, name: Dict[str, Any] = RegexDict()):
    scene_record: SceneRecord = SceneManager().get_scene(session.scene)
    plugin_name: str = name.get("name", __plugin_name__).strip()
    scene_record.clear_record()
    await today_waifu_refresh.finish(f"{plugin_name}已刷新！")
