# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
# encoding: utf-8
import scraperwiki
import urlparse
import lxml.html


# create a new function, which gets passed a variable we're going to call 'url'
def scrape_dof(url):
    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)
    
    #line below selects all <div class="notice-search-item">
    rows = root.cssselect("div.notice-search-item")
    
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
       
        #n = 0
        #for a in row.cssselect("a"):
        #    print(n)
        #    print(a.get('href'))
        #    n = n+1
        
        link = row.cssselect("a")
        link1 = link[0].get('href')
        
        element = row.cssselect("div")
        dofref = element[6].text_content()
        title = element[1].text_content()
        klient = element[3].text_content()
        kgtype = element[4].text_content()
        kgdato = element[7].text_content()
        
        record['DofRef'] = dofref
        record['Title'] = title
        record['Klient'] = klient
        record['Kungj_type'] = kgtype
        record['Kungj_dato'] = kgdato
        record['Link'] = link1
       
        
        # Finally, save the record to the datastore - 'Name' is our unique key
        scraperwiki.sqlite.save(["Dofref"], record)
        
#doflist = ['www.doffin.no/Notice?query=&PageNumber=1&PageSize=20&OrderingType=0&OrderingDirection=1&NoticeType=3&IncludeExpired=false']
doflist = ['www.doffin.no/Notice?&OrderingType=0&OrderingDirection=1&IsAdvancedSearch=false&IncludeExpired=false&Cpvs=09200000+35110000+44610000+45220000+45230000+51200000+51100000+51800000+71300000+71530000+76000000']
for url in doflist:
    fullurl = 'http://'+url
    print 'scraping ', fullurl
    scrape_dof(fullurl)
    print 'and done'
