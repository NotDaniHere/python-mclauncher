import subprocess
import os
import minecraft_launcher_lib
import sys
import PySimpleGUI as sg



def launch_minecraft(version_type):


    options = {
    "username": "testname",
    }

    if version_type == "fabric":
        latest_version = "fabric-loader-0.14.12-1.19.3"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)
        subprocess.run(minecraft_command)
    if version_type == "vanilla":
        latest_version = "1.19.3"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)
        subprocess.run(minecraft_command)


layout = [[sg.Button('Launch Minecraft Fabric', command=launch_minecraft("vanilla"))],]
window = sg.Window('Python Minecraft Launcher', layout)


while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    window.close()






