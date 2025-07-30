`import cv2 as cv
import pyautogui as py
import numpy as np
import time;
import random
import socket
import threading
       
connect=True
flag=False
def is_online(host="8.8.8.8",port=53,timeout=3):
    while(True):
        global connect
        #print(connect)
        try:
            socket.setdefaulttimeout(timeout)
            socket.create_connection((host,port))
            connect=True
        except(socket.timeout,socket.error):
            connect=False



# for clicking the buttom in random way
def click_button(bx_start,bx_end,by_start,by_end,flag):
     if(not connect):
         flag=True
         return
     # get the random coordinates
     x=random.randint(bx_start,bx_end)
     y=random.randint(by_start,by_end)

     
     # now click the mouse cursor in a random way
     duration=random.uniform(0.8,1.3)
     py.moveTo(x,y,duration=duration,tween=py.easeInOutQuad)

     # if flag is true
     if(flag==True):
         # first : how many clicks
         click=random.randint(1,5)
         # time bw clicks
         interval=random.uniform(0.2,0.4)
         py.click(button='left',clicks=click,interval=interval)
     # if flag is false then click only once 
     else:
          py.click()

         

# for adding the random delays in the clicks
def random_delay():
    delay=random.uniform(0.5, 3)
    time.sleep(delay)
    

#to caputure the image and convert it into opencv format
# and more specifically get the data of region of interest
def get_image_data(x,y,width,height):
    #first we will take screenshot of the entire screen;
    screenshot=py.screenshot()
    image=np.array(screenshot)
    #convert it into open cv usable form
    image=cv.cvtColor(image,cv.COLOR_RGB2BGR)
    #now determine our roi where we want our image data to analysed
    roi=image[y:y+height,x:x+width]
    return roi

# to detect the end of the match
def detect_end(x,y,width,height,r,g,b,tolerance):
    #first of all get the usable data for specific part we need
    roi=get_image_data(x,y,width,height)
    #now get the avg of the roi
    avg_row=np.mean(roi,axis=0)
    avg_color=np.mean(avg_row,axis=0)
     # print(avg_color) # its in BGR
    if( (avg_color[0]<=tolerance+b)and(avg_color[0]>=b-tolerance) and
        (avg_color[1]<=tolerance+g)and(avg_color[1]>=g-tolerance) and
        (avg_color[2]<=tolerance+r)and(avg_color[2]>=r-tolerance) ):
        
        return True
    print(avg_color) # its in BGR
    return False


def find_points(start_x,end_x,start_y,end_y,points):
    # when out of bound
    if(start_y>=end_y):
        return

    # define the sampling distance randomly: i.e the distance bw two points to be considered
    distance=random.randint(200,250)
    for i in range(start_x,end_x,distance):
        points.append([i,start_y])

    #now go down some  rows to get more points
    down=random.randint(100,150)
    find_points(start_x,end_x,start_y+down,end_y,points)
        
        
# now this is fast custom click with number of clicks specified
def custom_click(x,y,repeat):
    if(not connect):
        Flag=True
        return
    duration=random.uniform(0.7,1)
    py.moveTo(x,y,duration=duration,tween=py.easeInOutQuad)
    click=random.randint(repeat,repeat+2)
    interval=random.uniform(0.08 ,0.15)
    py.click(button='left',clicks=click,interval=interval)
    
# the trigger function
def trigger(x,y):

    # then click many times there
    custom_click(x,y,5)
    #if is triggers then return true else return false
    # detect_ end coord can be different as per troop
    # for bar:detect_end(348,882,43,19,119.5,119.5,119.5,15)
    if(detect_end(348,882,43,19,119.5,119.5,119.5,40)):
        return True
    return False

     
#find trigger point to releasing the troops
def find_trigger():

    #first of all collect all the random points for testing then
    points=[]
    find_points(292,1790,80,835,points)
    # now we will shuffle the points
    print(len(points))
    random.shuffle(points)
    #after that we will move our cursor to each point  release the first troop and if if it does it then return from there
    for  i in range(len(points)):
        #print("x: ", points[i][0],"y: ", points[i][1])
        print(i)
        #if goes offline then do the convention
        if(not connect):
            Flag=True
            return
        #now lets move our pointer to these points and see if it causes trigger
        if(trigger(points[i][0],points[i][1])==True):
            print("trigger found ")
            print("x: ", points[i][0],"y: ", points[i][1])
            return



    
# function for deploying troops
def deploy_troops():
    """ what will we do  is that image the l shape we have the top left most corner and two end points making L (upside down)
        we will examine all the points with some differnce bw them on this L and then reduce the size of this L  and do the same
        untill we get the point which produces the reaction of deployment of troops i.e turning dark of that area
        once we got this trigger point we can use it to deploy every other troop """
    # step 1 : zoom out as much as possible
    zoom_out=random.randint(40,70)
    py.scroll(-zoom_out)

    #activate first troop by clicking on it 992
    click_button(346,427,880,940,False)
    #step2:moving the mouse to the trigger point
    find_trigger()

    #step3: deploying all the troops to the trigger point
    x,y=py.position()
    time.sleep(1.4)
    click_button(461,542,880,992,False)
    custom_click(x,y,5)
    time.sleep(1.1)
    click_button(579,663,880,992,False)
    custom_click(x,y,5)
    time.sleep(1.2)
    click_button(697,777,880,992,False)
    custom_click(x,y,5)
    
    # again clicking for boost useless though
    click_button(461,542,880,992,False)
    
    click_button(579,663,880,992,False)
    
    click_button(697,777,880,992,False)
    
"""
while(True):
    time.sleep(5)
    print(detect_end(348,882,43,19,119.5,119.5,119.5,5) )
 """
count=0;

#launch a thread for continuos internet monitoring
connectivity=threading.Thread(target=is_online)
connectivity.start()


#HERE ONWARDS OUR MAIN GAME LOOP WILL START
while(True):
     count=count+1
     print("we have done for: ",count," so far")
    
     #don't proceed until we are online
     # we will come to know we are not online when the flag will be raised
     if(flag==True):
         while(True):
             print("we are offline")
             time.sleep(5)
             click_button(598,655,563,572,True)
             if(connect):
                 print("back online")
                 time.sleep(2)
                 break

          
     # wait for to come to home screen
     flag=False  # the flag is used for  continue loop if internet goes off
     while(True):
          #[114.80407524 234.01567398 205.60501567]
          #100.82915361 205.61755486 180.60501567
          # if we got offline during this continue to next loop again and wait there for getting online
          if(not connect):
               flag=True;
               break
          if((detect_end(1774,219,29,22,180,205,100,40)==True)or(detect_end(1774,219,29,22,205,234,114,40)==True)):
               break
          time.sleep(1.2)
     #if no internet;
     if(flag==True):
          continue

     
     #wait additional seconds
     wait_time=random.uniform(2,5)
     time.sleep(wait_time)
     print("starting again !")
     # part1: MATCHMAKING
     # start by clicking at match button:
     click_button(120,221,865,975,False)
     #add delay
     random_delay()
     click_button(1226,1544,631,731,True)
     #wait until you get the attack screen
     flag=False
     while(True):
         # for bar:if(detect_end(348,882,43,19,60,121,254 ,15)==True)
         # universal detection: surrender button[144.73076923 137.88461538 134.61538462]
         if(not connect):
              flag=True;
              break
         if(detect_end(348,882,43,19,60,121,254 ,40)==True):
             break
         time.sleep(1.1)
     #if no internet;
     if(flag==True):
          continue

     
     print("deploying troops")
     #254.90820073 121.21542228  60.77600979
     #part2:DEPLOYING TROOPS
     deploy_troops()
     print("deploying troops successfull")
    
     #part3:RETURN TO MAIN MENU
     #when to return to menu
     """ two cases are there when we have to return to the home
     first: the match has ended early (using detect_end())
     second: the match will automatcially terminated after 3 minutes
     either of the two options we can  have"""
     start_time=time.time()
     end_time=start_time+190# add 180 (3 minutes) that will indicate the end
     flag=False
     while(True):
         if(not connect):
              flag=True;
              break  
    
         #stop if current_time exceeds the end_time
         current_time=time.time()
         if(current_time>=end_time):
             print("returning home via end_time")
             break
         #stop if deted_end returned true
         if(detect_end(90,920,1600,80,0,0,0,15) ):
             print("returning home via detect_end()")
             break
         # else pause for 5 seconds to continue the process again
         time.sleep(5);
     #if no internet;
     if(flag==True):
          continue
    
     #iniciate the return home click
     click_button(855,1061,832,910,True)
     #move to random points
    
connectivity.join()
    
    
    
