#implementiranje potrebnih paketa
from aiohttp import web
import requests

#Worker tokenizer (WT) mikroservis
routes = web.RouteTableDef()

@routes.post("/")
async def selected(request):
    json_data = await request.json()
    #deklaracija i inicijalizacija nove varijable kao početne prazne liste
    wt2 = []
    #provjera ako username počinje slovom d ili D
    for user in json_data:
        if 'username' in user and user['username'].lower().startswith('d'):
            wt2.append(user['username'])

    #ispis rezultata
    res2 = wt2
    print(res2)

    requests.post('http://127.0.0.1:8085/gatherData', json = res2)

    return web.json_response(res2, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8084)