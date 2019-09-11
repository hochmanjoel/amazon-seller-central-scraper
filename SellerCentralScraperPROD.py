import os
import sys
from os import listdir
from bs4 import BeautifulSoup # Imports tool for examining the doc
import urllib.request # Imports tool to allow access to website
import requests
from lxml import html
from csv import DictWriter # Imports tool to create CSV

def main():
	exportDict = {} # Dictionary to export to CSV
	files = os.listdir('/Users/joelhochman/Documents/Miscellaneous/MicroBiome/SecondRun/HTML/') # The files to scrape through
	approved = ['.htm'] # For filtering out non-HTML
	files[:] = [url for url in files if any(sub in url for sub in approved)] # Ensures program only looks through HTML
	print(files) # Check to make sure the files being checked
	for file in files:
		soup = BeautifulSoup(open("/Users/joelhochman/Documents/Miscellaneous/MicroBiome/SecondRun/HTML/" + file), 'html.parser') # Sets up each file for parsing
		rows = soup.find_all('tbody')[1].find_all('tr') # Creates a variable for each row which is equal to each transaction (unique orderId)
		print('\n' + file)
		for row in rows: # For each row of data, which is each unique transaction
			cells = row.find_all('td')
			if(cells[6].div.div.div.div.span.span.text) == 'Pending': #Pending orders are not included
				continue
			orderId = cells[2].div.a.text
			date = cells[1].div.div.div.text
			if (row.find(attrs={'data-test-id': "buyer-name-with-link"}) == None): # If there is no buyer name, leave variable blank
				name = ''
			elif (row.find(attrs={'data-test-id': "buyer-name-with-link"}).text != None):
				name = row.find(attrs={'data-test-id': "buyer-name-with-link"}).text
			if cells[4].div.div.div.div.a.div.text.find('Pack of 6'): # If product is Pack of 6
				product = 'Pack of 6'
			product = 'Single'
			quantity = cells[4].div.div.find('b').text
			try:
				subtotal = cells[4].div.div.find_all('div')[6].text[15:]
			except IndexError: # In case there is no subtotal (edge case that exists)
				subtotal = 0
			print(name)
			print(subtotal)
			exportDict[orderId] = {'date': date, 'name': name, 'product': product, 'quantity': quantity, 'subtotal': subtotal} # Creates the dictionary to export
	print(exportDict) # = SUCCESS
	with open('amazonData.csv', 'w') as output: # Exports dictionary to CSV
		fnames = ['orderId', 'date', 'name', 'product', 'quantity', 'subtotal'] # Field names for CSV
		writer = DictWriter(output, fieldnames=fnames)
		writer.writeheader()
		for x in exportDict:
			writer.writerow({'orderId': x, 'date': exportDict[x]['date'], 'name': exportDict[x]['name'], 'product': exportDict[x]['product'], 'quantity': exportDict[x]['quantity'], 'subtotal': exportDict[x]['subtotal']})

if __name__ == '__main__':
	main()
