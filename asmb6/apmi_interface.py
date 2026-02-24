import requests
import re
import json
from .parser import sanitize, serialize, parse_sensors, Sensors

start_ref = """<?xml version="1.0" encoding="UTF-8"?>

<jnlp spec="1.0+" codebase="""
end_ref = """    </application-desc>
</jnlp>
"""


class APMI:
    def __init__(self, ip, http_port=80):
        self.http_port = http_port
        self.username = None
        self.ip = ip
        self.session = requests.Session()
        self.base = f"http://{self.ip}:{self.http_port}"

    def login(self, username, password) -> int:
        """
        Important:
            Always call logout() before terminating the program.

            Failing to do so may leave an active session on the
            ASMB6-iKVM, which can cause login issues during
            development or repeated test runs.
        """
        data = {
            "WEBVAR_USERNAME": username,
            "WEBVAR_PASSWORD": password,
        }

        res = self.session.post(self.base + "/rpc/WEBSES/create.asp", data=data)
    
        json_res = json.loads(serialize(sanitize(res.text)))["WEBVAR_JSONVAR_WEB_SESSION"]
        status = json_res["HAPI_STATUS"]
        if status != 0:
            print(f"Invalid credential")
        else:
            session_cookie = json_res["WEBVAR_STRUCTNAME_WEB_SESSION"][0]["SESSION_COOKIE"]
            
            self.session.cookies.set("Username", username, domain=self.ip, path="/")
            self.session.cookies.set("Language", "EN", domain=self.ip, path="/")
            self.session.cookies.set("SessionCookie", session_cookie, domain=self.ip, path="/")
            self.username = username
        
        return status

    def logout(self)->int:
        res = self.session.get(self.base + "/rpc/WEBSES/logout.asp")
        self.session = requests.Session()
        self.username = None
        return json.loads(serialize(sanitize(res.text)))["WEBVAR_JSONVAR_WEB_SESSION_LOGOUT"]["HAPI_STATUS"]

    def validate_session(self)->int:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.get(self.base + "/rpc/WEBSES/validate.asp").text
        return json.loads(serialize(sanitize(res.text)))["WEBVAR_JSONVAR_WEB_SESSION_VALIDATE"]["HAPI_STATUS"]
    
    def sensors(self) -> Sensors:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.get(self.base + "/rpc/getallsensors.asp")
        raw = json.loads(serialize(sanitize(res.text)))
        sensors_data = raw["WEBVAR_JSONVAR_HL_GETALLSENSORS"][
            "WEBVAR_STRUCTNAME_HL_GETALLSENSORS"
        ]
        sensors = parse_sensors(sensors_data)
        return sensors

    def status(self) -> int:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.get(self.base + "/rpc/hoststatus.asp")
        raw = json.loads(serialize(sanitize(res.text)))
        return raw["WEBVAR_JSONVAR_HL_SYSTEM_STATE"][
            "WEBVAR_STRUCTNAME_HL_SYSTEM_STATE"
        ][0]["JF_STATE"]

    def pwr_btn_status(self) -> int:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.get(self.base + "/rpc/PWRbutton.asp")
        raw = json.loads(serialize(sanitize(res.text)))
        return raw["WEBVAR_JSONVAR_HL_BUTTON_STATE"][
            "WEBVAR_STRUCTNAME_HL_BUTTON_STATE"
        ][0]["PB_STATE"]

    def turn_off_board(self, immediate=False) -> None:
        """
        Note:
            immediate=True may not turn the board off if it was powered on
            less than 15 seconds before this call.
        """
        if not self.username:
            raise Exception("You need to be authenticated")
        if immediate:
            res = self.session.post(
                self.base + "/rpc/hostctl.asp", data={"WEBVAR_POWER_CMD": 0}
            )
        else:
            res = self.session.post(
                self.base + "/rpc/hostctl.asp", data={"WEBVAR_POWER_CMD": 5}
            )

    def turn_on_board(self) -> None:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.post(
            self.base + "/rpc/hostctl.asp", data={"WEBVAR_POWER_CMD": 1}
        )

    def power_cycle_board(self) -> None:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.post(
            self.base + "/rpc/hostctl.asp", data={"WEBVAR_POWER_CMD": 2}
        )

    def reset_board(self) -> None:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.post(
            self.base + "/rpc/hostctl.asp", data={"WEBVAR_POWER_CMD": 3}
        )

    def get_events(self) -> dict:
        if not self.username:
            raise Exception("You need to be authenticated")
        res = self.session.get(self.base + "/rpc/getallselentries.asp")
        result = json.loads(serialize(sanitize(res.text)))[
            "WEBVAR_JSONVAR_HL_GETALLSELENTRIES"
        ]["WEBVAR_STRUCTNAME_HL_GETALLSELENTRIES"][:-1]
        return result

    def get_jnlp(self) -> str:
        if not self.username:
            raise Exception("You need to be authenticated")
        
        res = self.session.get(
            self.base + f"/Java/jviewer.jnlp?EXTRNIP={self.base}&JNLPSTR=JViewer",
            stream=True,
        )

        data = b""
        try:
            for chunk in res.iter_content(1):
                if chunk:
                    data += chunk
        except requests.exceptions.RequestException as e:
            # Strings parsed from the firmware's jviewer.jnlp template.
            if data.startswith(start_ref.encode()) and data.endswith(end_ref.encode()):
                print("Notice: The data appears to have downloaded correctly, but the firmware closed the connection before all content-length data was received.")
            else:
                raise e

        return data.decode()
