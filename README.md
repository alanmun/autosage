# autosage.py
Automatically BeatSage entire youtube playlists for Beat Saber

A Python script by Alan

**Dependencies: (aka what you need to even use it)**
- Python (works with 3.9.x, but it might work with older Python versions as well)
- FireFox browser (just need to install FireFox on your computer, the script will open FireFox in the background to access the website)
- selenium (you can quickly install selenium by doing: `pip install selenium` in terminal once Python is installed)

**Get started:**

1. Download autosage.py to your computer.
2. Put autosage.py in your custom levels folder (not required but recommended)
3. Open up your terminal/shell of choice, navigate to your custom levels folder or wherever the script is located, and do 

        python autosage.py
4. This will launch the script, and it will explain how to use every option currently available on BeatSage within the script
5. Enjoy!

**Note:** This script relies on files not being added or removed from the folder the script resides in, while it is running. Don't add, create, or remove any files from wherever you placed autosage.py while its running or it may crash!

**Example:** Here is a command you can give it, and what it will do:

`python autosage.py https://www.youtube.com/playlist?list=PLadVUcdkRukIb_ekf5J1_ErGPsohB6wE2 e ep b o s 90 origins v2`
>e and ep

Chooses expert and expert plus difficulties for every song in the playlist respectively
>b and o

b option turns on bombs, and o option turns on obstacles
>s and 90

These two options select Standard mode and 90 Degree mode
>origins

Tells BeatSage you want the environment for every song to be Origins (remember that in game you can always change these anyways!)
>v2

Tells BeatSage you want the model version to be the V2 algorithm

If you find this tool really helpful, maybe consider giving me a tip at: ko-fi.com/epinephrine
