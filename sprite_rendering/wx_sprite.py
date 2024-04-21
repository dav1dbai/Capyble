import wx
import wx.adv
import math
import random
import time

global app

def createApp():
    app = wx.App()

def mainLoop():
    app.MainLoop()

# class TextPanel(wx.Frame):
global app

def createApp():
    app = wx.App()

def mainLoop():
    app.MainLoop()

class TextPanel(wx.Frame):
    def __init__(self, parent, text):
        wx.Frame.__init__(self, parent, title="Text Panel", style=wx.FRAME_FLOAT_ON_PARENT | wx.STAY_ON_TOP)

        self.SetBackgroundColour("#F8D6AE")
        self.SetForegroundColour(wx.BLACK)
        # Create a static text control to display the text
        self.static_text = wx.StaticText(self, label=text)
        self.button = wx.Button(self)
        self.textinput = wx.TextCtrl(self,size = (self.static_text.GetSize()[0],25))
        self.Bind(wx.EVT_BUTTON, self.onSubmit, self.button)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSubmit, self.textinput)
        # Set up sizer to arrange the controls
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.static_text, 0, wx.ALL, border=5)  # Add some padding
        sizer.Add(self.textinput, 0, wx.ALL, border=5) 
        sizer.Add(self.button, 0, wx.ALL, border=5) 
        self.SetSizer(sizer)

        # Fit the frame to the size of the static text
        sizer.Fit(self)

    def onSubmit(self, event):
            user_input = self.textinput.GetValue()
            print("User Input:", user_input)



class Sprite(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Shaped Window",
                style = wx.STAY_ON_TOP | wx.FRAME_SHAPED | wx.SIMPLE_BORDER )
        #self.hasShape = True
        
        #movement
        self.delta = wx.Point(0,0)
    
        self.text = "hello!"
        self.panel = TextPanel(self,self.text)
        self.panel.Show()

        #gif translation
        self.frame = 0
        self.max_frame = 7
        self.updateImage("standing")
    
        #positions
        self.win = self.GetScreenPosition()
        self.screen_size = wx.DisplaySize()[0]

        #event bindings
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)

        #self.anim = wx.adv.Animation('./assets/testtrans.gif')
        #self.anim_ctrl = wx.adv.AnimationCtrl(self, -1, self.anim)
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.anim_ctrl)
        #self.SetSizerAndFit(sizer)
        #self.Show()
        #self.anim_ctrl.Play()
    
    def updateImage(self,pose):
        pose_dict = {
            "sitleft" : "./assets/sitleft.png",
            "sitright" : "./assets/sitleft.png",
            "standing" : "./assets/capystand.png",
            "jumping" : "./assets/capyjump.png",
            "walk0" : "./assets/0.png",
            "walk1" : "./assets/1.png",
            "walk2" : "./assets/2.png",
        }
        self.imgpath = pose_dict[pose]
        image = wx.Image(self.imgpath)          
        self.bmp = wx.Bitmap(image)
        self.SetClientSize((self.bmp.GetWidth(), self.bmp.GetHeight()))
        self.dc = wx.ClientDC(self)
        self.dc.DrawBitmap(self.bmp, 0,0, True)
        self.SetWindowShape()

    def SetWindowShape(self, evt=None):
        panel_size = self.panel.GetSize()
        bmp_size = self.bmp.GetSize()

        # Calculate the total height including the panel and the bitmap
        total_height = panel_size[1] + bmp_size[1]

        # Set the size of the frame to accommodate the panel and the bitmap
        self.SetClientSize((max(panel_size[0], bmp_size[0]), total_height))

        # Adjust the position of the panel to be at the top of the frame
        self.panel.SetPosition(wx.Point(0, 0))

        # Create a region for the window shape
        r = wx.Region()
        r.Union((0, 0, max(panel_size[0], bmp_size[0]), total_height))
        self.hasShape = self.SetShape(r)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0,0, True)

    def OnExit(self, evt):
        self.Close()

    #def MoveOrigin(self):
    
    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            pos = self.ClientToScreen(evt.GetPosition())
            newPos = (pos.x - self.delta.x, pos.y - self.delta.y)
            self.Move(newPos)

    def updateCoords(self):
        self.screen_size = wx.DisplaySize()
        self.win = self.GetScreenPosition()

    def traverse(self, coords, duration):
        self.updateCoords()
        dest_x = coords[0]
        dest_y = coords[1]
        dx = dest_x - self.win.x
        dy = dest_y - self.win.y

        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance != 0:
            dx_unit = dx / distance
            dy_unit = dy / distance
        else:
            dx_unit, dy_unit = 0, 0
        
        steps = int(distance)
        cycle_length = 3
        steps_per_image = 5  # Define how many steps per image change, adjusted for short distances
        
        for step in range(steps):
            # Calculate the new position based on the step along the trajectory
            x = self.win.x + int(step * dx_unit)
            y = self.win.y + int(step * dy_unit)
            
            # Update image according to the walk cycle
            current_image = rf"walk{(step // steps_per_image) % 3}"
            self.updateImage(current_image)
            
            self.panel.Move(wx.Point(x, y))
            self.Move(wx.Point(x, y + self.panel.GetSize()[1]))
            wx.GetApp().Yield()  # Allow other events to be processed
            time.sleep(duration / steps)  # Pause to create the illusion of animation
        self.updateCoords()
        self.panel.Move(wx.Point(self.win.x, self.win.y))    
        self.updateImage("walk1")
        wx.GetApp().Yield()

    def jump(self):
        time.sleep(0.5)
        for i in range(5):
            self.updateImage('standing')
            wx.GetApp().Yield()
            time.sleep(0.5)
            self.updateImage('jumping')
            wx.GetApp().Yield()
            
            print("jumping")
            time.sleep(0.5)
        self.updateImage('standing')
        wx.GetApp().Yield()