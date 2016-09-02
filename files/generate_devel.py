#!/usr/bin/python
import yaml
import glob

devel = yaml.load(open("host-devel.yml.tpl"))[0]

for filename in glob.glob('host-service*.yml'):
    desc = yaml.load(open(filename))[0]
    for role in desc['roles']:
        if role['role'] == 'jail':
            devel['roles'].append(role)

with open("host-devel.yml", 'w') as f:
    yaml.dump([devel], f, default_flow_style=False)

local = yaml.load(open("local.yml"))
devel = []
hosts = []
for play in local:
    if 'include' not in play:
        continue
    if play['include'] == 'track-config.yml':
        continue
    if play['include'].startswith('host'):
        continue
    if play['include'].startswith('vm'):
        continue
    playbook = yaml.load(open(play['include']))
    # remove local connection from jail config
    for i in playbook:
        if 'connection' in i:
            del i['connection']
        if 'hosts' in i:
            hosts.append(i['hosts'])
    devel.extend(playbook)

with open("devel.yml", 'w') as f:
    yaml.dump(devel, f, default_flow_style=False)

with open("devel", 'w') as f:
    f.write("\n".join(hosts))
