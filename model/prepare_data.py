"""Organize the Kaggle "Hot Dog - Not Hot Dog" dataset into our layout.

Kaggle ships `hot_dog`/`not_hot_dog` under `train`/`test`. Our training code expects
`yes`/`no` under `train`/`validation`. This maps one onto the other and verifies the result.

    python model/prepare_data.py --source model/data/seefood   # reorganize the download
    python model/prepare_data.py --verify                      # count what's there
"""

import argparse
import shutil
from pathlib import Path

MODEL_DIR = Path(__file__).resolve().parent
DATA_DIR = MODEL_DIR / "data"

TARGET_DIRS = {
    ("train", "yes"): DATA_DIR / "train" / "yes",
    ("train", "no"): DATA_DIR / "train" / "no",
    ("validation", "yes"): DATA_DIR / "validation" / "yes",
    ("validation", "no"): DATA_DIR / "validation" / "no",
}

# (kaggle_split, kaggle_class) -> (our_split, our_class)
KAGGLE_TO_TARGET = {
    ("train", "hot_dog"): ("train", "yes"),
    ("train", "not_hot_dog"): ("train", "no"),
    ("test", "hot_dog"): ("validation", "yes"),
    ("test", "not_hot_dog"): ("validation", "no"),
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}


def _count_images(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(1 for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)


def reorganize(source: Path) -> None:
    # Copy (not move) so a wrong run doesn't force re-downloading from Kaggle.
    if not source.exists():
        raise SystemExit(f"❌ Source folder not found: {source}\n"
                         f"   Download the dataset first (see model/data/README.md).")

    total_copied = 0
    for (kaggle_split, kaggle_class), (our_split, our_class) in KAGGLE_TO_TARGET.items():
        src_folder = source / kaggle_split / kaggle_class
        dst_folder = TARGET_DIRS[(our_split, our_class)]
        dst_folder.mkdir(parents=True, exist_ok=True)

        if not src_folder.exists():
            print(f"⚠️  Skipping missing source folder: {src_folder}")
            continue

        copied = 0
        for img in src_folder.iterdir():
            if img.suffix.lower() in IMAGE_EXTENSIONS:
                shutil.copy2(img, dst_folder / img.name)
                copied += 1

        total_copied += copied
        print(f"  {kaggle_split}/{kaggle_class:12s} → {our_split}/{our_class:3s}  ({copied} images)")

    print(f"\n✅ Copied {total_copied} images into the train/validation layout.")
    verify()


def verify() -> None:
    print("\nDataset summary")
    print("-" * 40)
    print(f"{'split':<12}{'yes (hotdog)':>14}{'no (not)':>12}")
    print("-" * 40)

    for split in ("train", "validation"):
        n_yes = _count_images(TARGET_DIRS[(split, "yes")])
        n_no = _count_images(TARGET_DIRS[(split, "no")])
        print(f"{split:<12}{n_yes:>14}{n_no:>12}")

        # Heavy imbalance lets the model fake accuracy by always guessing the majority class.
        if n_yes and n_no and max(n_yes, n_no) / min(n_yes, n_no) > 1.5:
            ratio = max(n_yes, n_no) / min(n_yes, n_no)
            print(f"  ⚠️  '{split}' is imbalanced ({ratio:.1f}x).")
    print("-" * 40)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, help="Path to the unzipped Kaggle 'seefood' folder.")
    parser.add_argument("--verify", action="store_true", help="Count images in the current layout.")
    args = parser.parse_args()

    if args.verify:
        verify()
    elif args.source:
        reorganize(args.source)
    else:
        parser.error("Provide --source <path> to organize the data, or --verify to count it.")


if __name__ == "__main__":
    main()
