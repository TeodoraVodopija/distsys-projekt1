import json
import aiofiles
import aiosqlite
from aiohttp import web
import sqlite3
import requests

conn = sqlite3.connect('base.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM base")
cf = cursor.fetchone()[0]

if cf == 0:
    print("The database is empty.")
else:
    print("The database not empty.")

routes = web.RouteTableDef()


@routes.get("/dataJson")
async def data_json(req):
    async with aiofiles.open('file-000000000040.json', mode='r') as file_data:
        r_data = {await file_data.readline() for _ in range(10)}
        data = [json.loads(line) for line in r_data]
        db = []
        result = []
        async with aiosqlite.connect("base.db") as db:
            for item in data:
                db_item = {}
                db_item["username"] = item["repo_name"].rsplit("/", 1)[0]
                db_item["ghlink"] = "https://github.com/" + item["repo_name"] + ".com"
                path = item["path"].rsplit("/", 1)
                if len(path) > 1:
                    db_item["filename"] = path[1]
                else:
                    db_item["filename"] = item["path"]

                db.append(db_item)
                await db.execute("INSERT INTO base (username, ghlink, filename) VALUES (?,?,?)",
                                (db_item["username"], db_item["ghlink"], db_item["filename"]))
            async with db.execute("SELECT * FROM base LIMIT 100") as cur:
                col = [column[0] for column in cur.description]
                result = await cur.fetchall()
                for row in result:
                    result.append(dict(zip(col, row)))
                data = result

                await db.commit()
        return web.json_response(data, status=200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)