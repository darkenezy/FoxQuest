import threading, json
import utils


def create_manager(settings="settings.json"):
    with open(settings, "r") as o:
        settings = json.load(o)

    return Manager(settings["quests"], settings)


def kill_done_chats(func):
    def wrapper(*args, **kws):
        result = func(*args, **kws)

        self, chat_id, *others = args

        if chat_id in self.chats and self.chats[chat_id].done:
            del self.chats[chat_id]

        return result

    return wrapper

class Manager:
    def __init__(self, quests=None, settings={}):
        if not quests:
            raise ValueError("Нет квестов!")

        self.settings = settings
        self.quests = {q.name: q for q in [Quest(i) for i in quests]}
        self.chats = {}

    def get_quest(self, chat):
        if chat is None:
            return None

        if chat.quest in self.quests:
            return self.quests[chat.quest]

        chat.done = True

        return None

    def get_chat(self, chat_id):
        return self.chats.get(chat_id)

    def create_chat(self, chat_id):
        current = self.chats.get(chat_id)

        if current is None or current.done:
            return [("text", "Пришлите название квета из списка:\n" + "\n".join(self.quests.keys()))]

        return [("text", "Вы уже играете! Напишите /reset, чтобы перестать играть.")]

    def reset_chat(self, chat_id):
        current = self.chats.get(chat_id)

        if current is None or current.done:
            return [("text", "Вы не играете! Напишите /start, чтобы начать игру.")]

        del self.chats[chat_id]

        return [("text", "Ваша игра отменена. Напишите /start, чтобы начать игру.")]

    def check_game_start(self, chat_id, message):
        current = self.chats.get(chat_id)

        if current is None or current.done:
            for q in self.quests.keys():
                if q.strip().lower() == message.strip().lower():
                    self.chats[chat_id] = Chat(chat_id, q)

                    return True

            return "Напишите /start, чтобы начать игру."

        return False

    def process_message(self, chat_id, text):
        state = self.check_game_start(chat_id, text)

        if isinstance(state, str):
            return [("text", state)]

        if state is True:
            return self.do_step(chat_id)

        if state is False:
            return self.update_step(chat_id, text=text)

    @kill_done_chats
    def do_step(self, chat_id, success=None):
        chat = self.get_chat(chat_id)
        quest = self.get_quest(chat)

        if chat is None or quest is None:
            return [("text", "Произошла ошибка! Попробуйте ещё раз.")]

        return quest.do_step(chat, success)

    @kill_done_chats
    def update_step(self, chat_id, text=None, location=None):
        chat = self.get_chat(chat_id)
        quest = self.get_quest(chat)

        if chat is None or quest is None:
            return [("text", "Произошла ошибка! Попробуйте ещё раз.")]

        return quest.update_step(chat, text=text, location=location)


class Chat:
    __slots__ = ("chat_id", "quest", "step", "done", "data")

    def __init__(self, chat_id, quest):
        self.chat_id = chat_id
        self.quest = quest

        self.done = False
        self.data = ""
        self.step = 0

class Quest:
    def __init__(self, quest_file):
        with open(quest_file, encoding="utf-8") as f:
            whole = json.load(f)

        self.quest = whole["quest"]
        self.name = whole["name"]

    def get_step(self, chat):
        if chat.step >= 0 and chat.step < len(self.quest):
            return self.quest[chat.step]

        chat.done = True

        return {}

    def check_for_goon(self, chat):
        step = self.get_step(chat)

        if not step or step["type"].startswith("wait_"):
            return False

        return True

    def parse_data(self, data):
        if data["type"] == "text":
            return [("text", data["message"])]

        elif data["type"] == "image":
            return [("image", data["url"])]

        elif data["type"] == "video":
            return [("video", data["url"])]

        elif data["type"] == "location":
            return [("location", data["location"])]

        return []

    def do_step(self, chat, success=None, first=True):
        step = self.get_step(chat)

        if not step:
            return

        tosend = None

        if step["type"] in ("text", "image", "video", "location"):
            chat.step += 1
            tosend = self.parse_data(step)

        elif step["type"] in ("wait_for_location", "wait_for_text"):
            if success:
                chat.step += 1
                tosend = self.do_step(chat, first=False)

            elif "mistake" in step and first:
                return self.parse_data(step["mistake"])

        if tosend is not None:
            if self.check_for_goon(chat):
                return tosend + self.do_step(chat, first=False)

            return tosend

    def update_step(self, chat, text=None, location=None):
        step = self.get_step(chat)

        if not step or (not text and not location):
            return

        if location and step["type"] == "wait_for_location":
            if "location" not in step:
                return self.do_step(chat, True)

            if utils.distance(step["location"]["lat"], step["location"]["long"], *location) < step.get("distance", 15):
                return self.do_step(chat, True)

        if text and step["type"] == "wait_for_text":
            if "text" not in step:
                return self.do_step(chat, True)

            if step.get("strict", False):
                if text == step["text"]:
                    return self.do_step(chat, True)
            else:
                if text.lower().strip() == step["text"].lower().strip():
                    return self.do_step(chat, True)

        return self.do_step(chat, False)
