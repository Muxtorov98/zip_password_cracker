import sys
import zipfile
import itertools

def brute_force(length):
    your_list = 'abcdefghijklmnopqrstuvwxyz'
    complete_list = []
    for current_length in range(1, length + 1):
        for item in itertools.product(your_list, repeat=current_length):
            yield ''.join(item)

def main():
    """
    Zipfile password cracker using brute-force dictionary attack
    """
    try:
        zipfilename = sys.argv[1]
        password_length = int(sys.argv[2])
    except IndexError:
        print("Usage: python script.py <zipfile> <max_password_length>")
        return
    except ValueError:
        print("Password length must be an integer.")
        return

    try:
        zip_file = zipfile.ZipFile(zipfilename)
    except FileNotFoundError:
        print(f"File '{zipfilename}' not found.")
        return

    for password in brute_force(password_length):
        try:
            print(f"Trying password: {password}")
            zip_file.extractall(pwd=password.encode('utf-8'))
            print("===================================")
            print(f"Password found: {password}")
            print("===================================")
            return
        except RuntimeError:
            # Wrong password, continue trying
            pass
        except zipfile.BadZipFile:
            print("Bad zip file.")
            return

    print("Password not found.")

if __name__ == '__main__':
    main()
