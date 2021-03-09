# autosage.py
Automatically BeatSage entire youtube playlists for Beat Saber

A Python script by Alan

Get started:

1. Download autosage.py to your computer.
2. Put autosage.py in your custom levels folder (not required but recommended)
3. Open up your terminal/shell of choice, navigate to your custom levels folder or wherever the script is located, and do 

        python autosage.py
4. This will launch the script, and it will explain how to use every option currently available on BeatSage within the script
5. Enjoy!

Note: This script relies on files not being added or removed from the folder the script resides in, while it is running. Don't add, create, or remove any files from wherever you placed autosage.py while its running or it may crash!

Example command you can give it, and what it will do:

    python autosage.py https://www.youtube.com/playlist?list=PLadVUcdkRukIb_ekf5J1_ErGPsohB6wE2 e ep b o s 90 origins v2

    e, ep
Chooses expert and expert plus difficulties for every song in the playlist respectively
    b, o
b option turns on bombs, and o option turns on obstacles
    s 90
These two options select Standard mode and 90 Degree mode
    origins
Tells BeatSage you want the environment for every song to be Origins (remember that in game you can always change these anyways!)
    v2
Tells BeatSage you want the model version to be the V2 algorithm
