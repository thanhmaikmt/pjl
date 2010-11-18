set -x
name=`date +%F`-podcode.zip
dst="/smb/eespjl/public_html/courses/CI/courseWork2010/code/"
dstfile=$dst/$name
rm $dstfile
zip  $dstfile src/* src/lectureExample/*
