def manga_fetch(dir,adres):
	import urllib,re,zipfile,os,sys
	if not os.path.isdir(dir):
		try:
			os.mkdir(dir)
		except OSError:
			print 'Nie mozna utworzyc folderu'
	os.chdir(dir)			
	##adres = 'http://www.mangapanda.com/yuureitou'
	domain = re.search('(http://.*?)/',adres,re.DOTALL).group(1)
	strona = urllib.urlopen(adres)
	zawartosc = strona.read()
	strona.close()

	chapter_table = re.search('<div\s*?id="chapterlist"\s*?>(.+?)</table>',zawartosc,re.DOTALL).group(1)
	chapters = re.findall('<a\s*?href="(.+?)"\s*?>',chapter_table,re.DOTALL)

	for c in chapters:
		nazwa_chaptera = ''.join(c.split('/'))
		if(zipfile.is_zipfile(nazwa_chaptera+'.zip')):
			continue
		sys.stdout.write('Pobieram '+nazwa_chaptera+'...\n')
		archiwum = zipfile.ZipFile(nazwa_chaptera+'.zip','w')
		adres = domain+c
		strona = urllib.urlopen(adres)
		zawartosc = strona.read()
		strona.close()
		lista = re.search('<\s*?div\s*?id=\"selectpage\"\s*?>(.*?)<\s*?/div\s*?>',zawartosc,re.DOTALL).group(1)
		lista_stron = re.findall('<\s*option\s*value="(.+?)".*?>',lista,re.DOTALL)
		##ile_stron = re.search('</select>\s*?of\s*?([\d]+)\s*</div>',zawartosc,re.DOTALL).group(1)
		for index,i in enumerate(lista_stron,start=1):
			strona = urllib.urlopen(domain+i)
			zawartosc = strona.read()
			strona.close()
			sys.stdout.write('\tTrwa pobieranie strony '+str(index)+' z '+str(len(lista_stron))+'... ')
			adres_obrazka = re.search('<\s*img.*?src="(.*?)".*?/>',zawartosc,re.DOTALL).group(1)
			nazwa_strony = str(index).zfill(len(str(len(lista_stron))))+os.path.splitext(adres_obrazka)[1]
			for p in range(3):
				try:
					urllib.urlretrieve(adres_obrazka,nazwa_strony)
				except IOError, e:
					print 'Blad I/O, ponawiam probe'
				else: break
			archiwum.write(nazwa_strony)
			os.remove(nazwa_strony)
			sys.stdout.write('Zakonczono\n')
		archiwum.close()
		sys.stdout.write('Zakonczono pobieranie '+nazwa_chaptera+'\n')
	os.chdir('..')


