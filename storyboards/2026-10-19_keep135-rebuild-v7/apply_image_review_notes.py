"""Apply document corrections after independent and peer image review."""
from pathlib import Path
import json

R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def put(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def amend(c):
    cid=c['id']
    selected={e['cut_id']:e['image_path'] for e in read('image_manifest_'+cid+'.json')['images'] if e.get('selected',True)}
    for s in c['shots']:
        s['image_file']=selected[s['id']]
        if cid=='C04' and s['id']=='K04':
            s['screen']='태블릿에 다수 반입 문서 목록과 AI 문서 대조의 확인 후보가 함께 보인다. RC가 후보의 왼쪽 신고 내부 탑승자 없음, 오른쪽 첨부 식사·물·수저를 짚어 직접 대조한다. 뒤쪽 CM은 화면을 직접 읽지 않고 RC 설명을 듣고 목마 쪽으로 짧게 눈을 돌린다.'
            s['next_motion']='RC가 신고 구절과 급식 요청을 차례로 짚으며 공개한다. CM은 설명을 듣고 목마로 눈을 돌린다. 마지막 수저 지목은 다음 원문 대조로 연결.'
        if cid=='C04' and s['id']=='K05':
            s['screen']='RC가 이미 나란히 펼쳐 든 실제 신고서의 탑승자 없음과 첨부 급식 메모를 보여준다. GU는 원문 초승달과 뒤 목마 표식을 대조하고 닫힌 배식 수레로 시선을 옮긴다.'
            s['first_frame']='실제 신고서와 급식 메모는 RC 손에 이미 펼쳐져 있다. 봉투·목마 초승달이 함께 보이고 GU는 원문을 보고 있다. GU가 원문 내용과 실물 표식을 확인하기 직전.'
            s['next_motion']='RC가 펼쳐 든 두 원문 내용이 맞음을 말로 확인한다. GU가 실물 표식과 수레로 시선을 옮긴다. 새로 펼치는 동작을 추가하지 않는다.'
            s['sound']='종이를 잡은 손의 작은 마찰음. 짧은 말 약1초와 표식·수레 시선이 겹침.'
        if cid=='C04' and s['id']=='K07':
            s['postproduction_notes']='실제 첫 프레임의 GU 장갑은 뚜껑 손잡이 바로 위다. 후속 첫 동작에서 손잡이를 확실히 잡은 뒤 뚜껑을 연다. 목마 창은 이 컷에서 닫힌 상태를 유지한다.'
        if cid=='C04' and s['id']=='K09':
            s['framing']='CM의 얼굴·망토 손을 전경에 두고 목마의 세 배식창을 후경에 유지하는 미디엄 와이드. 작은 나무 숟가락이 밝은 수레 앞에서 읽힐 크기. 행사명은 실제 복합 배경의 우상단에 대비 패널로 배치.'
            s['subtitle']='28–34초 전체6초, 우상단 짙은 반투명 패널에 3행: 2026년 품질팀 / AI 실행 결과 / 발표 대회. 보조 문구는 생략.'
            s['postproduction_notes']='행사명 권장 안전영역: 화면 가로64~98%, 세로2~20%의 우상단. 짙은 반투명 패널 위 흰색 3행 제목을 6초 유지한다. 병사 얼굴·세 창·그릇·지휘관 얼굴/손/숟가락을 가리지 않는다. 이 위치는 정지 PNG 기준이며 향후 움직임과 실제 합성 가독성은 다시 확인한다. GU는 국자를 드는 동작 시작까지만, 높은 창에 실제 배식 완료를 추가하지 않는다.'
        if cid=='C02' and s['id'] in ['K07','K08','K09']:
            s['postproduction_notes']='현재 PNG의 전화 화면과 출력사진은 같은 현장·인물·장비 구성을 참조했지만 픽셀 동일성을 보장하지 않는다. 향후 영상에서는 K07 실제 촬영 순간의 한 사진을 확정해 K08·K09 출력/게시 영역에 동일하게 재사용한다. K07 실제 담당자의 지목 동작과 휴대전화 미리보기의 시점을 맞춘다. 보조 참조 원본은 images/C02/S07_document_photo.png이며 현재 첫프레임9장에 포함하지 않는다.'
    shots={s['id']:s for s in c['shots']}
    for scene in c.get('scene_list',[]):
        s=shots[scene['linked_cuts'][0]]
        for a,b in [('image_file','image_file'),('representative_frame','first_frame'),('framing','framing'),('next_motion','next_motion')]:scene[a]=s[b]
        scene['continuity']=s['continuity_in']+' / '+s['continuity_out']
        if s.get('postproduction_notes'):scene['postproduction_notes']=s['postproduction_notes']
    if cid=='C04':
        for t in c['text_assets']:
            if t['cut']=='K09':
                t['exact']=['2026년 품질팀 AI 실행 결과 발표 대회']
                t['rule']='우상단 짙은 반투명 패널, 3행, 6초. 별도 보조 문구 생략. 최종 합성은 향후 확인.'
    return c

def main():
    assert read('image_cross_reviews.json')['status']=='all_three_returned'
    draft=read('director_draft.json')
    draft['concepts']=[amend(c) for c in draft['concepts']]
    put('director_draft.json',draft)
    allboards=read('storyboards.json')
    new={c['id']:c for c in draft['concepts']}
    allboards['concepts']=[new.get(c['id'],c) for c in allboards['concepts']]
    for cid in ['C01','C03','C05']:
        assert next(c for c in allboards['concepts'] if c['id']==cid)==read('retained_concept_'+cid+'.json')
    put('storyboards.json',allboards)
    print('Image review document amendments applied; PNG bytes unchanged.')

if __name__=='__main__':main()
