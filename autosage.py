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
	environment = "DefaultEnvironment"
	model = "v2-flow"
	if 'n' in args:
		if "Normal" not in difficulties: difficulties.append("Normal")
	if 'h' in args:
		if "Hard" not in difficulties: difficulties.append("Hard")
	if 'e' in args:
		if "Expert" not in difficulties: difficulties.append("Expert")
	if 'ep' in args:
		if "ExpertPlus" not in difficulties: difficulties.append("ExpertPlus")
	if "n" not in args and 'h' not in args and 'e' not in args and 'ep' not in args: #If none are included, default to all
		difficulties = ["Normal", "Hard", "Expert", "ExpertPlus"]

	if 's' in args:
		gamemodes.append("Standard")
	if '90' in args:
		gamemodes.append("90Degree")
	if 'no' in args:
		gamemodes.append("NoArrows")
	if '1s' in args:
		gamemodes.append("OneSaber")
	if 's' not in args and '90' not in args and 'no' not in args and '1s' not in args: #If no game modes given, default to Standard only
		gamemodes = ["Standard"]

	if 'b' in args:
		events.append("Bombs")
	if 'db' in args:
		events.append("DotBlocks")
	if 'o' in args:
		events.append("Obstacles")
	if 'b' not in args and 'db' not in args and 'o' not in args: #If no event options given, default to all
		events = ["Bombs", "DotBlocks", "Obstacles"]

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

	options = [difficulties, gamemodes, events, environment, model]
	return options

def setLinks(playlist):
	links = []
	print("Getting your songs from your playlist...")
	opts = Options()
	opts.headless = True
	browser = Firefox(options=opts)
	browser.get(playlist)
	div = browser.find_element_by_id("contents")
	linksAsATags = div.find_elements(By.TAG_NAME, "a")
	for link in linksAsATags:
		if link.get_attribute("class") == "yt-simple-endpoint style-scope ytd-playlist-video-renderer":
			print(link.text)
			links.append(link.get_attribute("href"))
	browser.close()
	print("Done.")
	sleep(1)
	return links

def main(links, options):
	difficulties = options[0]
	gamemodes = options[1]
	events = options[2]
	environment = options[3]
	model = options[4]
	counter = 1
	total = len(links)
	print("Your selected difficulties: " + str(difficulties))
	print("Your selected gamemodes: " + str(gamemodes))
	print("Your selected events: " + str(events))
	print("Your environment: " + environment)
	print("Your model: " + model)
	print("Do CTRL+C (CMD+C on Mac) if any of these seem wrong to fix them before continuing.\n")
	sleep(1)
	opts = Options()
	opts.headless = True
	opts.set_preference("browser.download.folderList", 2) #Download to whatever is stated two lines below
	opts.set_preference("browser.download.manager.showWhenStarting", False) #Hide download progress
	opts.set_preference("browser.download.manager.focusWhenStarting", False)
	opts.set_preference("browser.helperApps.alwaysAsk.force", False)
	opts.set_preference("browser.download.dir", os.getcwd()) #Set directory to download to to wherever this script is
	opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
	opts.set_preference("browser.helperApps.neverAsk.openFile", "application/octet-stream")
	for link in links:
		print("Starting to work on song " + str(counter) + " of " + str(total))
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
		buttons[0].click()

		print("Setting difficulties...")
		for i in diffinputs:
			print(i.get_attribute("value"))
			if i.get_attribute("value") not in difficulties and i.is_selected():
				#scrollShim(browser, i, -550)
				#actions.move_to_element(i).click().perform()
				span = i.find_element(By.XPATH, '..')
				span.click()
			if i.get_attribute("value") in difficulties and not i.is_selected():
				#print("    " + str(i.get_attribute("value")) + "was " + str(i.is_selected()))
				#scrollShim(browser, i, -550)
				#actions.move_to_element(i).click().perform()
				span = i.find_element(By.XPATH, '..')
				span.click()
				#print("    " + str(i.get_attribute("value")) + "is now " + str(i.is_selected()))

		print("Setting game modes...")
		for i in gamemodeinputs:
			if i.get_attribute("value") not in gamemodes and i.is_selected():
				#scrollShim(browser, i, -550)
				#actions.move_to_element(i).click().perform()
				span = i.find_element(By.XPATH, '..')
				span.click()
			if i.get_attribute("value") in gamemodes and not i.is_selected():
				#scrollShim(browser, i, -550)
				#actions.move_to_element(i).click().perform()
				span = i.find_element(By.XPATH, '..')
				span.click()

		print("Setting events...")
		for i in eventinputs:
			if i.get_attribute("value") not in events and i.is_selected():
				#scrollShim(browser, i, -550)
				#actions.move_to_element(i).click().perform()
				span = i.find_element(By.XPATH, '..')
				span.click()
			if i.get_attribute("value") in events and not i.is_selected():
				#scrollShim(browser, i, -550)
				#actions.move_to_element(i).click().perform()
				span = i.find_element(By.XPATH, '..')
				span.click()

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
		
		while True:
			try:
				divcheck = browser.find_element_by_class_name('nuxt-progress')
			except Exception as e:
				print("BeatSage finished loading this song on its webpage, now processing it...")
				break

		#Temporary submission fix:
		try:
			rect.click()
			rect.click()
			rect.click()
			rect.click()
		except Exception as e:
			pass
		
		#Below commented out because it would work normally but firefox is again fucking stupid
		"""scrollShim(browser, rect, -900)
		actions.move_to_element(rect)
		actions.move_by_offset(-150, 0)
		actions.click_and_hold()
		actions.move_by_offset(150, 0)
		actions.release()
		actions.perform()"""

		print("BeatSage is processing this song right now, this is the longest step and could take awhile, usually one to three minutes...")
		start = time()
		while(len([name for name in os.listdir('.') if os.path.isfile(name)]) == fileCount): sleep(1)
		total = time() - start
		print("Processing and download for this song complete. Time taken: " + str(total)[0:5] + " seconds\n")
		counter += 1
		browser.close()
	print("Done downloading every beatmap. Unzipping contents to same folder...")
	unzipandclean()
	print("All finished. Enjoy :)")

def scrollShim(passed_in_driver, object, offset): #Because FireFox is dumb apparently
	x = object.location['x']
	y = object.location['y']
	scroll_by_coord = 'window.scrollTo(%s,%s);' % (
		x,
		y+offset
	)
	passed_in_driver.execute_script(scroll_by_coord)

def unzipandclean(): #Unzips any zip files in cwd and deletes the zip files.
	for file in os.listdir(os.getcwd()):
		if file.endswith(".zip"):
			print("Unzipping " + str(file) + "...    ", end="") #end= prevents a newline
			with zipfile.ZipFile(file, 'r') as zip_ref:
				zip_ref.extractall(os.getcwd() + "/" + file[0:-4])
			print("Done. \n Deleting zip file")
			os.remove(file)
	print("Done unzipping all files!")

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

	Misc options:

	unzip - If there is an issue during the runtime of the script, or you just wanted to, this will mass unzip all zipped folders and delete the zipped versions, use this option

	Environments (select one):

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

	Models (select one):

	v2
	v2f
	v1
	""")
		quit()
	if "unzip" in sys.argv:
		unzipandclean()
		exit()
	links = setLinks(sys.argv[1])
	opts = setOptions(sys.argv[2:])
	main(links, opts)