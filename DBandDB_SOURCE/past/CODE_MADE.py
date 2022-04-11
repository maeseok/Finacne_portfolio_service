import pandas as pd
import pickle

#pandas 모듈을 사용하여 html을 읽어와 데이터프레임을 생성한다.
stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0] 
# 필요한 것은 "회사명"과 "종목코드" 이므로 필요없는 column들은 제외
stock_code = stock_code[['회사명', '종목코드']] 
# 한글 컬럼명을 영어로 변경 
stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'}) 
# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
stock_code.code = stock_code.code.map('{:06d}'.format) 


codepath="./code.txt"
f = open(codepath,"w")
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 
stock_code.to_pickle(codepath)
f.close()
