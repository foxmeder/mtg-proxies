import argparse

import numpy as np

import localfile
import scryfall
from mtgproxies import fetch_scans_scryfall, print_cards_fpdf, print_cards_matplotlib
from mtgproxies.cli import parse_decklist_spec


def papersize(string: str) -> np.ndarray:
    spec = string.lower()
    if spec == "a4":
        return np.array([21, 29.7]) / 2.54
    if "x" in spec:
        split = spec.split("x")
        return np.array([float(split[0]), float(split[1])])
    raise argparse.ArgumentTypeError()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare a decklist for printing.")
    parser.add_argument(
        "decklist",
        metavar="decklist_spec",
        help="path to a decklist in text/arena format, or manastack:{manastack_id}, or archidekt:{archidekt_id}",
    )
    parser.add_argument("outfile", help="output file. Supports pdf, png and jpg.")
    parser.add_argument("--dpi", help="dpi of output file (default: %(default)d)", type=int, default=300)
    parser.add_argument(
        "--paper",
        help="paper size in inches or preconfigured format (default: %(default)s)",
        type=papersize,
        default="a4",
        metavar="WIDTHxHEIGHT",
    )
    parser.add_argument(
        "--scale",
        help="scaling factor for printed cards (default: %(default)s)",
        type=float,
        default=1.0,
        metavar="FLOAT",
    )
    parser.add_argument(
        "--border_crop",
        help="how much to crop inner borders of printed cards (default: %(default)s)",
        type=int,
        default=14,
        metavar="PIXELS",
    )
    parser.add_argument(
        "--background",
        help='background color, either by name or by hex code (e.g. black or "#ff0000", default: %(default)s)',
        type=str,
        default=None,
        metavar="COLOR",
    )
    parser.add_argument("--cropmarks", action=argparse.BooleanOptionalAction, default=True, help="add crop marks")
    parser.add_argument(
        "--faces",
        help="which faces to print (default: %(default)s)",
        choices=["all", "front", "back"],
        default="all",
    )
    parser.add_argument("--local_scan_path", type=str, help="path to local scan cache", default=None)
    parser.add_argument("--lang", type=str, help="prefer this language", default=None)
    parser.add_argument("--cache_path", type=str, help="path to cache directory", default=None)
    parser.add_argument(
        "--card_space", help="space between cards (default: %(default)s)", type=int, default=0, metavar="PIXELS"
    )
    args = parser.parse_args()

    # Set cache path
    if args.cache_path is not None:
        print("Using cache path:", args.cache_path)
        scryfall.set_cache_path(args.cache_path)

    # Set local scan path
    if args.local_scan_path is not None:
        print("Using local scan path:", args.local_scan_path)
        localfile.set_local_scan_path(args.local_scan_path)

    # Set preferred language
    if args.lang is not None:
        print("Preferring language:", args.lang)
        scryfall.set_prefer_lang(args.lang)

    # Parse decklist
    decklist = parse_decklist_spec(args.decklist)

    # Fetch scans
    images = fetch_scans_scryfall(decklist, faces=args.faces)

    # Plot cards
    if args.outfile.endswith(".pdf"):
        import matplotlib.colors as colors

        background_color = args.background
        if background_color is not None:
            background_color = (np.array(colors.to_rgb(background_color)) * 255).astype(int)

        print_cards_fpdf(
            images,
            args.outfile,
            papersize=args.paper * 25.4,
            cardsize=np.array([2.5, 3.5]) * 25.4 * args.scale,
            border_crop=args.border_crop,
            background_color=background_color,
            cropmarks=args.cropmarks,
            card_space=args.card_space,
        )
    else:
        print_cards_matplotlib(
            images,
            args.outfile,
            papersize=args.paper,
            cardsize=np.array([2.5, 3.5]) * args.scale,
            dpi=args.dpi,
            border_crop=args.border_crop,
            background_color=args.background,
        )
