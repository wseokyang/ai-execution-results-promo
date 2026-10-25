from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
files=sorted(p.glob('proof_*.jpg'));sheet=Image.new('RGB',(1280,220*((len(files)+3)//4)),(30,30,30))
for i,f in enumerate(files):
 im=Image.open(f).resize((320,180));x=i%4*320;y=i//4*220;sheet.paste(im,(x,y+24));ImageDraw.Draw(sheet).text((x+5,y+5),f.stem,fill='white')
sheet.save(p/'proof_contact.jpg')
