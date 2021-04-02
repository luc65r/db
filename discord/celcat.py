import arrow
from config import cfg
import html
import json
import re
import requests
from urllib.parse import parse_qs

class Course:
    def __init__(self, data):
        self.uid = data['id']
        self.start = arrow.get(data['start'], tzinfo='Europe/Paris')
        self.end = arrow.get(data['end'], tzinfo='Europe/Paris')
        self.category = data['eventCategory']
        d = [html.unescape(s) for s in data['description'].split('\r\n') if s]
        self.name = d[2]
        self.location = d[4] if len(d) > 4 else None
        self.prof = d[6].replace('<br />', ', ') if len(d) > 6 else None

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    def __str__(self):
        s = (
            f'{self.start.format("dddd D MMMM YYYY", locale="fr").capitalize()}\n'
            f'{self.start.format("H:mm", locale="fr")} - '
            f'{self.end.format("H:mm", locale="fr")}\n'
            f'{self.category} {self.name}'
        )
        if self.location is not None:
            s += f'\n{self.location}'
        if self.prof is not None:
            s += f'\n{self.prof}'
        return s

class Calendar:
    def __init__(self, start=None, end=None):
        self.start = arrow.now() if start is None else start
        self.end = self.start.shift(weeks=+1) if end is None else end
        self.courses = []

    def fetch(self):
        s = requests.Session()
        rlt = s.get("https://services-web.u-cergy.fr/calendar/LdapLogin")
        rvt = re.search(
            '<input name="__RequestVerificationToken".*?value="([^"]+)"',
            str(rlt.content),
        ).group(1)
        rlogin = s.post("https://services-web.u-cergy.fr/calendar/LdapLogin/Logon", data = {
            'Name': cfg['celcat']['name'],
            'Password': cfg['celcat']['password'],
            '__RequestVerificationToken': rvt,
        })
        fid = parse_qs(rlogin.url)['FederationIds'][0]
        rcd = s.post("https://services-web.u-cergy.fr/calendar/Home/GetCalendarData", data = {
            'start': self.start.format('YYYY-MM-DD'),
            'end': self.end.format('YYYY-MM-DD'),
            'resType': '104',
            'calView': 'month',
            'federationIds[]': fid,
        })
        calData = json.loads(rcd.content)
        for d in calData:
            try:
                self.courses.append(Course(d))
            except:
                pass
        self.courses.sort()

    def next_course(self):
        now = arrow.now()
        for c in self.courses:
            if c.start > now:
                return c

        return None