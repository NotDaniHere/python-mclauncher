#Minecraft Launcher

import subprocess
import os
import minecraft_launcher_lib
import sys

launcherVersion = 'v0.12a'
launcherProductionStatus = 'Private'
minecraftVersion = "1.19.3"
getFromGithubResources = "https://github.com/NotDaniHere/python-mclauncher-resources/raw/main/"
sodium = 'sodium-fabric-mc1.19.3-0.4.6+build.20.jar'
betterf3 = 'BetterF3-5.0.0-Fabric-1.19.3-pre2.jar'
kotlin = 'fabric-language-kotlin-1.8.7+kotlin.1.7.22.jar'
appleskin = 'appleskin-fabric-mc1.19.3-2.4.2.jar'
authme = 'authme-mc1.19.3-5.0.0.jar'
bookshelf = 'Bookshelf-Fabric-1.19.3-17.0.2.jar'
clothconfig = 'cloth-config-9.0.94-fabric.jar'
clumps = 'Clumps-fabric-1.19.3-9.0.0+15.jar'
collective = 'collective-fabric-1.19.3-5.45.jar'
enchantmentdescription = 'EnchantmentDescriptions-Fabric-1.19.3-14.0.2.jar'    
fabricapi = 'fabric-api-0.69.1+1.19.3.jar'
fpsreducer = 'FpsReducer2-fabric-1.19.3-2.2.jar'
fullbright = 'fullbrightnesstoggle-fabric_1.19.3-2.3.jar'
journeymap = 'journeymap-1.19.3-5.9.0-fabric.jar'
lazydfu = 'lazydfu-0.1.3.jar'
litematica = 'litematica-fabric-1.19.3-0.13.0.jar'
malilib = 'malilib-fabric-1.19.3-0.14.0.jar'
memoryleakfix = 'memoryleakfix-1.19.3-0.7.0.jar'
modmenu = 'modmenu-5.0.2.jar'
reesessodium = 'reeses_sodium_options-1.4.9+mc1.19.2-build.67.jar'
replaymod = 'replaymod-1.19.3-2.6.10.jar'
tlskincape = 'tl_skin_cape_fabric_1.19.2-1.27.jar'
voicechat = 'voicechat-fabric-1.19.3-2.3.24.jar'
yetanotherconfigmod = 'YetAnotherConfigLib-2.1.1.jar'
zoomify = 'Zoomify-2.9.2.jar'
fabricmodloader = "fabric-loader-0.14.12-1.19.3.jar"
fabricmodloaderjson = "fabric-loader-0.14.12-1.19.3.json"
args = ["-Xmx1024M", "-Xms512M", "-jar", "%appdata%/python-mclauncher/fabric-loader-0.14.12-1.19.3/fabric-loader-0.14.12-1.19.3.jar"]


def customLaunchMinecraft():
    subprocess.run(["java", *args])

def printProductionStatus():
    print("Current launcher production status is " + launcherProductionStatus + " and Launcher Version " + launcherVersion)

def makeMCDirectories():
    os.system("cd %appdata% && mkdir python-mclauncher")  

def useFabricMC():
    vanilla_version = "1.19.3"
    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(vanilla_version):
        print("This version is not supported by fabric")
        sys.exit(0)
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    callback = {
        "setStatus": lambda text: print(text)
    }
    minecraft_launcher_lib.fabric.install_fabric(vanilla_version, minecraft_directory, callback=callback)

version = "fabric-loader-0.14.12-1.19.3"


minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
print("Insert your Minecraft Username")
options = {
    "username": input()
}


minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)



if __name__ == "__main__":
    useFabricMC()

def getFabricMods():
    os.system("cd %appdata%/python-mclauncher && mkdir mods && cd mods && curl.exe -o " + getFromGithubResources + sodium)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + betterf3)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + kotlin)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + appleskin)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + authme)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + bookshelf)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + clothconfig)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + clumps)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + collective)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + enchantmentdescription)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + fabricapi)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + fpsreducer)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + fullbright)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + journeymap)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + lazydfu)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + litematica)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + malilib)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + modmenu)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + reesessodium)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + replaymod)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + tlskincape)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + voicechat)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + yetanotherconfigmod)
    os.system("cd %appdata%/python-mclauncher && cd mods && curl.exe -O " + getFromGithubResources + zoomify)





# Start Minecraft
printProductionStatus()
subprocess.call(minecraft_command)