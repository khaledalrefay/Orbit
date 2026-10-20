"""Build the icon specimen data for brand/exploration/round-4/icons.html.

Usage: python3 -I brand/tools/build_icon_specimens.py <src> brand/exploration/round-4/icons-data.js
<src> holds the extracted npm tarballs (npm pack, then tar -xzf each into a folder named after the tarball):
lucide-static@1.50.0, @tabler/icons@3.48.0, @phosphor-icons/core@2.1.1, @material-symbols/svg-400@0.47.5.
Each concept lists candidate names per library; the first one found wins.
"""
import json, os, re, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
L = f'{SRC}/lucide-static-1.50.0/package/icons'
T = f'{SRC}/tabler-icons-3.48.0/package/icons'
P = f'{SRC}/phosphor-icons-core-2.1.1/package/assets'
M = f'{SRC}/material-symbols-svg-400-0.47.5/package/rounded'
# concept: (group, ar, lucide, tabler, phosphor, material) ; each a "|"-separated candidate list
C = [
 ('nav','today','اليوم','house','home','house','home'),
 ('nav','programs','البرامج','layout-grid','layout-grid','squares-four','grid_view'),
 ('nav','habits','العادات','square-check-big|square-check','square-check','check-square','check_box'),
 ('nav','focus','التركيز','timer','clock-hour-4|alarm','timer','timer'),
 ('nav','progress','التقدّم','chart-column|bar-chart-3','chart-bar','chart-bar','bar_chart'),
 ('ui','settings','الإعدادات','settings','settings','gear','settings'),
 ('ui','more','المزيد','ellipsis','dots','dots-three','more_horiz'),
 ('ui','add','إضافة','plus','plus','plus','add'),
 ('ui','close','إغلاق','x','x','x','close'),
 ('ui','back','رجوع','chevron-left','chevron-left','caret-left','chevron_left'),
 ('ui','play','بدء','play','player-play','play','play_arrow'),
 ('ui','pause','إيقاف','pause','player-pause','pause','pause'),
 ('ui','skip','تخطٍّ','skip-forward','player-skip-forward','skip-forward','skip_next'),
 ('ui','edit','تعديل','pencil','pencil','pencil-simple','edit'),
 ('ui','delete','حذف','trash-2','trash','trash','delete'),
 ('ui','bell','تذكير','bell','bell','bell','notifications'),
 ('ui','calendar','التقويم','calendar','calendar','calendar-blank','calendar_today'),
 ('ui','search','بحث','search','search','magnifying-glass','search'),
 ('ui','info','شرح','info','info-circle','info','info'),
 ('ui','archive','أرشفة','archive','archive','archive','archive'),
 ('ui','check','تم','check','check','check','check'),
 ('cat','stretch','تمدّد ومرونة','person-standing','stretching|stretching-2','person-simple-tai-chi','sports_gymnastics|self_improvement'),
 ('cat','strength','بناء وقوة','dumbbell','barbell','barbell','fitness_center'),
 ('cat','cardio','هوائي','activity','run','person-simple-run','directions_run'),
 ('cat','general','عام','shapes','category','shapes','category'),
 ('habit','water','ماء','droplet','droplet','drop','water_drop'),
 ('habit','read','قراءة','book-open','book','book-open','menu_book'),
 ('habit','sleep','نوم','moon','moon','moon','bedtime'),
 ('habit','bed','سرير','bed','bed','bed','bed'),
 ('habit','walk','مشي','footprints','walk','person-simple-walk','directions_walk'),
 ('habit','bike','دراجة','bike','bike','bicycle','directions_bike'),
 ('habit','swim','سباحة','waves','swimming','swimming-pool','pool'),
 ('habit','meditate','تأمّل','flower-2','yoga','flower-lotus','self_improvement'),
 ('habit','breathe','تنفّس','wind','wind','wind','air'),
 ('habit','stairs','درج','stairs|trending-up','stairs','stairs|steps','stairs'),
 ('habit','coffee','قهوة','coffee','coffee','coffee','coffee'),
 ('habit','veg','خضار','carrot','carrot','carrot','nutrition'),
 ('habit','salad','وجبة صحية','salad','salad','bowl-food','restaurant'),
 ('habit','pill','فيتامين','pill','pill','pill','pill'),
 ('habit','phone','الهاتف','smartphone','device-mobile-off','device-mobile-slash','mobile_off'),
 ('habit','eye','راحة العين','eye','eye','eye','visibility'),
 ('habit','sun','شمس','sun','sun','sun','light_mode'),
 ('habit','alarm','استيقاظ','alarm-clock','alarm','alarm','alarm'),
 ('habit','journal','يوميات','notebook-pen','notebook','notebook','edit_note'),
 ('habit','music','موسيقى','music','music','music-notes','music_note'),
 ('habit','language','لغة','languages','language','translate','translate'),
 ('habit','code','برمجة','code','code','code','code'),
 ('habit','laptop','عمل','laptop','device-laptop','laptop','laptop_mac|computer|laptop_chromebook'),
 ('habit','learn','تعلّم','brain','brain','brain','psychology'),
 ('habit','save','ادخار','piggy-bank','pig-money','piggy-bank','savings'),
 ('habit','clean','ترتيب','spray-can','spray','spray-bottle','cleaning_services'),
 ('habit','plant','نبات','sprout','plant','plant','potted_plant'),
 ('habit','pet','حيوان أليف','dog','dog','dog','pets'),
 ('habit','call','اتصال','phone','phone','phone','call'),
 ('habit','friends','أصدقاء','users','users','users','group'),
 ('habit','gratitude','امتنان','heart','heart','heart','favorite'),
 ('habit','mood','مزاج','smile','mood-smile','smiley','mood'),
 ('habit','smoke','بلا تدخين','cigarette-off','smoking-no','cigarette-slash','smoke_free'),
 ('habit','mosque','صلاة','mosque|moon-star','building-mosque','mosque','mosque'),
 ('habit','shower','استحمام','shower-head','bath','shower','shower'),
 ('habit','target','هدف','target','target','target','adjust'),
]
def rd(p):
    return open(p).read() if os.path.exists(p) else None
def inner(svg):
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    body = re.sub(r'(?s)^.*?<svg[^>]*>', '', svg); body = re.sub(r'</svg>\s*$', '', body.strip())
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    body = re.sub(r'<path stroke="none" d="M0 0h24v24H0z" fill="none"\s*/>', '', body)  # tabler bbox
    body = re.sub(r'<rect width="256" height="256" fill="none"\s*/>', '', body)  # phosphor bbox
    return vb, re.sub(r'\s+', ' ', body).strip()
def find(cands, fn):
    for n in cands.split('|'):
        s = fn(n)
        if s: return n, s
    return None, None
data = {'lucide': {}, 'tabler': {}, 'phosphor': {}, 'material': {}}
miss = []
for g, key, ar, lu, ta, ph, ma in C:
    n, s = find(lu, lambda n: rd(f'{L}/{n}.svg'))
    if s: data['lucide'][key] = {'n': n, 'o': inner(s)}
    else: miss.append(('lucide', key))
    n, s = find(ta, lambda n: rd(f'{T}/outline/{n}.svg'))
    if s:
        e = {'n': n, 'o': inner(s)}; f = rd(f'{T}/filled/{n}.svg')
        if f: e['f'] = inner(f)
        data['tabler'][key] = e
    else: miss.append(('tabler', key))
    n, s = find(ph, lambda n: rd(f'{P}/regular/{n}.svg'))
    if s:
        e = {'n': n, 'o': inner(s)}
        for w, suf in (('light', '-light'), ('bold', '-bold'), ('duotone', '-duotone'), ('fill', '-fill')):
            v = rd(f'{P}/{w}/{n}{suf}.svg')
            if v: e[w[0] if w != 'duotone' else 'd'] = inner(v)
        data['phosphor'][key] = e
    else: miss.append(('phosphor', key))
    n, s = find(ma, lambda n: rd(f'{M}/{n}.svg'))
    if s:
        e = {'n': n, 'o': inner(s)}; f = rd(f'{M}/{n}-fill.svg')
        if f: e['f'] = inner(f)
        data['material'][key] = e
    else: miss.append(('material', key))
counts = {
 'lucide': len(os.listdir(L)),
 'tabler': len(os.listdir(f'{T}/outline')),
 'phosphor': len(os.listdir(f'{P}/regular')),
 'material': len([f for f in os.listdir(M) if not f.endswith('-fill.svg')]),
}
concepts = [{'g': g, 'k': k, 'ar': ar} for g, k, ar, *_ in C]
js = '/* Generated by brand/tools/build_icon_specimens.py from the npm packages below. Icon data: Lucide 1.50.0 (ISC), Tabler 3.48.0 (MIT), Phosphor core 2.1.1 (MIT), Material Symbols Rounded 400 0.47.5 (Apache-2.0). */\n'
js += 'window.ICONS = ' + json.dumps({'concepts': concepts, 'counts': counts, 'lib': data}, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(OUT, 'w').write(js)
print('missing', miss); print(counts); print(os.path.getsize(OUT))
