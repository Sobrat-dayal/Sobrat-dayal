"""Refresh local GitHub profile graphics. Python standard library only."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from datetime import date, datetime, timezone
from urllib.request import Request, urlopen
import json
import os

USER = 'Sobrat-Dayal'
ROOT = Path(__file__).resolve().parents[1]

def fetch(url, api=False):
    headers = {'User-Agent': 'Sobrat-Dayal-profile-readme'}
    if api:
        headers['Accept'] = 'application/vnd.github+json'
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return response.read().decode('utf-8')

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-date' in attrs and 'data-level' in attrs:
            day = date.fromisoformat(attrs['data-date'])
            level = int(attrs['data-level'])
            if level not in range(5):
                raise ValueError('Unexpected contribution intensity')
            self.days[day] = level

def text(x, y, content, size=16, color='#b6c5dc', weight='400'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(content))}</text>'

def svg(body, height, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-label="{escape(label)}"><rect x=".5" y=".5" width="959" height="{height-1}" rx="16" fill="#10192b" stroke="#30405c"/>{body}</svg>\n'

def main():
    profile = json.loads(fetch(f'https://api.github.com/users/{USER}', True))
    if profile['login'].lower() != USER.lower():
        raise ValueError('Unexpected account')
    repos = []
    page = 1
    while True:
        batch = json.loads(fetch(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}', True))
        if not isinstance(batch, list):
            raise ValueError('Unexpected repositories response')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    calendar = Calendar()
    calendar.feed(fetch(f'https://github.com/users/{USER}/contributions'))
    days = sorted(calendar.days)
    if len(days) < 300 or (days[-1] - days[0]).days < 300:
        raise ValueError('Incomplete calendar; preserving previous graphics')
    if (datetime.now(timezone.utc).date() - days[-1]).days > 3:
        raise ValueError('Stale calendar; preserving previous graphics')
    updated = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    owned = [r for r in repos if not r['fork']]
    values = [(len(repos), 'Public repositories'), (len(owned), 'Non-fork repositories'),
              (sum(r['stargazers_count'] for r in owned), 'Stars · non-fork repos'), (profile['followers'], 'Followers')]
    body = text(28, 39, 'GITHUB / PUBLIC SNAPSHOT', 15, '#69e2df', '700')
    for i, (value, label) in enumerate(values):
        x = 28 + i * 233
        body += text(x, 104, value, 40, '#f2f6ff', '700') + text(x, 135, label, 14)
    body += text(28, 179, f'GitHub API · Updated {updated}', 12, '#90a2bd')
    stats = svg(body, 202, 'Verified public GitHub statistics for Sobrat Dayal')

    body = text(28, 39, 'CONTRIBUTIONS / THE LAST YEAR', 15, '#69e2df', '700')
    body += text(28, 64, f'{days[0].isoformat()} — {days[-1].isoformat()}', 12)
    colors = ['#1b2940', '#1b5861', '#268b91', '#42b9bb', '#79ebe0']
    start_ordinal = days[0].toordinal() - ((days[0].weekday() + 1) % 7)
    for day in days:
        n = day.toordinal() - start_ordinal
        x, y = 28 + (n // 7) * 17, 87 + (n % 7) * 17
        level = calendar.days[day]
        body += f'<rect x="{x}" y="{y}" width="13" height="13" rx="3" fill="{colors[level]}"><title>{day.isoformat()} · GitHub intensity level {level} of 4</title></rect>'
    body += text(28, 238, f'GitHub public calendar · Updated {updated}', 12, '#90a2bd')
    body += text(728, 238, 'Less', 12)
    for i, color in enumerate(colors):
        body += f'<rect x="{764+i*18}" y="226" width="13" height="13" rx="3" fill="{color}"/>'
    body += text(865, 238, 'More', 12)
    contributions = svg(body, 263, 'Public GitHub contribution intensity calendar for Sobrat Dayal')
    for filename, content in [('stats.svg', stats), ('contributions.svg', contributions)]:
        target = ROOT / 'assets' / filename
        temporary = target.with_suffix('.tmp')
        temporary.write_text(content, encoding='utf-8')
        temporary.replace(target)
    print(f'Refreshed {len(repos)} repositories and {len(days)} calendar days from GitHub ({updated}).')

if __name__ == '__main__':
    main()
