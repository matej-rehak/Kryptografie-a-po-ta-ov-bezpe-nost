import math
import collections
import matplotlib.pyplot as plt

def clean(text: str) -> str:
    cleaned_chars = []
    for c in text.upper():
        if c.isalpha() and ord(c) < 128:
            cleaned_chars.append(c)
    return ''.join(cleaned_chars)


def key_order(key: str) -> list[int]:
    key = key.upper()
    indexed = sorted(range(len(key)), key=lambda i: (key[i], i))
    order = [0] * len(key)
    for rank, col in enumerate(indexed):
        order[col] = rank
    return order

def columnar_encrypt(plaintext: str, key: str) -> str:
    pt = clean(plaintext)
    n = len(key)
    # padding
    pad = (-len(pt)) % n
    pt += 'X' * pad

    rows = len(pt) // n
    grid = []
    for i in range(rows):
        row = pt[i * n: (i + 1) * n]
        grid.append(list(row))

    order = key_order(key)
    num_cols = n
    col_by_rank = sorted(range(num_cols), key=lambda c: order[c])

    ciphertext = ''
    for col in col_by_rank:
        for row in grid:
            ciphertext += row[col]
    return ciphertext


def columnar_decrypt(ciphertext: str, key: str) -> str:
    ct = clean(ciphertext)
    n = len(key)
    rows = len(ct) // n

    order = key_order(key)
    col_by_rank = sorted(range(n), key=lambda c: order[c])

    grid_cols = {}
    idx = 0
    for col in col_by_rank:
        grid_cols[col] = list(ct[idx:idx+rows])
        idx += rows

    plaintext = ''
    for r in range(rows):
        for c in range(n):
            plaintext += grid_cols[c][r]
    return plaintext

def row_encrypt(plaintext: str, key: str) -> str:
    pt = clean(plaintext)
    n = len(key)
    pad = (-len(pt)) % n
    pt += 'X' * pad

    rows = len(pt) // n
    grid = [list(pt[i*n:(i+1)*n]) for i in range(rows)]

    order = key_order(key)
    ciphertext = ''
    for row in grid:
        reordered = [None] * n
        for col in range(n):
            reordered[order[col]] = row[col]
        ciphertext += ''.join(reordered)
    return ciphertext


def row_decrypt(ciphertext: str, key: str) -> str:
    ct = clean(ciphertext)
    n = len(key)
    rows = len(ct) // n

    order = key_order(key)

    plaintext = ''
    for i in range(rows):
        row = list(ct[i*n:(i+1)*n])
        original = [None] * n
        for col in range(n):
            original[col] = row[order[col]]
        plaintext += ''.join(original)
    return plaintext

def char_frequency(text: str) -> dict:
    text = clean(text)
    freq = collections.Counter(text)
    return dict(sorted(freq.items()))


def index_of_coincidence(text: str) -> float:
    text = clean(text)
    n = len(text)
    freq = collections.Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic


def plot_histogram(freq: dict, title: str):
    letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    counts = [freq.get(l, 0) for l in letters]
    plt.figure(figsize=(12, 4))
    plt.bar(letters, counts, color='steelblue')
    plt.title(title)
    plt.xlabel('Znak')
    plt.ylabel('Počet výskytů')
    plt.tight_layout()
    plt.savefig(f'{title.replace(" ", "_")}.png', dpi=100)
    plt.close()
    print(f"  Histogram uložen: {title}.png")

KEY = "PROJEV"
PLAINTEXT = (
    "RUSKYPREZIDENTVLADIMIRPUTINPRONESLVECTVRTEKTRADICNIPROJEVOSTAVUFEDERACEVENOVALS"
    "ETOMUZERUSKOMUSIPOKRACOVATVTRANSFORMACIANEMUZESESPOKOJITSESOUCASNYMSTAVEMZ"
    "MINILSTOUPAJICIPOCETCHUDYCHIZAOSTALOUINFRASTRUKTURUNUTNOUPODPORUDUCHODCUMIM"
    "LADYMRODINYMABYSEZVRYTILNEPRIZNIVYDEMOGRAFICKYVYVOJ"
)

M1 = (
    "RTGNDKZEZBQPKMBOBIEIBBHRSSQMOZAZZBUMJWZCHDZARTQDTRUCHKTDUWGDMMOHRMLASIT"
    "NDDQTRQZUTHQMHHMSZPZECMETMITOQIOHZVMSDDQRNDKCGWPEUMHSDKTPNTAHZKTSMQTO"
    "UQWEMLGBTLQPNTAJZAZOSMBLNBKVMWOIJTQSMWGPNLZUKCBRDAPEMJGDDUMXHUMLMMEER"
    "BETTXZU"
)

M2 = (
    "YDAPRVTDRSEEAMSICTOAEKESAIOCTCSITROOHIMYEIIDAVKILRPLRAPOFCVOUSAVFIZOSATMTIEYOUS"
    "UNPCMYNSTRYRYSZVINSVRIVUAOTRURTSCUPTCSZSJCDAOATTDUUDIYYPVGKJRRNITNCKCJAEESZOOV"
    "AMEEJOYEIPPHIAFUNPUDLOAVNNMIVUETMIETTNEVRNEEMKANAMSIUMMLAOUZLRKUODCADBREI"
    "OCOPEDUOEEIOTDVLUKPORRNSOSNVNUICHTNRUUROMRMZLZEFY"
)

print("ÚLOHA 1a: Columnar Transposition")
ct_col = columnar_encrypt(PLAINTEXT, KEY)
print(f"Klíč: {KEY}")
print(f"Šifrový text: {ct_col}")
pt_col = columnar_decrypt(ct_col, KEY)
print(f"Dešifrování: {pt_col}")
pt_stripped = pt_col.rstrip('X')[:len(clean(PLAINTEXT))]

print()
print("  ÚLOHA 1b: Row Transposition")
ct_row = row_encrypt(PLAINTEXT, KEY)
print(f"Klíč: {KEY}")
print(f"Šifrový text: {ct_row}")
pt_row = row_decrypt(ct_row, KEY)
print(f"Dešifrování: {pt_row}")
pt_stripped2 = pt_row.rstrip('X')[:len(clean(PLAINTEXT))]

print()
print("ÚLOHA 2: Kryptoanalýza")

for name, text in [("M1", M1), ("M2", M2)]:
    freq = char_frequency(text)
    ic = index_of_coincidence(text)
    print(f"\n{name}:")
    print(f"Délka textu: {len(clean(text))}")
    print(f"Index koincidence: {ic:.6f}")
    print(f"Četnosti: {freq}")
    plot_histogram(freq, f"Histogram {name}")