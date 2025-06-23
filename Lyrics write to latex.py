# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 10:42:41 2025

@author: charl
"""

"""
The aim of this file is to take text files as inputs, each containing 
marked up lyrics to one song, and write command promts to the latex
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

title
category (1=Traditional,2=Contemporary,3=Modern)
any alernate titles such as first line
go in immediately following lines

artist name, if required to distingish a song goes after exactly 1 blank line

after this, spaces make no difference, and until the first
stanza label, nothing else is read

a line of 3 or less characters is interpereted as a stanza label,
and will appear as an internal hyperlink to navigate between stanzas
verse numbers and C (for chorus) are suggested
other potential choices may be B or Br (bridge); C1 , C2 (if choruses change);
I or Int (intro); O or Out (outro)

1
What is written here will
be taken as lines in a stanza
with "1" as the label, 
usually meaning verse 1

2
a stanza will be made up of all 
lines until the next stanza reference,
or the end of the document,

ignoring of blank lines
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
#hypertarget:
C=r"\hypertarget{"
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

#} at end of all


def printsong(file):
    print(f"%{title}",file=file) #break point to help locate future songs in aphabetical order
    print(A,file=file)
    leng=len(label)
    for l in range(leng): print("\hyperlink{%s%s%s%s}{%s}" %(title,alttitles,art,labell[l],label[l]),file=file)
    print(B,title,"}\n",file=file)
    print(f'{C}{title}{alttitles}{art}{labell[0]}{D}{title} {art}{E}',textsize,"}{",colsep,f'{F}\n{stanzas[0]}',G,file=file)#1st stanza with title
    for l in range(1,leng):
        print(f'{C}{title}{alttitles}{art}{labell[l]}{D}{E}',textsize,"}{",colsep,f'{F}\n{stanzas[l]}',G,file=file)#other stanzas with no title
    #last bracket ends the hyperlinks in the footnote environment 
    print("}",file=file)
    
def add_to_contents(location,entries):
   
    location=location.splitlines()

    #mark lines which remain unchanged at start and end
    firstlines=location.index(r"\begin{columns}")
    lastlines=location.index(r"\end{columns}")
    lastline=len(location)

    #read list elements from section contents page
    sectioncontents=[line for line in location if r'\item \hyperlink' in line]

    #add new entry
    for entry in entries:
        if entry==title:
            sectioncontents.append("    \\item \\hyperlink{%s%s%s%s}{%s %s}"%(title,alttitles,art,labell[0],entry,art))
        else:
            sectioncontents.append("    \\item \\hyperlink{%s%s%s%s}{%s (%s)}"%(title,alttitles,art,labell[0],entry,title))
        
    


    
    sectioncontents=sorted(sectioncontents, key=lambda x: x.split("{")[2])
    scontlen=len(sectioncontents)

    #number of pages the contents can fit across
    #pages=int(scontlen/24)+1
    #########################as yet unused- may be useful for troubleshooting overful contents


    newtext=""
    for line in range(firstlines+1):newtext+="%s\n"%(location[line])
    newtext+="""\\column{0.05\\textwidth}
    \\column{0.45\\textwidth}
    \\begin{itemize}\n"""

    for entry in range(min(12,int((scontlen+1)/2))):newtext+="%s\n"%(sectioncontents[entry])

    newtext+="""\\end{itemize}
    \\column{0.45\\textwidth}
    """
    if scontlen>1:
        newtext+="\\begin{itemize}\n"
        for entries in range(entry+1,min(24,scontlen)):newtext+="%s\n"%(sectioncontents[entries])
        newtext+="\\end{itemize}\n"
    newtext+="\\column{0.05\\textwidth} \n\n"
    for line in range(lastlines-1,lastline):newtext+="%s\n"%(location[line])
    location=newtext
    return location
    
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
    global cat
    global ref
    global label
    global labell
    global art
    global textsize
    global colsep
    global alttitles
    global stanzas
    s=open(file,"r")
    ref=[]
    label=[]
    labell=[]

    song= s.readlines()

    #close song file
    s.close()

    song=[line.rstrip() for line in song] #removes \n and spaces from each line

   
    title= song[0] 
    if song[1].isdigit():
        cat=int(song.pop(1))
    else: cat=0

    alttitles=[]
    art=""
    p=1
    while len(song[p])>3:
        alttitles.append(song[p])
        p=p+1
    #this interperets any lines before the first stanza label or blank line as an alternative title 
    if len(song[p])==0 and len(song[p+1])>3:
        art=f'({song[p+1]})'
    #this interperets a text line after a blank line (immediately following any titles) as an artist's name
        
    song=list(filter(None,song)) #removes empty lines  
    length=len(song) #number of lines to search for stanza labels

    for a in range(length): #search lines for stanza labels
        if len(song[a])<=3: #any line no more than 3 characters interpreted as stanza label
            ref.append(a)
            label.append(song[a]) #lists of line references and stanza labels
            while song[a] in labell:
                song[a]+="I"
            labell.append(song[a]) #the labels in labell are unique, and will be used for
                                   #hyperlink references, while those in label will be visible
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
    for t in range(len(label)):    
        for l in range(ref[t]+1,ref[t+1]): #append lines between stanza references
            stanzas[t].append(song[l])
        stanzas[t]="\\\ \n".join(stanzas[t]) #make each stanza a string, with \\ as newline command in LaTeX
    

    
    
    
        
#%%




"""
Now write to latex file
"""

def write_song(origin,destination):
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
        entries=[title]
        for a in range(len(alttitles)):
            entries.append(alttitles[a])
        lyr[0]=lyr[0].split('%*')
        lyr[0][cat]=add_to_contents(lyr[0][cat], entries)
        lyr[0]='%*'.join(lyr[0])
    else: print('no category given')


    l=1
    while f'%{title.lower()}'>=lyr[l+1].lower():  
        l=l+1#find the section with the correct start letter
        if l+1==len(lyr):break

    sections=[]
    for t in alttitles:
        a=1
        while f'%{t.lower()}'>=lyr[a+1].lower():  
            a=a+1#find the section with the correct start letter
            if a+1==len(lyr):break
        sections.append(a)
        
    for a in range(len(alttitles)):
        if sections[a]!=l:
            lyr[sections[a]]=add_to_contents(lyr[sections[a]],[alttitles[a]])
            
            
        
    for a in range(l):begin+=f'{lyr[a]}%**'#single string of all sections before
    section=lyr[l].split('%*')#relevent section split into songs
    for a in range(l+1,len(lyr)):end+=f'%**{lyr[a]}'#single string of all sections after


    #add to section contents:
    entries=[title]
    for a in range(len(alttitles)):
        if sections[a]==l:
            entries.append(alttitles[a])
    section[0]=add_to_contents(section[0],entries)


    l=1
    if f'%{title.lower()}'<section[-1].lower():
        while f'%{title.lower()}'>=section[l].lower(): l=l+1 #find alphabetical place within section
    else: l=len(section)
    for a in range(l):before+=f'{section[a]}%*'#single string of all songs before
    for a in range(l,len(section)):after+=f'%*{section[a]}'#single string of all songs after
        
    lyrics=open(destination,"w")
    print(begin,before,file=lyrics)
    printsong(lyrics)
    print(after,end,file=lyrics)           
    #close file          
    lyrics.close()


#%%

with open(r"C:\Users\charl\OneDrive\Documents\Lyrics\Lyrics_basic_template.txt","r") as temp:
    original=temp.read()
with open(r"C:\Users\charl\OneDrive\Documents\Lyrics\Song_template.txt", "w") as temp:
    print(original,file=temp)
    
with open(r"C:\Users\charl\OneDrive\Documents\Lyrics\adresses.txt","r") as adresses:
    songs=adresses.readlines()
    songs=[line.rstrip() for line in songs]
for song in songs:
    read_song(song)

    write_song(r"C:\Users\charl\OneDrive\Documents\Lyrics\Song_template.txt",r"C:\Users\charl\OneDrive\Documents\Lyrics\Song_template.txt")
    
           
             

    