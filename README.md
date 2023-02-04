### 설계 중점 및 느낀점

추후 개발때, 부딛힐 수 있는 ci/cd 와
개발환경 차이에서 생길 수 있는 문제를 container 기술로
해결하려고 노력했습니다.

또한 유닛 테스트와 통합 테스트를 구성할 수 있도록 노력했습니다.

docker-container 를 python 코드에서 컨트롤 할 수 있도록
test-container 를 염두하고 작업을 해보았지만,
코드가 너무 길어지고, 결국 중복 작업이 불가피하다고 느꼈습니다.

이유: docker-compose 나 k8s 세팅이 추가된다면, test-container 도 
같은 구성을 가져야합니다.

덕분에 github action 에서 docker-compose build 하는 세팅을 찾았고 
이를 적용하여, 테스트 환경 문제도 어느정도 해결된 것 같습니다.

아쉬운 점은 python orm 에 대한 미숙함과 dependency injection 을 구성하려다가 시간을 많이 보냈고
기능 구현만 아슬하게 끝낸것 입니다.

또한 테스트 코드가 너무 빈약해서, 테스트 코드를 많이 추가해야 할 것 같습니다.

또, service 를 분리하지 못한 부분이 아쉽습니다.

---

이외 여러 문제점

- jwt 는 액세스 토큰만 발급합니다.
- openApi spec 이 부재합니다. (대신 테스트 할 수 있도록 이메일로 postman json 파일 첨부하겠습니다.)
- 중복된 로직 코드가 많습니다.
