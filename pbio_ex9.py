import random

def generate_sequence(length: int, distribution: dict) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""

    nucleotides = ["A", "C", "G", "T"]

    weights = [
        distribution["A"],
        distribution["C"],
        distribution["G"],
        distribution["T"]
    ]

    sequence = "".join(
        random.choices(
            nucleotides,
            weights=weights,
            k=length
        )
    )

    return sequence

def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji.
    Klucze: "A", "C", "G", "T" (wartości float, %),
           "GC" (wartość float, %)."""
    length = len(sequence)

    stats = {}

    for nucleotide in ["A", "C", "G", "T"]:
        count = sequence.count(nucleotide)
        stats[nucleotide] = (count / length) * 100

    gc_count = sequence.count("G") + sequence.count("C")
    stats["GC"] = (gc_count / length) * 100

    return stats


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię w losową pozycję sekwencji.
    Imię zapisane małymi literami."""
    index = random.randint(0, len(sequence))
    return sequence[:index]+name.lower()+sequence[index:]

def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"

    lines = []

    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    return header + "\n" + "\n".join(lines)

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

# DODATKOWE funkcjonalnosci
'''
4. Sekwencja komplementarna i odwrotnie komplementarna,
a więc program generuje i wyświetla nić komplementarną oraz nić odwrotnie komplementarną
(pamiętasz z wykładów co to oznacza?).
Obie dopisuje jako dodatkowe rekordy do pliku FASTA z odpowiednimi oznaczeniem w ID.
'''
def complementary_sequence(sequence: str) -> str:
    complement = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    result = ""

    for nucleotide in sequence:
        result += complement[nucleotide]

    return result

def reverse_complement(sequence: str) -> str:
    return complementary_sequence(sequence)[::-1]

'''
5. Transkrypcja in silico -program generuje sekwencję mRNA (zamiana T na U) i
zapisuje ją jako odrębny rekord w pliku FASTA.
'''
def transcribe_dna(sequence: str) -> str:
    return sequence.replace("T", "U")

'''
3. Wyszukiwanie motywów .. po wygenerowaniu sekwencji program wyszukuje w niej wskazany przez użytkownika motyw (np. "ATG") i
wypisuje wszystkie pozycje wystąpień (indeksowanie od 1, zgodnie z konwencją biologiczną).

'''
def find_motif(sequence: str, motif: str) -> list:
    positions = []

    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i + len(motif)] == motif:
            positions.append(i + 1)

    return positions

'''
2. Konfigurowalny rozkład nukleotydów czyli użytkownik podaje
procentowy udział każdego nukleotydu.
Program waliduje, czy suma wynosi 100%.
'''
def get_nucleotide_distribution() -> dict:
    while True:
        try:
            a = float(input("Podaj procent A: "))
            c = float(input("Podaj procent C: "))
            g = float(input("Podaj procent G: "))
            t = float(input("Podaj procent T: "))

            total = a + c + g + t

            if total != 100:
                print("Błąd: suma procentów musi wynosić 100.")
                continue

            return {
                "A": a,
                "C": c,
                "G": g,
                "T": t
            }

        except ValueError:
            print("Błąd: podaj poprawne liczby.")


def main():
    # PODSTAWA
    length = validate_positive_int("Podaj dlugosc sekwencji: ")
    seq_id = validate_id("Podaj ID sekwencji: ")
    seq_desc = input("Podaj opis sekwencji: ")

    distribution = get_nucleotide_distribution()

    sequence = generate_sequence(
        length,
        distribution
    )

    stats = calculate_stats(sequence)
    sequence_with_name = insert_name(sequence,input("Podaj imię: "))
    fasta_content = format_fasta(
        seq_id,
        seq_desc,
        sequence_with_name
    )
    print(fasta_content)


    # Statystyki
    print(f"\nStatystyki sekwencji (n={length}):")

    for nucleotide in ["A", "C", "G", "T"]:
        print(f"  {nucleotide}: {stats[nucleotide]:.2f}%")

    print(f"  GC-content: {stats['GC']:.2f}%")


    # Zapis do pliku
    filename = f"{seq_id}.fasta"



    print(f"\nSekwencja zapisana do pliku: {filename}")


    # DODATKOWE funkcjonalnosci
    complementary = complementary_sequence(sequence)
    reverse_comp = reverse_complement(sequence)

    complementary_fasta = format_fasta(
        seq_id + "_complementary",
        "Nić komplementarna",
        complementary
    )

    reverse_fasta = format_fasta(
        seq_id + "_reverse_complementary",
        "Nić odwrotnie komplementarna",
        reverse_comp
    )

    # Dodanie do glownego fasta
    fasta_content += "\n\n" + complementary_fasta
    fasta_content += "\n\n" + reverse_fasta

    # transkrypcja
    transcribe_seq = transcribe_dna(sequence)
    transcribe_fasta = format_fasta(
        seq_id + "_transcribe",
        "Transkrypcja",
        transcribe_seq
    )
    fasta_content += "\n\n" + transcribe_fasta

    motif = input("Podaj motyw do wyszukania: ").upper()

    positions = find_motif(sequence, motif)

    if positions:
        print(f"Motyw znaleziony na pozycjach: {positions}")
    else:
        print("Nie znaleziono motywu.")

    with open(filename, "w") as file:
        file.write(fasta_content)

if __name__ == "__main__":
    main()
