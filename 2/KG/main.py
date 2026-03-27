import matplotlib.pyplot as plt

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def preprocess_text(text):
    return "".join(char.upper() for char in text if char.isalpha() and char.isascii())

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        shifted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        result += shifted_char
    return result

def encrypt_shift(text, shift):
    return caesar_cipher(text, shift)

def decrypt_shift(text, shift):
    return caesar_cipher(text, -shift)

def brute_force_shift(text):
    normalized_text = preprocess_text(text)
    
    print("=" * 66)
    print(f"{'SHIFT':<10} | {'DECRYPTED TEXT (PREPROCESSED)'}")
    print("-" * 66)
    
    for shift in range(26):
        decrypted = caesar_cipher(normalized_text, shift)
        preview = decrypted[:50] + ("..." if len(decrypted) > 50 else "")
        print(f"{shift:<10} | {preview}")
        
    print("=" * 66)

def vigenere_cipher(text, key, decrypt=False):
    normalized_text = preprocess_text(text)
    normalized_key = preprocess_text(key)
    
    if not normalized_key:
        raise ValueError("Key must contain at least one alphabetic character.")
        
    result = ""
    key_len = len(normalized_key)
    
    for i, char in enumerate(normalized_text):
        shift = ord(normalized_key[i % key_len]) - ord('A')
        if decrypt:
            shift = -shift
        
        shifted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        result += shifted_char
    return result

def encrypt_vigenere(text, key):
    return vigenere_cipher(text, key, decrypt=False)

def decrypt_vigenere(text, key):
    return vigenere_cipher(text, key, decrypt=True)

def generate_histogram(text):
    normalized_text = preprocess_text(text)
    frequencies = {}
    for char in normalized_text:
        frequencies[char] = frequencies.get(char, 0) + 1
    
    all_chars = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    labels = all_chars
    counts = [frequencies.get(char, 0) for char in all_chars]
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue', edgecolor='navy')
    plt.xlabel('Znak')
    plt.ylabel('Četnost')
    plt.title('Histogram četnosti znaků šifrového textu')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    print("\nZobrazuji histogram...")
    plt.show()

def main():
    print(brute_force_shift(read_file("file.txt")))
    
    plaintext = read_file("file1.txt")
    key = "ZIMA"
    
    print("Vigenère Cipher Verification:")
    print(f"Key: {key}")
    
    ciphertext = encrypt_vigenere(plaintext, key)
    print(f"\nCiphertext:\n{ciphertext}")
    
    expected_ciphertext = "RTGNDKZEZBQPKMBOBIEIBBHRSSQMOZAZZBUMJWZCHDZARTQDTRUCHKTDUWGDMMOHRMLASITNDDQTRQZUTHQMHHMSZPZECMETMITOQIOHZVMSDDQRNDKCGWPEUMHSDKTPNTAHZKTSMQTOUQWEMLGBTLQPNTAJZAZOSMBLNBKVMWOIJTQSMWGPNLZUKCBRDAPEMJGDDUMXHUMLMMEERBETTXZU"
    
    if ciphertext == expected_ciphertext:
        print("\nSUCCESS: Ciphertext matches expected output!")
    else:
        print(f"Expected:\n{expected_ciphertext}")
        
    generate_histogram(ciphertext)

if __name__ == "__main__":
    main()