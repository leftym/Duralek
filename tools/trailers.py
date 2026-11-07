import subprocess, os, glob
T='/tmp/claude-0/-home-claude/cea64cde-fa3b-594e-9c77-a1e722f904fd/scratchpad/duralek/tr'
OUT='/home/claude/duralek/trailers'; os.makedirs(OUT,exist_ok=True)
def run(a): subprocess.run(a,check=True,stderr=subprocess.PIPE)
def norm(src,ss,dur,W,H,out,crop=None):
    vf=(crop+',' if crop else '')+f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p,setsar=1'
    run(['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(dur),'-i',src,'-an','-vf',vf,'-c:v','libx264','-crf','18','-preset','veryfast',out])
def still(img,dur,W,H,out,zoom_in=True):
    n=int(dur*30); z='min(zoom+0.0009,1.12)' if zoom_in else 'if(eq(on,0),1.12,max(zoom-0.0009,1.0))'
    run(['ffmpeg','-v','error','-y','-loop','1','-i',img,'-t',str(dur),'-vf',
        f'scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},zoompan=z=\'{z}\':d={n}:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s={W}x{H}:fps=30,format=yuv420p,setsar=1',
        '-c:v','libx264','-crf','18','-preset','veryfast',out])
def join(clips,durs,xf,music,mss,out,poster_t=1.5):
    args=['ffmpeg','-v','error','-y']
    for c in clips: args+=['-i',c]
    if music: args+=['-ss',str(mss),'-i',music]
    fc=[];prev='[0:v]';off=0
    for i in range(1,len(clips)):
        off+=durs[i-1]-xf
        fc.append(f'{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.3f}[v{i}]');prev=f'[v{i}]'
    total=sum(durs)-xf*(len(clips)-1)
    fc.append(f'{prev}fade=t=in:st=0:d=0.6,fade=t=out:st={total-0.8:.3f}:d=0.8[vout]')
    if music: fc.append(f'[{len(clips)}:a]atrim=0:{total:.3f},afade=t=in:st=0:d=0.8,afade=t=out:st={total-1.6:.3f}:d=1.6,volume=0.9[aout]')
    args+=['-filter_complex',';'.join(fc),'-map','[vout]']
    if music: args+=['-map','[aout]','-c:a','aac','-b:a','96k']
    args+=['-c:v','libx264','-crf','27','-preset','slow','-profile:v','high','-pix_fmt','yuv420p','-movflags','+faststart','-t',f'{total:.3f}',out]
    run(args)
    run(['ffmpeg','-v','error','-y','-ss',str(poster_t),'-i',out,'-frames:v','1','-q:v','4',out.replace('.mp4','.jpg')])
    print(os.path.basename(out),f'{total:.1f}s',os.path.getsize(out)//1024,'KB')

# Aliʻi: the painted opening, 600x800, music Before the Tide Turns
V='/home/claude/alii-fix/game/src/video/'
sc=['c_dawn','c_village','c_gather','c_fleet','c_battle','c_union','c_triumph']
cl=[];d=[]
for i,s in enumerate(sc):
    o=f'{T}/a{i}.mp4';norm(V+s+'.mp4',0.6,2.9,600,800,o);cl.append(o);d.append(2.9)
join(cl,d,0.5,'/home/claude/alii-fix/game/src/music/m_menu.m4a',2,f'{OUT}/alii.mp4')

# Od Sela do Vrha: its intro film, 540x960, menu music
src='/home/claude/odseladosuperligemobile/game/src/vid/intro.mp4'
segs=[(0.5,4.0),(9.0,3.5),(26.5,3.5),(32,3.0),(39.5,4.5)]
cl=[];d=[]
for i,(ss,du) in enumerate(segs):
    o=f'{T}/o{i}.mp4';norm(src,ss,du,540,960,o);cl.append(o);d.append(du)
join(cl,d,0.5,'/home/claude/odseladosuperligemobile/game/src/snd/mu-menu.mp3',0,f'{OUT}/od-sela-do-vrha.mp4')

# Up the Village: title art and screens, 540x960, theme music
imgs=['/home/claude/up-the-village/assets/art/title.webp']+[f'/home/claude/up-the-village/docs/store-assets/play-{n}.png' for n in ['1-welcome','2-club-before-the-match','3-match-half-time','4-gazette','7-grounds']]
cl=[];d=[]
for i,im in enumerate(imgs):
    src=im
    if im.endswith('.webp'):
        from PIL import Image; Image.open(im).convert('RGB').save(f'{T}/utv_title.png'); src=f'{T}/utv_title.png'
    o=f'{T}/u{i}.mp4';du=3.2 if i==0 else 2.8;still(src,du,540,960,o,zoom_in=i%2==0);cl.append(o);d.append(du)
join(cl,d,0.5,'/home/claude/up-the-village/assets/audio/music_theme.mp3',0,f'{OUT}/up-the-village.mp4',poster_t=1.2)

# From the Block: its intro slideshow, recorded; the top buttons cropped away. No sound (the game's music is synthesized live).
src=glob.glob(f'{T}/ftbvid/*.webm')[0]
segs=[(1.2,3.2),(6.3,3.2),(11.3,3.2),(16.3,3.2),(21.3,3.2),(26.3,3.2),(31.3,3.4)]
cl=[];d=[]
for i,(ss,du) in enumerate(segs):
    o=f'{T}/f{i}.mp4';norm(src,ss,du,540,888,o,crop='crop=450:740:0:60');cl.append(o);d.append(du)
join(cl,d,0.5,None,0,f'{OUT}/from-the-block.mp4')

# Huakaʻi: story art, 960x540, title music
SA='/home/claude/huakai/assets/story/'
imgs=[SA+'title.png',SA+'arrival.png',SA+'launch_2.png',SA+'kona_storm.png',SA+'gathering.png',SA+'end_card.png']
cl=[];d=[]
for i,im in enumerate(imgs):
    o=f'{T}/h{i}.mp4';du=3.0;still(im,du,960,540,o,zoom_in=i%2==0);cl.append(o);d.append(du)
mus='/home/claude/huakai/assets/audio/music/title.ogg'
if not os.path.exists(mus): mus='/home/claude/huakai/assets/audio/music/village.ogg'
join(cl,d,0.5,mus,0,f'{OUT}/huakai.mp4',poster_t=0.8)
