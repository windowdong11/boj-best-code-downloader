# Boj-Best-Code-Downloader

백준에서 가장 최적화된 코드 다운로드하는 프로그램

## 사용법 (how-to-use)

Windows : ```python main.py```  
Linux : ```python3 main.py```(확인안해봤음)

```
[BOJ Code Downloader]
        Mode
        1.  Run with cookie (require cookie named 'OnlineJudge')
        2.  Run with selenium (require id, pw)
enter mode (default:1) : <mode_number>
# Mode 1
enter cookie named "OnlineJudge" (which published after login) : <cookie>
# Mode 2
id : <boj id>
pw : <boj pw>

use debug mode? (Y/N, default: Y) : <Y/N>
```

### Username

![username](/images/username.PNG)  

### Cookie

![cookie](/images/cookie.PNG)  

### 쿠키 확인방법 (how-to-check-cookie)

1. f12를 통해 개발자 모드로 들어간다.
2. Application탭에서 Storage>Cookies>https://www.acmicpc.net을 연다.
3. "OnlineJudge"를 검색하면 Value에 쿠키값이 들어있다.

## 문제해결, 쿠키를 잘 입력했는데 안될때 (Troubleshooting)

1. 로그아웃된 경우(로그인 상태 유지 체크x)
2. 로그인 상태 유지 체크했는데도 안되는 경우
원인 : 세션만료

### 로그아웃 된 경우

로그아웃 된 경우, 다시 로그인 할때, 쿠키값이 변경 되는데,  
다시 로그인하고, 쿠키값을 새로 넣어주면 된다.

### 로그인 상태 유지 체크했는데도 안되는 경우

백준 사이트 한번 들어갔다 와주면 된다.(또는 새로고침)  
만약 로그인이 풀리면 토큰이 바뀌었는지 확인하고 진행하면 된다.

## 종속성(Requirements)

python3(작성버전 3.8.3), requests, BeautifulSoup, selenium, ChromeDriver

```
pip install requests
pip install BeautifulSoup
pip install selenium
```

ChromeDriver : https://sites.google.com/a/chromium.org/chromedriver/downloads
(Windows 기준)  
크롬 드라이버를 다운받고,  
C:\WebDriver\bin\ 에 chromedriver.exe 저장  
C:\WebDriver\bin\ 을 환경변수, Path에 추가  
(C:\WebDriver\bin\은 어느위치든 상관없음)  
아래 사진처럼 환경변수 추가  
![설정방법](/images/env_setting.png)


## TODO

- [ ] (기능)언어별 최적화된 코드 다운로드  
- [x] (최적화)이미 다운로드 된 파일은 다운로드하지 않도록 하기  

## Update Log

2020.12.4

1. 첫 버전 작성 및 업로드, 멀티스레딩 추가  

2020.12.5

1. 파일명을 기준으로, 이미 다운된 파일은 다운하지 않도록 변경  
2. 셀레니움을 통한 로그인 후, 쿠키 가져오는 기능 추가
