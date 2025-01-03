import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Opis modelu SIR
# S - Podatni
# I - Zakażeni
# R - Usunięci (wyleczeni lub zmarli)
# beta - współczynnik zakażalności
# gamma - współczynnik śmiertelności

def sir_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

# Rozwiązanie równań
def solve_sir(S0, I0, R0, beta, gamma, t_max, dt):
    t_values = np.arange(0, t_max, dt)  # Czas symulacji 
    y0 = [S0, I0, R0] # Warunki początkowe
    solution = odeint(sir_model, y0, t_values, args=(beta, gamma)) # Rozwiązanie równań metodą odeint
    return t_values, solution       # Zwracamy czas i wyniki

# Parametry wejściowe dla czterech różnych zestawów
params = [      
    (0.99, 0.01, 0.0, 0.5, 0.5),    #(S0 , I0, R0, beta, gamma)
    (0.95, 0.05, 0.0, 0.7, 0.1),
    (0.90, 0.10, 0.0, 0.9, 0.05),
    (0.85, 0.15, 0.0, 0.1, 0.9)
]

t_max = 200 # Czas symulacji 
dt = 0.1    # Krok czasowy

# Wizualizacja wyników
fig, axs = plt.subplots(2, 2, figsize=(12, 10)) # 4 wykresy w 2x2 o wymiarach 12x10 

for i, (S0, I0, R0, beta, gamma) in enumerate(params):  # Dla każdego zestawu parametrów
    T, results = solve_sir(S0, I0, R0, beta, gamma, t_max, dt)  # Rozwiązujemy równania
    S, I, R = results.T     # Rozpakowujemy wyniki
    ax = axs[i//2, i%2]             # Wybieramy odpowiedni subplot
    ax.plot(T, S, label='Podatni (S)')  # Tworzymy wykresy
    ax.plot(T, I, label='Zakażeni (I)')     
    ax.plot(T, R, label='Usunięci (R)')
    ax.set_title(f'Zestaw {i+1}')   # Dodajemy tytuł
    ax.set_xlabel('Czas')        # Dodajemy opisy osi
    ax.set_ylabel('Udział populacji')   
    ax.legend()                # Dodajemy legendę
    ax.grid()               # Dodajemy siatkę

plt.suptitle('Model SIR dla zestawu parametrów początkowych')   # Dodajemy tytuł główny
plt.tight_layout(rect=[0, 0.03, 1, 0.95])   # Dopasowujemy wykresy
plt.show()        # Wyświetlamy wykresy
