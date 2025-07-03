#!/usr/bin/env python3
"""
Interactive Tour Planner
========================
A minimal command-line assistant that suggests places to visit in a given destination.
It relies on the free (but key-protected) OpenTripMap API.

Quick start:
    # export OPENTRIPMAP_API_KEY=<your_key_here>
    python tour_planner.py

Author: OpenAI Assistant
"""
import os
import sys
import textwrap
from typing import Any, Dict, List, Optional

import requests
from tabulate import tabulate

API_BASE = "https://api.opentripmap.com/0.1/en"
API_KEY_ENV = "OPENTRIPMAP_API_KEY"

def require_api_key() -> str:
    key = os.environ.get(API_KEY_ENV)
    if not key:
        print(
            f"\nERROR: This program needs an OpenTripMap API key.\n"
            f"Please obtain a free key from https://opentripmap.io/ and set it via\n"
            f"    export {API_KEY_ENV}=YOUR_KEY\n"
        )
        sys.exit(1)
    return key


def geocode_place(place: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Return dict with lat/lon and other info for the place or None if not found."""
    url = f"{API_BASE}/places/geoname"
    resp = requests.get(url, params={"name": place, "apikey": api_key}, timeout=10)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def fetch_poi_list(lat: float, lon: float, api_key: str, radius: int = 5000, limit: int = 20) -> List[Dict[str, Any]]:
    url = f"{API_BASE}/places/radius"
    params = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "limit": limit,
        "rate": 2,  # quality rating 2+ (0=all, 3=top)
        "apikey": api_key,
        "format": "json"
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_poi_details(xid: str, api_key: str) -> Dict[str, Any]:
    url = f"{API_BASE}/places/xid/{xid}"
    resp = requests.get(url, params={"apikey": api_key}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def truncate(text: str, width: int = 80) -> str:
    return textwrap.shorten(text, width=width, placeholder="…")


def display_places(poi_list: List[Dict[str, Any]]):
    table = []
    for idx, poi in enumerate(poi_list, start=1):
        name = poi.get("name") or "(Unnamed)"
        kinds = truncate(poi.get("kinds", ""), 40)
        dist = int(poi.get("dist", 0))
        table.append([idx, name, kinds, f"{dist} m"])
    headers = ["#", "Place", "Kinds", "Distance"]
    print()
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print()


def interactive_loop():
    api_key = require_api_key()
    print("============================")
    print("  Welcome to Tour Planner!  ")
    print("============================\n")
    while True:
        place = input("Enter a destination city (or 'q' to quit): ").strip()
        if place.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            return
        if not place:
            continue

        geo = geocode_place(place, api_key)
        if geo is None:
            print(f"Sorry, '{place}' not found. Please try another destination.\n")
            continue

        lat = geo["lat"]
        lon = geo["lon"]
        print(f"\nFound {geo['name']} at (lat {lat:.4f}, lon {lon:.4f}).")
        print("Searching for interesting places within 5 km…")

        try:
            pois = fetch_poi_list(lat, lon, api_key)
        except requests.RequestException as e:
            print("Error fetching places:", e)
            continue
        if not pois:
            print("No points of interest found. Try another place?\n")
            continue

        display_places(pois)

        while True:
            sel = input("Enter the # of a place to learn more, 'n' for new place, or 'q' to quit: ").strip()
            if sel.lower() in {"q", "quit", "exit"}:
                print("Goodbye!")
                return
            if sel.lower() == "n":
                break  # ask for new city
            if not sel.isdigit():
                print("Please enter a valid number.")
                continue
            idx = int(sel) - 1
            if not (0 <= idx < len(pois)):
                print("Number out of range.")
                continue

            xid = pois[idx]["xid"]
            try:
                details = fetch_poi_details(xid, api_key)
            except requests.RequestException as e:
                print("Error getting details:", e)
                continue

            name = details.get("name", "(Unnamed)")
            kinds = details.get("kinds", "")
            wiki_extract = details.get("wikipedia_extracts", {}).get("text")
            website = details.get("url")
            print("\n" + "=" * 60)
            print(name)
            print("=" * 60)
            print(f"Kinds: {kinds}")
            if wiki_extract:
                print("\n" + textwrap.fill(wiki_extract, width=80))
            if website:
                print(f"\nMore info: {website}")
            print("=" * 60 + "\n")


def main():
    try:
        interactive_loop()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")


if __name__ == "__main__":
    main()