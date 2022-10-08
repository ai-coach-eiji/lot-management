[Japanese/<a href="https://github.com/ai-coach-eiji/lot-management/blob/main/README_EN.md">English</a>]

# lot-management
Hope this helps your lot management.

# How does it work?
1. When you press the 'Scan' button, the VideoCapture module of OpenCV starts and take 1 frame.
2. If there is a QRcode in the image, the decode contents will be written in that image using pyzbar module.
3. The results displayed in the screen.

# How to use it?
1. Just press the 'Scan' button in the screen.
2. You get the contents of QRcode in csv file.

# ToDo
Local Config
---
- [x] ~~Display the snapshot image~~
- [x] ~~Read the QRcode image~~
- [ ] Replace the background with video input
- [ ] Outputs the decode contents as csv file

Production Config
---
- [ ] Check with iPhone

# Reference
- OpenCV: [カメラから動画を撮影する](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_video_display/py_video_display.html)
- Materialize: [アプリ画面のレイアウト](https://materializecss.com/carousel.html)
- Filip Němeček's Blog: [画像の表示方法](https://nemecek.be/blog/8/django-how-to-send-image-file-as-part-of-response)
- Qiita: [QRコードを読み取る方法](https://qiita.com/igor-bond16/items/0dbef691a71c2e5e37d7)
- PyPi: [pyzbarのインストール（Mac）](https://pypi.org/project/pyzbar/)
- stackoverflow: [pyzbarのインストール（Colab）](https://stackoverflow.com/questions/63217735/import-pyzbar-pyzbar-unable-to-find-zbar-shared-library)
- Qiita: [デコード内容（リスト）が空の場合の判定方法](https://qiita.com/yonedaco/items/d0f65ca3dad2e085a51d)
- KinoCode: [PythonでGoogleスプレッドシートを読み込む方法](https://kino-code.com/python_spreadsheets/)
- WATLAB Blog: [画像に日本語を描画する方法](https://watlab-blog.com/2019/08/25/image-text/)
- Google Fonts: [小杉丸フォント](https://fonts.google.com/specimen/Kosugi+Maru?selection.family=Kosugi+Maru&sidebar.open=true#standard-styles)
- deecode blog: [StreamingHttpResponseを使ったカメラストリーミング](https://deecode.net/?p=382)



# Author
北島栄司 （[https://twitter.com/1220castillo](https://twitter.com/1220castillo)）

# License
- This project is licensed under the MIT License - see the [LICENSE](https://github.com/ai-coach-eiji/lot-management/blob/main/LICENSE) file for details.