# name of the spec file
name=bout++-nightly
# Author:
who="David Schwörer <schword2mail.dcu.ie>"
# Version to use
vm="4.1.2"
# Get the most recent full version
version=$(git ls-remote https://github.com/dschwoerer/BOUT-dev.git|grep my_v4|cut -c 1-40)

short=${version:0:7}
if grep $version $name.spec &>/dev/null
then
    echo "up to date"
    exit 0
else
    old=$(grep "%global commit" $name.spec)
    sed "s/$old/%global commit $version/" $name.spec -i
    rel=$(grep "Release:" $name.spec)
    dat=$(date +%Y%m%d)
    newver=$(date +%Y%m%d)git$short
    sed -i "s/$rel/Release:        $(date +%Y%m%d)git%{shortcommit}%{?dist}/" $name.spec
    sed -i "s/%changelog/%changelog\n* $(date "+%a %b %d %Y") $who - $vm-$newver\n- Update to version $short\n/" $name.spec
    #git diff
    git commit -pm "Update $name to version $short"
fi
