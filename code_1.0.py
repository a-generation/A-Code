import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QPixmap, QImage
from PyQt5.Qt import QRegExp
from io import BytesIO
from PIL import Image

class HTMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(HTMLHighlighter, self).__init__(parent)

        self.highlightingRules = []

        # HTML tag format
        tagFormat = QTextCharFormat()
        tagFormat.setForeground(QColor("blue"))
        tagFormat.setFontWeight(QFont.Bold)
        tagPattern = QRegExp("<[^>]*>")
        self.highlightingRules.append((tagPattern, tagFormat))

        # HTML attribute format
        attrFormat = QTextCharFormat()
        attrFormat.setForeground(QColor("red"))
        attrPattern = QRegExp("\\b\\w+(?=\\=)")
        self.highlightingRules.append((attrPattern, attrFormat))

        # HTML value format
        valueFormat = QTextCharFormat()
        valueFormat.setForeground(QColor("magenta"))
        valuePattern = QRegExp("\"[^\"]*\"(?=\\s|>)")
        self.highlightingRules.append((valuePattern, valueFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)

class HTMLViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("A-Code (HTML) v1.0")
        self.setGeometry(100, 100, 1200, 600)

        layout = QHBoxLayout()

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier", 12))
        self.highlighter = HTMLHighlighter(self.editor.document())
        self.editor.textChanged.connect(self.updatePreview)

        self.browser = QWebEngineView()
        self.error_html = """
<!DOCTYPE HTML>
<html>
<head>
    <title>Preview Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-align: left;
            font-family: monospace;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Couldn't provide preview for empty page code.</h1>
        <pre>
&lt;!DOCTYPE HTML&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;/body&gt;
&lt;/html&gt;
        </pre>
    </div>
</body>
</html>
"""
        self.browser.setHtml(self.error_html)

        layout.addWidget(self.editor)
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def updatePreview(self):
        html = self.editor.toPlainText()
        if html.strip() == "":
            self.browser.setHtml(self.error_html)
        else:
            self.browser.setHtml(html)

class BannerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(" ")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.banner = QLabel(self)
        pixmap = self.loadBannerImage()
        self.banner.setPixmap(pixmap)
        self.banner.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.banner)

        self.setLayout(layout)

        QTimer.singleShot(5000, self.closeBanner)

    def loadBannerImage(self):
        url = "https://raw.githubusercontent.com/a-generation/A-Code/main/banner_a.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGBA")
        img = img.resize((600, 400))  # Resize the image to fit 600x400
        data = img.tobytes("raw", "RGBA")
        qim = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

    def closeBanner(self):
        self.close()
        self.mainWindow = HTMLViewer()
        self.mainWindow.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    banner = BannerWindow()
    banner.show()
    sys.exit(app.exec_())
