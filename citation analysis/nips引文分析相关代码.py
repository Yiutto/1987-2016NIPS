# aa=Author-Affliciation
# ecc= cited the amount
# f = field
# id = Paper_id
# r_Id = Refrences_id
# ti = title
# w = words
# y = year



# 定义附属机构Id及name的字典
# aff_id_name = {'185261750':'University of Toronto',
#                 '97018004':'Stanford University',
#                 '63966007':'Massachusetts Institute of Technology',
#                 '95457486':'University of California, Berkeley',
#                 '1290206253':'Microsoft',
#                  '74973139':'Carnegie Mellon University',
#                  '1291425158':'Google',
#                  '149899117':'Max Planck Society',
#                  '45129253':'University College London',
#                  '197251160':'Hebrew University of Jerusalem',
#                  '20089843':'Princeton University',
#                  '36258959':'University of California, San Diego',
#                  '122411786':'California Institute of Technology',
#                  '70931966':'Université de Montréal',
#                  '36672615':'Courant Institute of Mathematical Sciences',
#                  '40347166':'University of Chicago',
#                  '1326498283':'French Institute for Research in Computer Science and Automation',
#                  '86519309':'University of Texas at Austin',
#                  '72090969':'Bell Labs',
#                  '1283103587':'AT&T'
#                  }


#-*- coding:utf-8 -*-
import pandas as pd
import re
import numpy as np
import itertools
nips_data = pd.read_csv('Microsoft Academic 2000-2015nips.csv')

#-----------------------------------------------------------------
#-------------------------Define Fuction(Start)---------------------------------
#-----------------------------------------------------------------


# ************************************************************************
#1.定义通过AuhorID来获取该作者发表所有论文的总被引量
def authIdToPaperIdEcc(s):
    data_id = list()
    i = 0
    length = len(nips_data)
    while i < length:
        if s in nips_data.aa[i]:
            data_id.append(i)
        i += 1
    AuthId_nips = nips_data.reindex(data_id)
    AuthId_ecc = list(AuthId_nips.ecc)
    return sum(AuthId_ecc)
# ******************************************************************************

# *********************************************************************
#2.定义通过AfflictionID如何输出Affliciation发表论文的总被引用量
def affIdToPaperIdEcc(s):
    data_id = list()
    i = 0
    length = len(nips_data)
    while i < length:
        if s in nips_data.aa[i]:
            data_id.append(i)
        i += 1
    AffId_nips = nips_data.reindex(data_id)
    AffId_ecc = list(AffId_nips.ecc)
    return sum(AffId_ecc)
# **************************************************************************

# **************************************************************************
#4 通过AfflictionID来获取该附属机构研究的领域
def affIdToField(s):
    data_id = list()
    i = 0
    length = len(nips_data)
    while i < length:
        if s in nips_data.aa[i]:
            data_id.append(i)
        i += 1
    AffId_nips = nips_data.reindex(data_id)
    AffId_field = AffId_nips.f
    all_fid = list()
    for field in AffId_field:
        fid = list()
        if str(field) != 'nan':
            fid = re.findall(r"'fId': \d+", field)
            all_fid.extend(fid)

    #all_fid有许多重复的fID，必须先用集合求出唯一id，然后统计各个fId个数
    myf = list(set(all_fid))
    paper_counts = list()
    for field in myf:
        paper_count = all_fid.count(field)
        paper_counts.append(paper_count)
    AffId_fId_Papers = pd.DataFrame({'fieldId': myf, 'papers': paper_counts})
    return AffId_fId_Papers
# **************************************************************************

# **************************************************************************
 #5 通过afId来获取该附属机构的H指数
def affId_H_index(s):#  s = 'afId': 63966007,
    data_id = list()
    i = 0
    length = len(nips_data)
    while i < length:
        if s in nips_data.aa[i]:
            data_id.append(i)
        i += 1
    AffId_nips = nips_data.reindex(data_id)
    #获取被引量
    citations = list(AffId_nips.ecc)

    #通过被引量求H指数
    citations.sort(reverse=True)
    for index in range(len(citations)):
        if index>=citations[index]:
            return index
    return len(citations)
# **************************************************************************

# **************************************************************************
 #6 通过auId来获取该附属机构的H指数
def auId_H_index(s):#  s = 'afId': 63966007,
    data_id = list()
    i = 0
    length = len(nips_data)
    while i < length:
        if s in nips_data.aa[i]:
            data_id.append(i)
        i += 1
    AuId_nips = nips_data.reindex(data_id)
    #获取被引量
    citations = list(AuId_nips.ecc)

    #通过被引量求H指数
    citations.sort(reverse=True)
    for index in range(len(citations)):
        if index>=citations[index]:
            return index
    return len(citations)
# **************************************************************************

# **************************************************************************
 # 7. 找出2个作者合作的论文数

 #a.定义作者Id对应的论文Id
def authIdToPaper(s):
    data_id = list()
    i = 0
    length = len(nips_data)
    while i < length:
        if s in nips_data.aa[i]:
            data_id.append(i)
        i += 1
    return data_id
#b.找出相同的Papers,auth_tuple是一个元组
def co_auth_papers(auth_tuple):
    s1, s2 = auth_tuple
    auth1_PaperId = authIdToPaper(s1)
    auth2_PaperId = authIdToPaper(s2)
    co_auth_PaperId = set(auth1_PaperId) & set(auth2_PaperId)
    return len(co_auth_PaperId)

    # def co_auth_papers(s1, s2):
    #     auth1_PaperId = authIdToPaper(s1)
    #     auth2_PaperId = authIdToPaper(s2)
    #     co_auth_PaperId = set(auth1_PaperId) & set(auth2_PaperId)
    #     return len(co_auth_PaperId)
# **************************************************************************


#-----------------------------------------------------------------
#-------------------------Define Fuction(End)---------------------------------
#-----------------------------------------------------------------


#-----------------------------------------------------------------
#------------------------Data Processing(Start)---------------------------------
#-----------------------------------------------------------------

# **************************************************************************
#1 整理author个数，相应AuthorId、Papers、eccs
aa = nips_data.aa
all_authorid = list()
for auth in aa:
    authorid = list()
    authorid = re.findall(r"'auId': \d+", auth)
    all_authorid.extend(authorid)

#all_authorid有许多重复的authorID，必须先用集合求出唯一id，然后统计各个authorId个数
myauthor = list(set(all_authorid))
paper_counts = list()
eccs = list()
for author in myauthor:
    paper_count = all_authorid.count(author)
    authId_ecc = authIdToPaperIdEcc(author)
    paper_counts.append(paper_count)
    eccs.append(authId_ecc)
authId_Papers_Eccs = pd.DataFrame({'authId': myauthor, 'papers': paper_counts, 'eccs': eccs})
authId_Papers_Eccs.to_csv('authId_Papers_Eccs.csv')
# **************************************************************************

# **************************************************************************
#2 整理affilication个数，相应AffId、Papers、eccs
aa = nips_data.aa
all_affid = list()
for aff in aa:
    affid = list()
    #用set()来将每一行相同的affID过滤掉
    affid = set(re.findall(r"'afId': \d+", aff))
    all_affid.extend(list(affid))

#all_affid有许多重复的authorID，必须先用集合求出唯一id，然后统计各个affId个数
myaff = list(set(all_affid))
paper_counts = list()
eccs = list()
for aff in myaff:
    paper_count = all_affid.count(aff)
    affId_ecc = affIdToPaperIdEcc(aff)
    paper_counts.append(paper_count)
    eccs.append(affId_ecc)
affId_Papers_Eccs = pd.DataFrame({'affId': myaff, 'papers': paper_counts, 'eccs': eccs})
affId_Papers_Eccs.to_csv('affId_Papers_Eccs.csv')
# **************************************************************************

# **************************************************************************
#3 整理field个数，相应fId、Papers
f = nips_data.f
all_fid = list()
for field in f:
    fid = list()
    if str(field) != 'nan':
        fid = re.findall(r"'fId': \d+", field)
        all_fid.extend(fid)

#all_fid有许多重复的fID，必须先用集合求出唯一fId，然后统计各个fId个数
myf = list(set(all_fid))
paper_counts = list()
# eccs = list()
for field in myf:
    paper_count = all_fid.count(field)
    paper_counts.append(paper_count)
    # affId_ecc = affIdToPaperIdEcc(aff)
    # eccs.append(affId_ecc)
fId_Papers = pd.DataFrame({'fieldId': myf, 'papers': paper_counts})
fId_Papers.to_csv('fId_Papers.csv')
# **************************************************************************

# **************************************************************************
#4 通过{u'afId': 63966007, u'afN': u'massachusetts institute of technology'}来获取该afId下研究的Field
afId_1_field = affIdToField("'afId': 63966007")
afId_1_field.to_csv('afId_1_field.csv')

# u'afN': u'university of toronto' u'afId': 185261750
afId_7_field = affIdToField("afId': 185261750")
afId_7_field.to_csv('afId_7_field.csv')
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#{u'auId': 198699297, u'afN': u'massachusetts institute of technology',
# **************************************************************************

# **************************************************************************
#5 通过afId来求每个附属机构的H指数

#a.求所有的afId
aa = nips_data.aa
all_affid = list()
for aff in aa:
    affid = list()
    #用set()来将每一行相同的affID过滤掉
    affid = set(re.findall(r"'afId': \d+", aff))
    all_affid.extend(list(affid))

    #all_affid有许多重复的authorID，必须先用集合求出唯一id，然后统计各个affId个数
myaff = list(set(all_affid))
#b.求afId对应的H指数
aff_H = {}
for affid in myaff:
    aff_H[affid] = affId_H_index(affid)
affHindex = pd.Series(aff_H)
affHindex.to_csv('affId_H_index.csv')
# **************************************************************************

# **************************************************************************
#6 通过auId来求每个附属机构的H指数

#a.求所有的afId
aa = nips_data.aa
all_authorid = list()
for auth in aa:
    authorid = list()
    authorid = re.findall(r"'auId': \d+", auth)
    all_authorid.extend(authorid)

    #all_authorid有许多重复的authorID，必须先用集合求出唯一id，然后统计各个authorId个数
myauthor = list(set(all_authorid))

#b.求auId对应的H指数
au_H = {}
for auid in myauthor:
    au_H[auid] = auId_H_index(auid)
auHindex = pd.Series(au_H)
auHindex.to_csv('auId_H_index.csv')
# **************************************************************************

# **************************************************************************
#7.求2个作者合作论文数（方法太慢了，还是用数据库处理比较好）
# au1 = auId': 2435751034   (Michael I. Jordan)
# au2 = 'auId': 2104401652  (Andrew Y. Ng)
# au3 = 'auId': 2122351653  (Thomas L. Griffiths)

auId1 = "auId': 2435751034"
auId2 = "'auId': 2104401652"
auId3 = "'auId': 2122351653"

co_auth_papers((auId1, auId2))
co_auth_papers((auId1, auId3))
co_auth_papers((auId2, auId3))

aa = nips_data.aa
all_authorid = list()
for auth in aa:
    authorid = list()
    authorid = re.findall(r"'auId': \d+", auth)
    all_authorid.extend(authorid)

    #all_authorid有许多重复的authorID，必须先用集合求出唯一id，然后统计各个authorId个数
myauthor = list(set(all_authorid))

co_auth = list(itertools.combinations(myauthor, 2))

coauth_papers = {}
for coau in co_auth:
    co_papers = co_auth_papers(coau)
    if co_papers:
        coauth_papers[coau] = co_papers

# **************************************************************************
# #python的排列组合
# >>> import itertools
# >>> print list(itertools.permutations([1,2,3,4],2))
# [(1, 2), (1, 3), (1, 4), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 1), (4, 2), (4, 3)]
#
# >>> print list(itertools.combinations([1,2,3,4],2))
# [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#a.求所有的afId

#-----------------------------------------------------------------









# **************************************************************************
# **************************************************************************


# data = [8, 18, 8, 6, 4, 5, 4]
#
# def H_index(citations):# citations must be list
#     citations.sort(reverse=True)
#     for index in range(len(citations)):
#         if index>=citations[index]:
#             return index
#     return len(citations)


#-----------------------------------------------------------------
#-----------------------------------------------------------------
