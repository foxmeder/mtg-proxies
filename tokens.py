import argparse
from pathlib import Path

import sbwsz
import scryfall
from mtgproxies.cli import parse_decklist_spec
from mtgproxies.decklists import Decklist


def get_tokens(decklist: Decklist):
    tokens = {}
    for card in decklist.cards:
        if card["layout"] in ["token", "double_faced_token"]:
            continue

        # Iterate over all prints, as not all have token information associated with them
        for card_print in scryfall.get_cards(oracle_id=card["oracle_id"]):
            if "all_parts" in card_print:
                for related_card in card_print["all_parts"]:
                    if related_card["component"] == "token":
                        # Related cards are only provided by their id.
                        # We need the oracle id to weed out duplicates
                        related = scryfall.get_cards(id=related_card["id"])[0]
                        tokens[related["oracle_id"]] = related

    # Resolve oracle ids to actual cards.
    return [scryfall.recommend_print(token) for token in tokens.values()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append the tokens created by the cards in a decklist to it.")
    parser.add_argument(
        "decklist",
        metavar="decklist_spec",
        help="path to a decklist in text/arena format, or manastack:{manastack_id}, or archidekt:{archidekt_id}",
    )
    parser.add_argument(
        "--format", help="output format (default: %(default)s)", choices=["arena", "text"], default="arena"
    )
    parser.add_argument("--lang", type=str, help="prefer this language", default=None)
    parser.add_argument("--cache_path", type=str, help="path to cache directory", default=None)
    args = parser.parse_args()

    # Set cache path
    if args.cache_path is not None:
        print("Using cache path:", args.cache_path)
        scryfall.set_cache_path(args.cache_path)
        sbwsz.set_cache_path(args.cache_path)

    # Set preferred language
    if args.lang is not None:
        print("Preferring language:", args.lang)
        scryfall.set_prefer_lang(args.lang)

    # Parse decklist
    decklist = parse_decklist_spec(args.decklist, warn_levels=["ERROR", "WARNING"])

    # Find tokens
    tokens = get_tokens(decklist)
    print(f"Found {len(tokens)} created tokens.")

    # Append tokens
    decklist.append_comment("")
    decklist.append_comment("Tokens")
    for token in tokens:
        decklist.append_card(1, token)

    # Write decklist
    out_file = args.decklist if Path(args.decklist).is_file() else f"{args.decklist.split(':')[-1]}.txt"
    decklist.save(out_file, fmt=args.format)

    print(f"Successfully appended to {Path(out_file).resolve()}.")
