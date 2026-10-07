"""Insane Fits teardown 2026-10-07 per Lukas.

Deletes the 7 ENABLED automations and the live 10% popup (MOBILE + DESKTOP).
Backup already on GitHub: elaiskai/insanefits-email-assets @9aaf0647
  _backup/2026-10-07-omnisend-teardown/

Leaves untouched: 8 disabled automations, Branded Email capture (embedded),
Black friday email form (landingPage), Main pop-up + Insanefits 10% popup (already
disabled), Signup box No.1 (draft), all campaigns/drafts, segments, contacts.
"""
import os, json, time, urllib.request, urllib.error

for line_ in open('/workspace/.env'):
    if line_.strip() and not line_.startswith('#'):
        k, _, v = line_.strip().partition('=')
        os.environ[k] = v.strip().strip('"').strip("'")

hdrs = {'X-API-KEY': os.environ['OMNISEND_API_KEY_INSANEFITS'],
        'Omnisend-Version': '2026-03-15', 'Content-Type': 'application/json'}
BASE = 'https://api.omnisend.com/api'
LOG = []


def call(path, method, body=None):
    data = json.dumps(body).encode() if body is not None else None
    for _ in range(5):
        r = urllib.request.Request(BASE + path, data=data, headers=hdrs, method=method)
        try:
            resp = urllib.request.urlopen(r, timeout=60)
            return resp.status, resp.read().decode()[:200]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(9)
                continue
            return e.code, e.read().decode()[:300]


# ascending revenue impact first, so any surprise shows up on the cheap ones
AUTOMATIONS = [
    ('6a212aec5e898a73f9a36e49', 'Product Reviews'),
    ('6abcd88b2c2ab323fbfa0710', '[IF] Nupirko proteina -> receptu knyga'),
    ('66d585db069079e2f07b3424', 'Customer Reactivation'),
    ('6a2137f38305508380599481', 'Abandoned Cart Trigger'),
    ('6a212c84de553f01826b7d26', 'Product Abandonment Engagement Split'),
    ('64e86ff13f32f55d16ae2d3d', 'Abandoned Checkout Trigger'),
    ('6a20877a8ac35d6deb9dc574', '[IF] Welcome serija (eLaiskai 2026-06)'),
]
FORMS = [
    ('6a2139701a67df459ff5b39c', '10% Popup MOBILE'),
    ('6a21394afb74517726d259a2', '10% Popup DESKTOP'),
]

print('=== AUTOMATIONS ===')
for aid, name in AUTOMATIONS:
    s, b = call('/automations/' + aid, 'DELETE')
    if s == 409:
        print('  409 -> disable first:', name, b[:120])
        s2, b2 = call('/automations/' + aid + '/disable', 'POST', {'contactsInWorkflow': 'exit'})
        print('    disable ->', s2, b2[:80])
        s, b = call('/automations/' + aid, 'DELETE')
    print(' ', s, name, b[:120])
    LOG.append({'type': 'automation', 'id': aid, 'name': name, 'status': s, 'body': b})
    time.sleep(0.5)

print('\n=== FORMS (disable, then delete) ===')
for fid, name in FORMS:
    s1, b1 = call('/forms/' + fid + '/disable', 'POST', {})
    print('  disable ->', s1, name, b1[:80])
    s2, b2 = call('/forms/' + fid, 'DELETE')
    print('  delete  ->', s2, name, b2[:120])
    LOG.append({'type': 'form', 'id': fid, 'name': name,
                'disable': s1, 'delete': s2, 'body': (b1 + ' | ' + b2)[:200]})
    time.sleep(0.5)

print('\n=== VERIFY ===')
d = json.loads(urllib.request.urlopen(urllib.request.Request(
    BASE + '/automations?limit=100', headers=hdrs), timeout=30).read())
left = d['automations']
print('automations remaining:', len(left), '| enabled:', sum(1 for a in left if a['isEnabled']))
for a in left:
    print('   ', 'ON ' if a['isEnabled'] else 'off', a['id'], a['name'])

f = json.loads(urllib.request.urlopen(urllib.request.Request(
    BASE + '/forms?limit=100', headers=hdrs), timeout=30).read())
print('\nforms remaining:', len(f['forms']))
for x in f['forms']:
    print('   ', x['status'], '|', x.get('displayType'), '|', x['name'])

json.dump(LOG, open('/workspace/clients/insanefits/_teardown_1007_log.json', 'w'),
          ensure_ascii=False, indent=1)
