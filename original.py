# modules used
from tkinter import *  # tkinter
from tkinter import font # tkFont
from tkinter import messagebox #message box
import time # time module
import base64 # base 64 module
# from urllib.request import urlopen # url open
from collections import OrderedDict # OrderedDict from collections module# make the window
window = Tk()
window.title("Make Your Own Schedule!") # title
window.geometry("850x532") # default dimensions
# container
container = Frame(window) # a frame to 'replace' the window
container.pack(expand=True,fill=BOTH) # fill the entire window
container.grid_rowconfigure(0,weight=1)
container.grid_columnconfigure(0,weight=1)
# output variables
Schedule = {} # Dictionary where all events in the schedule will be stored
currenttime = (time.localtime(time.time())[3]) *60 + (time.localtime(time.time())[4])   # get the current time in the form of minutes
schedulestarttime,lunchtime,dinnertime,endlunchtime,enddinnertime = currenttime,0,0,0,0
beforeschool = False
# set fonts
headfont = font.Font(family="Ink Free",size = 26, weight="bold")
textfont = font.Font(family="HelvLight",size = 12, weight = "bold")
subfont = font.Font(family = "Ink Free",size = 20,weight="bold")
# set the background color
backcolor = "#edf3ff"
buttoncolor = "#4583e8"
#  set all screens
screens = []
for screen in range(9):
    screens.append(Frame(container,bg = backcolor))
    screens[screen].grid(row=0,column=0,sticky="nsew")
# functions
def makeSchedule(screen):  # function to use all of the events in Schedule dict to make a schedule
    global schedulestarttime,assignments,Schedule,taskname,tasktime
    if (not beforeschool):
        schedulestarttime = (time.localtime(time.time())[3]) *60 + (time.localtime(time.time())[4])
    registerAssignment(taskname.get(),tasktime.get())
    Schedule = OrderedDict(sorted(Schedule.items(),key=lambda x:x[1]))
    assignmentnum = 0
    limit = len(assignments)
    while assignmentnum < limit: # for every task
        task = list(assignments.keys())[assignmentnum] # get the task name
        index = 0
        for event in Schedule: # for each event
            nexteventstart = -1 # set next event start to a time that can never be after the schedule start time when the next event isn't after the schedule start time
            if index + 1 < len(Schedule): # as long as the index for the next element is less than the limit (1 less than that of the actual length)
                index += 1
                nexteventstart = int(list(Schedule.values())[index][0]) # set it to the start of the next event only if there is a 'next event'
            if (Schedule[event][0] >= schedulestarttime) and (index == 1): # if the event starting time is right after the time the schedule starts
                if addAssignmentBetweenEvent(task,schedulestarttime,Schedule[event][0]) == True:
                    break
            if Schedule[event][1] >= schedulestarttime:
                if addAssignmentBetweenEvent(task,Schedule[event][1],nexteventstart) == True:
                    break
            elif nexteventstart >= schedulestarttime: # NOTE: elif used because the program might not be able to add assignment between the first event end time and the next event, in which case, it shouldn't just plop in assignment
                if addAssignmentBetweenEvent(task,schedulestarttime,nexteventstart) == True:
                    break
        limit = len(assignments)
        assignmentnum += 1
    printSchedule(screen, Schedule)

def addAssignmentBetweenEvent(task,time1,time2):  # add assignment between events in schedule
    done = False
    if (time2 - time1) >= assignments[task]:  # see if there is time for the homework between it and the event after it
        markScheduleEvent(str(task), time1, time1 + assignments[task])
        done = True
    elif (time2 - time1) > 0:  # see if there is any time at all
        markScheduleEvent(str(task), time1, time2)
        registerAssignment(str(task) + " Continued", assignments[task] - (time2 - time1))  # make another assignment that will be a continuation of the homework assignment
        done = True
    return done

def printSchedule(screen,Schedule):
    scrollbar = Scrollbar(screens[8],orient=VERTICAL)
    schedulebox = Listbox(screens[8],yscrollcommand=scrollbar.set)
    scrollbar.config(command=schedulebox.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    schedulebox.config(font=subfont,bg=backcolor)
    schedulebox.pack(side=LEFT,fill=BOTH,expand=1)
    schedulebox.insert(0,"Schedule")
    print("Schedule")
    schedulebox.itemconfig(0,{'fg': 'red'})
    Schedule = OrderedDict(sorted(Schedule.items(), key=lambda x: x[1]))
    for event in Schedule:
        firsthour,firstminute = MinutestoTime(Schedule[event][0])
        secondhour,secondminute = MinutestoTime(Schedule[event][1])
        item = firsthour + ":" + firstminute + " to " + secondhour + ":" + secondminute + " " + str(event)
        print(item)
        schedulebox.insert(END,item)
    screens[screen].tkraise()

def MinutestoTime(minutes):
    hour = int(minutes/60)
    if hour > 12:
        hour = hour - 12
    minutes = abs(minutes) % 60
    if hour == 0:
        hour = "00"
    if minutes == 0 or minutes < 10:
        minutes = "0" + str(minutes)
    return str(hour),str(minutes)

def timeEntry(screen,initial,x,y):
    Hour = makeWidget("Entry", "hr", screen, 0.05, 0.05,x,y)
    colon = makeWidget("Label", ":", screen, 0.05, 0.05,x+0.05,y)
    minute = makeWidget("Entry", "min", screen, 0.05, 0.05,x+0.1,y)
    ampmoptions = ["AM","PM"]
    ampm = StringVar(window)
    ampm.set(initial)
    dropampm = OptionMenu(screens[screen],ampm,*ampmoptions)
    placeWidget(dropampm,0.1,0.05,x+0.2,y)
    return Hour, colon, minute, ampm,dropampm

def makeWidget(type,text,screen,width,height,x,y,command = None,font=textfont,image=None):
    var = 0
    if type == "Label":
        var = Label(screens[screen],text = text, image = image,bg = backcolor)
        var.image = image # keep a reference to the image if used
    elif type == "Button":
        var = Button(screens[screen],borderwidth = 0,text = text,image=image,bg = buttoncolor,fg = "#ffffff",command=command)
    elif type == "Entry":
        var = Entry(screens[screen])
        var.insert(END,text)
    elif type == "Message":
        var = Message(screens[screen],text = text, bg = backcolor)
    elif type == "Dropdown":
        tkvar = StringVar(window)
        var = OptionMenu(screens[screen],tkvar,*text)
    placeWidget(var,width,height,x,y,font)
    return var

def placeWidget(widget,width,height,x,y,font=textfont):
    widget.configure(font=font)
    widget.place(relwidth = width,relheight = height,relx = x,rely = y)

def addMealTimes(screen,lshour,lsminute,lehour,leminute,lampm,lempm,dshour,dsminute,dehour,deminute,dampm,dempm):
    # use the parameters given to get the lunch time and dinner time slots.
    global lunchtime,dinnertime,endlunchtime,enddinnertime
    lunchtime = TimeToMinutes(numberof(lshour.get()),numberof(lsminute.get()),lampm.get())
    endlunchtime = TimeToMinutes(numberof(lehour.get()),numberof(leminute.get()),lempm.get())
    dinnertime = TimeToMinutes(numberof(dshour.get()),numberof(dsminute.get()),dampm.get())
    enddinnertime = TimeToMinutes(numberof(dehour.get()),numberof(deminute.get()),dempm.get())
    if lunchtime < dinnertime and endlunchtime < dinnertime: # check if lunch occurs before dinner time
        if "School" not in Schedule.keys() or lunchtime >= Schedule["School"][1]: # as long as the user eats lunch after school
            Schedule["Lunch"] = [lunchtime,endlunchtime] # add it in his/her schedule
        Schedule["Dinner"] = [dinnertime,enddinnertime] # add dinner time as well
        screens[screen].tkraise()
    else:
        messagebox.showerror("Error", "I am pretty sure you eat lunch before dinner")

def addSchoolTime(screen,starthour,startminute,endhour,endminute,ampm,ampm1):
    global schedulestarttime, currenttime
    starttime = TimeToMinutes(numberof(starthour.get()),numberof(startminute.get()),ampm.get())
    endtime = TimeToMinutes(numberof(endhour.get()),numberof(endminute.get()),ampm1.get())
    Schedule["School"] = [starttime,endtime]
    bedtime = addBedtime(starttime-60)
    Schedule["Sleep"] = [bedtime,starttime-60]
    if currenttime < starttime:
        if currenttime >= starttime-60:
            Schedule["Prepare for School"] = [currenttime,starttime]
        else:
            Schedule["Prepare for School"] = [starttime-60,starttime]
        beforeschool = True
        schedulestarttime = endtime
    elif currenttime >= starttime and currenttime < endtime:
        Schedule["School"] = [currenttime,endtime]
        beforeschool = True
        schedulestarttime = endtime
    else:
        schedulestarttime = currenttime
    screens[screen].tkraise()

def addBreakfast(screen,eatingtime):
    global schedulestarttime
    Schedule["Breakfast"] = [schedulestarttime,schedulestarttime + numberof(eatingtime)]
    schedulestarttime += numberof(eatingtime)
    screens[screen].tkraise()

def addBedtime(wakeuptime):
    if (wakeuptime - 480) < 0:
        bedtime = 1440 + (wakeuptime - 480)
    else:
        bedtime = (wakeuptime - 480)
    return bedtime

def TimeToMinutes(hour,minute,ampm):
    if (ampm == "PM" and hour != 12) or (ampm == "AM" and hour == 12):
        hour += 12
    return hour * 60 + minute
def numberof(str):
    try:
        number = int(str)
        return number
    except:
        messagebox.showerror("Error","Please enter a proper number(s)")

def addEvent(screen,x, width):
    global questionx,eventaddbutton, eventname,ehour,ecolon,eminute,eampm3,edropampm3, eventy, eventaddbutton,ehourend,ecolonend,eminuteend,eampm4end,edropampm4end
    assigntoSchedule(eventname,ehour,eminute,eampm3,ehourend,eminuteend,eampm4end)
    eventx = lunchx + 0.05
    eventy += 0.1
    eventname = makeWidget("Entry","Event Name",6,questionwidth/2,0.05,questionx,eventy)
    ehour,ecolon,eminute,eampm3,edropampm3 = timeEntry(6,"PM",eventx,eventy)
    to = makeWidget("Label","To",6,0.05,0.05,eventx+0.3,eventy)
    ehourend,ecolonend,eminuteend,eampm4end,edropampm4end = timeEntry(6,"PM",eventx+0.4,eventy)
    eventaddbutton.place(rely = eventy + 0.1)

def registerEvents(screen):
    global eventname,ehour,eminute,eampm3,ehourend,eminuteend, eampm4end
    assigntoSchedule(eventname,ehour,eminute,eampm3,ehourend,eminuteend,eampm4end)
    screens[screen].tkraise()

def assigntoSchedule(name,hour1,minute1,ampm1,hour2,minute2, ampm2):
    start = TimeToMinutes(numberof(hour1.get()),numberof(minute1.get()),ampm1.get())
    end = TimeToMinutes(numberof(hour2.get()), numberof(minute2.get()), ampm2.get())
    Schedule[(name.get())] = [start, end]

def markScheduleEvent(name,start,end):
    global Schedule
    Schedule[name] = [start, end]
    Schedule = OrderedDict(sorted(Schedule.items(), key=lambda x: x[1]))

def addAssignment(screen):
    global assignments,assignmenty,assignmentx,taskname,tasktime
    assignmenty += 0.1
    registerAssignment(taskname.get(),tasktime.get())
    taskname = makeWidget("Entry","Assignment Name",screen,questionwidth,0.05,assignmentx,assignmenty)
    tasktime = makeWidget("Entry","Time(in minutes)",screen,questionwidth,0.05,assignmentx+questionwidth+0.1,assignmenty)
    addassignment.place(rely = assignmenty + 0.1)

def registerAssignment(name,time):
    global assignments
    if name not in assignments.keys() and time not in assignments.values():
        assignments[name] = numberof(time)
# heading
heading = makeWidget("Label","Make Your Own Schedule!",0,0.9,0.1,0.05,0.05,font=headfont)
### photo of routinely person
##routineimg = PhotoImage(data = base64.encodestring( urlopen("http://umbrellawithdee.com/wp-content/uploads/2016/09/Routine.png").read()))  # This image was retrieved from UR Umbrella with dee
##routinelyperson = makeWidget("Label","something",0,0.5,0.4,0.25,0.15,image=routineimg)
# description of the program's purpose
purpose = makeWidget("Message","Tired of staying up all night because of homework? Well, you've come to the right place! We will make a schedule for you for tonight based on the homework assignments you have.",0,0.5,0.3,0.25,0.25)
# button to go to the next screen 
next = makeWidget("Button","Start!",0, 0.2, 0.1, 0.4, 0.65,command=lambda:screens[1].tkraise())
# -- second screen (Weekday or weekend?)--
# elements for second screen
# heading for second
heading2 = makeWidget("Label","Is it a weekday or weekend?",1,0.9,0.1,0.05,0.45,font=headfont)
# button for weekday 
weekdaybtn = makeWidget("Button","Weekday",1,0.2,0.1,0.25,0.65,command=lambda:screens[2].tkraise())
# button for weekend
weekendbtn = makeWidget("Button","Weekend",1,0.2,0.1,0.55,0.65,command=lambda:screens[3].tkraise())
# variable to track which screen was visited
weekdayorend = 0
# -- third screen (School Hours)--
# heading
heading3 = makeWidget("Label","School Hours",2,0.9,0.1,0.05,0.05,font=headfont)
# Ask User When He Leaves For School
questionwidth = 0.4
questionx = 0.15
timewidth = 0.05
askleave = makeWidget("Label","When do you leave for school?",2,questionwidth,0.05,questionx,0.25)
Leavehour, Leavecolon, Leaveminute, ampm1,dropampm1 = timeEntry(2,"AM",questionx+questionwidth+timewidth,0.25)
# Ask User when He/She Returns Home
askreturn = makeWidget("Label","When do you return home?",2,questionwidth,0.05,questionx,0.45)
Returnhour,Returncolon,Returnminute,ampm2,dropampm2 = timeEntry(2,"PM",questionx+questionwidth+timewidth,0.45)
# button to go to the next screen
toscreen4 = makeWidget("Button","Next",2,0.1,0.1,0.8,0.85,command=lambda:addSchoolTime(5,Leavehour,Leaveminute,Returnhour,Returnminute,ampm1,ampm2))
# previous button
back3 = makeWidget("Button","Back",2,0.1,0.1,0.1,0.85,command=lambda:screens[1].tkraise())
# -- fourth screen (Morning Routine)--
# heading
heading4 = makeWidget("Label","Morning Routine",3,0.9,0.1,0.05,0.05,font=headfont)
# ask did user have breakfast
breakfast = makeWidget("Label","Did you have breakfast?",3,0.9,0.1,0.05,0.45,font=subfont)
# button for weekday
Yes = makeWidget("Button","Yes",3,timewidth,0.1,0.5 - 2*(timewidth),0.65,command=lambda:screens[5].tkraise())
# button for weekend
No = makeWidget("Button","No",3,timewidth,0.1,0.5 + timewidth,0.65,command=lambda:screens[4].tkraise())
# previous button
back4 = makeWidget("Button","Back",3,0.1,0.1,0.1,0.85,command=lambda:screens[1].tkraise())
# -- fifth screen (Time needed to eat breakfast) --
heading5 = makeWidget("Label","How long will it take you to eat breakfast?",4,0.9,0.1,0.05,0.2,font=headfont)
breakfasttime = makeWidget("Entry","Time(in minutes)",4,0.6,0.05,0.2,0.6)
#previous button
back5 = makeWidget("Button","Back",4,0.1,0.1,0.1,0.85,command=lambda:screens[3].tkraise())
#next button
toscreen6 = makeWidget("Button","Next",4,0.1,0.1,0.8,0.85,command=lambda:addBreakfast(5,breakfasttime.get()))
# -- sixth screen (Meal Times)--
# heading
heading6 = makeWidget("Label","Meal Times",5,0.9,0.1,0.05,0.05,font=headfont)
# Ask User about Lunch
questionwidth = 0.3
questionx = 0.05
timewidth = 0.05
lunchx = questionx+questionwidth/3+timewidth
asklunch = makeWidget("Label","Lunch",5,questionwidth/2,0.05,questionx,0.25,font=subfont)
lunchhour,lunchcolon,lunchminute,ampm3,dropampm3 = timeEntry(5,"PM",lunchx,0.25)
to = makeWidget("Label","To",5,0.05,0.05,lunchx+0.3,0.25)
lunchend,lunchendcolon,lunchendminute,ampm4,dropampm4 = timeEntry(5,"PM",lunchx+0.4,0.25)
# Ask User about dinner
askdinner = makeWidget("Label","Dinner",5,questionwidth/2,0.05,questionx,0.45,font=subfont)
dinnerhour,dinnercolon,dinnerminute,ampm5,dropampm5 = timeEntry(5,"PM",lunchx,0.45)
secondto = makeWidget("Label","To",5,0.05,0.05,lunchx+0.3,0.45)
dinnerend,dinnerendcolon,dinnerendminute,ampm6,dropampm6 = timeEntry(5,"PM",lunchx+0.4,0.45)
# previous button
back7 = makeWidget("Button","Back",5,0.1,0.1,0.1,0.85,command=lambda:screens[1].tkraise())
#next button
toscreen7 = makeWidget("Button","Next",5,0.1,0.1,0.8,0.85,command=lambda:addMealTimes(6,lunchhour,lunchminute,lunchend,lunchendminute,ampm3,ampm4,dinnerhour,dinnerminute,dinnerend,dinnerendminute,ampm5,ampm6))
# -- seventh screen (Other Events)
# heading
heading7 = makeWidget("Label","Other Events",6,0.9,0.1,0.05,0.05,font=headfont)
# Ask User about Event
eventx = lunchx + 0.05
eventy = 0.25
eventname = makeWidget("Entry","Event Name",6,questionwidth/2,0.05,questionx,eventy)
ehour,ecolon,eminute,eampm3,edropampm3 = timeEntry(6,"PM",eventx,eventy)
to1 = makeWidget("Label","To",6,0.05,0.05,eventx+0.3,eventy)
ehourend,ecolonend,eminuteend,eampm4end,edropampm4end = timeEntry(6,"PM",eventx+0.4,eventy)
eventaddbutton = makeWidget("Button","Add Event",6,questionwidth,0.05,eventx,eventy + 0.1,command=lambda:addEvent(7,eventx,questionwidth))
# previous button
back8 = makeWidget("Button","Back",6,0.1,0.1,0.1,0.85,command=lambda:screens[1].tkraise())
#next button
toscreen8 = makeWidget("Button","Next",6,0.1,0.1,0.8,0.85,command=lambda:registerEvents(7))
# -- eighth screen (Homework Assignments)
heading8 = makeWidget("Label","Homework",7,0.9,0.1,0.05,0.05,font=headfont)
assignmenty = 0.25
assignmentx = 0.15
assignments = {}
taskname = makeWidget("Entry","Assignment Name",7,questionwidth,0.05,assignmentx,0.25)
tasktime = makeWidget("Entry","Time(in minutes)",7,questionwidth,0.05,assignmentx+questionwidth+0.1,0.25)
addassignment = makeWidget("Button","Add Assignment",7,questionwidth,0.05,assignmentx,0.35,command=lambda:addAssignment(7))
# previous button
back6 = makeWidget("Button","Back",7,0.1,0.1,0.1,0.85,command=lambda:screens[5].tkraise())
#next button
toscreen9 = makeWidget("Button","Next",7,0.1,0.1,0.8,0.85,command=lambda:makeSchedule(8))
#ninth screen (Schedule)
heading9 = makeWidget("Label","Schedule:",8,0.9,0.1,0.05,0.05,font=subfont)
# show first screen
screens[0].tkraise()
window.mainloop()
