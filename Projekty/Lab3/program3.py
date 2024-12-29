#dekoratory

import time        # Moduł time do mierzenia czasu wykonania funkcji
import numpy as np      # NumPy to biblioteka do obliczeń na macierzach i wektorach
from statistics import mean, stdev  # Moduł statistics do obliczania średniej i odchylenia standardowego
from tqdm import tqdm       # Moduł tqdm do wyświetlania paska postępu

# Dekorator do mierzenia czasu wykonania funkcji
class TimerDecorator:       # Klasa dekoratora
    def __init__(self, func):       
        self.func = func        # Przypisanie funkcji do zmiennej
        self.times = []     # Lista czasów wykonania funkcji

    def __call__(self, *args, **kwargs):        
        start_time = time.perf_counter()    # Pobranie czasu rozpoczęcia funkcji    
        result = self.func(*args, **kwargs) 
        end_time = time.perf_counter()          # Pobranie czasu zakończenia funkcji

        # Zapisanie czasu wykonania funkcji
        elapsed_time = end_time - start_time
        self.times.append(elapsed_time)    # Dodanie czasu do listy

        return result

    def stats(self):        # Funkcja do obliczania statystyk
        if not self.times:      # Sprawdzenie, czy są jakieś dane
            return "Brak danych do statystyk."
        return {
            "średnia": mean(self.times),        # Obliczenie średniej, minimalnej, maksymalnej wartości i odchylenia standardowego
            "min": min(self.times),
            "max": max(self.times),
            "odchylenie standardowe": stdev(self.times) if len(self.times) > 1 else 0.0
        }

# Przykładowa funkcja czasochłonna
@TimerDecorator
def czasochlonna_funkcja():     # Funkcja zwracająca odwrotność macierzy
    np.random    # Generowanie losowej macierzy
    macierz = np.random.rand(4000, 4000)        # Macierz 5000x5000
    wynik = np.linalg.inv(macierz + np.eye(4000))       # Obliczenie odwrotności macierzy (podobno czasochłonna funkcja)
    return wynik        

# Testowanie dekoratora
if __name__ == "__main__":     
    for _ in tqdm(range(10), desc="Processing"):     # Pętla z paskiem postępu
        czasochlonna_funkcja()                      # Wywołanie funkcji

    # Pobranie statystyk
    dekorator = czasochlonna_funkcja            # Przypisanie funkcji do zmiennej
    print("Statystyki czasu wykonania:")        # Wyświetlenie statystyk
    print(dekorator.stats())                    # Wywołanie funkcji obliczającej statystyki

#skrypt z przycisku