from PIL import ImageFont,ImageDraw,Image 
import numpy as np
import random 

class captcha():
   def __init__(self,length,noise):
    #setup background image
    img_arr=np.zeros(shape=(65,150,3),dtype=np.uint8)
    self.bg_array={"black":img_arr,"white": img_arr+255}
    if random.randint(0,1) == 0:
        self.bg_clr="black"
        self.font_clr="white"
        self.geo_clr="white"
    else:
        self.bg_clr="white" 
        self.font_clr="black" 
        self.geo_clr="black"  

    self.captcha_text=self.get_text(length)
    #self.font_clr,self.geo_clr=self.get_clr()
    self.font_name="font"+str(random.randint(11,17))+".ttf"
    self.font_size=28
    self.noise=noise
    self.img=Image.fromarray(self.bg_array[self.bg_clr])
    self.text_coord=(20,11)
   
   def get_text(self,length):
       tot_char="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890" 
       captcha="".join(random.sample(tot_char,int(length)))
       return captcha

   def add_noise(self):
       img_arr=np.array(self.img)
       for i in range(img_arr.shape[0]):
           for j in range(img_arr.shape[1]):
                  rand_val=random.random()
                  #making pixels black and white :)
                  if rand_val<self.noise:
                      img_arr[i][j] =0
                  elif rand_val>1-self.noise:
                      img_arr[i][j]=255
        
       self.img=Image.fromarray(img_arr)              
    
   def add_text(self):
       draw=ImageDraw.Draw(self.img)
       font=ImageFont.truetype('./font/'+self.font_name,self.font_size)
       draw.text(self.text_coord,self.captcha_text,font=font,fill=self.font_clr)
   
   def save_img(self):
        self.img.save('captcha.png')

   def add_geo(self):
       #0->line
       #1->rectangle
       #2-> ellipse 
       #3->arc
       #def text coord-> 20,11
       #image size -> 65, 150
       img_draw=ImageDraw.Draw(self.img)
       lines=random.randint(4,7)       
       for i in range(0,lines):                 
             try:
                 x1=random.randint(0,150)
                 y1=random.randint(0,65)
                 x2=random.randint(0,150)
                 y2=random.randint(0,65)
                 img_draw.line(((x1,y1),(x2,y2)),width=1,fill=self.geo_clr)
             except Exception as err:
                 print(err)
                 continue
       #no of shapes to generate
       shape_no=random.randint(2,4)
       for i in range(shape_no):
          #type of shape to generate
          shape_gen=random.sample([1,2,3],2)
          if 1 in shape_gen:
              
              #1-> rectangle
              #lower left x coordinate 
              x1=random.randint(0,75)
              #lower left y coordinate
              y1=random.randint(0,32)
              #upper right x coordinate
              x2=random.randint(75,150)
              #upper right y coordinate
              y2=random.randint(33,65)  
              #draw rectangle :)
              
              img_draw.rectangle(((x1,y1),(x2,y2)),outline=self.geo_clr)
          
          if 2 in shape_gen:
              #2->ellipse
              #create bounding box :)
              #lower left x coordinate 
              x1=random.randint(0,75)
              #lower left y coordinate
              y1=random.randint(0,32)
              #upper right x coordinate
              x2=random.randint(75,150)
              #upper right y coordinate
              y2=random.randint(33,65)    
              #draw ellipse
              img_draw.ellipse(((x1,x2),(y1,y2)),outline=self.geo_clr)
          
          if 3 in shape_gen:
               #create bounding box :)
              #lower left x coordinate 
              x1=random.randint(0,75)
              #lower left y coordinate
              y1=random.randint(0,32)
              #upper right x coordinate
              x2=random.randint(75,150)
              #upper right y coordinate
              y2=random.randint(33,65)    
              #start angle  in degree
              start=random.randint(0,90)
              #end angle in degree
              end=random.randint(180,270)
              img_draw.arc(((x1,x2),(y1,y2)),start=start,end=end,fill=self.geo_clr)


   def generate_captcha(self):
    self.add_geo()
    self.add_text()        
    self.add_noise()   
    self.save_img()

cap=captcha(5,0.06)
cap.generate_captcha()