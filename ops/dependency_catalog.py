"""Read-only, grant-scoped software units across Runtime observations.

An inventory package is not automatically a managed installation. Versions and
physical origins remain distinct; membership never proves scientific use.
"""
import hashlib
import re

CATEGORIES = {'languages':'Languages','simulation':'Simulation',
              'machine-learning':'Machine Learning','gpu':'GPU & Drivers',
              'libraries':'Libraries & Tools'}
FAMILIES = {
    'languages':{'python','isaac-python','pypy','node','nodejs','java','openjdk','rust','go','julia','r'},
    'simulation':{'isaacsim','isaac-sim','isaaclab','isaac-lab','mujoco','pybullet','gazebo','genesis'},
    'machine-learning':{'torch','pytorch','tensorflow','jax','jaxlib','lerobot','transformers','onnxruntime','onnxruntime-gpu'},
    'gpu':{'cuda','cuda-toolkit','cudnn','tensorrt','nvidia driver','nvidia-driver','cupy'},
}
LABELS = {'python':'Python','isaac-python':'Kit Python','isaacsim':'Isaac Sim',
          'isaac-sim':'Isaac Sim','isaaclab':'Isaac Lab','isaac-lab':'Isaac Lab',
          'torch':'PyTorch','pytorch':'PyTorch','cuda':'CUDA','cudnn':'cuDNN','lerobot':'LeRobot'}

def normalized(name):
    return re.sub(r'[-_.]+','-',name.strip().casefold())

def current(item,items):
    if item.get('curation',{}).get('state')=='archived':return False
    if item.get('legacy'):return True
    if item['manifest'].get('reconciliation'):return bool(item.get('aliases'))
    return not any(other['id']==item['id'] and (other.get('revision') or 0)>(item.get('revision') or 0) for other in items)

def listing(catalog,history=False):
    units={};items=catalog.get('runtimes',[])
    for item in items:
        active=current(item,items)
        if not active and not history:continue
        manifest=item['manifest'];selectors=item.get('primary_dependencies',manifest.get('primary_dependencies',[])) or []
        for dep in manifest.get('dependencies') or []:
            if not isinstance(dep,dict) or not all(isinstance(dep.get(k),str) and dep[k] for k in ('name','version')):continue
            if dep.get('catalog') is False or dep.get('deprecated'):continue
            name=normalized(dep['name']);category=dep.get('category')
            if not isinstance(category,str):category=None
            family=next((key for key,names in FAMILIES.items() if name in names),None)
            declared=dep.get('catalog') is True or category in CATEGORIES or any(
                normalized(s['name'])==name and ('scope' not in s or s['scope']==dep.get('scope')) for s in selectors)
            if not declared and not family:continue
            category=category if category in CATEGORIES else family or 'libraries'
            key='dependency-'+hashlib.sha256(name.encode()).hexdigest()[:24]
            unit=units.setdefault(key,{'id':key,'name':name,'label':LABELS.get(name,dep['name']),
                'category':category,'classifications':set(),'versions':{},'runtimes':{}})
            # Explicit classification takes precedence over a fallback suggestion.
            if category in CATEGORIES and dep.get('category')==category:unit['classifications'].add(category)
            ref={'id':item['id'],'revision':item.get('revision'),
                 'entity':'runtime:'+item['id']+':'+str(item.get('revision') or 'legacy'),
                 'label':item.get('curation',{}).get('label') or manifest.get('label',item['id']),
                 'current':active,'scope':dep.get('scope') if isinstance(dep.get('scope'),str) else ''}
            origin=dep.get('origin') if isinstance(dep.get('origin'),dict) else {}
            location={k:origin[k] for k in ('type','path') if isinstance(origin.get(k),str)}
            if not location:
                location={'type':'image'} if ref['scope'] in ('image','image-os','isaac-extension') else {'type':'unrecorded'}
            if location.get('type') in ('image','bundled-extension'):location['image']=manifest.get('runtime',{}).get('image')
            version=unit['versions'].setdefault(dep['version'],{'version':dep['version'],'installations':{}})
            marker=tuple(sorted(location.items()));install=version['installations'].setdefault(marker,{'origin':location,'runtimes':{}})
            refkey=(ref['entity'],ref['scope']);install['runtimes'][refkey]=ref;unit['runtimes'][ref['entity']]=ref
    result=[]
    for unit in units.values():
        explicit=sorted(unit.pop('classifications'),key=list(CATEGORIES).index)
        if explicit:unit['category']=explicit[0]
        unit['runtimes']=sorted(unit['runtimes'].values(),key=lambda r:r['entity'])
        versions=[]
        for version in unit['versions'].values():
            version['installations']=[{**i,'runtimes':sorted(i['runtimes'].values(),key=lambda r:(r['entity'],r['scope']))} for _,i in sorted(version['installations'].items(),key=lambda pair:str(pair[0]))]
            versions.append(version)
        unit['versions']=sorted(versions,key=lambda v:v['version']);result.append(unit)
    result.sort(key=lambda d:(list(CATEGORIES).index(d['category']),d['label'].casefold()))
    return {'status':catalog.get('status','ok'),'dependencies':result,
        'categories':[{'id':key,'label':label,'count':sum(d['category']==key for d in result)} for key,label in CATEGORIES.items()],
        **({'reason':catalog['reason']} if 'reason' in catalog else {}),
        'basis':'declared software units and representative installed metadata; no filesystem discovery or execution-use claim'}
