from pathlib import Path

R=Path(__file__).resolve().parent
S=R.parent/'2026-10-19_keep13-rebuild-v6'
for name in ['merge_images.py','build_delivery.py','build_overview.py','validate_links.py','package_delivery.py']:
    text=(S/name).read_text(encoding='utf-8')
    replacements={
        "['C01','C03']":"['C01','C03','C05']",
        'keep13_rebuild_v6':'keep135_rebuild_v7',
        '1·3안 유지 / 2·4·5안 새 이야기':'1·3·5안 유지 / 2·4안 새 이야기',
        '1·3안 유지, 2·4·5안 새 이야기 — V6':'1·3·5안 유지, 2·4안 다시 구성 — V7',
        'V5 C01·C03의 콘티와 채택 PNG 17장은':'V6 C01·C03·C05의 콘티와 채택 PNG 25장은',
        '1·3안 유지 / 세 이야기 교체 · V6':'1·3·5안 유지 / 두 이야기 교체 · V7',
        '대회 · V6':'대회 · V7',
        'V6 · 컷별':'V7 · 컷별',
        '1·3안은 그대로.<br>2·4·5안은 새 이야기와 새 얼굴.':'1·3·5안은 그대로.<br>2·4안은 AI 실행이 사건의 중심.',
        '유지한 두 안의 콘티와 이미지 17장은 변경하지 않았습니다. 새 세 안은 사건·반전과 등장인물부터 다시 구성했습니다.':'유지한 세 안의 콘티와 이미지 25장은 변경하지 않았습니다. 새 두 안은 AI로 해본 일과 결과를 보여주는 행동이 사건과 반전을 만들도록 다시 구성했습니다.',
        '{len(checks)-17}장 새 첫 프레임 + 17장 유지':'{len(checks)-25}장 새 첫 프레임 + 25장 유지',
        '>1·3안 보존<':'>1·3·5안 보존<',
        "'new_images':len(checks)-17,'retained_images':17,'C01_C03_objects_unchanged'":"'new_images':len(checks)-25,'retained_images':25,'C01_C03_C05_objects_unchanged'",
        "'preserved':17":"'preserved':25",
    }
    for old,new in replacements.items():text=text.replace(old,new)
    (R/name).write_text(text.rstrip()+'\n',encoding='utf-8')
print('V7 delivery scripts prepared')
