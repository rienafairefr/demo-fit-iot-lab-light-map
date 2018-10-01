#!/usr/bin/env python
import random
from math import sqrt, inf

from iotlabcli import auth, rest, experiment

user, passwd = auth.get_user_credentials()
api = rest.Api(user, passwd)

number_nodes = 64

nodes = experiment.info_experiment(api, site='lille', archi='m3', state='Alive')['items']
for node in list(nodes):
    try:
        node['x'] = float(node['x'])
        node['y'] = float(node['y'])
        node['z'] = float(node['z'])
    except ValueError:
        nodes.remove(node)

node_idx = random.randint(0, len(nodes)-1)
selected_nodes = [nodes.pop(node_idx)]


def dist(node1, node2):
    return sqrt(pow(node1['x'] - node2['x'],2)\
                + pow(node1['y'] - node2['y'], 2)\
                + pow(node1['z'] - node2['z'], 2))


while len(selected_nodes) < number_nodes:
    distances = []
    for node in nodes:
        sum_dist = 0
        for selected_node in selected_nodes:
            sum_dist += dist(node, selected_node)
        distances.append(sum_dist)

    dist_max = max(distances)
    idx_node = distances.index(dist_max)
    node = nodes.pop(idx_node)
    selected_nodes.append(node)
    print('%d selected nodes ...' % len(selected_nodes))

min_dists = []
for node1 in selected_nodes:
    min_dist = inf
    for node2 in selected_nodes:
        if node1 == node2:
            continue
        dist12 = dist(node1, node2)
        if dist12 < min_dist:
            min_dist = dist12

    min_dists.append(min_dist)

print('Max distance to nearest neighboar %f m' % max(min_dists))

select_str = '+'.join(node['network_address'].split('.lille')[0][3:] for node in selected_nodes)

print('selection:')
print(select_str)
