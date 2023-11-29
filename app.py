# Developed By Sandeep Kasturi
# System Software integrated by Openai LLM Model Chatgpt

import openai
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QFileDialog, QSplashScreen, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

# System packages for Processing and Speech convertion

import subprocess
import webbrowser
import requests
from gtts import gTTS
import os

# Defining the application details

LICENSE = "BSD 2 CLAUSE"
AUTHOR = "Sandeep Kasturi"
PROJECT = "STAR GPT AI APP"
PRODUCT_NAME = "STAR GPT AI APP"
COMPANY_NAME = "Sandeep Kasturi AI Verse company"
VERSION = "17"
APPLICATION_TYPE = ".exe"

# Set up the OpenAI API

openai.api_key = "your_api_key_from_openai"


# Function to generate code using OpenAI API

def generate_code(prompt, language, engine):
    response = openai.Completion.create(
        engine=engine,
        prompt=f"{prompt} in {language}",
        max_tokens=3048,  # Set a lower value to fit within the model's maximum context length
        temperature=0.5,
        n=1,
        stop=None,
        frequency_penalty=0.4,
        presence_penalty=0.6,
        best_of=1,
    )
    code = response.choices[0].text.strip()
    return code


# Function to generate image using OpenAI API
# Function to open Notepad and write code/content

def write_to_notepad(content, is_code=True):
    try:
        if is_code:
            file_name = "star_gpt_code.txt"
        else:
            file_name = "star_gpt_content.txt"

        with open(file_name, "w+") as file:
            file.write(content)
        subprocess.Popen(["notepad.exe", file_name])
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred while writing to Notepad:\n{str(e)}")




# Function to convert text to speech using gTTS

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_file = 'prompt_answer.mp3'
        tts.save(audio_file)
        os.system(audio_file)
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred while converting text to speech:\n{str(e)}")



# Function to download and open the image

def download_and_open_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open("generated_image.png", "wb") as file:
                file.write(response.content)
            webbrowser.open("generated_image.png")
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred while generating the image:\n{str(e)}")

# Main function for code/content generation

def generate_code_or_content(prompt, language, is_content, engine):
    try:
        if is_content:
            generated_content = generate_code(prompt, language, engine)
            write_to_notepad(generated_content)
            QMessageBox.information(main_window, "Success", "Successfully generated the content")
        else:
            generated_code = generate_code(prompt, language, engine)
            write_to_notepad(generated_code)
            QMessageBox.information(main_window, "Success", "Successfully generated the code")
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred during code/content generation:\n{str(e)}")


# Function to open URLs in a web browser
def open_url(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred while opening the URL:\n{str(e)}")


class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super(SplashScreen, self).__init__(pixmap)
        self.setWindowFlags(Qt.SplashScreen)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("STAR PROGRAMMER")
        self.setWindowFlags(PyQt5.QtCore.Qt.WindowMinimizeButtonHint | PyQt5.QtCore.Qt.WindowMaximizeButtonHint)

        self.init_ui()

    def init_ui(self):
        theme_default_btn = QPushButton("Default", self)
        theme_default_btn.setGeometry(PyQt5.QtCore.QRect(20, 20, 80, 30))
        theme_default_btn.setStyleSheet("background-color: #CAADFF;")
        theme_default_btn.clicked.connect(self.theme_default_btn_clicked)

        theme_dark_btn = QPushButton("Dark", self)
        theme_dark_btn.setGeometry(PyQt5.QtCore.QRect(110, 20, 80, 30))
        theme_dark_btn.setStyleSheet("background-color: grey;")
        theme_dark_btn.clicked.connect(self.theme_dark_btn_clicked)

        theme_light_btn = QPushButton("Light", self)
        theme_light_btn.setGeometry(PyQt5.QtCore.QRect(200, 20, 80, 30))
        theme_light_btn.setStyleSheet("background-color: #D6E8DB;")
        theme_light_btn.clicked.connect(self.theme_light_btn_clicked)

        prompt_label = QLabel("Enter Prompt:", self)
        prompt_label.setGeometry(PyQt5.QtCore.QRect(20, 60, 100, 30))
        self.prompt_input = QLineEdit(self)
        self.prompt_input.setGeometry(PyQt5.QtCore.QRect(140, 60, 600, 30))

        language_label = QLabel("Request for:", self)
        language_label.setGeometry(PyQt5.QtCore.QRect(20, 100, 150, 30))
        self.language_input = QLineEdit(self)
        self.language_input.setGeometry(PyQt5.QtCore.QRect(190, 100, 550, 30))

        code_btn = QPushButton("Generate Code", self)
        code_btn.setGeometry(PyQt5.QtCore.QRect(20, 160, 150, 40))
        code_btn.setStyleSheet("background-color: #DCBFFF;")
        code_btn.clicked.connect(self.generate_code_btn_clicked)

        content_btn = QPushButton("Generate Content", self)
        content_btn.setGeometry(PyQt5.QtCore.QRect(20, 220, 150, 40))
        content_btn.setStyleSheet("background-color: #86A789;")
        content_btn.clicked.connect(self.generate_content_btn_clicked)

        image_btn = QPushButton("Generate Image", self)
        image_btn.setGeometry(PyQt5.QtCore.QRect(20, 280, 150, 40))
        image_btn.setStyleSheet("background-color: #F7EFE5;")
        image_btn.clicked.connect(self.generate_image_btn_clicked)

        tts_btn = QPushButton("Text-to-Speech", self)
        tts_btn.setGeometry(PyQt5.QtCore.QRect(20, 340, 150, 40))
        tts_btn.setStyleSheet("background-color: #A0E9FF;")
        tts_btn.clicked.connect(self.text_to_speech_btn_clicked)

        continue_code_btn = QPushButton("Continue Generating Code", self)
        continue_code_btn.setGeometry(PyQt5.QtCore.QRect(20, 400, 200, 40))
        continue_code_btn.setStyleSheet("background-color:#DCBFFF;")
        continue_code_btn.clicked.connect(self.continue_generating_code_btn_clicked)

        continue_content_btn = QPushButton("Continue Generating Content", self)
        continue_content_btn.setGeometry(PyQt5.QtCore.QRect(230, 400, 200, 40))
        continue_content_btn.setStyleSheet("background-color: #86A789;")
        continue_content_btn.clicked.connect(self.continue_generating_content_btn_clicked)

        help_btn_clicked = QPushButton("Help", self)
        help_btn_clicked.setGeometry(PyQt5.QtCore.QRect(440, 400, 120, 40))
        help_btn_clicked.setStyleSheet("background-color: #F9B572;")
        help_btn_clicked.clicked.connect(self.help_btn_clicked)

        report_btn_clicked = QPushButton("Report or Message", self)
        report_btn_clicked.setGeometry(PyQt5.QtCore.QRect(570, 400, 180, 40))
        report_btn_clicked.setStyleSheet("background-color: #8467D7")
        report_btn_clicked.clicked.connect(self.report_btn_clicked)

        open_in_view_clicked = QPushButton("Open in Web", self)
        open_in_view_clicked.setGeometry(PyQt5.QtCore.QRect(570, 400, 180, 40))
        open_in_view_clicked.setStyleSheet("background-color: #8467D7")
        open_in_view_clicked.clicked.connect(self.open_in_view_clicked)

        format_btn = QPushButton("Change File Format", self)
        format_btn.setGeometry(PyQt5.QtCore.QRect(20, 460, 180, 40))
        format_btn.setStyleSheet("background-color: lightgreen;")
        format_btn.clicked.connect(self.change_format_btn_clicked)

        download_app_btn = QPushButton("Download Apk", self)
        download_app_btn.setGeometry(PyQt5.QtCore.QRect(20, 460, 180, 40))
        download_app_btn.setStyleSheet("background-color: grey;")
        download_app_btn.clicked.connect(self.download_app_btn)

        exit_btn = QPushButton("Exit", self)
        exit_btn.setGeometry(PyQt5.QtCore.QRect(230, 460, 120, 40))
        exit_btn.setStyleSheet("background-color: tomato;")
        exit_btn.clicked.connect(self.exit_btn_clicked)

    def resizeEvent(self, event):
        if self.windowState() & PyQt5.QtCore.Qt.WindowMaximized:
            self.setGeometry(QApplication.desktop().availableGeometry().adjusted(10, 10, -10, -10))
        else:
            self.setGeometry(160, 130, 1000, 650)

    def generate_code_btn_clicked(self):
        prompt = self.prompt_input.text()
        language = self.language_input.text()
        generate_code_or_content(prompt, language, False, "text-davinci-003")

    def generate_content_btn_clicked(self):
        prompt = self.prompt_input.text()
        language = self.language_input.text()
        generate_code_or_content(prompt, language, True, "text-davinci-003")

    def generate_image_btn_clicked(self):
        # Display information message
        QMessageBox.information(self, "Info", "Sorry, we are working on that. We will update this in the future.")

        # Ask the user if they want to redirect to a third-party AI image generating tool
        response = self.show_yes_no_dialog("Do you want me to Redirect to third-party AI image generating tool?")

        if response == "Yes":
            # Redirect to sample.com
            self.webbrowser.open("https://bing.com/create")
        else:
            # Display a message if the user chooses not to redirect
            QMessageBox.information(self, "Info", "Okay, you said no.")

    def show_yes_no_dialog(self, message):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Question)
        dialog.setText(message)
        dialog.setWindowTitle("Confirmation")

        # Add Yes and No buttons
        dialog.addButton(QMessageBox.Yes)
        dialog.addButton(QMessageBox.No)

        # Set the default button to No
        dialog.setDefaultButton(QMessageBox.No)

        # Show the dialog and return the user's choice
        return dialog.exec_()

    def redirect_to_website(self, url):
        # Code to redirect to the specified website goes here
        pass
    def text_to_speech_btn_clicked(self):
        prompt = self.prompt_input.text()
        text_to_speech(prompt)

    def continue_generating_code_btn_clicked(self):
        language = self.language_input.text()
        generate_code_or_content("", language, False, "text-davinci-003")

    def continue_generating_content_btn_clicked(self):
        language = self.language_input.text()
        generate_code_or_content("", language, True, "text-davinci-003")

    def help_btn_clicked(self):
        open_url("https://github.com/sandeepkasturi")  # Replace with the actual GitHub link

    def report_btn_clicked(self):
        open_url("https://instagram.com/sandeep_kasturi_")

    def download_app_btn(self):
        open_url("https://mega.nz/file/asVVhRyL#MZZS7TZ9c0iO5hGNa3WIzEcMaxquTXGoSZ-7odSBfw0")

    def open_in_view_clicked(self):
        open_url("https://star-programmer.vercel.app")

    def change_format_btn_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = file_dialog.getSaveFileName(self, "Change File Format", "",
                                                   "All Files (*);; Plain Text Files (*.txt);; Windows Batch Files (*.bat);; VB Script Files (*.vbs);; Java Files (*.java);; Bash Files (*.sh);; HTML Files (*.html);;CSS Files (*.css);;JavaScript Files (*.js);;Python Files (*.py)",
                                                   options=options)
        if file_path:
            file_extension = os.path.splitext(file_path)[1]
            QMessageBox.information(self, "Info", f"Selected file format: {file_extension}")

    def exit_btn_clicked(self):
        QMessageBox.information(self, "warning:", "Are you sure? You want to exit the application")
        if 1:
            sys.exit()
        else:
            sys.exit()

    def theme_default_btn_clicked(self):
        PyQt5.QtWidgets.QApplication.setStyle(PyQt5.QtWidgets.QStyleFactory.create("Fusion"))

    def theme_dark_btn_clicked(self):
        PyQt5.QtWidgets.QApplication.setStyle(PyQt5.QtWidgets.QStyleFactory.create("Fusion"))
        palette = PyQt5.QtGui.QPalette()
        palette.setColor(PyQt5.QtGui.QPalette.Window, PyQt5.QtGui.QColor(53, 53, 53))
        palette.setColor(PyQt5.QtGui.QPalette.WindowText, PyQt5.QtCore.Qt.white)
        palette.setColor(PyQt5.QtGui.QPalette.Base, PyQt5.QtGui.QColor(25, 25, 25))
        palette.setColor(PyQt5.QtGui.QPalette.AlternateBase, PyQt5.QtGui.QColor(53, 53, 53))
        palette.setColor(PyQt5.QtGui.QPalette.ToolTipBase, PyQt5.QtCore.Qt.white)
        palette.setColor(PyQt5.QtGui.QPalette.ToolTipText, PyQt5.QtCore.Qt.white)
        palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.white)
        palette.setColor(PyQt5.QtGui.QPalette.Button, PyQt5.QtGui.QColor(53, 53, 53))
        palette.setColor(PyQt5.QtGui.QPalette.ButtonText, PyQt5.QtCore.Qt.white)
        palette.setColor(PyQt5.QtGui.QPalette.BrightText, PyQt5.QtCore.Qt.red)
        palette.setColor(PyQt5.QtGui.QPalette.Link, PyQt5.QtGui.QColor(42, 130, 218))
        palette.setColor(PyQt5.QtGui.QPalette.Highlight, PyQt5.QtGui.QColor(42, 130, 218))
        palette.setColor(PyQt5.QtGui.QPalette.HighlightedText, PyQt5.QtCore.Qt.black)
        PyQt5.QtWidgets.QApplication.setPalette(palette)

    def theme_light_btn_clicked(self):
        PyQt5.QtWidgets.QApplication.setStyle(PyQt5.QtWidgets.QStyleFactory.create("Fusion"))
        PyQt5.QtWidgets.QApplication.setPalette(PyQt5.QtWidgets.QApplication.style().standardPalette())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load your splash screen image
    splash_pixmap = QPixmap("star-png.png")  # Replace with your actual path
    splash = SplashScreen(splash_pixmap)

    # Create a stacked widget to manage splash screen and main window
    stacked_widget = QStackedWidget()
    stacked_widget.addWidget(splash)

    # Create the main window
    main_window = MainWindow()
    stacked_widget.addWidget(main_window)

    stacked_widget.show()

    # Set up a timer to switch to the main window after 4 seconds
    switch_timer = QTimer()
    switch_timer.timeout.connect(lambda: stacked_widget.setCurrentIndex(1))
    switch_timer.start(4000)

    app.exec_()
    sys.exit()

# MIT License Approved Project
# BSD Clause 2 License Approved Project
# General Public License Approved Project
# Developed and Production, Management -- Sandeep Kasturi 21030-CM-136. Founder of Sandeep Kasturi AI Verse (SKAV)
# https://sandeepkasturiaiverse.mydurable.com/
