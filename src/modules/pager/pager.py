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
IMGS_PATH = './src/modules/pager/screenshots'

class Pager:   
    def get_site_data(self, name='', url='', id='', type='img'):
        path = f"{IMGS_PATH}/{id}/{name}/"
        
        if not os.path.isdir(f"{IMGS_PATH}/{id}"):
            os.makedirs(f"{IMGS_PATH}/{id}")
            
        if not os.path.isdir(path):
            os.makedirs(path)
            
        if not os.path.isdir(path+'/changes'):
            os.makedirs(path+'/changes')

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            if type == 'img':
                print('make screen')
                page.screenshot(path=f"{path}/img.png")

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
                        elem_bounds = elem.bounding_box()
                        
                        if not elem_bounds:
                            continue
                        try:
                            if (elem_bounds['width'] * elem_bounds['height'] < page_bounds['height']*page_bounds['width']*0.6) and (not (elem_bounds['height'] / elem_bounds['width'] > 5 or elem_bounds['width'] / elem_bounds['height'] > 5)) and (elem_bounds['width'] * elem_bounds['height'] > 50*50) and elem.is_visible() and str(zlib.compress(elem.inner_text().encode())) not in old_html:
                                if elem.inner_html() not in used_list:
                                    elem.screenshot(path=f"{path}/changes/{changes_count}.png")
                                    changes_count += 1
                                    # save only 5 first elements
                                    if changes_count > 10:
                                        break
                                    used_list += ('\n'+elem.inner_html())
                                    print('new element')
                                else: 
                                    print('element already used')
                        except:
                            pass
                    else:
                        pass
                else:
                    pass
                        
                    browser.close()
                print('html-check done:', time.time() - start_time)

                return changes_count
     
    def get_img(self, name='', id=''):
        img = io.imread(f"{IMGS_PATH}/{id}/{name}/img.png")
        return img
    
    def get_path(self, name='', id=''):
        return f"{IMGS_PATH}/{id}/{name}"
    
    def find_difference(self, old_img, new_img, name ,id):

        white_image = old_img.copy()
        white_image[:,:,:] = 1
        new_img = np.where(new_img != old_img, new_img, white_image)

        io.imsave(f"{IMGS_PATH}/{id}/{name}/difference.png", util.img_as_ubyte(new_img))
    
    def update(self, name='', url='', id='', type='img'):
        if type == 'img':
            old_img = []

            try:
                old_img = self.get_img(name, id)
            except:
                self.get_site_data(name, url, id, type)
                return {"name":name, "status":"new", "path":self.get_path(name, id)}

            self.get_site_data(name, url, id, type)
            new_img = self.get_img(name,id)

            is_difference = not np.array_equal(old_img,new_img)
            if is_difference:
                self.find_difference(old_img, new_img, name, id)
            
            return {"is_change": is_difference, "name":name, "path":self.get_path(name,id), "status":"update"}

        if type == 'html':
            changes_count = self.get_site_data(name, url, id, type)
            return {"is_change": changes_count > 0, "name":name, "path":self.get_path(name,id), "status":"update", "changes_count":changes_count}

pager = Pager()
