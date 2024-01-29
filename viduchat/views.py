import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings

SERVER_PORT = settings.SERVER_PORT
OPENVIDU_URL = settings.OPENVIDU_URL
OPENVIDU_SECRET = settings.OPENVIDU_SECRET

# Create your views here.
# POST 요청만 받게 하겠음.
@api_view(['POST'])
def initializeSession(request):
    try:
        if request.POST:
            body = request.POST.dict() #플라스크에서 딕셔너리 형태로 들어왔음.
        else:
            body = {}
        # 세션 초기화
        res = requests.post(
            OPENVIDU_URL + "openvidu/api/sessions",
            verify=False,
            auth=("OPENVIDUAPP", OPENVIDU_SECRET),
            headers={'Content-type': 'application/json'},
            json=body
        )
        # HTTP 응답 상태코드 에러 발생시 예외 처리 -> except
        res.raise_for_status() 

        # flask) response.json()["sessionId"] 
        # -> 응답으로 받는 json객체에서 sessionId키의 value만 가져오겠다.
        # -> 세션 식별자
        sessionId = res.json()["sessionId"]
        data = {
            "sessionId": sessionId,
        }
        return JsonResponse(data)
    except requests.exceptions.HTTPError as err:
        # 409(Conflict error) : 서버와 클라이언트의 충돌
        # 여러 클라이언트가 동시 request를 보내면 데이터 일관성을 위해 나기도 함.
        if (err.response.status_code == 409):
            # Session already exists in OpenVidu
            # sessionId request에 이미 있는 customSessionId를 가져온다면 충돌에러를 낸다.
            return JsonResponse({"sessionId": request.POST.get("customSessionId")})
        else:
            return JsonResponse({"error": str(err)})

@api_view(['POST'])   
def createConnection(request, sessionId):
    if request.POST:
        body = request.POST.dict()
    else:
        body = {}
    res = requests.post(
        OPENVIDU_URL + "openvidu/api/sessions/" + sessionId + "/connection",
        verify=False,
        auth=("OPENVIDUAPP", OPENVIDU_SECRET),
        headers={'Content-type': 'application/json'},
        json=body
    )
    token = res.json()["token"]
    return JsonResponse({"token": token})