1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
import os
import google.oauth2.credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors
 
# Bu fonksiyon, Google API'ye erişim için yetkilendirme sağlar
def get_authenticated_service():
    creds = None
    # Erişim tokenlarını diskte depolamak için dosya yolu
    token_path = 'token.json'
 
    # Eğer daha önce yetkilendirme yapılmışsa, onu yükle
    if os.path.exists(token_path):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(token_path)
 
    # Token geçerli değilse veya yoksa, kullanıcıyı yetkilendir
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                ['https://www.googleapis.com/auth/youtube.upload']
            )
            creds = flow.run_local_server(port=0)
 
        # Yetkilendirme bilgilerini diske kaydet
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
 
    # Yetkilendirilmiş bir YouTube servisi döndür
    return build('youtube', 'v3', credentials=creds)
 
def upload_video(youtube, file, title, description):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
        },
        'status': {
            'privacyStatus': 'public'  # Video'nun gizlilik durumu: 'public', 'private', veya 'unlisted'
        }
    }
 
    # Video yükleme isteği yap
    try:
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=file
        ).execute()
 
        video_id = response['id']
        print(f"Video başarıyla yüklendi. Video ID: {video_id}")
    except googleapiclient.errors.HttpError as e:
        print(f"Hata: {e}")
        return None
 
# Google API'ye erişim için yetkilendirilmiş bir servis oluştur
youtube_service = get_authenticated_service()
 
# Yüklemek istediğiniz video dosyasının yolu
video_file_path = 'video.mp4'
 
# Videoyu yükle
upload_video(
    youtube_service,
    video_file_path,
    title='Yüklediğiniz Video Başlığı',
    description='Yüklediğiniz Video Açıklaması'
)
