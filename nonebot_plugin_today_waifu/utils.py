import datetime
from functools import wraps
from typing import Callable, Set

from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_uninfo import Uninfo, Interface


async def get_scene_members(session: Uninfo, interface: Interface) -> Set[str]:
    """
    获取群成员列表
    :param session:
    :param interface:
    :return:
    """
    members = await interface.get_members(session.scene.type, session.scene.id)
    return set(i.id for i in members)


async def construct_message(session: Uninfo, interface: Interface, message: str, waifu_id: str = None) -> UniMessage:
    if waifu_id is None:
        return UniMessage.text(message)
    if not isinstance(interface, Interface):
        return UniMessage.text(f"[用户({waifu_id})信息获取失败]" + message)
    try:
        waifu = await interface.get_member(session.scene.type, session.scene.id, waifu_id)
    except Exception:
        waifu = None
    if not waifu:
        return UniMessage.text(f"[用户({waifu_id})信息获取失败]" + message)
    if not waifu.user.avatar:
        return UniMessage.text(f"[头像({waifu_id})获取失败]" + message)
    avatar = UniMessage.image(url=waifu.user.avatar)
    msg = UniMessage.text(message) + avatar
    if waifu_id != session.self_id:
        member_name = waifu.nick or waifu.user.nick or waifu.user.name or waifu.user.id or waifu_id
        msg = msg + UniMessage.text(f"{member_name}({waifu_id})")
    return msg


def auto_save(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.save()
        return result

    return wrapper


def get_today() -> str:
    return str(datetime.date.today())


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
