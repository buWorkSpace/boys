# boys

deep learning project

가상환경 실행
source ./.venv/bin/actiavte

'./memberPhoto'에 본인 정면 사징을 넣어야 member로 인식 가능

걍 main.py만 실행하면 시작함

### 간단 설명

얼굴을 탐지 후 deepSort로 tracking 시작

1. "추적 중인 얼굴이 처음 등장했는지?", "멤버가 아니면서 30프레임 이상 추적되고 있는지?(재확인용)
    - 개발자 확인용으로 './checkFaceFolder'에 자른 얼굴 저장
      -> deepface로 확인 (return: True, False)
      -> True면 초록색 선으로 'member' 표시
      -> False면 빨간색 선으로 'UnKnown' 표시

=> 적당히 테스트느 되는데 성능이 떨어지는거 같고 느림, deepface 비동기로 해봐야겠음
