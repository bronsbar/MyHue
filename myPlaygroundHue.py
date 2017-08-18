# Playground for Hue

import phue
from phue import Bridge
from phue import Light, Group, Sensor

import RPi.GPIO as GPIO

import time
from datetime import date

import json
import os

# Windows system
import tkinter as tk
from tkinter import ttk

class My_listbox(tk.Listbox):
    def __init__(self, parent,column, row, lblist,*args, **kwargs):
        tk.Listbox.__init__(self,parent,*args,**kwargs)
        self.parent=parent
        self.fill_list= [item.name for item in lblist]
        self.fill_list.sort()
        self.row=row
        self.column=column
        self.grid(row=row,column=column, padx=5, pady=5)
        self.fill_listbox()
        self.selection = []
         
    def fill_listbox(self):
        index=0
        for item in self.fill_list:
            self.insert(index, item)
            index += 1
            
    def onselect(self,event, updatebox1, updatebox2):
        'updatebox1 and updatebox2 two objects for which the update method needs to run'
        self.selection = self.curselection()
        self.selection = [self.get(x) for x in self.selection]
        print(self.selection)
        if updatebox1 != "" :
                updatebox1.update(self.selection)
        if updatebox2 !="":
                updatebox2.update(self.selection)

class Disable_lights(My_listbox):
    'subclass of My_listbox with update method for disable lights box'
    def __init__(self, parent,column, row, lblist,*args, **kwargs):
        My_listbox.__init__(self, parent,column, row, lblist,*args, **kwargs)
                  
    def update(self, inputlist):
        self.fill_list = []
        for selected_groups in inputlist:
            for lightgroups in group_diction.keys():
                if group_diction[lightgroups]['name']==selected_groups:
                    lights=group_diction[lightgroups]['lights'] #gives the list of light ID's in the group
                    lightsbyname = [bridge_bureau[int(x)].name for x in lights]
                    self.fill_list+=lightsbyname
        self.delete(0,tk.END)
        self.fill_listbox()
        

    def onselect(self,event):
            self.selection = self.curselection()
            self.selection = [self.get(x) for x in self.selection]
            print (self.selection)

class First_scene(My_listbox):
    'subclass of My_listbox with update method for first scene'
    def __init__(self, parent,column, row, lblist,*args, **kwargs):
        My_listbox.__init__(self, parent,column, row, lblist,*args, **kwargs)
                  
    def update(self, inputlist):
        self.fill_list = []
        for selected_groups in inputlist:
            for group_id in group_diction.keys():
                if selected_groups == group_diction[group_id]['name']:
                    for scene_id in scene_diction.keys():
                        if scene_diction[scene_id]['lights'] ==  group_diction[group_id]['lights']:
                            self.fill_list.append(scene_diction[scene_id]['name'])
        print (self.fill_list)                  
        self.delete(0,tk.END)
        self.fill_listbox()
        

    def onselect(self,event):
            self.selection = self.curselection()
            self.selection = [self.get(x) for x in self.selection]
            print (self.selection)




class windows(tk.Tk):
    switches = []
    test_switch = {}
    
    def __init__(self, *args, **kwargs):
       tk.Tk.__init__(self, *args, **kwargs)
       self.title("Bart's Domotica")
       self.create_top_menu()
       self.topframe()
       self.middleframe()
       self.buttonframe()

         
    def create_top_menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Project",command=self.loadproject)
        self.filemenu.add_command(label="Save Project",command=self.saveproject)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",command=self.exit)
        
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.aboutmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        self.config(menu=self.menubar)

    def topframe(self):
        top_bar_frame=tk.Frame(self)
        top_bar_frame.config(height=25)
        top_bar_frame.grid(row=0, columnspan=12,padx=5,pady=5)
        tk.Label(top_bar_frame, text='Switch Number:').grid(row=0,column=0)
        self.switch_number = tk.IntVar()
        self.switch_number.set(1)
        self.switch_number_widget = tk.Spinbox(top_bar_frame,width=2,textvariable=self.switch_number, from_=1, to=10)
        self.switch_number_widget.grid(row=0, column=2)
        tk.Label(top_bar_frame, text='Switch Name:').grid(row=0,column=3)
        self.switch_name = tk.StringVar()
        self.switch_name_widget = tk.Entry(top_bar_frame, textvariable=self.switch_name)
        self.switch_name_widget.grid(row=0, column=4)
        tk.Label(top_bar_frame, text='I/O Port:').grid(row=0,column=5)
        self.IO_number = tk.IntVar()
        self.IO_number.set(1)
        self.IO_number_widget = ttk.Combobox(top_bar_frame,width=5,textvariable=self.IO_number, values=(1,5,26,3))
        self.IO_number_widget.grid(row=0, column=6)

    def middleframe(self):
        'Frame holding all the listboxes'
        middle_frame=tk.Frame(self)
        middle_frame.config(height=25)
        middle_frame.grid(row=1, columnspan=6,rowspan= 12, padx=5,pady=10)

        tk.Label(middle_frame, text='Light Groups:').grid(row=2,column=0, sticky='w', padx=5)
        self.lblightgroups=My_listbox(parent=middle_frame, height=10, selectmode=tk.MULTIPLE, exportselection=0,
                                 row=3, column=0, lblist=bridge_bureau.groups)

        tk.Label(middle_frame, text='Disable Lights in Groups:').grid(row=2,column=2, sticky='w', padx=5)
        self.lbdisable_lights=Disable_lights(parent=middle_frame, lblist=bridge_bureau.lights, height=10, selectmode=tk.MULTIPLE, exportselection=0,
                                 row=3, column=2)
        
        tk.Label(middle_frame, text='Disable Sensors:').grid(row=2,column=1, sticky='w', padx=5)
        self.lbsensors=My_listbox(parent=middle_frame, height=10, selectmode=tk.MULTIPLE, exportselection=0,
                                 row=3, column=1, lblist=bridge_bureau.sensors)

        tk.Label(middle_frame, text='First Scene:').grid(row=2,column=3, sticky='w', padx=5)
        self.lbfirst_scene=First_scene(parent=middle_frame, height=10, exportselection=0,
                                 row=3, column=3, lblist=bridge_bureau.scenes)
        
        self.lblightgroups.bind('<<ListboxSelect>>', lambda event, updatebox1=self.lbdisable_lights, updatebox2=self.lbfirst_scene
                           : self.lblightgroups.onselect(event, updatebox1,updatebox2))

        self.lbsensors.bind('<<ListboxSelect>>', lambda event, updatebox1="", updatebox2=""
                           : self.lbsensors.onselect(event, updatebox1,updatebox2))
        
        self.lbdisable_lights.bind('<<ListboxSelect>>', self.lbdisable_lights.onselect)

        self.lbfirst_scene.bind('<<ListboxSelect>>', self.lbfirst_scene.onselect)

    def buttonframe(self):
        button_frame=tk.Frame(self)
        button_frame.config(height=25)
        button_frame.grid(row=15, columnspan=6,padx=5,pady=10)

        create_switch_button=tk.Button(button_frame,text="Create Switch")
        create_switch_button.grid(row=15,column=0)

        delete_switch_button=tk.Button(button_frame,text="Delete Switch")
        delete_switch_button.grid(row=15,column=1)

        test_switch_button=tk.Button(button_frame,text="Test Switch", command=self.test_switch)
        test_switch_button.grid(row=15,column=2)

        quit_button=tk.Button(button_frame,text="Quit", command=self.destroy)
        quit_button.grid(row=15,column=4)
        
    def test_switch(self):
        test_switch = {"switch number":self.switch_number.get(),"switch name":self.switch_name.get(),"IO port":self.IO_number.get(),
                       "switch groups":self.lblightgroups.selection,"disabled sensors":self.lbsensors.selection,
                       "disabled lights":self.lbdisable_lights.selection,
                       "first scene":self.lbfirst_scene.selection[0]}
        for groups in self.lblightgroups.selection:
            bridge_bureau.run_scene(groups,self.lbfirst_scene.selection[0])
        for lights in self.lbdisable_lights.selection:
            bridge_bureau[lights].on =False
            
        print(test_switch)
    def loadproject(self):
        pass
    def saveproject(self):
        pass
    def exit(self):
        pass

        
        
  
class Switch ():
    ' Switch class defines a io-port, first scene to execute, lights and scenes in the group'
    def __init__(self,switch_name,switch_ioport,switch_group,switch_user):
        self.switch_name = switch_name
        self.switch_ioport = switch_ioport
        self.switch_group = switch_group
        self.switch_group_id = bridge_bureau.get_group_id_by_name(self.switch_group)
        self.time_pressed = time.time()
        self.switch_user = switch_user
        self.group_class = Group(bridge_bureau,switch_group) #Class Group
        self.lights_in_group = sorted (bridge_bureau.get_group(switch_group, 'lights'))
        self.scenes_in_group =  [x for x in scene_diction.keys() if (sorted(scene_diction[x]['lights']) == self.lights_in_group) &
                                (scene_diction[x]['name']!= 'Uit')]
        self.sofie_scene = self.find_scene_Sofie() # first scene to be ran
        self.last_scene = self.sofie_scene

    # check if there is a Sofie scene in list if so, this is the start scene
    def find_scene_Sofie(self) :
        for x in self.scenes_in_group :
            if scene_diction[x]['name'] == "Sofie" :
                return self.scenes_in_group.index(x)
        return 0

    # method update switch attributes
    def update_switch_attributes(self):
        self.lights_in_group = sorted (bridge_bureau.get_group(self.switch_group, 'lights'))
        self.scenes_in_group =  [x for x in scene_diction.keys() if (sorted(scene_diction[x]['lights']) == self.lights_in_group) &
                                (scene_diction[x]['name']!= 'Uit')]
        self.sofie_scene = self.find_scene_Sofie() # first scene to be ran
        self.last_scene = self.sofie_scene
        return

        
    def callback(self,channel):
        time_now =time.time()
        while GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
        print ("switch name: {} pushed for group: {} at {} on {}".format(self.switch_name,self.switch_group,                                                                         time.strftime("%H:%M:%S"),date.today()))
        push_time = time.time()-time_now
        print ("push time is: {}".format(push_time))
        if (push_time > 1.2) & (bridge_bureau.get_group(group_id=self.switch_group, parameter="on") == True):
            print("long push")
           # switch group off by setting group_class.on equal to False
            self.group_class.on = False
            # check if all lights of group are out
            for lights in self.lights_in_group:
                while bridge_bureau.get_light(int(lights),"on")==True:
                    time.sleep(0.1)
                    bridge_bureau.set_light(int(lights),"on", False)
                    print ("light : ",lights, "was not off and command has been resend")
                    time.sleep(0.2) # avoid sending more then 5 commands per second
                    counter += 1
                    if counter == 3 :
                        print ("cannot reach light: ", lights )
                        counter = 0
                        break
                    
            self.last_scene = self.sofie_scene # back to basis scene = 0 if there is no Sofie scene in list
            print ("lights are out!")
        elif (push_time > 0.3) & (push_time < 1.2):
            bridge_bureau.activate_scene(self.switch_group_id, self.scenes_in_group[self.last_scene])
            print("scene is num {} name {}  ".format(self.last_scene,scene_diction[self.scenes_in_group[self.last_scene]]['name']))
            print("")
            #check if all lights in the group are on, if not send on signal again, try 5 times
            for lights in self.lights_in_group:
                while bridge_bureau.get_light(int(lights),"on")==False:
                    time.sleep(0.1)
                    bridge_bureau.set_light(int(lights),"on", True)
                    print ("light:", lights, "was not on and command has been resend")
                    time.sleep(0.2)#avoid sending more than 5 commands per second
                    counter += 1
                    if counter == 3 :
                        print ("cannot reach light: ", lights )
                        counter = 0
                        break

            if self.last_scene == len (self.scenes_in_group)-1 :
                self.last_scene = 0
            else :
                self.last_scene += 1

def read_bridge_info ():
    global bridge_bureau
    global lights_diction
    global group_diction
    global group_dic_name_lights
    global sensor_diction
    global scene_diction
    global scene_dic_name_lights
    global bridge_bureau_ip
    global laptop_username
    global iphone_bart
  
    # bridge_bureau is an object of type Bridge
    bridge_bureau = Bridge(ip = bridge_bureau_ip, username = iphone_bart)

    # make a Diction of all lights by names
    lights_diction = bridge_bureau.get_light_objects(mode="name")
    
    # make a Diction of all groups by key= name and value = [lights]
    group_diction = bridge_bureau.get_group()
    group_dic_name_lights = {}
   
    # make a diction of all sensors
    sensor_diction = bridge_bureau.get_sensor()
    for x in sensor_diction :
        if sensor_diction[x]["name"]=="Hal kamer Gust" :
            print (sensor_diction[x]["config"])
    

    # make a diction of all scenes

    scene_diction = bridge_bureau.get_scene()
    scene_dic_name_lights = {}
    return

try:
    #Initial setup
    print("Initial setup")
    GPIO.setmode(GPIO.BCM)
    # Bridge setup
    bridge_bureau_ip = "10.0.1.2"
    laptop_username = "Hc7SUdAjDIUVgu2Zpr4MU0zoP258UBl7W1u8GLqN"
    iphone_bart = 'fTK7yEWdh9HQaSfxZi94ArSpMlbT86DH67jjxAQj'
    # bridge_bureau is an object of type Bridge
    bridge_bureau = Bridge(ip = bridge_bureau_ip, username = iphone_bart)

    # make a Diction of all lights by names
    lights_diction = bridge_bureau.get_light_objects(mode="name")
    
    # make a Diction of all groups by key= name and value = [lights]
    group_diction = bridge_bureau.get_group()
    group_dic_name_lights = {}
   
    # make a diction of all sensors
    sensor_diction = bridge_bureau.get_sensor()
    for x in sensor_diction :
        if sensor_diction[x]["name"]=="Hal kamer Gust" :
           pass
            

    # make a diction of all scenes

    scene_diction = bridge_bureau.get_scene()
    scene_dic_name_lights = {}
    
    # Read list of switches out of text file switches.txt
    # txt files ends with "end"
    # connected_switches is a list of list with name switch, io port, group name

    with open ("switches.txt") as switches_file:
       read_switches =[ line for line in switches_file if line != "end"]
       connected_switches = [json.loads(x) for x in read_switches]
       print (connected_switches)

    # Create Switch Objects based on info in switches.txt   
    # switches[] is the list with all the switch objects
    switches = []
    for x in connected_switches :
        switches.append(Switch (x[0],x[1],x[2],iphone_bart))
    
    # set for all switches pull_up down definition and the add_event_detect
    for switch_object in switches :
        GPIO.setup(switch_object.switch_ioport,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch_object.switch_ioport,GPIO.FALLING,callback=switch_object.callback,bouncetime=200)

    # End of Inital Setup
        
   # while True:
        #time interval for update
        
        #time.sleep(60)
        #read_bridge_info()
        #for switch in switches :
            #switch.update_switch_attributes()
            #print ("switch : {} attributes updated ".format(switch))
        #print ("bridge info read at time: {} date: {} ".format(time.strftime("%H:%M:%S"),date.today()))
    #    pass

    w=windows()
    w.mainloop()
    GPIO.cleanup()
    print("bye bye")
except KeyboardInterrupt:
    GPIO.cleanup()
   

    

