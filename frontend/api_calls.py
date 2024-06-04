import os
import requests
import logging
from datetime import datetime
from typing import List, Dict

API_ADDRESS = os.getenv("API_ADDRESS", "http://127.0.0.1")
API_PORT = os.getenv("API_PORT", ":8000" )


def get_peer_status(peer_name: str) -> str:
    data = {"peer_name": peer_name}
    resp = requests.post(API_ADDRESS + API_PORT +
                         "/get_peer_status/", json=data)
    resp = resp.json()

    floor2 = ('et', 'si', 'ev')
    floor3 = ('ge', 'pr', 'va', 'un')
    fullnames = {
        'et': 'Eternity',
        'si': 'Singularity',
        'ev': 'Evolution',
        'ge': 'Genom',
        'pr': 'Progress',
        'va': 'Vault',
        'un': 'Universe'
    }
    peer_row = ""

    peer_info = resp.get('peers').get(peer_name)
    cluster = peer_info.get('cluster', '')

    peer_row = f"<code>{peer_name}</code> | "\
        f"<i>"\
        f"{fullnames.get(cluster, '')} "\
        f"{cluster}-{peer_info.get('row', '')}{peer_info.get('col', '')}, "\
        f"{'Floor 2' if cluster in floor2 else 'Floor 3' if cluster in floor3 else ''}"\
        f"</i>\n"

    return peer_row


def get_friends(tg_id: int) -> List[str]:
    friends: List[str] = []
    data = {"tg_id": tg_id}
    resp = requests.post(API_ADDRESS + API_PORT +
                         "/get_friends_status/", json=data)
    resp = resp.json()
    peers = resp['peers']
    for peer in peers:
        friends.append(peer)

    friends.sort()
    return friends


def add_friend(tg_id: int, peer_name: str) -> str:
    data = {"tg_id": tg_id, "peer_name": peer_name}
    resp = requests.post(API_ADDRESS + API_PORT + "/add_friend/", json=data)


def delete_friend(tg_id: int, peer_name: str) -> List:
    data = {"tg_id": tg_id, "peer_name": peer_name}
    resp = requests.post(API_ADDRESS + API_PORT + "/delete_friend/", json=data)


def get_friends_status(tg_id: int) -> str:
    answer: str = ""
    data = {"tg_id": tg_id}
    resp = requests.post(API_ADDRESS + API_PORT +
                         "/get_friends_status/", json=data)
    resp = resp.json()
    peers = resp['peers']
    online_peers_list = []
    offline_peers_list = []
    for peer in peers:
        if peers.get(peer).get('status') == 0:
            offline_peers_list.append(peer)
        else:
            online_peers_list.append(peer)

    offline_peers_list.sort()
    online_peers_list.sort()
    new_line = '\n'
    answer = f"{f'<b>Peers online:</b>{new_line}' if len(online_peers_list) > 0 else ''}"\
        f"{pretty_peers_print(online_peers_list, peers, 1)}"\
        f"{f'<b>Peers offline:</b>{new_line}' if len(offline_peers_list) > 0 else ''}"\
        f"{pretty_peers_print(offline_peers_list, peers, 0)}"

    return answer


def pretty_peers_print(peers_list: List[str], info: Dict[str, str], is_online: int) -> str:
    answer = ""
    floor2 = ('et', 'si', 'ev')
    floor3 = ('ge', 'pr', 'va', 'un')
    fullnames = {
        'et': 'Eternity',
        'si': 'Singularity',
        'ev': 'Evolution',
        'ge': 'Genom',
        'pr': 'Progress',
        'va': 'Vault',
        'un': 'Universe'
    }

    for peer in peers_list:
        peer_info = info.get(peer)
        cluster = peer_info.get('cluster', '')
        peer_row = f"<code>{peer}</code> | "\
            f"<i>"\
            f"{fullnames.get(cluster, '')} "\
            f"{cluster}-{peer_info.get('row', '')}{peer_info.get('col', '')}, "\
            f"{'Floor 2' if cluster in floor2 else 'Floor 3' if cluster in floor3 else ''}"\
            f"</i>\n"
        if is_online == 0:
            time = datetime.fromisoformat(
                peer_info.get('time', '').replace('Z', ''))
            strtime = time.strftime('%Y-%m-%d %H:%M')
            peer_row += strtime
            peer_row += '\n'
        answer += peer_row

    return answer