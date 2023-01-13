#implementiranje potrebnih paketa
from aiohttp import web
import requests
import aiounittest

#Worker tokenizer (WT) mikroservis
routes = web.RouteTableDef()

@routes.post("/")
async def selected(request):
    json_data = await request.json()

    # provjera ako username počinje slovom d/D
    res = [d['username'] for d in json_data if 'username' in d and d['username'].lower().startswith('w')]

    # ispis rezultata
    print(res)

    requests.post('http://127.0.0.1:8085/gatherData', json = res)

    return web.json_response(res, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8083)

class test(aiounittest.AsyncTestCase):
    async def test_selected(self):
        res = await selected()
        self.assertEqual(res, web.json_response(res, status = 200))

    async def test_await_selected(self):
        with self.assertRaises(Exception) as e:
            await selected()