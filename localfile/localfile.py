from __future__ import annotations

import re

"""Simple interface to the local card scan."""

from pathlib import Path

from mtgproxies.decklists import Card, Decklist

local_scan_path = None


def set_local_scan_path(path: str):
    global local_scan_path
    local_scan_path = path.split(",")


def recommend_print(card: Card, mode="best"):
    global local_scan_path
    if local_scan_path is None:
        return card
    found = recommend_local_scan(card, mode)
    if not found:
        return card
    # Sort by mtime and take the newest one
    # images.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    # largest_image = max(images, key=lambda x: x.stat().st_size)

    print(f"Using local scan {found} for {card['name']}")
    card.proxy_local_scan = found
    return card


def recommend_local_scan(card: Card, mode="best") -> Path | None:
    global local_scan_path
    image_extensions = [".jpg", ".jpeg", ".png"]

    # find all image files whose filename contains card_name in local_scan_path
    img_paths = card_img_path(card)
    local_paths = [Path(p) for p in local_scan_path]

    for p in local_paths:
        for card_path in img_paths:
            for file in p.glob(card_path, case_sensitive=False):
                if file.suffix.lower() in image_extensions:
                    return file
    return None


def card_img_path(card) -> list[str]:
    # format card name
    card_name = local_card_name(card["name"])
    other_card_name = card["name"].replace("æ", "ae").replace("í", "i").replace("á", "a").replace("û", "u")
    img_path = []
    if card["set"]:
        if "collector_number" in card:
            img_path += [
                f'{card["set"]}/{card["name"]}.{card["collector_number"]}.*',
                f'{card["set"]}/{other_card_name}.{card["collector_number"]}.*',
                f'{card["set"]}/*{card["set"]}-{card["collector_number"]}-{card["name"]}.*',
                f'{card["set"]}/*{card["set"]}-{card["collector_number"]}-{other_card_name}.*',
                f'{card["set"]}/*{card["set"]}-{card["collector_number"]}-{card_name}.*',
            ]
        img_path += [
            f'{card["set"]}/{card["name"]}.*',
            f'{card["set"]}/{other_card_name}.*',
            # f'{card["set"]}/{card_name}.*',
            f'{card["set"]}/*-{card_name}.*',
            f'{card["set"]}/*-{card["name"]}.*',
            f'{card["set"]}/*-{other_card_name}.*',
        ]
    if "layout" in card and card["layout"] == "token":
        img_path += [f"TOK/{card["set"]}/{card["name"]}.*"]
    return img_path


def local_card_name(card_name: str) -> str:
    card_name = card_name.split("//")[0].strip()
    card_name = card_name.replace("æ", "ae").replace("í", "i").replace("á", "a").replace("û", "u")
    return "-".join([s for s in re.split(r",|'|\s|:|\.|/", card_name.lower()) if s.strip()])


def parse_local_dir(p: str | Path) -> tuple[Decklist, bool, list]:
    # list all images in p recursively
    print(f"Parsing local dir: {p}")
    p = Path(p)
    return (
        Decklist(
            [
                Card(1, card={"name": file.stem}, proxy_local_scan=file)
                for file in list(p.rglob("*.jpg", case_sensitive=False)) + list(p.rglob("*.png", case_sensitive=False))
                if file.is_file()
            ],
            p.stem,
        ),
        True,
        [],
    )
