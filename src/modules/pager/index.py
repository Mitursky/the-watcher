import matplotlib
matplotlib.use('TkAgg')

from skimage import io
from skimage import util
io.use_plugin('matplotlib')
import numpy as np
import atexit
from ..db.index import *

from skimage.transform import resize
from playwright.sync_api import sync_playwright
import os
import time
import zlib
from bot import *

IMGS_PATH = './modules/pager/screenshots'
MIN_CHANGED_ELEMENT_SIZE = 50*50
MIN_SIZE_CHANGED_ELEMENT_ON_SCREEN = 0.6
MAX_RATION_WIDTH_AND_HEIGHT = 5
MAX_OUTPUT_CHANGES_COUNT = 10

class Pager:   

    # get sites data in img or html mode
    def get_site_data(self, name='', url='', id='', type='img', message=None, tgbot=None):
        path = f"{IMGS_PATH}/{id}/{name}/"
        
        if not os.path.isdir(f"{IMGS_PATH}/{id}"):
            os.makedirs(f"{IMGS_PATH}/{id}")
            
        if not os.path.isdir(path):
            os.makedirs(path)
            
        if not os.path.isdir(path+'/changes'):
            os.makedirs(path+'/changes')

        with sync_playwright() as p:
            if tgbot:
                bot.edit_message_text_caption(message,  tgbot, "⌚ Открываем браузер")
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            if type == 'img':
                print('make screen')
                if tgbot:
                    bot.edit_message_text_caption(message, tgbot, "⌚ Делаем скриншот")
                page.screenshot(path=f"{path}/img.png", full_page=True)

            # swtich if type == 'img' or type == 'html'
            if type == 'html':
                start_time = time.time()
                print('html-check')
                

                old_html = False
                try:
                    old_html = open(f"{path}/index.html", 'r')
                    if old_html:
                        old_html = old_html.read().split('/wathcer-elem-tag/')
                except:
                    print('no old html')
                    old_html = False
                
                if tgbot:
                    if old_html:
                        bot.edit_message_text_caption(message,  tgbot, "⌚ Считываем предыдущий HTML файл")
                    else: 
                        bot.edit_message_text_caption(message,  tgbot, "⌚ Создаём новый HTML файл")

                changes_count = 0

                # download html of page
                html_data = open(f"{path}/index.html", 'w')
                
                # parse the html page to list of elements
                elems = page.query_selector_all('div')
                page_bounds = page.query_selector('body').bounding_box()

                for elem in elems:
                    # save the elements how text
                    if elem and elem.is_visible() and elem.inner_text() and elem.inner_html():
                        html_data.write(str(zlib.compress(elem.inner_text().encode()))+'/wathcer-elem-tag/')


                html_data.close()
                    # checking difference elements in elems and old_html
                    # make list of used elements
                used_list = ''
                    
                iterations = 0
                if old_html:
                    for elem in elems:
                        iterations += 1
                        # counting progress iterations of elems
                        print('Progress: ', str(iterations)+'/'+str(len(elems)))
                        # every 10% of progress edit message
                        if iterations % (len(elems)//10) == 0:
                            if tgbot:
                                bot.edit_message_text_caption(message,  tgbot, "⌚ Сравниваем элементы "+str(iterations)+'/'+str(len(elems)))

                        elem_bounds = elem.bounding_box()
                        
                        if not elem_bounds:
                            continue
                        try:
                            if (elem_bounds['width'] * elem_bounds['height'] < page_bounds['height']*page_bounds['width']*MIN_SIZE_CHANGED_ELEMENT_ON_SCREEN) and (not (elem_bounds['height'] / elem_bounds['width'] > MAX_RATION_WIDTH_AND_HEIGHT or elem_bounds['width'] / elem_bounds['height'] > MAX_RATION_WIDTH_AND_HEIGHT)) and (elem_bounds['width'] * elem_bounds['height'] > MIN_CHANGED_ELEMENT_SIZE) and elem.is_visible() and str(zlib.compress(elem.inner_text().encode())) not in old_html:
                                if elem.inner_html() not in used_list:
                                    elem.screenshot(path=f"{path}/changes/{changes_count}.png")
                                    changes_count += 1
                                    # save only 5 first elements
                                    if changes_count > MAX_OUTPUT_CHANGES_COUNT:
                                        break
                                    used_list += ('\n'+elem.inner_html())
                                    # add new element to used list
                        except:
                            pass
                    
                    browser.close()

                print('html-check done:', time.time() - start_time)

                return changes_count
     
    # get img 
    def get_img(self, name='', id=''):
        img = io.imread(f"{IMGS_PATH}/{id}/{name}/img.png")
        return img
    
    # get path to main user folder
    def get_path(self, name='', id=''):
        return f"{IMGS_PATH}/{id}/{name}"
    
    # find difference between two images
    def find_difference(self, old_img, new_img, name ,id):

        if old_img.shape[0] > new_img.shape[0]:
            white_image = old_img.copy()
        else:
            white_image = new_img.copy()

        white_image[:,:,:] = 1
        # if old_img.shape[0] not equal new_img.shape[0] add white line to the end of image
        if old_img.shape[0] < new_img.shape[0]:
            need_image = resize(white_image, (new_img.shape[0]-old_img.shape[0], old_img.shape[1]))
            old_img = np.concatenate((old_img, need_image), axis=0)

        if new_img.shape[0] < old_img.shape[0]:
            need_image = resize(white_image, (old_img.shape[0]-new_img.shape[0], new_img.shape[1]))
            new_img = np.concatenate((new_img, need_image), axis=0)
        new_img = np.where(new_img != old_img, new_img, white_image)

        io.imsave(f"{IMGS_PATH}/{id}/{name}/difference.png", util.img_as_ubyte(new_img))
    
    # update sites data in two mods img or html
    def update(self, name='', url='', id='', type='img', message=None, tgbot=None):
        if type == 'img':
            old_img = []

            try:
                old_img = self.get_img(name, id)
            except:
                self.get_site_data(name, url, id, type, message, tgbot)
                return {"name":name, "status":"new", "path":self.get_path(name, id)}

            self.get_site_data(name, url, id, type, message, tgbot)
            new_img = self.get_img(name,id)

            is_difference = not np.array_equal(old_img,new_img)
            if is_difference:
                if tgbot:
                    bot.edit_message_text_caption(message, tgbot, "⌚ Находим изменившиеся элементы")
                self.find_difference(old_img, new_img, name, id)
            
            return {"is_change": is_difference, "name":name, "path":self.get_path(name,id), "status":"update"}

        if type == 'html':
            is_html = True
            try:
                old_html = open(f"{self.get_path(name,id)}/index.html", 'r')
            except:
                is_html = False
            changes_count = self.get_site_data(name, url, id, type, message, tgbot)
            status = "update"
            if not is_html:
                status = "new"
            return {"is_change": changes_count > 0, "name":name, "path":self.get_path(name,id), "status": status, "changes_count":changes_count}

pager = Pager()