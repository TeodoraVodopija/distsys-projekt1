import json
import aiofiles
import aiosqlite
from aiohttp import web
import sqlite3

connection = sqlite3.connect('base.db')
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM project_base")
c = cursor.fetchone()[0]

if c == 0:
    print("The database is empty.")
else:
    print("The database is not empty.")

routes = web.RouteTableDef()


@routes.get("/dataJson")
async def data_json(request):
    async with aiofiles.open('file-000000000040.json', mode='r') as file_data:
        data_read = {await file_data.readline() for _ in range(10)}
        all_data = [json.loads(line) for line in data_read]
        database = []
        final = []
        async with aiosqlite.connect("base.db") as db:
            for item in all_data:
                items = {}
                items["username"] = item["repo_name"].rsplit("/", 1)[0]
                items["ghlink"] = "https://github.com/" + item["repo_name"] + ".com"
                path_parts = item["path"].rsplit("/", 1)
                if len(path_parts) > 1:
                    items["filename"] = path_parts[1]
                else:
                    items["filename"] = item["path"]

                database.append(items)
                await db.execute("INSERT INTO project_base (username, ghlink, filename) VALUES (?,?,?)",
                                 (items["username"], items["ghlink"], items["filename"]))
            async with db.execute("SELECT * FROM project_base LIMIT 100") as cur:
                columns = [column[0] for column in cur.description]
                result = await cur.fetchall()
                for row in result:
                    final.append(dict(zip(columns, row)))
                data = final

                await db.commit()
        return web.json_response(data, status=200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)
