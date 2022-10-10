[<a href="https://github.com/ai-coach-eiji/lot-management">Japanese</a>/English]

# lot-management
Hope this helps your lot management.

# How does it work?
1. The VideoCapture module of OpenCV will run and take 1 frame when you press the 'Scan' button.
2. If there is a QRcode in the image, the decode contents will be written in that image using pyzbar module.
3. The results will be displayed in the screen.

# How to use it?
1. Just press the 'Scan' button in the screen.
2. You will see the contents of QRcode in the screen.
3. The results will be written in the Google spred sheet.

# ToDo
Local Config
---
- [x] ~~Display the snapshot image~~
- [x] ~~Read the QRcode image~~
- [x] ~~Replace the background with video input~~
- [ ] Add the scan sound
- [x] ~~Integrate prd. and ship. sheets~~
- [x] ~~Create the update sheets system~~
- [x] ~~Create the output csv system~~
- [x] ~~Create the submit sheets system~~
- [x] ~~Create signUp system~~

Production Config
---
- [ ] Check with iPhone
- [x] ~~Chenge the scan process from backend to frontend~~
- [ ] Confirm the Google auth in production

# Reference
- OpenCV: [Reading images](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_video_display/py_video_display.html)
- Materialize: [App layout(EN)](https://materializecss.com/carousel.html)
- Filip Němeček's Blog: [How to display images in the screen?](https://nemecek.be/blog/8/django-how-to-send-image-file-as-part-of-response)
- Qiita: [How to decode QRcode images?(JA)](https://qiita.com/igor-bond16/items/0dbef691a71c2e5e37d7)
- PyPi: [pyzbar install for Mac()](https://pypi.org/project/pyzbar/)
- stackoverflow: [pyzbar install for Colab(EN)](https://stackoverflow.com/questions/63217735/import-pyzbar-pyzbar-unable-to-find-zbar-shared-library)
- Qiita: [How to check if list is empty?(JA)](https://qiita.com/yonedaco/items/d0f65ca3dad2e085a51d)
- KinoCode: [How to read google spredsheet using python?(JA)](https://kino-code.com/python_spreadsheets/)
- WATLAB Blog: [How to draw japanese text in the image?(JA)](https://watlab-blog.com/2019/08/25/image-text/)
- Google Fonts: [Kosugi Maru](https://fonts.google.com/specimen/Kosugi+Maru?selection.family=Kosugi+Maru&sidebar.open=true#standard-styles)
- deecode blog: [Camera streaming with 'StreamingHttpResponse'(JA)](https://deecode.net/?p=382)
- stackoverflow: [Convert image from url to Base64(EN)](https://stackoverflow.com/questions/22172604/convert-image-from-url-to-base64#answer-22172860)
- Pystyle: [How to convert the image to base64 format(JA)](https://pystyle.info/opencv-convert-image-to-base64/)
- Qiita: [How to get japanese datetime?(JA)](https://qiita.com/keisuke0508/items/df2594770d63bf124ccd)
- stackoverflow: [How to convert empty cells into None value?(EN)](https://stackoverflow.com/questions/38442634/googlesheet-apiv4-getting-empty-cells)
- stackoverflow: [Find index of all rows with null value(EN)](https://stackoverflow.com/questions/44869327/find-index-of-all-rows-with-null-values-in-a-particular-column-in-pandas-datafra)
- stackoverflow: [How to open a materialize modal without btn?(EN)](https://stackoverflow.com/questions/40430576/how-i-can-open-a-materialize-modal-when-a-window-is-ready)
- DelftStack: [How to get index of row?(EN)](https://www.delftstack.com/ja/howto/python-pandas/pandas-get-index-of-row/)
- stackoverflow: [Get selected value in dropdown(EN)](https://stackoverflow.com/questions/1085801/get-selected-value-in-dropdown-list-using-javascript)
- Web-tsuku: [How to create input form with digit limit?(JA)](https://web-tsuku.life/input-only-number-digit/)
- azukipan blog: [How to create a required form?(JA)](https://www.azukipan.com/posts/javascript-form-disabled/)
- Qiita: [How to use Object.entries()?(JA)](https://qiita.com/wifeofvillon/items/15359535a834832e08ea)
- Qiita: [How to pass a value from template to js?(JA)](https://qiita.com/satsukiya/items/ee6746a8dad6d042d2f1)
- Qiita: [How to download csv file in Django?(JA)](https://qiita.com/vossibop/items/258a147f185da5c480d4)
- FANTOM: [The config when downloading csv file in Django(JA)](https://blog.fantom.co.jp/2019/06/06/set-the-character-code-of-the-downloaded-csv-to-shift-jis-by-django/)
- codegrepper: [get selected option id javascript(EN)](https://www.codegrepper.com/code-examples/javascript/get+selected+option+id+javascript)
- stackoverflow: [How to convert string to intin Pandas?(EN)](https://stackoverflow.com/questions/42719749/pandas-convert-string-to-int)
- CODING W/RICKY: [Plotting with Plotly + Django(EN)](https://www.codingwithricky.com/2019/08/28/easy-django-plotly/)
- plotly: [Text on scatter plots with Graph Objects(EN)](https://plotly.com/python/text-and-annotations/)
- pandas doc: [pandas.Series.shift(EN)](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.shift.html#pandas-series-shift)
- stackoverflow: [Deleting a specific cell and shifting up(EN)](https://stackoverflow.com/questions/64672380/gspread-deleting-a-specific-cell-and-shifting-up)
- django-allauth: [django-allauth Doc(EN)](https://django-allauth.readthedocs.io/en/latest/providers.html)
- django Doc: [release-notes(EN)](https://django-allauth.readthedocs.io/en/latest/release-notes.html#section-5)
- Google Identity: [Sign-In Branding Guidelines(EN)](https://developers.google.com/identity/branding-guidelines#padding)
- pythonanywhere: [How to set environment variables for your web apps?(EN)](https://help.pythonanywhere.com/pages/environment-variables-for-web-apps)
- stackoverflow: [Draw video on canvas(EN)](https://stackoverflow.com/questions/33834724/draw-video-on-canvas-html5)
- stackoverflow: [Horizontally flipping(EN)](https://stackoverflow.com/questions/47742208/horizontally-flipping-getusermedias-webcam-image-stream)
- stackoverflow: [flip img in canvas without scaling(EN)](https://stackoverflow.com/questions/29237305/how-to-flip-an-image-with-the-html5-canvas-without-scaling)
REFFECT: [How to display webcam frames in the browser?(JA)](https://reffect.co.jp/html/javascript-webcamera)
- stackoverflow: [Select native for IOS & Android(EN)](https://stackoverflow.com/questions/60307437/materializecss-select-native-for-ios-android)



# Author
Eiji Kitajima （[https://twitter.com/1220castillo](https://twitter.com/1220castillo)）

# License
- This project is licensed under the MIT License - see the [LICENSE](https://github.com/ai-coach-eiji/lot-management/blob/main/LICENSE) file for details.