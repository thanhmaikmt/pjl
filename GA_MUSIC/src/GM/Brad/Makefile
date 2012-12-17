CLASSDIR=/home/pjl/classes
SRC := $(shell  echo *.java)
BYTE = ${SRC:.java=.class}



# compile usercode Java

all:
	javac -source 1.3 -classpath "../:/home/pjl/classes/JSynClasses.jar"  -g *.java

docs:
	javadoc -d doc  *.java

clean:
	-rm -rf ${CLASSDIR}/G
	
