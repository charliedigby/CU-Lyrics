# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 13:57:39 2025

@author: charl
"""
#%% Song class
import json
song={}
docu={}
A=r"""{\setbeamertemplate{footline}
{ 
 {\usebeamerfont{section in head/foot}
 \begin{beamercolorbox}[ht=4.5ex,dp=1.5ex,%
      leftskip=.3cm,rightskip=.3cm plus1fil]{section in head/foot}
 \usebeamercolor[fg]{section in head/foot}%
 \fontsize{12}{25}\selectfont 
"""
 #insert hyperlinks here
B=r""" 
 \end{beamercolorbox}%
  \begin{beamercolorbox}[ht=2.5ex,dp=1.125ex,%
   leftskip=.3cm,rightskip=.3cm plus1fil]{subsection in head/foot}
   \insertauthor
 \end{beamercolorbox}%
 }
}
\subsection{"""
#insert title here and close with bracket

#now begin the slides:
#hypertarget: (phantomsection helps locate hypertarget at top of slide)
C="""\\phantomsection
\\hypertarget{"""
#begin the frame:
D="""}{}
\\begin{frame}{"""
#for 1st slide, insert title
E="""}
\\fontsize{"""
#insert text size and column seperation, divided by }{
F="}\\selectfont\n"
#insert slide text
G="\n\n\\end{frame}\n"
H="""}
 \\vfill
  \\centering
  \\begin{beamercolorbox}[sep=8pt,center,shadow=true,rounded=true]{title}
    \\usebeamerfont{title}
    """
I="""    
  \\end{beamercolorbox}
  \\vfill
\\end{frame}
"""

class Song:
    def __init__(self,title,alttitles,artist,cat,Wtitle,Walttitles,lyrics,errors):
        self.title=title
        self.alttitles=alttitles
        self.Wtitle=Wtitle
        self.Walttitles=Walttitles
        self.artist=artist
        self.lyrics=lyrics
        self.cat=cat
        self.errors=errors
    def dictionarify(self):
        song_dictionaries[self.title+json.dumps(self.alttitles)+self.Wtitle+json.dumps(self.Walttitles)+self.artist]={"title":self.title,
                                  "Wtitle":self.Wtitle,"alttitles":self.alttitles,"Walttitles":self.Walttitles,"cat":self.cat,
                                  "artist":self.artist,"lyrics":self.lyrics,"errors":self.errors}
    def stanzaSplit(self,stanza,attempt=1):#function to rejoin and manually split a stanza
        stanz=stanza
        stanza=[]
        for slide in stanz:
            stanza+=slide
        
        for i in range(len(stanza)): print("    "+str(i+1)+") "+stanza[i])
        print("Do you want to split this stanza over multiple slides?")
        print("Slides shouldn't be longer than 10 lines each, and ideally should be roughly equal length")
        print("Type the numbers associated with the first line on each slide (excluding 1), seperated by commas")
        print("If you want the stanza to only take 1 slide, simply press enter")
        user_input=input()
        try:
            if "," in user_input:             
                splits=[int(split)-1 for split in user_input.split(",")]
            elif user_input=="":splits=[]
            else: splits=[int(user_input)-1]
        except: 
            if attempt<=3:
                print("Input not recognized, try again:")
                attempt+=1
                return self.stanzaSplit(stanz,attempt)#rerun the function
            else: return #cease after 3 failed attempts
        else:
            splits1=[0]+splits
            splits2=splits+[len(stanza)]
            stanza=[stanza[i:j] for i,j in zip(splits1,splits2)] 
            return stanza
    def assignSlides(self,language="Bil"):
        if language=="Eng": i=2
        elif language=="Cym": i=3
        elif language=="Bil": i=4        
        for j in len(self.lyrics):
            listed=list(self.lyrics[j])
            listed[i]=self.stanzaSplit(self.lyrics[j][i])
            self.lyrics[j]=tuple(listed)
    def measureSlide(self,slide):
        if type(slide[0]) is list:
            lengths=[max([len(line[i]) for i in range(2)])for line in slide]
            return len(slide)*2,max(lengths)
        else:
            lengths=[len(line) for line in slide]
            return len(slide),max(lengths)        
    def biggestMeasure(self,language):
        if language=="Eng": i=2
        elif language=="Cym": i=3
        elif language=="Bil": i=4
        else: return
        slides=[]
        for stanza in self.lyrics:
            slides+=stanza[i]
        lines=[self.measureSlide(slide)[0] for slide in slides]
        chars=[self.measureSlide(slide)[1] for slide in slides]
        return max(lines),max(chars)
    def textSize(self,slide=False,language="Eng"):
        if slide:
            measure=self.measureSlide(slide)
        else: measure=self.biggestMeasure(language)
        textsize=min(900/measure[1],150/measure[0])###this may vary depending on aspect ratio
        colsep=textsize*1.2
        return str(textsize),str(colsep)
    def writeSlide(self,first_slide_in_stanza,uniformSize,slide,l,language):
        if uniformSize:
            measure=self.textSize(language=language)
        else:
            measure=self.textSize(slide=slide)
        textsize=measure[0]
        sep=measure[1]
        if type(slide[0]) is list:#viz, if bilingual stanza
            slide=["\\Eng{"+line[0]+"}\\\ \n\\Cym{"+line[1]+"}" for line in slide]
        stanza="\\\ \n".join(slide)#make each stanza a string, with \\ as newline command in LaTeX
        if first_slide_in_stanza:#only make hyperlink for first slide
            text=f'{C}{self.title}{self.alttitles}{self.artist}{self.lyrics[l][1]}{D}'
        else: text="\\begin{frame}{"
        text+=E+textsize+"}{"+sep+F+"\n"+stanza+G#stanza slides       
        return text
    def write(self,language,uniformSize=True):
        if language=="Bil" and self.errors["bilingual"]:
            language="Eng"
        
        text=A#set footer
        leng=len(self.lyrics)
        for l in range(leng): text+="\hyperlink{%s%s%s%s}{%s  }" %(self.title,self.alttitles,self.artist,self.lyrics[l][1],self.lyrics[l][0])#insert hyperlinks
        text+=B+self.title+"}\n"
        text+=f'{C}{self.title}{self.alttitles}{self.artist}{D}{H}{self.title} {self.artist}{I}\n'#title page for song
        for l in range(leng):
            first_slide_in_stanza=True
            if self.lyrics[l][2][0] and (language=="Eng" or (language=="Bil" and not self.lyrics[l][3][0])):
                for slide in self.lyrics[l][2]:
                    text+=self.writeSlide(first_slide_in_stanza=first_slide_in_stanza,uniformSize=uniformSize,slide=slide,l=l,language=language)
                    first_slide_in_stanza=False
            elif self.lyrics[l][3][0] and (language=="Cym" or (language=="Bil" and not self.lyrics[l][2][0])):
                for slide in self.lyrics[l][3]:
                    text+=self.writeSlide(first_slide_in_stanza=first_slide_in_stanza,uniformSize=uniformSize,slide=slide,l=l,language=language)
                    first_slide_in_stanza=False
            elif language=="Bil" and self.lyrics[l][4][0][0]:
                for slide in self.lyrics[l][4]:
                    text+=self.writeSlide(first_slide_in_stanza=first_slide_in_stanza,uniformSize=uniformSize,slide=slide,l=l,language=language)
                    first_slide_in_stanza=False
            else:return
        text+="}\n\n"#end song's footnote settings
        return text
    def allTitles(self,language):
        E=set([self.title]+self.alttitles)
        W=set([self.Wtitle]+self.Walttitles)
        
        if language=="Cym":items=W
        elif language=="Eng":items=E
        elif language=="Bil":items=W.union(E)
        else: items={}
        items.discard("")#prevent empty entries
        return items
    def getContents(self,language="Bil"):
        items=self.allTitles(language)
        new_items=[]
        for item in items:
            similar=[]
            for a_song in song.values():
                if item in a_song.allTitles(language) and a_song!=self:
                    similar.append(a_song)
            if similar==[]:
                new_items.append(item)
            elif self.artist and self.artist not in [a_song.artist for a_song in similar]:
                new_items.append(item+" "+self.artist)
            else:
                sim=[]
                for a_song in similar:
                    sim.append(a_song.allTitles(language))
                different=[other_title for other_title in items if other_title not in sim]
                if different: new_items.append(item+" ("+different[0]+")")
                else:print("similarity error: "+item)
        hyperref=f'{self.title}{self.alttitles}{self.artist}'    
        return [(item,hyperref,self.cat) for item in new_items]
       
        
        


#%% Document class

class Document:
    def __init__(self,language="Eng",songs=song,aspect_ratio="169",theme="Berlin",Ecolour="0056B8",Wcolour="222222",logo_address="CU_logo.jpeg",uniformSize=True,beforeWorship=["1","2","3"],worship=[],afterWorship=["4"]):
        self.language=language
        self.songs=songs
        self.aspect_ratio=aspect_ratio
        self.theme=theme
        self.Ecol=Ecolour
        self.Wcol=Wcolour
        self.logo_address=logo_address
        self.uniformSize=uniformSize
        self.beforeWorship=beforeWorship
        self.worship=worship
        self.afterWorship=afterWorship
    def dictionarify(self):
        global docu
        docu={"language":self.language,"aspect_ratio":self.aspect_ratio,
                  "theme":self.theme,"Ecolour":self.Ecol,"Wcolour":self.Wcol,"logo_address":self.logo_address,
                  "uniformSize":self.uniformSize,"beforeWorship":self.beforeWorship,
                  "afterWorship":self.afterWorship}
    def preamble(self):
        text="\\documentclass[aspectratio="+self.aspect_ratio+"]{beamer}\n"
        text+="\\usepackage{graphicx} % Required for inserting images\n"
        text+="\\usepackage{pdfpages}\n"
        text+="\\usetheme{"+self.theme+"}\n"
        text+="\\usepackage{xcolor}\n"
        text+="\\usepackage{fontspec}\n\\setmainfont{Times New Roman}\n"
        text+="\\definecolor{Eng}{HTML}{"+self.Ecol+"}\n"
        text+="\\definecolor{Cym}{HTML}{"+self.Wcol+"}\n"
        text+="\\newcommand{\\Eng}[1]{\\textcolor{Eng}{\\textsf{#1}}}\n"
        text+="\\newcommand{\\Cym}[1]{\\textcolor{Cym}{\\textit{#1}}}\n\n"
        text+="\\setbeamertemplate{footline}\n{%\n"
        text+="  {\\usebeamerfont{section in head/foot}\n\n"  
        text+="    \\begin{beamercolorbox}[ht=2.5ex,dp=1.125ex,%\n"
        text+="    leftskip=.3cm,rightskip=.3cm plus1fil]{subsection in head/foot}\n"
        text+="    \\insertauthor\n"
        text+="  \\end{beamercolorbox}%\n  }\n}\n\n\n"
        text+="\\setbeamertemplate{navigation symbols}{}\n"
        text+="\\title{Hymns and songs}\n\\author{Aberystwyth CU}\n\\date{}\n\n"
        text+="\\usepackage{hyperref}\n\n"
        text+="%text allignment package\n\\usepackage{ragged2e}\n\\Centering\n\n"
        text+="%allows text to fill whole width of slides\n\\setbeamersize{text margin left=0pt,text margin right=0pt}\n\n"
        text+="%CU logo on every slide\n\\logo{\\includegraphics[height=1.5cm]{"+self.logo_address+"}}\n\n"
        text+="%the following code removes the dots from the navigation\n"
        text+="\\makeatletter\n\\def\\beamer@writeslidentry{\\clearpage\\beamer@notesactions}\n\\makeatother\n\n"
        return text
    def contentsList(self,section,entries,sectionAbbr):
        e=entries
        if len(e)==0:
            return ""#if no entries, don't make contents page
        A=9
        B=8#these variables hold max number of entries in each column
        text="\\section{ "+sectionAbbr+" }\n\n"  #section name becomes navigation button in top bar
        text+="\\begin{frame}[t]{"+section+"}\n"  #frame title appears at top of first page of conntents
        while e:       
            text+="\\begin{columns}[t]\n\\column{0.05\\textwidth}\n\\column{0.45\\textwidth}\n"
            text+="\\begin{itemize}\n"""            
            if len(e)<A+B:
                A=int((len(e)+1)/2)
                B=int(len(e)/2)#if slide underful, evenly distribute between columns
            elif A+B<len(e)<A+B+4:
                A=A-1
                B=B-1#ensures next slide never has less than 3 entries- slightly evens distribution between slides
            for entry in range(A): 
                if e: text+=e.pop(0)+"\n"
                else: text+="    \\item[] \\phantom{1}\n" #fill space with phantom elements to maintain consistent format
            text+="    \\item[] \\phantom{1}\n\\end{itemize}\n"
            text+="\\column{0.45\\textwidth}\n"
            text+="\\begin{itemize}\n"
            for entry in range(B): 
                if e: text+=e.pop(0)+"\n"
                else: text+="    \\item[] \\phantom{1}\n"
            if e:
                text+="    \\item[] \\textit{Continued on next slide...}\n"
                text+="\\end{itemize}\n\\column{0.05\\textwidth}\n\\end{columns}\n"
                text+="\\end{frame}\n\\begin{frame}[t]\n"
                
            else: text+="    \\item[] \\phantom{1}\n"
            A=11
            B=10#maximum lengths of columns for subsequent slides of contents (longer due to lack of header)
        text+="\\end{itemize}\n\\column{0.05\\textwidth}\n"
        text+="\\end{columns}\n\\end{frame}\n\n"        
        return text
    def writeDoc(self):
        categories=[]
        c=["Traditional","Contemporary","Modern"]#category names- this list could be updated to be passed as a parameter
        ca=["Trad","Contemp","Mod"]#abbreviated category names will show on navigation bar
        sections=[]
        contents_entries=[]
        for song in self.songs.values():
            contents_entries+=song.getContents()
        
        contents_entries=sorted(contents_entries, key=lambda x: x[0])  #sort alphabetically by entry
        
        for cat in range(1,4):            
            categories.append((c[cat-1],ca[cat-1],["    \\item \\hyperlink{"+entry[1]+"}{"+entry[0]+"}\n" for entry in contents_entries if entry[2]==cat]))
        #    if not categories[-1][2]:categories.pop(-1)
        sections.append(("Num",[song for song in self.songs.values() if str.isdigit(song.title[0])],["    \\item \\hyperlink{"+entry[1]+"}{"+entry[0]+"}" for entry in contents_entries if str.isdigit(entry[0][0])]))
        if not sections[0][2]:sections.pop(0) #if nothing in contents, remove contents section
        for letter in ["A",'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
            sections.append((letter,[son for son in self.songs.values() if son.title[0].upper()==letter],["    \\item \\hyperlink{"+entry[1]+"}{"+entry[0]+"}" for entry in contents_entries if entry[0][0].upper()==letter]))
        #    if not sections[-1][2]:sections.pop(-1)  #if nothing in contents, remove contents section
        
            
        text=self.preamble()
        text+="\\begin{document}\n\n"
        text+="\\maketitle\n\n"
        for cat in categories:
            text+=self.contentsList(cat[0],cat[2],cat[1])
        
        for section in sections:
            text+=self.contentsList(section[0],section[2],section[0])
            for song in section[1]:
                text+=song.write(self.language,self.uniformSize)
        text+="\\end{document}"
        return text
    def plan(self):
        print("Choose the slides for the beginning, then pressing enter after each slide.")
        print("Press enter with no input to move to worship section, and likewise for the end.")
        
        schedule=[[],[],[]]
        for section in schedule:
            user_input=" "
            while user_input!="":
                user_input=input()
                if user_input!="": section.append(user_input)
        self.beforeWorship=schedule[0]
        self.afterWorship=schedule[2]
        self.worship=[self.songs[request] for request in schedule[1] if request in self.songs]
    def planWorship(self):
        print("Choose songs, pressing enter after each slide.")
        user_input=" "
        section=[]
        while user_input!="":
            user_input=input()
            if user_input!="": section.append(user_input)
     
        self.worship=[self.songs[request] for request in section if request in self.songs]
    def getSlide(self,file_name):
        text="\\includepdf{"
        text+=file_name+".png"
        text+="}\n"
        return text
    def writeEquip(self):
        text=self.preamble()
        text+="\\begin{document}\n\n"
        for slide in self.beforeWorship:
            text+=self.getSlide(slide)
        for request in self.worship:
            text+="\\section{ "+request.title+" }\n\n"
            text+=request.write(self.language,self.uniformSize)
        for slide in self.afterWorship:
            text+=self.getSlide(slide)
        text+="\\end{document}"
        return text
        
#%%

        
    
#%% read song function
def read_song(file):
    global song_dictionaries
    s=open(file,"r")
    ref=[]
    Wref=[]
    label=[]
    labell=[]
    english_lines_error=False
    welsh_lines_error=False
    length_error=False
    bilingual_lines_error=False
    bilingual_error=False

    song= s.readlines()

    #close song file
    s.close()

    song=[line.rstrip() for line in song] #removes \n and spaces from each line

   
    title=""
    Wtitle=""
    
    for a in range(2):#takes a line in first two lines begining with W- as Welsh title
        if song[a].startswith("W-"): 
            Wtitle=(song.pop(a))[2:]
    if song[0]: title=song[0] #Remaining first line taken as English title- leave space if no English title   
    
    if song[1].isdigit():
        cat=int(song.pop(1))
    else: cat=0

    alttitles=[]
    Walttitles=[]
    art=""
    p=1
    while len(song[p])>3:
        if song[p].startswith("W-"):
            Walttitles.append(song[p][2:])
            p=p+1
        else:
            alttitles.append(song[p])
            p=p+1
    if not title and alttitles: title=alttitles.pop(0)
    if not Wtitle and Walttitles: Wtitle=Walttitles.pop(0) #if either title field empty while alternate titles exist, the first becomes main title for that language
        
    #this interperets any lines before the first stanza label or blank line as an alternative title 
    if len(song[p])==0 and len(song[p+1])>3:
        art=f'({song[p+1]})'
    #this interperets a text line after a blank line (immediately following any titles) as an artist's name
        
    song=list(filter(None,song)) #removes empty lines  
    length=len(song) #number of lines to search for stanza labels

    for a in range(length): #search lines for stanza labels
        if len(song[a])<=3 and song[a]!="-" and song[a]!="W" and not '['in song[a]: #any line no more than 3 characters interpreted as stanza label, unless [] used, or W
            ref.append(a)
            label.append(song[a]) #lists of line references and stanza labels
            while song[a] in labell:
                song[a]+="I"
            labell.append(song[a]) #the labels in labell are unique, and will be used for
                                   #hyperlink references, while those in label will be visible
        elif '[' in song[a]:
            song[a]=song[a].replace("[","")
            song[a]=song[a].replace("]","")
        elif song[a]=="W":
            Wref.append(a)
    ref.append(length) #codes the last line+1 as final stanza reference, to bookend the last stanza
        
    
            
    #collect the stanzas

    stanzas=[[] for l in label]
    Wstanzas=[[] for l in label]
    
    for t in range(len(label)): 
        endEng=ref[t+1]
        for w in Wref:
            if ref[t]<w<ref[t+1]:
                endEng=w
                break
        for l in range(ref[t]+1,endEng): #append lines between stanza references
            stanzas[t].append(song[l])
       
        for l in range(endEng+1,ref[t+1]):
            Wstanzas[t].append(song[l])
    
    #ascertain longest line length to choose font size
    longest=len(max(song,key=len)) #length of longest line
    if longest>61:
        length_error=True
    lyrics=[]    
    
    for s in range(len(stanzas)):
        split=[i for i in range(len(stanzas[s])) if stanzas[s][i]=="-"]
        splits=[split[i]-i for i in range(len(split))]
        for i in splits: stanzas[s].pop(i)
        splits1=[0]+splits
        splits2=splits+[len(stanzas[s])]
        englishStanza=[stanzas[s][i:j] for i,j in zip(splits1,splits2)]
        for slide in englishStanza: #if any slide is too long, flag an error
            if len(slide)>10: english_lines_error=True
        
        split=[i for i in range(len(Wstanzas[s])) if Wstanzas[s][i]=="-"]
        splits=[split[i]-i for i in range(len(split))]
        for i in splits: Wstanzas[s].pop(i)
        splits1=[0]+splits
        splits2=splits+[len(Wstanzas[s])]
        welshStanza=[Wstanzas[s][i:j] for i,j in zip(splits1,splits2)]
        for slide in welshStanza: 
            if len(slide)>10: welsh_lines_error=True
        
        if len(englishStanza)!=len(welshStanza): bilingual_error=True #if lines don't match between languages, flag error
        for eslide,wslide in zip(englishStanza,welshStanza):
            if len(eslide)!=len(wslide): bilingual_error=True
        
        bilingualStanza=[[[e,c] for e,c in zip(eng,cym)] for eng,cym in zip(englishStanza,welshStanza)]
        try:
            for slide in bilingualStanza:
                if len(slide[0])+len(slide[1])>10: bilingual_lines_error=True
        except:bilingual_lines_error=True
        lyrics.append((label[s],labell[s],englishStanza,welshStanza,bilingualStanza))
        
    errors={"length":length_error,"english lines":english_lines_error,"welsh lines":welsh_lines_error,"bilingual lines":bilingual_lines_error,"bilingual":bilingual_error}    
    
    if title+json.dumps(alttitles)+Wtitle+json.dumps(Walttitles)+art in song_dictionaries:
        print("This song already seems to exist:")
        print(song_dictionaries[title+json.dumps(alttitles)+Wtitle+json.dumps(Walttitles)+art])
        print("Do you want to?:\nA. Overwrite\nB. Save as a version of the same song\nC. Exit (either to discontinue attempt or make changes to distinguish the songs from each other)")
        user_response=False
        while not user_response in ["A","B","C"]:
            user_response=input("Type \"A\", \"B\" or \"C\", then press enter").upper()
            if user_response=="A": continue
            elif user_response=="B": print("Sorry, this function is still under development, and is currently unavailable")
            elif user_response=="C": return
            else:print("Entry not recognized, please try again.")
        
    song_dictionaries[title+json.dumps(alttitles)+Wtitle+json.dumps(Walttitles)+art]={"title":title,"Wtitle":Wtitle,"alttitles":alttitles,"Walttitles":Walttitles,"cat":cat,
                              "artist":art,"lyrics":lyrics,"errors":errors}
    makeClass(song_dictionaries[title+json.dumps(alttitles)+Wtitle+json.dumps(Walttitles)+art])
#%% 
        
def makeClass(song_dict):
    global song
    song[song_dict["title"]+json.dumps(song_dict["alttitles"])+song_dict["Wtitle"]+json.dumps(song_dict["Walttitles"])+song_dict["artist"]]=Song(**song_dict)
def saveSongs(file="songs JSON.txt"):
    for a_song in song.values():
        a_song.dictionarify()
    with open(file,"w") as f:
        text=json.dumps(song_dictionaries)
        print(text,file=f)

def saveDoc(file="document JSON.txt"):
    doc.dictionarify()
    with open(file,"w") as f:
        print(json.dumps(docu),file=f)

def save():
    saveSongs()
    saveDoc()
   
    
    
from pathlib import Path
def readJoblot():
    song_paths=[]        
    folder_path = Path("Songs")
    for file in folder_path.iterdir():
        if file.is_file():  # Check if it's a file
            song_paths.append(file)       
    for song in song_paths:
        read_song(song)
        
        
with open("songs JSON.txt","r") as f:
    text=f.read()
song_dictionaries=json.loads(text)

with open("document JSON.txt","r") as f:
    text=f.read()
docu=json.loads(text)

for songs in song_dictionaries.values():
    makeClass(songs)   

doc=Document(**docu)


def test():
    with open("test.tex","w") as f:
        print(doc.writeDoc(),file=f)
