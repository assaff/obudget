#### encoding: utf8

import json
filenames = [ "financial_report/2000-2008/out.json",
              "financial_report/2009/out.json",
              "history_neto/history.json",
              "2010_planned/out.json",
              "2011_planned/out.json",
              "2012_planned/out.json",
              "queries/out.json",
              "title_cleaning.json"
              ]

alldata = {}
keys = set()

out = file('master.json','w')

for f in filenames:
    print f
    try:
        data = file(f).read()
    except Exception,e:
        print e
        continue
    for line in data.split('\n'):
        try:
            rec = json.loads(line)
            if rec.get('title') == None: continue
            if rec['code'].startswith('0000'):
                continue
            key = "%s|%10s" % (rec['year'],rec['code'])
            keys.add(key)
            alldata.setdefault(key,{}).update(rec)
        except Exception,e:
            print "error %s in line %r" % (e,line)
    
for year in range(1992,2013):
    totalkey = '%s|%8s' % (year,"00")
    if totalkey in keys:
        continue
    totalrec = { 'title'     : u'המדינה',
                 'year'      : year,
                 'budget_id' : '00',
                 }
    for key in keys:
        if key.startswith(totalkey):
            rec = alldata[key]
            for k,v in rec.iteritems():
                if type(v) == int:
                    totalrec[k] = totalrec.setdefault(k,0) + v

    print 'total:',year,totalrec
                     
    alldata.setdefault(totalkey,{}).update(totalrec)
    
        
keys = list(keys)
keys.sort()

for k in keys:
    out.write( json.dumps(alldata[k])+'\n' )
