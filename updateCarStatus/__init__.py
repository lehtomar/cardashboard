import logging
import volkswagencarnet
import azure.functions as func
import json

class WeConnection:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        vw = volkswagencarnet.Connection(self.username, self.password, guest_lang='fi')
        # login to carnet
        vw._login()

        self.connection = vw

    def updateCars(self):
        self.connection.update()
        self.vehicle = list(self.connection.vehicles)[0]

    def getCarJson(self, index=0):
        return self.vehicle.json

    def startAction(self, action):
        if action == 'start-charge':
            resp = self.vehicle.start_charging()

        elif action == 'stop-charge':
            resp = self.vehicle.stop_charging()

        elif action == 'start-ac':
            resp = self.vehicle.start_climatisation()

        elif action == 'stop-ac':
            resp = self.vehicle.stop_climatisation()

        elif action == 'start-window-heating':
            resp = self.vehicle.start_window_heater()

        elif action == 'stop-window-heating':
            resp = self.vehicle.stop_window_heater()
        else:
            resp = 'No action started'

        return resp

    def logout(self):
        self.connection._logout()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Invalid request",
             status_code=400
        )
    

    name = req_body.get('username')
    pwd = req_body.get('pwd')
    action = req_body.get('action')

    gte = WeConnection(username=name, password=pwd)
    gte.login()

    if not gte.connection.logged_in:
        return func.HttpResponse(
             "Invalid request",
             status_code=400
        )
    

    gte.updateCars()
    appDict = gte.startAction(action=action)
    app_json = json.dumps(appDict)

    gte.logout()

    if json:
        return func.HttpResponse(app_json)
    else:
        return func.HttpResponse(
             "Invalid request",
             status_code=400
        )
