# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import wx
import serial
import time

import sys

from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

string1 = ["--完美！","--优秀！","--良好！","--及格！","--糟糕透了！"]

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)

class IrTest(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #self.DelButton = wx.Button(self, wx.ID_ANY, u"删除")
        self.Text = wx.TextCtrl(self,wx.ID_ANY,style = wx.TE_MULTILINE)
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer1.Add(self.Text,1,wx.ALIGN_CENTER| wx.LEFT|wx.EXPAND,3)
        self.SetSizer(self.sizer1)
        self.SetAutoLayout(1)
        self.sizer1.Fit(self)
        self.time0 = wx.Timer(self,wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.timerhand, self.time0)
        self.time0.Start(100)
        self.colflag = 0
        #txcol = wx.Colour(255,0,0)
        #self.Text.SetBackgroundColour(txcol)
        self.ser = serial.Serial()
        self.ser.port = "/dev/ttyUSB0"
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2
        self.ser.open()
        #ser.flush()
        time.sleep(0.1)
        self.ser.flushInput()
        self.ser.flushOutput()



    def timerhand(self,event):
        if self.colflag == 1:
            txcol = wx.Colour(255,255,255)
            self.Text.SetBackgroundColour(txcol)
            self.colflag = 0
            return
        ch = self.ser.read()
        if ch:
            txcol = wx.Colour(255,0,0)
            self.Text.SetBackgroundColour(txcol)
            self.time0.Start(200)
            ch = ord(ch)
            if ch == 3:
                s = string1[0]
            elif ch > 3 and ch < 5:
                s = string1[1]
            elif ch > 4 and ch < 8:
                s = string1[2]
            elif ch > 7 and ch < 11:
                s = string1[3]
            else:
                s = string1[4]

            s = str(ch) + s + '\n'

            self.Text.write(s)
            self.colflag = 1







app = wx.App(False)
frame = wx.Frame(None,title = "Ir Test",size = (800,500),pos = (300,200))
panel = IrTest(frame)
frame.Show()
app.MainLoop()



