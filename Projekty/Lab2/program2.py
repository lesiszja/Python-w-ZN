# ising 2D monte carlo simulation
import os       # Biblioteka do obsługi systemu operacyjnego
import argparse     # Biblioteka do obsługi argumentów wiersza poleceń
import numpy as np      # Biblioteka do obliczeń numerycznych
from PIL import Image, ImageSequence        # Biblioteka do obsługi obrazów
from tqdm import tqdm       # Biblioteka do paska postępu
import time

class IsingSimulation:    # Klasa symulacji modelu Isinga
    def __init__(self,makrosteps=1, grid_size=15, B=1, J=1, beta=0.5, spin_value=0.5, output_directory="result_images/",prefix=None, pixel_size=10, gif_name=None, magnetization_file=None):   # Konstruktor klasy
        self.grid_size = grid_size      
        self.prefix = prefix
        self.B = B
        self.J = J
        self.beta = beta
        self.spin_value = spin_value
        self.sim_steps = makrosteps*grid_size**2       # Liczba kroków symulacji
        self.output_directory = output_directory    
        self.pixel_size = pixel_size 
        self.gif_name = gif_name if gif_name and gif_name.endswith('.gif') else (gif_name + '.gif' if gif_name else None)            # Nazwa pliku GIF
        self.magnetization_file = magnetization_file if magnetization_file and magnetization_file.endswith('.txt') else (magnetization_file + '.txt' if magnetization_file else None)    # Nazwa pliku z magnetyzacją
        os.makedirs(self.output_directory, exist_ok=True)       # Tworzenie katalogu na obrazy
        self.np_simulation_grid = self.fill_np_simulation_grid()    # Wypełnienie siatki losowymi wartościami
        print(f"Rozpoczęcie symulacji. Png zaipsują się w: {self.output_directory} losowość: {self.spin_value} liczba kroków: {self.sim_steps} siatka: {self.grid_size}")

    # Funkcja obliczająca hamiltonian dla danego spinu
    def hamiltonian(self, i, j, v):             # Obliczanie hamiltonianu
        shape = self.np_simulation_grid.shape       # Pobranie rozmiaru siatki
        if (0 < i < shape[0]-1) and (0 < j < shape[1]-1):       # Sprawdzenie czy spin nie jest na brzegu
            return -v * (self.np_simulation_grid[i-1, j] + self.np_simulation_grid[i+1, j] + self.np_simulation_grid[i, j-1] + self.np_simulation_grid[i, j+1])   # Obliczenie hamiltonianu
        return 0        # Zwrócenie 0 jeśli spin jest na brzegu


    def fill_np_simulation_grid(self):    # Wypełnianie siatki losowymi wartościami
        return np.random.choice([-1, 1], size=(self.grid_size, self.grid_size), p=[self.spin_value, 1-self.spin_value])   # Losowanie wartości dla siatki

    # Algorytm Monte Carlo do symulacji modelu Isinga
    def monte_carlo_alg(self):
        for _ in range(self.grid_size**2):    # Dla każdego spinu w siatce
            i, j = np.random.randint(1, self.grid_size-1), np.random.randint(1, self.grid_size-1)   # Losowanie współrzędnych
            spin_value = self.np_simulation_grid[i, j]      # Pobranie wartości spinu
            dE = 2 * spin_value * (self.np_simulation_grid[i-1, j] + self.np_simulation_grid[i, j-1] + self.np_simulation_grid[i+1, j] + self.np_simulation_grid[i, j+1])   # Obliczenie zmiany energii

            if (dE < 0) or (np.exp(-self.beta * dE) > np.random.random()):  # Sprawdzenie czy zmiana energii jest korzystna
                self.np_simulation_grid[i, j] = -spin_value   # Zmiana wartości spinu

    # Funkcja zapisująca aktualny stan siatki jako obraz PNG
    def save_image(self, iteration):
        img_array = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.uint8)   # Tworzenie tablicy obrazu
        img_array[self.np_simulation_grid == 1] = [255, 105, 180]  # Kolor różowy dla dodatnich spinów
        img_array[self.np_simulation_grid == -1] = [0, 128, 0]     # Kolor zielony dla ujemnych spinów
        img = Image.fromarray(img_array)        # Tworzenie obrazu z tablicy
        img = img.resize((self.grid_size * self.pixel_size, self.grid_size * self.pixel_size), Image.NEAREST)   # Zmiana rozmiaru obrazu
        img.save(os.path.join(self.output_directory, f"{self.prefix}{iteration}.png"))  # Zapis obrazu

    # Funkcja tworząca GIF z zapisanych obrazów
    def create_gif(self):
        images = []    # Lista obrazów
        for k in range(self.sim_steps):     # Dla każdego kroku symulacji
            img_path = os.path.join(self.output_directory, f"{self.prefix}{k}.png")  # Ścieżka do obrazu
            images.append(Image.open(img_path))     # Dodanie obrazu do listy
        images[0].save(os.path.join(self.output_directory, self.gif_name), save_all=True, append_images=images[1:], duration=100, loop=0)   # Zapisanie obrazów jako GIF
        print(f"GIF zapisany jako {os.path.join(self.output_directory, self.gif_name)}")    # Wyświetlenie komunikatu

    # Funkcja obliczająca magnetyzację
    def calculate_magnetization(self):  
        return np.sum(self.np_simulation_grid)  # Obliczenie sumy wartości spinów

    # Funkcja uruchamiająca symulację
    def run_simulation(self):
        start_time = time.time()
        magnetization_values = []   # Lista magnetyzacji
        for k in tqdm(range(self.sim_steps), desc="Running Simulation", colour='green'):    # Dla każdego kroku symulacji
            if self.prefix:    # Jeśli prefix istnieje
                self.save_image(k)  # Zapis obrazu
            self.monte_carlo_alg()  # Uruchomienie algorytmu Monte Carlo
            if self.magnetization_file:     # Jeśli plik z magnetyzacją istnieje
                magnetization_values.append(self.calculate_magnetization())     # Obliczenie magnetyzacji
        if self.gif_name:       # Jeśli nazwa pliku GIF istnieje
            self.create_gif()       # Stworzenie GIFa
        if self.magnetization_file:     # Jeśli plik z magnetyzacją istnieje
            self.save_magnetization(magnetization_values)   # Zapis magnetyzacji
        end_time = time.time()  # Zapisz czas zakończenia
        elapsed_time = end_time - start_time  # Oblicz czas trwania
        print(f"Gotowe. Zapisano {self.sim_steps} w {self.output_directory}Czas trwania: {elapsed_time:.2f} sekund")   # Wyświetlenie komunikatuu

    # Funkcja zapisująca magnetyzację do pliku
    def save_magnetization(self, magnetization_values):     
        with open(os.path.join(self.output_directory, self.magnetization_file), "w") as f:  # Otwarcie pliku do zapisu
            for value in magnetization_values:  # Dla każdej wartości magnetyzacji
                f.write(f"{value}\n")   # Zapis wartości do pliku
        print(f"Magnetyzacja zapisana w {os.path.join(self.output_directory, self.magnetization_file)}")


if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Process some integers')
    parser.add_argument('--grid', '-g', type=int, default=10, help='Rozmiar siatki')    # Dodanie argumentów rozmiaru siatki
    parser.add_argument('--B', type=float, default=1, help='Wartość pola B')        # Dodanie argumentów pola B
    parser.add_argument('--J', type=float, default=1, help='Wartość stałej J')      # Dodanie argumentów stałej J
    parser.add_argument('--beta', type=float, default=0.5, help='Wartość beta')     # Dodanie argumentów beta
    parser.add_argument('--spin','-s', type=float, default=0.5, help='Prawdopodobieństwo losowego spinu')       # Dodanie argumentów prawdopodobieństwa losowego spinu
    parser.add_argument('--output_prefix', '-o', type=str, default=None, help='prefix dla plików wyjściowych')       # Dodanie argumentów prefixu
    parser.add_argument('--gif_name', '-gname', type=str, default=None, help='Nazwa pliku GIF z animacją')      # Dodanie argumentów nazwy pliku GIF
    parser.add_argument('--magnetization_file', '-mfile', type=str, default=None, help='Nazwa pliku do zapisu magnetyzacji')        # Dodanie argumentów nazwy pliku magnetyzacji
    parser.add_argument('--makrosteps', '-m', type=int, default=1, help='Liczba makrokroków')       # Dodanie argumentów liczby makrokroków
    args = parser.parse_args()    # Parsowanie argumentów

    simulation = IsingSimulation(makrosteps=args.makrosteps,grid_size=args.grid, B=args.B, J=args.J, beta=args.beta, spin_value=args.spin, prefix=args.output_prefix, gif_name=args.gif_name, magnetization_file=args.magnetization_file)   # Inicjalizacja symulacji
    simulation.run_simulation()    # Uruchomienie symulacji


#poetry run python .\program2.py 
#poetry run python .\program2.py -o obraz -gname gif -mfile magnetyzacja


