import mysql.connector
import json
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS, cross_origin
import requests
import sys
import time
import webbrowser
import os

def getReports(val,Id):

   if val=="1":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1

       query = "SELECT idCorpus,entry from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

           
       for icd in crp_ids:

           if str(icd[0])==Id:
              query1 = "SELECT idDocument from document where idCorpus="+str(icd[0])
              l=[]
              
              cursor = conn.cursor()
              cursor.execute(query1)
              docs = cursor.fetchall()

              cursor.close()

              doc_ids=[]

              for x in docs:
                  query11 = "SELECT idDocument from documentmm where idDocument="+str(x[0])
              
                  cursor = conn.cursor()
                  cursor.execute(query11)
                  ds = cursor.fetchall()

                  for y in ds:
                      doc_ids.append(y)

                  cursor.close()

              if len(doc_ids)==0:
                  continue
              else:
                 data={}
                 data["idCorpus"]=icd[0]
                 data["corpusEntry"]=icd[1]
                 n=icd[1].split("_")
                 n.pop(0)
                 data["corpusName"]="_".join(n)
                 textFrames=[]
                 videoFrames=[]
                 

                 for id1 in doc_ids:
                  
                     
                     query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                     
                     cursor = conn.cursor()
                     cursor.execute(query2)
                     para_ids = cursor.fetchall()

                     cursor.close()

                     for id2 in para_ids:
                         query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
                         
                         cursor = conn.cursor()
                         cursor.execute(query3)
                         sent_ids = cursor.fetchall()

                         cursor.close()

                         for id3 in sent_ids:

                             query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query4)
                             fe_ids = cursor.fetchall()

                             feset_ids= set(fe_ids)

                             cursor.close()

                             feset=[]

                             if (None,) in feset_ids:
                                 feset_ids.remove((None,))

                             for id4 in feset_ids:

                                 query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                                 cursor = conn.cursor()
                                 cursor.execute(query5)
                                 fe = cursor.fetchall()

                                 feset.append(fe)

                                 cursor.close()

                             f_ids=[]

                             for id4 in feset_ids:
                                 query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                                 cursor = conn.cursor()
                                 cursor.execute(query6)
                                 f = cursor.fetchall()

                                 for x in f:
                                     f_ids.append(x)

                                 cursor.close()

                             fset_ids=set(f_ids)

                             fset=[]

                             for id4 in fset_ids:
                                 query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(id4[0])
                                 cursor = conn.cursor()
                                 cursor.execute(query7)
                                 f = cursor.fetchall()

                                 for x in f:
                                     fset.append(x)

                                 cursor.close()

                             fset=set(fset)

                             for x in fset:
                                d={}
                                d["idFrame"]=x[0]
                                d["frameEntry"]=x[1]
                                fn=x[1].split("_")
                                fn.pop(0)
                                d["frameName"]="_".join(fn)
                                textFrames.append(d)


                 doc_ids=[]

                 for x in docs:
                     query11 = "SELECT idDocument from documentmm where idDocument="+str(x[0])
                 
                     cursor = conn.cursor()
                     cursor.execute(query11)
                     ds = cursor.fetchall()

                     for y in ds:
                         doc_ids.append(y)

                     cursor.close()

                 if len(doc_ids)==0:
                     continue

                 val=0

                 l=[]
                 Feset=[]
                 Feset_ids=[]
                 Fset={}

                 for id1 in doc_ids:
                     
                     query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                     
                     cursor = conn.cursor()
                     cursor.execute(query2)
                     para_ids = cursor.fetchall()

                     cursor.close()

                     for id2 in para_ids:
                         query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
                         
                         cursor = conn.cursor()
                         cursor.execute(query3)
                         sent_ids = cursor.fetchall()

                         cursor.close()

                         smm_ids=[]

                         for id3 in sent_ids:

                             query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(id3[0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query41)
                             smm = cursor.fetchall()

                             smm_ids.append(smm[0])

                             cursor.close()


                         for id3 in smm_ids:

                             query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

                             cursor = conn.cursor()
                             cursor.execute(query42)
                             ann_id = cursor.fetchall()

                             cursor.close()

                             query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query4)
                             fe_ids = cursor.fetchall()

                             feset_ids= set(fe_ids)

                             cursor.close()

                             if (None,) in feset_ids:
                                 feset_ids.remove((None,))

                             
                             for x in feset_ids:
                                 Feset_ids.append(x)

                 Feset_ids=set(Feset_ids)

                 for id4 in Feset_ids:
                      query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query5)
                      fe = cursor.fetchall()

                      Feset.append(fe[0])

                      cursor.close()
                                 

                 Feset_ids=list(Feset_ids)

                 d1=dict.fromkeys(Feset_ids)
                 d2=dict.fromkeys(Feset)

                 F_ids=[]

                 for id4 in Feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      d1[id4]=f

                      cursor.close()


                      for x in f:
                          query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                          cursor = conn.cursor()
                          cursor.execute(query7)
                          f1 = cursor.fetchall()


                          if len(f1)!=0:
                             for x in f1:
                                d={}
                                d["idFrame"]=x[0]
                                d["frameEntry"]=x[1]
                                fn=x[1].split("_")
                                fn.pop(0)
                                d["frameName"]="_".join(fn)
                                videoFrames.append(d)

                          cursor.close()

                 data["textFrames"]=textFrames
                 data["videoFrames"]=videoFrames
                 djson["data"]=data
            
       conn.close()

       #with open('report1.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson
       

   elif val=="2":

           djson={}
           djson["reportNumber"]=val
           djson["reportTitle"]="Report "+val
           conn = mysql.connector.connect(
                    host="server2.framenetbr.ufjf.br",
                    user="fnbrasil",
                    password="OssracF1982",
                    database="webtool_db"
                   )
           v=1
                   

           query11= "SELECT idDocument,entry from document WHERE idDocument="+Id

           cursor = conn.cursor()
           cursor.execute(query11)
           d = cursor.fetchall()

           id1=d[0]

           data={}
           data["idDocument"]=id1[0]
           data["documentEntry"]=id1[1]
           n=id1[1].split("_")
           n.pop(0)
           data["documentName"]="_".join(n)
           textFrames=[]
           videoFrames=[]

           l=[]
           Fset=[]
        
           
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               for id3 in sent_ids:

                   query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query4)
                   fe_ids = cursor.fetchall()

                   feset_ids= set(fe_ids)

                   cursor.close()

                   feset=[]

                   if (None,) in feset_ids:
                       feset_ids.remove((None,))

                   for id4 in feset_ids:

                       query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                       cursor = conn.cursor()
                       cursor.execute(query5)
                       fe = cursor.fetchall()

                       feset.append(fe)

                       cursor.close()

                   f_ids=[]

                   for id4 in feset_ids:
                       query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                       cursor = conn.cursor()
                       cursor.execute(query6)
                       f = cursor.fetchall()

                       for x in f:
                           f_ids.append(x)

                       cursor.close()

                   fset_ids=set(f_ids)

                   fset=[]

                   for id4 in fset_ids:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(id4[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f = cursor.fetchall()

                       for x in f:
                           d={}
                           d["idFrame"]=x[0]
                           d["frameEntry"]=x[1]
                           fn=x[1].split("_")
                           fn.pop(0)
                           d["frameName"]="_".join(fn)
                           textFrames.append(d)

                       cursor.close()

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               smm_ids=[]

               for id3 in sent_ids:

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(id3[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   smm_ids.append(smm[0])

                   cursor.close()


               for id3 in smm_ids:

                   query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

                   cursor = conn.cursor()
                   cursor.execute(query42)
                   ann_id = cursor.fetchall()

                   cursor.close()

                   query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
            
                   cursor = conn.cursor()
                   cursor.execute(query4)
                   fe_ids = cursor.fetchall()

                   feset_ids= set(fe_ids)

                   cursor.close()

                   if (None,) in feset_ids:
                       feset_ids.remove((None,))

                   
                   for x in feset_ids:
                       Feset_ids.append(x)

           Feset_ids=set(Feset_ids)

           for id4 in Feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               Feset.append(fe[0])

               cursor.close()
                       

           Feset_ids=list(Feset_ids)

           d1=dict.fromkeys(Feset_ids)
           d2=dict.fromkeys(Feset)

           F_ids=[]
           Fset=[]

           for id4 in Feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()


                for x in f:
                    query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    if len(f1)!=0:
                       for x in f1:
                             d={}
                             d["idFrame"]=x[0]
                             d["frameEntry"]=x[1]
                             fn=x[1].split("_")
                             fn.pop(0)
                             d["frameName"]="_".join(fn)
                             videoFrames.append(d)

                    cursor.close()

                data["textFrames"]=textFrames
                data["videoFrames"]=videoFrames
                djson["data"]=data
            
           conn.close()

           #with open('report2.json', 'w') as fp:
             #json.dump(djson, fp, indent=4)

           return djson

   elif val=="3":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       s=[]
       s1=[]
       data=[]

       s1.append((int(Id),))
       
       query41= "SELECT idSentence FROM sentencemm WHERE idSentenceMM="+Id
            
       cursor = conn.cursor()
       cursor.execute(query41)
       smm = cursor.fetchall()

       cursor.close()
       s.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:
           query= "SELECT text FROM sentence WHERE idSentence="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query)
           txt = cursor.fetchall()

           cursor.close()
           
           d1={}
           d1["idSentence"]=d_buf[id3][0]
           d1["SentenceText"]=txt[0]
           textFrames=[]
           videoFrames=[]

           
           query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
           
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe)

               cursor.close()

               f_ids=[]

           for id4 in feset_ids:
               query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query6)
               f = cursor.fetchall()

               for x in f:
                   f_ids.append(x)

               cursor.close()

           fset_ids=set(f_ids)

           fset=[]

           for id4 in fset_ids:
                query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query7)
                f = cursor.fetchall()

                for x in f:
                   d2={}
                   d2["idFrame"]=x[0]
                   d2["frameEntry"]=x[1]
                   fn=x[1].split("_")
                   fn.pop(0)
                   d2["frameName"]="_".join(fn)
                   
                   textFrames.append(d2)

                cursor.close()

           d1["textFrames"]=textFrames


           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()


           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)


           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()
                f=set(f)

                cursor.close()

                for x in f:
                    query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    if len(f1)!=0:
                       for x in f1:
                          d2={}
                          d2["idFrame"]=x[0]
                          d2["frameEntry"]=x[1]
                          fn=x[1].split("_")
                          fn.pop(0)
                          d2["frameName"]="_".join(fn)
                         
                          videoFrames.append(d2)

                    cursor.close()

           d1["videoFrames"]=videoFrames

           data.append(d1)                    

       conn.close()

       djson["data"]=data

       #with open('report3.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson

   elif val=="4":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1

       query = "SELECT idCorpus,entry from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:

           if str(icd[0])==Id:
                
              query1 = "SELECT idDocument from document where idCorpus="+str(icd[0])
              l=[]
              
              cursor = conn.cursor()
              cursor.execute(query1)
              docs = cursor.fetchall()

              cursor.close()

              doc_ids=[]

              for x in docs:
                  query11 = "SELECT idDocument from documentmm where idDocument="+str(x[0])
              
                  cursor = conn.cursor()
                  cursor.execute(query11)
                  ds = cursor.fetchall()

                  for y in ds:
                      doc_ids.append(y)

                  cursor.close()

              if len(doc_ids)==0:
                  continue
              else:
                 data={}
                 data["idCorpus"]=icd[0]
                 data["corpusEntry"]=icd[1]
                 n=icd[1].split("_")
                 n.pop(0)
                 data["corpusName"]="_".join(n)
                 textFramesFE=[]
                 videoFramesFE=[]

                 val=0

                 l=[]
                 Feset=[]
                 Feset_ids=[]
                 Fset=[]

                 for id1 in doc_ids:
                     
                     query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                     
                     cursor = conn.cursor()
                     cursor.execute(query2)
                     para_ids = cursor.fetchall()

                     cursor.close()

                     for id2 in para_ids:
                         query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
                         
                         cursor = conn.cursor()
                         cursor.execute(query3)
                         sent_ids = cursor.fetchall()

                         cursor.close()

                         for id3 in sent_ids:

                             query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query4)
                             fe_ids = cursor.fetchall()

                             feset_ids= set(fe_ids)

                             cursor.close()

                             if (None,) in feset_ids:
                                 feset_ids.remove((None,))

                             
                             for x in feset_ids:
                                 Feset_ids.append(x)

                 Feset_ids=set(Feset_ids)

                 for id4 in Feset_ids:
                      query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query5)
                      fe = cursor.fetchall()

                      Feset.append(fe[0])

                      cursor.close()
                                 

                 Feset_ids=list(Feset_ids)

                 d1=dict.fromkeys(Feset_ids)
                 d2={}

                 F_ids=[]

                 for id4 in Feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      d1[id4]=f

                      cursor.close()

                      Fset=[]

                      for x in f:
                          query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                          cursor = conn.cursor()
                          cursor.execute(query7)
                          f1 = cursor.fetchall()

                          Fset.append(f1)
                          for x in f1:
                            d={}
                            d["idFrame"]=x[0]
                            d["frameEntry"]=x[1]
                            fn=x[1].split("_")
                            fn.pop(0)
                            d["frameName"]="_".join(fn)
                            fes=[]
                            query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                            cursor = conn.cursor()
                            cursor.execute(query71)
                            fe = cursor.fetchall()

                            for y in fe:
                               if (y[0],) in Feset_ids:
                                  d3={}
                                  d3["idFrameElement"]=y[0]
                                  d3["frameElementEntry"]=y[1]
                                  fn1=x[1].split("_")
                                  fn1.pop(0)
                                  d3["frameElementName"]="_".join(fn1)
                                  fes.append(d3)

                            cursor.close()
                                  
                            d["fes"]=fes
                            textFramesFE.append(d)

                          cursor.close()

                      if len(Fset)==0:
                          d2[Feset[Feset_ids.index(id4)][0]]=[]
                      else:
                          d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]

                 data["textFramesFE"]=textFramesFE
                   
              
                 val=0

                 l=[]
                 Feset=[]
                 Feset_ids=[]
                 Fset=[]

                 for id1 in doc_ids:
                     
                     query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                     
                     cursor = conn.cursor()
                     cursor.execute(query2)
                     para_ids = cursor.fetchall()

                     cursor.close()

                     for id2 in para_ids:
                         query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
                         
                         cursor = conn.cursor()
                         cursor.execute(query3)
                         sent_ids = cursor.fetchall()

                         cursor.close()

                         smm_ids=[]

                         for id3 in sent_ids:

                             query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(id3[0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query41)
                             smm = cursor.fetchall()

                             smm_ids.append(smm[0])

                             cursor.close()


                         for id3 in smm_ids:

                             query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

                             cursor = conn.cursor()
                             cursor.execute(query42)
                             ann_id = cursor.fetchall()

                             cursor.close()

                             query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query4)
                             fe_ids = cursor.fetchall()

                             feset_ids= set(fe_ids)

                             cursor.close()

                             if (None,) in feset_ids:
                                 feset_ids.remove((None,))

                             
                             for x in feset_ids:
                                 Feset_ids.append(x)

                 Feset_ids=set(Feset_ids)

                 for id4 in Feset_ids:
                      query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query5)
                      fe = cursor.fetchall()

                      Feset.append(fe[0])

                      cursor.close()
                                 

                 Feset_ids=list(Feset_ids)

                 F_ids=[]

                 for id4 in Feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()


                      cursor.close()

                      Fset=[]

                      for x1 in f:
                             query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x1[0])
                             cursor = conn.cursor()
                             cursor.execute(query7)
                             f1 = cursor.fetchall()

                             Fset.append(f1)
                             for x in f1:
                               d={}
                               d["idFrame"]=x[0]
                               d["frameEntry"]=x[1]
                               fn=x[1].split("_")
                               fn.pop(0)
                               d["frameName"]="_".join(fn)
                               fes=[]
                               query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                               cursor = conn.cursor()
                               cursor.execute(query71)
                               fe = cursor.fetchall()

                               for y in fe:
                                  if (y[0],) in Feset_ids:
                                     d3={}
                                     d3["idFrameElement"]=y[0]
                                     d3["frameElementEntry"]=y[1]
                                     fn1=x[1].split("_")
                                     fn1.pop(0)
                                     d3["frameElementName"]="_".join(fn1)
                                     fes.append(d3)

                               cursor.close()
                                     
                               d["fes"]=fes
                               videoFramesFE.append(d)
                      
                 data["videoFramesFE"]=videoFramesFE
                 djson["data"]=data
            
       conn.close()

       #with open('report4.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson



   elif val=="5":
           djson={}
           djson["reportNumber"]=val
           djson["reportTitle"]="Report "+val
           conn = mysql.connector.connect(
                    host="server2.framenetbr.ufjf.br",
                    user="fnbrasil",
                    password="OssracF1982",
                    database="webtool_db"
                   )
           v=1
                

           query11= "SELECT idDocument,entry from document WHERE idDocument="+Id

           cursor = conn.cursor()
           cursor.execute(query11)
           d = cursor.fetchall()

           id1=d[0]

           data={}
           data["idDocument"]=id1[0]
           data["documentEntry"]=id1[1]
           n=id1[1].split("_")
           n.pop(0)
           data["documentName"]="_".join(n)
           textFramesFE=[]
           videoFramesFE=[]
           Feset_ids=[]
           Feset=[]
           
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               for id3 in sent_ids:

                   query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query4)
                   fe_ids = cursor.fetchall()

                   feset_ids= set(fe_ids)

                   cursor.close()

                   if (None,) in feset_ids:
                       feset_ids.remove((None,))

                   
                   for x in feset_ids:
                       Feset_ids.append(x)

           Feset_ids=set(Feset_ids)

           for id4 in Feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               Feset.append(fe[0])

               cursor.close()
                       

           Feset_ids=list(Feset_ids)

           F_ids=[]

           for id4 in Feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                Fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       Fset.append(f1)
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         fes=[]
                         query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                         cursor = conn.cursor()
                         cursor.execute(query71)
                         fe = cursor.fetchall()

                         for y in fe:
                            if (y[0],) in Feset_ids:
                               d3={}
                               d3["idFrameElement"]=y[0]
                               d3["frameElementEntry"]=y[1]
                               fn1=x[1].split("_")
                               fn1.pop(0)
                               d3["frameElementName"]="_".join(fn1)
                               fes.append(d3)

                         cursor.close()
                               
                         d["fes"]=fes
                         textFramesFE.append(d)

                       cursor.close()
                   
                    

           data["textFramesFE"]=textFramesFE
            
       
           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               smm_ids=[]

               for id3 in sent_ids:

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(id3[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   smm_ids.append(smm[0])

                   cursor.close()


               for id3 in smm_ids:

                   query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

                   cursor = conn.cursor()
                   cursor.execute(query42)
                   ann_id = cursor.fetchall()

                   cursor.close()

                   query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
            
                   cursor = conn.cursor()
                   cursor.execute(query4)
                   fe_ids = cursor.fetchall()

                   feset_ids= set(fe_ids)

                   cursor.close()

                   if (None,) in feset_ids:
                       feset_ids.remove((None,))

                   
                   for x in feset_ids:
                       Feset_ids.append(x)

           Feset_ids=set(Feset_ids)

           for id4 in Feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               Feset.append(fe[0])

               cursor.close()
                       

           Feset_ids=list(Feset_ids)


           F_ids=[]

           for id4 in Feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()


                cursor.close()

                Fset=[]

                for x1 in f:
                          query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x1[0])
                          cursor = conn.cursor()
                          cursor.execute(query7)
                          f1 = cursor.fetchall()

                          Fset.append(f1)
                          for x in f1:
                            d={}
                            d["idFrame"]=x[0]
                            d["frameEntry"]=x[1]
                            fn=x[1].split("_")
                            fn.pop(0)
                            d["frameName"]="_".join(fn)
                            fes=[]
                            query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                            cursor = conn.cursor()
                            cursor.execute(query71)
                            fe = cursor.fetchall()

                            for y in fe:
                               if (y[0],) in Feset_ids:
                                  d3={}
                                  d3["idFrameElement"]=y[0]
                                  d3["frameElementEntry"]=y[1]
                                  fn1=x[1].split("_")
                                  fn1.pop(0)
                                  d3["frameElementName"]="_".join(fn1)
                                  fes.append(d3)

                            cursor.close()
                                  
                            d["fes"]=fes
                            videoFramesFE.append(d)

           data["videoFramesFE"]=videoFramesFE

      
           conn.close()

           djson["data"]=data

           #with open('report5.json', 'w') as fp:
              #json.dump(djson, fp, indent=4)

           return djson


   elif val=="6":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       
       conn = mysql.connector.connect(
                 host="server2.framenetbr.ufjf.br",
                 user="fnbrasil",
                 password="OssracF1982",
                 database="webtool_db")
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       s1=[]
       data=[]
       
       cursor.close()

       s1.append((int(Id),))
       
       query41= "SELECT idSentence FROM sentencemm WHERE idSentenceMM="+Id
            
       cursor = conn.cursor()
       cursor.execute(query41)
       smm = cursor.fetchall()

       cursor.close()
       s.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:
           query= "SELECT text FROM sentence WHERE idSentence="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query)
           txt = cursor.fetchall()

           cursor.close()
           
           d1={}
           d1["idSentence"]=d_buf[id3][0]
           d1["SentenceText"]=txt[0]
           textFramesFE=[]
           videoFramesFE=[]
           query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)


           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         fes=[]
                         query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                         cursor = conn.cursor()
                         cursor.execute(query71)
                         fe = cursor.fetchall()

                         for y in fe:
                            if (y[0],) in feset_ids:
                               d3={}
                               d3["idFrameElement"]=y[0]
                               d3["frameElementEntry"]=y[1]
                               fn1=x[1].split("_")
                               fn1.pop(0)
                               d3["frameElementName"]="_".join(fn1)
                               fes.append(d3)

                         cursor.close()
                               
                         d["fes"]=fes
                         textFramesFE.append(d)

                       cursor.close()

           d1["textFramesFE"]=textFramesFE      
            

           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()

           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)

           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         fes=[]
                         query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                         cursor = conn.cursor()
                         cursor.execute(query71)
                         fe = cursor.fetchall()

                         for y in fe:
                            if (y[0],) in feset_ids:
                               d3={}
                               d3["idFrameElement"]=y[0]
                               d3["frameElementEntry"]=y[1]
                               fn1=x[1].split("_")
                               fn1.pop(0)
                               d3["frameElementName"]="_".join(fn1)
                               fes.append(d3)

                         cursor.close()
                               
                         d["fes"]=fes
                         videoFramesFE.append(d)

                       cursor.close()

           d1["videoFramesFE"]=videoFramesFE
           data.append(d1)
     
       conn.close()
       djson["data"]=data

       #with open('report6.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson


   elif val=="7":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val

       
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1
       query = "SELECT idCorpus,entry from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

           
       for icd in crp_ids:
          
           if str(icd[0])==Id:
              query1 = "SELECT idDocument from document where idCorpus="+str(icd[0])
              l=[]
              
              cursor = conn.cursor()
              cursor.execute(query1)
              docs = cursor.fetchall()

              cursor.close()

              doc_ids=[]

              for x in docs:
                  query11 = "SELECT idDocument from documentmm where idDocument="+str(x[0])
              
                  cursor = conn.cursor()
                  cursor.execute(query11)
                  ds = cursor.fetchall()

                  for y in ds:
                      doc_ids.append(y)

                  cursor.close()

              if len(doc_ids)==0:
                  continue
              else:
                 data={}
                 data["idCorpus"]=icd[0]
                 data["corpusEntry"]=icd[1]
                 n=icd[1].split("_")
                 n.pop(0)
                 data["corpusName"]="_".join(n)
                 textFrames=[]
                 videoFrames=[]
                 docs=[]
                 

                 for x in doc_ids:
                   query11= "SELECT idDocument,entry from document WHERE idDocument="+str(x[0])

                   cursor = conn.cursor()
                   cursor.execute(query11)
                   d = cursor.fetchall()

                   for y in d:
                      docs.append(y)
                
                   cursor.close()

                 for id1 in docs:
                   
                    s=[]
                    s1=[]
                    query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                    
                    cursor = conn.cursor()
                    cursor.execute(query2)
                    para_ids = cursor.fetchall()

                    cursor.close()

                    for id2 in para_ids:
                        query3= "SELECT idSentence,text from sentence where idParagraph="+str(id2[0])
                        
                        cursor = conn.cursor()
                        cursor.execute(query3)
                        sent_ids = cursor.fetchall()

                        cursor.close()

                        for x in sent_ids:
                            s.append(x)

                            query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
                     
                            cursor = conn.cursor()
                            cursor.execute(query41)
                            smm = cursor.fetchall()

                            cursor.close()
                            s1.append(smm[0])

                    d_buf= dict(zip(s, s1))

                    for id3 in s:
                          query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                           
                          cursor = conn.cursor()
                          cursor.execute(query4)
                          fe_ids = cursor.fetchall()

                          feset_ids= set(fe_ids)

                          cursor.close()

                          feset=[]

                          if (None,) in feset_ids:
                              feset_ids.remove((None,))

                          for id4 in feset_ids:
                              query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                              cursor = conn.cursor()
                              cursor.execute(query5)
                              fe = cursor.fetchall()

                              feset.append(fe[0])

                              cursor.close()

                          feset_ids=list(feset_ids)


                          f_ids=[]
                          fset=[]

                          query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                          cursor = conn.cursor()
                          cursor.execute(query41)
                          ts = cursor.fetchall()

                          x=ts[0]
                                       
                          hms=x[0].split(":")
                                        
                          h=int(hms[0])
                          m=int(hms[1])
                          sl=hms[2].split(".")
                          secs=int(sl[0])+int(sl[1])/100
                          t1=h*3600+m*60+secs
                                        
                                        
                          hms=x[1].split(":")
                          h=int(hms[0])
                          m=int(hms[1])
                          sl=hms[2].split(".")
                          secs=int(sl[0])+int(sl[1])/100
                          t2=h*3600+m*60+secs

                          for id4 in feset_ids:
                               query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                               cursor = conn.cursor()
                               cursor.execute(query6)
                               f = cursor.fetchall()

                               cursor.close()

                               fset=[]

                               for x in f:
                                      query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                                      cursor = conn.cursor()
                                      cursor.execute(query7)
                                      f1 = cursor.fetchall()

                                      
                                      for x in f1:
                                        d={}
                                        d["idFrame"]=x[0]
                                        d["frameEntry"]=x[1]
                                        fn=x[1].split("_")
                                        fn.pop(0)
                                        d["frameName"]="_".join(fn)
                                        d["startTime"]=t1
                                        d["endTime"]=t2

                                        cursor.close()

                                        textFrames.append(d)

                                      cursor.close()     
                           

                          query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

                          cursor = conn.cursor()
                          cursor.execute(query42)
                          ann_id = cursor.fetchall()

                          cursor.close()

                          query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                           
                          cursor = conn.cursor()
                          cursor.execute(query4)
                          fe_ids = cursor.fetchall()

                          feset_ids= set(fe_ids)

                          cursor.close()

                          feset=[]

                          if (None,) in feset_ids:
                              feset_ids.remove((None,))

                          for id4 in feset_ids:
                              query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                              cursor = conn.cursor()
                              cursor.execute(query5)
                              fe = cursor.fetchall()

                              feset.append(fe[0])

                              cursor.close()

                          feset_ids=list(feset_ids)

                          f_ids=[]
                          fset=[]
                          start=[]
                          end=[]

                          query41= "SELECT startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                          cursor = conn.cursor()
                          cursor.execute(query41)
                          ts = cursor.fetchall()

                          for x in ts:
                             start.append(x[0])
                             end.append(x[1])

                          cursor.close()

                          for id4 in feset_ids:
                               query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                               cursor = conn.cursor()
                               cursor.execute(query6)
                               f = cursor.fetchall()

                               cursor.close()

                               fset=[]

                               for x in f:
                                      query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                                      cursor = conn.cursor()
                                      cursor.execute(query7)
                                      f1 = cursor.fetchall()

                                      
                                      for x in f1:
                                        d={}
                                        d["idFrame"]=x[0]
                                        d["frameEntry"]=x[1]
                                        fn=x[1].split("_")
                                        fn.pop(0)
                                        d["frameName"]="_".join(fn)
                                        d["startTime"]=start[fe_ids.index(id4)]*0.033
                                        d["endTime"]=end[fe_ids.index(id4)]*0.033
                                        

                                        cursor.close()
                                              
                                        videoFrames.append(d)

                                      cursor.close()

                 data["textFrames"]=textFrames
                 data["videoFrames"]=videoFrames
                 djson["data"]=data
     
       conn.close()


       #with open('report7.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson
       


   elif val=="8":
           djson={}
           djson["reportNumber"]=val
           djson["reportTitle"]="Report "+val

          
           conn = mysql.connector.connect(
                    host="server2.framenetbr.ufjf.br",
                    user="fnbrasil",
                    password="OssracF1982",
                    database="webtool_db"
                   )
           v=1
                   
           query1 = "SELECT idDocument from documentmm"
          
           cursor = conn.cursor()
           cursor.execute(query1)
           doc_ids = cursor.fetchall()
          
           cursor.close()
           docs=[]


           query11= "SELECT idDocument,entry from document WHERE idDocument="+Id

           cursor = conn.cursor()
           cursor.execute(query11)
           d = cursor.fetchall()

           id1=d[0]

           data={}
           data["idDocument"]=id1[0]
           data["documentEntry"]=id1[1]
           n=id1[1].split("_")
           n.pop(0)
           data["documentName"]="_".join(n)
           textFrames=[]
           videoFrames=[]
           Feset_ids=[]
           Feset=[]
          
           s=[]
           s1=[]
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence,text from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               for x in sent_ids:
                   s.append(x)

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s1.append(smm[0])

           d_buf= dict(zip(s, s1))

           for id3 in s:
                 query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                  
                 cursor = conn.cursor()
                 cursor.execute(query4)
                 fe_ids = cursor.fetchall()

                 feset_ids= set(fe_ids)

                 cursor.close()

                 feset=[]

                 if (None,) in feset_ids:
                     feset_ids.remove((None,))

                 for id4 in feset_ids:
                     query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                     cursor = conn.cursor()
                     cursor.execute(query5)
                     fe = cursor.fetchall()

                     feset.append(fe[0])

                     cursor.close()

                 feset_ids=list(feset_ids)


                 f_ids=[]
                 fset=[]

                 query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                 cursor = conn.cursor()
                 cursor.execute(query41)
                 ts = cursor.fetchall()

                 x=ts[0]
                              
                 hms=x[0].split(":")
                               
                 h=int(hms[0])
                 m=int(hms[1])
                 sl=hms[2].split(".")
                 secs=int(sl[0])+int(sl[1])/100
                 t1=h*3600+m*60+secs
                               
                               
                 hms=x[1].split(":")
                 h=int(hms[0])
                 m=int(hms[1])
                 sl=hms[2].split(".")
                 secs=int(sl[0])+int(sl[1])/100
                 t2=h*3600+m*60+secs

                 for id4 in feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      cursor.close()

                      fset=[]

                      for x in f:
                             query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                             cursor = conn.cursor()
                             cursor.execute(query7)
                             f1 = cursor.fetchall()

                             
                             for x in f1:
                               d={}
                               d["idFrame"]=x[0]
                               d["frameEntry"]=x[1]
                               fn=x[1].split("_")
                               fn.pop(0)
                               d["frameName"]="_".join(fn)
                               d["startTime"]=t1
                               d["endTime"]=t2

                               textFrames.append(d)

                             cursor.close()     
                  

                 query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

                 cursor = conn.cursor()
                 cursor.execute(query42)
                 ann_id = cursor.fetchall()

                 cursor.close()

                 query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                  
                 cursor = conn.cursor()
                 cursor.execute(query4)
                 fe_ids = cursor.fetchall()

                 feset_ids= set(fe_ids)

                 cursor.close()

                 feset=[]

                 if (None,) in feset_ids:
                     feset_ids.remove((None,))

                 for id4 in feset_ids:
                     query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                     cursor = conn.cursor()
                     cursor.execute(query5)
                     fe = cursor.fetchall()

                     feset.append(fe[0])

                     cursor.close()

                 feset_ids=list(feset_ids)

                 f_ids=[]
                 fset=[]
                 start=[]
                 end=[]

                 query41= "SELECT startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                 cursor = conn.cursor()
                 cursor.execute(query41)
                 ts = cursor.fetchall()

                 for x in ts:
                    start.append(x[0])
                    end.append(x[1])

                 cursor.close()

                 for id4 in feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      cursor.close()

                      fset=[]

                      for x in f:
                             query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                             cursor = conn.cursor()
                             cursor.execute(query7)
                             f1 = cursor.fetchall()

                             
                             for x in f1:
                               d={}
                               d["idFrame"]=x[0]
                               d["frameEntry"]=x[1]
                               fn=x[1].split("_")
                               fn.pop(0)
                               d["frameName"]="_".join(fn)
                               d["startTime"]=start[fe_ids.index(id4)]*0.033
                               d["endTime"]=end[fe_ids.index(id4)]*0.033

                               videoFrames.append(d)

                             cursor.close()

           data["textFrames"]=textFrames
           data["videoFrames"]=videoFrames
     
           conn.close()
           djson["data"]=data

           #with open('report8.json', 'w') as fp:
             #json.dump(djson, fp, indent=4)

           return djson
       


   elif val=="9":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       s1=[]
       data=[]
       
       cursor.close()

       s1.append((int(Id),))
       
       query41= "SELECT idSentence FROM sentencemm WHERE idSentenceMM="+Id
            
       cursor = conn.cursor()
       cursor.execute(query41)
       smm = cursor.fetchall()

       cursor.close()
       s.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:

           query= "SELECT text FROM sentence WHERE idSentence="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query)
           txt = cursor.fetchall()

           cursor.close()
           
           d1={}
           d1["idSentence"]=d_buf[id3][0]
           d1["SentenceText"]=txt[0]
           textFramesFE=[]
           videoFramesFE=[]
           query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)


           f_ids=[]
           fset=[]

           query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
           cursor = conn.cursor()
           cursor.execute(query41)
           ts = cursor.fetchall()

           x=ts[0]
                        
           hms=x[0].split(":")
                         
           h=int(hms[0])
           m=int(hms[1])
           sl=hms[2].split(".")
           secs=int(sl[0])+int(sl[1])/100
           t1=h*3600+m*60+secs
                         
                         
           hms=x[1].split(":")
           h=int(hms[0])
           m=int(hms[1])
           sl=hms[2].split(".")
           secs=int(sl[0])+int(sl[1])/100
           t2=h*3600+m*60+secs

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         d["startTime"]=t1
                         d["endTime"]=t2

                         cursor.close()
                               
                         textFramesFE.append(d)

                       cursor.close()

           d1["textFramesFE"]=textFramesFE      
            

           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()

           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)

           f_ids=[]
           fset=[]
           start=[]
           end=[]

           query41= "SELECT startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

           cursor = conn.cursor()
           cursor.execute(query41)
           ts = cursor.fetchall()

           for x in ts:
              start.append(x[0])
              end.append(x[1])

           cursor.close()

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         d["startTime"]=start[fe_ids.index(id4)]*0.033
                         d["endTime"]=end[fe_ids.index(id4)]*0.033
                         
                         videoFramesFE.append(d)

                       cursor.close()

           d1["videoFramesFE"]=videoFramesFE
           data.append(d1)
     
       conn.close()
       djson["data"]=data

       #with open('report9.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson


   elif val=="10":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val

       
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1
       query = "SELECT idCorpus,entry from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

           
       for icd in crp_ids:
           if str(icd[0])==Id:

              query1 = "SELECT idDocument from document where idCorpus="+str(icd[0])
              l=[]
              
              cursor = conn.cursor()
              cursor.execute(query1)
              docs = cursor.fetchall()

              cursor.close()

              doc_ids=[]

              for x in docs:
                  query11 = "SELECT idDocument from documentmm where idDocument="+str(x[0])
              
                  cursor = conn.cursor()
                  cursor.execute(query11)
                  ds = cursor.fetchall()

                  for y in ds:
                      doc_ids.append(y)

                  cursor.close()

              if len(doc_ids)==0:
                  continue
              else:
                 data={}
                 data["idCorpus"]=icd[0]
                 data["corpusEntry"]=icd[1]
                 n=icd[1].split("_")
                 n.pop(0)
                 data["corpusName"]="_".join(n)
                 textFramesFE=[]
                 videoFramesFE=[]
                 docs=[]
                 

                 for x in doc_ids:
                   query11= "SELECT idDocument,entry from document WHERE idDocument="+str(x[0])

                   cursor = conn.cursor()
                   cursor.execute(query11)
                   d = cursor.fetchall()

                   for y in d:
                      docs.append(y)
                
                   cursor.close()

                 for id1 in docs:
                   
                    s=[]
                    s1=[]
                    query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                    
                    cursor = conn.cursor()
                    cursor.execute(query2)
                    para_ids = cursor.fetchall()

                    cursor.close()

                    for id2 in para_ids:
                        query3= "SELECT idSentence,text from sentence where idParagraph="+str(id2[0])
                        
                        cursor = conn.cursor()
                        cursor.execute(query3)
                        sent_ids = cursor.fetchall()

                        cursor.close()

                        for x in sent_ids:
                            s.append(x)

                            query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
                     
                            cursor = conn.cursor()
                            cursor.execute(query41)
                            smm = cursor.fetchall()

                            cursor.close()
                            s1.append(smm[0])

                    d_buf= dict(zip(s, s1))

                    for id3 in s:
                          query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                           
                          cursor = conn.cursor()
                          cursor.execute(query4)
                          fe_ids = cursor.fetchall()

                          feset_ids= set(fe_ids)

                          cursor.close()

                          feset=[]

                          if (None,) in feset_ids:
                              feset_ids.remove((None,))

                          for id4 in feset_ids:
                              query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                              cursor = conn.cursor()
                              cursor.execute(query5)
                              fe = cursor.fetchall()

                              feset.append(fe[0])

                              cursor.close()

                          feset_ids=list(feset_ids)


                          f_ids=[]
                          fset=[]

                          query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                          cursor = conn.cursor()
                          cursor.execute(query41)
                          ts = cursor.fetchall()

                          x=ts[0]
                                       
                          hms=x[0].split(":")
                                        
                          h=int(hms[0])
                          m=int(hms[1])
                          sl=hms[2].split(".")
                          secs=int(sl[0])+int(sl[1])/100
                          t1=h*3600+m*60+secs
                                        
                                        
                          hms=x[1].split(":")
                          h=int(hms[0])
                          m=int(hms[1])
                          sl=hms[2].split(".")
                          secs=int(sl[0])+int(sl[1])/100
                          t2=h*3600+m*60+secs

                          for id4 in feset_ids:
                               query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                               cursor = conn.cursor()
                               cursor.execute(query6)
                               f = cursor.fetchall()

                               cursor.close()

                               fset=[]

                               for x in f:
                                      query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                                      cursor = conn.cursor()
                                      cursor.execute(query7)
                                      f1 = cursor.fetchall()

                                      
                                      for x in f1:
                                        d={}
                                        d["idFrame"]=x[0]
                                        d["frameEntry"]=x[1]
                                        fn=x[1].split("_")
                                        fn.pop(0)
                                        d["frameName"]="_".join(fn)
                                        fes=[]
                                        query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                                        cursor = conn.cursor()
                                        cursor.execute(query71)
                                        fe = cursor.fetchall()

                                        for y in fe:
                                           if (y[0],) in feset_ids:
                                              d3={}
                                              d3["idFrameElement"]=y[0]
                                              d3["frameElementEntry"]=y[1]
                                              fn1=x[1].split("_")
                                              fn1.pop(0)
                                              d3["frameElementName"]="_".join(fn1)
                                              d3["startTime"]=t1
                                              d3["endTime"]=t2
                                              fes.append(d3)

                                        cursor.close()
                                              
                                        d["fes"]=fes
                                        textFramesFE.append(d)

                                      cursor.close()     
                           

                          query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

                          cursor = conn.cursor()
                          cursor.execute(query42)
                          ann_id = cursor.fetchall()

                          cursor.close()

                          query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                           
                          cursor = conn.cursor()
                          cursor.execute(query4)
                          fe_ids = cursor.fetchall()

                          feset_ids= set(fe_ids)

                          cursor.close()

                          feset=[]

                          if (None,) in feset_ids:
                              feset_ids.remove((None,))

                          for id4 in feset_ids:
                              query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                              cursor = conn.cursor()
                              cursor.execute(query5)
                              fe = cursor.fetchall()

                              feset.append(fe[0])

                              cursor.close()

                          feset_ids=list(feset_ids)

                          f_ids=[]
                          fset=[]
                          start=[]
                          end=[]

                          query41= "SELECT startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                          cursor = conn.cursor()
                          cursor.execute(query41)
                          ts = cursor.fetchall()

                          for x in ts:
                             start.append(x[0])
                             end.append(x[1])

                          cursor.close()

                          for id4 in feset_ids:
                               query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                               cursor = conn.cursor()
                               cursor.execute(query6)
                               f = cursor.fetchall()

                               cursor.close()

                               fset=[]

                               for x in f:
                                      query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                                      cursor = conn.cursor()
                                      cursor.execute(query7)
                                      f1 = cursor.fetchall()

                                      
                                      for x in f1:
                                        d={}
                                        d["idFrame"]=x[0]
                                        d["frameEntry"]=x[1]
                                        fn=x[1].split("_")
                                        fn.pop(0)
                                        d["frameName"]="_".join(fn)
                                        fes=[]
                                        query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                                        cursor = conn.cursor()
                                        cursor.execute(query71)
                                        fe = cursor.fetchall()

                                        for y in fe:
                                           if (y[0],) in feset_ids:
                                              d3={}
                                              d3["idFrameElement"]=y[0]
                                              d3["frameElementEntry"]=y[1]
                                              fn1=x[1].split("_")
                                              fn1.pop(0)
                                              d3["frameElementName"]="_".join(fn1)
                                              d3["startTime"]=start[fe_ids.index(id4)]*0.033
                                              d3["endTime"]=end[fe_ids.index(id4)]*0.033
                                              fes.append(d3)

                                        cursor.close()
                                              
                                        d["fes"]=fes
                                        videoFramesFE.append(d)

                                      cursor.close()

                 data["textFramesFE"]=textFramesFE
                 data["videoFramesFE"]=videoFramesFE
                 djson["data"]=data
     
       conn.close()


       #with open('report10.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson

      

   elif val=="11":
           djson={}
           djson["reportNumber"]=val
           djson["reportTitle"]="Report "+val

       
           conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
           v=1
           query11= "SELECT idDocument,entry from document WHERE idDocument="+Id

           cursor = conn.cursor()
           cursor.execute(query11)
           d = cursor.fetchall()

           id1=d[0]

           data={}
           data["idDocument"]=id1[0]
           data["documentEntry"]=id1[1]
           n=id1[1].split("_")
           n.pop(0)
           data["documentName"]="_".join(n)
           textFramesFE=[]
           videoFramesFE=[]
           Feset_ids=[]
           Feset=[]
          
           s=[]
           s1=[]
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence,text from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               for x in sent_ids:
                   s.append(x)

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s1.append(smm[0])

           d_buf= dict(zip(s, s1))

           for id3 in s:
                 query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                  
                 cursor = conn.cursor()
                 cursor.execute(query4)
                 fe_ids = cursor.fetchall()

                 feset_ids= set(fe_ids)

                 cursor.close()

                 feset=[]

                 if (None,) in feset_ids:
                     feset_ids.remove((None,))

                 for id4 in feset_ids:
                     query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                     cursor = conn.cursor()
                     cursor.execute(query5)
                     fe = cursor.fetchall()

                     feset.append(fe[0])

                     cursor.close()

                 feset_ids=list(feset_ids)


                 f_ids=[]
                 fset=[]

                 query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                 cursor = conn.cursor()
                 cursor.execute(query41)
                 ts = cursor.fetchall()

                 x=ts[0]
                              
                 hms=x[0].split(":")
                               
                 h=int(hms[0])
                 m=int(hms[1])
                 sl=hms[2].split(".")
                 secs=int(sl[0])+int(sl[1])/100
                 t1=h*3600+m*60+secs
                               
                               
                 hms=x[1].split(":")
                 h=int(hms[0])
                 m=int(hms[1])
                 sl=hms[2].split(".")
                 secs=int(sl[0])+int(sl[1])/100
                 t2=h*3600+m*60+secs

                 for id4 in feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      cursor.close()

                      fset=[]

                      for x in f:
                             query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                             cursor = conn.cursor()
                             cursor.execute(query7)
                             f1 = cursor.fetchall()

                             
                             for x in f1:
                               d={}
                               d["idFrame"]=x[0]
                               d["frameEntry"]=x[1]
                               fn=x[1].split("_")
                               fn.pop(0)
                               d["frameName"]="_".join(fn)
                               fes=[]
                               query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                               cursor = conn.cursor()
                               cursor.execute(query71)
                               fe = cursor.fetchall()

                               for y in fe:
                                  if (y[0],) in feset_ids:
                                     d3={}
                                     d3["idFrameElement"]=y[0]
                                     d3["frameElementEntry"]=y[1]
                                     fn1=x[1].split("_")
                                     fn1.pop(0)
                                     d3["frameElementName"]="_".join(fn1)
                                     d3["startTime"]=t1
                                     d3["endTime"]=t2
                                     fes.append(d3)

                               cursor.close()
                                     
                               d["fes"]=fes
                               textFramesFE.append(d)

                             cursor.close()     
                  

                 query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

                 cursor = conn.cursor()
                 cursor.execute(query42)
                 ann_id = cursor.fetchall()

                 cursor.close()

                 query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                  
                 cursor = conn.cursor()
                 cursor.execute(query4)
                 fe_ids = cursor.fetchall()

                 feset_ids= set(fe_ids)

                 cursor.close()

                 feset=[]

                 if (None,) in feset_ids:
                     feset_ids.remove((None,))

                 for id4 in feset_ids:
                     query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                     cursor = conn.cursor()
                     cursor.execute(query5)
                     fe = cursor.fetchall()

                     feset.append(fe[0])

                     cursor.close()

                 feset_ids=list(feset_ids)

                 f_ids=[]
                 fset=[]
                 start=[]
                 end=[]

                 query41= "SELECT startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

                 cursor = conn.cursor()
                 cursor.execute(query41)
                 ts = cursor.fetchall()

                 for x in ts:
                    start.append(x[0])
                    end.append(x[1])

                 cursor.close()

                 for id4 in feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      cursor.close()

                      fset=[]

                      for x in f:
                             query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                             cursor = conn.cursor()
                             cursor.execute(query7)
                             f1 = cursor.fetchall()

                             
                             for x in f1:
                               d={}
                               d["idFrame"]=x[0]
                               d["frameEntry"]=x[1]
                               fn=x[1].split("_")
                               fn.pop(0)
                               d["frameName"]="_".join(fn)
                               fes=[]
                               query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                               cursor = conn.cursor()
                               cursor.execute(query71)
                               fe = cursor.fetchall()

                               for y in fe:
                                  if (y[0],) in feset_ids:
                                     d3={}
                                     d3["idFrameElement"]=y[0]
                                     d3["frameElementEntry"]=y[1]
                                     fn1=x[1].split("_")
                                     fn1.pop(0)
                                     d3["frameElementName"]="_".join(fn1)
                                     d3["startTime"]=start[fe_ids.index(id4)]*0.033
                                     d3["endTime"]=end[fe_ids.index(id4)]*0.033
                                     fes.append(d3)

                               cursor.close()
                                     
                               d["fes"]=fes
                               videoFramesFE.append(d)

                             cursor.close()

           data["textFramesFE"]=textFramesFE
           data["videoFramesFE"]=videoFramesFE
     
           conn.close()
           djson["data"]=data

           #with open('report11.json', 'w') as fp:
             #json.dump(djson, fp, indent=4)

           return djson



   elif val=="12":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1
                

       s=[]
       s1=[]
       data=[]


       s1.append((int(Id),))
       
       query41= "SELECT idSentence FROM sentencemm WHERE idSentenceMM="+Id
            
       cursor = conn.cursor()
       cursor.execute(query41)
       smm = cursor.fetchall()

       cursor.close()
       s.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:

           query= "SELECT text FROM sentence WHERE idSentence="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query)
           txt = cursor.fetchall()

           cursor.close()
           
           d1={}
           d1["idSentence"]=d_buf[id3][0]
           d1["SentenceText"]=txt[0]
           textFramesFE=[]
           videoFramesFE=[]
           query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)


           f_ids=[]
           fset=[]

           query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
           cursor = conn.cursor()
           cursor.execute(query41)
           ts = cursor.fetchall()

           x=ts[0]
                        
           hms=x[0].split(":")
                         
           h=int(hms[0])
           m=int(hms[1])
           sl=hms[2].split(".")
           secs=int(sl[0])+int(sl[1])/100
           t1=h*3600+m*60+secs
                         
                         
           hms=x[1].split(":")
           h=int(hms[0])
           m=int(hms[1])
           sl=hms[2].split(".")
           secs=int(sl[0])+int(sl[1])/100
           t2=h*3600+m*60+secs

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         fes=[]
                         query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                         cursor = conn.cursor()
                         cursor.execute(query71)
                         fe = cursor.fetchall()

                         for y in fe:
                            if (y[0],) in feset_ids:
                               d3={}
                               d3["idFrameElement"]=y[0]
                               d3["frameElementEntry"]=y[1]
                               fn1=x[1].split("_")
                               fn1.pop(0)
                               d3["frameElementName"]="_".join(fn1)
                               d3["startTime"]=t1
                               d3["endTime"]=t2
                               fes.append(d3)

                         cursor.close()
                               
                         d["fes"]=fes
                         textFramesFE.append(d)

                       cursor.close()

           d1["textFramesFE"]=textFramesFE      
            

           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()

           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)

           f_ids=[]
           fset=[]
           start=[]
           end=[]

           query41= "SELECT startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

           cursor = conn.cursor()
           cursor.execute(query41)
           ts = cursor.fetchall()

           for x in ts:
              start.append(x[0])
              end.append(x[1])

           cursor.close()

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       cursor.close()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         fes=[]
                         query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                         cursor = conn.cursor()
                         cursor.execute(query71)
                         fe = cursor.fetchall()

                         for y in fe:
                            if (y[0],) in feset_ids:
                               d3={}
                               d3["idFrameElement"]=y[0]
                               d3["frameElementEntry"]=y[1]
                               fn1=x[1].split("_")
                               fn1.pop(0)
                               d3["frameElementName"]="_".join(fn1)
                               d3["startTime"]=start[fe_ids.index(id4)]*0.033
                               d3["endTime"]=end[fe_ids.index(id4)]*0.033
                               fes.append(d3)

                         cursor.close()
                               
                         d["fes"]=fes
                         videoFramesFE.append(d)

           d1["videoFramesFE"]=videoFramesFE
           data.append(d1)
     
       conn.close()
       djson["data"]=data

       #with open('report12.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson
       

   elif val=="13":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1

       query = "SELECT idCorpus,entry from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:
           if str(icd[0])==Id:
                
              query1 = "SELECT idDocument from document where idCorpus="+str(icd[0])
              l=[]
              
              cursor = conn.cursor()
              cursor.execute(query1)
              docs = cursor.fetchall()

              cursor.close()

              doc_ids=[]

              for x in docs:
                  query11 = "SELECT idDocument from documentmm where idDocument="+str(x[0])
              
                  cursor = conn.cursor()
                  cursor.execute(query11)
                  ds = cursor.fetchall()

                  for y in ds:
                      doc_ids.append(y)

                  cursor.close()

              if len(doc_ids)==0:
                  continue
              else:
                 data={}
                 data["idCorpus"]=icd[0]
                 data["corpusEntry"]=icd[1]
                 n=icd[1].split("_")
                 n.pop(0)
                 data["corpusName"]="_".join(n)
                 videoFramesFE=[]

                 val=0

                 l=[]
                 Feset=[]
                 Feset_ids=[]
                 Fset=[]

                 for id1 in doc_ids:
                     
                     query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
                     
                     cursor = conn.cursor()
                     cursor.execute(query2)
                     para_ids = cursor.fetchall()

                     cursor.close()

                     for id2 in para_ids:
                         query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
                         
                         cursor = conn.cursor()
                         cursor.execute(query3)
                         sent_ids = cursor.fetchall()

                         cursor.close()

                         smm_ids=[]

                         for id3 in sent_ids:

                             query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(id3[0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query41)
                             smm = cursor.fetchall()

                             smm_ids.append(smm[0])

                             cursor.close()


                         for id3 in smm_ids:

                             query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

                             cursor = conn.cursor()
                             cursor.execute(query42)
                             ann_id = cursor.fetchall()

                             cursor.close()

                             query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                      
                             cursor = conn.cursor()
                             cursor.execute(query4)
                             fe_ids = cursor.fetchall()

                             feset_ids= set(fe_ids)

                             cursor.close()

                             if (None,) in feset_ids:
                                 feset_ids.remove((None,))

                             
                             for x in feset_ids:
                                 Feset_ids.append(x)

                 Feset_ids=set(Feset_ids)

                 for id4 in Feset_ids:
                      query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query5)
                      fe = cursor.fetchall()

                      Feset.append(fe[0])

                      cursor.close()
                                 

                 Feset_ids=list(Feset_ids)

                 d1=dict.fromkeys(Feset_ids)
                 d2={}

                 F_ids=[]

                 for id4 in Feset_ids:
                      query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                      cursor = conn.cursor()
                      cursor.execute(query6)
                      f = cursor.fetchall()

                      d1[id4]=f

                      cursor.close()

                      Fset=[]

                      for x in f:
                             query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x[0])
                             cursor = conn.cursor()
                             cursor.execute(query7)
                             f1 = cursor.fetchall()

                             Fset.append(f1)
                             for x in f1:
                               d={}
                               d["idFrame"]=x[0]
                               d["frameEntry"]=x[1]
                               fn=x[1].split("_")
                               fn.pop(0)
                               d["frameName"]="_".join(fn)
                               fes=[]
                               query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                               cursor = conn.cursor()
                               cursor.execute(query71)
                               fe = cursor.fetchall()

                               for y in fe:
                                  if (y[0],) in Feset_ids:
                                     d3={}
                                     d3["idFrameElement"]=y[0]
                                     d3["frameElementEntry"]=y[1]
                                     fn1=x[1].split("_")
                                     fn1.pop(0)
                                     d3["frameElementName"]="_".join(fn1)
                                     fes.append(d3)

                               cursor.close()
                                     
                               d["fes"]=fes
                               videoFramesFE.append(d)
                      
                 data["videoFramesFE"]=videoFramesFE
                 djson["data"]=data
           
            
       conn.close()


       #with open('report13.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson


   elif val=="14":
           djson={}
           djson["reportNumber"]=val
           djson["reportTitle"]="Report "+val
           conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                   )
           v=1

                
           query11= "SELECT idDocument,entry from document WHERE idDocument="+Id

           cursor = conn.cursor()
           cursor.execute(query11)
           d = cursor.fetchall()

           id1=d[0]

           data={}
           data["idDocument"]=id1[0]
           data["documentEntry"]=id1[1]
           n=id1[1].split("_")
           n.pop(0)
           data["documentName"]="_".join(n)
           textFramesFE=[]
           videoFramesFE=[]
           Feset_ids=[]
           Feset=[]
           
           query2= "SELECT idParagraph from paragraph where idDocument="+str(id1[0])
           
           cursor = conn.cursor()
           cursor.execute(query2)
           para_ids = cursor.fetchall()

           cursor.close()

           for id2 in para_ids:
               query3= "SELECT idSentence from sentence where idParagraph="+str(id2[0])
               
               cursor = conn.cursor()
               cursor.execute(query3)
               sent_ids = cursor.fetchall()

               cursor.close()

               smm_ids=[]

               for id3 in sent_ids:

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(id3[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   smm_ids.append(smm[0])

                   cursor.close()


               for id3 in smm_ids:

                   query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

                   cursor = conn.cursor()
                   cursor.execute(query42)
                   ann_id = cursor.fetchall()

                   cursor.close()

                   query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
            
                   cursor = conn.cursor()
                   cursor.execute(query4)
                   fe_ids = cursor.fetchall()

                   feset_ids= set(fe_ids)

                   cursor.close()

                   if (None,) in feset_ids:
                       feset_ids.remove((None,))

                   
                   for x in feset_ids:
                       Feset_ids.append(x)

           Feset_ids=set(Feset_ids)

           for id4 in Feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               Feset.append(fe[0])

               cursor.close()
                       

           Feset_ids=list(Feset_ids)

           F_ids=[]

           for id4 in Feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                Fset=[]

                for x1 in f:
                          query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x1[0])
                          cursor = conn.cursor()
                          cursor.execute(query7)
                          f1 = cursor.fetchall()

                          Fset.append(f1)
                          for x in f1:
                            d={}
                            d["idFrame"]=x[0]
                            d["frameEntry"]=x[1]
                            fn=x[1].split("_")
                            fn.pop(0)
                            d["frameName"]="_".join(fn)
                            fes=[]
                            query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                            cursor = conn.cursor()
                            cursor.execute(query71)
                            fe = cursor.fetchall()

                            for y in fe:
                               if (y[0],) in Feset_ids:
                                  d3={}
                                  d3["idFrameElement"]=y[0]
                                  d3["frameElementEntry"]=y[1]
                                  fn1=x[1].split("_")
                                  fn1.pop(0)
                                  d3["frameElementName"]="_".join(fn1)
                                  fes.append(d3)

                            cursor.close()
                                  
                            d["fes"]=fes
                            videoFramesFE.append(d)

           data["videoFramesFE"]=videoFramesFE


           djson["data"]=data
           conn.close()
           #with open('report14.json', 'w') as fp:
             #json.dump(djson, fp, indent=4)

           return djson

   elif val=="15":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
       )
       v=1

       s=[]
       s1=[]
       data=[]


       s1.append((int(Id),))
       
       query41= "SELECT idSentence FROM sentencemm WHERE idSentenceMM="+Id
            
       cursor = conn.cursor()
       cursor.execute(query41)
       smm = cursor.fetchall()

       cursor.close()
       s.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:

           query= "SELECT text FROM sentence WHERE idSentence="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query)
           txt = cursor.fetchall()

           cursor.close()
           
           d1={}
           d1["idSentence"]=d_buf[id3][0]
           d1["SentenceText"]=txt[0]
           textFramesFE=[]
           videoFramesFE=[]

           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(d_buf[id3][0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()

           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

            
           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()

           feset_ids= set(fe_ids)

           cursor.close()

           feset=[]

           if (None,) in feset_ids:
               feset_ids.remove((None,))

           for id4 in feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           feset_ids=list(feset_ids)

           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idFrame FROM `view_frameelement` WHERE idFrameElement="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                cursor.close()

                fset=[]

                for x1 in f:
                       query7= "SELECT idFrame,entry FROM frame WHERE idFrame="+str(x1[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f1 = cursor.fetchall()

                       
                       for x in f1:
                         d={}
                         d["idFrame"]=x[0]
                         d["frameEntry"]=x[1]
                         fn=x[1].split("_")
                         fn.pop(0)
                         d["frameName"]="_".join(fn)
                         fes=[]
                         query71= "SELECT idFrameElement,entry FROM `view_frameelement` WHERE idFrame="+str(x[0])
                         cursor = conn.cursor()
                         cursor.execute(query71)
                         fe = cursor.fetchall()

                         for y in fe:
                            if (y[0],) in feset_ids:
                               d3={}
                               d3["idFrameElement"]=y[0]
                               d3["frameElementEntry"]=y[1]
                               fn1=x[1].split("_")
                               fn1.pop(0)
                               d3["frameElementName"]="_".join(fn1)
                               fes.append(d3)

                         cursor.close()
                               
                         d["fes"]=fes
                         videoFramesFE.append(d)

                       cursor.close()

           d1["videoFramesFE"]=videoFramesFE
           data.append(d1)
     
       conn.close()
       djson["data"]=data                    
                
            
       conn.close()

       #with open('report15.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)

       return djson

   elif val=="16":
       djson={}
       djson["reportNumber"]=val
       djson["reportTitle"]="Report "+val
       conn = mysql.connector.connect(
              host="server2.framenetbr.ufjf.br",
              user="fnbrasil",
              password="OssracF1982",
              database="webtool_db"
                )
       v=1
                

       s=[]
       s1=[]
       data=[]


       s1.append((int(Id),))
       
       query41= "SELECT idSentence FROM sentencemm WHERE idSentenceMM="+Id
            
       cursor = conn.cursor()
       cursor.execute(query41)
       smm = cursor.fetchall()

       cursor.close()
       s.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:

          query= "SELECT text FROM sentence WHERE idSentence="+str(id3[0])

          cursor = conn.cursor()
          cursor.execute(query)
          txt = cursor.fetchall()

          cursor.close()
           
          d1={}
          d1["idSentence"]=d_buf[id3][0]
          d1["SentenceText"]=txt[0]
          textFramesFE=[]
          videoFramesFE=[]
          tern_qualia_rel={}
          query4= "SELECT DISTINCT idSubCorpus FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
 
          cursor = conn.cursor()
          cursor.execute(query4)
          sc = cursor.fetchall()

          cursor.close()

          for id4 in sc:
               query5= "SELECT idLU FROM `view_subcorpuslu` WHERE idSubCorpus="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               tlu = cursor.fetchall()

               cursor.close()

               query50= "SELECT name FROM `view_lu` WHERE idLU="+str(tlu[0][0])

               cursor = conn.cursor()
               cursor.execute(query50)
               tlu_name = cursor.fetchall()

               cursor.close()

               query53= "SELECT frameEntry FROM `view_lu` WHERE idLU="+str(tlu[0][0])

               cursor = conn.cursor()
               cursor.execute(query53)
               fr = cursor.fetchall()

               cursor.close()

               query51= "SELECT idFrame FROM `view_lu` WHERE idLU="+str(tlu[0][0])

               cursor = conn.cursor()
               cursor.execute(query51)
               frame = cursor.fetchall()

               cursor.close()

               query52 = "SELECT idLU FROM `view_lu` WHERE idFrame="+str(frame[0][0])

               cursor = conn.cursor()
               cursor.execute(query51)
               flus = cursor.fetchall()

               cursor.close()

               rels=[]

               for flu in flus:

                  query6= "SELECT lu2.idLU,r.idEntity3 FROM view_relation r"
                  query6= query6+" JOIN view_lu lu1 ON (r.idEntity1 = lu1.idEntity)"
                  query6= query6+" JOIN view_lu lu2 ON (r.idEntity2 = lu2.idEntity)"
                  query6= query6+" LEFT JOIN qualia q on (r.idEntity3 = q.idEntity)"
                  query6= query6+" LEFT JOIN view_relation rq on (q.idEntity = rq.idEntity1)"
                  query6= query6+" WHERE (lu1.idLU = \'"+str(tlu[0][0])+"\')"
                  query6= query6+" AND (r.relationGroup = 'rgp_qualia')"
                  query6= query6+" AND (rq.relationType = 'rel_qualia_frame')"
                  query6= query6+" AND (lu1.idLanguage = 1)"
                  query6= query6+" AND (lu2.idLanguage = 1)"
                  query6= query6+" UNION"
                  query6= query6+" SELECT lu1.idLU,r.idEntity3"
                  query6= query6+" FROM view_relation r"
                  query6= query6+" JOIN view_lu lu1 ON (r.idEntity1 = lu1.idEntity)"
                  query6= query6+" JOIN view_lu lu2 ON (r.idEntity2 = lu2.idEntity)"
                  query6= query6+" LEFT JOIN qualia q on (r.idEntity3 = q.idEntity)"
                  query6= query6+" LEFT JOIN view_relation rq on (q.idEntity = rq.idEntity1)"
                  query6= query6+" WHERE (lu2.idLU = \'"+str(flu[0])+"\')"
                  query6= query6+" AND (r.relationGroup = 'rgp_qualia')"
                  query6= query6+" AND (rq.relationType = 'rel_qualia_frame')"
                  query6= query6+" AND (lu1.idLanguage = 1)"
                  query6= query6+" AND (lu2.idLanguage = 1)"

                  cursor = conn.cursor()
                  cursor.execute(query6)
                  rel = cursor.fetchall()
                  

                  rel_names=[]

                  for r in rel:
                     
                     query60 = "SELECT name FROM `view_lu` WHERE idLU="+str(r[0])
                     cursor = conn.cursor()
                     cursor.execute(query60)
                     rel_name = cursor.fetchall()

                     
                     query61 = "SELECT info FROM qualia WHERE idEntity="+str(r[1])
                     cursor = conn.cursor()
                     cursor.execute(query61)
                     qr_name = cursor.fetchall()

                     if len(qr_name)==0:
                        d={}
                        d["Lexical Unit in Frame"]=rel_name[0][0]
                        d["Qualia Relation"]=''
                        rel_names.append(d)
                     else:
                        d={}
                        d["Lexical Unit in Frame"]=rel_name[0][0]
                        d["Qualia Relation"]=qr_name[0][0]
                        rel_names.append(d)

                  cursor.close()
               tern_qualia_rel["Lexical Unit in Sentence"]=tlu_name[0]
               tern_qualia_rel["Frame"]=fr[0][0]
               tern_qualia_rel["Relations to LUs"]=rel_names

          d1["Ternary_Qualia_Relations"]=tern_qualia_rel
               
          data.append(d1)
            
       conn.close()
       djson["data"]=data

       #with open('report16.json', 'w') as fp:
          #json.dump(djson, fp, indent=4)


       return djson
          

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False
cors = CORS(app)

@app.route('/report',methods=['POST','GET','OPTIONS'])
@cross_origin()
def getreport():
   val = request.json["val"]
   Id = request.json["Id"]
   print(val)
   print(Id)

   reports={}

   if val=="1":
      r1=getReports("1",Id)
      r2=getReports("4",Id)
      r3=getReports("7",Id)
      r4=getReports("10",Id)
      r5=getReports("13",Id)
      reports["1"]=r1
      reports["2"]=r2
      reports["3"]=r3
      reports["4"]=r4
      reports["5"]=r5
      
   elif val=="2":
      r1=getReports("2",Id)
      r2=getReports("5",Id)
      r3=getReports("8",Id)
      r4=getReports("11",Id)
      r5=getReports("14",Id)
      reports["1"]=r1
      reports["2"]=r2
      reports["3"]=r3
      reports["4"]=r4
      reports["5"]=r5
      
   elif val=="3":
      r1=getReports("3",Id)
      r2=getReports("6",Id)
      r3=getReports("9",Id)
      r4=getReports("12",Id)
      r5=getReports("15",Id)
      r6=getReports("16",Id)
      reports["1"]=r1
      reports["2"]=r2
      reports["3"]=r3
      reports["4"]=r4
      reports["5"]=r5
      reports["6"]=r6

   #print(reports)
   return jsonify(reports)   

if __name__=='__main__':
   app.run(debug=False, host='0.0.0.0')
       


