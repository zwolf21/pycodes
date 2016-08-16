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
# ret = utbmv('https://www.youtube.com/watch?v=eTlDQuvs_SQ')


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
# ret = xlspget(r'C:\Users\HS\Desktop\양지병원원내약품리스트_20160621.xlsx', '\d{9}') # 엑셀파일에서 EDI 코드 추출하기


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
		


# ret = docpget(r'C:\Users\HS\Desktop\보험코드.docx','\d{9}')
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
url='http://w2.hunet.hscdn.com/hunet/M_Learning/HLSC16743/High/01_01_01.mp4'
to = 'C:\\Users\\HS\\Desktop\\test.mp4'
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

tgtPath = r'C:\Users\HS\Documents\KSHP'
PDFRotator(tgtPath,recursive=False)
