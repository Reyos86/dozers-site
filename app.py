from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import requests
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

MESSAGES_FILE = 'messages.json' 

KM_TO_MI = 0.621371
M_TO_MI = 0.000621371

founders = [
    {
        "name": "DarkShockGamer",
        "image": "founders/shock.png",
        "nickname": "The Jeep-Flipping Mod Extraordinaire",
        "bio": "Hey, I’m DarkShockGamer. I help keep things running smoothly as a moderator on our Discord server. Whether it's navigating wild in-game moments (yes, even the occasional jeep flip) or helping the community stay connected and respectful, I’m always here to keep the wheels turning.",
        "youtube": "https://www.youtube.com/@DarkShockGamer1",
        "twitch": "https://www.twitch.tv/blackshockgamer",
        "token": "8bf12bdc"
    },
    {
        "name": "BullDozerBates",
        "image": "founders/dozer.jpg",
        "nickname": "His Jeep Goes Beep-Beep",
        "bio": "Dozer’s the glue holding the squad together — mostly duct tape and sarcasm, but it works. If he’s not cracking one-liners, he’s already two grid squares ahead, casually lining up the next intercept like it’s a Sunday drive.",
        "youtube": "https://www.youtube.com/@bulldozerbates",
        "token": "dccb23c4"
      #  "twitch": "https://twitch.tv/skysniper"
    },
    {
        "name": "PilotWinks",
        "image": "founders/pilot.png",
        "nickname": "Jeff #1",
        "bio": "I don't chase storms to escape the calm—I chase them to meet the chaos head-on and come out stronger on the other side.",
        "youtube": "https://youtube.com/@garodah?si=qc9CkDalQ-t9TszC",
      #  "twitch": "https://twitch.tv/skysniper",
        "token": "e414efd7"
    },
        {
        "name": "Queen-B",
        "image": "founders/queen.png",
        "nickname": "Jeff Herder",
        "bio": "Queen-B is the life of the convoy — loud on comms, quick with the jokes, and somehow still the one keeping everyone on track. She may bring the chaos, but when it’s go-time, she’s all business (with a side of sass)!",
        "youtube": "https://youtube.com/@queenbukkake?si=zmGKoZBhUdMjrhh5",
      #  "twitch": "https://twitch.tv/skysniper",
        "token": "6ccbaf4b"    
    },
        {
        "name": "Reyos",
        "image": "founders/reyos.png",
        "nickname": "Snack Provider",
        "bio": "Calm in the chaos, steady on the intercept — they call the shots without needing to shout. Whether leading a van full of Jeffs into the storm or quietly crafting the next great squad moment, they’re always chasing something bigger… usually with radar in one hand and a joke in the other.",
        "youtube": "https://www.youtube.com/@reyos86",
        "twitch": "https://www.twitch.tv/reyos86",
        "token": "a55f058c"    
    },
        {
        "name": "Joe \"Garodah\"",
        "image": "founders/joe.png",
        "nickname": "The Weatherman",
        "bio": "Joe didn’t just study weather — he probably majored in “knowing where the storm is before the radar does.” While the rest of us are yelling “WHERE’S IT GOING?”, Joe’s already halfway there, sipping coffee and marking the probe spot with GPS-level precision.",
        "youtube": "https://youtube.com/@garodah?si=qc9CkDalQ-t9TszC",
        "token": "236a1685",    
        "twitch": "https://twitch.tv/GarodahKing"
    },
        {
        "name": "Dre \"BeardedSerb\"",
        "image": "founders/bearded.png",
        "nickname": "CodeChaser",
        "bio": "tech-savvy wizard behind our Discord and a seasoned gamer with stories for days. When he’s not wrangling IT by day, you’ll catch him streaming GTA RP on ONX or tearing up the track in iRacing with his squad, The Wrong Stuff — all without a schedule, just good vibes.",
        "youtube": "https://www.youtube.com/channel/UCHb0kIy3Sa5Qbl5hxAfn8ew",
      #  "twitch": "https://twitch.tv/skysniper"
    },        
    {
        "name": "Warren Modding",
        "image": "founders/warren.png",
        "nickname": "The Stormsmith",
        "bio": "Builds mods by night and chases twisters by instinct. Whether he’s coding new gear for the crew or floorboarding it toward a rotating supercell, Warren’s the kind of guy who can deploy a probe and patch a config file in the same breath.",
      #  "youtube": "https://youtube.com/@garodah?si=qc9CkDalQ-t9TszC",
      #  "twitch": "https://www.twitch.tv/bearded_serb/about"
    },        {
        "name": "Ayeejax",
        "image": "founders/aj.png",
        "nickname": "Radar Renegade",
        "bio": "AJ doesn’t check the radar — the radar checks with AJ. Known for casually flirting with EF3s and turning missed intercepts into highlight reels, Ayeejax lives by one motto: if there’s a storm worth chasing, he’s already down the road yelling “SEND IT!” over comms.",
        "youtube": "https://www.youtube.com/channel/UCISTQmtiSMZuzJNX_YYJ-0A",
    #    "twitch": "https://www.twitch.tv/applejacks1980",
        "token": "9c1628ac"
    },    
]

def get_outbrk_stats(token):
    try:
        url = f"https://api.outbrkgame.com/api/stats?token={token}"
        response = requests.get(url)
        if response.status_code != 200:
            return {}

        data = response.json()
        stats = {item["name"]: item["value"] for item in data.get("playerstats", {}).get("stats", [])}

        return {
            "driven_miles": round(stats.get("distance_travelled_driving", 0) * KM_TO_MI, 2),
            "foot_miles": round(stats.get("distance_travelled_onfoot", 0) * M_TO_MI, 2),
            "direct_intercepts": int(stats.get("tornado_direct_hits", 0)),
            "probes_deployed": int(stats.get("probes_deployed", 0)),
            "probes_recovered": int(stats.get("probes_recovered", 0)),
            "best_chase_score": int(stats.get("best_chase_score", 0))
        }

    except Exception as e:
        print(f"Error fetching stats for token {token}: {e}")
        return {}

import os

# Initialize Sheets client
def get_gsheet_client():
    creds = Credentials.from_service_account_file('/etc/secrets/dozers-leaderboard-3c46cc25ae6b.json')
    client = gspread.authorize(creds)
    return client

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        display_name = request.form.get("display_name")
        token = request.form.get("token")

        # Ensure file exists and load
        users = []
        if os.path.exists("outbrk_users.json"):
            with open("outbrk_users.json", "r") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        
        # Append new user
        users.append({
            "display_name": display_name,
            "token": token
        })

        # Save the updated list
        with open("outbrk_users.json", "w") as f:
            json.dump(users, f, indent=2)

        return redirect(url_for('signup'))  # or 'index' if preferred

    return render_template('signup.html')
    
@app.route('/media')
def media():
    return render_template('media.html')

@app.route('/twitch_status')
def twitch_status():
    client_id = os.environ.get("TWITCH_CLIENT_ID")
    access_token = os.environ.get("TWITCH_ACCESS_TOKEN")

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "user_login": "reyos86"
    }

    response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params)
    data = response.json()
    
    if data.get("data"):
        return jsonify({"live": True})
    else:
        return jsonify({"live": False})

@app.route('/youtube_status')
def youtube_status():
    api_key = "AIzaSyANJffTPuadaGCnDcqpTs-B20e74Msp7Zs"
    channel_ids = { 
        "DarkShockGamer1": "UClkdz-_SpaJkgcIktqtfPdg",
        "Twista_HuntaLIVE": "UCh21stagaKCZAMRrtaP01gg"
    }

    live_streams = []

    for name, channel_id in channel_ids.items():
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {
            "part": "id",
            "channelId": channel_id,
            "eventType": "live",
            "type": "video",
            "key": api_key
        }

        response = requests.get(search_url, params=search_params)
        data = response.json()

        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            live_streams.append({
                "name": name,
                "videoId": video_id
            })

    return jsonify(live_streams)


@app.route('/weather')
def get_weather():
    api_key = "35b5f6e19f2be4347afe5d6076b4d008"

    try:
        # ✅ Get clean IP from comma list
        x_forwarded_for = request.headers.get('X-Forwarded-For', '')
        client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.remote_addr

        # ✅ Geolocation
        geo_res = requests.get(f"https://ipwho.is/{client_ip}")
        geo_data = geo_res.json()
        print("Geo data:", geo_data)

        # ✅ Fallback if IP lookup fails
        if not geo_data.get("success"):
            print("⚠️ Fallback to Joplin, MO")
            lat, lon = 37.0855, -94.5134
            city, region = "Joplin", "MO"
        else:
            lat = geo_data.get("latitude")
            lon = geo_data.get("longitude")
            city = geo_data.get("city", "Unknown")
            region = geo_data.get("region", "Unknown")

        # ✅ Weather API call
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
        res = requests.get(url)
        weather_data = res.json()
        print("Weather data:", weather_data)

        # ✅ Current Weather
        current = weather_data.get("current", {})
        temperature = current.get("temp")
        description = current.get("weather", [{}])[0].get("description", "No description").title()
        icon = current.get("weather", [{}])[0].get("icon", "")

        # ✅ Alerts
        alert = None
        if "alerts" in weather_data and len(weather_data["alerts"]) > 0:
            alert_data = weather_data["alerts"][0]
            alert = {
                "event": alert_data.get("event", "Weather Alert"),
                "description": alert_data.get("description", ""),
                "sender": alert_data.get("sender_name", "")
            }
        
        return jsonify({
            "location": {"city": city, "region": region},
            "temperature": temperature,
            "narrative": description,
            "icon": icon,
            "alert": alert
        })

    except Exception as e:
        print("Weather error:", e)
        return jsonify({"error": "Unable to load weather data."}), 500
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']

        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r') as f:
                messages = json.load(f)
        else:
            messages = []

        messages.append({'username': username, 'message': message})

        with open(MESSAGES_FILE, 'w') as f:
            json.dump(messages, f)

        return redirect(url_for('index'))

    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as f:
            messages = json.load(f)
    else:
        messages = []

    enhanced_founders = []
    for founder in founders:
        if "token" in founder:
            stats = get_outbrk_stats(founder["token"])
            founder["stats"] = stats
        enhanced_founders.append(founder)
    
    return render_template('index.html', messages=messages, founders=enhanced_founders)


if __name__ == "__main__":
    app.run(debug=True)
