ALLCVS:= $(shell ls *.java Makefile )
ROOT=../../../.. 
JAVAFLAGS =  -source 1.3 -classpath ${ROOT} ${OPT}

all:
	javac ${JAVAFLAGS} *.java 


add:
	cvs add ${ALLCVS}

commit:
	cvs commit ${ALLCVS}

clean:
	rm -f ${ROOT}/uk/ac/bath/util/*.class
