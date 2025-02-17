from masonite.routes import Route

ROUTES = [
    Route.api('gra', "api.TestController"),
    Route.api('users', "api.UsersController")
]
