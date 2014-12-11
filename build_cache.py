import gmenu
import pickle
class Cache:
    def __init__(self):
        self.cachefile='appmenu_cache.p'
        self.cache=self.load_cache()
        if not self.cache:
            self.cache=self.create_cache()

    def create_cache(self): 
        tree=gmenu.lookup_tree('unity-lens-applications.menu')
        root=tree.get_root_directory()
        table={}
        for category in root.get_contents():
            apps=[]
            for program in category.get_contents():
                apps.append({'name':program.name,'icon':program.icon,'exec':program.get_desktop_file_path()})
            table[(category.name,category.icon)]=apps
        with open(self.cachefile,'w') as f:
            pickle.dump(table,f)
        return table

    def get_cache(self):
        return self.cache

    def load_cache(self):
        try:
            with open(self.cachefile) as f:
                cache=pickle.load(f)
            return cache
        except:
            return False

def main():
    cache=Cache()
    print cache.get_cache()

if __name__ == '__main__':
    main()

        
