
"""
category_mapping.py

Google Play 14-category mapping utilities for:
- Mapping raw policy terms -> (top_key, subtype)
- Parsing Data safety label sections -> normalized (top_key -> subtypes)
- Tracing mapped vs non-mapped policy strings

Top keys follow GOOGLE_SCHEMA keys.
"""

import re
from typing import Dict, List, Tuple, Set
from collections import defaultdict


# Google Play 14-data category schema

GOOGLE_SCHEMA: Dict[str, Dict[str, List[str]]] = {
    "personal_info": {"label": "Personal Info", "subtypes": [
        "name", "email address", "user ids", "address", "phone number",
        "race and ethnicity", "political or religious beliefs",
        "sexual orientation", "other personal info"
    ]},
    "location": {"label": "Location", "subtypes": [
        "approximate location", "precise location","geolocation"
    ]},
    "financial_info": {"label": "Financial Info", "subtypes": [
        "user payment info", "purchase history", "credit or debit card number",
        "credit score", "other financial info"
    ]},
    "messages": {"label": "Messages", "subtypes": [
        "emails", "sms or mms", "other in-app messages"
    ]},
    "photos_videos": {"label": "Photos and Videos", "subtypes": [
        "photos", "videos"
    ]},
    "audio": {"label": "Audio", "subtypes": [
        "voice or sound recordings", "music files", "other audio files"
    ]},
    "files_docs": {"label": "Files and Docs", "subtypes": [
        "files and docs"
    ]},
    "calendar": {"label": "Calendar", "subtypes": [
        "calendar events"
    ]},
    "contacts": {"label": "Contacts", "subtypes": [
        "contacts"
    ]},
    "app_activity": {"label": "App Activity", "subtypes": [
        "app interactions",
        "in-app search history",
        "installed apps",
        "other user-generated content",
        "other actions",
        "page views and taps"
    ]},
    "web_browsing": {"label": "Web Browsing", "subtypes": [
        "web browsing history"
    ]},
    "app_info_perf": {"label": "App Info and Performance", "subtypes": [
        "crash logs", "diagnostics", "other app performance data"
    ]},
    "device_or_other_ids": {"label": "Device or Other IDs", "subtypes": [
        "device or other ids"
    ]},
    "health_fitness": {"label": "Health and Fitness", "subtypes": [
        "health info", "fitness info", "sleep info", "menstrual cycle",
        "heart rate", "steps", "workouts", "other health and fitness info"
    ]},
}

# Helpers
def canon(s: str) -> str:
    """Lowercase, trim, collapse whitespace."""
    return re.sub(r"\s+", " ", s.strip().lower())

#  policy term -> (top_key, subtype)

TERM_TO_SUBTYPE_RULES: List[Tuple[str, Tuple[str, str]]] = [
    # ---------- Personal info ----------
    (r"\bemail addresses?\b", ("personal_info", "email address")),
    (r"\bemail\b", ("personal_info", "email address")),
    (r"\bname(s)?\b", ("personal_info", "name")),
    (r"(?<!email )(?<!ip )\b(address|mailing address|home address)\b",
    ("personal_info", "address")),

    # Phone / telephone numbers
    (r"\b(phone|telephone|mobile)( number)?s?\b",
    ("personal_info", "phone number")),
    (r"\b(user id|user ids|account id|account number|account name|profile id|uid|handle|screen ?name)\b",
    ("personal_info", "user ids")),

    # Other personal info
    (r"\b(date of birth|dob|birthday|age|gender identity|sex|biological sex|veteran status|other (personal )?info)\b",
    ("personal_info", "other personal info")),
    (r"\brace( and)? ethnicity\b",
    ("personal_info", "race and ethnicity")),
    (r"\b(political|religious) beliefs?\b",
    ("personal_info", "political or religious beliefs")),
    (r"\bsexual orientation\b",
    ("personal_info", "sexual orientation")),
    (r"\bprofile (photo|picture|avatar|image)\b",
    ("personal_info", "other personal info")),


    # Device or Other IDs
    (r"\b(?:"                                   
    r"ip address(?:es)?"                       
    r"|identifiers?|device (?:info|information|identifiers?)"
    r"|android id"
    r"|advertising ids?"                       
    r"|advertising identifiers?"              
    r"|ad id|aaid|gaid"
    r"|imei|imsi|iccid|serial number|mac address|bluetooth (?:mac|address)|wifi (?:mac|bssid|ssid)"
    r"|cookie|cookies?"
    r"|push (?:token|identifier)|fcm token|apns token"
    r"|device ?ids?|deviceid|e-?tags?|etag"
    r"|idfa|idfv|ifa|udid"
    r"|installation id|install id|instance id"
    r"|firebase (?:installation|instance) id"
    r"|hardware (?:id|identifier|identifiers)"
    r")\b",
    ("device_or_other_ids", "device or other ids")),


    # Location
    (r"\b(gps|latitude|longitude|lat[, ]?long|coordinate(s)?|precise location)\b",
     ("location", "precise location")),
    (r"\b(approximate location|country|city|region|state|zip|postal code|timezone|location( information)?)\b",
     ("location", "approximate location")),
    (r"\b(precise\s+geo[- ]?location|fine\s+location|exact\s+location|gps[- ]?based\s+location|a[- ]?gps)\b",
    ("location", "precise location")),
    (r"\b(geo[- ]?location|geolocat(?:e|es|ed|ing)|geo[- ]?tag(?:s?|ged|ging)|geo[- ]?fenc(?:e|es|ed|ing)|geospatial|coarse\s+location|city[- ]?level\s+location|ip(?:-based)?\s+location|ip\s+geolocation|network[- ]?based\s+location|wifi\s+triangulation|cell(?:ular)?\s+(?:tower|triangulation))\b",
    ("location", "approximate location")),

   # Financial info
    (r"\bpurchase history\b",
    ("financial_info", "purchase history")),
    (r"\b(payment|billing|transaction)( info| information| details)?\b",
    ("financial_info", "user payment info")),
    (r"\b(credit|debit) card( number)?\b",
    ("financial_info", "credit or debit card number")),
    (r"\bcredit score\b",
    ("financial_info", "credit score")),
    (r"\b(salary|debt|loan|bank account(?: number)?|bank details?|bank information|financial data|financial information|financial info|other financial info)\b",
    ("financial_info", "other financial info")),

    # Contacts
    (r"\bcontacts?|address book|phone ?book|contact (list|info|details)|friend(?:s)? (?:list|lists)\b",
    ("contacts", "contacts")),
    (r"\bcalls?\b", ("contacts", "contacts")),

    # Photos/Videos
    (r"\b(photos?|images?|pictures?|avatars?|visuals?|visual|media|screenshots?|camera data|camera)\b",
    ("photos_videos", "photos")),
    (r"\bvideos?\b", ("photos_videos", "videos")),

    # Audio
    (r"\b(voice|sound) recordings?\b", ("audio", "voice or sound recordings")),
    (r"\bmusic files?\b", ("audio", "music files")),
    (r"\baudio files?\b", ("audio", "other audio files")),
    (r"\bmic(?:rophone)?\b", ("audio", "microphone")),
    (r"\bmicrophone (?:audio|data|recordings?)\b", ("audio", "microphone")),
    (r"\bsounds?\b", ("audio", "other audio files")),
    (r"\baudio (?:information|info|data|content)\b", ("audio", "other audio files")),
    (r"\baudio\b", ("audio", "other audio files")),

    # Calendar (Calendar → calendar events)
    (r"\b(calendar(?: data| events?)?|dates?)\b",
    ("calendar", "calendar events")),


    # Files/Docs
    (r"\b(documents?|docs?|pdfs?|spreadsheets?|files?)\b", ("files_docs", "files and docs")),
    # Email
    (r"\b(email messages?|email content|emails?)\b(?!\s*address)",
    ("messages", "emails")),
    # SMS / MMS / text messages
    (r"\b(sms|mms|text messages?)\b",
    ("messages", "sms or mms")),
    # Chats / DMs / in-app messages
    (r"\b(chat(s)?|chat content|instant messages?|direct messages?|dms?|in-?app messages?)\b",
    ("messages", "other in-app messages")),
    # Generic "messages" (but not preceded by email / text / sms / mms)
    (r"(?<!email )(?<!text )(?<!sms )(?<!mms )\bmessages?\b",
    ("messages", "other in-app messages")),


    # App activity
    (r"\b(number of times (they )?visit(s)? (a|the) page|visit counts?|page visit(s)?|page views?|screen views?|taps?|clicks?|button presses?)\b",
     ("app_activity", "page views and taps")),
    (r"\bapp interactions?\b", ("app_activity", "app interactions")),
    (r"\b(in-?app search history|in-?app search|search (queries|terms) (in app|in-?app))\b",
     ("app_activity", "in-app search history")),
    (r"\binstalled apps?\b", ("app_activity", "installed apps")),
    (r"\b(user[-\s]?generated content(?:s)?|user contents?|user content|ugc|bios?|notes?|open[-\s]?ended responses?)\b",
    ("app_activity", "other user-generated content")),
    (r"\b(gameplay|likes?|dialog options?|other actions?)\b",
     ("app_activity", "other actions")),
    (r"\b(?:in-?app|in-?game)\s+(?:activity|activities|interaction|interactions?)\b",
     ("app_activity", "app interactions")),
    (r"\b(?:user|account|app|game)\s+interactions?\b",
     ("app_activity", "app interactions")),
    (r"\busage (?:data|information|stats|statistics)\b",
     ("app_activity", "other actions")),
    (r"\bsession (?:duration|length|time)\b",
     ("app_activity", "other actions")),
    (r"\btime spent\b",
     ("app_activity", "other actions")),
    (r"\b(?:game|play) time\b",
     ("app_activity", "other actions")),
    (r"\bachievements?\b",
     ("app_activity", "other actions")),
    (r"\bscores?\b",
     ("app_activity", "other actions")),
    (r"\bratings?\b",
     ("app_activity", "other actions")),
    (r"\binteractions?\s+(?:with\s+)?(?:ads?|advertis(?:ing|ers)|our teams|features?)\b",
     ("app_activity", "other actions")),
    (r"\bapp\s+usuage\b", ("app_activity", "app interactions")),
    (r"\bviewing data\b", ("app_activity", "page views and taps")),
    (r"\btime spent(?: on (?:particular )?pages?)?\b", ("app_activity", "page views and taps")),
    (r"\bactivities on the services\b", ("app_activity", "other actions")),
    (r"\binformation about (?:your|their|user) activities?\b", ("app_activity", "app interactions")),
    (r"\bactivities?\s+on\s+(?:the|our)\s+services?\b", ("app_activity", "app interactions")),


    # Web browsing 
    (r"\bbrowser\s+(?:information|info|data)\b", ("web_browsing", "web browsing history")),
    (r"\breferring pages?(?: and urls?)?\b", ("web_browsing", "web browsing history")),
    (r"\blanding pages?\b", ("web_browsing", "web browsing history")),
    (r"\binternet activity\b", ("web_browsing", "web browsing history")),
    (r"\b(?:web\s*)?brows(?:er|ing)\s*(?:history|data|activity|behavio?r)\b",
     ("web_browsing", "web browsing history")),
    (r"\b(?:urls?|links?)\s+(?:visited|viewed|clicked)\b",
     ("web_browsing", "web browsing history")),
    (r"\bweb\s*sites?\s+(?:visited|viewed|accessed)\b",
     ("web_browsing", "web browsing history")),
    (r"\bpages?\s+(?:visited|viewed)\b",
     ("web_browsing", "web browsing history")),
    (r"\bweb browsing history|websites? (a )?user has visited\b",
     ("web_browsing", "web browsing history")),

    # App info & performance
    (r"\bcrash logs?\b", ("app_info_perf", "crash logs")),
    (r"\bcrash data\b", ("app_info_perf", "crash logs")),
    (r"\bcrash reports?\b", ("app_info_perf", "crash logs")),  #
    (r"\bdiagnostics?\b", ("app_info_perf", "diagnostics")),
    (r"\b(performance|telemetry|startup|launch|cpu|memory|ram|heap|battery|latency|throughput|fps|frame rate|locale|language|carrier|oem|model|sdk|os|screen|build)\b",
    ("app_info_perf", "other app performance data")),
    (r"\blog files?\b", ("app_info_perf", "other app performance data")),
    (r"\blog data\b", ("app_info_perf", "other app performance data")),
    (r"\bweb server logs?\b", ("app_info_perf", "other app performance data")),
    (r"\berror logs?\b", ("app_info_perf", "other app performance data")),
    (r"\berror reports?\b", ("app_info_perf", "other app performance data")),  # NEW
    (r"\bwi-?fi strength\b", ("app_info_perf", "other app performance data")),
    (r"\bwi-?fi detection (?:tech|technology)\b", ("app_info_perf", "other app performance data")),
    (r"\bbrowser\s+(?:type|version)\b", ("app_info_perf", "other app performance data")),
    (r"\buser[- ]agent\b", ("app_info_perf", "other app performance data")),
    (r"\bhttp\s*headers?\b|\breferr?er\b", ("app_info_perf", "other app performance data")),

    # Health & Fitness
    (r"\b(health|medical|wellness|medical records|symptoms?)\b", ("health_fitness", "health info")),
    (r"\b(body temperature|temperature readings?)\b", ("health_fitness", "health info")),
    (r"\b(fitness|exercise|physical activity|workout|training)\b", ("health_fitness", "fitness info")),
    (r"\b(steps?|step count)\b", ("health_fitness", "steps")),
    (r"\b(heart rate|bpm)\b", ("health_fitness", "heart rate")),
    (r"\bsleep\b", ("health_fitness", "sleep info")),
    (r"\b(menstrual|period tracking|cycle)\b", ("health_fitness", "menstrual cycle")),
  
]

# Mapping functions
def map_term_to_google(term: str) -> Tuple[str, str, bool]:
    """
    Map a raw policy term to (top_key, subtype, matched_bool).
    If no explicit rule matches, fallback heuristics try to keep it in-scope.
    """
    t = canon(term)
    for pat, out in TERM_TO_SUBTYPE_RULES:
        if re.search(pat, t):
            return out[0], out[1], True

    if re.search(r"\b(name|email address|age|gender|address|phone|profile|username|user id)\b", t):
        return "personal_info", "other personal info", True

    return "app_activity", "other actions", False

def parse_label_sections(label: Dict) -> Dict[str, Dict[str, Set[str]]]:
    """
    Parse a DS label object to:
      {
        "shared":   { top_key: {subtypes...}, ... },
        "collected":{ top_key: {subtypes...}, ... }
      }
    Accept strings/lists/dicts as values.
    """
    out = {"shared": defaultdict(set), "collected": defaultdict(set)}
    label_topcat_map = {
        "personal info": "personal_info",
        "location": "location",
        "financial info": "financial_info",
        "messages": "messages",
        "photos and videos": "photos_videos",
        "audio": "audio",
        "files and docs": "files_docs",
        "calendar": "calendar",
        "contacts": "contacts",
        "app activity": "app_activity",
        "web browsing": "web_browsing",
        "app info and performance": "app_info_perf",
        "device or other ids": "device_or_other_ids",
        "health and fitness": "health_fitness",
    }

    def extract_subtypes(text: str, top_key: str) -> Set[str]:
        t = canon(text)
        declared: Set[str] = set()

        if top_key == "location":
            if any(k in t for k in ["precise", "gps", "latitude", "longitude", "lat long", "coordinate"]):
                declared.add("precise location")
            if any(k in t for k in ["approximate", "country", "city", "region", "state", "zip", "postal", "timezone", "location"]):
                declared.add("approximate location")

        if top_key == "personal_info":
            if "name" in t: declared.add("name")
            if "email address" in t or re.search(r"\bemail addresses?\b", t):
                declared.add("email address")
            if "phone" in t: declared.add("phone number")
            if "address" in t: declared.add("address")
            if "user id" in t or "user ids" in t or "account id" in t or "account number" in t or "account name" in t:
                declared.add("user ids")
            if "race" in t and "ethnic" in t: declared.add("race and ethnicity")
            if "political" in t or "religious" in t: declared.add("political or religious beliefs")
            if "sexual orientation" in t: declared.add("sexual orientation")
            if any(k in t for k in ["dob", "date of birth", "birthday", "gender identity", "veteran", "other info"]):
                declared.add("other personal info")

        if top_key == "device_or_other_ids":
            if any(k in t for k in ["device", "identifier", "ip address", "advertising", "cookie", "gaid", "aaid", "android id", "imei", "imsi", "serial", "mac", "push", "token"]):
                declared.add("device or other ids")

        if top_key == "financial_info":
            if "purchase history" in t: declared.add("purchase history")
            if any(k in t for k in ["payment", "billing", "transaction"]):
                declared.add("user payment info")
            if any(k in t for k in ["credit card", "debit card"]):
                declared.add("credit or debit card number")
            if "credit score" in t: declared.add("credit score")
            if any(k in t for k in ["salary", "debt", "loan", "other financial info"]):
                declared.add("other financial info")

        if top_key == "app_activity":
            if any(k in t for k in ["number of times", "visit a page", "page view", "screen view", "tap", "click", "button press"]):
                declared.add("page views and taps")
                declared.add("app interactions")
            if any(k in t for k in ["app interactions", "interaction", "sections they tap"]):
                declared.add("app interactions")
            if any(k in t for k in ["in-app search", "search history", "search queries", "search terms"]):
                declared.add("in-app search history")
            if "installed apps" in t:
                declared.add("installed apps")
            if any(k in t for k in ["user-generated content", "ugc", "bios", "notes", "open-ended responses"]):
                declared.add("other user-generated content")
            if any(k in t for k in ["gameplay", "likes", "dialog options", "other actions"]):
                declared.add("other actions")

        if top_key == "app_info_perf":
            if "crash" in t: declared.add("crash logs")
            if "diagnostic" in t: declared.add("diagnostics")
            if any(k in t for k in ["performance", "telemetry", "startup", "launch", "cpu", "memory", "battery", "latency", "throughput", "fps", "locale", "language", "carrier", "oem", "model", "sdk", "os", "screen", "build", "log file", "web server log", "error log", "user agent", "http header", "referrer"]):
                declared.add("other app performance data")

        if top_key == "messages":
            if any(k in t for k in ["sms", "mms", "text"]):
                declared.add("sms or mms")
            if "email" in t:
                declared.add("emails")
            if any(k in t for k in ["chat", "instant message", "direct message", "dm", "in-app message"]):
                declared.add("other in-app messages")

        if top_key == "photos_videos":
            if any(k in t for k in ["photo", "image", "picture", "screenshot"]):
                declared.add("photos")
            if "video" in t:
                declared.add("videos")

        if top_key == "audio":
            if any(k in t for k in ["voice", "sound", "recording", "microphone", "audio"]):
                declared.add("other audio files")
            if "music" in t:
                declared.add("music files")
            if re.search(r"\b(voice|sound) recordings?\b", t):
                declared.add("voice or sound recordings")


        if top_key == "files_docs":
            if any(k in t for k in ["file", "document", "pdf", "doc", "sheet", "spreadsheet"]):
                declared.add("files and docs")

        if top_key == "contacts":
            if any(k in t for k in ["contacts", "address book", "phone book", "contact list"]):
                declared.add("contacts")

        if top_key == "calendar":
            if "calendar" in t or "event" in t:
                declared.add("calendar events")

        if top_key == "health_fitness":
            if any(k in t for k in ["health", "medical", "wellness", "symptom", "record"]):
                declared.add("health info")
            if any(k in t for k in ["fitness", "exercise", "physical activity", "workout", "training"]):
                declared.add("fitness info")
            if "steps" in t:
                declared.add("steps")
            if any(k in t for k in ["heart rate", "bpm"]):
                declared.add("heart rate")
            if "sleep" in t:
                declared.add("sleep info")
            if any(k in t for k in ["menstrual", "period", "cycle"]):
                declared.add("menstrual cycle")
        if top_key == "web_browsing":
            if any(k in t for k in [
                "web browsing history",
                "web browsing",
                "browser history",
                "websites visited",
                "sites visited",
                "pages visited",
                "urls visited",
                "links visited",
                "links clicked"
            ]):
                declared.add("web browsing history")


        return declared

    def add_to_out(section_obj, top_label, values):
        top_key = label_topcat_map.get(canon(top_label))
        if not top_key or top_key not in GOOGLE_SCHEMA:
            return
        if isinstance(values, str):
            text = values
        elif isinstance(values, list):
            text = ", ".join(values)
        elif isinstance(values, dict):
            text = ", ".join(str(v) for v in values.values())
        else:
            text = str(values)
        subs = extract_subtypes(text, top_key)
        if subs:
            section_obj[top_key].update(subs)

    for section_key, out_key in [("Data shared", "shared"), ("Data collected", "collected")]:
        sec = label.get(section_key, {})
        if isinstance(sec, dict):
            for top_label, values in sec.items():
                add_to_out(out[out_key], top_label, values)

    return out

def parse_policy_items_with_trace(policy: Dict[str, List[str]]):
    """
    Map policy items to schema with trace:
      returns (mapped, mapped_strings, non_schematized)
    - mapped: {"shared": {top_key: {subtypes...}}, "collected": {...}}
    - mapped_strings: {"shared": set([...]), "collected": set([...])}
    - non_schematized: {"shared": [...], "collected": [...]}
    """
    mapped = {"shared": defaultdict(set), "collected": defaultdict(set)}
    mapped_strings = {"shared": set(), "collected": set()}
    non_schematized = {"shared": [], "collected": []}

    for sect in ["shared", "collected"]:
        for item in policy.get(sect, []) or []:
            top, sub, matched = map_term_to_google(item)
            if matched:
                mapped[sect][top].add(sub)
                mapped_strings[sect].add(item)
            else:
                non_schematized[sect].append(item)

    return mapped, mapped_strings, non_schematized
