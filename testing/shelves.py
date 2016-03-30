import shelve

d = shelve.open("testdata")

d['egg'] = 'helloworld'
print(d['egg'] + '!')
d.close()
