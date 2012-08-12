#!/usr/bin/env python

"""
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Based on commander.py from PyPose:
    PyPose: Bioloid pose system for arbotiX robocontroller
    Copyright (c) 2009,2010 Michael E. Ferguson.  All right reserved.

"""

import time, sys, serial
import wx

# Commander definitions


width = 400

class Commander(wx.Frame):
    TIMER_ID = 100

    def __init__(self, parent, ser, comndr, debug = False):
        wx.Frame.__init__(self, parent, -1, "ArbotiX Commander", style = wx.DEFAULT_FRAME_STYLE & ~ (wx.MAXIMIZE_BOX))
        self.ser = ser
        self.comndr = comndr
        sizer = wx.GridBagSizer(20,40)
        #Debug txt Window
        self.logger = wx.TextCtrl(self, size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL)
        sizer.Add(self.logger, (0,0),wx.GBSpan(1,2),wx.EXPAND|wx.LEFT,5)

        #Debug status window
        status= wx.StaticBox(self, -1, 'Status')
        status.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        statusBox = wx.StaticBoxSizer(status, orient=wx.VERTICAL)
        statusSizer = wx.GridSizer(rows=7, cols=2, hgap=5, vgap=5)
        statusSizer.Add(wx.StaticText(self, -1, "Power on: "))
        self.statusPower = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusPower)
        statusSizer.Add(wx.StaticText(self, -1, "Voltage: "))
        self.statusVoltage = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusVoltage)
        statusSizer.Add(wx.StaticText(self, -1, "Control Mode: "))
        self.statusControlMode = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusControlMode)
        statusSizer.Add(wx.StaticText(self, -1, "Gait: "))
        self.statusGait = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusGait)
        statusSizer.Add(wx.StaticText(self, -1, "Balance Mode: "))
        self.statusBalanceMode = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusBalanceMode)
        statusSizer.Add(wx.StaticText(self, -1, "Body Y offset: "))
        self.statusBodyYOffset = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusBodyYOffset)
        statusSizer.Add(wx.StaticText(self, -1, "Speed Control: "))
        self.statusSpeedControl = wx.TextCtrl(self, style=wx.TE_READONLY)
        statusSizer.Add(self.statusSpeedControl)
        statusBox.Add(statusSizer)
        sizer.Add(statusBox, (0,2), wx.GBSpan(1,1), wx.EXPAND|wx.BOTTOM|wx.CENTER,5)
        # Left Joystick control
        lt_joy = wx.StaticBox(self, -1, 'Left joystick')
        lt_joy.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        lt_joyBox = wx.StaticBoxSizer(lt_joy,orient=wx.VERTICAL)
        lt_joySizer = wx.GridBagSizer(5,5)
        lt_joySizer.Add(wx.StaticText(self, -1, "Vertical"),(0,1), wx.GBSpan(1,1),wx.ALIGN_CENTER_VERTICAL)
        self.lt_vert = wx.Slider(self, -1, 0, -125, 125, wx.DefaultPosition, (-1, 200), wx.SL_VERTICAL | wx.SL_LABELS)
        lt_joySizer.Add(self.lt_vert,(0,0),wx.GBSpan(3,1))
        lt_joySizer.Add(wx.StaticText(self, -1, "Horizontal"),(1,1), wx.GBSpan(1,2),wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL)
        self.lt_hor = wx.Slider(self, -1, 0, -125, 125, wx.DefaultPosition, (200, -1), wx.SL_HORIZONTAL | wx.SL_LABELS)
        lt_joySizer.Add(self.lt_hor,(2,1),wx.GBSpan(1,2), wx.ALIGN_BOTTOM)
        lt_joyBox.Add(lt_joySizer)
        sizer.Add(lt_joyBox, (1,0), wx.GBSpan(1,1), wx.EXPAND|wx.BOTTOM|wx.LEFT,5)


        # Button control
        buttons= wx.StaticBox(self, -1, 'Buttons')
        buttons.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        buttonsBox = wx.StaticBoxSizer(buttons, orient=wx.VERTICAL)
        buttonsSizer = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=5)
        self.button_L4 = wx.ToggleButton(self, -1, 'L4')
        buttonsSizer.Add(self.button_L4)
        self.button_R1 = wx.ToggleButton(self, -1, 'R1')
        buttonsSizer.Add(self.button_R1)
        self.button_L5 = wx.ToggleButton(self, -1, 'L5')
        buttonsSizer.Add(self.button_L5)
        self.button_R2 = wx.ToggleButton(self, -1, 'R2')
        buttonsSizer.Add(self.button_R2)
        self.button_L6 = wx.ToggleButton(self, -1, 'L6')
        buttonsSizer.Add(self.button_L6)
        self.button_R3 = wx.ToggleButton(self, -1, 'R3')
        buttonsSizer.Add(self.button_R3)
        self.button_LT = wx.ToggleButton(self, -1, 'LT')
        buttonsSizer.Add(self.button_LT)
    	self.button_RT = wx.ToggleButton(self, -1, 'RT')
        buttonsSizer.Add(self.button_RT)
        buttonsBox.Add(buttonsSizer)
        sizer.Add(buttonsBox, (1,1), wx.GBSpan(1,1), wx.EXPAND|wx.BOTTOM|wx.CENTER,5)

        #Right joystick control
        rt_joy = wx.StaticBox(self, -1, 'Right joystick')
        rt_joy.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        rt_joyBox = wx.StaticBoxSizer(rt_joy,orient=wx.VERTICAL)
        rt_joySizer = wx.GridBagSizer(5,5)
        rt_joySizer.Add(wx.StaticText(self, -1, "Vertical"),(0,1), wx.GBSpan(1,1),wx.ALIGN_CENTER_HORIZONTAL)
        self.rt_vert = wx.Slider(self, -1, 0, -125, 125, wx.DefaultPosition, (-1, 200), wx.SL_VERTICAL | wx.SL_LABELS)
        rt_joySizer.Add(self.rt_vert,(0,0),wx.GBSpan(3,1))
        rt_joySizer.Add(wx.StaticText(self, -1, "Horizontal"),(1,1), wx.GBSpan(1,2),wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM)
        self.rt_hor = wx.Slider(self, -1, 0, -125, 125, wx.DefaultPosition, (200, -1), wx.SL_HORIZONTAL | wx.SL_LABELS)
        rt_joySizer.Add(self.rt_hor,(2,1),wx.GBSpan(1,2),wx.ALIGN_BOTTOM)
        rt_joyBox.Add(rt_joySizer)
        sizer.Add(rt_joyBox, (1,2), wx.GBSpan(1,1), wx.EXPAND|wx.BOTTOM|wx.RIGHT,5)

        # timer for output
        self.timer = wx.Timer(self, self.TIMER_ID)
        self.timer.Start(33)
        wx.EVT_CLOSE(self, self.onClose)
        wx.EVT_TIMER(self, self.TIMER_ID, self.onTimer)

        self.SetSizerAndFit(sizer)
        self.Show(True)

    def centerLeftjoy(self, event):
        self.lt_vert.SetValue(0)
        self.lt_hor.SetValue(0)

    def centerRightjoy(self, event):
        self.rt_vert.SetValue(0)
        self.rt_hor.SetValue(0)

    def onClose(self, event):
        self.timer.Stop()
        self.sendPacket(0,0,0,0,0)
        self.Destroy()

    def getButtons(self):
        send_buttons=0
        if self.button_R1.GetValue():
            send_buttons += BUT_R1
        if self.button_R2.GetValue():
            send_buttons += BUT_R2
        if self.button_R3.GetValue():
            send_buttons += BUT_R3
        if self.button_L4.GetValue():
            send_buttons += BUT_L4
        if self.button_L5.GetValue():
            send_buttons += BUT_L5
        if self.button_L6.GetValue():
            send_buttons += BUT_L6
        if self.button_RT.GetValue():
            send_buttons += BUT_RT
        if self.button_LT.GetValue():
            send_buttons += BUT_LT
        return send_buttons

    def onTimer(self, event=None):
        # configure output

        if self.comndr.inWaiting() > 8:
            incomming = self.comndr.read(self.comndr.inWaiting())
            self.ser.write(incomming)
            self.readPacket(incomming)
        while self.ser.inWaiting() > 0:
            self.debugRead()
        self.timer.Start(5)

    def debugRead(self):
        line = ser.readline()
        if line.startswith("Power: "):
                self.statusPower.ChangeValue(line[6:len(line)-1])
        elif line.startswith("Voltage: "):
                self.statusVoltage.ChangeValue(line[8:len(line)-1])
        elif line.startswith("Gait: "):
                self.statusGait.ChangeValue(line[6:len(line)-1])
        elif line.startswith("ControlMode: "):
            if line[13] == "0":
                self.statusControlMode.ChangeValue("Walk")
            elif line[13] == "1":
                self.statusControlMode.ChangeValue("Translate")
            elif line[13] == "2":
                self.statusControlMode.ChangeValue("Rotate")
            elif line[13] == "3":
                self.statusControlMode.ChangeValue("Single leg")
            elif line[13] == "4":
                self.statusControlMode.ChangeValue("GP Player")
            else:
                self.statusControlMode.ChangeValue("Unknown mode")
                self.logger.WriteText(line)
        elif line.startswith("BalanceMode: "):
            if line[13] == "1":
                self.statusBalanceMode.ChangeValue("True")
            else:
                self.statusBalanceMode.ChangeValue("False")
        elif line.startswith("Body Y Offset: "):
            self.statusBodyYOffset.ChangeValue(line[15:len(line)-1])
        elif line.startswith("Speed Control: "):
            self.statusSpeedControl.ChangeValue(line[15:len(line)-1])
        else:
            self.logger.WriteText(line)

    def readPacket(self, data):
        while(len(data) > 8):

            if ord(data[1]) == 255 and ord(data[2]) != 255:
                rt_vrt = ord(data[2]) - 128
                rt_hor = ord(data[3]) - 128
                lt_vrt = ord(data[4]) - 128
                lt_hor = ord(data[5]) - 128
                buttn = ord(data[6])
                ext = ord(data[7])
                chksum = ord(data[8])
                if chksum == 255 - ((rt_vrt+128+rt_hor+128+lt_vrt+128+lt_hor+128+buttn+ext)%256):
                    self.rt_vert.SetValue(rt_vrt)
                    self.rt_hor.SetValue(rt_hor)
                    self.lt_vert.SetValue(lt_vrt)
                    self.lt_hor.SetValue(lt_hor)
                    self.setButtons(buttn)
                    data = data[8:]
                else:
                    print "CHK sum error"
                    data = data[1:]
            else:
                data = data[1:]
    def setButtons(self, buttn):
        '''
        BUT_R1      0x01
        BUT_R2      0x02
        BUT_R3      0x04
        BUT_L4      0x08
        BUT_L5      0x10
        BUT_L6      0x20
        BUT_RT      0x40
        BUT_LT      0x80
        '''
        self.button_R1.SetValue((buttn & 0x01))
        self.button_R2.SetValue((buttn & 0x02))
        self.button_R3.SetValue((buttn & 0x04))
        self.button_RT.SetValue((buttn & 0x40))
        self.button_L4.SetValue((buttn & 0x08))
        self.button_L5.SetValue((buttn & 0x10))
        self.button_L6.SetValue((buttn & 0x20))
        self.button_LT.SetValue((buttn & 0x80))

    def sendPacket(self, right_vertical, right_horizontal, left_vertical, left_horizontal, send_buttons):
        # send output
        self.ser.write('\xFF')
        self.ser.write(chr(right_vertical+128))
        self.ser.write(chr(right_horizontal+128))
        self.ser.write(chr(left_vertical+128))
        self.ser.write(chr(left_horizontal+128))
        self.ser.write(chr(send_buttons))
        self.ser.write(chr(0))
        self.ser.write(chr(255 - ((right_vertical+128+right_horizontal+128+left_vertical+128+left_horizontal+128+send_buttons)%256)))
        #print 'Sent: Rt_vert: ', right_vertical+128, ', Rt_hor: ', right_horizontal+128, ', lt_vert: ', left_vertical+128, ', lt_hor: ', left_horizontal+128, ', Butn: ', send_buttons, '\n'

if __name__ == "__main__":
    # commander.py <serialport>
    ser = serial.Serial()
    comndr = serial.Serial()
    ser.baudrate = 38400
    comndr.baudrate = 38400
    if len(sys.argv) >= 3:
        ser.port = sys.argv[1]
	comndr.port = sys.argv[2]
    else:
        ser.port = "/dev/ttyUSB0"
	comndr.port = "/dev/ttyUSB1"
    ser.timeout = 0.5
    comndr.timeout = 0.5
    ser.open()
    comndr.open()
    app = wx.PySimpleApp()
    frame = Commander(None, ser, comndr, True)
    app.MainLoop()

