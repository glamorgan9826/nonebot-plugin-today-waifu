from pathlib import Path
from typing import List, Set

from pydantic import BaseModel, Field


class Config(BaseModel):
    # 全局配置
    today_waifu_ban_id_list: Set[str] = Field(default_factory=set)
    today_waifu_aliases: List[str] = Field(default_factory=list)
    today_waifu_record_dir: Path = Path(__file__).parent / "record_v2"
    today_waifu_superuser_opt: bool = False
    today_waifu_group_member_cache: bool = False

    # 群组配置（默认）
    today_waifu_default_change_waifu: bool = True
    today_waifu_default_limit_times: int = 2
    today_waifu_auto_withdraw: bool = False
    today_waifu_auto_withdraw_delay: int = 5
    today_waifu_auto_set_other_half: bool = False
    today_waifu_select_mode: str = "random"
    today_waifu_active_days: int = 3
