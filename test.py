from crawler import tmkCrawler

from time import time

print('Import was successful.')
t = tmkCrawler()
print('Crawler was successfully initialized with the following url address:')
print(t.url)

query1 = "[txt txtid ~ 'Tel. 24. ' or meta ~ 'Tel. 24. ' [w focus tag ~ 'Loc$'] ]"
query2 = "[w focus tag ~ 'Loc$']"
query3 = "[txt txtid ~ 'Bosz'[w focus nrm ~ '^nem+csak$'] ]"
query4 = "[w focus tag ~ 'Acc$']"
query5 = "[txt txtid ~ 'Bosz. 1a., ' or meta ~ 'Bosz. 1a., ' [txt txtid ~ 'Bosz'[w focus nrm ~ '^nem+csak$'] ] ]"
query6 = "[w focus nrm ~ '^kedves$'] "

print('Query: {}'.format(query6))
t0 = time()
df = t.get_tmk_df(query6)
print('Downloading and data manipulation took {} seconds for query {}.'.format((time()-t0), query6))
print(df.shape)