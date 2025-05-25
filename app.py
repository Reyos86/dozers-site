from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

MESSAGES_FILE = 'messages.json'

founders = [
    {
        "name": "DarkShockGamer",
        "image": "founders/shock.png",
        "nickname": "The Jeep-Flipping Mod Extraordinaire",
        "bio": "Hey, I’m DarkShockGamer. I help keep things running smoothly as a moderator on our Discord server. Whether it's navigating wild in-game moments (yes, even the occasional jeep flip) or helping the community stay connected and respectful, I’m always here to keep the wheels turning.",
        "youtube": "https://www.youtube.com/@DarkShockGamer1",
        "twitch": "https://www.twitch.tv/blackshockgamer"
    },
    {
        "name": "BullDozerBates",
        "image": "founders/dozer.jpg",
        "nickname": "His Jeep Goes Beep-Beep",
        "bio": "Dozer’s the glue holding the squad together — mostly duct tape and sarcasm, but it works. If he’s not cracking one-liners, he’s already two grid squares ahead, casually lining up the next intercept like it’s a Sunday drive.",
        "youtube": "https://www.youtube.com/@bulldozerbates",
      #  "twitch": "https://twitch.tv/skysniper"
    },
    {
        "name": "PilotWinks",
        "image": "founders/pilot.png",
        "nickname": "Jeff #1",
        "bio": "I don't chase storms to escape the calm—I chase them to meet the chaos head-on and come out stronger on the other side.",
        "youtube": "https://youtube.com/@garodah?si=qc9CkDalQ-t9TszC",
      #  "twitch": "https://twitch.tv/skysniper"
    },
        {
        "name": "Queen-B",
        "image": "founders/queen.png",
        "nickname": "Jeff Herder",
        "bio": "Queen-B is the life of the convoy — loud on comms, quick with the jokes, and somehow still the one keeping everyone on track. She may bring the chaos, but when it’s go-time, she’s all business (with a side of sass)!",
        "youtube": "https://youtube.com/@queenbukkake?si=zmGKoZBhUdMjrhh5",
      #  "twitch": "https://twitch.tv/skysniper"
    },
        {
        "name": "Reyos",
        "image": "founders/reyos.png",
        "nickname": "Snack Provider",
        "bio": "Calm in the chaos, steady on the intercept — they call the shots without needing to shout. Whether leading a van full of Jeffs into the storm or quietly crafting the next great squad moment, they’re always chasing something bigger… usually with radar in one hand and a joke in the other.",
        "youtube": "https://www.youtube.com/@reyos86",
        "twitch": "https://www.twitch.tv/reyos86"
    },
        {
        "name": "Joe \"Garodah\"",
        "image": "founders/joe.png",
        "nickname": "The Weatherman",
        "bio": "Joe didn’t just study weather — he probably majored in “knowing where the storm is before the radar does.” While the rest of us are yelling “WHERE’S IT GOING?”, Joe’s already halfway there, sipping coffee and marking the probe spot with GPS-level precision.",
        "youtube": "https://youtube.com/@garodah?si=qc9CkDalQ-t9TszC",
      #  "twitch": "https://twitch.tv/skysniper"
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
    #    "twitch": "https://www.twitch.tv/applejacks1980"
    },    
]

@app.route('/media')
def media():
    return render_template('media.html')

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

    return render_template('index.html', messages=messages, founders=founders)

if __name__ == "__main__":
    app.run(debug=True)
