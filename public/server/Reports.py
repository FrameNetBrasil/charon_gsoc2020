import mysql.connector
import json
from flask import Flask,render_template,request
from flask_cors import CORS
import requests
import sys
import time
import webbrowser
import os

def getReports(val):

   if val=="1":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:
                    
           query1 = "SELECT idDocument from document where idCorpus="+str(icd[0])
           l=[]
           Fset=[]
           
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
                           query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                           cursor = conn.cursor()
                           cursor.execute(query6)
                           f = cursor.fetchall()

                           for x in f:
                               f_ids.append(x)

                           cursor.close()

                       fset_ids=set(f_ids)

                       fset=[]

                       for id4 in fset_ids:
                           query7= "SELECT entry FROM frame WHERE idFrame="+str(id4[0])
                           cursor = conn.cursor()
                           cursor.execute(query7)
                           f = cursor.fetchall()

                           for x in f:
                               fset.append(x)

                           cursor.close()

                       fset=set(fset)

                       for x in fset:
                           Fset.append(x)

           Fset=set(Fset)
           Fset=list(Fset)
                           
           l.append(Fset)
           d[icd[0]]=l
           
       print(d)   
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       do={}

       for icd in crp_ids:
                
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
           d2=dict.fromkeys(Feset)

           F_ids=[]

           for id4 in Feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()


                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    if len(f1)!=0:
                       Fset.append(f1[0])

                    cursor.close()

           Fset=set(Fset)
           Fset=list(Fset)
           do[icd[0]]=Fset
       print("\n")
       print(do)
           
            
       conn.close()

       with open('report1.json', 'w') as fp:
          json.dump(d, fp)

       with open('report1.json', 'a') as fp:
          json.dump(do, fp)

   elif val=="2":

       print("I am here.")
       
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       d={}

       for id1 in doc_ids:

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
                       query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                       cursor = conn.cursor()
                       cursor.execute(query6)
                       f = cursor.fetchall()

                       for x in f:
                           f_ids.append(x)

                       cursor.close()

                   fset_ids=set(f_ids)

                   fset=[]

                   for id4 in fset_ids:
                       query7= "SELECT entry FROM frame WHERE idFrame="+str(id4[0])
                       cursor = conn.cursor()
                       cursor.execute(query7)
                       f = cursor.fetchall()

                       for x in f:
                           fset.append(x)

                       cursor.close()

                   fset=set(fset)

                   for x in fset:
                       Fset.append(x)

           Fset=set(Fset)
           Fset=list(Fset)
                       
           l.append(Fset)
           d[id1[0]]=l

            
       print(d)
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       do={}

       val=0

       for id1 in doc_ids:

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()


                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    if len(f1)!=0:
                       Fset.append(f1[0])

                    cursor.close()

           Fset=set(Fset)
           Fset=list(Fset)
           do[id1[0]]=Fset
           
       print("\n")
       print(do)
       conn.close()

       with open('report2.json', 'w') as fp:
          json.dump(d, fp)

       with open('report2.json', 'a') as fp:
          json.dump(do, fp)

   elif val=="3":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       s=[]
       s1=[]

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

               for x in sent_ids:
                   s.append(x)
                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s1.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

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

               feset.append(fe)

               cursor.close()

               f_ids=[]

           for id4 in feset_ids:
               query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query6)
               f = cursor.fetchall()

               for x in f:
                   f_ids.append(x)

               cursor.close()

           fset_ids=set(f_ids)

           fset=[]

           for id4 in fset_ids:
                query7= "SELECT entry FROM frame WHERE idFrame="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query7)
                f = cursor.fetchall()

                for x in f:
                    fset.append(x)

                cursor.close()

           fset=set(fset)

           fset=list(fset)

           l=[]
           l.append(fset)

           d[d_buf[id3][0]]=l
       
       print("\n")
       print(d)
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       
       cursor.close()

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

               for x in sent_ids:
                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s.append(smm[0])

       do={}
       
       for id3 in s:

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

           d1=dict.fromkeys(feset_ids)
           d2=dict.fromkeys(feset)

           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()
                f=set(f)

                d1[id4]=f

                cursor.close()

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    if len(f1)!=0:
                       fset.append(f1[0])

                    cursor.close()

           if len(fset)==0:
              fset=[]
           else:
              fset=set(fset)

           fset=list(fset)
           do[id3[0]]=fset
       print("\n")
       print(do)
            
       conn.close()

       with open('report3.json', 'w') as fp:
          json.dump(d, fp)

       with open('report3.json', 'a') as fp:
          json.dump(do, fp)

   elif val=="4":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:
                
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=[]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]

           d[icd[0]]=d2
       print("\n")
       print(d)
           
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       do={}

       for icd in crp_ids:
                
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=[]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]
           do[icd[0]]=d2
       print("\n")
       print(do)
           
            
       conn.close()

       with open('report4.json', 'w') as fp:
          json.dump(d, fp)

       with open('report4.json', 'a') as fp:
          json.dump(do, fp)


   elif val=="5":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       d={}

       val=0

       for id1 in doc_ids:

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=[]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]

           d[id1[0]]=d2
       print("\n")
       print(d)
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       do={}

       val=0

       for id1 in doc_ids:

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
           d2={}

           F_ids=[]

           for id4 in Feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=[]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]
           do[id1[0]]=d2
           
       print("\n")
       print(do)
       conn.close()

       with open('report5.json', 'w') as fp:
          json.dump(d, fp)

       with open('report5.json', 'a') as fp:
          json.dump(do, fp)

   elif val=="6":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       s1=[]
       
       cursor.close()

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

               for x in sent_ids:
                   s.append(x)

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s1.append(smm[0])

       d_buf= dict(zip(s, s1))
       d={}

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

           d1=dict.fromkeys(feset_ids)
           d2={}

           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[feset_ids.index(id4)][0]]=[]
                else:
                    d2[feset[feset_ids.index(id4)][0]]=fset[0]

           d[d_buf[id3][0]]=d2
       print("\n")
       print(d)
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       
       cursor.close()

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

               for x in sent_ids:
                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s.append(smm[0])

       do={}

       for id3 in s:

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

           d1=dict.fromkeys(feset_ids)
           d2={}

           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[feset_ids.index(id4)][0]]=[]
                else:
                    d2[feset[feset_ids.index(id4)][0]]=fset[0]

           do[id3[0]]=d2
       print("\n")
       print(do)
            
       conn.close()

       with open('report6.json', 'w') as fp:
          json.dump(d, fp)

       with open('report6.json', 'a') as fp:
          json.dump(do, fp)

   elif val=="7":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:
                
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

           val=0

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           start=[]
           end=[]

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
                      query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                
                      cursor = conn.cursor()
                      cursor.execute(query41)
                      smm = cursor.fetchall()

                      x=smm[0]
                        
                      hms=x[0].split(":")
                         
                      h=int(hms[0])
                      m=int(hms[1])
                      sl=hms[2].split(".")
                      s=int(sl[0])+int(sl[1])/100
                      t1=h*3600+m*60+s
                         
                         
                      hms=x[1].split(":")
                      h=int(hms[0])
                      m=int(hms[1])
                      sl=hms[2].split(".")
                      s=int(sl[0])+int(sl[1])/100
                      t2=h*3600+m*60+s

                      cursor.close()
                      

                      query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                
                      cursor = conn.cursor()
                      cursor.execute(query4)
                      fe_ids = cursor.fetchall()


                      fes=[value for value in fe_ids if value != (None,)]

                       
                      for x in fes:
                           Feset_ids.append(x)
                           start.append(t1)
                           end.append(t2)

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]

           d[icd[0]]=d2
           
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       do={}

       for icd in crp_ids:
                
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

           val=0

           l=[]
           Feset=[]
           Feset_ids=[]
           start=[]
           end=[]
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

                       query4= "SELECT idFrameElement,startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                
                       cursor = conn.cursor()
                       cursor.execute(query4)
                       fe_ids = cursor.fetchall()

                       cursor.close()

                       
                       for x in fe_ids:
                           Feset_ids.append(x[0])

                       for x in fe_ids:
                          start.append(x[1]*0.033)
                          end.append(x[2]*0.033)

           for id4 in Feset_ids:
                query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4)
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4)
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
           do[icd]=d2
           
       conn.close()

       l=list(d.values())
       l1=list(do.values())
       x=l[0]
       y=l1[0]
       lx=list(x.keys())
       ly=list(y.keys())
       
       k=list(do.keys())
       dmain={}
       lfr=[]
       for a_fe in lx:
          if x[a_fe][0] not in lfr:
             lfr.append(x[a_fe][0])

       lfr.remove('')
       lfr.remove([])

       lr=[]
       for z in lfr:
          lr.append(z[0][0])


       df=dict.fromkeys(lr)

       for z in df.keys():
          df[z]=[]

       for a_fe in lx:
          if a_fe in ly:
             for fr in lr:
                il=[]
                il.append((fr,))
                if '' not in x[a_fe]:
                   if il in x[a_fe]:
                      df[fr].append([[x[a_fe][1],x[a_fe][2]],[y[a_fe][1],y[a_fe][2]]])

       dmain[k[0][0]]=df
       print(dmain)

       with open('report7.json', 'w') as fp:
          json.dump(dmain, fp)


   elif val=="8":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       d={}

       val=0

       for id1 in doc_ids:

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           start=[]
           end=[]
           
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
                  query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                  cursor = conn.cursor()
                  cursor.execute(query41)
                  smm = cursor.fetchall()

                  x=smm[0]
                        
                  hms=x[0].split(":")
                         
                  h=int(hms[0])
                  m=int(hms[1])
                  sl=hms[2].split(".")
                  s=int(sl[0])+int(sl[1])/100
                  t1=h*3600+m*60+s
                         
                         
                  hms=x[1].split(":")
                  h=int(hms[0])
                  m=int(hms[1])
                  sl=hms[2].split(".")
                  s=int(sl[0])+int(sl[1])/100
                  t2=h*3600+m*60+s

                  cursor.close()
                      

                  query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                
                  cursor = conn.cursor()
                  cursor.execute(query4)
                  fe_ids = cursor.fetchall()


                  fes=[value for value in fe_ids if value != (None,)]

                       
                  for x in fes:
                     Feset_ids.append(x)
                     start.append(t1)
                     end.append(t2)

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]

           d[id1[0]]=d2
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       do={}

       val=0

       for id1 in doc_ids:

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           start=[]
           end=[]
           
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

                  query4= "SELECT idFrameElement,startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                
                  cursor = conn.cursor()
                  cursor.execute(query4)
                  fe_ids = cursor.fetchall()

                  cursor.close()

                       
                  for x in fe_ids:
                     Feset_ids.append(x[0])

                  for x in fe_ids:
                     start.append(x[1]*0.033)
                     end.append(x[2]*0.033)

           Feset_ids=set(Feset_ids)

           for id4 in Feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4)
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4)
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
           do[id1[0]]=d2
           
       conn.close()

       l=list(d.values())
       l1=list(do.values())
       x=l[0]
       y=l1[0]
       lx=list(x.keys())
       ly=list(y.keys())
       
       k=list(do.keys())
       dmain={}
       lfr=[]
       for a_fe in lx:
          if x[a_fe][0] not in lfr:
             lfr.append(x[a_fe][0])

       lfr.remove('')
       lfr.remove([])

       lr=[]
       for z in lfr:
          lr.append(z[0][0])


       df=dict.fromkeys(lr)

       for z in df.keys():
          df[z]=[]

       for a_fe in lx:
          if a_fe in ly:
             for fr in lr:
                il=[]
                il.append((fr,))
                if '' not in x[a_fe]:
                   if il in x[a_fe]:
                      df[fr].append([[x[a_fe][1],x[a_fe][2]],[y[a_fe][1],y[a_fe][2]]])

       dmain[k[0]]=df
       print(dmain)
       with open('report8.json', 'w') as fp:
          json.dump(dmain, fp)


   elif val=="9":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       s1=[]
       
       cursor.close()

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

               for y in sent_ids:
                   s.append(y)

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(y[0])
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s1.append(smm[0])
                   

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:

           smm=d_buf[id3]
           
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

           d1=dict.fromkeys(feset_ids)
           d2={}

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[feset_ids.index(id4)][0]]=[[],t1,t2]
                else:
                    d2[feset[feset_ids.index(id4)][0]]=[fset[0],t1,t2]

           d[d_buf[id3][0]]=d2
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       
       cursor.close()

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

               for x in sent_ids:
                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s.append(smm[0])

       do={}


       for id3 in s:

           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()

           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()


           cursor.close()

           feset=[]

           

           for id4 in fe_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           fe_ids=list(fe_ids)

           d1=dict.fromkeys(fe_ids)
           d2={}

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

           for id4 in fe_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[fe_ids.index(id4)][0]]=[[],start[fe_ids.index(id4)]*0.033,end[fe_ids.index(id4)]*0.033]
                else:
                    d2[feset[fe_ids.index(id4)][0]]=[fset[0],start[fe_ids.index(id4)]*0.033,end[fe_ids.index(id4)]*0.033]

           do[id3[0]]=d2
            
       conn.close()

       l=list(d.values())
       l1=list(do.values())

       df=[]

       for x in l:
          lx=list(x.keys())
          y=l1[l.index(x)]
          ly=list(y.keys())


          lfr=[]
          for z in lx:
             if z in ly:
                if x[z][0] not in lfr:
                   lfr.append(x[z][0])

          if [] in lfr:
             lfr.remove([])

          lr=[]
          for z in lfr:
             lr.append(z[0][0])

          fd=dict.fromkeys(lr)
          for f in fd.keys():
             fd[f]=[]

             
          for z in lx:
             if z in ly:
                if x[z][0] in lfr:
                   a=x[z][0]
                   fd[a[0][0]].append([[x[z][1],x[z][2]],[y[z][1],y[z][2]]])
          df.append(fd)
       
       dmain=dict(zip(list(do.keys()),df))
          
       print(dmain)
       with open('report9.json', 'w') as fp:
          json.dump(dmain, fp)


   elif val=="10":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:
                
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

           val=0

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           start=[]
           end=[]

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
                      query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                
                      cursor = conn.cursor()
                      cursor.execute(query41)
                      smm = cursor.fetchall()

                      x=smm[0]
                        
                      hms=x[0].split(":")
                         
                      h=int(hms[0])
                      m=int(hms[1])
                      sl=hms[2].split(".")
                      s=int(sl[0])+int(sl[1])/100
                      t1=h*3600+m*60+s
                         
                         
                      hms=x[1].split(":")
                      h=int(hms[0])
                      m=int(hms[1])
                      sl=hms[2].split(".")
                      s=int(sl[0])+int(sl[1])/100
                      t2=h*3600+m*60+s

                      cursor.close()
                      

                      query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                
                      cursor = conn.cursor()
                      cursor.execute(query4)
                      fe_ids = cursor.fetchall()


                      fes=[value for value in fe_ids if value != (None,)]

                       
                      for x in fes:
                           Feset_ids.append(x)
                           start.append(t1)
                           end.append(t2)

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]

           d[icd[0]]=d2
           
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       do={}

       for icd in crp_ids:
                
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

           val=0

           l=[]
           Feset=[]
           Feset_ids=[]
           start=[]
           end=[]
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

                       query4= "SELECT idFrameElement,startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                
                       cursor = conn.cursor()
                       cursor.execute(query4)
                       fe_ids = cursor.fetchall()

                       cursor.close()

                       
                       for x in fe_ids:
                           Feset_ids.append(x[0])

                       for x in fe_ids:
                          start.append(x[1]*0.033)
                          end.append(x[2]*0.033)

           for id4 in Feset_ids:
                query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4)
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4)
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
           do[icd[0]]=d2
           
       conn.close()

       l=list(d.values())
       l1=list(do.values())
       x=l[0]
       y=l1[0]
       lx=list(x.keys())
       ly=list(y.keys())
       df={}
       k=list(do.keys())
       dmain={}
       for a_fe in lx:
          if a_fe in ly:
             df[a_fe]=[x[a_fe],y[a_fe]]

       dmain[k[0]]=df
       print(dmain)
       with open('report10.json', 'w') as fp:
          json.dump(dmain, fp)

   elif val=="11":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       d={}

       val=0

       for id1 in doc_ids:

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           start=[]
           end=[]
           
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
                  query41= "SELECT startTimestamp,endTimestamp FROM sentencemm WHERE idSentence="+str(id3[0])
                  cursor = conn.cursor()
                  cursor.execute(query41)
                  smm = cursor.fetchall()

                  x=smm[0]
                        
                  hms=x[0].split(":")
                         
                  h=int(hms[0])
                  m=int(hms[1])
                  sl=hms[2].split(".")
                  s=int(sl[0])+int(sl[1])/100
                  t1=h*3600+m*60+s
                         
                         
                  hms=x[1].split(":")
                  h=int(hms[0])
                  m=int(hms[1])
                  sl=hms[2].split(".")
                  s=int(sl[0])+int(sl[1])/100
                  t2=h*3600+m*60+s

                  cursor.close()
                      

                  query4= "SELECT idFrameElement FROM `view_labelfecetarget` WHERE idSentence="+str(id3[0])
                
                  cursor = conn.cursor()
                  cursor.execute(query4)
                  fe_ids = cursor.fetchall()


                  fes=[value for value in fe_ids if value != (None,)]

                       
                  for x in fes:
                     Feset_ids.append(x)
                     start.append(t1)
                     end.append(t2)

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]

           d[id1[0]]=d2
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       
       cursor.close()

       do={}

       val=0

       for id1 in doc_ids:

           l=[]
           Feset=[]
           Feset_ids=[]
           Fset=[]
           start=[]
           end=[]
           
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

                  query4= "SELECT idFrameElement,startFrame,endFrame FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])
                
                  cursor = conn.cursor()
                  cursor.execute(query4)
                  fe_ids = cursor.fetchall()

                  cursor.close()

                       
                  for x in fe_ids:
                     Feset_ids.append(x[0])

                  for x in fe_ids:
                     start.append(x[1]*0.033)
                     end.append(x[2]*0.033)

           Feset_ids=set(Feset_ids)

           for id4 in Feset_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4)
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4)
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=["",start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=[Fset[0],start[Feset_ids.index(id4)],end[Feset_ids.index(id4)]]
           do[id1[0]]=d2
           
       conn.close()

       l=list(d.values())
       l1=list(do.values())
       x=l[0]
       y=l1[0]
       lx=list(x.keys())
       ly=list(y.keys())
       df={}
       k=list(do.keys())
       dmain=dict.fromkeys(list(do.keys()))
       for a_fe in lx:
          if a_fe in ly:
             df[a_fe]=[x[a_fe],y[a_fe]]

       dmain[k[0]]=df
       print(dmain)
       with open('report11.json', 'w') as fp:
          json.dump(dmain, fp)


   elif val=="12":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       s1=[]
       
       cursor.close()

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

               for y in sent_ids:
                   s.append(y)

                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(y[0])
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s1.append(smm[0])
                   

       d_buf= dict(zip(s, s1))
       d={}

       for id3 in s:

           smm=d_buf[id3]
           
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

           d1=dict.fromkeys(feset_ids)
           d2={}

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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[feset_ids.index(id4)][0]]=[[],t1,t2]
                else:
                    d2[feset[feset_ids.index(id4)][0]]=[fset[0],t1,t2]

           d[d_buf[id3][0]]=d2
            
       conn.close()

       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       
       cursor.close()

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

               for x in sent_ids:
                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s.append(smm[0])

       do={}


       for id3 in s:

           query42= "SELECT idAnnotationSetMM FROM annotationsetmm WHERE idSentenceMM="+str(id3[0])

           cursor = conn.cursor()
           cursor.execute(query42)
           ann_id = cursor.fetchall()

           cursor.close()

           query4= "SELECT idFrameElement FROM objectmm WHERE idAnnotationSetMM="+str(ann_id[0][0])

           cursor = conn.cursor()
           cursor.execute(query4)
           fe_ids = cursor.fetchall()


           cursor.close()

           feset=[]

           

           for id4 in fe_ids:
               query5= "SELECT entry FROM frameelement WHERE idFrameElement="+str(id4[0])
               cursor = conn.cursor()
               cursor.execute(query5)
               fe = cursor.fetchall()

               feset.append(fe[0])

               cursor.close()

           fe_ids=list(fe_ids)

           d1=dict.fromkeys(fe_ids)
           d2={}

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

           for id4 in fe_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[fe_ids.index(id4)][0]]=[[],start[fe_ids.index(id4)]*0.033,end[fe_ids.index(id4)]*0.033]
                else:
                    d2[feset[fe_ids.index(id4)][0]]=[fset[0],start[fe_ids.index(id4)]*0.033,end[fe_ids.index(id4)]*0.033]

           do[id3[0]]=d2
            
       conn.close()

       l=list(d.values())
       l1=list(do.values())

       df=[]

       for x in l:
          lx=list(x.keys())
          y=l1[l.index(x)]
          ly=list(y.keys())

          fd=[]
          for z in lx:
             if z in ly:
                fd.append([z,x[z],y[z]])
          df.append(fd)
                   
       
       dmain={}
       k=list(do.keys())


       for z in k:

          dmain[z]=df[z-1]
          
       print(dmain)
       with open('report12.json', 'w') as fp:
          json.dump(dmain, fp)

   elif val=="13":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1

       query = "SELECT idCorpus from corpus"

       cursor = conn.cursor()
       cursor.execute(query)
       crp_ids = cursor.fetchall()

       cursor.close()

       d={}

       for icd in crp_ids:
                
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
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=[]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]
           d[icd[0]]=d2
       print("\n")
       print(d)
           
            
       conn.close()

       with open('report13.json', 'w') as fp:
          json.dump(d, fp)


   elif val=="14":
        conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
        v=1

                
        query1 = "SELECT idDocument from documentmm"
       
        cursor = conn.cursor()
        cursor.execute(query1)
        doc_ids = cursor.fetchall()
       
        cursor.close()

        d={}

        val=0

        for id1 in doc_ids:

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
           d2={}

           F_ids=[]

           for id4 in Feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                Fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    Fset.append(f1)

                    cursor.close()

                if len(Fset)==0:
                    d2[Feset[Feset_ids.index(id4)][0]]=[]
                else:
                    d2[Feset[Feset_ids.index(id4)][0]]=Fset[0]
           d[id1[0]]=d2
           
        print("\n")
        print(d)
        conn.close()
        with open('report14.json', 'w') as fp:
          json.dump(d, fp)
      

   elif val=="15":
       conn = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="test_db"
                )
       v=1
                
       query1 = "SELECT idDocument from documentmm"
       
       cursor = conn.cursor()
       cursor.execute(query1)
       doc_ids = cursor.fetchall()
       s=[]
       
       cursor.close()

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

               for x in sent_ids:
                   query41= "SELECT idSentenceMM FROM sentencemm WHERE idSentence="+str(x[0])
            
                   cursor = conn.cursor()
                   cursor.execute(query41)
                   smm = cursor.fetchall()

                   cursor.close()
                   s.append(smm[0])

       d={}


       for id3 in s:

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

           d1=dict.fromkeys(feset_ids)
           d2={}

           f_ids=[]
           fset=[]

           for id4 in feset_ids:
                query6= "SELECT idEntity2 FROM entityrelation WHERE idEntity1="+str(id4[0])
                cursor = conn.cursor()
                cursor.execute(query6)
                f = cursor.fetchall()

                d1[id4]=f

                cursor.close()

                fset=[]

                for x in f:
                    query7= "SELECT entry FROM frame WHERE idFrame="+str(x[0])
                    cursor = conn.cursor()
                    cursor.execute(query7)
                    f1 = cursor.fetchall()

                    fset.append(f1)

                    cursor.close()

                if len(fset)==0:
                    d2[feset[feset_ids.index(id4)][0]]=[]
                else:
                    d2[feset[feset_ids.index(id4)][0]]=fset[0]

           d[id3[0]]=d2
       print("\n")
       print(d)
            
       conn.close()

       with open('report15.json', 'w') as fp:
          json.dump(d, fp)

   return 

app = Flask(__name__)
cors = CORS(app)

@app.route('/report',methods=['GET','POST'])
def getreport():
   val=request.form['val']
   getReports(val)
   #val=input("Enter yes if satisfied with detected objects and no to create and track own objects...")
   #if val=="no":
      #v=1
      #objectTracking.detect_and_track(video_path,sid,start_time,end_time,v)

   return 'ok'
   

if __name__=='__main__':
   app.run()
       


