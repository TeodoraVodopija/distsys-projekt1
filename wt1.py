#implementiranje potrebnih paketa
from aiohttp import web
import requests
import unittest

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
    res = wt1
    print(res)

    requests.post('http://127.0.0.1:8085/gatherData', json = res)

    return web.json_response(res, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8083)

class test(unittest.TestCase):
    async def test_selected(self):
        res = await selected()
        self.assertEqual(res, web.json_response(res, status = 200))