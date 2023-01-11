#implementiranje potrebnih paketa
from aiohttp import web

#mikroservis - web
routes = web.RouteTableDef()

@routes.post("/")
async def selected(request):
    json_data = await request.json()
    #deklaracija i inicijalizacija nove varijable kao početne prazne liste
    data = []
    for d in json_data:
        #spremanje podataka u praznu listu data
        data.append(d)
    result = data
    #ispis rezultata u konzolu
    print("result: ", result)
    """
    url1 = 'http://127.0.0.1:8083/'
    url2 = 'http://127.0.0.1:8084/'
    
    requests.post(url1, json=result)
    requests.post(url2, json=result)
    """
    return web.json_response(result, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8080)