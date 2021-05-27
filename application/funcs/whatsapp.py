from twilio.rest import Client
# https://www.twilio.com/console/sms/whatsapp/sandbox

from time import sleep
from ..database.config import Config_twilio
config = Config_twilio()



# message = client.messages.create(
#                               body='Hello there!',
#                               from_='whatsapp:+14155238886',
#                               to='whatsapp:+972533405708'
#                           )

# print(message.sid)

class Whatsapp():
    def __init__(self):
        self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        self.from_num = config.twilio_num
        self.new_workers_nums = config.new_workers_nums
        self.new_job_nums = config.new_job_nums

    def send_to(self, msg, num):
        if type(num) == str:
            if num[0] == '+':
                to_num = 'whatsapp:'+str(num)
            elif num[0] == 'w':
                to_num = num
            else:
                to_num = 'whatsapp:+' + str(num)
        else:
            to_num = 'whatsapp:+' + str(num)
        _ = self.client.messages.create(body=msg, from_=self.from_num, to=to_num)

    def new_worker_msg(self, msg):
        for num in self.new_workers_nums:
            _ = self.client.messages.create(body=msg, from_=self.from_num, to=num)
            sleep(0.1)

    def new_job_msg(self, msg):
        for num in self.new_job_nums:
            _ = self.client.messages.create(body=msg, from_=self.from_num, to=num)
            sleep(0.1)


# twilio
# https://wa.me/+14155238886?text=join%20claws-dropped



# https://wa.me/+972533405708?text=I'm%20interested%20in%20your%20car%20for%20sale


if __name__ == '__main__':
    wa = Whatsapp()
    wa.new_worker_msg('test')