import secrets
import string


def buat_karakter_acak() -> str:
    vowels = set("aiueo")
    rnd = secrets.SystemRandom()

    def sample_unique(n: int, max_vowels: int = 1):
        alphabet = list(string.ascii_lowercase)
        while True:
            s = rnd.sample(alphabet, n)
            if sum(1 for c in s if c in vowels) <= max_vowels:
                return s

    if secrets.randbelow(2):
        base = sample_unique(6, max_vowels=1)
        base_vowel_count = sum(1 for c in base if c in vowels)
        if base_vowel_count == 1:
            # avoid creating a second vowel by duplicating a consonant
            consonants_in_base = [c for c in base if c not in vowels]
            dup = rnd.choice(consonants_in_base)
        else:
            dup = rnd.choice(base)
        huruf = base + [dup]
    else:
        huruf = sample_unique(7, max_vowels=1)

    rnd.shuffle(huruf)
    return "2" + "".join(huruf)


if __name__ == "__main__":
    print(buat_karakter_acak())
