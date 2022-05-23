from selenium import webdriver
import matplotlib
matplotlib.use('TkAgg')

from skimage import io
from skimage import util
io.use_plugin('matplotlib')
import numpy as np
import atexit
from ..db.index import *
import os
from skimage.transform import rescale
import difflib

IMGS_PATH = './src/modules/pager/screenshots'

class Pager:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./src/modules/pager/chromedriver")
    
    def get_site_data(self, name='', url='', id=''):
        path = f"{IMGS_PATH}/{id}/{name}/"
        
        self.driver.get(url)
        html = self.driver.page_source
        
        
        old_html = open(f"{path}/index.html", 'r')
        if old_html:
            old_html = old_html.read()
            print(result)
            
        if not os.path.isdir(f"{IMGS_PATH}/{id}"):
            os.makedirs(f"{IMGS_PATH}/{id}")
            
        if not os.path.isdir(path):
            os.makedirs(path)
            
        html_file = open(f"{path}/index.html", 'w')
        html_file.write(html)
        html_file.close()
        
        self.driver.get_screenshot_as_file(f"{path}/img.png")

     
    def get_img(self, name='', id=''):
        img = io.imread(f"{IMGS_PATH}/{id}/{name}/img.png")
        return img
    
    def get_path(self, name='', id=''):
        return f"{IMGS_PATH}/{id}/{name}"
    
    def find_difference(self, old_img, new_img, name ,id):

        # old_img = rescale(old_img, 0.25, anti_aliasing=False)
        # new_img = rescale(new_img, 0.25, anti_aliasing=False)

        # for y in range(difference.shape[0]):
        #     for x in range(difference.shape[1]):
        #         if not str(difference[y,x]) == "[0.]":
        #             difference[y,x] = new_img[y,x]
      
        # difference = np.where(new_img != old_img, new_img, 0.0)
        difference = new_img - old_img
        io.imsave(f"{IMGS_PATH}/{id}/{name}/difference.png", difference)
    
    def update(self, name='', url='', id=''):
        old_img = []
        try:
            old_img = self.get_img(name, id)
        except:
            self.get_site_data(name, url, id)
           
            return {"name":name, "status":"new", "path":self.get_path(name, id)}
        
        self.get_site_data(name, url, id)
        new_img = self.get_img(name,id)

        is_difference = not np.array_equal(old_img,new_img)
        if is_difference:
            self.find_difference(old_img, new_img, name, id)
        
        return {"is_change": is_difference, "name":name, "path":self.get_path(name,id), "status":"update"}
    
    
    
    def quit(self):
        self.driver.quit()

pager = Pager()

atexit.register(pager.quit)
# pager.check_changes(name='vk_com1', url="https://google.com")