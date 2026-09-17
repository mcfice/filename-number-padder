import os
import re
from ftplib import FTP

def main():

    question = input("Is directory a remote server? (y/n): ")

    #for normal directory (non ftp)

    if question.lower() == 'n':

        directory = input("Enter the directory path where the files are located: ")

        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        except FileNotFoundError:
            print("Directory not found.")
            return

        print(f"Found {len(files)} files in the directory.")

        num_of_digits = int(input("Enter the number of digits for the new file names: "))

        if len(files) > 10**num_of_digits - 1:
            print(f"Error: {num_of_digits} digits too small for {len(files)} files.")
            return

        for file in files:
            m = re.search(r'(\d+)', file)
            if m:
                number = m.group(1)
                new_number = number.zfill(num_of_digits)
                new_file_name = re.sub(r'(\d+)', new_number, file, count=1)
                new_path = os.path.join(directory, new_file_name)
                old_path = os.path.join(directory, file)
                if os.path.exists(new_path) and new_path != old_path:
                    print(f"Warning: '{new_file_name}' already exists. Exiting")
                    return
                os.rename(old_path, new_path)
                print(f"Renamed {file} to {new_file_name}")


    #ftp server

    else:

        host = input("Enter FTP host: ")
        port = int(input("Enter FTP port (e.g. 21): "))
        anon = input("Anonymous login? (y/n): ")

        ftp = FTP()
        ftp.connect(host, port)

        if anon.lower() == 'y':
            ftp.login()
        else:
            user = input("Enter username: ")
            password = input("Enter password: ")
            ftp.login(user, password)

        directory = input("Enter the directory path where the files are located: ")
        ftp.cwd(directory)

        files = ftp.nlst()
        files = [f for f in files if '.' in f or True]  # keep simple

        current_files = set(files)   # <-- live set of names on the server

        print(f"Found {len(files)} files in the directory.")

        num_of_digits = int(input("Enter the number of digits for the new file names: "))

        if len(files) > 10**num_of_digits - 1:
            print(f"Error: {num_of_digits} digits too small for {len(files)} files.")
            ftp.quit()
            return

        for file in files:
            m = re.search(r'(\d+)', file)
            if m:
                number = m.group(1)
                new_number = number.zfill(num_of_digits)
                new_file_name = re.sub(r'(\d+)', new_number, file, count=1)
                if new_file_name == file:
                    continue
                if new_file_name in current_files:
                    print(f"Warning: '{new_file_name}' already exists. Exiting")
                    ftp.quit()
                    return
                ftp.rename(file, new_file_name)
                current_files.discard(file)
                current_files.add(new_file_name)
                print(f"Renamed {file} to {new_file_name}")

        ftp.quit()

if __name__ == "__main__":
    main()

