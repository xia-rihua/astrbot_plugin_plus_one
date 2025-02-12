from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event.filter import event_message_type, EventMessageType

@register("astrbot_plugin_plus_one", "DUAAAA", "群聊相同文本消息自动+1的插件", "1.0.0", "https://github.com/xia-rihua/astrbot_plugin_plus_one")
class RepeatSamePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.last_message_state = {}  # 记录每个群的最后一条消息状态

    def update_state(self, group_id, text, triggered=False):
        """更新群聊状态信息"""
        self.last_message_state[group_id] = {"text": text, "triggered": triggered}

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        if event.get_sender_id() == event.message_obj.self_id:
            return  # 避免处理机器人自己发送的消息

        group_id = event.message_obj.group_id
        current_text = event.message_str.strip()
        if not current_text:
            return  # 忽略空消息

        last_state = self.last_message_state.get(group_id, {"text": None, "triggered": False})

        if last_state["text"] == current_text:
            if not last_state["triggered"]:
                yield event.plain_result(current_text)
                self.update_state(group_id, current_text, triggered=True)
        else:
            self.update_state(group_id, current_text)
