#!/usr/bin/env python
# coding: utf-8

# ## Qidと日本語名の対応付け
# Wikidataではすべてのエンティティ・関係にidが振ってあります。jsonファイルでデータを取得できるのですが使用しないデータが大量に記載されているため、必要なデータのみを取り出してデータベースに登録できる状態にします。<br>
# エンティティのidがQidです。
# 

# In[21]:


import time
import json
import requests
from tqdm.notebook import tqdm
import csv
csv.field_size_limit(1000000000)

import sqlite3
import csv
from tqdm.notebook import tqdm

conn = sqlite3.connect('kv.sqlite3')
c = conn.cursor()

c.execute("""CREATE TABLE entity
 (Qid CHAR(20) NOT NULL,
 localid CHAR(20) NOT NULL,
 name CHAR(200) NOT NULL);""")

c.execute("""CREATE TABLE relation
 (Pid CHAR(20) NOT NULL,
 localid CHAR(20) NOT NULL,
 name CHAR(200) NOT NULL);""")

c.execute("""CREATE TABLE triple
 (ent_head CHAR(20) NOT NULL,
 ent_tail CHAR(20) NOT NULL,
 rel CHAR(20) NOT NULL);""")

sql = 'insert into entity (Qid,localid,name) values (?,?,?)'
with open('entity2id_ja.csv', 'r',encoding="UTF-8") as f: 
    b = csv.reader(f)
    for t in tqdm(b):
        #print(t)
        c.execute(sql, tuple(t[:3]))

sql = 'insert into relation (Pid,localid,name) values (?,?,?)'
with open('relation2id_ja.csv', 'r',encoding="UTF-8") as f: 
    b = csv.reader(f)
    for t in tqdm(b):
        #print(t)
        c.execute(sql, tuple(t[:3]))

sql = 'insert into triple (ent_head,ent_tail,rel) values (?,?,?)'
with open('triple2id_graphize.csv', 'r',encoding="UTF-8") as f: 
    b = csv.reader(f)
    for t in tqdm(b):
        #print(t)
        c.execute(sql, tuple(t[:3]))

conn.commit()
c.close()
