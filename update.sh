# name of the spec file
name=$(ls *spec)
if test $(echo $name|wc -w) -gt 1
then
    echo "more then one spec file found - aborting"
    exit 3
fi
name=${name%.spec}

# Author:
who="David Schwörer <schword2mail.dcu.ie>"
# Version to use
if [ "$1" ]
then
    vm="$1"
else
    vm=$(echo $(grep Version: $name.spec | cut -d: -f2))
fi
# Get the most recent full version
case $name in
    bout++-nightly)
        version=$(git ls-remote https://github.com/dschwoerer/BOUT-dev.git|grep my_v4|cut -c 1-40)
        ;;
    mangareader)
        version=$(git ls-remote https://github.com/dschwoerer/$name.git|grep master|cut -c 1-40)
        ;;
    *)
        echo "Cannot resolve upstream version - aborting"
        exit 2
        ;;
esac

echo $version

short=${version:0:7}
if grep $version $name.spec &>/dev/null && grep "$vm" $name.spec|grep "Version:" &>/dev/null
then
    echo "up to date"
    exit 0
else
    old=$(grep "%global commit" $name.spec)
    sed "s/$old/%global commit $version/" $name.spec -i
    ver=$(grep "Version:" $name.spec)
    sed -i "s/$ver/Version:        $vm/" $name.spec
    rel=$(grep "Release:" $name.spec)
    dat=$(date +%Y%m%d)
    newver=$(date +%Y%m%d)git$short
    sed -i "s/$rel/Release:        $(date +%Y%m%d)git%{shortcommit}%{?dist}/" $name.spec
    sed -i "s/%changelog/%changelog\n* $(date "+%a %b %d %Y") $who - $vm-$newver\n- Update to version $vm - $short\n/" $name.spec
    #git diff
    git commit -pm "Update $name to version $vm - $short"
fi

project=scripts
if test $name == bout++-nightly || test $name == bout++
then
    project=bout
fi

rm $name*tar.gz
rm $name*src.rpm
set -e
spectool -g $name.spec
rpkg srpm

echo fedpkg --release f$(uname -r|cut -f2 -dc|cut -d. -f1) --module-name $name  local
echo fedpkg --release f27 --module-name $name  mockbuild

echo copr-cli build $project $name*src.rpm
