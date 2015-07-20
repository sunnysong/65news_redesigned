#!usr/bin/env python
# -*- coding: gbk -*-

from bs4 import BeautifulSoup
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# using selenium to get the html source of a dynamci page
# tested successfully

def load_url(url):
	""" if get_next is set to True,
	the function will scrape the next page in the pagination panel
	by default, it will start with page 2

	"""
	# driver = webdriver.Firefox()
	driver = webdriver.PhantomJS()
	driver.get(url)
	WebDriverWait(driver, 500).until(
		EC.presence_of_element_located((By.CLASS_NAME, "articleDetailList")))

	html_page = driver.page_source
	driver.quit()
	return html_page

def get_page(url, loop_times=0):
	# click on the next page
	# wait for the page to load
	# Xpath //*[@id="page_news"]/div/a[2]
	# xpath is not consistent, not suitable for pinpointing the next page
	# if on the last page on the pagination panel
	# next_page = driver.findElement(By.CLASS_NAME, 'next')
	driver = webdriver.Firefox()
	driver.get(url)
	mouse = webdriver.ActionChains(driver)

	WebDriverWait(driver, 500).until(
		EC.presence_of_element_located((By.CLASS_NAME, "articleList")))

	html_pages = []
	html_page = driver.page_source
	# html_pages.append(html_page)
	html_pages.insert(0, html_page)

	i = 0
	# span_element = driver.find_element(By.CLASS_NAME, 'next')

	while i <= loop_times:
		driver.find_element_by_css_selector('a.next').click()
		# mouse.move_to_element(span_element).click(span_element).perform()
		time.sleep(2)
		WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.CLASS_NAME, "article")))

		html_page = driver.page_source

		html_pages.append(html_page)
		i += 1
		time.sleep(3)
	driver.quit()

	return html_pages

def make_list_soup(html_page):
	soup = BeautifulSoup(html_page)
	soup = soup.findAll('div', {'class': 'article'})
	# the above line returns an array, to call find_all on its member elements
	# we need to iterate over it.

	return soup
# is it best to define one function for each properties? like get_date, get_title
# or just one function which returns a tuple

def make_detail_soup(html_page):
	soup = BeautifulSoup(html_page)

	return soup

def make_post(bsObj):
	# Iterate over the articles on the current page
	for each in bsObj:
			# get title
		from app import db
		from app.models import Post

		title = each.find('div', {'class': 'content'}).h4.get_text()
		# get summary
		posted = Post.query.filter_by(title=title).first()
		if not posted:
			summary = each.p.get_text()

			# get keywords
			temp = []
			for a in each.find('div', {'class': 'keywords'}):
				temp.append(a.get_text())
			# keywords should be returned as a string delimited by ,
			# i.e. 'pollution, ep'
			keywords = ','.join(temp)

			# get external links for imgs
			# add the upload feature for imgs in the future
			try:
				href = each.find('img').attrs['src']
			except:
				href = ''
			# how to deal with articles that did not upload imgs

			site = 'http://120.24.245.101/info/view/container/index/'
			detail_url = site + each.find('h4').a.attrs['href']


			# load the detail page, make page soup
			detail_page = load_url(detail_url)
			detail_soup = make_detail_soup(detail_page)


			# get timestamp
			timestamp = detail_soup.find('span', {'class':'article_time'}).get_text()
			# 2015-07-08 14:10:40
			# convert it to a datetime object, 14:10

			# get body_html, preserve the tags
			body_html = detail_soup.find('div', {'class':'article_detail'})
			body_html = str(body_html)

			# get source
			source = detail_soup.find('span', {'class':'article_source'}).get_text()

			#update model, database


			# (self, title, summary, source, timestamp, keywords, img_href, body_html)
			post = Post(title, summary, source, timestamp, keywords, href, body_html)
			db.session.add(post)
			db.session.commit()
		



# for each div.article we find, we call the make_post method
def main():
	urllist = [('#a_news', 12), ('#a_industry', 7), ('#a_technology', 6),
			   ('#a_encyclopedia',8), ('#a_original', 0)]
	site = 'http://120.24.245.101/info/view/container/index/index.html'
	for url, loop_times in urllist:
		url = site + url
		pages = get_page(url, loop_times) 

		for page in pages:
			soup = make_list_soup(page)
			make_post(soup)

if __name__ == '__main__':

	main()

