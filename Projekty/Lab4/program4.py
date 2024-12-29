import os
import argparse
import numpy as np
from PIL import Image, ImageSequence
from tqdm import tqdm
import time
import numba
from numba import types, typed

@numba.njit(parallel=True)
def fill_np_simulation_grid(grid_size, spin_value):
    grid = np.empty((grid_size, grid_size), dtype=np.int8)
    for i in numba.prange(grid_size):
        for j in range(grid_size):
            if np.random.random() < spin_value:
                grid[i, j] = -1
            else:
                grid[i, j] = 1
    return grid

@numba.njit
def hamiltonian(np_simulation_grid, i, j, v):
    shape = np_simulation_grid.shape
    if (0 < i < shape[0]-1) and (0 < j < shape[1]-1):
        return -v * (np_simulation_grid[i-1, j] + np_simulation_grid[i+1, j] + np_simulation_grid[i, j-1] + np_simulation_grid[i, j+1])
    return 0

@numba.njit
def monte_carlo_alg(np_simulation_grid, grid_size, beta):
    for _ in range(grid_size**2):
        i, j = np.random.randint(1, grid_size-1), np.random.randint(1, grid_size-1)
        spin_value = np_simulation_grid[i, j]
        dE = 2 * spin_value * (np_simulation_grid[i-1, j] + np_simulation_grid[i, j-1] + np_simulation_grid[i+1, j] + np_simulation_grid[i, j+1])
        if (dE < 0) or (np.exp(-beta * dE) > np.random.random()):
            np_simulation_grid[i, j] = -spin_value


def save_image(np_simulation_grid, grid_size, pixel_size, output_directory, prefix, iteration):
    img_array = np.zeros((grid_size, grid_size, 3), dtype=np.uint8)
    img_array[np_simulation_grid == 1] = [255, 105, 180]
    img_array[np_simulation_grid == -1] = [0, 128, 0]
    img = Image.fromarray(img_array)
    img = img.resize((grid_size * pixel_size, grid_size * pixel_size), Image.NEAREST)
    img.save(os.path.join(output_directory, f"{prefix}{iteration}.png"))

def create_gif(output_directory, prefix, sim_steps, gif_name):
    images = []
    for k in range(sim_steps):
        img_path = os.path.join(output_directory, f"{prefix}{k}.png")
        images.append(Image.open(img_path))
    images[0].save(os.path.join(output_directory, gif_name), save_all=True, append_images=images[1:], duration=100, loop=0)
    print(f"GIF zapisany jako {os.path.join(output_directory, gif_name)}")

@numba.njit
def calculate_magnetization(np_simulation_grid):
    return np.sum(np_simulation_grid)

def save_magnetization(output_directory, magnetization_file, magnetization_values):
    with open(os.path.join(output_directory, magnetization_file), "w") as f:
        for value in magnetization_values:
            f.write(f"{value}\n")
    print(f"Magnetyzacja zapisana w {os.path.join(output_directory, magnetization_file)}")

def run_simulation(makrosteps, grid_size, B, J, beta, spin_value, output_directory, prefix, pixel_size, gif_name, magnetization_file):
    os.makedirs(output_directory, exist_ok=True)
    np_simulation_grid = fill_np_simulation_grid(grid_size, spin_value)
    sim_steps = makrosteps * grid_size**2
    start_time = time.time()
    magnetization_values = []

    for k in tqdm(range(sim_steps), desc="Running Simulation", colour='green'):
        if prefix:
            save_image(np_simulation_grid, grid_size, pixel_size, output_directory, prefix, k)
        monte_carlo_alg(np_simulation_grid, grid_size, beta)
        if magnetization_file:
            magnetization_values.append(calculate_magnetization(np_simulation_grid))

    if gif_name:
        create_gif(output_directory, prefix, sim_steps, gif_name)
    if magnetization_file:
        save_magnetization(output_directory, magnetization_file, magnetization_values)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Gotowe. Zapisano {sim_steps} w {output_directory}Czas trwania: {elapsed_time:.2f} sekund")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers')
    parser.add_argument('--grid', '-g', type=int, default=10, help='Rozmiar siatki')
    parser.add_argument('--B', type=float, default=1, help='Wartość pola B')
    parser.add_argument('--J', type=float, default=1, help='Wartość stałej J')
    parser.add_argument('--beta', type=float, default=0.5, help='Wartość beta')
    parser.add_argument('--spin','-s', type=float, default=0.5, help='Prawdopodobieństwo losowego spinu')
    parser.add_argument('--output_prefix', '-o', type=str, default=None, help='prefix dla plików wyjściowych')
    parser.add_argument('--gif_name', '-gname', type=str, default=None, help='Nazwa pliku GIF z animacją')
    parser.add_argument('--magnetization_file', '-mfile', type=str, default=None, help='Nazwa pliku do zapisu magnetyzacji')
    parser.add_argument('--makrosteps', '-m', type=int, default=1, help='Liczba makrokroków')
    args = parser.parse_args()

    gif_name = args.gif_name + '.gif' if args.gif_name else None
    magnetization_file = args.magnetization_file + '.txt' if args.magnetization_file else None

    run_simulation(makrosteps=args.makrosteps, grid_size=args.grid, B=args.B, J=args.J, beta=args.beta, spin_value=args.spin, output_directory="result_images/", prefix=args.output_prefix, pixel_size=10, gif_name=gif_name, magnetization_file=magnetization_file)


#poetry run python .\program4.py
#poetry run python .\program4.py -o obraz -gname gif -mfile magnetyzacja -g 20 -m 2