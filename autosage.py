from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

opts = Options()
opts.headless = True
browser = Firefox(options=opts)
BEATSAGE = 'https://beatsage.com/#'

def scrollShim(passed_in_driver, object, offset): #Because FireFox is dumb apparently
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y+offset
    )
    passed_in_driver.execute_script(scroll_by_coord)

def askForOptions():
	difficulties = ["Hard", "Expert", "ExpertPlus"]
	gamemodes = ["Standard", "90Degree"]
	events = ["Bombs", "DotBlocks", "Obstacles"]
	options = [difficulties, gamemodes, events]
	return options

def askForPlaylist():
	print("Paste a link to a youtube playlist you want to beat sage en masse: ")
	playlist = ["https://www.youtube.com/watch?v=tLyRpGKWXRs&list=PLadVUcdkRukLWYxF_mg6XEuxSmTmLuv2C&index=14"]
	return playlist

def main(links, options):
	difficulties = ["Hard", "Expert", "ExpertPlus"]
	gamemodes = ["Standard", "90Degree"]
	events = ["Bombs", "DotBlocks", "Obstacles"]
	for link in links:
		browser.get(BEATSAGE)
		actions = ActionChains(browser)
		#Find input tag with value Hard, Expert, ExpertPlus, 90Degree, Standard, Bombs, DotBlocks, Obstacles
		inputs = browser.find_elements(By.TAG_NAME, 'input') #All input tags from page
		textinputand = inputs[0:2] #the url text field for song, and something else
		diffinputs = inputs[2:6] #The inputs for difficulties
		gamemodeinputs = inputs[6:10] #inputs for game modes, patreon disabled ones removed
		eventinputs = inputs[11:14] #inputs for bombs and other song events
		advsettings = browser.find_elements(By.TAG_NAME, 'select')

		inputs[0].send_keys(link)
		buttons = browser.find_elements(By.TAG_NAME, 'button') #buttons[0] contains the magnifying glass search button we want
		scrollShim(browser, buttons[0], -550)
		actions.move_to_element(buttons[0]).click().perform() #Click on the magnifying glass search button
		
		#Setting difficulties
		for i in diffinputs:
			if i.get_attribute("value") not in difficulties and i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
				print("I clicked on input: " + i.get_attribute("value") + " and now it is: " + str(i.is_selected()))
			if i.get_attribute("value") in difficulties and not i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
				print("I clicked on input: " + i.get_attribute("value") + " and now it is: " + str(i.is_selected()))

		#Setting game modes
		for i in gamemodeinputs:
			if i.get_attribute("value") not in gamemodes and i.is_selected():
				print(i.get_attribute("value") + " was true, setting to false")
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
			if i.get_attribute("value") in gamemodes and not i.is_selected():
				print(i.get_attribute("value") + " was false, setting to true")
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()

		#Setting events
		for i in eventinputs:
			if i.get_attribute("value") not in events and i.is_selected():
				print(i.get_attribute("value") + " was true, setting to false")
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
			if i.get_attribute("value") in events and not i.is_selected():
				print(i.get_attribute("value") + " was false, setting to true")
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()

		#Setting environment and model version
		div = browser.find_element_by_id("contentIdForA11y1")
		browser.execute_script("arguments[0].setAttribute(\"style\", \"\")", div)
		env = Select(advsettings[0])
		model = Select(advsettings[1])
		env.select_by_value("DefaultEnvironment")
		model.select_by_value("v2-flow")
		sleep(1)

		#Submit and have it start working on your song
		g = browser.find_element_by_id('bottom') #top rect says cant click
		rect = g.find_element_by_class_name('red')
		
		#Temporary submission fix:
		try:
			rect.click()
			rect.click()
			rect.click()
			rect.click()
		except Exception as e:
			Print("Caught exception that isn't my fault because firefox webdriver is fucking stupid")
		
		#Below commented out because it would work normally but firefox is again fucking stupid
		"""scrollShim(browser, rect, -900)
		actions.move_to_element(rect)
		actions.move_by_offset(-150, 0)
		actions.click_and_hold()
		actions.move_by_offset(150, 0)
		actions.release()
		actions.perform()"""

		print("Sleeping for 180")
		sleep(180)

	browser.close()

if __name__ == "__main__":
   links = askForPlaylist()
   opts = askForOptions()
   main(links, opts)