# boys

deep learning project
* 실행전 준비 사항

1. 가상환경 실행 (라이브러리 설치)
  source ./.venv/bin/actiavte

2. .env 파일 생성후 입력
  # 보내는 사람 네이버 아이디
  NAVER_ID = '이메일'
  NAVER_PASS = '비밀번호'

  # 수신자(헬스장 사장님)
  RECIPIENT_ID = "이메일"

3. start.py만 실행하면 시작함

### 간단 설명

얼굴을 탐지 후 deepSort로 tracking 시작

1. "추적 중인 얼굴이 처음 등장했는지?", "멤버가 아니면서 30프레임 이상 추적되고 있는지?(재확인용)
    - 개발자 확인용으로 './checkFaceFolder'에 자른 얼굴 저장
      -> deepface로 확인 (return: True, False)
      -> True면 초록색 선으로 'member' 표시
      -> False면 빨간색 선으로 'UnKnown' 표시

