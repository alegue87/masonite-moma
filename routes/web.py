from masonite.routes import Route
from masonite.api import Api

ROUTES = [
    Route.get("/", "WelcomeController@show"),
    Route.get("/add/@var", "WelcomeController@add"),
    Route.get('/load', "WelcomeController@load"),
    Route.get('/load_jobs', "WelcomeController@load_jobs"),
    Route.post('/api', "WelcomeController@gra"),

]
ROUTES += Api.routes(auth_route="/api/auth", reauth_route="/api/reauth")