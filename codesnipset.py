######## youtube 동영상 url 추출

from urllib.parse import *
from urllib.request import *
import json,re
def utbmv(url):
	with urlopen(url) as u:
		html = u.read().decode()
	g = re.search(r'ytplayer.config = ({.+});\b', html)
	if g:
		jd = json.loads(g.groups()[0])
		jd = jd['args']['url_encoded_fmt_stream_map']
		urllist = parse_qs(jd)['url']
		ret = []
		for urlexp in urllist:
			urlprs = urlparse(urlexp)
			ret.append(urlunparse(urlprs))
		return ret
# ret = utbmv('https://www.youtube.com/watch?v=abcd')


########## xls 파일로 부터 패턴 추출함수
import xlrd
import re
def xlspget(xls, pat):
	retPat = []
	p = re.compile(pat)
	wb = xlrd.open_workbook(xls)
	for nsht in range(wb.nsheets):
		sht = wb.sheet_by_index(nsht)
		for r in range(sht.nrows):
			for c in sht.row(r):
				if p.findall(c.value):
					retPat+=p.findall(c.value)
	return retPat
# ret = xlspget(r'C:\Users\HS\Desktop\x.xlsx', '\d{9}') # 엑셀파일에서 EDI 코드 추출하기


########### doc 파일로부터 패턴 추출
from zipfile import ZipFile
from html.parser import HTMLParser
import re
def docpget(doc, pat):
	p = re.compile(pat)
	class docXLMParser(HTMLParser):
		ret = ''
		def handle_data(self, data):
			self.ret += data
		def get_data(self):
			return self.ret
	with open(doc, 'rb') as fp:
		z = ZipFile(fp)
		xml = z.read('word/document.xml').decode()
		psr = docXLMParser()
		psr.feed(xml)
		return  p.findall(xml)
		


# ret = docpget(r'C:\Users\HS\Desktop\edis.docx','\d{9}')
# print(' '.join(ret))

######## 배열객체 정렬하여 출력하기

import pprint
table =\
 [
 ['id','ip','contents','date','good','bad'],
 ['ez05****','49.143.xxx.206','con','2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212','con','2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212','con','2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212','con','2016-01-31T17:54:28.0+0900' , 0, 0],
 ['ez34****','49.143.xxx.212','con','2016-01-31T17:54:28.0+0900' , 0, 0]
 ]

# width = max(map(lambda x: len(repr(x)),table))*2
# pp=pprint.PrettyPrinter(compact=True, width = width, indent=4)
# pp.pprint(table)

#### 예외정보 잡아 내기

import sys
import traceback

try:
	1/0
except:	
	type_err, val_err, trcbk = sys.exc_info()
	# print(type_err.__name__, val_err,sep='\n')
	traceback.print_exception(type_err, val_err, trcbk)
else:
	pass


### 다운로드시 프로그레스바 cmd창에 표현: 명령 프롬프트 상에서표현
url=''
to = ''
urlretrieve(url,to, lambda b,bs,ts: sys.stdout.write('\r[{}{}] {:0.0%}'.format('#'*round(b*bs/ts*20),'.'*(20-round(b*bs/ts*20)),b*bs/ts)))


## 테이블(리스트)를 csv 형식의 파일로 전환, 대상 파일 이름이 존재 하면 filename(n).csv 과 같이 넘버링하여 생성해 줌
import os, csv
def tbl2csv(retTbl, retFile, isrun = True):
	if os.path.exists(retFile):
		fn, ext = os.path.splitext(retFile)
		mat = re.match('(.*)\((\d+)\)', fn)
		if mat:
			f, n = mat.groups()
			fn = '{}({})'.format(f, int(n)+1)
		else:
			fn = '{}({})'.format(fn, 1)
		fname = fn + ext
		tbl2csv(retTbl, fname, isrun)
	else:
		with open(retFile,'wt', newline ='') as fp:
			wtr = csv.writer(fp)
			for row in retTbl:
				wtr.writerow(row)
		if isrun:
			os.startfile(retFile)


## URL 에서 호스트 URL만 추출
from urllib.parse import *
url = 'https://www.druginfo.co.kr/detail/product.aspx?pid=47815'
host = urljoin(url,'/')
# print(host) # https://www.druginfo.co.kr/
newurl = urljoin(url,'d.html') # detail 이하 경로 d.html로 덮어씀 
# print(newurl) # https://www.druginfo.co.kr/detail/d.html



## 윈도우 cmd 명령어 실행 하기
from subprocess import *
print(check_output('dir', shell=True).decode('cp949'))

## maketrans 사용
trantab = ''.maketrans('abcdef', '123456')
'as soon as possible'.translate(trantab)


## pdf 파일 회전 하기
import tempfile, glob, os
from PyPDF2 import PdfFileReader, PdfFileWriter
def PDFRotator(pdf, rot=90, recursive=True):
	if pdf.endswith('.pdf'): 			
		with tempfile.TemporaryFile() as tmp:
			with open(pdf, 'r+b') as rfp:
				rPdf, wPdf = PdfFileReader(rfp), PdfFileWriter()
				for page in map(lambda x:x.rotateClockwise(rot), rPdf.pages):
					wPdf.addPage(page)
				wPdf.write(tmp)
				tmp.seek(0)
			with open(pdf, 'wb') as wfp:
				wfp.write(tmp.read())
	elif os.path.isdir(pdf):
		for f in glob.glob(os.path.join(pdf,'*' if recursive else '*.pdf')):
			PDFRotator(f, rot)

tgtPath = r'C:\pdfPath'
PDFRotator(tgtPath,recursive=False)


# 장고 스타일 정렬
# ret = sort_record(ret, ordering=['약품명', '-불출일자'])

from xlrd import open_workbook

def sort_record(records, ordering=[]):
    s = records
    for col in reversed(ordering):
        reverse = col.startswith('-')
        col = col.strip('-')
        s = sorted(s, key=lambda row:row[col], reverse=reverse)
    return s

def records_from(excel, sheet_index=0):
	wb = open_workbook(excel)
	ws = wb.sheet_by_index(sheet_index)
	return [dict(zip(ws.row_values(0),ws.row_values(r))) for r in range(1, ws.nrows)]


path = '마약잔량.xls'
ret = records_from(path)
ret = sort_record(ret, ordering=['약품명', '불출일자'])


# 테이블, url 크롤링
from bs4 import BeautifulSoup
from urllib.request import *
from urllib.parse import *
import re

class Crawler(object):
	"""docstring for Crawler"""
	def __init__(self, url, page_encoding='utf-8', **req_header):
		self.url = url
		req = Request(url)
		for hdr, val in req_header.items():
			req.add_header(hdr, val)
		self.soup = BeautifulSoup(urlopen(req).read().decode(encoding=page_encoding), 'html.parser')


	def show_html(self):
		print(self.soup)
		
	def ext_links(self, regPattern, **tagAttr):
		rex = re.compile(regPattern)
		for tag, attr in tagAttr.items():
			qry = '{}[{}]'.format(tag, attr)
			links = self.soup.select(qry)
			return [link for link in links if rex.search(link[attr])]

	def ext_tables(self, *column, only_data=True):
		spc = re.compile('\s+')
		ret = []
		for table in self.soup('table'):
			if table('table'):
				continue
			hdr, *recs = table('tr')
			hdr_val = [spc.sub(' ', hdr.text).strip() for hdr in hdr.select('td, th')]

			if set(column) <= set(hdr_val):
				if only_data:
					ret+=[dict(zip(hdr_val, [spc.sub(' ',rec.text).strip() for rec in rec('td')])) for rec in recs]
				else:
					ret+=[dict(zip(hdr_val, [rec for rec in rec('td')])) for rec in recs]
		return ret



# 엑셀 데이터 작업 
from itertools import groupby
from operator import itemgetter

import xlrd

class ExcelParser:

	def __init__(self, xl_path = None, file_content=None, sheet_index=0, **extra_fields):
		wb = xlrd.open_workbook(xl_path) if xl_path else xlrd.open_workbook(file_content=file_content)
		ws = wb.sheet_by_index(sheet_index)
		fields = ws.row_values(0)
		self._records = [dict(zip(fields, ws.row_values(i))) for i in range(1, ws.nrows)]
		for row in self._records:
			row.update(**extra_fields)

	def __getitem__(self, index):
		return self._records[index]
	
	def __len__(self):
		return len(self._records)

	def __call__(self):
		return self._records

	def select(self, *fields, where=lambda row:row):
		if not fields:
			fields = self._records[0].keys()	
		ret =  [{k:v for k, v in row.items() if k in fields} for row in self._records if where(row)]
		self._records = ret
		return self

	def order_by(self, *rules):
		for rule in reversed(rules):
			rvs = rule.startswith('-')
			rule = rule.strip('-')
			self._records.sort(key=lambda x: x[rule], reverse=rvs)
		return self
			
	def distinct(self, *cols):
		ret = sorted(self._records, key= itemgetter(*cols))
		self._records =  [next(l) for g, l in groupby(ret, key=itemgetter(*cols))]
		return self
	
	def update(self, where=lambda row:row, **set):
		for row in self._records:
			if not where(row):
				continue
			for k, func in set.items():
				row[k] = func(row)
		return self

	def group_by(self, field, subtotal=False, **having):
		self._records.sort(key=itemgetter(field))
		ret = []
		sb = []
		for g, l in groupby(self._records, key=itemgetter(field)):
			row = list(l)
			padrow = {}.fromkeys(self._records[0].keys(),'')
			sb.append(row)
			d = {}
			for k, func in having.items():
				s = func([float(e[k]) for e in row])
				padrow[field] = g
				padrow[k] = s
				
				d.setdefault(g,[]).append({k: s})
			sb.append(padrow)
			ret.append(d)
		return sb if subtotal else ret
	



path = '마약잔량.xls'


exl= ExcelParser(path, 잔여량=0) # adding extra fields

exl.order_by('불출일자','-병동') # django style sort

# chaining method
exl = exl.select('불출일자','처방일자', '병동','약품명','잔여량','집계량','총량', where=lambda x: '2016-06-01' < x['불출일자'] < '2016-06-16' and x['처방일자']==x['불출일자'] and x['약품명']!='염산페치딘 주사 1ml').update(잔여량=lambda row: float(row['집계량'])- float(row['총량']))
# groupby using sum, len...(Count)
g=exl.group_by('약품명', subtotal=False, 잔여량=sum, 집계량=len)
# print(exl())
print(list(g))