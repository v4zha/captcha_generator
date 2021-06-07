from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random


class captcha():
    def __init__(self, length, noise,img_name):

        # setup background image
        self.img_width=300
        self.img_height=150
        img_arr = np.zeros(shape=(self.img_height, self.img_width, 3), dtype=np.uint8)
        self.bg_array = {"black": img_arr, "white": img_arr+255}
        if random.randint(0, 1) == 0:
            self.bg_clr = "black"
            self.font_clr = "white"
            self.geo_clr = "white"
        else:
            self.bg_clr = "white"
            self.font_clr = "black"
            self.geo_clr = "black"
        
        self.captcha_text = self.get_text(length)
        # self.font_clr,self.geo_clr=self.get_clr()
        self.font_name =str(random.randint(1, 13)).zfill(2)+".ttf"
        self.font_size = 48
        self.noise = noise
        self.img = Image.fromarray(self.bg_array[self.bg_clr])
        self.text_coord = (int(self.img_width/10),0)
        self.img_name="./static/captcha_img/"+img_name+".png"

    def get_text(self, length):
        tot_char = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
        captcha = "".join(random.sample(tot_char, int(length)))
        return captcha

    def add_noise(self):
        img_arr = np.array(self.img)
        for i in range(img_arr.shape[0]):
            for j in range(img_arr.shape[1]):
                rand_val = random.random()
                # making pixels black and white :)
                if rand_val < self.noise:
                    img_arr[i][j] = 0
                elif rand_val > 1-self.noise:
                    img_arr[i][j] = 255

        self.img = Image.fromarray(img_arr)

    def add_text(self):
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype('./font/'+self.font_name, self.font_size)
        x,y=(self.text_coord)
        for i in range(len(self.captcha_text)):            
            fac=random.randint(int(self.img_height/3),int(2*self.img_height/3))
            del_y=fac+y
            draw.text((x,del_y), self.captcha_text[i],font=font, fill=self.font_clr)
            x+=self.img_width/7

    def save_img(self):
        self.img.save(self.img_name)

    def add_geo(self):
        # 0->line
        # 1->rectangle
        # 2-> ellipse
        # 3->arc
        # def text coord-> 20,11
        # image size -> 65, 150
        height_fac=int(self.img_height/2)
        width_fac=int(self.img_width/2)
        geo_width=2
        img_draw = ImageDraw.Draw(self.img)
        lines = random.randint(4, 7)
        for i in range(0, lines):
            try:
                x1 = random.randint(0, self.img_width)
                y1 = random.randint(0, self.img_width)
                x2 = random.randint(0, self.img_width)
                y2 = random.randint(0, self.img_width)
                img_draw.line(((x1, y1), (x2, y2)), width=geo_width, fill=self.geo_clr)
            except Exception as err:
                print(err)
                continue
        # no of shapes to generate
        shape_no = random.randint(2, 4)
        for i in range(shape_no):
            # type of shape to generate
            shape_gen = random.sample([1, 2, 3], 2)
            if 1 in shape_gen:

                # 1-> rectangle
                # lower left x coordinate
                x1 = random.randint(0, width_fac)
                # lower left y coordinate
                y1 = random.randint(0, height_fac)
                # upper right x coordinate
                x2 = random.randint(width_fac+1, self.img_width)
                # upper right y coordinate
                y2 = random.randint(height_fac+1, self.img_width)
                # draw rectangle :)

                img_draw.rectangle(((x1, y1), (x2, y2)), outline=self.geo_clr,width=geo_width)

            if 2 in shape_gen:
                # 2->ellipse
                # create bounding box :)
                # lower left x coordinate
                x1 = random.randint(0, width_fac)
                # lower left y coordinate
                y1 = random.randint(0,height_fac)
                # upper right x coordinate
                x2 = random.randint(width_fac+1, self.img_width)
                # upper right y coordinate
                y2 = random.randint(height_fac+1, self.img_width)
                # draw ellipse
                img_draw.ellipse(((x1, x2), (y1, y2)), outline=self.geo_clr,width=geo_width)

            if 3 in shape_gen:
                # create bounding box :)
                # lower left x coordinate
                x1 = random.randint(0, width_fac)
                # lower left y coordinate
                y1 = random.randint(0, height_fac)
                # upper right x coordinate
                x2 = random.randint(width_fac+1, self.img_width)
                # upper right y coordinate
                y2 = random.randint(height_fac+1, self.img_width)
                # start angle  in degree
                start = random.randint(0, 90)
                # end angle in degree
                end = random.randint(180, 270)
                img_draw.arc(((x1, x2), (y1, y2)), start=start,
                             end=end, fill=self.geo_clr,width=geo_width)

    def generate_captcha(self):
        self.add_geo()
        self.add_text()
        self.add_noise()
        self.save_img()
        return self.captcha_text
