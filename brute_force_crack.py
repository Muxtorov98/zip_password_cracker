import sys
import itertools
import string

try:
    import zipfile
except ImportError:
    print("zipfile kutubxonasi topilmadi.")
    sys.exit(1)

try:
    import rarfile
except ImportError:
    rarfile = None
    print("rarfile kutubxonasi topilmadi. RAR fayllarni ochish uchun o'rnatilishi kerak.")

def brute_force(length):
    chars = string.ascii_lowercase
    for current_length in range(1, length + 1):
        for attempt in itertools.product(chars, repeat=current_length):
            yield ''.join(attempt)

def main():
    if len(sys.argv) != 3:
        print("Qo'llanma: python script.py <fayl> <max_password_length>")
        sys.exit(1)

    filename = sys.argv[1]
    max_length = int(sys.argv[2])

    # Faylni tekshirish va turini aniqlash
    if filename.lower().endswith('.zip'):
        try:
            with zipfile.ZipFile(filename) as zf:
                for password in brute_force(max_length):
                    try:
                        print(f"Yozilmoqda: {password}")
                        zf.extractall(pwd=password.encode('utf-8'))
                        print(f"Topildi! Parol: {password}")
                        return
                    except RuntimeError:
                        pass
                    except zipfile.BadZipFile:
                        print("Yomon ZIP fayl.")
                        return
        except FileNotFoundError:
            print("Fayl topilmadi.")
        except zipfile.BadZipFile:
            print("Yomon ZIP fayl.")
    elif filename.lower().endswith('.rar'):
        if rarfile is None:
            print("rarfile kutubxonasi o'rnatilmagan. O'rnatish uchun: pip install rarfile")
            return
        try:
            with rarfile.RarFile(filename) as rf:
                for password in brute_force(max_length):
                    try:
                        print(f"Yozilmoqda: {password}")
                        rf.extractall(path='.', pwd=password)
                        print(f"Topildi! Parol: {password}")
                        return
                    except rarfile.RarWrongPassword:
                        pass
                    except rarfile.BadRarFile:
                        print("Yomon RAR fayl.")
                        return
        except FileNotFoundError:
            print("Fayl topilmadi.")
        except rarfile.BadRarFile:
            print("Yomon RAR fayl.")
    else:
        print("Fayl ZIP yoki RAR formatida emas.")

if __name__ == '__main__':
    main()
