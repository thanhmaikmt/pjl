ALLCVS:= $(shell ls *.java Makefile )

#JAVAFLAGS =  -deprecation -classpath ../../../..:/home/pjl/classes/java-getopt-1.0.9.jar:/home/pjl/classes/JSynClasses.jar

JAVAFLAGS =  -deprecation -classpath ../../../..	

all:
	javac -source 1.3 ${JAVAFLAGS} *.java 

run:
	java -Xmx500m -cp ../../../..:${CLASSPATH} uk.ac.bath.gui.Gui 

rungc:
	java -verbose:gc -ea -Xmx500m -cp ../../../..:${CLASSPATH} uk.ac.bath.gui.Gui 

prof:
	java -ea -Xprof -Xmx500m -cp ../../../..:${CLASSPATH} uk.ac.bath.gui.Gui 

add:
	cvs add ${ALLCVS}

commit:
	cvs commit ${ALLCVS}

clean:
	rm -f ${ROOT}/uk/ac/bath/util/*.class
