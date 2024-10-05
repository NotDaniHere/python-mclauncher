import os
import subprocess
import requests
import platform
import sys
import tempfile
import uuid

def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded file to {save_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
    return True

def check_java_version():
    try:
        result = subprocess.run(["java", "-version"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        version_info = result.stderr.decode()
        
        for line in version_info.splitlines():
            if "version" in line:
                version = line.split('"')[1]
                major_version = int(version.split('.')[0])
                print(f"Detected Java version: {version}")
                return major_version
    except Exception as e:
        print(f"Error checking Java version: {e}")
        return None

    return None

def install_java():
    system = platform.system()
    java_url = None
    java_installer = None

    if system == "Windows":
        java_url = "https://download.oracle.com/java/21/archive/jdk-21_windows-x64_bin.exe"
        java_installer = "jdk-21_windows-x64_bin.exe"
    elif system == "Linux":
        java_url = "https://download.oracle.com/java/21/archive/jdk-21_linux-x64_bin.tar.gz"
        java_installer = "jdk-21_linux-x64_bin.tar.gz"
    elif system == "Darwin":
        java_url = "https://download.oracle.com/java/21/archive/jdk-21_macos-x64_bin.dmg"
        java_installer = "jdk-21_macos-x64_bin.dmg"
    else:
        print("Unsupported OS. Please install Java manually.")
        sys.exit(1)

    # Use a secure temporary directory
    temp_dir = tempfile.mkdtemp()
    java_path = os.path.join(temp_dir, java_installer)

    print("Downloading Java...")
    if not download_file(java_url, java_path):
        sys.exit(1)

    # Install Java
    print("Installing Java...")
    try:
        if system == "Linux":
            # Check if the directory exists and remove it if necessary
            jdk_install_dir = "/usr/local/jdk-21"
            if os.path.exists(jdk_install_dir):
                print(f"Removing existing directory: {jdk_install_dir}")
                subprocess.run(["sudo", "rm", "-rf", jdk_install_dir], check=True)

            # Extract to a temporary directory
            extract_dir = os.path.join(temp_dir, "jdk-21")
            subprocess.run(["tar", "-xzf", java_path, "-C", temp_dir], check=True)

            # Move the JDK to /usr/local
            subprocess.run(["sudo", "mv", os.path.join(temp_dir, "jdk-21"), jdk_install_dir], check=True)

            # Update alternatives
            subprocess.run(["sudo", "update-alternatives", "--install", "/usr/bin/java", "java", f"{jdk_install_dir}/bin/java", "1"], check=True)
            subprocess.run(["sudo", "update-alternatives", "--install", "/usr/bin/javac", "javac", f"{jdk_install_dir}/bin/javac", "1"], check=True)

        print("Java installed successfully.")
    except Exception as e:
        print(f"Error installing Java: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary files
        if os.path.exists(temp_dir):
            subprocess.run(["sudo", "rm", "-rf", temp_dir])

def set_java_alternatives():
    try:
        # Ensure that the newly installed Java is set as the default
        subprocess.run(["sudo", "update-alternatives", "--set", "java", "/usr/local/jdk-21/bin/java"], check=True)
        subprocess.run(["sudo", "update-alternatives", "--set", "javac", "/usr/local/jdk-21/bin/javac"], check=True)
        print("Java alternatives updated.")
    except Exception as e:
        print(f"Error updating Java alternatives: {e}")
        sys.exit(1)

def get_latest_minecraft_version():
    try:
        response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
        response.raise_for_status()
        manifest = response.json()
        latest_version = manifest['latest']['release']
        print(f"Latest Minecraft version: {latest_version}")
        return latest_version
    except Exception as e:
        print(f"Error fetching the latest Minecraft version: {e}")
        return None

def get_version_info(version):
    try:
        response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
        response.raise_for_status()
        manifest = response.json()
        
        for ver in manifest['versions']:
            if ver['id'] == version:
                return ver['url']
        return None
    except Exception as e:
        print(f"Error fetching version info: {e}")
        return None

def download_minecraft_version(version):
    version_info_url = get_version_info(version)
    if not version_info_url:
        print("Could not find version info.")
        return False

    try:
        response = requests.get(version_info_url)
        response.raise_for_status()
        version_info = response.json()
        
        jar_url = version_info['downloads']['client']['url']
        jar_path = os.path.expanduser(f"~/.minecraft/versions/{version}/{version}.jar")
        
        os.makedirs(os.path.dirname(jar_path), exist_ok=True)
        print("Downloading the Minecraft JAR file...")
        if not download_file(jar_url, jar_path):
            return False

        json_path = os.path.expanduser(f"~/.minecraft/versions/{version}/{version}.json")
        print("Downloading the version JSON file...")
        if not download_file(version_info_url, json_path):
            return False
        
        libraries = version_info['libraries']
        for lib in libraries:
            if 'downloads' in lib and 'artifact' in lib['downloads']:
                lib_url = lib['downloads']['artifact']['url']
                lib_path = os.path.expanduser(f"~/.minecraft/libraries/{lib['downloads']['artifact']['path']}")
                
                # Skip downloading if already exists and is the right version
                if os.path.exists(lib_path):
                    print(f"Library already exists: {lib_path}, skipping download.")
                else:
                    os.makedirs(os.path.dirname(lib_path), exist_ok=True)
                    print(f"Downloading library: {lib_url}")
                    if not download_file(lib_url, lib_path):
                        return False
        
        return True
    except Exception as e:
        print(f"Error downloading Minecraft version: {e}")
        return False

def launch_minecraft(username, jar_path):
    # Set the correct java path
    java_path = "/usr/local/jdk-21/bin/java"  # Specify the exact path to the new Java installation
    classpath = [jar_path]
    libraries_dir = os.path.expanduser("~/.minecraft/libraries")

    for root, dirs, files in os.walk(libraries_dir):
        for file in files:
            if file.endswith('.jar'):
                classpath.append(os.path.join(root, file))

    classpath_str = os.pathsep.join(classpath)

    # Generate a random UUID for the session
    session_uuid = str(uuid.uuid4())

    java_options = [
        "-Xmx1024M",
        "-Xms512M",
        "-cp", classpath_str,
        "-Djava.library.path=" + libraries_dir,
        "-Duser.home=" + os.path.expanduser("~/.minecraft"),
        "-Dlauncher.name=CustomLauncher",
        "-Dlauncher.version=1.0"  # Optional: specify the launcher version
    ]

    command = [java_path] + java_options + [
        "net.minecraft.client.main.Main",
        "--username", username,
        "--version", os.path.basename(jar_path).replace('.jar', ''),
        "--assetsDir", os.path.expanduser("~/.minecraft/assets"),
        "--gameDir", os.path.expanduser("~/.minecraft"),
        "--uuid", session_uuid,  # Use the generated UUID
        "--accessToken", "null",  # Set to null for offline mode
        "--clientid", "null",  # Set clientid to null
        "--offline"  # Indicates offline mode
    ]

    print("Launching command:")
    print(" ".join(command))
    print(f"Classpath: {classpath_str}")

    try:
        subprocess.Popen(command)
        print("Launching Minecraft...")
    except Exception as e:
        print(f"Error launching Minecraft: {e}")

def main():
    print("Welcome to the Minecraft CLI Launcher!")

    java_version = check_java_version()
    if java_version is None or java_version < 21:
        install_java()
        set_java_alternatives()  # Update alternatives after installing

    latest_version = get_latest_minecraft_version()
    if not latest_version:
        return

    if not download_minecraft_version(latest_version):
        return

    jar_path = os.path.expanduser(f"~/.minecraft/versions/{latest_version}/{latest_version}.jar")

    username = input("Enter your Minecraft Username: ")
    if not username.strip():
        print("Error: Please enter a valid username.")
        return

    launch_minecraft(username, jar_path)

if __name__ == "__main__":
    main()
