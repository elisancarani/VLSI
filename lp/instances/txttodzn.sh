#!bin/bash
regex="[^/]*$"

mkdir -p instancesdzn
cd instances
for f in ./* 
	do 
		#echo -e " " >> $f
		cd ../instancesdzn
		
		exec 3< ../instances/$f
		
		read -u 3 -r line #< ../instances/$f
		echo "w = $line ;" > "${f%.*}.dzn"
		read -u 3 -r line
		echo "n = $line ;" >> "${f%.*}.dzn"
		echo -n "silicons = [" >> "${f%.*}.dzn"
		while read -u 3 -r line
			do
				echo "|$line" | sed 's/ /,/g' >> "${f%.*}.dzn"
			done  < ../instances/$f
		echo "|];" >> "${f%.*}.dzn"
		cd ../instances
	done