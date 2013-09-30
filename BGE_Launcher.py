#!/usr/bin/python2.7
import wx
import wx.xrc
import sys
import subprocess
from ui import MainFrame
import sys, string, os
import zipfile
import shutil
from xml.dom import minidom
import tempfile

	
class MainFrame2(MainFrame):
	def __init__(self,parent):
		super(MainFrame2,self).__init__(parent)
		### zip pathes
		self.filename = "game.data"
		self.folderpath = os.path.join(os.getcwd(),"data","player")
		self.filepath = os.path.join(self.folderpath,"game.data")
		
		self.tmpFolder = tempfile.mkdtemp()

		### write XML file
		try:
			f = open("./data/player/config.xml","r")
			print("config.xml found!")
		except:
			print("config.xml not found! writing file.")
			self.initXML()
		
		### launcher settings
		doc = minidom.parse(os.path.join(self.folderpath,"config.xml"))
		self.window_title=doc.getElementsByTagName('title')[0].attributes['value'].value
		self.blendfile=doc.getElementsByTagName('blendfile')[0].attributes['value'].value
		self.show_framerate=int(doc.getElementsByTagName('show_framerate')[0].attributes['value'].value)
		self.nomipmap=int(doc.getElementsByTagName('nomipmap')[0].attributes['value'].value)
		self.splash_screen = doc.getElementsByTagName('splash_screen')[0].attributes['value'].value
		self.aa = int(doc.getElementsByTagName('aa')[0].attributes['value'].value)
		self.fullscreen = eval(doc.getElementsByTagName('fullscreen')[0].attributes['value'].value)
		self.res_index = int(doc.getElementsByTagName('res_index')[0].attributes['value'].value)
		
		self.resolutions = []
		for resolution in doc.getElementsByTagName('resolution'):
			self.resolutions.append(resolution.attributes['value'].value)
		

		
		
		###launcher title
		self.title = self.window_title
		
		### set height and width to splashscreen size
		self.splash=wx.Image(os.path.join(os.getcwd(),self.splash_screen)).ConvertToBitmap()
		height = self.splash.GetHeight()
		width = self.splash.GetWidth()
		self.SetSizeWH(width, height+150)
		
		### Create Dropdownbox with all setable Resolutions
		for item in self.resolutions:
			self.m_resolution.Append(item)
		self.m_resolution.SetSelection(self.res_index)
		self.m_aa.SetSelection(self.aa)
		self.m_fullscreen.SetValue(self.fullscreen)

		### pick icon.png that is displayed at the upper left corner
		try:
			ico = wx.Icon('./data/images/icon.png', wx.BITMAP_TYPE_PNG)
			self.SetIcon(ico)
		except:
			pass
		

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
		createElement("aa","value","0")
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
		createElement("res_index","value",str(self.m_resolution.GetCurrentSelection()))
		createElement("aa","value",str(self.m_aa.GetCurrentSelection()))
		createElement("fullscreen","value",str(self.m_fullscreen.GetValue()))
		createElement("splash_screen","value",self.splash_screen)
		
		for resolution in self.resolutions:
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
		self.fullscreen = self.m_fullscreen.GetValue()
		if self.fullscreen == True:
			return '-f '
		else:
			return '-w '
	
	### blenderplayer option anti aliasing
	def antiAliasing(self):
		self.aa = self.m_aa.GetStringSelection()
		if self.aa == 'off':
			return '0'
		else:
			return self.aa
	
	### runs the blenderplayer with the launcher settings
	def runBlender(self):
		self.resolution = self.m_resolution.GetStringSelection()
		active_res = self.resolution.partition('x')
		### change to folder to blenderplayer folder
		os.chdir(self.folderpath)
		
		### blenderplayer command
		command = ("blenderplayer" + ### Blenderplayer path
				   ' ' + '-m ' + self.antiAliasing() + ### Antialiasing settings
				   ' -g show_framerate = ' + str(self.show_framerate) + ### Framerate settings
				   ' -g nomipmap = '+ str(self.nomipmap) + ### Mipmap settings
				   ' ' + self.fullScreenMode()  + active_res[0] + ' ' + active_res[2] + ' ' + ### Resolution settings 
				   os.path.join(self.tmpFolder,self.blendfile)) ### Blendfile path
				   
		### execute a process that starts the blenderplayer with settings from the launcher
		proc = subprocess.Popen(command,shell=True)
		stdout,stderr = proc.communicate()
		if stderr == None:
			### if blenderplayer process ends, the tmp folder will be deleted and launcher exits
			self.deleteTmpFolder()
			sys.exit(0)
		
	### start button click
	def OnStartGameClick( self, event ):
		self.saveXML()	
		self.unzipData(self.tmpFolder,self.filename,self.filepath)	
		self.Hide()
		self.runBlender()
		
	### exit button click	
	def OnExitClick( self, event ):
		self.deleteTmpFolder()
		sys.exit(0)

app = wx.PySimpleApp()
frame = MainFrame2(None)
frame.Show(1)
app.MainLoop()