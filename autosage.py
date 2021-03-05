import sys
import os
import zipfile
from time import sleep, time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

BEATSAGE = 'https://beatsage.com/#'

def setOptions(args):
	difficulties = []
	gamemodes = []
	events = []
	if 'n' in args:
		difficulties.append("Normal")
	if 'h' in args:
		difficulties.append("Hard")
	if 'e' in args:
		difficulties.append("Expert")
	if 'ep' in args:
		difficulties.append("ExpertPlus")
	if 's' in args:
		gamemodes.append("Standard")
	if '90' in args:
		gamemodes.append("90Degree")
	if 'no' in args:
		gamemodes.append("NoArrows")
	if '1s' in args:
		gamemodes.append("OneSaber")
	if 'b' in args:
		events.append("Bombs")
	if 'db' in args:
		events.append("DotBlocks")
	if 'o' in args:
		events.append("Obstacles")

	if 'default' in args:
		environment = "DefaultEnvironment"
	elif 'origins' in args:
		environment = "Origins"
	elif 'triangle' in args:
		environment = "TriangleEnvironment"
	elif 'nice' in args:
		environment = "NiceEnvironment"
	elif 'big mirror' in args:
		environment = "BigMirrorEnvironment"
	elif 'imagine dragons' in args:
		environment = "DragonsEnvironment"
	elif 'kda' in args:
		environment = "KDAEnvironment"
	elif 'monstercat' in args:
		environment = "MonstercatEnvironment"
	elif 'crab rave' in args:
		environment = "CrabRaveEnvironment"
	elif 'panic at the disco' in args:
		environment = "PanicEnvironment"
	elif 'rocket league' in args:
		environment = "RocketEnvironment"
	elif 'green day' in args:
		environment = "GreenDayEnvironment"
	elif 'green day grenade' in args:
		environment = "GreenDayGrenadeEnvironment"
	elif 'timbaland' in args:
		environment = "TimbalandEnvironment"
	elif 'fitbeat' in args:
		environment = "FitBeatEnvironment"
	elif 'linkin park' in args:
		environment = "LinkinParkEnvironment"

	if 'v2' in args:
		model = "v2"
	elif 'v2f' in args:
		model = "v2-flow"
	elif 'v1' in args:
		model = "v1"

	#Temporary hard codes for ease of testing
	difficulties = ["Hard", "Expert", "ExpertPlus"]
	gamemodes = ["Standard", "90Degree"]
	events = ["Bombs", "DotBlocks", "Obstacles"]
	environment = "DefaultEnvironment"
	model = "v2-flow"

	options = [difficulties, gamemodes, events, environment, model]
	return options

def setLinks(playlist):
	#Code to seperate playlist into individual youtube links
	links = ["https://www.youtube.com/watch?v=tLyRpGKWXRs&list=PLadVUcdkRukLWYxF_mg6XEuxSmTmLuv2C&index=14", "https://www.youtube.com/watch?v=kMmtcZgBYX4"]
	return links

def main(links, options):
	difficulties = options[0]
	gamemodes = options[1]
	events = options[2]
	environment = options[3]
	model = options[4]
	opts = Options()
	opts.headless = True
	opts.set_preference("browser.download.folderList", 2) #Download to whatever is stated two lines below
	opts.set_preference("browser.download.manager.showWhenStarting", False) #Hide download progress
	opts.set_preference("browser.download.dir", os.getcwd()) #Set directory to download to to wherever this script is
	opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
	for link in links:
		print("Starting to work on: " + str(link))
		browser = Firefox(options=opts)
		browser.get(BEATSAGE)
		actions = ActionChains(browser)

		fileCount = len([name for name in os.listdir('.') if os.path.isfile(name)])
		#Find input tag with value Hard, Expert, ExpertPlus, 90Degree, Standard, Bombs, DotBlocks, Obstacles
		inputs = browser.find_elements(By.TAG_NAME, 'input') #All input tags from page
		textinputand = inputs[0:2] #the url text field for song, and something else
		diffinputs = inputs[2:6] #The inputs for difficulties
		gamemodeinputs = inputs[6:10] #inputs for game modes, patreon disabled ones removed
		eventinputs = inputs[11:14] #inputs for bombs and other song events
		advsettings = browser.find_elements(By.TAG_NAME, 'select')

		inputs[0].send_keys(link) #Add a youtube link to the text field
		buttons = browser.find_elements(By.TAG_NAME, 'button') #buttons[0] contains the magnifying glass search button we want
		scrollShim(browser, buttons[0], -550)
		actions.move_to_element(buttons[0]).click().perform() #Click on the magnifying glass search button

		print("Setting difficulties...")
		for i in diffinputs:
			if i.get_attribute("value") not in difficulties and i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
			if i.get_attribute("value") in difficulties and not i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()

		print("Setting game modes...")
		for i in gamemodeinputs:
			if i.get_attribute("value") not in gamemodes and i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
			if i.get_attribute("value") in gamemodes and not i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()

		print("Setting events...")
		for i in eventinputs:
			if i.get_attribute("value") not in events and i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()
			if i.get_attribute("value") in events and not i.is_selected():
				scrollShim(browser, i, -550)
				actions.move_to_element(i).click().perform()

		print("Setting the environment and model version...")
		div = browser.find_element_by_id("contentIdForA11y1")
		browser.execute_script("arguments[0].setAttribute(\"style\", \"\")", div)
		env = Select(advsettings[0])
		modelversion = Select(advsettings[1])
		env.select_by_value(environment)
		modelversion.select_by_value(model)

		#Submit and have it start working on your song
		g = browser.find_element_by_id('bottom') #top rect says cant click
		rect = g.find_element_by_class_name('red')
		
		#Temporary submission fix:
		sleep(2) #Waste two seconds because I'm too fast for beat sage >:)
		try:
			rect.click()
			rect.click()
			rect.click()
			rect.click()
		except Exception as e:
			print("Caught exception that isn't my fault because firefox webdriver is stupid")
		
		#Below commented out because it would work normally but firefox is again fucking stupid
		"""scrollShim(browser, rect, -900)
		actions.move_to_element(rect)
		actions.move_by_offset(-150, 0)
		actions.click_and_hold()
		actions.move_by_offset(150, 0)
		actions.release()
		actions.perform()"""

		#Maybe place a loop here that checks for that div popup changing so you can tell if the download started?
		print("BeatSage is processing this song right now, this is the longest step and could take awhile, usually one to three minutes...")
		start = time()
		while(len([name for name in os.listdir('.') if os.path.isfile(name)]) == fileCount): sleep(1)
		total = time() - start
		print("Processing and download for this song complete. Time taken: " + str(total)[0:5] + " seconds\n")
		browser.close()
	print("Done downloading every beatmap. Unzipping contents to same folder...")
	for file in os.listdir(os.getcwd()):
		if file.endswith(".zip"):
			print("Unzipping " + str(file))
			with zipfile.ZipFile(file, 'r') as zip_ref:
				zip_ref.extractall(os.getcwd() + "/" + file[0:-4])
			print("Done. \n Deleting zip file")
			os.remove(file)
	print("Done.")

def scrollShim(passed_in_driver, object, offset): #Because FireFox is dumb apparently
	x = object.location['x']
	y = object.location['y']
	scroll_by_coord = 'window.scrollTo(%s,%s);' % (
		x,
		y+offset
	)
	passed_in_driver.execute_script(scroll_by_coord)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print(" HOW TO USE: ")
		print("""
 Copy paste your playlist link, followed by every BeatSage option you want ticked ON, with a space between each! \n
 Example with all options on, environment default, model set to V2-Flow:
 python autosage.py https://www.youtube.com/watch?v=q6EoRBvdVPQ&list=PLZ4DbyIWUwCq4V8bIEa8jm2ozHZVuREJP n h e ep s 90 no 1s b db o default v2f

	List of options:

	n - Normal
	h - Hard
	e - Expert
	ep - Expert Plus
	s - Standard
	90 - 90 Degrees
	no - No Arrows
	1s - One Saber
	b - Bombs
	db - Dot Blocks
	o - Obstacles

	Environments:

	default
	origins
	triangle
	nice
	big mirror
	imagine dragons
	kda
	monstercat
	crab rave
	panic at the disco
	rocket league
	green day
	green day grenade
	timbaland
	fitbeat
	linkin park

	Models:

	v2
	v2f
	v1
			""")
		quit()
	links = setLinks(sys.argv[1])
	opts = setOptions(sys.argv[2:])
	main(links, opts)