#implementiranje potrebnih paketa
import json
import aiofiles
import aiosqlite
from aiohttp import web
import sqlite3
import requests

#spajanje sa bazom podataka (ime baze - base.db)
connection = sqlite3.connect('base.db')
#kreiranje kursor objekta
cursor = connection.cursor()

#čitanje iz baze podataka
cursor.execute("SELECT COUNT(*) FROM project_base")
#dohvaćanje prvog retka iz tablice baze podataka
c = cursor.fetchone()[0]

#provjera ako je baza podataka prazna
if c == 0:
    print("The database is empty.")
else:
    print("The database is not empty.")

#mikroservis - web
routes = web.RouteTableDef()

#ruta mikroservisa
@routes.get("/dataJson")
#asinkrona funkcija json_data
async def json_data(request):
    #čitanje json datoteke
    async with aiofiles.open('file-000000000040.json', mode = 'r') as file_data:
        #čitanje podataka iz json datoteke liniju po liniju
        data_read = {await file_data.readline() for _ in range(10000)}
        #zapisivanje pročitanih podataka iz json datoteke u varijablu
        all_data = [json.loads(line) for line in data_read]
        #inicijaliziranje varijabla na početnu praznu listu koju kasnije punimo podacima
        base_data = []
        final = []
        #konekcija sa bazom podataka
        async with aiosqlite.connect("base.db") as database:
            #for petlja za prolazak kroz json datoteku
            for item in all_data:
                #inicijaliziranje varijable na početni prazan dictionary
                items = {}
                #zapisivanje username-a (samo početni dio repo_name-a - splitanje)
                items["username"] = item["repo_name"].rsplit("/", 1)[0]
                #zapisivanje github linka sa dodavanjem url adrese
                items["ghlink"] = "https://github.com/" + item["repo_name"] + ".com"
                #zapisivanje file-a, provjera ako je ruta samo do / ili ima i poddirektorija
                path = item["path"].rsplit("/", 1)
                if len(path) > 1:
                    items["filename"] = path[1]
                else:
                    items["filename"] = item["path"]
                #dodavanje u bazu podataka onih podataka koje smo isčitali iz json datoteke
                base_data.append(items)
                await database.execute("INSERT INTO project_base (username, ghlink, filename) VALUES (?,?,?)",
                                      (items["username"], items["ghlink"], items["filename"]))
            #selektiranje iz spremljene baze podataka koju smo napunili gornjim podacima
            async with database.execute("SELECT * FROM project_base LIMIT 100") as cur:
                #dohvaćanje imena stupaca
                columns = [column[0] for column in cur.description]
                #dohvaćanje svih redaka kao listu tuple-a
                result = await cur.fetchall()
                #prazan dictionary u koji se spremaju podaci
                response = {}
                #prolazak kroz bazu podataka i uzimanje podataka
                for row in result:
                    service_id, usernames, github_links, paths = row
                    response = {
                        "service_id": service_id,
                        "data": {
                            "usernames": usernames,
                            "githubLinks": github_links,
                            "paths": paths
                        }
                    }
                    #zapisivanje u listu
                    final.append(dict(zip(columns, row)))
                #prebacivanje listu u varijablu
                data = final

                #prosljeđivanje liste podataka drugom mikroservisu
                requests.post('http://127.0.0.1:8081', json = data)

                await database.commit()
        #vraćanje rezultata asinkrone funkcije
        return web.json_response(response, status = 200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8080)