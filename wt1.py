#implementiranje potrebnih paketa
from aiohttp import web
import requests

#Worker tokenizer (WT) mikroservis
routes = web.RouteTableDef()

@routes.post("/")
async def selected(request):
    json_data = await request.json()
    #deklaracija i inicijalizacija nove varijable kao početne prazne liste
    wt1 = []
    #provjera ako username počinje slovom w/W
    for user in json_data:
        if 'username' in user and user['username'].lower().startswith('w'):
            wt1.append(user['username'])

    #ispis rezultata
    res1 = wt1
    print(res1)

    requests.post('http://127.0.0.1:8085/gatherData', json = res1)

    return web.json_response(res1, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8083)