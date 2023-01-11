#implementiranje potrebnih paketa
from aiohttp import web
import asyncio
import aiofiles

#mikroservis - web
routes = web.RouteTableDef()

#ruta mikroservisa
@routes.post("/gatherData")
#asinkrona funkcija
async def create_file(request):
    json_data = await request.json()
    list_of_usernames = []
    for username in json_data:
        list_of_usernames.append(username)
    print(list_of_usernames)

    #zapisivanje u novu tekstualnu datoteku
    filename = "file.txt"
    async with aiofiles.open(filename, 'w') as file:
        await file.write(username)

        if len(list_of_usernames) > 10:
            tasks = [asyncio.create_task(create_file(filename))]

        for task in asyncio.as_completed(tasks):
                result = await task
        print(result)
    return web.json_response(list_of_usernames, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8085)