import os
import zipfile
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import sleep, time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

BEATSAGE = 'https://beatsage.com/#'
browser = None #Just make our browser global so I can attempt to access it anywhere
customLevelPath = None

class WorkerThread(Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		main()

def setOptions():
	difficulties = []
	gamemodes = []
	events = []

	if isNormal.get(): difficulties.append("Normal")
	if isHard.get(): difficulties.append("Hard")
	if isExpert.get(): difficulties.append("Expert")
	if isExpertPlus.get(): difficulties.append("ExpertPlus")

	if isStandard.get(): gamemodes.append("Standard")
	if isNinety.get(): gamemodes.append("90Degree")
	if isNoarrows.get(): gamemodes.append("NoArrows")
	if isOnesaber.get(): gamemodes.append("OneSaber")

	if isBombs.get(): events.append("Bombs")
	if isDotblocks.get(): events.append("DotBlocks")
	if isObstacles.get(): events.append("Obstacles")

	startToSend = 0 if start.get() == "" else int(start.get()) 
	endToSend = -1 if end.get() == "" else int(end.get())

	options = [difficulties, gamemodes, events, envChoice.get(), modelChoice.get(), startToSend, endToSend]
	return options

def setLinks(playlist, check=True):
	#titles = {}
	links = []
	status.set("Getting your songs from your playlist...")
	opts = Options()
	opts.headless = True
	browser = Firefox(options=opts)
	browser.get(playlist)
	div = browser.find_element_by_id("contents")
	linksAsATags = div.find_elements(By.TAG_NAME, "a")
	for link in linksAsATags:
		if link.get_attribute("class") == "yt-simple-endpoint style-scope ytd-playlist-video-renderer":
			status.set(link.text)
			links.append(link.get_attribute("href"))
			#titles[link.get_attribute("title")] = link.get_attribute("href") #Key = title Value = its link
	'''
	if check:
		status.set("Checking if any songs in the playlist have already been beatsage'd (to skip them)")
		for folder in (item for item in os.listdir(os.getcwd()) if os.path.isdir(os.getcwd() + "\\" + item)):
			for title in titles.keys():
				if title in folder:
					status.set(title + " was already found in folder: " + folder + ", skipping")
					titles[title] = ""
	links = [i for i in titles.values() if i] #If string is anything but empty string it should be True. "" evals to False
	'''
	browser.close()
	status.set("Done.")
	sleep(1)
	return links

def main():
	links = setLinks(linkChoice.get())
	options = setOptions()

	global customLevelPath #I doubt this is needed but I cant figure out so far why the fuck oslistdir isn't detecting zips in main, but can in unzipandclean
	difficulties = options[0]
	gamemodes = options[1]
	events = options[2]
	environment = options[3]
	model = options[4]
	start: int = options[5]
	end: int = options[6]
	counter = 1
	total = end if end != -1 else len(links)
	status.set("Warning: Do not add or remove files from the folder this app is running from or it could cause the script to fail to download one or more songs. \n")
	sleep(3)
	opts = Options()
	opts.headless = True
	opts.set_preference("browser.download.folderList", 2) #Download to our directory, not default Downloads
	opts.set_preference("browser.download.manager.showWhenStarting", False) #Hide download progress
	opts.set_preference("browser.download.manager.focusWhenStarting", False)
	opts.set_preference("browser.helperApps.alwaysAsk.force", False)
	customPathBackSlashes = customLevelPath.replace("/", "\\")
	opts.set_preference("browser.download.dir", customPathBackSlashes) #Set directory to download to to wherever this script is
	opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
	opts.set_preference("browser.helperApps.neverAsk.openFile", "application/octet-stream")
	for link in links:
		if start > counter:
			counter += 1
			continue
		if end != -1 and counter > end:
			break
		try:
			status.set("Starting to work on song " + str(counter) + " of " + str(total))
			browser = Firefox(options=opts)
			browser.get(BEATSAGE)
			actions = ActionChains(browser)

			fileCount = len(os.listdir(customLevelPath))
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

			status.set("Setting difficulties...")
			for i in diffinputs:
				if i.get_attribute("value") not in difficulties and i.is_selected():
					#scrollShim(browser, i, -550)
					#actions.move_to_element(i).click().perform()
					span = i.find_element(By.XPATH, '..')
					span.click()
				if i.get_attribute("value") in difficulties and not i.is_selected():
					#status.set("    " + str(i.get_attribute("value")) + "was " + str(i.is_selected()))
					#scrollShim(browser, i, -550)
					#actions.move_to_element(i).click().perform()
					span = i.find_element(By.XPATH, '..')
					span.click()
					#status.set("    " + str(i.get_attribute("value")) + "is now " + str(i.is_selected()))

			status.set("Setting game modes...")
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

			status.set("Setting events...")
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

			status.set("Setting the environment and model version...")
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
					browser.find_element_by_class_name('nuxt-progress')
				except Exception as e:
					status.set("BeatSage finished loading this song on its webpage, now processing it...")
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
			sleep(1)
			try:
				browser.find_element_by_class_name("uploading")
			except Exception as e:
				status.set("Beat Sage couldn't process this song for some reason. It said to try again later. Skipping this song and moving onto the next...")
				counter += 1
				browser.close()
				continue
			status.set("BeatSage is processing this song right now, this is the longest step and could take awhile, usually one to three minutes...")
			startTime = time()
			while(len(os.listdir(customLevelPath)) == fileCount): sleep(1)
			finishTime = time() - startTime
			status.set("Processing and download for this song complete. Time taken: " + str(finishTime)[0:5] + " seconds\n")
			counter += 1
			browser.close()
		except KeyboardInterrupt as e: #Catch SIGINT and attempt to close firefox if it was still open
			try:
				browser.close()
			except Exception as e:
				pass
		except Exception as e:
			print(e)
			status.set("Some unknown error has occurred on this song. Skipping it and trying the next song")
			counter += 1
			browser.close()
			continue
	status.set("Done downloading every beatmap. Unzipping contents to same folder...")
	unzipandclean()
	status.set("You're ready to play. Enjoy :)")

def scrollShim(passed_in_driver, object, offset): #Because FireFox is dumb apparently
	x = object.location['x']
	y = object.location['y']
	scroll_by_coord = 'window.scrollTo(%s,%s);' % (
		x,
		y+offset
	)
	passed_in_driver.execute_script(scroll_by_coord)

def unzipandclean(): #Unzips any zip files in cwd and deletes the zip files.
	if customLevelPath is None: return #Guard against path not supplied

	for file in os.listdir(customLevelPath):
		if file.endswith(".zip"):
			status.set("Unzipping " + str(file) + "...    ") #end= prevents a newline
			with zipfile.ZipFile(customLevelPath+"/"+file, 'r') as zip_ref:
				zip_ref.extractall(customLevelPath + "/" + file[0:-4])
			status.set("Done. Deleting zip file...")
			os.remove(customLevelPath+"/"+file)
	status.set("Done unzipping all files!")

def getCustomLevelsPath():
	global customLevelPath
	customLevelPath = filedialog.askdirectory()

def createWorker():
	if customLevelPath is None: return 
	worker = WorkerThread()
	worker.start()
	monitor(worker)

def monitor(thread):
	if thread.is_alive():
		root.after(100, lambda: monitor(thread))

if __name__ == "__main__":

	#Build the overall GUI
	root = Tk()
	root.title("Autosage")
	root.iconbitmap(r'C:\\Users\\Alan\\Desktop\\autosage\\autosage.ico')
	mainframe = ttk.Frame(root, padding="12 12 12 12")
	mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)

	#Get CustomLevels directory
	customLevelsLabel = ttk.Label(mainframe, text="First, show me where your CustomLevels folder is, something like: \"...\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels\":")
	customLevelsLabel.grid(column=0, row=0, columnspan=2, sticky=(W))
	customLevelButton = ttk.Button(mainframe, text="Locate Folder", command=getCustomLevelsPath).grid(column=2, row=0, sticky=(W))


	#Get playlist link
	linkLabel = ttk.Label(mainframe, text="Paste a link to a public or unlisted YouTube playlist (not to a song in the playlist but the playlist link itself):").grid(column=0, row=1, sticky=(W))
	linkChoice = StringVar(value="")
	linkEntry = ttk.Entry(mainframe, textvariable=linkChoice).grid(column=1, row=1, columnspan=4, sticky=(W, E))

	#Difficulties
	difficultiesLabel = ttk.Label(mainframe, text="Difficulties:").grid(column=0, row=2, sticky=(W))
	isNormal = BooleanVar(value=True)
	isHard = BooleanVar(value=True)
	isExpert = BooleanVar(value=True)
	isExpertPlus = BooleanVar(value=True)
	normal = ttk.Checkbutton(mainframe, variable=isNormal, text="Normal").grid(column=1, row=2, sticky=(W))
	hard = ttk.Checkbutton(mainframe, variable=isHard, text="Hard").grid(column=2, row=2, sticky=(W))
	expert = ttk.Checkbutton(mainframe, variable=isExpert, text="Expert").grid(column=3, row=2, sticky=(W))
	expertplus = ttk.Checkbutton(mainframe, variable=isExpertPlus, text="Expert Plus").grid(column=4, row=2, sticky=(W))

	#Game modes
	gamemodesLabel = ttk.Label(mainframe, text="Game modes:").grid(column=0, row=3, sticky=(W))
	isStandard = BooleanVar(value=True)
	isNinety = BooleanVar(value=True)
	isNoarrows = BooleanVar(value=False)
	isOnesaber = BooleanVar(value=False)
	standard = ttk.Checkbutton(mainframe, variable=isStandard, text="Standard").grid(column=1, row=3, sticky=(W))
	ninety = ttk.Checkbutton(mainframe, variable=isNinety, text="90 Degrees").grid(column=2, row=3, sticky=(W))
	noarrows = ttk.Checkbutton(mainframe, variable=isNoarrows, text="No Arrows").grid(column=3, row=3, sticky=(W))
	onesaber = ttk.Checkbutton(mainframe, variable=isOnesaber, text="One Saber").grid(column=4, row=3, sticky=(W))

	#Events
	eventsLabel = ttk.Label(mainframe, text="Events:").grid(column=0, row=4, sticky=(W))
	isBombs = BooleanVar(value=True)
	isDotblocks = BooleanVar(value=True)
	isObstacles = BooleanVar(value=True)
	bombs = ttk.Checkbutton(mainframe, variable=isBombs, text="Bombs").grid(column=1, row=4, sticky=(W))
	dotblocks = ttk.Checkbutton(mainframe, variable=isDotblocks, text="Dot Blocks").grid(column=2, row=4, sticky=(W))
	obstacles = ttk.Checkbutton(mainframe, variable=isObstacles, text="Obstacles").grid(column=3, row=4, sticky=(W))

	#Environments
	environmentLabel = ttk.Label(mainframe, text="Choose an environment to override with:").grid(column=0, row=5, sticky=(W))
	envs =	[
		"",
		"DefaultEnvironment",
		"Origins",
		"TriangleEnvironment",
		"NiceEnvironment",
		"BigMirrorEnvironment",
		"DragonsEnvironment",
		"KDAEnvironment",
		"MonstercatEnvironment",
		"CrabRaveEnvironment",
		"PanicEnvironment",
		"RocketEnvironment",
		"GreenDayEnvironment",
		"GreenDayGrenadeEnvironment",
		"TimbalandEnvironment",
		"FitBeatEnvironment",
		"LinkinParkEnvironment"]
	envChoice = StringVar()
	envChoice.set(envs[1])
	environment = ttk.OptionMenu(mainframe, envChoice, *envs).grid(column=1, row=5, sticky=(W)) #.get() on associated control variable will get the selected choice as a string

	modelLabel = ttk.Label(mainframe, text="Choose a model to create beatmaps with (v2f recommended):").grid(column=0, row=6, sticky=(W))
	models = ["", "v1", "v2", "v2-flow"]
	modelChoice = StringVar()
	modelChoice.set(models[3])
	model = ttk.OptionMenu(mainframe, modelChoice, *models).grid(column=1, row=6, sticky=(W))

	startLabel = ttk.Label(mainframe, text="Choose the song number in playlist to start with (1, 2, 99, etc):").grid(column=0, row=7, sticky=(W))
	start = StringVar(value="1")
	startCombo = ttk.Entry(mainframe, textvariable=start).grid(column=1, row=7, sticky=(W))
	endLabel = ttk.Label(mainframe, text="Choose the song number in playlist to stop at (1, 2, 99, etc):").grid(column=0, row=8, sticky=(W))
	end = StringVar(value="")
	endCombo = ttk.Entry(mainframe, textvariable=end).grid(column=1, row=8, sticky=(W))

	startButton = ttk.Button(mainframe, text="Begin!", command=createWorker).grid(column=0, row=9, sticky=(W, E))
	unzipButton = ttk.Button(mainframe, text="Unzip & delete everything in CustomLevels", command=unzipandclean).grid(column=1, row=9, columnspan=2, sticky=(W, E))

	status = StringVar()
	statusLabel = ttk.Label(mainframe, textvariable=status).grid(column=0, row=10, columnspan=5, sticky=(W, E))

	#Pad everything in GUI nicely
	for child in mainframe.winfo_children(): 
		child.grid_configure(padx=5, pady=5)

	root.bind("<Return>", startButton) #Hitting enter will press start

	#Start event loop so app displays!
	root.mainloop()

	#Note: If you get Message: process unexpected closed with status 0 as a selenium exception, that is because Firefox needs to update. Try again after its up to date.
	#Note: If you get Message: Unable to locate element: [] make sure you are in the overall page for the playlist, not a specific song in that playlist