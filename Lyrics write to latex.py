# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 10:42:41 2025

@author: charl
"""

"""
The aim of this file is to take text files as inputs, each containing 
marked up lyrics to one song, and write command promts to the LaTeX
file for the lyrics presentation.
For each file/song, the code will need to generate:
    -suitably formatted lyric slides
    -internal navigation hyperlinks
    -contents/hyperlink entries in the main contents and relevent subcontents pages
    (May add stylistic contents pages, i.e.Modern/Contemporary/Traditional)
    
    -the slides will need to be placed in correct alphabetical position
    -the contents page entries are to be in alphabetical position
    -the code will need to detect when a contents column is full, and nudge entries into
    the next column/slide
    
"""
# %%
"""
**********************************************************************
Format for input lyrics:

English title- if none, leave empty line
W-welsh title follows W- with no space- if none, this line should not exist
category (1=Traditional,2=Contemporary,3=Modern)
any alernate titles such as first line
go in immediately following lines
W-Welsh alternate titles follow W- with no space

artist name, if required to distingish a song, goes after exactly 1 blank line

after this, spaces make no difference, and until the first
stanza label, nothing else is read

a line of 3 or less characters is interpereted as a stanza label (unless [] used),
and will appear as an internal hyperlink to navigate between stanzas
verse numbers and C (for chorus) are suggested
other potential choices may be B or Br (bridge); C1 , C2 (if choruses change);
I or Int (intro); O or Out (outro)

1
What is written here will
be taken as lines in a stanza
with "1" as the label, 
usually meaning verse 1
W
If there are welsh lyrics for a stanza,
write them after a W line

C
W
If a stanza has only welsh lyrics,
simply make the stanza label followed by the W line

2
a stanza will be made up of all 
lines until the next stanza reference,
or the end of the document,

ignoring all blank lines
3
if some lines are very long, consider breaking them up- this one would format very oddly. 
It's better that this is done manually to avoid the code breaking the line in an unusual place.
likewise if a staza has a lot of lines
then consider breaking it up with a hyphen
-
on a single line in a logical place
this will allocate it into 2 stanzas
the second will be labeled with a "-"
this prevents overcrowded slides
**************************************************************************
"""
# %%



r"""template for song entry
{\setbeamertemplate{footline}
{% 
 {\usebeamerfont{section in head/foot}
 \begin{beamercolorbox}[ht=4.5ex,dp=1.5ex,%
      leftskip=.3cm,rightskip=.3cm plus1fil]{section in head/foot}
   \usebeamercolor[fg]{section in head/foot}%
   \fontsize{12}{25}\selectfont 
 \hyperlink{<songname>1}{1}  \hyperlink{<songname>C}{C}  \hyperlink{<songname>2}{2}
    ####these hyperlinks are the only things that change in this section
 \end{beamercolorbox}%
  \begin{beamercolorbox}[ht=2.5ex,dp=1.125ex,%
   leftskip=.3cm,rightskip=.3cm plus1fil]{subsection in head/foot}
   \insertauthor
 \end{beamercolorbox}%
 }
}
\subsection{<songname>}
\hypertarget{<songname>1}{}
\begin{frame}{<songname>}
\fontsize{21}{28}\selectfont %set font size and line spacing

As the deer pants for the water\\
so my soul longs after You\\
You alone are my heart's desire\\
and I long to worship You
\end{frame}
\hypertarget{<songname>C}{}
\begin{frame}{}
\fontsize{21}{28}\selectfont %as previous

You alone are my strength, my shield,\\
To You alone may my spirit yield,\\
You alone are my heart's desire\\
and I long to worship You
    
\end{frame}
\hypertarget{<songname>2}{}
\begin{frame}{}
\fontsize{21}{28}\selectfont %as previous

You're my friend and You are my brother\\
even though You are a King,\\
I love You more than any other,\\
so much more than anything
    
\end{frame}
}

"""
# %%Function to print the formatted song slides to latex file

A=r"""{\setbeamertemplate{footline}
{ 
 {\usebeamerfont{section in head/foot}
 \begin{beamercolorbox}[ht=4.5ex,dp=1.5ex,%
      leftskip=.3cm,rightskip=.3cm plus1fil]{section in head/foot}
 \usebeamercolor[fg]{section in head/foot}%
 \fontsize{12}{25}\selectfont """
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

#} at end of all


def printsong(file):
    print(f"%*%{title}",file=file) #break point to help locate future songs in aphabetical order
    print(A,file=file)
    leng=len(label)
    for l in range(leng): print("\hyperlink{%s%s%s%s}{%s}" %(title,alttitles,art,labell[l],label[l]),file=file)
    print(B,title,"}\n",file=file)
    print(f'{C}{title}{alttitles}{art}{D}{H}{title} {art}{I}',file=file)#title page for song
    for l in range(leng):
        print(f'{C}{title}{alttitles}{art}{labell[l]}{D}{E}',textsize,"}{",colsep,f'{F}\n{stanzas[l]}',G,file=file)#stanza slides
    #last bracket ends the hyperlinks in the footnote environment 
    print("}",file=file)
    
    
"""
Need to create a method fror spreding a contents list over multiple slides (if overful)
This will also entail making a way for a multi-slide contents list to be read effectively.
So long as column environment is not used for anything other than contents lists, the present method will only
need adjusting by targetting the final use of \end{columns}

Another issue to resolve is that of contents entries taking multiple lines, thus upsetting the distribution


"""
def list_rindex(li, x):
    for i in reversed(range(len(li))):
        if li[i] == x:
            return i
    raise ValueError("{} is not in list".format(x))
#helpful function to inverse the index function and find last instance of an object
    
def add_to_contents(location,entries):
   
    location=location.splitlines()

    #mark lines which remain unchanged at start and end
    firstlines=location.index(r"\begin{columns}[t]")
    lastlines=list_rindex(location,r"\end{columns}")#changing to last instance ensures reading all contents entries,
    #but will cause problems if column environment is used elsewhere- PLEASE DO NOT DO THIS!
    #an edit could be made to remove this issue- if this is desired, lines could be added to the LaTeX template
    #as markers, so that the index function can be used on these lines instead of the column commands
    #obviously, these lines should begin with % so LaTeX does not read them
    lastline=len(location)

    #read list elements from section contents page
    sectioncontents=[line for line in location if r'\item \hyperlink' in line]

    #add new entry
    for entry in entries:
        if entry==title:
            reference=f"{entry} {art}"            
        else:
            reference=f"{entry} ({title})"
        phantom=""
        while len(reference)+len(phantom)<35:
            phantom+=" 1" #phantom text added to ensure all contents entries occupy at least 2 lines
            
        sectioncontents.append("    \\item \\hyperlink{%s%s%s}{%s} \\phantom{%s}"%(title,alttitles,art,reference,phantom))
            
        
    
    sectioncontents=sorted(sectioncontents, key=lambda x: x.split("{")[2])


    newtext=""
    for line in range(firstlines+1):newtext+="%s\n"%(location[line])
    A=6
    B=5#maximum lengths of columns for first slide of contents
    while sectioncontents:
        newtext+="""\\column{0.05\\textwidth}
        \\column{0.45\\textwidth}
        \\begin{itemize}\n"""
        
        if len(sectioncontents)<A+B:
            A=int((len(sectioncontents)+1)/2)
            B=int(len(sectioncontents)/2)#if slide underful, evenly distribute between columns
        elif A+B<len(sectioncontents)<A+B+4:
            A=A-1
            B=B-1#ensures next slide never has less than 3 entries- slightly evens distribution between slides

        for entry in range(A): 
            if sectioncontents: newtext+="%s\n"%(sectioncontents.pop(0))
            else: newtext+="    \\item[] \\phantom{1}"

        newtext+="""\\end{itemize}
        \\column{0.45\\textwidth}
        \\begin{itemize}
        """

        for entry in range(B): 
            if sectioncontents: newtext+="%s\n"%(sectioncontents.pop(0))
            else: newtext+="    \\item[] \\phantom{1}"
        if sectioncontents:
            newtext+="""    \\item[] \\textit{Continued on next slide...}
            \\end{itemize}
            \\column{0.05\\textwidth} 
            \\end{columns}
            \\end{frame}
            \\begin{frame}[t]
            \\begin{columns}[t]
            """
        else: newtext+="    \\item[] \\phantom{1}"
        A=7
        B=6#maximum lengths of columns for subsequent slides of contents (longer due to lack of header)
    
    newtext+="\\end{itemize}\n \\column{0.05\\textwidth} \n\n"
    for line in range(lastlines-1,lastline):newtext+="%s\n"%(location[line])
    location=newtext
    return location

"""
perhaps use \phantom{text} to make all entries the same number of characters long, thus spaced equally

"""
    
#############edit this to make sure all subequent lines included            
#############start each section with  %**%A (or relevent letter)   
# %%

#open files

title=''
cat=''
ref=''
label=''
labell=''
art=''
textsize=''
colsep=''
alttitles=''
stanzas=''

"""
Begin by reading the song and preparing it into appropriate format
"""
def read_song(file):
    global title
    global Wtitle
    global cat
    global ref
    global Wref
    global label
    global labell
    global art
    global textsize
    global colsep
    global alttitles
    global Walttitles
    global stanzas
    global Wstanzas
    s=open(file,"r")
    ref=[]
    Wref=[]
    label=[]
    labell=[]

    song= s.readlines()

    #close song file
    s.close()

    song=[line.rstrip() for line in song] #removes \n and spaces from each line

   
    title=Wtitle=False
    
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
        if len(song[a])<=3 and song[a]!="W" and not '['in song[a]: #any line no more than 3 characters interpreted as stanza label, unless [] used, or W
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
        
            

    #ascertain longest line length to choose font size
    longest=len(max(song,key=len)) #length of longest line
    if longest>61:
        print("You've got a really long line in there, it might format badly")
        
    stanzlen=[]
    for i in range(len(ref)-1):
        stanzlen.append(ref[i+1]-ref[i]-1) #find length of each stanza
    bigstan=max(stanzlen) #find the longest stanza length
       
    size=[40,33,28,23,20,18,15,13]
    cols=[45,39,34,30,27,23,19,17]
    maxlen=[18,21,25,31,37,44,51,61]#lists of boundary text sizes and max string length which will fit with that size
    maxstan=[4,4,5,6,7,8,9,10]#maximum number of lines for the given textsize

    p=0
    while longest>maxlen[p] and p<7: p=p+1 #choose smaller font if line too long
    while bigstan>maxstan[p] and p<7: p=p+1 #choose smaller font if too many lines
    textsize=size[p]
    colsep=cols[p]


    #collect the stanzas

    stanzas=[[] for l in label]
    Wstanzas=stanzas
    for t in range(len(label)): 
        endEng=ref[t+1]
        for w in Wref:
            if ref[t]<w<ref[t+1]:
                endEng=w
                break
        for l in range(ref[t]+1,endEng): #append lines between stanza references
            stanzas[t].append(song[l])
        stanzas[t]="\\\ \n".join(stanzas[t]) #make each stanza a string, with \\ as newline command in LaTeX
        for l in range(endEng+1,ref[t+1]):
            Wstanzas[t].append(song[l])
    

    
    
    
        
#%%




"""
Now write to latex file
"""

def write_song(origin,destination,language):
    #open latex file
    lyrics=open(origin,"r")
    lyr=lyrics.read().split('%**') #divide into alphabetical sections (with %** as marker characters)
    lyrics.close()
    begin=''
    before=''
    after=''
    end=''

    #add to category contents
    if 0<cat<4:
        entries=[]
        if title: 
            entries.append(title)
            for a in range(len(alttitles)):
                entries.append(alttitles[a])
        if Wtitle: 
            entries.append(Wtitle)
            for a in range(len(Walttitles)):
                entries.append(Walttitles[a])
        lyr[0]=lyr[0].split('%*')
        lyr[0][cat]=add_to_contents(lyr[0][cat], entries)
        lyr[0]='%*'.join(lyr[0])
    else: print('no category given')


    l=1
    if title:
        while f'%{title.lower()}'>=lyr[l+1].lower():  
            l=l+1#find the section with the correct start letter
            if l+1==len(lyr):break
    else:
        while f'%{Wtitle.lower()}'>=lyr[l+1].lower():  
            l=l+1#find the section with the correct start letter
            if l+1==len(lyr):break

    sections=[]
    alternative_titles= alttitles + Walttitles
    for t in alternative_titles:
        a=1
        while a+1!=len(lyr) and f'%{t.lower()}'>=lyr[a+1].lower():  
            a=a+1#find the section with the correct start letter
    
        sections.append(a)#this assigns each alternate title a section into which the contents entry is inserted
 #this should ensure each entry is in the correct alphabetical section       

    for a in range(len(alternative_titles)):
        if sections[a]!=l:
            lyr[sections[a]]=add_to_contents(lyr[sections[a]],[alternative_titles[a]])
            
            
        
    for a in range(l):begin+=f'{lyr[a]}%**'#single string of all sections before
    section=lyr[l].split('%*')#relevent section split into songs
    for a in range(l+1,len(lyr)):end+=f'%**{lyr[a]}'#single string of all sections after


    #add to section contents:
    entries=[]
    alternative_titles.append(Wtitle)
    if title:
        entries=[title]
    for a in range(len(alternative_titles)):
        if sections[a]==l:
            entries.append(alternative_titles[a])
    section[0]=add_to_contents(section[0],entries)

    if title:
        t=title
    else: t=Wtitle
    l=1
    if f'%{t.lower()}'<section[-1].lower():
        while f'%{t.lower()}'>=section[l].lower(): l=l+1 #find alphabetical place within section
    else: l=len(section)
    for a in range(l):before+=f'{section[a]}%*'#single string of all songs before
    before=before[:-2]#last %* removed from 'before' and added to 'printsong()' to prevent newline affecting song order
    for a in range(l,len(section)):after+=f'%*{section[a]}'#single string of all songs after
        
    lyrics=open(destination,"w")
    print(f"{begin}{before}",file=lyrics)#f-string prevents a space between the parts, which was previously problematic
    printsong(lyrics)
    print(after,end,file=lyrics)           
    #close file          
    lyrics.close()


#%%

with open(r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\Lyrics_basic_template.txt","r") as temp:
    original=temp.read()
with open(r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\2nd draft.tex", "w") as temp:
    print(original,file=temp)
    
with open(r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\adresses.txt","r") as adresses:
    songs=adresses.readlines()
    songs=[line.rstrip() for line in songs]
for song in songs:
    read_song(song)

    write_song(r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\2nd draft.tex",r"C:\Users\charl\OneDrive\Documents\CU lyrics\CU-Lyrics\2nd draft.tex","Eng")
    
           
             

    
