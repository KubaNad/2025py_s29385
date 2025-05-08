# generator_fasta.py

# CEL PROGRAMU:
# Program służy do generowania losowej sekwencji DNA o zadanej długości i zapisania jej w formacie FASTA.
# Użytkownik podaje długość sekwencji, identyfikator, opis i imię, które zostaje osadzone w sekwencji,
# ale nie wpływa na jej statystyki biologiczne. Program wylicza procentową zawartość nukleotydów A, C, G, T
# oraz stosunek CG/AT. Plik wynikowy zapisuje sekwencję w zgodnym formacie FASTA.

# KONTEKST ZASTOSOWANIA:
# Narzędzie edukacyjne i testowe do generowania przykładowych danych biologicznych w bioinformatyce,
# np. do testów parserów FASTA, algorytmów biologii molekularnej czy ćwiczeń programistycznych.

import random            # Importujemy bibliotekę do generowania liczb losowych
import textwrap          # Import do łamania długich linii tekstu (np. co 60 znaków w FASTA)

# ==========================
# FUNKCJA: Generowanie sekwencji DNA
# ==========================

# ORIGINAL:
# def generate_dna_sequence(length):
#     return ''.join(random.choices('ACGT', k=length))
# MODIFIED (dodano parametr seed dla powtarzalności wyników przy testowaniu/debugowaniu):
def generate_dna_sequence(length, seed=None):
    """Generuje losową sekwencję DNA złożoną z nukleotydów A, C, G, T"""
    if seed is not None:
        random.seed(seed)  # Ustawiamy seed losowania (opcjonalnie)
    return ''.join(random.choices('ACGT', k=length))  # Losujemy ciąg znaków


# ==========================
# FUNKCJA: Wstawianie imienia użytkownika
# ==========================
def insert_name(sequence, name):
    """Wstawia imię użytkownika w losowym miejscu sekwencji (nie wpływa na analizę DNA)"""
    insert_pos = random.randint(0, len(sequence))  # Losowe miejsce wstawienia
    return sequence[:insert_pos] + name + sequence[insert_pos:]  # Wstawienie imienia


# ==========================
# FUNKCJA: Obliczanie statystyk sekwencji
# ==========================
def calculate_stats(sequence):
    """Oblicza statystyki procentowe zawartości A, C, G, T i stosunek CG/AT"""
    dna_only = ''.join([base for base in sequence if base in 'ACGT'])  # Pomijamy litery spoza DNA
    total = len(dna_only)  # Całkowita długość analizowanej sekwencji
    stats = {nuc: (dna_only.count(nuc) / total) * 100 for nuc in 'ACGT'}  # Procenty każdego nukleotydu
    cg_ratio = ((stats['C'] + stats['G']) / (stats['A'] + stats['T'])) if (stats['A'] + stats['T']) > 0 else 0
    return stats, cg_ratio  # Zwracamy słownik i stosunek CG/AT


# ==========================
# FUNKCJA: Zapis do pliku FASTA
# ==========================

# ORIGINAL:
# def save_to_fasta(filename, header, sequence):
#     with open(filename, 'w') as f:
#         f.write(f">{header}\n")
#         f.write(sequence + '\n')
# MODIFIED (dodano łamanie linii co 60 znaków, zgodnie z formatem FASTA):
def save_to_fasta(filename, header, sequence):
    """Zapisuje sekwencję DNA do pliku w formacie FASTA"""
    with open(filename, 'w') as f:
        f.write(f">{header}\n")  # Nagłówek FASTA zaczyna się od ">"
        wrapped_seq = '\n'.join(textwrap.wrap(sequence, 60))  # Linia co 60 znaków
        f.write(wrapped_seq + '\n')


# ==========================
# GŁÓWNA CZĘŚĆ PROGRAMU
# ==========================

if __name__ == "__main__":
    # Pobieranie danych od użytkownika

    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))
    # MODIFIED (dodano walidację wejścia od użytkownika dla długości):
    while True:
        try:
            length = int(input("Podaj długość sekwencji: "))
            if length <= 0:
                print("Długość musi być większa od zera.")
                continue
            break
        except ValueError:
            print("Podaj poprawną liczbę całkowitą.")

    seq_id = input("Podaj ID sekwencji: ").strip()  # ID np. A123
    description = input("Podaj opis sekwencji: ").strip()  # np. Losowa sekwencja testowa
    name = input("Podaj imię: ").strip()  # Imię użytkownika, np. Mike

    # MODIFIED: dodano seed, aby możliwe było testowanie z powtarzalnymi wynikami
    dna_sequence = generate_dna_sequence(length, seed=42)

    sequence_with_name = insert_name(dna_sequence, name)  # Wstawiamy imię do sekwencji
    header = f"{seq_id} {description}"  # Budujemy nagłówek FASTA
    filename = f"{seq_id}.fasta"  # Nazwa pliku to ID + rozszerzenie

    save_to_fasta(filename, header, sequence_with_name)  # Zapis do pliku

    stats, cg_ratio = calculate_stats(sequence_with_name)  # Statystyki biologiczne

    # Wyświetlenie wyników
    print(f"Sekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    for nuc in 'ACGT':
        print(f"{nuc}: {stats[nuc]:.1f}%")
    print(f"%CG: {stats['C'] + stats['G']:.1f}")
    print(f"Stosunek CG/AT: {cg_ratio:.2f}")
