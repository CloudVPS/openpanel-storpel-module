#!/usr/bin/env python
from OpenPanel import authd
from OpenPanel.modapi import panelmodule, panelclass
import sys, os, json

class Storpel(panelclass):
        def create(self, objectid, object, tree):
            model=tree['Storpel']['model']
            storpelid=tree['Storpel']['id']
            f = open(storpelid+'.storpel','w')
            f.write("Model %s\n" % model)
            f.write("Hostname %s\n" % storpelid)
            parentdom = tree['Domain']['id']
            for alias in tree['Domain'].get('Domain:Alias', dict()).keys():
                aliasdom = storpelid.replace(parentdom, alias)
                f.write("Alias %s\n" % aliasdom)
            for user,fields in tree['Storpel'].get('StorpelUser', dict()).items():
                f.write("User %s:%s\n" % (user, fields['password']))
            
            f.close()
            authd.do('installfile', storpelid+".storpel","/etc/storpels")
            authd.do('quit')

            return 'ok!'
        
        update = create

class StorpelUser(panelclass):
    def create(self, objectid, object, tree):
        Storpel(self.req).update(objectid, object, tree) # hack, modapi should make this easy

    update = create
    def delete(self, objectid, tree):
        Storpel(self.req).update(objectid, None, tree)

class StorpelModule(panelmodule):
    Storpel = Storpel
    StorpelUser = StorpelUser

StorpelModule().run()
