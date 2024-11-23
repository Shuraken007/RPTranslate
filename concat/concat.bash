rm -f tmp;
rm -f tmp; touch tmp;
for file in ../original/*; do 
   cat $file >> tmp;
   echo "\n\n" >> tmp; 
done
cat tmp | grep -E 'Unauthorized.+\:' > dump.txt;
cat tmp | grep -vE 'Unauthorized.+\:' > concat.txt;

rm -f tmp;

python3 convert.py