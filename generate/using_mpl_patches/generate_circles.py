"""First AxiDraw experiments."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from tqdm import tqdm
from pathlib import Path

SAVE_DIR = Path("svg_layers")

X_BOUNDS = [-10, 10]
Y_BOUNDS = [-10, 10]
MIN_RADIUS = 0.1
MAX_RADIUS = 2

N_TRIES = 500


def main():
    circles = _make_circles(n_tries=N_TRIES)
    patches_dict = _divide_circles_into_patches(circles=circles)
    # _plot_a(patches_a=blue_patches, patches_b=red_patches)
    for patch_name, patches in patches_dict.items():
        file_name = f"{patch_name}.svg"
        save_patches(patches=patches, file_path=SAVE_DIR / file_name)

    print("stop")


def _make_circles(n_tries: int = 500):
    circles = []
    for _ in tqdm(range(N_TRIES)):
        cx, cy = np.random.uniform(*X_BOUNDS), np.random.uniform(*Y_BOUNDS)
        c = np.array([cx, cy])

        r = MAX_RADIUS

        for ci, ri in circles:

            dist = np.linalg.norm(c - ci)
            largest_r = dist - ri
            largest_r = np.clip(largest_r, 0, largest_r)
            r = min(r, largest_r)

        if r >= MIN_RADIUS:
            circles.append((c, r))
    return circles


def _divide_circles_into_patches(circles: list):
    blue_patches = []
    red_patches = []

    for c, r in tqdm(circles):

        if np.random.random() > 0.5:
            blue_patches.append(mpatches.Circle(c, r, fill=None, edgecolor="blue"))
        else:
            red_patches.append(mpatches.Circle(c, r, fill=None, edgecolor="red"))

    patches_dict = {"blue": blue_patches, "red": red_patches}
    return patches_dict


def _plot_a(patches_list: list):
    fig, ax = plt.subplots(figsize=(10, 10))

    plt.grid(False)
    plt.axis("off")
    ax.set_aspect("equal")

    ax.set_xlim(X_BOUNDS)
    ax.set_ylim(Y_BOUNDS)

    collection = PatchCollection(patches_list, match_original=True)
    ax.add_collection(collection)

    plt.show()


def save_patches(patches, file_path: Path = None):
    if file_path is None:
        file_path = SAVE_DIR / "default_file.svg"

    fig, ax = plt.subplots(figsize=(10, 10))

    plt.grid(False)
    plt.axis("off")
    ax.set_aspect("equal")

    ax.set_xlim(X_BOUNDS)
    ax.set_ylim(Y_BOUNDS)

    collection = PatchCollection(patches, match_original=True)
    ax.add_collection(collection)

    file_path.parent.mkdir(parents=False, exist_ok=True)
    plt.savefig(file_path.with_suffix(".svg"), bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    main()
