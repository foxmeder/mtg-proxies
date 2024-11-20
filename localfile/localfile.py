from __future__ import annotations

import re

"""Simple interface to the local card scan."""

from pathlib import Path

local_scan_path = None


def set_local_scan_path(path: str):
    global local_scan_path
    local_scan_path = path.split(",")


def recommend_print(card, mode="best"):
    global local_scan_path
    if local_scan_path is None:
        return card

    image_extensions = [".jpg", ".jpeg", ".png"]

    # find all image files whose filename contains card_name in local_scan_path
    img_paths = card_img_path(card)
    founds = [
        file
        for path in [Path(p) for p in local_scan_path]
        for card_path in img_paths
        for file in path.glob(card_path, case_sensitive=False)
    ]

    images = [file for file in founds if file.suffix in image_extensions]
    if len(images) == 0:
        return card
    # Sort by mtime and take the newest one
    images.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    # largest_image = max(images, key=lambda x: x.stat().st_size)

    print(f'Found {len(images)} local scan for {card["name"]}')
    print(f"Using {images[0]} for {card['name']}")
    if "image_uris" in card:
        card["image_uris"]["png"] = str(images[0])
    else:
        card["image_uris"] = {"png": str(images[0])}
    return card


def card_img_path(card) -> list[str]:
    if "layout" in card and card["layout"] == "token":
        return [f"TOK/*/{card["name"]}.*"]
    # format card name
    card_name = "-".join([s for s in re.split(r",|'|\s", card["name"].lower()) if s.strip()])
    img_path = []
    if card["set"]:
        img_path = [
            f'{card["set"]}/*{card_name}.*',
            f'{card["set"]}/{card["name"]}.full.*',
            f'{card["set"]}/{card["name"]}[1-9].full.*',
        ]
        if "collector_number" in card:
            img_path += [f'{card["set"]}/{card["name"]}.{card["collector_number"]}.full.*']
    return img_path + [
        f"*{card_name}.*",
        f'{card["name"]}.full.*',
    ]
