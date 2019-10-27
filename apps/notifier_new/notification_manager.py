import appdaemon.plugins.hass.hassapi as hass
import datetime
import globals

"""
Class Notification_Manager handles sending text to notfyng service
"""
__NOTIFY__ = "notify/"

class Notification_Manager(hass.Hass):

    def initialize(self):
        self.text_last_message = globals.get_arg(self.args, "text_last_message")

    def send_notify(self, data, assistant_name: str):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        title = data["title"]
        message = data["message"].replace("\n","").replace("   ","").replace("  "," ")
        url = data["url"]
        _file = data["file"]
        caption = data ["caption"]
        notify_name = data["notify"]
        link = data["link"]

        self.log = ("[MESSAGGIO]: {}".format(message))

        ### SAVE IN INPUT_TEXT.LAST_MESSAGE
        self.set_state(self.text_last_message, state = message[:245])

        if title !="":
            title = ("*[{} - {}]* *{}*".format(assistant_name, timestamp, title))
        else:
            title = ("*[{} - {}]*".format(assistant_name, timestamp))
        
        if link !="":
            message = ("{} {}".format(message,link))

        if caption =="":
            caption = ("{}\n{}".format(title,message))

        if url !="":
            extra_data = { "photo": 
                            {"url": url,
                            "caption": caption}
                        }
        elif _file !="":
            extra_data = { "photo": 
                            {"file": _file,
                            "caption": caption}
                        }
        if url !="" or _file !="":
            self.call_service(__NOTIFY__ + notify_name, 
                            message = "", 
                            data = extra_data)
        else:                    
            self.call_service(__NOTIFY__ + notify_name, 
                            message = message, 
                            title = title)

    def send_persistent(self, data):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        #title = data["title"]
        message = data["message"].replace("\n","").replace("   ","").replace("  "," ")
        self.call_service("persistent_notification/create",
                        notification_id = "info_messages",
                        message = ("{} - {}".format(timestamp, message)),
                        title = "Centro Messaggi")