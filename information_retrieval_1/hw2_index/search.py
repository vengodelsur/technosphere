# import sys
from index import Index

# argv = sys.argv
# argv = argv[1:] 

index = Index()
while (True):
    try:
        query = raw_input()
    except (EOFError):
        break

    print query
    found_urls = index.urls_by_query(query)
    print len(found_urls)
    for url in found_urls:
        print url 

    
