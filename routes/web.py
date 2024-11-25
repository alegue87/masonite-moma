from masonite.routes import Route

ROUTES = [
    Route.get("/", "WelcomeController@show"),
    Route.get("/add/@var", "WelcomeController@add"),
    Route.get('/delall', "WelcomeController@delall"),
]
