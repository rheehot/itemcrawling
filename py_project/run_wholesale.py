# 모듈 가져오기
# pip install selenium
# pip install bs4
# pip install pymysql
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import time
import sys
from DbMgr import DBHelper as Db
from Tour import TourInfo
from ItemInfo import ItemInfo

# 명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pymysql as my


# 사전에 필요한 정보를 로드 => DB Shell, batch 파일에서 인자로 받아서 세팅
db       = Db()
main_url='https://ecigarettes-wholesale.com'
keyword='vapor'

#상품정보를 담는 리스트 (Tourinfo 리스트)
iteminfo_list = []

# 드라이버 로드
driver = wd.Chrome(executable_path='chromedriver.exe')

driver.implicitly_wait(3)
# 차후 -> 옵션 부여하여 (프록시, 에이전트 조작, 이미지를 배제)
# 크롤링을 오래 돌리면 => 임시파일들이 쌓인다  => 템프파일 삭제

# 로그인
driver.get('https://ecigarettes-wholesale.com/index.php?route=account/login')
driver.find_element_by_id('input-email').send_keys('ausumvapor@gmail.com')
driver.find_element_by_id('input-password').send_keys('vapor101')

driver.implicitly_wait(1)

# login 버튼 클릭
# driver.find_element_by_class_name('btn btn-primary button').click()
# driver.find_element_by_class_name('btn btn-primary button').submit()

# type = submit 방식
driver.find_element_by_css_selector("input[type='submit']").click()

# 사이트 접속 (get)
# main page
driver.get(main_url)

driver.maximize_window() # For maximizing window
driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

# 검색창을 찾아서 검색어 입력
# id : SearchGNBText
driver.find_element_by_name("search").send_keys(keyword)

# 수정할 경우 => 뒤에 내용이 붙어버림 => .clear() -> send_keys

driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

# 검색 버튼 클릭
# class : search-btn
# driver.find_element_by_css_selector('button.search-btn').click()
from selenium.webdriver.common.keys import Keys
driver.find_element_by_name("search").send_keys(Keys.RETURN)

# 잠시 대기 => 페이지가 로드되고 나서 즉각적으로 데이터를 획득하는 행위는 자제
# 명시적 대기 => 특정 요소가 로케이트 (발견될 때까지) 대기

# try:
#     element = WebDriverWait(driver,10).until(
#         #지정한 한개 요소가 올라오면 wait 종료
#         EC.presence_of_element_located((By.CLASS_NAME, 'row main-products product-grid'))
#     )
# except Exception as e:
#     print('오류 발생', e)

# 암묵적 대기 => DOM이 다 로드 될때까지 대기하고 먼저 로드 되면 바로 진행
# 요소를 찾을 특정 시간 동안 DOM 플링을 지시 예를 들어 10초 이내 라고
# 발견 되면 진행
driver.implicitly_wait( 10 )

# 일단 중지
# sys.exit(1)

# 절대적 대기 => time.sleep(10)  -> 클라우으 페어(디도스 방어 솔루션)

# 더보기 눌러서 => 게시판 진입
# driver.find_element_by_css_selector('.oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click()

# 게시판에서 데이터를 가져올 때
# 데이터가 많으면 세션 (혹시 로그인을 해서 접근되는 사이트인 경우) 관리
# 특정 단위별로 로그아웃 로그인 계속 시도

# 특정 게시물이 사라질 경우 => 팝업 발생 (없는...) => 팝업 처리 필요
# 게시판 스캔시 => 임계점을 모름!!
# 게시판 스캔 => 메타 정보 획득 => loop 를 돌려서 일괄적으로 방문 접근 처리

# 상품 정보

# searchModule.SetCategoryList(1, '') 스크립트 실행
# 16인 임시값, 게시물을 넘어갔을 때 현상을 보려고 확인차 입력하는 값
for page in range(1, 2):# 16):
    try:
        # 자바스크립트 구동하기
        # driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)

        # load more 방식
        if page > 1: # 2번째 부터 more 버튼 클릭
            driver.find_element_by_css_selector('ias-trigger ias-trigger-next button').click()

        time.sleep(2)
        # print("%s 페이지 이동" % page)
        # print("%s load more click" % page)
        #################################################
        # 여러 사이트에서 정보를 수집할 경우 공통 정보 정의 단계 필요
        # 상품명, 코멘트, 기간1, 기간2, 가격, 평점, 썸네일, 링크 (상품상세정보)
        boxItems = driver.find_elements_by_css_selector('.product-grid-item')
        # boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')
        # print('row main-products product-grid', boxItems)

        # 상품 하나 하나 접근
        for li in boxItems:
            # 이미지를 링크값을 사용할 것인가? 직접 다운로드 해서 우리 서버에 업로드 (ftp) 할 것인가?
            # print( '썸네임', li.find_element_by_css_selector('img').get_attribute('src') )
            # print( '링크',   li.find_element_by_css_selector('a').get_attribute('href') )
            # print( '상품명', li.find_element_by_css_selector('h4.name').text )
            # print( '가격',   li.find_element_by_css_selector('.price').text )
            # print( '코멘트', li.find_element_by_css_selector('.description').text )
            # area = ''

            # for info in li.find_elements_by_css_selector('.info-row .proInfo'):
            #     print(info.text)
            # print('='*100)

            # 데이터모음
            # li.find_elements_by_css_selector('.info-row .proInfo')[1].text
            # 데이터가 부족하거나 없을 수도 있음으로 직접 인덱스로 표현은 위험성이 있음
            # title, price, area, link, img, contents=None
            # self.title = title
            # self.price = price
            # self.area = area
            # self.link = link
            # self.img = img
            # self.contents = contents

            obj = ItemInfo(
                li.find_element_by_css_selector('h4.name').text,
                li.find_element_by_css_selector('.price').text,
                'area',
                li.find_element_by_css_selector('a').get_attribute('href'),
                li.find_element_by_css_selector('img').get_attribute('src'),
                li.find_element_by_css_selector('.description').text
            )
            iteminfo_list.append( obj )
    except Exception as e1:
        print('오류', e1)

# 일단 중지
# sys.exit(1)

# print(tour_list, len(tour_list))
# 수집한 정보를 개수를 루프 => 페이지 방문 => 콘텐츠 획득 (상품상세정보) =. 디비

for iteminfo in iteminfo_list:
    #  item => iteminfo
    # print (type(iteminfo))
    # 링크 데이터에서 실데이터 획득
    # 분해 (split)
    # arr = iteminfo.link.split(',')

    # if arr:
    # 대체
    # link = arr[0].replace('searchModule.OnClickDetail(','')
    #슬라이싱 앞에 ', 뒤에 ' 제거
    # detail_url = link[1:-1]
    #상세 페이지 이동 : URL 값이 완성된 형태인지 확인 (http~)
    # driver.get(detail_url)
    time.sleep(2)
    # pip install bs4
    # 현재 페이지를 beautifulsoup의 DOM으로 구성
    # soup = bs(driver.page_source, 'html.parser')
    #현재 상세정보 페이지에서 스케쥴 정보를 획득
    # data = soup.select('.tip-cover')
    # print(type(data), len(data), data[0].contents)
    #DB 입력 => pip install pymysql
    # 데이터 sum
    # content_final = ''
    # for c in data[0].contents:
    #     content_final += str(c)

    # html 콘첸츠 데이터 전처리 (디비에 입력 가능토록)
    # import re
    # content_final   = re.sub("'", '"', content_final)
    # content_final   = re.sub(re.compile(r'\r\n|\r|\n|\n\r+'), '', content_final)

    # self.title = title
    # self.price = price
    # self.area = area
    # self.link = link
    # self.img = img
    # self.contents = contents

    link_notnull = ''
    if not iteminfo.link:
        link_notnull = 'None'
    else:
        link_notnull = iteminfo.link

    img_notnull = ''
    if not iteminfo.img:
        img_notnull = 'None'
    else:
        img_notnull = iteminfo.img

    # 콘텐츠 내용에 따라서 전처리 => data[0].contents
    db.db_insertCrawlingData(
            iteminfo.title,
            iteminfo.price,
            '',
            '',
            keyword,
            img_notnull,
            link_notnull
    )

# 종료

driver.close()
driver.quit()
sys.exit()

# 추가 작업
# proxy , agent
# mobile, pc 구분
# image 제거
# time 텀을 주어 페이지가 다 올라올 때까지 유지 필요
# m.naver.com 로그인해서 www.naver.com 로 가는 방식 사용
# login session 유지 처리, 안되면 접근권한 없음이 발생 (주기적으로 login/logout 처리)
# ghost server duplicate?