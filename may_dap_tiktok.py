import json
import requests
from datetime import datetime
import os
import re
import yt_dlp # Dung de download video (im desperated)



class MayDapTikTok:
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug
        self.output_dir = "./tiktok" # Duong dan luu tru video/JSON
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"     # Su dung headers de vuot WAF (https://en.wikipedia.org/wiki/Web_application_firewall)
        }
        os.makedirs(self.output_dir, exist_ok=True)         # Tao thuc muc luu tru neu chua co


    def print_ascii_banner():
        banner = r"""
⠀⢀⣒⠒⠆⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⡛⠛⠻⣷⣶⣦⣬⣕⡒⠤⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡿⢿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣳⠖⢋⣩⣭⣿⣶⡤⠶⠶⢶⣒⣲⢶⣉⣐⣒⣒⣒⢤⡀⠀⠀⠀⠀⠀⠀⠀
⣿⠀⠉⣩⣭⣽⣶⣾⣿⢿⡏⢁⣴⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠉⠙⠲⢭⣯⣟⡿⣷⣘⠢⡀⠀⠀⠀⠀⠀
⠹⣷⣿⣿⣿⣿⣿⢟⣵⠋⢠⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣾⣦⣾⣢⠀⠀⠀⠀
⠀⠹⣿⣿⣿⡿⣳⣿⠃⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⠟⠀⠀⠀⠀
⠀⠀⠹⣿⣿⣵⣿⠃⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠛⣯⡇⠛⣽⣦⣿⠀⠀⠀⠀⢀⠔⠙⣄⠀⠀⠀⠀⠀⠀⣠⠳⡀⠀⠀⠀⠀⢿⡵⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣸⣿⣿⣿⠿⢿⠟⠀⠀⠀⢀⡏⠀⠀⠘⡄⠀⠀⠀⠀⢠⠃⠀⠹⡄⠀⠀⠀⠸⣿⣷⡀⠀⠀⠀
⠀⠀⠀⢰⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⢸⠒⠤⢤⣀⣘⣆⠀⠀⠀⡏⢀⣀⡠⢷⠀⠀⠀⠀⣿⡿⠃⠀⠀⠀
⠀⠀⠀⠸⣿⣿⠟⢹⣥⠀⠀⠀⠀⠀⣸⣀⣀⣤⣀⣀⠈⠳⢤⡀⡇⣀⣠⣄⣸⡆⠀⠀⠀⡏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠁⠀⢸⢟⡄⠀⠀⠀⠀⣿⣾⣿⣿⣿⣿⠁⠀⠈⠙⠙⣯⣿⣿⣿⡇⠀⠀⢠⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠇⢨⢞⢆⠀⠀⠀⡿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⣿⣿⣿⡿⡇⠀⣠⢟⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡼⠀⢈⡏⢎⠳⣄⠀⡇⠙⠛⠟⠛⠀⠀⠀⠀⠀⠀⠘⠻⠛⢱⢃⡜⡝⠈⠚⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣅⠁⢸⣋⠈⢣⡈⢷⠇⠀⠀⠀⠀⠀⣄⠀⠀⢀⡄⠀⠀⣠⣼⢯⣴⠇⣀⡀⢸⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠳⡌⠛⣶⣆⣷⣿⣦⣄⣀⠀⠀⠀⠈⠉⠉⢉⣀⣤⡞⢛⣄⡀⢀⡨⢗⡦⠎⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠪⣿⠁⠀⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠉⠁⢸⠀⠀⠀⠄⠙⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠚⡉⢳⡄⠡⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠁⣠⣧⣤⣄⣀⡀⡰⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⠔⠉⠀⠀⠀⠀⢀⣧⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣅⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠆⠀⠀⠀⣀⣼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠁⣠⠖⠒⠒⠛⢿⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠑⠤⠴⠞⢋⣵⣿⢿⣿⣿⣿⣿⣿⣿⠗⣀⠀⠀⠀⠀⠀⢰⠇⠀⠀⠀⠀⢀⡼⣶⣤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠟⢛⣿⠀⠙⠲⠽⠛⠛⠵⠞⠉⠙⠳⢦⣀⣀⡞⠀⠀⠀⠀⡠⠋⠐⠣⠮⡁⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣎⡀⢀⣾⠇⢀⣠⡶⢶⠞⠋⠉⠉⠒⢄⡀⠉⠈⠉⠀⠀⠀⣠⣾⠀⠀⠀⠀⠀⢸⡀
⠀⠀⠀⠀⠀⠀⠀⠘⣦⡀⠘⢁⡴⢟⣯⣞⢉⠀⠀⠀⠀⠀⠀⢹⠶⠤⠤⡤⢖⣿⡋⢇⠀⠀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠵⠗⠺⠟⠖⢈⡣⡄⠀⠀⠀⠀⢀⣼⡤⣬⣽⠾⠋⠉⠑⠺⠧⣀⣤⣤⡠⠟⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠷⠶⠦⠶⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                        
 __  __    _ __   __  ____    _    ____    _____ ___ _  _______ ___  _  __
|  \/  |  / \\ \ / / |  _ \  / \  |  _ \  |_   _|_ _| |/ /_   _/ _ \| |/ /
| |\/| | / _ \\ V /  | | | |/ _ \ | |_) |   | |  | || ' /  | || | | | ' / 
| |  | |/ ___ \| |   | |_| / ___ \|  __/    | |  | || . \  | || |_| | . \ 
|_|  |_/_/   \_\_|   |____/_/   \_\_|       |_| |___|_|\_\ |_| \___/|_|\_\

                                                        By K4ahr             


    """
        print(banner)


    def validate_url(self): # Check URL hop le
        pattern = r"(https?://(vm|vt|www)\.tiktok\.com/[\w/]+/?|https?://www\.tiktok\.com/@[\w\.-]+/video/\d+)" # Su dung regex de kiem tra URL
        if not re.match(pattern, self.url):
            print("[Error] Day khong phai URL TikTok ????")
            return False
        return True



    def get_final_url(self): # Doi tu link shorten sang URL goc
        try:
            response = requests.head(self.url, allow_redirects=True, timeout=10)
            final_url = response.url
            print(f"[Info] URL goc: {final_url}")
            self.url = final_url  
            return True
        except requests.RequestException as e:
            print(f"[Error] Khong the xu li URL goc: {e}")
            return False
        

    def fetch_html(self): # Scrape HTML cua video
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = response.text
            print(f"[Info] Nhap du lieu HTML thanh cong voi: {len(html)} ky tu")
            return html
        except requests.RequestException as e:
            print(f"[Error] Nhap du lieu HTML that bai: {e}")
            return None

    def extract_video_data(self, html): # Xuat block script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" tu HTML
        try:
            match = re.search(
                r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.+?)</script>',
                html
            )
            if not match:
                print("[Error] Could not find __UNIVERSAL_DATA_FOR_REHYDRATION__ block.")
                return None

            json_text = match.group(1)
            data = json.loads(json_text)
            # Xuat du lieu tu block script
            item = data["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]

            # Tach hashtag va mo ta video
            raw_desc = item.get("desc", "")
            hashtags = re.findall(r"#(\w+)", raw_desc)
            desc_only = re.sub(r"#\w+", "", raw_desc).strip()

            video_data = {
                "id": item["id"],
                "desc": desc_only,
                "author": item["author"]["uniqueId"],
                "duration": item["video"]["duration"],
                "views": item["stats"]["playCount"],
                "likes": item["stats"]["diggCount"],
                "comments": item["stats"]["commentCount"],
                "saves": item["stats"]["collectCount"],
                "hashtags": hashtags
            }
            print(f"[Info] Trich xuat du lieu thanh cong video ID: {video_data['id']}")
            return video_data
        
        except Exception as e:
            print(f"[Error] Trich xuat du lieu that bai: {e}")
            return None


    def save_json(self, data):
        # Xuat file data JSON
        os.makedirs("tiktok", exist_ok=True)
        filename = f"tiktok/tiktok_{data['id']}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f: # Luu du lieu JSON voi utf-8 cho ky tu tieng Viet
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[Success] Luu thanh cong JSON duoi file {filename}")
        except Exception as e:
            print(f"[Error] Khong the luu JSON: {e}")

    
    def save_html_debug(self, html):
        # Xuat file HTML de debug
        with open("tiktok/debug_tiktok.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("[Debug] Da luu HTML vao debug_tiktok.html")


    def download_with_ytdlp(self): # Su dung thu vien yt-dlp de download video
        try:
            print("[Info] Dang su dung yt-dlp de tai video...")

            ydl_opts = {
                'outtmpl': 'tiktok/tiktok_%(id)s.%(ext)s',
                'format': 'mp4',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

        except Exception as e:
            print(f"[Error] yt-dlp tai video that bai: {e}")






    def run(self):
        # Chay scraper
        if not self.validate_url():  # Check URL hop le
            return
        if not self.get_final_url(): # Doi tu link shorten sang URL goc
            return
        html = self.fetch_html() # Lay HTML
        if not html:
            return
        if self.debug:
            self.save_html_debug(html)        
        video_data = self.extract_video_data(html) # Trich xuat du lieu video
        if video_data: # Neu trich xuat thanh cong
            self.save_json(video_data)  # Luu du lieu JSON
            self.download_with_ytdlp() # Tai video bang yt-dlp


        



# Main function de hoat dong va input tu nguoi dung
def main():
    try:
        MayDapTikTok.print_ascii_banner() # In ra con fumo
        input_url = input("Nhap URL TikTok: ").strip() # Nhap URL tu nguoi dung
        scraper = MayDapTikTok(input_url, debug=False) # Set debug=True de luu HTML
        scraper.run()
    except KeyboardInterrupt:
        print("\n[Info] Thoat chuong trinh (phat hien nguoi dung Ctrl+C)")




if __name__ == "__main__":
    main()
