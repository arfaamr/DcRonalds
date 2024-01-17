import requests 
import os
API_KEY = os.environ['API_KEY']

class Item:								

	total_cost = 0						
	prep_time = 0							#total time to prepare all ordered items
	delivery_time = 0
	tip_amt = 0
	ordered = []						
    
	def __init__(self,num,name,price,t):
		self.num = num                  
		self.name = name
		self.price = price
		self.time = t											

	def order(self):
		Item.total_cost += self.price
		Item.prep_time += self.time
		Item.ordered.append(self)

		print("Added 1 %s to your order. Your bill is now $%.2f. \n" % (self.name, Item.total_cost))
        

#menu items
item1 = Item(1,"Chicken DcNuggets",3,3)
item2 = Item(2,"Fillet-A-Fish",5,2)
item3 = Item(3,"DcFlurry",4,2)
item4 = Item(4,"Midi Fries",4,3)
item5 = Item(5,"Big Dac",7,5)

itemObjs = [item1,item2,item3,item4,item5]


print("Welcome to DcRonald's!")

def find_branch():													#user's address and local branch addresses are sent to MapQuest website to find which branch is nearest to the user 		

	print("Find the nearest DcRonald's branch to you.")

	home = input("Enter your address: (example - 1800 Liberty St, Windsor, ON) ")

	#Addresses of local "DcRonald's" (AKA McDonald's :( )
	loc1 = "883 Huron Church Line Rd, Windsor, ON"
	loc2 = "93 Wyandotte St E, Windsor, ON"
	loc3 = "3354 Dougall Ave, Windsor, ON"
	loc4 = "3195 Howard Ave, Windsor, ON"
	loc5 = "2780 Tecumseh Rd E, Windsor, ON"

	locations = [home, loc1, loc2,loc3,loc4,loc5] 	#home is first location, so distance and time will be calculated between home and all other locations

	#MapQuest Route Matrix calculates distance and driving times between locations
	url = "http://www.mapquestapi.com/directions/v2/routematrix?key=%s" % API_KEY
	params = {
		"locations": locations
	}
	response = requests.post(url, json=params)
	routeMatrix = response.json()

	distances = routeMatrix["distance"]
	times = routeMatrix["time"]
	del distances[0]																#remove home to home calculation
	del times[0]

	minDist = min(distances)
	pos = distances.index(minDist)
	nearest = locations[pos+1]
	Item.delivery_time = int(times[pos]//60) 						#time in minutes to get from user's home to the nearest branch

	print("Your nearest branch is at %s." % nearest)
	print("\n")


def menu():										#displays menu, takes user input, if item number is valid, calls Item.order() method to order item
	print("Select an item off our menu by entering the corresponding number, or 0 to complete your order.")
 
	print('''				DcRonald's 
——————————————————————————————————————————''')
	
	for i,item in enumerate(itemObjs):
		line = str(i+1) + ". " + item.name + " "*(35-len(item.name)-3) + "- $%.2f" % item.price
		print(line)

	print('''
0. Complete order
——————————————————————————————————————————''')

	while True:
		itemNum = int(input("Enter item number: "))
		if itemNum == 0 and len(Item.ordered) == 0:
			print("Please order something first.\n")
		elif itemNum == 0 and len(Item.ordered) > 0:
			print("")
			break
		elif itemNum >0 and itemNum <= itemObjs[-1].num:   
			itemObjs[itemNum-1].order()
		else:
			print("Please enter a valid order number.\n")


def add_tip():								#if user is dining in or getting takeout delivered, they can choose to tip
  Item.tip_amt = int(input("\nHow much would you like to tip? $"))
  print('')
  return


def misc_choices():						#miscellaneous choices - choose between dine-in and takeout, and pick-up and delivery
	print("Would you like to:")
	while True:
		choice1 = int(input("1. dine in, or 2. takeout? Enter the corresponding number: "))
		if choice1 == 1:
			add_tip()
			print("Your order will be ready in %d minute(s). Please be at the restaurant in %d minutes at the latest, or let us know at 123-456-6789 if you can't make it." % (Item.prep_time, Item.prep_time+15))
			break
		elif choice1 == 2:
			while True:
				choice2 = int(input("1. pick up or 2. get it delivered? Enter the corresponding number: "))
				if choice2 == 1:
					print("Your order will be ready in %d minutes. Please pick it up in %d minutes at the latest, or let us know at 123-456-6789 if you can't make it." % (Item.prep_time, Item.prep_time+15))
					break
				elif choice2 == 2:
					add_tip()
					print("Your order should reach you in %d minutes at the latest. Please contact us at 123-456-6789 if it doesn't reach you by then." % (Item.prep_time+Item.delivery_time))
					break
				else:
					print("Invalid answer.")
			break
		else:
			print("Invalid answer.")


def bill():										#displays bill with all charges
	print("\nThank you for ordering! Here is your bill:\n")

	receipt = ""
	for i,item in enumerate(Item.ordered):
		line = str(i+1) + ". " + item.name + " "*(35-len(item.name)-3) + "- $%.2f" % item.price + "\n"
		receipt += line
	
	if Item.tip_amt >0:
		line = "Tip" + " "*(35-3) + "- $%.2f" % Item.tip_amt + "\n" + "\n"
		receipt += line 
	
	line = "Total:" + " "*(35-6) + "- $%.2f" % (Item.total_cost+Item.tip_amt)
	receipt += line

	print('''				DcRonald's 
——————————————————————————————————————————''')
	print(receipt)
	print('''——————————————————————————————————————————
				Thank You!
	''')


find_branch()
menu()
misc_choices()
bill()

