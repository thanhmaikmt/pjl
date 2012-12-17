CLASSDIR=/home/pjl/classes

# compile usercode Java

all:
	javac -g -classpath "..:/home/pjl/classes/JSynClasses.jar" -deprecation *.java

docs:
	javadoc -d doc  *.java

clean:
	-rm -f *.class */*.class
	-rm -f \#* */\#*	
	
