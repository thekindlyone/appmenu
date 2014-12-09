from ConfigParser import RawConfigParser,NoOptionError
import os
import pickle

class Cache:
    def __init__(self):
        self.appdir='/usr/share/applications'       
        self.cachefile='appmenu_cache'
        self.parser=RawConfigParser()
        if not os.path.exists(self.cachefile):
            # print 'test'
            self.create_cache()
        

    def get_field(self,filename,field):      
        try:
            # print filename
            return self.parser.get('Desktop Entry',field)
        except NoOptionError:
            # print 'ding'
            return False


    def fetch_metadata(self,filename):
        print filename
        self.parser.read(os.path.join(self.appdir,filename))
        fields=['name','comment','icon','terminal','categories','exec']
        # print {field:get_field(filename,field) for field in fields}
        return {field:self.get_field(filename,field) for field in fields}

    def sortify(self,master_table):
        sorted_table={}
        for category,programs in master_table.iteritems():
            programs.sort(key=lambda program:program['name'])
            sorted_table[category]=programs
        return sorted_table

    def create_cache(self):
        # print os.listdir(self.appdir) 
        master_table={}
        dicts=(self.fetch_metadata(filename) for filename in os.listdir(self.appdir) 
               if os.path.splitext(filename)[-1]=='.desktop')
        # print list(dicts)
        for fields in dicts:
            # print fields
            categories=fields.get('categories')
            if categories:
                categories=filter(None,categories.split(';'))
            else:
                categories=['misc']
            for category in categories:
                print category
                # master_table[category]=master_table.get(category,[])+fields
                master_table.setdefault(category, []).append(fields)

        master_table=self.sortify(master_table)
        # print master_table
        with open(self.cachefile,'w') as f:
            pickle.dump(master_table,f)
        return master_table


    def load_cache(self):
        try:
            with open(self.cachefile) as f:
                master_table=pickle.load(f)
                print 'load success'
        except:
            return self.create_cache()

        return master_table

    def get_cache(self):
        return self.load_cache()


if __name__ == '__main__':
    cache=Cache()
    print cache.get_cache()










