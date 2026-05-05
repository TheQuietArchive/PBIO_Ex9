#todo zapis do fasta
#todo calculate stats
#todo cztery dodatkowe funkcjonalnosci
#todo usunac print debugi

import random

def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    nucleotides = ['A', 'C', 'G', 'T']
    sequence = ""
    for i in range(length):
        sequence+=random.choice(nucleotides)

    print(sequence) # debug
    return sequence

def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości float, %),
           "GC" (wartość float, %)."""


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    index = random.randint(0, len(sequence))
    return sequence[:index]+name.lower()+sequence[index:]

def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""

def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu.
    W przypadku błędu powtarza pytanie."""
    while True:
        val = input(prompt)

        # Sprawdzenie czy val jest liczba
        try:
            val = int(val)
        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
            continue

        # Sprawdzenie czy val miesci sie w przedziale
        if val < min_val or val > max_val or val is None:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")
            continue

        return val

def validate_id(prompt: str) -> str:
    while True:
        seq_id = input(prompt)

        # Sprawdzenie czy ktorys znak jest znakiem bialym
        if seq_id=="" or any(char.isspace() for char in seq_id):
            print(f"Błąd: wartość id nie moze byc bialym znakiem.")
            continue

        return seq_id

def main():
    length = validate_positive_int("Podaj dlugosc sekwencji: ")
    sequence = generate_sequence(length)
    seq_id = validate_id("Podaj ID sekwencji: ")
    seq_desc = input("Podaj opis sekwencji: ")
    sequence = insert_name(sequence,input("Podaj imię: "))
    print(sequence) # debug

if __name__ == "__main__":
    main()
