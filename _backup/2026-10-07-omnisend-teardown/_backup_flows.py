"""Backup of all ENABLED Insane Fits automations + forms (full JSON + email content).

Read-only against Omnisend. Writes to a local folder for GitHub push.
"""
import os, time, urllib.request, urllib.error, json

for line_ in open('/workspace/.env'):
    if line_.strip() and not line_.startswith('#'):
        k, _, v = line_.strip().partition('=')
        os.environ[k] = v.strip().strip('"').strip("'")

hdrs = {'X-API-KEY': os.environ['OMNISEND_API_KEY_INSANEFITS'],
        'Omnisend-Version': '2026-03-15'}
BASE = 'https://api.omnisend.com/api'
OUT = '/workspace/clients/insanefits/_backup/2026-10-07-omnisend-teardown'


def get(path):
    for _ in range(6):
        try:
            r = urllib.request.Request(BASE + path, headers=hdrs)
            return json.loads(urllib.request.urlopen(r, timeout=60).read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(9)
                continue
            raise


def safe(s):
    return ''.join(c if c.isalnum() or c in '-_' else '-' for c in (s or '')).strip('-')[:50]


def content_ids(blocks, acc):
    for b in blocks or []:
        if b.get('type') == 'action':
            se = (b.get('action') or {}).get('sendEmail') or {}
            if se.get('contentID'):
                acc.append((se['contentID'], se.get('subject')))
        elif b.get('type') == 'abTesting':
            ab = b.get('abTesting') or {}
            content_ids(ab.get('aBlocks'), acc)
            content_ids(ab.get('bBlocks'), acc)
    return acc


os.makedirs(OUT, exist_ok=True)
manifest = {'exportedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'brand': 'insanefits', 'automations': [], 'forms': []}

autos = get('/automations?limit=100')['automations']
json.dump(autos, open(OUT + '/_automations-list-all15.json', 'w'), ensure_ascii=False, indent=1)

for a in autos:
    if not a.get('isEnabled'):
        continue
    full = get('/automations/' + a['id'])
    d = OUT + '/automations/' + a['id'] + '-' + safe(a['name'])
    os.makedirs(d, exist_ok=True)
    json.dump(full, open(d + '/automation.json', 'w'), ensure_ascii=False, indent=1)
    emails = []
    for cid, subj in content_ids(full.get('blocks'), []):
        c = get('/email-content/' + cid)
        json.dump(c, open(d + '/content-' + cid + '.json', 'w'), ensure_ascii=False, indent=1)
        html = []
        for sec in c.get('sections') or []:
            for row in sec.get('rows') or []:
                for col in row.get('columns') or []:
                    for blk in col.get('blocks') or []:
                        if blk.get('type') == 'html':
                            h = blk.get('html')
                            html.append(h if isinstance(h, str) else ((h or {}).get('htmlCode') or ''))
        if html:
            open(d + '/content-' + cid + '.html', 'w').write('\n<!-- block -->\n'.join(html))
        emails.append({'contentID': cid, 'subject': subj, 'htmlBlocks': len(html)})
        time.sleep(0.4)
    manifest['automations'].append({'id': a['id'], 'name': a['name'],
                                    'trigger': ((full.get('trigger') or {}).get('condition') or {}).get('event'),
                                    'emails': emails})
    print('OK automation', a['name'], len(emails), 'emails')

forms = get('/forms?limit=100')['forms']
json.dump(forms, open(OUT + '/_forms-list-all.json', 'w'), ensure_ascii=False, indent=1)
os.makedirs(OUT + '/forms', exist_ok=True)
for f in forms:
    json.dump(f, open(OUT + '/forms/' + f['id'] + '-' + safe(f['name']) + '.json', 'w'),
              ensure_ascii=False, indent=1)
    manifest['forms'].append({'id': f['id'], 'name': f['name'], 'status': f['status']})
    print('OK form', f['status'], f['name'])

json.dump(manifest, open(OUT + '/MANIFEST.json', 'w'), ensure_ascii=False, indent=1)
print('\nmanifest ->', OUT + '/MANIFEST.json')
