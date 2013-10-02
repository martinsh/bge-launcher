from PyQt4 import QtCore, QtGui
from ui import Ui_MainWindow
import atexit
from functools import partial

import subprocess
import sys, string, os
import zipfile
import shutil
from xml.dom import minidom
import tempfile


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	_fromUtf8 = lambda s: s
	

class BgeLauncher(Ui_MainWindow):
	def setupUi(self, MainWindow):
		sshFile = "style.css"
		with open(sshFile,"r") as fh:
			MainWindow.setStyleSheet(fh.read())
	
		### inherit from main class
		super(BgeLauncher,self).setupUi(MainWindow)
		
		### zip pathes
		self.filename = "game.data"
		self.folderpath = os.path.join(os.getcwd(),"data","player")
		self.filepath = os.path.join(self.folderpath,"game.data")
		
		### create tmp Folder
		self.tmpFolder = tempfile.mkdtemp()
		
		### write XML file
		try:
			f = open("./data/player/config.xml","r")
			print("config.xml found!")
		except:
			print("config.xml not found! writing file.")
			self.initXML()
		
		### Load XML config file
		self.doc = minidom.parse(os.path.join(self.folderpath,"config.xml"))
		self.window_title=self.doc.getElementsByTagName('title')[0].attributes['value'].value
		self.blendfile=self.doc.getElementsByTagName('blendfile')[0].attributes['value'].value
		self.show_framerate=int(self.doc.getElementsByTagName('show_framerate')[0].attributes['value'].value)
		self.nomipmap=int(self.doc.getElementsByTagName('nomipmap')[0].attributes['value'].value)
		self.splash_screen = self.doc.getElementsByTagName('splash_screen')[0].attributes['value'].value
		self.aa = self.doc.getElementsByTagName('aa')[0].attributes['value'].value
		self.fullscreenSettings = eval(self.doc.getElementsByTagName('fullscreen')[0].attributes['value'].value)
		self.res_index = int(self.doc.getElementsByTagName('res_index')[0].attributes['value'].value)
		
		### load SplashScreen
		self.splashPixmap = QtGui.QPixmap(_fromUtf8(self.splash_screen))
		self.formSize = QtCore.QSize(self.splashPixmap.width(),self.splashPixmap.height()+100)
		self.splash.setPixmap(self.splashPixmap)
		
		### resize Launcher to the Splashscreen and set Window Title
		self.mainWindow = MainWindow
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", self.window_title, None, QtGui.QApplication.UnicodeUTF8))
		MainWindow.resize(self.formSize)
		MainWindow.setMinimumSize(self.formSize)
		MainWindow.setMaximumSize(self.formSize)
		self.splash.setMaximumSize(self.formSize)
		
		#MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		#MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		
		### Center Window on Screen
		self.screenResolution = QtGui.QDesktopWidget().screenGeometry()
		MainWindow.setGeometry(0,0,self.splashPixmap.width(),self.splashPixmap.height()+100)
		MainWindow.move((self.screenResolution.width()/2) - (self.formSize.width()/2),
						(self.screenResolution.height()/2) - (self.formSize.height()/2))
		
		### connect Button with methode that is executed
		QtCore.QObject.connect(self.playButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.runBlenderplayer)
		QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.quitLauncher)
		### load available Resolutions from XML
		self.resolution.addItems(self.addResolution())
		self.resolution.setCurrentIndex(self.res_index)
		self.fullscreen.setCheckState(self.fullscreenSettings)
		self.antiAliasing.setCurrentIndex(self.antiAliasing.findText(self.aa))
	
	### load resolutions from config file
	def addResolution(self):
		resolutions = []
		for resolution in self.doc.getElementsByTagName('resolution'):
			resolutions.append(resolution.attributes['value'].value)
		return resolutions	
	
	### write config file		
	def initXML(self):
		doc = minidom.Document()
		url = ""
		settings = doc.createElementNS(url,"launcher")
		doc.appendChild(settings)
		
		def createElement(elementName,attributeName,value):
			item = doc.createElementNS(url,elementName)
			item.setAttributeNS(url,attributeName,value)
			settings.appendChild(item)
		
		createElement("title","value","BGE Launcher")
		
		createElement("blendfile","value",os.path.join("data","game.blend"))
		createElement("nomipmap","value","0")
		createElement("show_framerate","value","0")
		createElement("res_index","value","0")
		createElement("fullscreen","value","False")
		createElement("aa","value","off")
		createElement("splash_screen","value",os.path.join("data","images","splash.png"))
		
		createElement("resolution","value","640x480")
		createElement("resolution","value","800x600")
		createElement("resolution","value","1024x768")
		createElement("resolution","value","1152x864")
		createElement("resolution","value","1280x720")
		createElement("resolution","value","1280x768")
		createElement("resolution","value","1280x800")
		createElement("resolution","value","1280x960")
		createElement("resolution","value","1280x1024")
		createElement("resolution","value","1440x900")
		createElement("resolution","value","1600x1200")
		createElement("resolution","value","1680x1050")
		createElement("resolution","value","1920x1080")
		createElement("resolution","value","1920x1200")
		
		file_object = open(os.path.join(self.folderpath,"config.xml"), "w")
		file_object.write(doc.toprettyxml());
		file_object.close()	
		
	### new congig.xml will be saved when game is started
	def saveXML(self):
		doc = minidom.Document()
		url = ""
		settings = doc.createElementNS(url,"launcher")
		doc.appendChild(settings)
		
		def createElement(elementName,attributeName,value):
			item = doc.createElementNS(url,elementName)
			item.setAttributeNS(url,attributeName,value)
			settings.appendChild(item)
		
		createElement("title","value",self.window_title)
		
		createElement("blendfile","value",self.blendfile)
		createElement("nomipmap","value",str(self.nomipmap))
		createElement("show_framerate","value",str(self.show_framerate))
		createElement("res_index","value",str(self.resolution.currentIndex()))
		createElement("aa","value",str(self.antiAliasing.currentText()))
		createElement("fullscreen","value",str(self.fullscreen.checkState()))
		createElement("splash_screen","value",self.splash_screen)
		
		for resolution in self.addResolution():
			createElement("resolution","value",resolution)
		
		file_object = open(os.path.join(self.folderpath,"config.xml"), "w")
		file_object.write(doc.toprettyxml());
		file_object.close()	
	
	### methode deletes the tmp folder
	def deleteTmpFolder(self):
		if os.path.exists(self.tmpFolder):
			shutil.rmtree(self.tmpFolder)
	
	### methode for unzipping the game files
	def unzipData(self,folderpath,filename,filepath):
		zfile = zipfile.ZipFile(filepath)
		for name in zfile.namelist():
			(dirname, filename) = os.path.split(name)
			if filename == "":
				if not os.path.exists(os.path.join(folderpath,dirname)):
					os.mkdir(os.path.join(folderpath,dirname))
			else:
				fd = open(os.path.join(folderpath,name),'wb')
				fd.write(zfile.read(name))
				fd.close()
		zfile.close()
	
		### blenderplayer option fullscreen
	def fullScreenMode(self):
		if self.fullscreen.checkState() == 2:
			return '-f '
		else:
			return '-w '
	
	### blenderplayer option anti aliasing
	def setAntiAliasing(self):
		if self.antiAliasing.currentText() == 'off':
			return '0'
		else:
			return str(self.antiAliasing.currentText())
	
	### runs the blenderplayer with the launcher settings
	def blenderplayerProcess(self):
	
	
		resolution = str(self.resolution.currentText()).partition('x')
		### change to folder to blenderplayer folder
		os.chdir(self.folderpath)
		
		
		### blenderplayer command
		command = (
				   "blenderplayer" # Blenderplayer
				   " -m " + self.setAntiAliasing() +# Anti Aliasing settings
				   " -g nomipmap = "+ str(self.nomipmap) + # Mipmap settings
				   " " + self.fullScreenMode() + resolution[0]+" "+resolution[2]+" "+# Resolution settings
				   os.path.join(self.tmpFolder,self.blendfile) #Blendfile path)
				   )
		
		### execute a process that starts the blenderplayer with settings from the launcher
		proc = subprocess.Popen(command,shell=True)
		proc.title = "test"
		stdout,stderr = proc.communicate()
		if stderr == None:
			### if blenderplayer process ends, the tmp folder will be deleted and launcher exits
			self.deleteTmpFolder()
			sys.exit(0)
	
	### start the blenderplayer with configured settings from the launcher
	def runBlenderplayer(self):
		self.saveXML()
		self.mainWindow.hide()
		self.unzipData(self.tmpFolder,self.filename,self.filepath)
		self.blenderplayerProcess()
	
	def quitLauncher(self):
		self.deleteTmpFolder()
		sys.exit(0)

	def awesome(self):
		print("awesome")


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = BgeLauncher()
	ui.setupUi(MainWindow)
	MainWindow.show()
	atexit.register(ui.quitLauncher)
	sys.exit(app.exec_())
		
# if __name__ == "__main__":
	# import sys
	# app = QtGui.QApplication(sys.argv)
	# Form = QtGui.QWidget()
	# ui = BgeLauncher()
	# ui.setupUi(Form)
	# Form.show()
	# atexit.register(ui.quitLauncher)
	# sys.exit(app.exec_())
	