import os
import re

def main():

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


if __name__ == "__main__":
    main()

