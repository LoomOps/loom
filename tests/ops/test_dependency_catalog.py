import copy
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'ops'))
import dependency_catalog

class DependencyCatalogTests(unittest.TestCase):
    def runtime(self,identity='sim',revision=1,deps=None,**extra):
        return {'id':identity,'revision':revision,'manifest':{'runtime':{'image':'sha256:'+identity},
            'dependencies':deps or [{'name':'Python','version':'3.12','scope':'image'}]},**extra}

    def test_shared_versions_keep_each_image_and_scope_without_inventing_one_install(self):
        items=[self.runtime('a'),self.runtime('b'),self.runtime('c',deps=[{'name':'Python','version':'3.11','scope':'image'}])]
        before=copy.deepcopy(items);result=dependency_catalog.listing({'runtimes':items})['dependencies']
        self.assertEqual(len(result),1);item=result[0]
        self.assertEqual(item['category'],'languages');self.assertEqual([x['version'] for x in item['versions']],['3.11','3.12'])
        self.assertEqual(len(item['versions'][1]['installations']),2);self.assertEqual(len(item['runtimes']),3)
        self.assertEqual(items,before)

    def test_bulk_inventory_is_hidden_but_explicit_units_and_categories_survive(self):
        deps=[{'name':'package-'+str(i),'version':'1','scope':'image'} for i in range(995)]
        deps+=[{'name':'isaacsim','version':'6.0.1','scope':'image'},
               {'name':'my-solver','version':'2','catalog':True,'category':'simulation','origin':{'type':'managed-directory','path':'/chosen/dependencies/solver'}},
               {'name':'torch','version':'2.8','scope':'image'},
               {'name':'CUDA','version':'12.8','scope':'image'},
               {'name':'retired','version':'1','catalog':True,'deprecated':True}]
        rows=dependency_catalog.listing({'runtimes':[self.runtime(deps=deps)]})['dependencies']
        self.assertEqual({r['name'] for r in rows},{'isaacsim','my-solver','torch','cuda'})
        solver=next(r for r in rows if r['name']=='my-solver');self.assertEqual(solver['versions'][0]['installations'][0]['origin']['path'],'/chosen/dependencies/solver')

    def test_unknown_explicit_unit_is_library_and_unrecorded_path_stays_unrecorded(self):
        item=self.runtime(deps=[{'name':'custom','version':'1','catalog':True}])
        row=dependency_catalog.listing({'runtimes':[item]})['dependencies'][0]
        self.assertEqual(row['category'],'libraries');self.assertEqual(row['versions'][0]['installations'][0]['origin'],{'type':'unrecorded'})

    def test_current_observations_archive_and_history(self):
        old=self.runtime('observed',1,aliases=[],curation={},legacy=False)
        old['manifest']['reconciliation']={'runtime_id':'python'}
        new=self.runtime('observed',2,aliases=['python'])
        new['manifest']['reconciliation']={'runtime_id':'python'}
        archived=self.runtime('archived',curation={'state':'archived'})
        catalog={'runtimes':[old,new,archived]}
        self.assertEqual(len(dependency_catalog.listing(catalog)['dependencies'][0]['runtimes']),1)
        self.assertEqual(len(dependency_catalog.listing(catalog,history=True)['dependencies'][0]['runtimes']),3)

    def test_ambiguous_interpreter_versions_are_kept_instead_of_disappearing(self):
        item=self.runtime(deps=[{'name':'Python','version':'3.11','scope':'/sim'},
                                {'name':'Python','version':'3.12','scope':'/lab'}])
        unit=dependency_catalog.listing({'runtimes':[item]})['dependencies'][0]
        self.assertEqual(len(unit['versions']),2)


    def test_conflicting_display_categories_are_order_independent_and_legacy_metadata_is_safe(self):
        items=[self.runtime('a',deps=[{'name':'Python','version':'3.11','category':'libraries','origin':'legacy','scope':None}]),
               self.runtime('b',deps=[{'name':'Python','version':'3.12','category':'languages'}])]
        forward=dependency_catalog.listing({'runtimes':items})
        self.assertEqual(forward,dependency_catalog.listing({'runtimes':list(reversed(items))}))
        self.assertEqual(forward['dependencies'][0]['category'],'languages')
        self.assertEqual(forward['dependencies'][0]['versions'][0]['installations'][0]['origin'],{'type':'unrecorded'})
