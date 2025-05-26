from typing import Dict, Any, List
from contextlib import redirect_stdout

from app.grafana.client import grafana_client

try:
    with open('system_prompt.txt', 'r', encoding='utf-8') as file:
        system_prompt = file.read()
except FileNotFoundError:
    print("Файл system_prompt.txt не найден")
    system_prompt = ""

try:
    with open('user_prompt.txt', 'r', encoding='utf-8') as file:
        user_prompt = file.read()
except FileNotFoundError:
    print("Файл user_prompt.txt не найден")
    user_prompt = ""


def extract_uid_and_type(datasources: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    return [
        {"uid": ds["uid"], "type": ds["type"]}
        for ds in datasources
        if "uid" in ds and "type" in ds
    ]


def extract_servers_and_jobs(targets_data: dict) -> List[Dict[str, str]]:
    extracted_data = []

    for target in targets_data.get("data", {}).get("activeTargets", []):
        address = target.get("discoveredLabels", {}).get("__address__", "")
        ip = address.split(":")[0] if address else "unknown"

        job = target.get("labels", {}).get("job", "unknown")

        extracted_data.append({"ip": ip, "job": job})

    return extracted_data


with open('context.txt', 'w', encoding='utf-8') as f, redirect_stdout(f):
    datasources = grafana_client.get(endpoint='/api/datasources')

    datasource_info = extract_uid_and_type(datasources)

    print("У меня развёрнута IT-инфраструктура, которую мониторит Grafana с помощью нескольких источников данных"
          " (UID и Type):")
    for idx, ds in enumerate(datasource_info, 1):
        print(f"{idx}. UID: {ds['uid']}, Type: {ds['type']}")
        if ds['type'] == 'prometheus':
            prometheus_datasource_id = ds['uid']

    targets = grafana_client.get(endpoint=f'/api/datasources/proxy/uid/{prometheus_datasource_id}/api/v1/targets')

    servers_info = extract_servers_and_jobs(targets)

    print("\nВот список серверов, поставленных на мониторинг, и их Jobs:")
    for idx, server in enumerate(servers_info, 1):
        print(f"{idx}. IP: {server['ip']}, Job: {server['job']}")


print("Отчет сохранен в context.txt")
