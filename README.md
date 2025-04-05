# M3U_MAX
A simple Python script to create and host your own IPTV .m3u playlists on Android using Termux — no root or PC required.

Install Termux

**Use F-Droid version (not from Play Store):**  
https://f-droid.org/en/packages/com.termux/

After installation, give storage permission:

```termux-setup-storage```


---

2. Update Termux & Install Dependencies

Run these commands in Termux:

pkg update && pkg upgrade -y
pkg install python git tmux -y
pip install requests cloudscraper pyfiglet colorama tmuxp


---

Usage

1. Download or Move the Folder

Place the M3U-MAX folder (with pmaker2.py) into your internal storage:

/storage/emulated/0/M3U-MAX/

Then in Termux:

cd ~/storage/shared/M3U-MAX
python pmaker2.py


---

2. Follow Script Instructions

Paste .m3u8 links one by one

Select category for each (Movies, Sports, etc.)

Type DONE when finished

Enter the playlist file name (e.g., mytv.m3u)


Your playlist will be saved in internal storage.


---

Hosting Your Playlist

1. Get your IP address:

ifconfig

Look for something like 192.168.1.x under wlan0.


2. Host your playlist file:

cd ~/storage/shared
python -m http.server 8080


3. Access the playlist via browser or IPTV player:



http://192.168.1.x:8080/mytv.m3u

Use this URL inside NS Player, TiviMate, etc.


---

Sniffing .m3u8 Links (Kiwi Method)

1. Install Kiwi Browser from the Play Store


2. Open Chrome Web Store inside Kiwi


3. Search and install:
M3U8 Sniffer TV – Find and Play HLS Streams


4. Play any video on a live Channel Stream Site


5. Tap the extension icon and copy the .m3u8 link


6. Paste it into pmaker2.py to add to your playlist




---

License

This project is licensed under the MIT License.
Free to use, modify, and share with credit.
