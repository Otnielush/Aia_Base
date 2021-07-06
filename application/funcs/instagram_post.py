from instabot import Bot
from ..database.config import Config_instagram

config = Config_instagram()

class Instagram():
    def __init__(self):
        self.bot = Bot()
        self.online_status = False
        self.login()

    def login(self):
        self.online_status = self.bot.login(username = config.user_name, password=config.password)

    def post_image(self, img, txt):
        if not self.online_status:
            self.login()
            if not self.online_status:
                print('Instagram login failed')
                return

        self.bot.upload_photo()

