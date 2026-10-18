from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'storyboards.json';d=json.loads(p.read_text(encoding='utf-8-sig'));cs={c['id']:c for c in d['concepts']}
cs['C01']['difficulty_reason']='포스터와 원본 첫 순간의 몸모양을 맞추고 의자가 빠지는 실제 동작을 보여야 한다. 코치의 뒤집힌 자세와 제자의 모방도 유지한다. 일반 제작 대안은 고정된 큰 모니터에 별도로 촬영·생성한 원본 동작을 합성하고, 교습소는 동일 세트에서 촬영하는 방식이다. 원본 사고를 두 정지 화면만으로 대체하지 않는다. 특정 도구 성공은 보장하지 않는다.'
cs['C05']['difficulty_reason']='가족 스릴러에서 공연으로 바뀌는 조명·감정, 개가 가방을 짧게 밀고 노트북을 보는 반응의 연속성이 필요하다. 운반 과정은 생략한다. 일반 제작 대안은 가방이 발앞에 닿는 낮은 구도와 개가 옆에서 노트북을 응시하는 구도를 연결하는 방식이다. 특정 동물 동작·생성 성공을 보장하지 않는다.'
c=cs['C04'];c['shots'][1]['sound']=c['shots'][1]['sound'].replace('5초','4초');c['shots'][3]['sound']='K02와 동일한 4초 패턴의 발소리·옷 마찰. 손짓→짧은 두 발빼기→인사에 같은 박자, 새 반복 없음.'
c=cs['C05'];ss={s['id']:s for s in c['shots']}
ss['K05']['transition']='합주 중 하드 컷. 운반 예고 없이 K06의 아빠 발앞 가방 반환을 공개.'
ss['K06']['transition']='악기 수납과 가방을 올리는 준비를 생략해 K07의 무릎 위 가방으로 컷.'
ss['K07']['transition']='같은 상태를 넓힌 K08의 마지막 가족 화면으로 컷.'
ss['K08']['continuity_in']='K07의 노트북·개 시선·악기 위치 유지. 새로운 실제 업무를 발명하거나 화면에 표시하지 않음.'
for cid in ['C01','C02','C04','C05']:
 c=cs[cid]
 c['scene_list']=[{'concept_id':cid,'scene_id':s['scene_id'],'linked_cuts':[s['id']],'representative_frame':s['first_frame'],'framing':s['framing'],'continuity':s['continuity_in']+' / '+s['continuity_out'],'aspect_ratio':'16:9','reference_cut':s['reference_cut'],'next_motion':s['next_motion'],'image_file':s['image_file'],'text_policy':'행사명·자막은 후편집. 생성 이미지에는 글자·로고 없음.'} for s in c['shots']]
d['status']='text_metadata_confirmation_pending'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'blind_storyboards.json').write_text(json.dumps({'instruction':'행동/대사먼저. C03보존확정.','concepts':[{'id':c['id'],'duration_seconds':c['duration_seconds'],'shots':[{k:s[k] for k in ['id','scene_id','start','end','screen','framing','subtitle','dialogue','sound','transition']} for s in c['shots']]} for c in d['concepts']]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v=json.loads((R/'text_revision_disposition.json').read_text(encoding='utf-8-sig'));v['changes']['A-S07/B-S05/C-S06/C-S07']='C05 예고시선전환삭제와새K06→K07→K08참조정정. C04음향4초패턴통일. C01대체지시도실제의자이탈과뒤집힌교본보존. C05난이도에서운반삭제.';(R/'text_revision_disposition.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('metadata corrected; C03 preserved')
