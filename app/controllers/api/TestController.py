from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response

class TestController(Controller):
    def index(self, view: View):
        return view.render("")

    def show(self, view: View):
        return view.render("")

    def store(self, view: View, request: Request, response: Response):
        return response.json({'prova': 'ciao'})
        #return view.render("")

    def update(self, view: View):
        return view.render("")

    def destroy(self, view: View):
        return view.render("")
