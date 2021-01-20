import os
import threading

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# 파일확장자 2020-12-04 업데이트
fileExtensions = {
    'Ada': 'ada',
    'Algol 68': 'a68',
    'Assembly (32bit)': '32bit.asm',
    'Assembly (64bit)': '64bit.asm',
    'Bash': 'sh',
    'Befunge': 'befunge.bf',
    'Boo': 'boo',
    'Brainfuck': 'brainfuck',
    'C# 6.0 (Mono)': '6.0mono.cs',
    'C# 9.0 (.NET)': 'NET.cs',
    'C++11 (Clang)': 'clang_cpp11.cpp',
    'C++11': 'cpp11.cpp',
    'C++14 (Clang)': 'clang_cpp14.cpp',
    'C++14': 'cpp14.cpp',
    'C++17 (Clang)': 'clang_cpp17.cpp',
    'C++17': 'cpp17.cpp',
    'C++20 (Clang)': 'clang_cpp20.cpp',
    'C++20': 'cpp20.cpp',
    'C++98 (Clang)': 'clang_cpp98.cpp',
    'C++98': 'cpp98.cpp',
    'C11 (Clang)': 'clang_c11.c',
    'C11': 'c11.c',
    'C2x (Clang)': 'clang_c2x.c',
    'C2x': 'c2x.c',
    'C90 (Clang)': 'clang_c90.c',
    'C90': 'c90.c',
    'C99 (Clang)': 'clang_c99.c',
    'C99': 'c99.c',
    'Cobol': 'cob',
    'D (LDC)': 'ldc.d',
    'D': 'd',
    'F# (.NET)': 'net.fs',
    'F# (Mono)': 'mono.fs',
    'Fortran': 'f95',
    'FreeBASIC': 'bas',
    'Go (gccgo)': 'gccgo.go',
    'Go': 'go',
    'Golfscript': 'gs',
    'Haxe': 'haxe.py',
    'INTERCAL': 'i',
    'Java 11': 'j11.java',
    'Java 15': 'j15.java',
    'Java 8 (OpenJDK)': 'j8openjdk.java',
    'Java 8': 'j8.java',
    'Kotlin (JVM)': 'jvm.kt',
    'Kotlin (Native)': 'native.kt',
    'LOLCODE': 'lol',
    'Lua': 'lua',
    'OCaml': 'ml',
    'Objective-C': 'm',
    'Objective-C++': 'mm',
    'PHP': 'php',
    'Pascal': 'pas',
    'Perl': 'pl',
    'Pike': 'pike',
    'PyPy2': 'pypy2.py',
    'PyPy3': 'pypy2.py',
    'Python 2': 'py2.py',
    'Python 3': 'py3.py',
    'R': 'R',
    'Rhino': 'rhino.js',
    'Ruby 2.7': 'rb2_7.rb',
    'Rust 2015': 'rs15.rs',
    'Rust 2018': 'rs18.rs',
    'Scheme': 'scm',
    'Swift': 'swift',
    'SystemVerilog': 'sv',
    'Tcl': 'tcl',
    'Text': 'txt',
    'TypeScript': 'ts',
    'VB.NET 4.0 (Mono)': 'vb4_0mono.vb',
    'Visual Basic (.NET)': 'net.vb',
    'Whitespace': 'ws',
    'awk': 'awk',
    'bc': 'bc',
    'node.js': 'js',
    'sed': 'sed',
    '아희': 'aheui',
}

def mkdir(dir):
    if not os.path.exists(dir):
            os.mkdir(dir)

def openFileToWrite(filedir):
    return open(os.path.join(workingDir, filedir), 'w+', encoding='utf-8')

def isSigned():
    # ul의 세번째 li의 텍스트가 "로그인"이면, 로그인 되지 않음
    return soup.find('ul', class_="loginbar").find_all('li')[2].text != "로그인"

# --------------------------크롤링

# 맞은 문제 번호 가져오는 함수
# 반환형 set(str)
def getSolvedProblems():
    problems = set()
    for tag in soup.find(class_='panel-body').findAll('a', class_="result-ac"):
        problems.add(tag.text)
    return problems

# 반환형 dict(),
# {
# 'solutionId' : str,
# 'spaceComplexity' : str,
# 'timeComplexity' : str,
# 'language' : rawdata[6],
# 'codeLength' : rawdata[7],
# }
def getOptimizedSolutionData(problemId):
    # 여기 URL을 크롤링해서 가져오는건 어떨까?
    # 장점 : queryObjs가 바뀌어도 상관없음
    # 단점 : 해당 문제 페이지를 get해야해서 크롤링 양 증가
    #        -> 크롤링을 싫어하시는 백준형님이 차단박을 수도..?
    queryObjs = { 
        'problem_id' : problemId,
        'user_id' : userName,
        'language_id': '-1',
        'result_id': '4',
        'from_mine' : '1',
    }
    problemURL = baseURL + '/status?'
    for queryOption in queryObjs:
        problemURL += queryOption + '=' + queryObjs[queryOption] + '&'
    problemURL = problemURL[:-1] # 백준에서 쿼리할때 URL과 똑같이 하기 위함, 주석처리해도 문제없음 (그냥 맘에 들어서 씀)
    # 문제 채점 결과 페이지 get
    tryCounter = 0
    while True:
        success = False
        try:
            tryCounter += 1
            res = session.get(problemURL)
            success = True
        except Exception as e:
            print("*Exception at main.py line 136, {}\n*[Request URL] : {}\n*[Retried] : {}\n".format(e, problemURL, tryCounter), end="")
            if tryCounter == 3:
                print("**********[Failed] : ", problemURL)
                return [dict(), []]
        if success:
            if tryCounter > 1:
                print("*[Success] : ", problemURL)
            break
    page = bs(res.text, 'html.parser')
    # 채점 결과 크롤링
    results = page.find('tbody').find_all('tr')
    # 채점 결과 데이터 가공 & 최적화 답안 검색
    # 필요한 데이터 : 채점번호(problemId), 언어(lang)
    # raw 데이터에서 순서 : 채점번호(0), 아이디(1), 문제번호(2), 결과(3), 메모리(4), 
    #                       시간(5), 언어(6), 코드 길이(7), 제출한 시간(8)
    # 최적화 답안 검색 : (언어별)시간->공간->코드길이->채점번호(최근)
    optimizedData = dict()
    printData = []
    for result in results:
        rawdata = result.find_all('td')
        data = {
            'solutionId' : rawdata[0].contents[0],
            'spaceComplexity' : rawdata[4].contents[0],
            'timeComplexity' : rawdata[5].contents[0],
            'language' : rawdata[6].contents[0].contents[0],
            'codeLength' : rawdata[7].contents[0],
        }
        if debugMode:
            printData.append(data)
        if len(optimizedData) == 0:
            optimizedData = data
        else:
            # asc(<) : 1(top priority), 2, 3, 4
            # desc(>) : 4(top priority), 3, 2, 1
            asc, desc = 0, 1
            priority = {
                'timeComplexity' : asc,
                'spaceComplexity' : asc,
                'codeLength' : asc,
                'solutionId' : desc,
            }
            for criterion in priority:
                if priority[criterion] == asc:
                    if data[criterion] < optimizedData[criterion]:
                        optimizedData = data
                        break
                else:
                    if data[criterion] > optimizedData[criterion]:
                        optimizedData = data
                        break
    return [optimizedData, printData]

def downloadBySolutionId(solutionId):
    res = session.get(baseURL + '/source/download/' + solutionId)
    return res.text

def makeFileDir(problemId, data):
    problemId = f'{problemId:0>5}'
    fileName = problemId
    if data['language'] in fileExtensions:
        fileName += '.' + fileExtensions[data['language']]
    else:
        fileName += '.unknown.txt'
    return [problemId, fileName]

def writeCodeToFile(code, filedir):
    with openFileToWrite(filedir) as file:
        file.write(code)


def getWriteOptimizedCode(problemId):
    data, printDatas = getOptimizedSolutionData(problemId)
    if len(data) == 0:
        return
    if debugMode:
        printForm = ""
        for printData in printDatas:
            printForm += str(printData)+'\n'
        printForm += "Best : {:>8}{:>12}{:>6}ms{:>8}MB{:>6}B\n".format(
            problemId, data['language'], data['timeComplexity'], data['spaceComplexity'], data['codeLength']
        )
        print(printForm, end="")
    fileDir, fileName = makeFileDir(problemId, data)

    mkdir(os.path.join(workingDir, fileDir))
    fileFullDir = os.path.join(fileDir, fileName)
    print(fileDir, " : ", fileName, " : ", fileFullDir)
    if not os.path.exists(fileFullDir):
        writeCodeToFile(downloadBySolutionId(data['solutionId']), fileFullDir)


if __name__ == '__main__':
    print(
    """[BOJ Code Downloader]
        Mode
        1.  Run with cookie (require cookie named 'OnlineJudge')
        2.  Run with selenium (require id, pw, should solve reCaptcha)"""
    )
    mode = int(input("enter mode (default:1) : "))

    userToken = ""
    userName = ""

    if mode == 1:
        userToken = input('enter cookie named "OnlineJudge" (which published after login) : ')
    elif mode == 2:
        userId = input("id : ")
        userPw = input("pw : ")
        baseURL = "https://www.acmicpc.net"
        driver = webdriver.Chrome()
        driver.get(baseURL + '/login')
        driver.find_element_by_name("login_user_id").send_keys(userId)
        driver.find_element_by_name("login_password").send_keys(userPw)
        driver.find_element_by_name("auto_login").click()
        driver.find_element_by_id("submit_button").click()
        # reCaptcha를 하기 위한 10분
        WebDriverWait(driver, 60 * 10).until(lambda x: x.find_element_by_class_name("tp-banner-container"))
        userToken = driver.get_cookie('OnlineJudge')['value']
        driver.quit()
    print("Your cookie ('OnlineJudge'): ", userToken)
    debugMode = input("Use debug mode? (Y/N, default: Y) : ")
    debugMode = not(debugMode == 'N' or debugMode == 'n')

    baseURL = 'https://www.acmicpc.net'

    workingDir = os.path.join(os.getcwd(), 'users', userName)
    mkdir(workingDir)
    
    with requests.Session() as session:
        # 로그인 핵심 토큰 지정
        session.cookies.set('OnlineJudge', userToken)
        # 메인 페이지 접속
        res = session.get(baseURL)
        soup = bs(res.text, "html.parser")
        # userName 추출
        try:
            userName = soup.find('a', class_='username').text
        except AttributeError:
            print("로그인 실패, 토큰 확인, 또는 웹사이트 새로고침")
        # 유저 페이지 이동
        res = session.get(baseURL + '/user/' + userName)
        soup = bs(res.text, "html.parser")

        if isSigned():
            print("로그인 성공")
        else:
            print("로그인 실패, 토큰 확인, 또는 웹사이트 새로고침")
            exit(1)
        
        solvedSet = getSolvedProblems()
        
        for problemId in solvedSet:
            th = threading.Thread(target=getWriteOptimizedCode, args=(problemId,), daemon=False)
            th.start()
            #getWriteOptimizedCode(problemId)



    # with open(os.path.join(working_dir, "soup.html"), 'w+', encoding='utf-8') as soup:
        
    # with open(os.path.join(working_dir, "req.html"), "r", encoding="utf8") as req:
