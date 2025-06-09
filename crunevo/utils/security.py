import os
from typing import Tuple, Optional

import requests
from user_agents import parse


def get_geo_location(ip: str) -> Tuple[Optional[str], Optional[str]]:
    """Retrieve country and city using ip-api.com if USE_GEOIP is enabled."""
    if not ip or os.getenv("USE_GEOIP", "0") != "1":
        return None, None
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=1)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("country"), data.get("city")
    except Exception:
        pass
    return None, None


def parse_device(user_agent: str) -> str:
    ua = parse(user_agent or "")
    if ua.is_mobile:
        return "Mobile"
    if ua.is_tablet:
        return "Tablet"
    return "PC"
