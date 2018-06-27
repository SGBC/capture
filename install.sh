git clone https://github.com/marbl/canu.git ;
cd canu/src ;
make -j 4 ;
cd ../.. ;
echo 'export PATH="/opt/canu/Linux-amd64/bin:$PATH"' > ~/.bashrc ;
source ~.bashrc
