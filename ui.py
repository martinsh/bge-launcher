# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"BGE Launcher", pos = wx.DefaultPosition, size = wx.Size( 500,436 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer28 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splash = wx.StaticBitmap( self.m_panel2, wx.ID_ANY, wx.Bitmap( u"data/images/splash.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_splash, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer28.Add( self.m_staticline1, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		sizer_resolution = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_label_resolution = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Resolution", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_resolution.Wrap( -1 )
		self.m_label_resolution.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer8.Add( self.m_label_resolution, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		sizer_resolution.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		m_resolutionChoices = []
		self.m_resolution = wx.Choice( self.m_panel2, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 160,-1 ), m_resolutionChoices, 0 )
		self.m_resolution.SetSelection( -1 )
		bSizer7.Add( self.m_resolution, 0, 0, 5 )
		
		sizer_resolution.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_fullscreen = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Fullscreen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_fullscreen.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer12.Add( self.m_fullscreen, 0, wx.ALL, 5 )
		
		sizer_resolution.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		bSizer28.Add( sizer_resolution, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )
		
		sizer_aa = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer81 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_label_aa = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Anti-Aliasing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_aa.Wrap( -1 )
		self.m_label_aa.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer81.Add( self.m_label_aa, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		sizer_aa.Add( bSizer81, 1, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		m_aaChoices = [ u"off", u"2", u"4", u"8", u"16" ]
		self.m_aa = wx.Choice( self.m_panel2, wx.ID_ANY, wx.Point( -1,-1 ), wx.Size( 160,-1 ), m_aaChoices, 0 )
		self.m_aa.SetSelection( 0 )
		bSizer9.Add( self.m_aa, 0, 0, 5 )
		
		sizer_aa.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		sizer_aa.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer28.Add( sizer_aa, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5 )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_play = wx.Button( self.m_panel2, wx.ID_ANY, u"Play", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.m_play, 0, wx.ALL, 5 )
		
		self.m_exit = wx.Button( self.m_panel2, wx.ID_ANY, u"Quit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.m_exit, 0, wx.ALL, 5 )
		
		bSizer28.Add( bSizer41, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, 5 )
		
		bSizer4.Add( bSizer28, 1, wx.EXPAND, 5 )
		
		self.m_panel2.SetSizer( bSizer4 )
		self.m_panel2.Layout()
		bSizer4.Fit( self.m_panel2 )
		bSizer2.Add( self.m_panel2, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnExitClick )
		self.m_play.Bind( wx.EVT_BUTTON, self.OnStartGameClick )
		self.m_exit.Bind( wx.EVT_BUTTON, self.OnExitClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnExitClick( self, event ):
		event.Skip()
	
	def OnStartGameClick( self, event ):
		event.Skip()
	
	

