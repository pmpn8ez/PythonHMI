#import pkg_resources.py2_warn
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
import sys
import os
from pylogix import PLC
#from kivy.core.window import Window
#Window.size = (450, 400)
#def resourcePath():
#    '''Returns path containing content - either locally or in pyinstaller tmp file'''
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS)

#    return os.path.join(os.path.abspath("."))

#Read from PLC Every 0.1 Seconds
def update(dt):
	global clx
	if clx:
		#Analog
		CH1OUT = clx.Read("HMI_ANALOG_OUTPUT_CH1")
		CH2OUT = clx.Read("HMI_ANALOG_OUTPUT_CH2")
		App.get_running_app().root.ids.CH1OUT.value = CH1OUT.Value
		App.get_running_app().root.ids.CH2OUT.value = CH2OUT.Value
		#Digital
		Indicators = clx.Read("HMI_DIG_OUTPUT")
		IntInd = int(Indicators.Value)
		IND0 = (IntInd&1) != 0
		IND1 = (IntInd&2) != 0
		IND2 = (IntInd&4) != 0
		IND3 = (IntInd&8) != 0
		IND4 = (IntInd&16) != 0
		IND5 = (IntInd&32) != 0
		IND6 = (IntInd&64) != 0
		IND7 = (IntInd&128) != 0
		IND8 = (IntInd&256) != 0
		IND9 = (IntInd&512) != 0
		IND10 = (IntInd&1024) != 0
		IND11 = (IntInd&2048) != 0
		IND12 = (IntInd&4096) != 0
		IND13 = (IntInd&8192) != 0
		IND14 = (IntInd&16384) != 0
		IND15 = (IntInd&32768) != 0

		if IND0: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND0.state = state
		if IND1: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND1.state = state
		if IND2: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND2.state = state
		if IND3: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND3.state = state
		if IND4: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND4.state = state
		if IND5: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND5.state = state
		if IND6: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND6.state = state
		if IND7: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND7.state = state
		if IND8: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND8.state = state
		if IND9: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND9.state = state
		if IND10: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND10.state = state
		if IND11: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND11.state = state
		if IND12: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND12.state = state
		if IND13: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND13.state = state
		if IND14: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND14.state = state
		if IND15: state='down'
		else: state='normal'
		App.get_running_app().root.ids.IND15.state = state
		global firstrun
		if firstrun:
			firstrun = False
			ch1read = clx.Read("HMI_ANALOG_INPUT_CH1")
			App.get_running_app().root.ids.CH1IN.value = ch1read.Value
			ch2read = clx.Read("HMI_ANALOG_INPUT_CH2")
			App.get_running_app().root.ids.CH2IN.value = ch2read.Value
			data = clx.Read("HMI_DIG_INPUT.4")
			App.get_running_app().root.ids.PB4.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.5")
			App.get_running_app().root.ids.PB5.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.6")
			App.get_running_app().root.ids.PB6.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.7")
			App.get_running_app().root.ids.PB7.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.12")
			App.get_running_app().root.ids.PB12.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.13")
			App.get_running_app().root.ids.PB13.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.14")
			App.get_running_app().root.ids.PB14.state = 'normal' if data.Value == 0 else 'down'
			data = clx.Read("HMI_DIG_INPUT.15")
			App.get_running_app().root.ids.PB15.state = 'normal' if data.Value == 0 else 'down'
ip=''
clx = None
ipset=False
ismicro=False
firstrun=True
class MyTextInput(TextInput):
	max_characters = NumericProperty(0)
	def insert_text(self, substring, from_undo=False):
		if len(self.text) >= self.max_characters and self.max_characters > 0:
			substring = ""
		TextInput.insert_text(self, substring, from_undo)

def microswap(bit):
		switcher={
			'0':'24',
			'1':'25',
			'2':'26',
			'3':'27',
			'4':'28',
			'5':'29',
			'6':'30',
			'7':'31',
			'8':'16',
			'9':'17',
			'10':'18',
			'11':'19',
			'12':'20',
			'13':'21',
			'14':'22',
			'15':'23',
			}
		return switcher.get(bit,'invalid')
class controller(FloatLayout):

	#Popup closed connect to PLC if valid IP set
	def closepop(self):
		global clx
		global ismicro
		global firstrun
		firstrun = True
		if ipset:
			clx = PLC(ip,2)
			if ismicro:
				App.get_running_app().root.ids.iplabel.text ='Connected '+ ip + ' Micro800'
			else:
				App.get_running_app().root.ids.iplabel.text ='Connected '+ ip + ' Logix'
			clx.Micro800 = ismicro
			print(ismicro)
			Clock.schedule_interval(update, 0.25)
		else:
			print('Nop')
	#Comms Popup
	def compopup(self):
		def setip(add):
			global ip
			global ipset
			global ismicro
			if str.isdigit(text.text) and int(text.text)>0 and int(text.text)<=255:
				ip ='192.168.2.'+ str(text.text)
				ismicro = check.active
				ipset=True
			else:
				text.text=""
				ipset=False
			print(ip)
			print(ipset)
		def clear(self,btn):
			text.text=''
		box = BoxLayout(orientation='vertical')
		box2=BoxLayout(orientation='horizontal')
		text = MyTextInput(size_hint=(1,1),text='IP#',multiline=False,input_filter='int',max_characters=3)
		text.bind(on_press=clear)
		text.bind(on_touch_down=clear)
		label1=Label(text='192.168.2.')
		box2.add_widget(label1)
		box2.add_widget(text)
		check=CheckBox(size_hint=(0.25,1))
		label=Label(text='IsMicro800')
		box2.add_widget(check)
		box2.add_widget(label)
		box.add_widget(box2)
		Okbtn = Button(text='SetIP')
		box.add_widget(Okbtn)
		Closebtn = Button(text='Close')
		box.add_widget(Closebtn)
		Okbtn.bind(on_release=setip)
		popup = Popup(title='Enter IP Address',auto_dismiss=False,size_hint=(0.6,0.5))
		popup.add_widget(box)
		Closebtn.bind(on_press=popup.dismiss)
		popup.bind(on_dismiss=controller.closepop)
		popup.open()

	def setbit(self,bit,value):
		global clx
		if ismicro:
			bit = microswap(bit)
		if ipset:
			tag = 'HMI_DIG_INPUT.'+str(bit)
			clx.Write(tag,value)

	def settoggle(self,bit,value):
		global clx
		if ismicro:
			bit = microswap(bit)
		if ipset:
			tag = 'HMI_DIG_INPUT.'+str(bit)
			if value == 'normal':
				clx.Write(tag,0)
			else:
				clx.Write(tag,1)
	def setanalog(self,channel,value):
		global clx
		if ipset:
			tag = 'HMI_ANALOG_INPUT_CH'+str(channel)
			clx.Write(tag,value)


class ControllerApp(App):
	icon= 'ATLogo.png'
	title='ATHMI'
	def __init__(self, **kwargs):
		super(ControllerApp, self).__init__(**kwargs)
	def build(self):
		return controller()


if __name__ == '__main__':
	#kivy.resources.resource_add_path(resourcePath())
	ControllerApp().run()
if clx:
	clx.Close()
