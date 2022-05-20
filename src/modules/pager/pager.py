from selenium import webdriver
import matplotlib
matplotlib.use('TkAgg')
from skimage import io
io.use_plugin('matplotlib')
import numpy as np

class Pager:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver")
    
    def get_websreen(self, name='', url=''):
        self.driver.get(url)
        self.driver.get_screenshot_as_file(f"./screenshots/{name}.png")
        self.driver.quit()
     
    def get_img(self, name=''):
        img = io.imread(f"./screenshots/{name}.png")
        return img
    
    def check_changes(self, name='', url=''):
        img1 = self.get_img(name)
        self.get_websreen(name, url)
        img2 = self.get_img(name)
        return not img1.all() == img2.all()

pager = Pager()
print(pager.check_changes(name='vk_com1', url="https://google.com"))