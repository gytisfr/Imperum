import requests, uvicorn
from fastapi import FastAPI

api = "https://discord.com/api"
redirect = "http://localhost:3000"

appId = "1006943755372343296"
publicKey = "07e08b0a3172fd0bb8e2b5e2607089b7fc3f06ffffc633ca05c6c1f63b0d9472"
clientSecret = "QENbUVpYRMXHwthJ6hBH0R-I6-OVPrhC"

app = FastAPI()



#title="Imperum Backend API",
#description="""nUSA's Imperum Service's Backend Functionality Application Programming Interface
#Bare URL: api.imperum.services
#Base Request: https://api.imperum.services/v1/
#Documentation: https://api.imperum.services/docs""",
#summary="Summary",
#version="1.0.0",
#contact={
#    "name": "Imperum Support",
#    "url": "aaaaa",
#    "email": "email@imperum.services"
#}



@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/v1/login")
def login(code : str):
    accessToken = requests.post(f"{api}/v10/oauth2/token", data={"grant_type": "authorization_code", "code": code, "redirect_uri": redirect}, auth=(appId, clientSecret)).json()
    info = json.loads(requests.get(f"{api}/v10/users/@me", headers={"Authorization": f"Bearer {accessToken['access_token']}"}).text)
    info["pfp"] = f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.webp"
    requests.post(f"{api}/oauth2/token/revoke", data={"token": accessToken["access_token"], "token_type_hint": "access_token"})
    return info

@app.get("/v1/bgc")
def bgc(authorization : str):
    print(1)
    return info

#app.run("0.0.0.0", port=8161)
uvicorn.run(app=app, host="0.0.0.0", port=8142)
#144.217.139.103:8142