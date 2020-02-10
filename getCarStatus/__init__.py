import logging
import volkswagencarnet
import azure.functions as func


class WeConnection:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        vw = volkswagencarnet.Connection(self.username, self.password, guest_lang='fi')
        # login to carnet
        vw._login()

        if not vw.logged_in:
            print('Could not login to carnet')
            sys.exit(1)
        else:
            self.connection = vw

    def updateCars(self):
        self.connection.update()

    def getCarJson(self, index=0):
        for vehicle in self.connection.vehicles:
            return vehicle.json
            break
    
    def logout(self):
        self.connection._logout()



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        print('ERROR')
        return func.HttpResponse(
             "Invalid request",
             status_code=400
        )
    

    name = req_body.get('username')
    pwd = req_body.get('pwd')

    gte = WeConnection(username=name, password=pwd)
    gte.login()
    gte.updateCars()


    json = gte.getCarJson()

    gte.logout()

    if json:
        return func.HttpResponse(json)
    else:
        return func.HttpResponse(
             "Invalid request",
             status_code=400
        )
