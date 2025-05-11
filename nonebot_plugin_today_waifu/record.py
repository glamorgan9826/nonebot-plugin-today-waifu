import json
import random
from pathlib import Path
from typing import Literal, Set, Dict

from pydantic import BaseModel, Field

from nonebot import get_plugin_config, logger
from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_uninfo import Uninfo, SceneType, Scene, Interface

from .config import Config
from .utils import get_today, singleton, auto_save, construct_message, get_scene_members

plugin_config = get_plugin_config(Config)
BAN_ID: Set[str] = plugin_config.today_waifu_ban_id_list
TODAY_WAIFU_GROUP_MEMBER_CACHE: bool = plugin_config.today_waifu_group_member_cache

RANDOM = "random"
ACTIVE = "active"


class SceneMemberRecord(BaseModel):
    members: Set[str] = Field(default_factory=set)


class ActiveRecord(BaseModel):
    # 活跃天数
    active_days: int = plugin_config.today_waifu_active_days
    # 活跃天数记录 用户id:离上次发言时间的天数
    active_record: Dict[str, int] = Field(default_factory=dict)
    # 今日发言用户id记录
    today_speak_record: Set[str] = Field(default_factory=set)

    def log_speak_record(self, user_id: str) -> bool:
        if user_id in self.today_speak_record:
            return False
        self.today_speak_record.add(user_id)
        return True

    def update_active_record(self):
        for uid in self.today_speak_record:
            self.active_record[uid] = self.active_days
        self.today_speak_record.clear()
        # 更新活跃用户记录，并移除超过配置中active_days活跃天数未发言的用户
        for uid in tuple(self.active_record.keys()):
            if self.active_record[uid] < 1:
                self.active_record.pop(uid)
            else:
                self.active_record[uid] -= 1

    def set_active_days(self, days: int):
        self.active_days = days


class SceneRecord(BaseModel):
    id: str
    type: SceneType
    today: str = Field(default_factory=get_today)
    member_cache: SceneMemberRecord = Field(default_factory=SceneMemberRecord, exclude=True)

    select_mode: Literal["random", "active"] = plugin_config.today_waifu_select_mode
    # 是否允许换老婆
    allow_change_waifu: bool = plugin_config.today_waifu_default_change_waifu
    # 换老婆次数
    limit_times: int = plugin_config.today_waifu_default_limit_times
    # 自动撤回
    auto_withdraw: bool = plugin_config.today_waifu_auto_withdraw
    # 自动撤回延迟
    auto_withdraw_delay: int = plugin_config.today_waifu_auto_withdraw_delay
    # 自动设置另一半
    auto_set_other_half: bool = plugin_config.today_waifu_auto_set_other_half

    # 抽到老婆的记录
    waifu_record: Dict[str, str] = Field(default_factory=dict)
    # 换老婆次数 用户id:换老婆次数
    waifu_change_record: Dict[str, int] = Field(default_factory=dict)
    active_record: ActiveRecord = Field(default_factory=ActiveRecord)

    @property
    def file_path(self) -> Path:
        return plugin_config.today_waifu_record_dir / f"scene_{self.id}" / f"record.json"

    def get_info(self) -> str:
        return (
            f"号码：{self.id}\n"
            f"场景：{self.type.name}\n"
            f"抽取模式：{'随机模式' if self.select_mode == RANDOM else '活跃模式'}\n"
            f"允许换老婆：{self.allow_change_waifu}\n"
            f"换老婆次数：{self.limit_times}\n"
            f"自动撤回：{self.auto_withdraw}\n"
            f"自动撤回延迟：{self.auto_withdraw_delay}\n"
            f"自动设置对方老婆：{self.auto_set_other_half}\n"
            f"活跃天数：{self.active_record.active_days}\n"
        )

    def save(self):
        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as f:
            f.write(self.model_dump_json())

    async def add_member(self, user_id: str, session: Uninfo, interface: Interface):
        if not self.member_cache.members:
            self.member_cache.members = await get_scene_members(session, interface)
            return
        self.member_cache.members.add(user_id)

    async def remove_member(self, user_id: str, session: Uninfo, interface: Interface):
        if not self.member_cache.members:
            self.member_cache.members = await get_scene_members(session, interface)
            return
        self.member_cache.members.discard(user_id)

    @auto_save
    def set_select_mode(self, mode: Literal["random", "active"]):
        self.select_mode = mode

    @auto_save
    def set_allow_change_waifu(self, allow: bool):
        self.allow_change_waifu = allow

    @auto_save
    def set_limit_times(self, times: int):
        self.limit_times = times

    @auto_save
    def set_auto_withdraw(self, enable: bool):
        self.auto_withdraw = enable

    @auto_save
    def set_auto_withdraw_delay(self, delay: int):
        self.auto_withdraw_delay = delay

    @auto_save
    def set_auto_set_other_half(self, enable: bool):
        self.auto_set_other_half = enable

    @auto_save
    def set_auto_set_other_half(self, enable: bool):
        self.auto_set_other_half = enable

    @auto_save
    def set_active_days(self, days: int):
        self.active_record.set_active_days(days)

    def log_speak_record(self, user_id: str):
        if self.active_record.log_speak_record(user_id):
            self.save()

    @auto_save
    def update_active_record(self):
        self.active_record.update_active_record()

    @auto_save
    def clear_record(self):
        self.waifu_record.clear()
        self.waifu_change_record.clear()

    def _today_check(self):
        """
        日期检测
        如果日期未变更，则直接返回
        否则切换日期，并更新相关记录
        :return:
        """
        today = get_today()
        if today == self.today:
            return
        self.today = today
        self.waifu_record.clear()
        self.waifu_change_record.clear()

    def _check_change_waifu_list(self, user_id: str) -> bool:
        """
        检查用户换老婆次数是否超过限制
        :param user_id:
        :return:
        """
        return self.allow_change_waifu and self.waifu_change_record.setdefault(user_id, 0) > self.limit_times + 1

    async def get_group_member(self, session: Uninfo, interface: Interface) -> Set[str]:
        if TODAY_WAIFU_GROUP_MEMBER_CACHE:
            if not self.member_cache.members:
                self.member_cache.members = await get_scene_members(session, interface)
            return self.member_cache.members
        if self.member_cache.members:
            self.member_cache.members.clear()
        return await get_scene_members(session, interface)

    async def select_random(self, user_id: str, session: Uninfo, interface: Interface) -> str:
        group_member_list = await self.get_group_member(session, interface)
        id_set = group_member_list - set(self.waifu_record.values()) - BAN_ID
        id_set.discard(user_id)
        if id_set:
            return random.choice(list(id_set))
        # 如果剩余群员列表为空，默认机器人作为老婆
        return session.self_id

    async def select_active(self, user_id: str, session: Uninfo, interface: Interface) -> str:
        id_set = set(self.active_record.keys()) - set(self.waifu_record.values()) - BAN_ID
        id_set.discard(user_id)
        if len(id_set) >= 5:
            return random.choice(list(id_set))
        return await self.select_random(user_id, session, interface)

    async def select_step(self, user_id: str, session: Uninfo, interface: Interface) -> str:
        """
        根据不同的选择模式抽取老婆
        :param user_id:
        :param session:
        :return:
        """
        if self.select_mode == RANDOM:
            return await self.select_random(user_id, session, interface)
        elif self.select_mode == ACTIVE:
            return await self.select_active(user_id, session, interface)
        raise Exception(f"not support select mode '{self.select_mode}'")

    def relation_step(self, user_id: str, waifu_id: str, ):
        self.waifu_record[user_id] = waifu_id
        self.waifu_change_record[user_id] = self.waifu_change_record.get(user_id, 0) + 1
        # 自动设置另一半(仅在对方没有抽取过waifu的情况下)
        if self.auto_set_other_half and self.waifu_change_record.get(user_id, 0) < 1:
            self.waifu_record[waifu_id] = user_id

    @auto_save
    async def change_waifu(self, session: Uninfo, interface: Interface) -> UniMessage:
        self._today_check()
        user = session.user
        # 不允许换老婆的情况
        if not self.allow_change_waifu:
            return await construct_message(session, interface, "\n请专一的对待自己的老婆哦")
        # 今天没抽老婆直接换老婆的情况
        if user.id not in self.waifu_record:
            return await construct_message(session, interface, "\n换老婆前请先娶个老婆哦，渣男")
        # 超出换老婆次数/机器人是老婆还换老婆的情况
        if (self.waifu_change_record.get(user.id, 0) > self.limit_times
                or self.waifu_record.get(user.id) == session.self_id):
            self.waifu_change_record[user.id] = self.waifu_change_record.get(user.id, 0) + 1
            return await construct_message(session, interface, "\n渣男，你今天没老婆了！")
        waifu_id: str = await self.select_step(user.id, session, interface)
        self.relation_step(user.id, waifu_id)
        # 最后一次换老婆的情况
        if self.waifu_change_record.get(user.id, 0) > self.limit_times:
            return await construct_message(
                session,
                interface,
                "\n渣男，再换你今天就没老婆了！\n你今天的群友老婆是我哦~" if waifu_id == session.self_id
                else "\n渣男，再换你今天就没老婆了！\n你今天的群友老婆是：",
                waifu_id,
            )
        return await construct_message(
            session,
            interface,
            "\n你今天的群友老婆是我哦~\n如果你这个渣男敢抛弃我的话，你今天就没老婆了哦" if waifu_id == session.self_id
            else "\n你今天的群友老婆是：",
            waifu_id,
        )

    @auto_save
    async def get_waifu(self, session: Uninfo, interface: Interface) -> UniMessage:
        self._today_check()
        user = session.user
        # 换老婆超过次数限制
        if self.allow_change_waifu and self._check_change_waifu_list(user.id):
            return await construct_message(session, interface, "\n渣男，你今天没老婆了！")
        # 如果已经抽过老婆，则直接返回对应的老婆
        if user.id in self.waifu_record:
            return await construct_message(
                session,
                interface,
                "\n你今天已经有老婆了，是我哦，不可以再有别人了呢~" if self.waifu_record[user.id] == session.self_id
                else "\n你今天已经有老婆了，要好好对待她哦~",
                self.waifu_record[user.id],
            )
        waifu_id: str = await self.select_step(user.id, session, interface)
        self.relation_step(user.id, waifu_id)
        return await construct_message(
            session,
            interface,
            "\n你今天的群友老婆是我哦~" if waifu_id == session.self_id else "\n你今天的群友老婆是：",
            waifu_id,
        )


@singleton
class SceneManager:
    scenes: Dict[str, SceneRecord] = {}

    def get_scene(self, scene: Scene) -> SceneRecord:
        return self.scenes.setdefault(scene.id, SceneRecord(id=scene.id, type=scene.type))

    def load(self):
        for dir_path in plugin_config.today_waifu_record_dir.glob("*"):
            dir_path: Path
            if not dir_path.is_dir():
                continue
            try:
                record_file: Path = dir_path.joinpath("record.json")
                if not record_file.is_file():
                    continue
                with open(record_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    scene = SceneRecord.model_validate(data)
                    self.scenes[scene.id] = scene
            except json.JSONDecodeError:
                logger.warning(f"Today Waifu: Failed to load scene record from {dir_path}")
