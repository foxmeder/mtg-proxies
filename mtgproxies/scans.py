from __future__ import annotations

from typing import Literal

from tqdm import tqdm

import localfile
import scryfall
from mtgproxies.decklists.decklist import Decklist


def fetch_scans_scryfall(decklist: Decklist, faces: Literal["all", "front", "back"] = "all") -> list[str]:
    """Search Scryfall for scans of a decklist.

    Args:
        decklist: The decklist to fetch scans for
        faces: Which faces to fetch ("all", "front", "back")

    Returns:
        List: List of image files
    """
    return [
        scan
        for card in tqdm(decklist.cards, desc="Fetching artwork")
        for card in [localfile.recommend_print(card)]
        for i, image_uri in enumerate(card.image_uris)
        for scan in [
            (
                scryfall.get_image(image_uri["png"], silent=True)
                if image_uri["png"].startswith("http")
                else image_uri["png"]
            )
        ]
        * card.count
        if faces == "all" or (faces == "front" and i == 0) or (faces == "back" and i > 0)
    ]
