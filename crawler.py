from robobrowser import RoboBrowser
import re
import pandas as pd

class tmkCrawler():
    def __init__(self, query = None, url = 'http://tmk.nytud.hu/query.html'):
        self.query = query
        self.url = url

    def get_tmk_df(self, query):
        self.query = query
        soup = self.get_result_html(query)
        print('TMK results for the query are returned.')
        # number of hits
        no = int(soup.find('p', 'rescnt').contents[0].split()[0])
        print('{} results found for the query.'.format(no))
        records = soup.find_all('div', 'sol')
        df = self.create_df(records)
        print('DF has been created.')

        return df

    def create_df(self, records):
        columns = ['id', 'text', 'focus_ind', 'year', 'type', 'location', 'correspondents', 'full']
        # df.append({'name': 'Zed', 'age': 9, 'height': 2}, ignore_index=True)
        df = pd.DataFrame(columns=columns)
        for record in records:
            bib, rec = self.parse_hit(record)
            focus_list = rec[1]
            text = rec[0]
            for focus in focus_list:
                df = df.append({'id': bib['id'],
                                'text': text,
                                'focus_ind': focus,
                                'year': bib['year'],
                                'type': bib['type'],
                                'location': bib['location'],
                                'correspondents': bib['correspondents'],
                                'full': bib['full']}, ignore_index=True)

        df['id'] = df['id'].astype('int')
        df['focus_ind'] = df['focus_ind'].astype('int')
        df['year'] = df['year'].astype('int')

        return df

    def save_tmk_results(self, query, file_name):
        df = self.get_tmk_df(query)
        df.to_json(file_name, force_ascii=False)

    def get_result_html(self, query):
        self.query = query
        browser = RoboBrowser(parser='html.parser')
        browser.open(self.url)
        form = browser.get_form()
        form['q'].value = query
        browser.submit_form(form)
        print('Query results returned.')
        return browser.parsed

    def parse_hit(self, record):
        bgr, sol = record.contents
        hit = sol.find('div', 'c')
        bib = self.get_background(bgr.string)  # dict
        rep = self.get_sentence_rep(hit)

        return (bib, rep)

    def get_background(self, background):
        # '[1] Nád. p. 3 1550-02-26, Nádasdy Tamás > Kanizsay Orsolya, nemes > feleség - 970974 '
        # '[1] Bosz. 1a., Abaúj-Torna megye, Szilas, 1736. ::: - 970221 '
        # '[4] Bosz. 23. Bihar megye, Keserű, 1714. ,> ,> (E) - 971201 '
        biblio = {}
        if background.split()[1] == 'Bosz.':
            biblio['type'] = 'Witch'
            #print(background)
            loc_span = re.search(r'([A-Za-záéöüóűúőí ]*\S+ (vár)?megye[A-Za-záéöüóűúőí ,]*)', background).span()
            #print(background[loc_span[0]:loc_span[1]].strip())
            biblio['location'] = background[loc_span[0] : loc_span[1]].strip()
            biblio['correspondents'] = ''
        else:
            biblio['type'] = 'Letter'
            biblio['correspondents'] = re.findall(r',([\S ]*>[ \S]*?)[,-]', background)[0].strip()
            biblio['location'] = ''
        year_ind = re.search(r'\d{4}', background).span()
        biblio['year'] = int(background[year_ind[0]: year_ind[1]])
        biblio['id'] = int(background.split(' - ')[1])
        biblio['full'] = background
        return biblio

    def get_sentence_rep(self, hit): # a hit is a structure with div class='c'
        words = hit.children
        focus_ind = []
        record_rep = []
        ind = 0
        for word in words:

            if word == '\n':
                # print('Line skipped')
                # print(word == '\n')
                pass
            elif word['class'][0] == 'gapped':
                # gapped word sequence
                subwords = word.find_all('div','w')
                for sw in subwords:
                    record_rep.append(self.get_word_rep(sw))
                    ind += 1
            elif word['class'][0] == 'focus':
                new_word = word.find('div', 'w')
                record_rep.append(self.get_word_rep(new_word))
                focus_ind.append(ind)
                ind += 1
            elif word['class'][0] == 'w':
                record_rep.append(self.get_word_rep(word))
                ind += 1
            elif word['class'][0] == 'cbnd':
                record_rep.append('BREAK')
                ind += 1
            else:
                raise NameError('Error: word type is not found\n{}'.format(word))
        return (record_rep, focus_ind)

    def get_word_rep(self, word_box):
        # original form
        org = word_box.find('span', 'org')
        org_del = org.find('span', 'del')
        # if deleted
        if org_del is not None:
            org = org.text
            org_del = org_del.text
            org = org.replace(org_del, '{'+org_del+'}') # the curly braces represent deletion
            nrm = word_box.find('span', 'nrm')
            nrm_del = nrm.find('span', 'del')
            if nrm_del is not None:
                nrm = nrm.text.replace(nrm_del.text, '{'+nrm_del.text+'}')
                return(self.replace_html(org),
                       self.replace_html(nrm),
                       '',
                       '')
            else:
                return (self.replace_html(org),
                    self.replace_html(nrm.text),
                    '',
                    '')
        # try to look for deletion attribute
        # normalized form
        else:
            nrm = word_box.find('span', 'nrm')
            # lemma
            lem = word_box.find('span', 'lem')
            # PoS tag
            tag = word_box.find('span', 'tag')

            return (self.replace_html(org.text),
                    self.replace_html(nrm.text),
                    self.replace_html(lem.text),
                    self.replace_html(tag.text))

    def replace_html(self, text):
        return text.replace('\xa0', ' ')

