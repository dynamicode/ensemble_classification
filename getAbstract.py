import solr
import os
from sets import Set

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
		response = solrConn.query(queryString)
		if(response.results):
			for hit in response.results:
				abstract = str(hit['abstract'])
				abstract = abstract.lower()
				title = str(hit['title'])
				if not os.path.exists(topic):
					os.makedirs(topic)
				fd = open(os.path.join(topic,title+'.txt'), 'w+')
				fd.write(abstract)
				fd.close()										
	except:
		pass

