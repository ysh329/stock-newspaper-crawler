__author__ = 'yuens'

from myclass.class_create_databases import *

database_name = "essayDB"

a = CreateDatabaseClass()
a.create_database(database_name)
a.create_table(database_name)