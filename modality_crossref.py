from bs4 import BeautifulSoup
import requests
import csv
import re
import six
import requests_cache

#requests_cache.install_cache
#requests_cache.clear()



#xhtml = source.json()["response"]["artifact"]["xhtml"]
#print (xhtml)
artifact_id_input = input("Enter an Artifact ID, a list of Artifact IDs, or 'b' to choose a branch ")
if 'b' in artifact_id_input:
	branch_input = input("Enter the desired branch (ex: biology, chemistry): ")
		
	source1 = requests.get("https://gamma.ck12.org/taxonomy/collection/collectionHandle=" + branch_input + "?collectionCreatorID=3&includeRelations=True").text

	soup = BeautifulSoup(source1, features="lxml")

	soupy = str(soup)

	soupy_split = soupy.split()
		
	isPublished_index = soupy_split.index('"isPublished":')
		
	if soupy_split[(isPublished_index + 1)] == 'true,':		
			
		soupy_absHandle_split = soupy.split('absoluteHandle')
			
		abs_handle_lst = []
			
		handle_lst = []
	
		art_id_lst = []
						
		for i in range(len(soupy_absHandle_split)):
			if "handle" in soupy_absHandle_split[i] and "encodedID" in soupy_absHandle_split[i]:
				for_split = (soupy_absHandle_split[i]).split()
				abs_handle0 = for_split[1]
				abs_handle = ((abs_handle0)[1:(len(abs_handle0)) - 2])
				handle_index = for_split.index('"handle":')
				handle = for_split[(handle_index + 1)]
					
				abs_handle_lst.append(abs_handle)
				handle_lst.append(handle)
	
		
		for i in range(len(abs_handle_lst)):
				
			source2 = requests.get("https://gamma.ck12.org/flx/get/minimal/modalities/" + abs_handle_lst[i]).text
			
			soup = BeautifulSoup(source2, features="lxml")
				
			soupo = str(soup)
				
			soupo_split = soupo.split()
				
			for i in range(len(soupo_split)):
				if soupo_split[i] == '[{"artifactID":':
					art_id = soupo_split[(i + 1)]
					if art_id not in art_id_lst:
						art_id_lst.append(art_id)
		
		artifact_id_input = art_id_lst				
						
						
def scrape(input_index):
	#inputs
	artifact_id_input_split = artifact_id_input.split(",")
	
	if "," in artifact_id_input:
		URL = "https://gamma.ck12.org/flx/get/detail/" + artifact_id_input_split[input_index]
	elif "," not in artifact_id_input and 'b' not in artifact_id_input:
		URL = "https://gamma.ck12.org/flx/get/detail/" + artifact_id_input
	
	run_times = len(artifact_id_input_split)
	#bs4_init
	source = requests.get(URL).text
	
	soup = BeautifulSoup(source, "lxml")
	
	lst = []
	
	#artifact_id
	para_text = soup.find("p").text
	para_split = para_text.split()
	artifact_id_str_index = para_split.index('{"artifactID":')
	artifact_id_num0 = para_split[(artifact_id_str_index + 1)]
	artifact_id_num = artifact_id_num0[0:(len(artifact_id_num0) - 1)]
	
	lst.append(artifact_id_num)


	#artifact_revision_id
	artifact_revision_id_str_index = para_split.index('"artifactRevisionID":')
	artifact_revision_id_num0 = para_split[(artifact_revision_id_str_index + 1)]
	artifact_revision_id_num = artifact_revision_id_num0[0:(len(artifact_revision_id_num0) - 1)]
	
	lst.append(artifact_revision_id_num)

	#latest_revision_num
	latest_revision_num_str_index = para_split.index('"latestRevision":')
	latest_revision_num0 = para_split[(latest_revision_num_str_index + 1)]
	latest_revision_num = latest_revision_num0[1:3]
	
	lst.append(latest_revision_num)
	
	
	#body_split
	body = soup.find("body").text
	body_split = body.split()
	
	
	#title
	for i in range(len(para_split)):
		if para_split[i] == '"perma":':
			perma0 = para_split[i + 1]
			perma_split = perma0.split("/")
			perma1 = perma_split[2]
			perma2 = perma1.split("-")
			title = ' '.join(perma2)
	
	lst.append(title)

	

	#hyperlinked_branches
	crossref = soup.find_all("a")
	crossref_join = ''.join(list(map(str, crossref)))
	crossref_split_for_branch = crossref_join.split("/")
	hyperlinked_branches_lst = []
	for i in range(len(crossref_split_for_branch)):
		if crossref_split_for_branch[i] == "c":
			hyperlinked_branch = crossref_split_for_branch[i + 1]
			hyperlinked_branches_lst.append(hyperlinked_branch) 

	lst.append(hyperlinked_branches_lst)

	#hyperlinked_url
	crossref = soup.find_all("a")
	crossref_join = ''.join(list(map(str, crossref)))
	crossref_split_for_url = crossref_join.split('"')
	hyperlinked_url_lst = []
	hyperlinked_url_raw_lst = []
	for i in range(len(crossref_split_for_url)):
		if crossref_split_for_url[i] ==  "' href='\\":
			hyperlinked_url_raw = crossref_split_for_url[i + 1]
			hyperlinked_url_raw_lst.append(hyperlinked_url_raw)
			hyperlinked_url0 = "www.ck12.org" + hyperlinked_url_raw 
			hyperlinked_url = hyperlinked_url0[0:(len(hyperlinked_url0) - 1)]
			hyperlinked_url_lst.append(hyperlinked_url) 

	lst.append(hyperlinked_url_lst)
	
	#hyperlinked_words
	hyperlinked_url_raw_lst_join = ''.join(list(map(str, hyperlinked_url_raw_lst)))
	hyperlinked_url_raw_lst_split = hyperlinked_url_raw_lst_join.split("/")
	hyperlinked_words_lst = []
	for i in range(2, len(hyperlinked_url_raw_lst_split)):
		if hyperlinked_url_raw_lst_split[i] == "c":
			hyperlinked_word0 = hyperlinked_url_raw_lst_split[i - 1]
			hyperlinked_word = hyperlinked_word0[0: (len(hyperlinked_word0) - 1)]
			hyperlinked_words_lst.append(hyperlinked_word) 

	lst.append(hyperlinked_words_lst)

	
	#referenced_branch

	for i in range(len(para_split)):
		if para_split[i] == '"collectionHandle":':
			referenced_branch0 = para_split[i + 1]
			referenced_branch = referenced_branch0[1:(len(referenced_branch0) - 2)]


	lst.append(referenced_branch)
		
	#URL
	#1: perma
	for i in range(len(para_split)):
		if para_split[i] == '"perma":':
			perma0 = para_split[i + 1]
			perma = perma0[1:(len(perma0) - 2)]
	
	#2: handle
	for i in range(len(para_split)):
		if para_split[i] == '"conceptCollectionAbsoluteHandle":':
			handle0 = para_split[i + 1]
			handle = handle0[1:(len(handle0) - 2)]


	#3: using referenced branch^^

	#url_construction
	url = "https://www.ck12.org/c/" + referenced_branch + "/" + handle + perma + "/"

	lst.append(url)

	lst.append(run_times)

	return(lst)
	
	


#csv file initiation
#main code
lst0  = scrape(0)
run_times = lst0[9]
with open('crossreflinks_word.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(["Artifact ID Number", "Artifact Revision ID Number", "Latest Revision Number", "Title", "List of Hyperlinked Branches", "List of Hyperlinked Links", "List of Hyperlinked Words", "Referenced Branch", "URL"])
	for i in range(run_times):
		for d in range(len(lst0[6])):
			lst = scrape(i)
			artifact_id_num = lst[0]
			artifact_revision_id_num = lst[1]
			latest_revision_num = lst[2]
			title = lst[3]
			hyperlinked_branches_lst_all = lst[4]
			hyperlinked_url_lst_all = lst[5]
			hyperlinked_words_lst_all = lst[6]
			referenced_branch = lst[7]
			url = lst[8]
			hyperlinked_branch = hyperlinked_branches_lst_all[d]
			hyperlinked_url = hyperlinked_url_lst_all[d]
			hyperlinked_word = hyperlinked_words_lst_all[d]
			writer.writerow([artifact_id_num, artifact_revision_id_num, latest_revision_num, title, hyperlinked_branch, hyperlinked_url, hyperlinked_word, referenced_branch, url])





