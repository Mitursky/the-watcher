from selenium import webdriver
from skimage.io import imread
import numpy as np

old_photo = imread('./screenshot.png')

# driver = webdriver.Chrome(executable_path="./chromedriver")
# driver.get('https://vk.com')

# driver.get_screenshot_as_file("screenshot.png")

new_photo = imread('./screenshot2.png')
print(np.array_equal(old_photo, new_photo))
# driver.quit()

print("end...")