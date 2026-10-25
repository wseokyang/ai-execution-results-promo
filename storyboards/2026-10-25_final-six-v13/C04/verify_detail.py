from render_c04 import *
final=OUT/'C04_Q-AI_Fair_final_v13.mp4'
groups=[('note',np.arange(3,4.75,.125),(570,180,900,370)),('handoff',np.arange(8.75,9.5,1/12),(580,340,910,490)),('papers',np.arange(20,24,.25),(320,345,710,585))]
for name,times,box in groups:
 picks={round(float(t)*FPS) for t in times};tiles=[]
 with av.open(str(final)) as c:
  for i,f in enumerate(c.decode(video=0)):
   if i not in picks:continue
   crop=f.to_image().crop(box);tile=Image.new('RGB',(400,274),(18,20,20));crop.thumbnail((400,245));tile.paste(crop,((400-crop.width)//2,26));ImageDraw.Draw(tile).text((10,4),f'{i/FPS:.3f}s',font=font(17),fill='white');tiles.append(tile)
 sheet=Image.new('RGB',(1200,274*math.ceil(len(tiles)/3)))
 for j,im in enumerate(tiles):sheet.paste(im,(j%3*400,j//3*274))
 sheet.save(OUT/f'detail_{name}.jpg',quality=96)
print('detail sheets saved')
