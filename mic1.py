#implementiranje potrebnih paketa
from aiohttp import web
import requests

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
    #prosljeđivanje podataka kao dictionary WT mikroservisu
    requests.post('http://127.0.0.1:8083/', json = result)
    requests.post('http://127.0.0.1:8084/', json = result)

    return web.json_response(result, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8081)