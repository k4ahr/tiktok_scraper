# MÁY DẬP TIKTOK

> Script crawler python để tải xuống và crawl dữ liệu của một video TikTok.

# Các tính năng chính
* Xuất dữ liệu của video TikTok
* Tải xuống video TikTok
* ~~Hỗ trợ cả video YouTube (nếu như config lại)~~
* In ra một con fumo ᗜˬᗜ

# Tuỳ chọn
* Tại dòng số 200, bạn có thể chỉnh `debug=True` để xuất toàn bộ HTML ra một file riêng để debug trong trường hợp file JSON không chứa dữ liệu

# Dependencies
* python
* requests
* yt-dlp

# Cài đặt

* Đầu tiên là ta sẽ phải có ngôn ngữ [Python](https://www.python.org/) cài đặt trên hệ thống cùng package installer [pip](https://pypi.org/project/pip/)

* Ta sẽ cần tải về một vài thư viện, sử dụng câu lệnh:

```bash
$ pip install -r requirements.txt
```

* Chạy chương trình chính:

```bash
$ python may_dap_tiktok.py
```


# Tại sao script không sử dụng bs4 ????
* *Vì TikTok không dùng thẻ HTML thông thường để hiển thị video. Thay vào đó, dữ liệu video được nhúng sẵn trong một thẻ <script> dạng JSON. Do đó, chỉ cần dùng re (regex) để trích xuất khối JSON và json.loads() để xử lý là đủ. Chính vì vậy nên mình nghĩ rằng sử dụng bs4 là không cần thiết và sẽ làm chậm chương trình.*

# Credit

<img src="https://raw.githubusercontent.com/k4ahr/dotfilesV2/refs/heads/main/.config/neofetch/osage.png" align="right" width="200px">

* Dữ liệu HTML công khai từ [TikTok](https://www.tiktok.com)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp): Thư viện mã nguồn mở để tải video trên các nền tảng
* [Art fumo cirno ASCII](https://emojicombos.com/cirno-fumo-ascii)
* Copilot ở trong Visual Studio Code để fix bug
* [Nỗ lực sử dụng bs4](https://stackoverflow.com/questions/59962476/tiktok-webscraping-using-beautifulsoup-but-not-getting-video-urls-or-video-ids) để tải video trên tiktok
* Slide số 6 của anh Tiến Đức
