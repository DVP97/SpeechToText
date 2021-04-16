#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout, QFileDialog, QLabel)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from moviepy.editor import *
import speech_recognition as sr
import pruebaBusqueda


class MainWindow(QMainWindow):
    def __init__(self):

        # inicializar UI
        super(MainWindow,self).__init__()
        loadUi("SI_main.ui",self)

        # variables       
        self.ruta = ""
        self.dir = ""

        # definir elementos de la UI y acciones/funciones asociadas
        self.setWindowTitle("Speech to text from .mp4")

        # Video y Media Player
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()

        # Botones video
        self.search_button.clicked.connect(self.openFile)
        self.play_button.clicked.connect(self.play_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)

        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        
        # Controles video
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.media_player.volume())
        self.seek_slider.sliderMoved.connect(self.media_player.setPosition)
        self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        self.media_player.positionChanged.connect(self.seek_slider.setValue)
        self.media_player.durationChanged.connect(partial(self.seek_slider.setRange, 0))
        self.media_player.stateChanged.connect(self.state_changed)
        self.video_widget.installEventFilter(self)

        #Textos: Botones y campos de texto
        self.save_button_org.clicked.connect(self.save_txt)
        self.save_button_mod.clicked.connect(self.save_txt)
        self.save_button_tag.clicked.connect(self.save_txt)
        self.procesar_txt_button.clicked.connect(self.procesar_txt)
        


    # pulsar boton play
    def play_clicked(self):
        if (self.media_player.state() in
            (QMediaPlayer.PausedState, QMediaPlayer.StoppedState)):
            print("Lets go")
            self.media_player.play()
            
            #generar pista audio a partir del video
            videoclip = VideoFileClip(self.dir+"/"+self.ruta)
            videoclip.audio.write_audiofile(self.dir+"/"+"audio.wav",codec='pcm_s16le')
            print(videoclip)
            
            #limpieza de audio
            r = sr.Recognizer()
            with sr.AudioFile(self.dir+"/"+"audio.wav") as source:
        
                r.adjust_for_ambient_noise(source,0.75)
                audio_clr = r.record(source)
                
                #clean_audio = AudioClip(audio_data)
                #videoclip.audio.write_audiofile(self.dir+"/"+"audio.wav",codec='pcm_s16le')

                # conversion speech to text
                text = r.recognize_google(audio_clr, language = "es-ES")
                print(text)
                #source.write(audio_clr)
                # comprobar audio limpiado
                self.txt_org.setText(text)
                self.txt_mod.setText(text)
            #txt_org = r.recognize_google(audio_clr)
            #print(txt_org)
            
        else:
            self.media_player.pause()


    # pulsar boton stop
    def stop_clicked(self):
        self.media_player.stop()
    

    # pulsar botones Guardar
    def save_txt(self):
        print("guardado")


    # pulsar boton procesar texto
    def procesar_txt(self):
        self.txt_tag.setText(pruebaBusqueda.procesarTxt(self.txt_mod.toPlainText()))

    # manejo pause/play del video
    def state_changed(self, newstate):
        states = {
            QMediaPlayer.PausedState: "Continuar",
            QMediaPlayer.PlayingState: "Pausa",
            QMediaPlayer.StoppedState: "Reproducir"
        }
        self.play_button.setText(states[newstate])
        self.stop_button.setEnabled(newstate != QMediaPlayer.StoppedState)
    

    # Video pantalla completa doble click
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
        return False
    
    # Abrir archivo de video
    def openFile(self):
        print("Done")
        fileName,_ = QFileDialog.getOpenFileName(self, "Archivo de video", '/home')
        if fileName != '':
            ruta=fileName.split("/")
            #print(ruta)
            videoName = fileName.split("/")[-1]
            
            for i in ruta[:-1]:
                if(i==ruta[0]):
                    self.dir = i
                else:
                    self.dir = self.dir +"/"+ i
            
            self.vidLayout.addWidget(self.video_widget)
            self.title_label.setText(' VIDEO: {}'.format(videoName))
            self.ruta = videoName
            VIDEO_PATH = fileName
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))

            self.media_player.setVideoOutput(self.video_widget)
            self.video_widget.setGeometry(30,30,700,300)
            
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)

#inicializar app
app=QtWidgets.QApplication(sys.argv)
#crear instancia clase initial
mainwindow=MainWindow()
#Stack
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec()