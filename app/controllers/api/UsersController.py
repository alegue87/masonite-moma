from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response

class UsersController(Controller):
    def index(self, view: View, response: Response):
        return response.json({'data': {'user': 'a'}})

    def show(self, view: View):
        return view.render("")

    def store(self, view: View, request: Request, response: Response):
        
        return request.json()
        # return view.render("")

    def update(self, view: View):
        return view.render("")

    def destroy(self, view: View):
        return view.render("")
