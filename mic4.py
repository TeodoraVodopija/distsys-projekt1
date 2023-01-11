#implementiranje potrebnih paketa
from aiohttp import web
import asyncio
import aiofiles
import aiounittest

#mikroservis - web
routes = web.RouteTableDef()

#ruta mikroservisa
@routes.post("/gatherData")
#asinkrona funkcija
async def create_file(request):
    json_data = await request.json()
    res = []
    for username in json_data:
        res.append(username)
    print(res)

    #zapisivanje u novu tekstualnu datoteku
    filename = "file.txt"
    async with aiofiles.open(filename, 'w') as file:
        await file.write(username)

        if len(res) > 10:
            tasks = [asyncio.create_task(create_file(filename))]

        for task in asyncio.as_completed(tasks):
                result = await task
        print(result)
    return web.json_response(res, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8085)

class test(aiounittest.AsyncTestCase):
    async def test_create_file(self):
        res = await create_file()
        self.assertEqual(res, web.json_response(res, status = 200))
