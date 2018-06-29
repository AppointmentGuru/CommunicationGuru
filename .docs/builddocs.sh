rm -rf ../docs
vuepress build 
mv .vuepress/dist ../docs
echo "Profit"
