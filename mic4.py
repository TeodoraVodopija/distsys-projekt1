#implementiranje potrebnih paketa
from aiohttp import web
import asyncio
import aiofiles
import aiounittest

usernames = []
file_path = 'file.txt'

#mikroservis - web
routes = web.RouteTableDef()

#ruta mikroservisa
@routes.post("/gatherData")
#asinkrona funkcija
async def create_file(request):
    json_data = await request.json()
    usernames.extend([username for username in json_data])
    print(usernames)

    if len(usernames) > 10:
        async with aiofiles.open(file_path, mode = 'w') as f:
            await f.write('\n'.join(usernames))
    return web.json_response(usernames, status=200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8085)

class test(aiounittest.AsyncTestCase):
    async def test_create_file(self):
        res = await create_file()
        self.assertEqual(res, web.json_response(res, status = 200))
