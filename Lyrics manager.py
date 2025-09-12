# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 13:57:39 2025

@author: charl
"""
#%% Song class
"""
import subprocess

def compile_latex(file_name):
    try:
        # Run XeLaTeX
        subprocess.run(["xelatex", file_name], check=True)
        
        # Run BibTeX
        subprocess.run(["bibtex", file_name.replace(".tex", "")], check=True)
        
        # Run MakeIndex
        subprocess.run(["makeindex", file_name.replace(".tex", ".idx")], check=True)
        
        # Run XeLaTeX twice more for proper references
        subprocess.run(["xelatex", file_name], check=True)
        subprocess.run(["xelatex", file_name], check=True)
        
        print("Compilation successful!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
compile_latex("document.tex")
"""
"""
Explanation
xelatex: Compiles the .tex file into a PDF.
bibtex: Processes the bibliography.
makeindex: Generates the index file.
Additional xelatex runs: Ensure all references, citations, and indices are updated correctly.
Dependencies
Ensure that XeLaTeX, BibTeX, and MakeIndex are installed and accessible via your system's PATH.
The .tex file should include proper bibliography and index commands.
"""


import json
song={}
docu={}
documents={}
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
    def update(self, attr_name, new_value, *args):
        
        if hasattr(self, attr_name):# Check if the attribute exists
            try:value=new_value.get()
            except:value=new_value
            finally:
                setattr(self, attr_name, value)  # Update the attribute
        else: print(attr_name,' not found')
    def updateBil(self,index):
        englishStanza=[]
        welshStanza=[]
        for slide in self.lyrics[index][2]:
            englishStanza+=slide
        for slide in self.lyrics[index][3]:
            welshStanza+=slide
        bilingualStanza=[[[e,c] for e,c in zip(englishStanza,welshStanza)]]
        new_stanza_list=list(self.lyrics[index])
        new_stanza_list[4]=bilingualStanza
        new_stanza_tuple=tuple(new_stanza_list)
        self.lyrics[index]=new_stanza_tuple
    def __init__(self,title,alttitles,artist,cat,Wtitle,Walttitles,lyrics,errors):
        self.title=title
        self.alttitles=alttitles
        self.Wtitle=Wtitle
        self.Walttitles=Walttitles
        self.artist=artist
        self.lyrics=lyrics
        self.cat=cat
        self.errors=errors
    def nameRef(self):
        return self.title+json.dumps(self.alttitles)+self.Wtitle+json.dumps(self.Walttitles)+self.artist
    def dictionarify(self):
        song_dictionaries[self.nameRef()]={"title":self.title,
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
    def uniqueEntry(self,item,language):
        items=self.allTitles(language)
        similar=[]
        for a_song in song.values():
            if item in a_song.allTitles(language) and a_song!=self:
                similar.append(a_song)
        if similar==[]:
            return item
        elif self.artist and self.artist not in [a_song.artist for a_song in similar]:
            return item+" "+self.artist
        else:
            sim=[]
            for a_song in similar:
                sim.append(a_song.allTitles(language))
            different=[other_title for other_title in items if other_title not in sim]
            if different: return item+" ("+different[0]+")"
            else:
                print("similarity error: "+item)
                return ""
    def getContents(self,language="Bil"):
        items=self.allTitles(language)
        new_items=[]
        for item in items:
            new_items.append(self.uniqueEntry(item,language))
            
        hyperref=f'{self.title}{self.alttitles}{self.artist}'    
        return [(item,hyperref,self.cat) for item in new_items]
    def getInfo(self):
        text="Title:\n  "
        text+=self.title
        
        if self.artist: 
            text+="\nArtist:\n  "
            text+=self.artist.strip('(,)')
        if self.alttitles: 
            text+="\nOther titles:"
            for t in self.alttitles:
                text+="\n  "
                text+=t
        
        return text
       
        
        


#%% Document class

class Document:
    def update(self, attr_name, new_value, *args):
        
        if hasattr(self, attr_name):# Check if the attribute exists
            try:value=new_value.get()
            except:value=new_value
            finally:
                setattr(self, attr_name, value)  # Update the attribute
        else: print(attr_name,' not found')
    def __init__(self,name,title,author,language="Eng",songs=[a_song for a_song in song.keys()],aspect_ratio="169",theme="Berlin",Ecolour="0056B8",Wcolour="222222",logo_address="CU_logo.jpeg",uniformSize=True):
        self.name=name
        self.title=title
        self.author=author
        self.language=language
        self.songs={}
        for a_song in songs:
            if a_song in song:
                self.songs[a_song]=song[a_song]
        self.aspect_ratio=aspect_ratio
        self.theme=theme
        self.Ecol=Ecolour
        self.Wcol=Wcolour
        self.logo_address=logo_address
        self.uniformSize=uniformSize
        self.type='document'
        
    def dictionarify(self):
        global docu
        docu["document"][self.name]={"name":self.name,"title":self.title,"author":self.author,"language":self.language,"aspect_ratio":self.aspect_ratio,
                  "theme":self.theme,"Ecolour":self.Ecol,"Wcolour":self.Wcol,"logo_address":self.logo_address,
                  "uniformSize":self.uniformSize,"songs":[a_song for a_song in self.songs.keys()]}
    def delete(self):
        docu["document"].pop(self.name,None)
        documents.pop(self.name,None)
        del self
    def rename(self,new_name):
        docu["document"].pop(self.name)
        self.name=new_name
        self.dictionarify()
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
        text+="\\title{"+self.title+"}\n\\author{"+self.author+"}\n\\date{}\n\n"
        text+="\\usepackage{hyperref}\n\n"
        text+="%text allignment package\n\\usepackage{ragged2e}\n\\Centering\n\n"
        text+="%allows text to fill whole width of slides\n\\setbeamersize{text margin left=0pt,text margin right=0pt}\n\n"
        if self.logo_address:
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
    def write(self):
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
    
    def create(self):
        name=self.name+".tex"
        with open(name,"w") as f:
            print(self.write(),file=f)
        #compile_latex(name)

class Equip(Document):
    def __init__(self,name,title,author,language="Eng",songs=song,aspect_ratio="169",theme="Berlin",Ecolour="0056B8",Wcolour="222222",logo_address="CU_logo.jpeg",uniformSize=True,beforeWorship=["1","2","3"],worship=[],afterWorship=["4"]):
        super().__init__(name,title,author,language,songs,aspect_ratio,theme,Ecolour,Wcolour,logo_address,uniformSize)
        self.beforeWorship=beforeWorship
        self.worship=[self.songs[request] for request in worship if request in self.songs]
        self.afterWorship=afterWorship
        self.type='equip'
    def dictionarify(self):
        global docu
        docu["equip"][self.name]={"name":self.name,"title":self.title,"author":self.author,"language":self.language,"aspect_ratio":self.aspect_ratio,
                  "theme":self.theme,"Ecolour":self.Ecol,"Wcolour":self.Wcol,"logo_address":self.logo_address,
                  "uniformSize":self.uniformSize,"beforeWorship":self.beforeWorship,"worship":[request.nameRef() for request in self.worship],
                  "afterWorship":self.afterWorship}  
    def rename(self,new_name):
        docu["equip"].pop(self.name)
        self.name=new_name
        self.dictionarify()
    def findSong(self,user_input,count=0):
        possible_songs=[a_song for a_song in self.songs.keys() if user_input.upper() in a_song.upper()]
        if possible_songs==[]:
            print("No songs appear to match. Try again:")
            return
        print("Which of these songs are you looking for?")
        for i in range(len(possible_songs)):
            print(str(i+1)+")  "+possible_songs[i])
        new_input=int(input("Type the number associated with the song you want: "))
        try: 
            result=possible_songs[new_input-1]
            return result
        except:
            if count<3:
                count+=1
                self.findSong(user_input,count)
            else: return
        
    def plan(self):
        print("Choose the slides for the beginning, then pressing enter after each slide.")
        print("Press enter with no input to move to the end.")
        
        schedule=[[],[]]
        for section in schedule:
            user_input=" "
            while user_input!="":
                user_input=input()
                if user_input!="": section.append(user_input)
        self.beforeWorship=schedule[0]
        self.afterWorship=schedule[1]
        self.planWorship()
    def planWorship(self):
        print("Choose songs, pressing enter after each entry.")
        user_input=" "
        section=[]
        while user_input!="":
            user_input=input()
            if user_input=="": continue
            elif user_input in self.songs:
                section.append(self.songs[user_input])
            else: 
                result=self.songs[self.findSong(user_input)]
                if result:
                    section.append(result)
        
        self.worship=section
    def getSlide(self,file_name):
        text="\\includepdf{"
        text+=file_name+".png"
        text+="}\n"
        return text
    def write(self):
        text=self.preamble()
        text+="\\begin{document}\n\n"
        for slide in self.beforeWorship:
            text+=self.getSlide(slide)
        for request in self.worship:
            text+="\\section{ "
            text+=request.title
            text+=" }\n\n"
            text+=request.write(self.language,self.uniformSize)
        for slide in self.afterWorship:
            text+=self.getSlide(slide)
        text+="\\end{document}"
        return text
class File(Document):
    def __init__(self,name,title,author,language="Eng",songs=song,aspect_ratio="169",theme="Berlin",Ecolour="0056B8",Wcolour="222222",logo_address="CU_logo.jpeg",uniformSize=True,beforeWorship=["1","2","3"],worship=[],afterWorship=["4"]):
        super().__init__(name,title,author,language,songs,aspect_ratio,theme,Ecolour,Wcolour,logo_address,uniformSize)
        self.type='file'
    def dictionarify(self):
        global docu
        docu["file"][self.name]={"name":self.name,"title":self.title,"author":self.author,"language":self.language,"aspect_ratio":self.aspect_ratio,
                  "theme":self.theme,"Ecolour":self.Ecol,"Wcolour":self.Wcol,"logo_address":self.logo_address,
                  "uniformSize":self.uniformSize,"beforeWorship":self.beforeWorship,"worship":[request.nameRef() for request in self.worship],
                  "afterWorship":self.afterWorship}  
    def rename(self,new_name):
        docu["file"].pop(self.name)
        self.name=new_name
        self.dictionarify()              
    
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
    for doc in documents.values():
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
    
def classifyDoc(document,type_of_doc):
    if type_of_doc=='document':
        documents[document["name"]]=Document(**document)
    elif type_of_doc=='equip':
        documents[document["name"]]=Equip(**document)
    elif type_of_doc=='file':
        documents[document["name"]]=File(**document)
    return documents[document["name"]]

for document in docu["document"].values():
    documents[document["name"]]=Document(**document)
for document in docu["equip"].values():
    documents[document["name"]]=Equip(**document)
for document in docu["file"].values():
    documents[document["name"]]=File(**document)
#%% TKinter

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import colorchooser

def on_close():
    # Ask the user for confirmation
    response = tk.messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
    
    if response:  # User chose "Yes"
        save()  # Save the content of the text widget
        root.destroy()  # Close the window
    elif response is False:  # User chose "No"
        root.destroy()  # Close the window
    # If response is None (Cancel), do nothing

def shuffle(widget):
    pos=widget.grid_info()
def shuffleSelect(widget,flag=True):
    pos=widget.grid_info()
    if flag:
        pos['row']+=10
        flag=False
    else:
        pos['row']-=10
        flag=True
    widget.grid(**pos)
    
class MultilineEntry(tk.Text):
    def update_size(self,event=None):
        # Get the number of lines and the longest line
        lines = self.get("1.0", "end-1c").split("\n")
        max_width = max(len(line) for line in lines)
        max_width= max(max_width,25)
        height = len(lines)    
        # Update the widget size
        self.config(width=max_width, height=height)
    def __init__(self,parent,textvariable,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.insert('1.0',textvariable)
        self.update_size()
        self.grid(row=0,column=0,sticky='nwes')
        self.bind("<KeyRelease>", self.update_size)

class Menubar(tk.Menu):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(*args,**kwargs)
        

        #Documents menu
        self.doc_menu=tk.Menu(self)
        self.add_cascade(menu=self.doc_menu, label='Documents')
        for instance in docu["document"].keys():
            self.doc_menu.add_command(label=instance,command=lambda i=documents[instance]:make_document_frame(i))
        if docu["equip"]:
            self.doc_menu.add_separator()
            self.doc_menu.add_command(label="Meeting slides")
            for instance in docu["equip"].keys():
                self.doc_menu.add_command(label=instance,command=lambda i=documents[instance]:make_document_frame(i))
        if docu["file"]:
            self.doc_menu.add_separator()
            self.doc_menu.add_command(label="Lyric files")
            for instance in docu["file"].keys():
                self.doc_menu.add_command(label=instance,command=lambda i=documents[instance]:make_document_frame(i))

        #song editor
        self.add_command(label="Song editor",command=make_song_frame)
        
class SongEditor(ttk.Frame):
    #def updateSanza(self,i,stanza):
    def writeStanzaFrame(self,i,j,stanza):
        self.var[i][j]={}
        fr=ttk.Frame(self.lyrics)#frame containing each language of stanza
        fr.grid(row=i*2,column=j,sticky='nsew')
        for k,slide in enumerate(stanza[j]):
            self.var[i][j][k]=tk.StringVar()
            try:
                #for single language stanzas
                self.var[i][j][k].set('\n'.join(slide))
            except:
                #for bilingual stanza
                self.var[i][j][k].set('\n'.join(['\n'.join(line) for line in slide]))
            label=ttk.Label(fr,textvariable=self.var[i][j][k])
            label.grid(row=(k*2)+1,column=0,sticky='nw')
            sep = ttk.Separator(fr, orient="horizontal")
            sep.grid(row=(k*2),column=0,sticky='we')#separator at top of each slide
        #at end of stanza frame:
        stanza_buttons=ttk.Frame(fr)
        stanza_buttons.grid(row=(k*2)+3,column=0,sticky='w')
        if stanza[j][0]:
            split_slides=ttk.Label(stanza_buttons,text='split')
            split_slides.grid(row=0,column=0)
            split_slides.bind("<Button-1>",lambda e,s=stanza[j]:self.splitCommand(s,e))
        if j!=4:
            edit_stanza=ttk.Label(stanza_buttons,text='edit')
            edit_stanza.grid(row=0,column=1)
            edit_stanza.bind("<Button-1>",lambda e,s=stanza[j],i=i,j=j,f=fr:self.editStanza(s, i, j, f, e))
        else:
            update_button=ttk.Label(stanza_buttons,text='update')
            update_button.grid(row=0,column=1)
            update_button.bind("<Button-1>",lambda e,i=i,s=stanza,f=fr:self.updateBil(i, s, f, e) )
    def updateBil(self,i,stanza,frame,*args):
        self.song.updateBil(i)
        self.writeStanzaFrame(i,4,self.song.lyrics[i])
        frame.grid_forget()
    def writeStanza(self,i,stanza):
        
        self.var[i]={}
        self.var[i][0]=tk.StringVar()
        self.var[i][0].set(stanza[0])
        lfr=ttk.Frame(self.lyrics)#frame containing stanza label
        lfr.grid(row=i*2,column=0,sticky='nw')#frame for the stanza label
        label=ttk.Label(lfr,textvariable=self.var[i][0])
        label.grid(row=0,column=0,sticky='nw')
        #rename_label=ttk.Button(lfr,text="rename",width=7,command=lambda l=label,s=stanza:editInfo(l,rename_label,self.song,s[0],mesg="rename"))
        #rename_label.grid(row=1,column=0,sticky='w')
        shuffle=ttk.Button(lfr,text='shuffle',width=7)
        shuffle.grid(row=2,column=0,sticky='w')
        for j in [2,3,4]:#for the lyrics parts of the stanza tuple
            self.writeStanzaFrame(i, j, stanza)
            
    def editStanza(self,stanza,i,j,frame,*args):
        
        #obtain grid information for frame
        pos=frame.grid_info()
        #create new frame to replace it
        new_frame=ttk.Frame(self)
        new_frame.columnconfigure(0,weight=1)
        new_frame.rowconfigure(0,weight=1)
        words=''
        for slide in stanza:#collect slides into one text variable
            words+='\n'.join(slide)
        
        #entry box to edit stanza
        entry=MultilineEntry(new_frame, words)
        #save button
        save_button=ttk.Button(new_frame,text='Save',command=lambda s=stanza,i=i,j=j,f=new_frame,e=entry:self.saveStanza(s,i,j,f,e))
        save_button.grid(row=1,column=0)
        #swap frames
        new_frame.grid(**pos)
        frame.grid_forget()
    def saveStanza(self,stanza, i, j, frame, entry):
        edited=entry.get('1.0', 'end')
        edit=edited.split('\n')
        edit=[line for line in edit if line]#remove empty lines
        new_stanza_list=[]
        for l in range(5):
            if l!=j:
                new_stanza_list.append(self.song.lyrics[i][l])
            else:
                new_stanza_list.append([edit])
        new_stanza_tuple=tuple(new_stanza_list)
        self.song.lyrics[i]=new_stanza_tuple
        self.writeStanzaFrame(i, j, self.song.lyrics[i])
        frame.grid_forget()
    def splitCommand(self,stanza,*args):
        return
    def infoFrame(self):
        info=ttk.Frame(self)
        ttk.Label(info,text='English title:').grid(row=0,column=0)
        ttk.Label(info,text='Welsh title:').grid(row=1,column=0)
        ttk.Label(info,text='Artist/author:').grid(row=0,column=6)
        
        self.song_title=ttk.Label(info,textvariable=self.titlevar)
        self.title_edit=ttk.Button(info,text="change",command=lambda: editInfo(self.song_title,self.title_edit,self.song,'title'))
        self.song_title.grid(row=0,column=1)
        self.title_edit.grid(row=0,column=2)
        
        self.song_Wtitle=ttk.Label(info,textvariable=self.Wtitlevar)
        self.Wtitle_edit=ttk.Button(info,text="change",command=lambda: editInfo(self.song_Wtitle,self.Wtitle_edit,self.song,'Wtitle'))
        self.song_Wtitle.grid(row=1,column=1)
        self.Wtitle_edit.grid(row=1,column=2)
        
        self.song_art=ttk.Label(info,textvariable=self.artvar)
        self.art_edit=ttk.Button(info,text="change",command=lambda: editInfo(self.song_art,self.art_edit,self.song,'artist'))
        self.song_art.grid(row=0,column=7)
        self.art_edit.grid(row=0,column=8)
        
        ttk.Label(info,text='Other titles:').grid(row=0,column=3)
        
        ttk.Label(info,text='Category:').grid(row=1,column=6)
        
        self.song_alttitles=ttk.Label(info,textvariable=self.alttitlesvar)
        self.alttitles_edit=ttk.Button(info,text="change",command=lambda: editInfo(self.song_alttitles,self.alttitles_edit,self.song,'alttitles'))
        self.song_alttitles.grid(row=0,column=4)
        self.alttitles_edit.grid(row=0,column=5)
        
        self.song_Walttitles=ttk.Label(info,textvariable=self.Walttitlesvar)
        self.Walttitles_edit=ttk.Button(info,text="change",command=lambda: editInfo(self.song_Walttitles,self.Walttitles_edit,self.song,'Walttitles'))
        self.song_Walttitles.grid(row=1,column=4)
        self.Walttitles_edit.grid(row=1,column=5)
        
        self.song_cat=ttk.Label(info,textvariable=self.catvar)
        self.cat_edit=ttk.Button(info,text="change",command=lambda: editInfo(self.song_cat,self.cat_edit,self.song,'cat'))
        self.song_cat.grid(row=1,column=7)
        self.cat_edit.grid(row=1,column=8)
        return info
    def newStanza(self):
        i=len(self.song.lyrics)
        self.song.lyrics.append(('','',[[]],[[]],[[]]))
        self.writeStanza(i, self.song.lyrics[i])
    def __init__(self,parent,song,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.song=song
        self.var={}
        self.titlevar=tk.StringVar(value=self.song.title)
        self.Wtitlevar=tk.StringVar(value=self.song.Wtitle)
        self.artvar=tk.StringVar(value=self.song.artist)
        self.alttitlesvar=tk.StringVar(value=self.song.alttitles)
        self.Walttitlesvar=tk.StringVar(value=self.song.Walttitles)
        self.catvar=tk.StringVar(value=self.song.cat)
        self.info=self.infoFrame()
        self.lyrics=ttk.Frame(self)
        for i,stanza in enumerate(self.song.lyrics):
            self.writeStanza(i, stanza)
        self.new_stanza_button=ttk.Button(self,text='New stanza',width=12,command=self.newStanza)
        self.new_stanza_button.grid(row=2,column=0,sticky='e')
        self.lyrics.grid_columnconfigure(0,minsize=40)
        self.lyrics.grid_columnconfigure(2,minsize=270)
        self.lyrics.grid_columnconfigure(3,minsize=270)
        self.lyrics.grid_columnconfigure(4,minsize=270)
        
        self.info.grid(row=0,column=0)
        self.lyrics.grid(row=1,column=0)
        
                
            
class DocumentEditor(ttk.Frame):
    def editSong(self,a_song):
        edit_window=tk.Toplevel(root)
        edit_window.title=a_song.title
        SongEditor(edit_window, a_song).grid(row=0,column=0)
    def infoCreate(self,song,index,event):
        global info
        flag=False
        try:
            pos=self.info.grid_info()
            if pos['row']!=index: flag=True
        except:flag=True
        finally:
            self.info.destroy()
            if flag:
                self.info=ttk.Frame(self.song_check)
                self.info.grid(column=0,row=index,columnspan=2,sticky='ew') 
                self.info_label=ttk.Label(self.info,text=song.getInfo())
                self.info_label.grid(column=0,row=0,sticky='w')
                self.info_button=ttk.Button(self.info,text="View",width=5,command=lambda s=song: self.editSong(s))
                self.info_button.grid(column=1,row=0,sticky='se')
    def updateSelection(self,a_song):
        if self.a[a_song.nameRef()].get()==1:
            self.file.songs[a_song.nameRef()]=a_song
        else: self.file.songs.pop(a_song.nameRef(),None)
    def onDelete(self):
        # Ask the user for confirmation
        response = tk.messagebox.askyesno("Delete document", "Are you sure you want to delete this document?\nThis document will be permanently deleted")
        
        if response:  # User chose "Yes"
            self.file.delete()  # Save the content of the text widget
            self.grid_forget()
            root['menu']=Menubar(root)
            make_document_frame(documents["CU lyrics"])
            del self
        
    def __init__(self,parent,doc,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.grid(column=0, row=0, sticky="nwes")
        self.columnconfigure(0,weight=3)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        
        self.file=doc
        

        ######parameter window
        self.doc_params=ttk.Frame(self)
        self.doc_params.grid(column=0,row=0,sticky="N")

        #create stringvars for each parameter
        self.namevar=tk.StringVar()
        self.titlevar=tk.StringVar()
        self.authvar=tk.StringVar()
        self.logovar=tk.StringVar()
        self.ratvar=tk.StringVar()
        self.langvar=tk.StringVar()
        self.themevar=tk.StringVar()
        self.ecolvar=tk.StringVar()
        self.wcolvar=tk.StringVar()
        self.sizevar=tk.BooleanVar()
        self.namevar.set(self.file.name)
        self.titlevar.set(self.file.title)
        self.authvar.set(self.file.author)
        self.logovar.set(self.file.logo_address)
        self.ratvar.set(self.file.aspect_ratio)
        self.langvar.set(self.file.language)
        self.themevar.set(self.file.theme)
        self.ecolvar.set('#'+self.file.Ecol)
        self.wcolvar.set(self.file.Wcol)
        self.sizevar.set(self.file.uniformSize)

        # Open logo image using Pillow
        #image = Image.open(file.logo_address)

        # Convert the Image object to a Tkinter-compatible PhotoImage object
        #photo = ImageTk.PhotoImage(image)

        self.doc_name=ttk.Label(self.doc_params, textvariable=self.namevar,font="TkHeadingFont")
        self.name_edit=ttk.Button(self.doc_params,text="change",command=lambda: editInfo(self.doc_name,self.name_edit,self.file,'name'))

        ttk.Label(self.doc_params,text="Title").grid(column=0,row=1,sticky='w')
        self.doc_title=ttk.Label(self.doc_params,textvariable=self.titlevar)
        self.title_edit=ttk.Button(self.doc_params,text="change",command=lambda: editInfo(self.doc_title,self.title_edit,self.file,'title'))

        ttk.Label(self.doc_params,text="Author").grid(column=2,row=1,sticky='w')
        self.doc_auth=ttk.Label(self.doc_params,textvariable=self.authvar)
        self.auth_edit=ttk.Button(self.doc_params,text="change",command=lambda: editInfo(self.doc_auth,self.auth_edit,self.file,'author'))

        ttk.Label(self.doc_params,text="Logo").grid(column=4,row=1,sticky='w')
        self.doc_logo=ttk.Label(self.doc_params,textvariable=self.logovar)
        self.logo_edit=ttk.Button(self.doc_params,text="change",command=lambda: editInfo(self.doc_logo,self.logo_edit,self.file,'logo_address'))
        #logo_thumb=ttk.Label(doc_params,image=photo)#at present, this won't update

        ttk.Label(self.doc_params,text="Theme").grid(column=0,row=4,sticky='w')
        self.doc_theme=ttk.Combobox(self.doc_params,textvariable=self.themevar)
        self.doc_theme.bind('<<ComboboxSelected>>',lambda e,d=self.themevar.get(): self.file.update('theme',d,e))
        self.doc_theme['values']=('Berlin',)

        ttk.Label(self.doc_params,text="Aspect ratio").grid(column=2,row=4,sticky='w')
        self.doc_rat=ttk.Combobox(self.doc_params,textvariable=self.ratvar)
        self.doc_rat.bind('<<ComboboxSelected>>',lambda e,d=self.ratvar.get(): self.file.update('aspect_ratio',d,e))
        self.doc_rat['values']=('169','43','1610','149','54','32')
        self.doc_rat.state(["readonly"])

        ttk.Label(self.doc_params,text="Uniform size").grid(column=4,row=4,sticky='w')
        self.doc_size=ttk.Checkbutton(self.doc_params,text="Make font size uniform for each song",variable=self.sizevar,command=lambda:self.file.update('uniformSize',self.sizevar.get()))

        """
        def chooseColour(event,variable):
            variable.set(colorchooser.askcolor(initialcolor='#ff0000'))
        ttk.Label(doc_params,text="English colour").grid(column=2,row=6,sticky='w')
        doc_ecol=ttk.Entry(doc_params)
        doc_ecol.winfo_rgb(color=ecolvar.get())
        doc_ecol.grid(column=2,row=7)
        doc_ecol.bind("<Button-1>",lambda e,c=ecolvar:chooseColour(e,c))
        """
        self.delete_button=ttk.Button(self.doc_params,text='delete',command=self.onDelete)
        self.create_button=ttk.Button(self.doc_params,text="Create",command=self.file.create)

        self.doc_name.grid(column=0,row=0,columnspan=5)
        self.name_edit.grid(column=10,row=0)
        self.doc_title.grid(row=2,column=0,sticky='w')
        self.title_edit.grid(row=2,column=1,sticky='w')
        self.doc_auth.grid(row=2,column=2,sticky='w')
        self.auth_edit.grid(row=2,column=3,sticky='w')
        self.doc_logo.grid(column=4,row=2,sticky='w')
        self.logo_edit.grid(column=5,row=2,sticky='w')
        #self.logo_thumb.grid(column=4,row=3,columnspan=2)
        self.doc_theme.grid(column=0,row=5,columnspan=2,sticky='w')
        self.doc_rat.grid(column=2,row=5,columnspan=2,sticky='w')
        self.doc_size.grid(column=4,row=5,columnspan=2,sticky='w')
        self.delete_button.grid(column=9,row=10)
        self.create_button.grid(column=10,row=10)




        ######song selection window
        self.song_check_canvas=tk.Canvas(self,width=245)#canvas is scrollable
        self.song_check_canvas.grid(column=1,row=0,sticky="nse")


        self.song_check=ttk.Frame(self.song_check_canvas)#frame inside canvas
        self.song_check.grid(column=0,row=0,sticky='ew')

        ###scrollbar for songs
        self.song_check_scroll=ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.song_check_canvas.yview)
        self.song_check_scroll.grid(column=2,row=0, sticky="ns")

        self.song_check_canvas.create_window((0, 0), window=self.song_check, anchor="nw")
        self.song_check_canvas.configure(yscrollcommand=self.song_check_scroll.set)

        # Configure the scrollable frame
        self.song_check.bind(
            "<Configure>",
            lambda e: self.song_check_canvas.configure(scrollregion=self.song_check_canvas.bbox("all")))



        #dictionary to hold info on inclusion of songs in document
        self.a={} 
        for a_song in song.keys():
            if a_song in self.file.songs.keys():
                self.a[a_song]=tk.IntVar(value=1)
            else: self.a[a_song]=tk.IntVar()
            
        
                    
                    
        #checkbutton for each song
        sorted_song = {key: song[key] for key in sorted(song)}
        for i,a_song in enumerate(sorted_song.values()):
            ttk.Checkbutton(self.song_check,text=a_song.uniqueEntry(a_song.title,self.file.language),variable=self.a[a_song.nameRef()],command=lambda s=a_song:self.updateSelection(s)).grid(column=0,row=i*2,sticky="w")
            elipsis=ttk.Label(self.song_check,text="...")
            elipsis.bind("<Button-1>",lambda e,s=a_song, j=(2*i)+1: self.infoCreate(s,j,e))
            elipsis.grid(column=1,row=i*2,sticky="e")

        self.info=ttk.Label(self.song_check)    



def editInfo(textwidget,buttonwidget,file,attr,mesg="change"):
    parent=root.nametowidget(textwidget.winfo_parent())
    grid=textwidget.grid_info()
    var=textwidget.cget("textvariable")
    font=textwidget.cget("font")
    textwidget.destroy()        
    textwidget=ttk.Entry(parent,textvariable=var)
    if attr=="name":
        buttonwidget.config(text="update",command=lambda: saveName(textwidget,buttonwidget,file,attr,font,mesg))
    else:
        buttonwidget.config(text="update",command=lambda: saveInfo(textwidget,buttonwidget,file,attr,font,mesg))
    textwidget.grid(**grid)

def asksaveoverwrite(title, message):
    def on_save():
        nonlocal result
        result = True
        dialog.destroy()

    def on_overwrite():
        nonlocal result
        result = False
        dialog.destroy()
        
    def on_cancel():
        nonlocal result
        result = None
        dialog.destroy()
        

    result = None
    dialog = tk.Toplevel()
    dialog.title(title)
    
    dialog.resizable(False, False)

    label = tk.Label(dialog, text=message, wraplength=250)
    label.grid(column=0,row=0)

    button_frame = tk.Frame(dialog)
    button_frame.grid(column=0,row=1,sticky='ew')
    for i in range(3):
        button_frame.columnconfigure(i,weight=1)

    save_button = ttk.Button(button_frame, text="Save", command=on_save)
    save_button.grid(column=0,row=0)

    overwrite_button = ttk.Button(button_frame, text="Overwrite", command=on_overwrite)
    overwrite_button.grid(column=1,row=0)
    
    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.grid(column=2,row=0)

    dialog.transient()  # Make the dialog modal
    dialog.grab_set()
    dialog.wait_window()
    return result
    
def saveName(textwidget,buttonwidget,file,attr,font,mesg):   
    old_file=getattr(file, 'name')#obtain details before update
    type_of_file=getattr(file, 'type')
    var=textwidget.cget("textvariable")
    new_name=root.getvar(name=var)
    if old_file!=new_name:
        query=asksaveoverwrite('Change of document name','You have changed the name of the document\nDo you wish to save as a new document, or overwrite the existing one?\nIf save is selected, the original document will revert to the previous save')
        if query:
            saveInfo(textwidget,buttonwidget,file,attr,font,mesg)#save change
            new_file=getattr(file, 'name')#obtain new details
            #save to dictionary and reload original and new as objects
            file.dictionarify()
            new_doc=classifyDoc(docu[type_of_file][new_file],type_of_file)
            classifyDoc(docu[type_of_file][old_file],type_of_file)
            #refresh view
            root['menu']=Menubar(root)
            make_document_frame(new_doc)
        elif query==False:
            saveInfo(textwidget,buttonwidget,file,attr,font,mesg)#save change
            new_file=getattr(file, 'name')#obtain new details
            #save to dictionary and reload new
            file.dictionarify()
            new_doc=classifyDoc(docu[type_of_file][new_file],type_of_file)
            #delete old
            file.delete()
            #refresh view
            root['menu']=Menubar(root)
            make_document_frame(new_doc)
        else:saveInfo(textwidget,buttonwidget,file,attr,font,mesg,change=False)
    else:saveInfo(textwidget,buttonwidget,file,attr,font,mesg)
    
        
        
    
def saveInfo(textwidget,buttonwidget,file,attr,font,mesg,change=True):
    parent=root.nametowidget(textwidget.winfo_parent())
    grid=textwidget.grid_info()
    var=textwidget.cget("textvariable")
    if change:
        file.update(attr,root.getvar(name=var))
    else:
        vari=tk.StringVar()
        vari.set(getattr(file, attr))
        print(getattr(file, attr))
    textwidget.destroy()        
    if change:
        textwidget=ttk.Label(parent,textvariable=var,font=font)
    else:
        textwidget=ttk.Label(parent,textvariable=vari,font=font)
    buttonwidget.config(text=mesg,command=lambda: editInfo(textwidget,buttonwidget,file,attr,mesg))
    textwidget.grid(**grid)
    



############create root window
root=tk.Tk()
root.title("Lyrics manager")
root.geometry('1250x600')
root.protocol("WM_DELETE_WINDOW", on_close)


############song view
list_of_songs=[a_song for a_song in song.values()]
list_of_songs=sorted(list_of_songs, key=lambda x: x.uniqueEntry(x.title,'Eng'))
def updateDetails(event,index):
    global editor
    try:
        editor.destroy()
    except: pass
    try:
        editor=SongEditor(song_frame,filtered_songs[index[0]])
    except:
        try:
            editor=SongEditor(song_frame,list_of_songs[index[0]])
        except: pass
    finally:
        editor.grid(column=1,row=0,rowspan=2,sticky='n')
    

song_frame=ttk.Frame(root,padding="5 5 5 5")

def on_focus_in(event):
    if search_bar.get() == "Search":
        search_bar.delete(0, tk.END)

def on_focus_out(event):
    if search_bar.get() == "":
        search_bar.insert(0, "Search")
        
def update_listbox(*args):
    """Filter the Listbox items based on the search query."""
    global song_list
    global filtered_songs
    search_query = search_var.get().lower()
    if search_query!="search":
        filtered_songs = [a_song for a_song in list_of_songs if search_query in a_song.nameRef().lower()]
    else: filtered_songs=list_of_songs
    filtered_items=[a_song.uniqueEntry(a_song.title,'Eng') for a_song in filtered_songs]
    listvar=tk.StringVar(value=filtered_items)
    song_list['listvariable']=listvar

search_var=tk.StringVar()



search_bar = tk.Entry(song_frame, textvariable=search_var, width=37)
search_bar.grid(row=0,column=0)
search_bar.insert(0, "Search")

search_bar.bind("<FocusIn>", on_focus_in)
search_bar.bind("<FocusOut>", on_focus_out)

list_of_song_names=[a_song.uniqueEntry(a_song.title,'Eng') for a_song in list_of_songs]
listvar=tk.StringVar(value=list_of_song_names)

song_list=tk.Listbox(song_frame,listvariable=listvar,width=37)
song_list.bind("<<ListboxSelect>>", lambda e: updateDetails(e,song_list.curselection()))
song_list.grid(column=0,row=1,sticky='ns')
search_var.trace("w", update_listbox)

song_frame.rowconfigure(1,weight=1)
song_frame.columnconfigure(1,weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


root.option_add('*tearOff', tk.FALSE)#prevents menus from tearing off
#
#
#
def make_document_frame(doc):
    global doc_frame
    global song_frame
    try:doc_frame.grid_remove()
    except:pass
    doc_frame=DocumentEditor(root, doc)
    song_frame.grid_remove()
def make_song_frame():
    global doc_frame
    global song_frame
    song_frame.grid(row=0,column=0,sticky='nwes')
    doc_frame.grid_remove()
#create menubar#

root['menu'] = Menubar(root)


#
#
make_document_frame(documents["CU lyrics"])

  
root.mainloop()