# dfir.py
import os
import hashlib
import csv
import psutil
import logging
from datetime import datetime

# --- Set up timestamped logging ---
log_filename = f"dfir_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Dfir:
    def generate_fingerprints(self) -> None:
        """Generate fingerprints (checksums) of all the Python files in the current directory."""
        file_list = [f for f in os.listdir() if f.endswith('.py')]
        if not file_list:
            print("No Python files found in the current directory.")
            logging.warning("No Python files found in the current directory.")
            return

        with open('checksums.csv', 'w', newline='') as checksums:
            writer = csv.writer(checksums, delimiter=',')
            for file_name in file_list:
                with open(file_name, 'r', encoding='utf-8') as file:
                    plain_text = file.read()
                    hashed_text = hashlib.sha256(plain_text.encode()).hexdigest()
                    writer.writerow([file_name, hashed_text])
                    print(f"Fingerprint written: {file_name} -> {hashed_text}")
                    logging.info(f"Fingerprint written: {file_name} -> {hashed_text}")
        print(" Fingerprint generation complete. Data written to checksums.csv.")
        logging.info("Fingerprint generation complete. Data written to checksums.csv.")

    def compare_fingerprints(self) -> bool:
        """Compare the fingerprints of all Python files with the stored checksums."""
        mismatch_found = False
        if not os.path.exists('checksums.csv'):
            msg = "No checksum file found. Run generate_fingerprints() first."
            print(msg)
            logging.warning(msg)
            return True

        with open('checksums.csv', 'r', newline='') as checksums:
            reader = csv.reader(checksums, delimiter=',')
            stored_hashes = {rows[0]: rows[1] for rows in reader if rows}

        for file_name in os.listdir():
            if file_name.endswith('.py'):
                with open(file_name, 'r', encoding='utf-8') as file:
                    plain_text = file.read()
                    hashed_text = hashlib.sha256(plain_text.encode()).hexdigest()
                    if stored_hashes.get(file_name) == hashed_text:
                        msg = f"{file_name} : OK"
                        print(msg)
                        logging.info(msg)
                    else:
                        msg = f"{file_name} : Mismatch"
                        print(msg)
                        logging.warning(msg)
                        mismatch_found = True

        return mismatch_found

    def get_last_logins_not_current_user(self, authorised_user: str) -> bool:
        """Check if any logged-in users differ from the specified authorized user."""
        unauthorized_user_found = False
        current_users = psutil.users()
        for user in current_users:
            username = user.name if hasattr(user, 'name') else user[0]
            if username.lower() != authorised_user.lower():
                msg = f"Unauthorized user found: {username}"
                print(msg)
                logging.warning(msg)
                unauthorized_user_found = True
            else:
                msg = f"{username} is an authorized user"
                print(msg)
                logging.info(msg)
        return unauthorized_user_found


if __name__ == "__main__":
    dfir = Dfir()

    # Step 1: Generate fingerprints if needed
    dfir.generate_fingerprints()

    # Step 2: Compare fingerprints
    if dfir.compare_fingerprints():
        msg = "---- Fingerprint mismatch found"
        print(msg)
        logging.warning(msg)
    else:
        msg = "---- No fingerprint mismatch found"
        print(msg)
        logging.info(msg)

    # Step 3: Check logged-in users
    if dfir.get_last_logins_not_current_user('Alba Palacio'):
        msg = "---- Unauthorized user found"
        print(msg)
        logging.warning(msg)
    else:
        msg = "---- No unauthorized user found"
        print(msg)
        logging.info(msg)
