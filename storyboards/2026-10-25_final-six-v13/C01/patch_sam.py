from pathlib import Path
p=Path('storyboards/2026-10-25_final-six-v13/C01/render_c01.py');s=p.read_text(encoding='utf-8');s=s.replace("def actor_mask(rgb,key,t):\n hsv=", "def actor_mask(rgb,key,t):\n exact=OUT/'foreground_masks'/key/f'{round(t*FPS):04d}.png'\n if exact.exists():return np.array(Image.open(exact)).astype(float)/255\n hsv=")
s=s.replace("rgb=overlay(rgb,art,mm.track(original),hmask)","rgb=overlay(rgb,art,mm.track(original),actor_mask(original,key,st))")
p.write_text(s,encoding='utf-8')
