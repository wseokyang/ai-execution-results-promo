from pathlib import Path
import json
R=Path(__file__).resolve().parent
ROOT=R.parent.parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    for name in ['storyboard_final_confirmation.json','image_final_confirmation.json']:
        q=read(name)
        assert q['status']=='all_three_confirmed' and set(q['reviewers'])=={'A','B','C'}
        assert all(not r['required_remaining'] for r in q['reviewers'].values())
    v=read('validation.json');assert v['status']=='passed' and v['new_images']==2 and v['reused_images']==41
    d=read('storyboards.json');d['status']='storyboards_and_first_frames_complete_user_creative_review_pending';put('storyboards.json',d)
    team=read('team_execution.json');team['status']='complete'
    for stage in team['actual_collaboration']:stage['status']='complete'
    team['limits']='정지 이미지 및 계획 대사/행동 검토. 실제 연기·음성·관객 반응 미검증.';put('team_execution.json',team)
    put('progress.json',{'status':'complete','stage':'storyboards_and_actual_first_frames','new_images':2,'reused_images':41,'unchanged_protected_images':25,'total_images':43,'Flow':'not_used','new_video_or_audio':False})
    put('delivery_status.json',{'status':'complete','scope':'C02/C04 limited tone polish; C01/C03/C05 unchanged; Git inline view','new_images':2,'reused_images':41,'total_images':43,'video_audio_flow':False,'V8_user_creative_acceptance':'pending'})
    put('review_summary.json',{
        'status':'required_storyboard_and_image_findings_closed',
        'user_scope':'V7 C02/C04 not bad, requested a little more atmosphere; C01/C03/C05 retained. Full image storyboard requested on Git.',
        'creative_changes':[
            'C02: 현장마다 네가 있었어라는 진지한 추적. 고정 카메라에 이제 못 움직여라고 말하고 수갑 클릭 뒤 음악만 0.6초 멈춘다.',
            'C02: 사례 설명 반복을 덜고 자기 사진을 떼려다 사진 가장자리를 펴 주는 행동으로 체면을 지킨다.',
            'C04: 숨소리도 내지 마라 다음 꼬르륵. AI 문서 비교의 수저 질문이 지휘관의 마지막 숟가락과 연결된다.',
            'C04: 그릇 공개 순간에 전쟁 음악을 끊고 들킨 지휘관도 지휘관부터라고 명령한다.',
            '이야기·AI 후보 대조와 사람 확인·길이·구별되는 외형 유지. 첫 프레임2장만 보완,41장 원본 재사용.'
        ],
        'github_finding':'V7 index.html and selected43 PNGs were already present on remote main. Added root inline Markdown and README entry for direct GitHub reading.',
        'storyboard_reviews':'storyboard_reviews.json','storyboard_cross':'storyboard_cross_reviews.json','storyboard_final':'storyboard_final_confirmation.json',
        'image_reviews':['image_review_A.json','image_review_B.json','image_review_C.json'],'image_cross':'image_cross_reviews.json','image_final':'image_final_confirmation.json',
        'reference_scope':'reference_basis.json','preservation':'preservation_manifest.json',
        'limits':['동작·음성·립싱크·관객 반응 미검증','내부 검수 완료는 V8 사용자 창작 수용을 뜻하지 않음','HTML 브라우저 자동 렌더 검수는 기존 로컬 파일 제한을 존중해 미실행. PNG 실제 열람·정적 HTML 링크·해시 검증.']})
    put('future_production_notes.json',{'scope':'향후 별도 영상 제작 요청 때 사용할 메모. 이번 영상·음원·Flow 실행 없음.',
        'notes':{c['id']:{s['id']:s.get('postproduction_notes','') for s in c['shots']} for c in d['concepts']},
        'constraints':['생성 원본 PNG 유지','C02 K07 한 번 촬영한 사진을 K08/K09에 동일하게 재사용','C04 K09 우상단 제목 패널은 실제 영상 움직임과 가독성 확인 필요','음향 절단과 발화는 아직 계획','새 영상 제작 요청 전에 ai-flow 재개 금지']})
    (R/'README.md').write_text('# V8 — 2·4안 대사·연출 보완\n\n[전체 이미지 콘티](index.html) · [Git에서 바로 읽는 이미지 콘티](https://github.com/wseokyang/ai-execution-results-promo/blob/main/콘티_바로보기.md) · [전체 컷 표](STORYBOARDS.md)\n\nC01·C03·C05 콘티 객체와 PNG25장은 V7 그대로입니다. C02 35초, C04 34초의 사건·AI 역할을 유지하고 대사·체면을 지키는 행동·음향을 다듬었습니다. C02 K01과 C04 K09 두 장을 내장 image_gen으로 보완했습니다. 나머지41장은 원본 재사용입니다.\n\n세 검수자의 독립 검토·교차 확인·필수 지적 확인을 거쳤습니다. 실제 동작·음성·립싱크·관객 반응을 검증한 결과는 아닙니다.\n\n[정확한 프롬프트·매핑](scene_manifest.json) · [검토 기록](review_summary.json) · [보존 증명](preservation_manifest.json) · [기술 검증](validation.json)\n\n기존 완성 C01 36초 영상·이전 콘티·배포 패키지·원자료 보존. 이번 Flow·영상·음원·크레딧 사용0.\n',encoding='utf-8')
    resume=ROOT/'RESUME_CODEX.txt';data=resume.read_bytes();marker='[2026-10-19 V8 최신 완료'
    if not data.startswith(marker.encode()):
        head=f'''{marker} — 1·3·5안 유지 / 2·4안 대사·연출 보완 / Git 이미지 열람 개선]
사용자: V7 2/4 나쁘지 않으나 조금 더 느낌 요청, 전체 이미지 콘티 Git 업로드 요청. 2/4 이야기·AI 역할·35/34초 유지. C01/C03/C05 전체 객체·25PNG 바이트 보존.
작업: storyboards/{R.name}/. C02 K01과 C04 K09 두 실제 첫 프레임만 보완. 41장 원본 재사용, 총43장. 정확한 채택 경로는 storyboards.json/scene_manifest.json.
Git 루트 콘티_바로보기.md에서43장 이미지와 대사를 직접 읽는다. README 맨 위 바로가기. V7 HTML/43PNG는 이미 업로드되어 있었으며 V8 HTML과 모든 PNG도 저장. 비공개 유지, 공개 Pages 없음.
세 명의 전체 콘티·실제 이미지 독립/교차/필수 지적 확인 완료. review_summary.json 확인. 실제 동작·음성·립싱크·관객 반응·V8 사용자 취향 승인 미확인.
Windows: C:/Users/wseok/.codex/visualizations/2026/10/19/01a13daf-3732-7b90-99a8-92c605090d35/B_comedy_tone_polish_v8/index.html. 같은 상위 폴더의 전체 ZIP. 패키지 검증 별도, Git 상태는 실제 log/remote 확인.
기존 C01 36초v07 SHA 유지. Flow·영상·음원·크레딧 사용0. ai-flow PAUSED 유지. 별도 영상 요청 전 재개 금지.

이하 이전 작업 이력 — 최신 V8 지시 우선

'''
        resume.write_bytes(head.replace('\n','\r\n').encode()+data)
    brief=ROOT/'team/brief.toml';data=brief.read_bytes();key='[creative_direction_2026_10_19_tone_polish_v8]'
    if key.encode() not in data:
        extra=f'''\n{key}
user_feedback = "V7 2/4 나쁘지 않으나 조금 더 느낌. 전체 이미지 콘티를 Git에서 쉽게 찾기."
new_run = "storyboards/{R.name}"
retained = "C01/C03/C05 전체 콘티 객체·25PNG 바이트 보존. C02/C04 이야기·AI 역할·35/34초 유지."
delivery = "2/4 대사·호흡·체면 유지 행동 보완. 새 PNG2장 + 재사용41장 =43장. Git 루트 콘티_바로보기.md 추가."
scope = "시나리오와 첫 프레임만. Flow·동영상·음원 금지, 예약 PAUSED 유지. 비공개 Git 유지."
'''
        data=data.replace('creative_direction_2026_10_19_keep_c01_c03_c05를 우선한다.'.encode(),'creative_direction_2026_10_19_tone_polish_v8을 우선한다.'.encode(),1)
        brief.write_bytes(data+extra.replace('\n','\r\n').encode())
    print({'status':'complete','new_images':2,'reused_images':41})

if __name__=='__main__':main()
