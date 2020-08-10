from flask import Flask, render_template, send_file
from flask import request
from io import BytesIO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import pickle
import sqlite3

app = Flask(__name__)


@app.route("/")
def default():
    renderpage = render_template("search.html")
    return renderpage

@app.route("/search")
def search():
    renderpage = render_template("search.html")
    return renderpage

@app.route("/result", methods=['POST'])
def result():
    conn = sqlite3.connect('kv.sqlite3')
    c = conn.cursor()
    G = nx.Graph()
    q = request.form['item']
    #q = "ヒト"
    c.execute("select * from entity where name='{}'".format(q))
    lst = c.fetchall()
    if len(lst)==0:
        return "この単語は登録されていません。こちらから登録情報を調べられます：https://www.wikidata.org/w/index.php?search=&search=&title=Special%3ASearch&go=Go"
    center = lst[0]#('Q5', '68', 'ヒト')
    G.add_node(center[2]) 

    c.execute("select * from triple where ent_head = "+center[1]+" or ent_tail="+center[1])
    lst = c.fetchall()
    for pair in lst[:100]:
        ent = pair[0]
        if ent==center[1]:
            ent=pair[1]
        c.execute("select * from entity where localid='{}'".format(ent))
        tmp = c.fetchall()
        if len(tmp)==0:
            continue
        node_name = tmp[0][2]
        G.add_node(node_name)
        G.add_edge(center[2], node_name)  

    plt.figure(figsize=(18,18))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw_networkx_labels(G, pos, fontsize=16, font_family="Yu Gothic", font_weight="bold")
    nx.draw_networkx(G,with_labels=False)
    
    img = BytesIO() # file-like object for the image
    plt.savefig(img) # save the image to the stream
    img.seek(0) # writing moved the cursor to the end of the file, reset
    plt.clf() # clear pyplot

    return send_file(img, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)