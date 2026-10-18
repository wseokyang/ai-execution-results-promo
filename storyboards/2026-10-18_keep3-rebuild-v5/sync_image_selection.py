from pathlib import Path
import json
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def replace_tree(x,old,new):
 if isinstance(x,str):return x.replace(old,new)
 if isinstance(x,list):return [replace_tree(v,old,new) for v in x]
 if isinstance(x,dict):return {k:replace_tree(v,old,new) for k,v in x.items()}
 return x
def main():
 d=read('storyboards.json');frozen=read('retained_concept_C03.json')
 for n,c in enumerate(d['concepts']):
  cid=c['id']
  if cid=='C03':assert c==frozen;continue
  chosen={e['cut_id']:e for e in read(f'image_manifest_{cid}.json')['images'] if e.get('selected',True)}
  assert set(chosen)=={s['id'] for s in c['shots']},(cid,len(chosen))
  if cid=='C04':
   for old,new in [('우측 힌지','좌측 힌지'),('오른쪽 힌지','왼쪽 힌지'),('문틀 오른쪽의 빈 받침','문틀 왼쪽의 빈 받침')]:c=replace_tree(c,old,new)
   c['image_continuity_decision']='S01 실제 이미지의 좌측 힌지를 기준으로 고정. 힌지 좌우 자체는 개그 필수요소가 아니므로 PD 변경 수용. 문 제거 후 전경 오른쪽 이동과 통과 공간은 유지.'
  if cid=='C05':
   c['image_continuity_decision']='S01 남매는 소파 팔걸이 뒤/쿠션 안쪽에 숨는다. K05 가방은 후경에서 식별되지 않지만 K02에서 소개됨. K06 가방은 이미 발앞에 도착하여 마지막 짧은 코 밀기부터 시작. K07 지퍼는 넓게 열려 있지만 노트북 뚜껑은 닫혀 있어 공개 동작은 유지.'
  if cid=='C02':
   c['shots'][0]['screen']=c['shots'][0]['screen'].replace('오른팔로','왼팔로')
   c['shots'][0]['first_frame']=c['shots'][0]['first_frame'].replace('왼쪽 팔 아래','오른쪽 팔 아래')
   c['shots'][7]['framing']='바깥 왼쪽에서 관객의 등 너머를 보는 고정 미디엄 와이드. 네 팬은 테이블 오른쪽 앞에, 단일 노트북은 왼쪽 끝에 있어 왼쪽 바닥 ST와 팬들 모두 표시면 앞쪽에 위치한다. ST와 노트북 사이 시야 틈을 확보한다.'
   c['shots'][8]['framing']='K08 관객 등 너머 축을 유지한 와이드. 노트북은 테이블 왼쪽 끝, 팬4명은 오른앞쪽, ST는 왼쪽 바닥과 보호 손을 유지. 좌상단 빈 벽에 후편집 자막.'
   c['shots'][7]['continuity_in']='K07에서 도착한 테이블 옆 빈자리. 카메라가 팬들 뒤쪽의 공동 관람 축으로 전환하며 네 팬은 같은 표시면 앞쪽에 남는다.'
   c['image_continuity_decision']='K01 BG 왼팔 보호/오른팔 노트북은 PD 수용. K07 후면3/4. K08–09는 관객 등 너머 구도로 바꾸고 노트북을 테이블 왼끝에 두어 스타/팬들 공동 관람 방향을 맞춤. 선택 S08_v6/S09_v3. 선행 K04/06/07의 가려진 검은면은 방향을 확정못해 재생성하지 않고 후속 화면광 메모로 남김.'
  for s in c['shots']:s['image_file']=chosen[s['id']]['image_path']
  c['scene_list']=[{'concept_id':cid,'scene_id':s['scene_id'],'linked_cuts':[s['id']],'representative_frame':s['first_frame'],'framing':s['framing'],'continuity':s['continuity_in']+' / '+s['continuity_out'],'aspect_ratio':'16:9','reference_cut':s['reference_cut'],'next_motion':s['next_motion'],'image_file':s['image_file'],'text_policy':'행사명·자막은 후편집. 생성 이미지에는 글자·로고 없음.'} for s in c['shots']]
  d['concepts'][n]=c
 d['status']='images_generated_independent_image_review_pending'
 d['scope']='4 rebuilt concepts with actual first frames, retained C03; no video/audio generation'
 d['notes']=[x for x in d['notes'] if not x.startswith('네 안 각 9컷') and not x.startswith('first_frame은')]
 note='최종 시간: C01 34초/9컷, C02 33초/9컷, 유지 C03 42초/8컷, C04 35초/9컷, C05 31초/8컷. 각 컷의 채택 실제 PNG는 image_file 및 scene_manifest.json을 따른다.'
 if note not in d['notes']:d['notes'].append(note)
 assert next(c for c in d['concepts'] if c['id']=='C03')==frozen
 dump('storyboards.json',d)
 print('selected image paths synced; C03 unchanged')
if __name__=='__main__':main()
