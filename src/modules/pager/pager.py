from selenium import webdriver
import matplotlib
matplotlib.use('TkAgg')
from skimage import io
io.use_plugin('matplotlib')
import numpy as np
import atexit
from ..db.index import *
import os

IMGS_PATH = './src/modules/pager/screenshots'

class Pager:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./src/modules/pager/chromedriver")
    
    def get_websreen(self, name='', url='', id=''):
        path = f"{IMGS_PATH}/{id}"
        self.driver.get(url)
        if not os.path.isdir(path):
            os.makedirs(path)
        self.driver.get_screenshot_as_file(f"{path}/{name}.png")
     
    def get_img(self, name='', id=''):
        img = io.imread(f"{IMGS_PATH}/{id}/{name}.png")
        return img
    
    def get_path(self, name='', id=''):
        return f"{IMGS_PATH}/{id}/{name}.png"
    
    def update(self, name='', url='', id=''):
        old_img = []
        try:
            old_img = self.get_img(name, id)
        except:
            self.get_websreen(name, url, id)
            return {"name":name, "status":"new", "path":self.get_path(name, id)}
        
        self.get_websreen(name, url, id)
        new_img = self.get_img(name,id)

        return {"is_change": not np.array_equal(old_img,new_img), "name":name, "path":self.get_path(name,id), "status":"update"}
    
    def quit(self):
        self.driver.quit()

pager = Pager()

atexit.register(pager.quit)
# pager.check_changes(name='vk_com1', url="https://google.com")