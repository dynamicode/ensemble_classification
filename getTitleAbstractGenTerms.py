import solr
import os
import codecs

# create a connection to a solr server
solrConn = solr.SolrConnection('http://ideal.cc.vt.edu/solr-ideal/collection2/')

# Open file containing list of topics
fd = open("leaf_topics.txt", "r")

# do a search for each topic
for line in fd:
	topic = line.rstrip()
	queryString = 'concept_desc:'+topic
	try:
		# get response object for query
		response = solrConn.query(queryString, rows = 1000)
		count = 0
		if(response.results):
			for hit in response.results:
				count += 1
				absPresent = 0
				genTermsPresent = 0
				if('abstract' in hit.keys()):
					absPresent = 1
					abstract = hit['abstract']
					abstract = abstract.lower()
				title = str(hit['title'])
				if('general_term' in hit.keys()):
					generalTerm = hit['general_term']
					genTermsPresent = 1

				if not os.path.exists(topic):
					os.makedirs(topic)
				fdinternal = codecs.open(os.path.join(topic, str(count)+'.txt'), 'w+','utf-8')
				if(absPresent == 1):
					fdinternal.write(abstract)
				fdinternal.write(title.lower())
				if(genTermsPresent == 1):
					fdinternal.write(str(generalTerm))	
				fdinternal.close()		
				
	except RuntimeError as e:
		print e
		pass

fd.close()
