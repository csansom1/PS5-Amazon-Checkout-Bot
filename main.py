from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from random import randint, randrange
import time
import  info
import random

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
AMAZON_URL = "https://www.amazon.ca/Playstation-3006648-PlayStation-Disc-Edition/dp/B09DPJ2TGW/ref=sr_1_3?brr=1&qid=1641519145&rd=1&s=videogames&sr=1-3"
AMAZON_TEST_URL = "https://www.amazon.ca/Toothpicks-Reusable-Container-Cocktail-Appetizers/dp/B08Y5WPCKM/ref=sr_1_6?crid=1R9OCVAUGCC28&keywords=toothpick&qid=1641616645&sprefix=toothpick%2Caps%2C73&sr=8-6" ## "https://www.amazon.ca/Namco-Bandai-13011-Tales-Arise/dp/B093B218BN/ref=sr_1_1?crid=3L65Q9ACAZOID&keywords=tales+of+arise+ps5&qid=1641519651&sprefix=tales%2Caps%2C96&sr=8-1"
WAIT_TIME = 7
PRICE_LIMIT = 700.00


class PS5AmazonBot:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Chrome(DRIVER_PATH)

	## Sign into site with the product
	def signIn(self):
		""" Sign into site with the product. """
		driver = self.driver  ## Navigate to URL

		## Enter Username
		username_elem = driver.find_element_by_xpath("//input[@name='email']")
		username_elem.clear()
		username_elem.send_keys(self.username)

		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		username_elem.send_keys(Keys.RETURN)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## Enter Password
		password_elem = driver.find_element_by_xpath("//input[@name='password']")
		password_elem.clear()
		password_elem.send_keys(self.password)

		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		password_elem.send_keys(Keys.RETURN)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

	## Find product under X amount
	def findProduct(self):
		""" Finds the product with global link. """
		driver = self.driver
		#driver.get(AMAZON_TEST_URL)
		driver.get(AMAZON_URL)
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## If the product is not available, wait until it is available
		isAvailable = self.isProductAvailable()

		while isAvailable == 'Currently unavailable.' or isAvailable > PRICE_LIMIT:
			#driver.get(AMAZON_TEST_URL)
			driver.get(AMAZON_URL)
			time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
			isAvailable = self.isProductAvailable()

		## Buy Now
		buy_now = driver.find_element_by_name('submit.buy-now')
		buy_now.click()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		self.signIn()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))

		## Place Order
		place_order = driver.find_element_by_name('placeYourOrder1')
		#place_order_text = place_order.get_attribute('value')
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		#print(f'***** PLACE ORDER: {place_order_text}')
		place_order.click()
		time.sleep(randint(WAIT_TIME >> 1, WAIT_TIME))
		print(f'***** ORDER PLACED')

	def isProductAvailable(self):
		""" Checks if product is available. """
		driver = self.driver
		try:
			price = driver.find_element_by_class_name('_p13n-desktop-sims-fbt_price_p13n-sc-price__bCZQt').text
			print(f'***** PRICE: {price}')
			return float(price[1:])
		except NoSuchElementException:
			print(f'***** CURRENTLY UNAVAILABLE.')
			return 'Currently unavailable.'

	def closeBrowser(self):
		""" Closes browser """
		print(f'***** CLOSE BROWSER')
		self.driver.close()


if __name__ == '__main__':
	shopBot = PS5AmazonBot(username=info.username, password=info.password)
	shopBot.findProduct()
	shopBot.closeBrowser()
