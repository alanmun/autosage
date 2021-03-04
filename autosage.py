from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)
BEATSAGE = 'https://beatsage.com/#'

def askForPlaylist():
	print("Paste a link to a youtube playlist you want to beat sage en masse: ")
	playlist = input()

	return 

def main(links=None):
	browser.get(BEATSAGE)
	difficulties = ["Hard", "Expert", "ExpertPlus"]
	gamemodes = ["Standard", "90Degree"]
	events = ["Bombs", "DotBlocks", "Obstacles"]

	#Find input tag with value Hard, Expert, ExpertPlus, 90Degree, Standard, Bombs, DotBlocks, Obstacles
	inputs = browser.find_elements(By.TAG_NAME, 'input') #All input tags from page
	textinputand = inputs[0:2] #the url text field for song, and something else
	diffinputs = inputs[2:6] #The inputs for difficulties
	gamemodeinputs = inputs[6:10] #inputs for game modes, patreon disabled ones removed
	eventinputs = inputs[11:14] #inputs for bombs and other song events
	advsettings = browser.find_elements(By.TAG_NAME, 'select')

	inputs[0].send_keys("https://www.youtube.com/watch?v=tLyRpGKWXRs&list=PLadVUcdkRukLWYxF_mg6XEuxSmTmLuv2C&index=14")
	#print("? " + inputs[0].get_attribute("value")) #Seems like above line works. input's value="" is set to ^

	#Doing sleep(7) and checking for inputs again still returns 15 total. So what about those two guys song artist and song title?
	print(dir(inputs[0]))
	print()
	print(dir(browser))
	print()
	print("Length of inputs: " + str(len(inputs)))
	print("Length of textinputand: " + str(len(textinputand)))
	print("Length of diffinputs: " + str(len(diffinputs)))
	print("Length of gamemodeinputs: " + str(len(gamemodeinputs)))
	print("Length of eventinputs: " + str(len(eventinputs)))
	print("Length of advsettings: " + str(len(advsettings)))
	
	#Setting difficulties
	for i in range(0, len(diffinputs)):
		print(str(i))
		if diffinputs[i].get_attribute("disabled") == "disabled":
			continue
		if diffinputs[i].get_attribute("value") not in difficulties and diffinputs[i].get_attribute("true-value") is True:
			diffinputs[i].click()
			print("I clicked on input: " + diffinputs[i].get_attribute("value") + " and now it is: " + diffinputs[i].get_attribute("true-value"))
		if diffinputs[i].get_attribute("value") in difficulties and diffinputs[i].get_attribute("true-value") is False:
			diffinputs[i].click()
			print("I clicked on input: " + diffinputs[i].get_attribute("value") + " and now it is: " + diffinputs[i].get_attribute("true-value"))
		print(diffinputs[i].get_attribute("value"))
		print(diffinputs[i].get_attribute("true-value"))
		print()

	#Setting model version
	print(dir(advsettings[0]))
	#There are three option tags. Set it to the one with value="v2-flow"
	#I think the site lets you skip having to drag click if you click four times on the note block
	#It's a rect tag, with class = red
	#For some reason another rect tag inside of it with no class name
	g = browser.find_element_by_id('bottom') #top rect says cant click
	rect = g.find_element_by_class_name('red')
	rect.click()

	print("Sleeping for 180")
	sleep(180)

	browser.close()

if __name__ == "__main__":
   #links = askForPlaylist()
   links = ""
   main(links)