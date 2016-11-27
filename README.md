# tmkBot  

The **tmkBot** is a Python tool for interacting with the TMK concordance webpage (http://tmk.nytud.hu) which is a corpus of Middle Hungarian non-official texts. The corpus was implemented with Emdros (http://emdros.org).
At the moment, the tool is capable of downloading the search results of queries provided in the full emdros format e.g. `[w focus nrm ~ '^kedves$’]` (cf. http://emdros.org/MQL-Query-Guide.pdf).  

The results are put in a data frame with the following columns:  
1. **id**: id of the query result  
2. **text**: **list of words** where a **word** has the form: `[original form, normalized form, lemma, PoS tag, deleted?]`, the deleted feature can take 2 values: 0 and 1 where 0 represents non-deleted and 1 represents deleted  
3. **focus_ind**: index of the word with the queried feature in the text list
year: year of creation  
4. **type**: letter/witch, type of the source document: can be a private letter or the transcript of witch trials  
5. **location**: place of creation of the source document (only applies to trial transcripts)  
6. **correspondents**: correspondents of letter sources, doesn’t apply to trial transcripts  
7. **full**: full reference to the source  

The query results can be returned as a Pandas data frame or can be saved as a JSON file.
