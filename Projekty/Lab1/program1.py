import argparse
import collections
import random
import time
from ascii_graph import Pyasciigraph
import tqdm
import collections
from collections import defaultdict
from _collections_abc import Iterable


def read_txt_file(file_path):               #funkcja do odczytu pliku
    with open(file_path, 'r') as file:
        return file.read()

def process_text(text, min_word_length=0, ignored_words=None, must_contain=None, cannot_contain=None):          #funkcja do przetwarzania tekstu
    words = text.split()    #dzieli tekst na słowa
    filtered_words = [word.lower() for word in words if len(word) >= min_word_length]   #filtruje słowa o długości większej niż min_word_length

    if ignored_words:
        filtered_words = [word for word in filtered_words if word not in ignored_words] #usuwa słowa z ignored_words

    if must_contain:
        filtered_words = [word for word in filtered_words if any(substring in word for substring in must_contain)]  #usuwa słowa które nie zawierają liter z must_contain

    if cannot_contain:
        filtered_words = [word for word in filtered_words if all(substring not in word for substring in cannot_contain)]    #usuwa słowa które zawierają litery z cannot_contain

    return filtered_words   #zwraca przefiltrowane słowa
    

def generate_histogram(words, limit=10):    #funkcja do generowania histogramu
    word_count = defaultdict(int)   #tworzy słownik z wartościami domyślnymi 0
    for word in words:  #dla każdego słowa w liście słów
        word_count[word] += 1   #zwiększa wartość w słowniku o 1

    sorted_word_count = sorted(word_count.items(), key=lambda item: item[1], reverse=True)[:limit]  #sortuje słowa po ilości wystąpień i wybiera limit pierwszych
    graph = Pyasciigraph()  #tworzy obiekt graf
   
    for index, line in enumerate(graph.graph('Word Frequency Histogram', sorted_word_count)):   #dla każdego elementu w liście słów
        if index <2:    #jeśli index jest mniejszy niż 2 to wypisuje bez zmiany koloru (2 bo 0 i 1 to tytuł i linia)
             print(line)
        else:   #jeśli index jest większy niż 2 to wypisuje z kolorami zależnymi od ilości wystąpień  
            print(f"\033[38;2;{sorted_word_count[index-2][1]*10};{80+sorted_word_count[index-2][1]*2};0m{line}\033[0m")
       

def main():    #funkcja główna
    parser = argparse.ArgumentParser(description='Process some integers')   
    parser.add_argument('filename', help='Nazwa pliku do przetworzenia')    #dodaje argument filename (nazwa pliku)
    parser.add_argument('--limit', '-l', type=int, default=10, help='Dla ilu wyrazów wyświetlić histogram')  #dodaje argument limit (domyślnie 10)
    parser.add_argument('--min_length', '-L', type=int, default=0, help='Minimalna długość słowa do wyświetlenia')  #dodaje argument min_length (domyślnie 0)
    parser.add_argument('--ignore', '-i', nargs='*', help='Lista słów do zignorowania') #dodaje argument ignore (domyślnie brak)
    parser.add_argument('--must_contain', '-m', nargs='*', help='Zbiór liter które muszą wystąpić w słowach')   #dodaje argument must_contain (domyślnie brak)
    parser.add_argument('--cannot_contain', '-c', nargs='*', help='Zbiór liter które nie mogą wystąpić w słowach')  #dodaje argument cannot_contain (domyślnie brak)

    args = parser.parse_args()  

    collections.Iterable = Iterable

    text = read_txt_file(args.filename)   #odczytuje plik
    words = process_text(text, args.min_length, args.ignore, args.must_contain, args.cannot_contain)    #przetwarza tekst
    with tqdm.tqdm(total=len(words), desc="Generating Histogram") as pbar:  #tworzy pasek postępu
        print("\n")
        generate_histogram(words, args.limit)   #generuje histogram
        pbar.update(len(words)) #aktualizuje pasek postępu
        



if __name__ == '__main__':  #jeśli plik jest uruchamiany jako skrypt
    main()


#poetry run python .\program1.py test.txt
#poetry run python .\program1.py test.txt -l 15 -L 3 -i the -m a -c t