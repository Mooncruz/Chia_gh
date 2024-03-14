csalt35='1e-5 1e-4 1e-3 1e-2 1e-1'
pH='3.00 4.65 6.00 7.00 8.00 9.00'

for i in $csalt35; do
    for j in $pH; do

	dir="csalt35-$i-pH-$j"
	mkdir $dir
	cd $dir
	cp ../inputs.in .
	sed -i "s/mmm/$i/g" inputs.in
	sed -i "s/xxx/$j/g" inputs.in
	../code/microgels-mc.x
	cd ..
    done
done 
    
