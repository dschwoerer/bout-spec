%global commit c2fbfdc35d3d0bfe1272cc8c3e89c7ecdc7fe8f5
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           bout++-nightly
Version:        4.1.2
Release:        20181108git%{shortcommit}%{?dist}
Summary:        Library for the BOUndary Turbulence simulation framework

License:        LGPLv3+
URL:            https://boutproject.github.io/
Source0:        https://github.com/dschwoerer/BOUT-dev/archive/%{commit}/%{name}-%{version}.tar.gz

# PR 1261
Patch0:          localedir.patch


%global test 1
%if 0%{?epel}
%global test 0
%endif

%global manual 1
%if 0%{?epel}
%global manual 0
%endif

BuildRequires:  m4
BuildRequires:  zlib-devel
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  gettext-devel
BuildRequires:  automake
BuildRequires:  environment-modules
BuildRequires:  netcdf-devel
BuildRequires:  netcdf-cxx%{?fedora:4}-devel
BuildRequires:  hdf5-devel
BuildRequires:  fftw-devel
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-Cython
BuildRequires:  python%{python3_pkgversion}-netcdf4
BuildRequires:  python%{python3_pkgversion}-scipy
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
BuildRequires:  gcc-c++
# cxx generation
BuildRequires:  python%{python3_pkgversion}-jinja2
# Documentation
%if %{manual}
BuildRequires:  doxygen
BuildRequires:  python3-sphinx
%endif

%global with_mpich 1
%global with_openmpi 1
%if 0%{?rhel} && 0%{?rhel} <= 6
%ifarch ppc64
# No mpich on ppc64 in EL6
%global with_mpich 0
%endif
%endif
%ifarch s390 s390x
# No openmpi on s390(x)
%global with_openmpi 0
%endif

%if %{with_mpich}
BuildRequires:  mpich-devel
%global mpi_list mpich
%endif
%if %{with_openmpi}
BuildRequires:  openmpi-devel
%global mpi_list %{?mpi_list} openmpi
%endif

%description
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.


%if %{with_mpich}
%package mpich
Requires: %{name}-common
Summary: BOUT++ mpich libraries
# Use bundled version, to reproduce upstream results
Provides: bundled(libpvode)
%package mpich-devel
Summary: BOUT++ mpich libraries
Requires: mpich-devel
Requires: netcdf-cxx%{?fedora:4}-devel
Requires: hdf5-devel
Requires: fftw-devel
Requires: %{name}-mpich = %{version}-%{release}
Requires: make

%description mpich-devel
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for mpich.

%description mpich
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for mpich.

%package -n python%{python3_pkgversion}-%{name}-mpich
Summary:  BOUT++ mpich library for python%{python3_pkgversion}
Requires: %{name}-mpich
BuildRequires: python%{python3_pkgversion}-devel
Requires: mpich
Requires: python%{python3_pkgversion}-mpich
Requires: python%{python3_pkgversion}-numpy
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}-mpich}
%description  -n python%{python3_pkgversion}-%{name}-mpich
This is the BOUT++ library python%{python3_pkgversion} with mpich.

%endif


%if %{with_openmpi}

%package openmpi
Requires: %{name}-common
Summary: BOUT++ openmpi libraries
# Use bundled version, to reproduce upstream results
Provides: bundled(libpvode)
%package openmpi-devel
Summary: BOUT++ openmpi libraries
Requires: openmpi-devel
Requires: netcdf-cxx%{?fedora:4}-devel
Requires: hdf5-devel
Requires: fftw-devel
Requires: make
Requires: %{name}-openmpi = %{version}-%{release}

%description openmpi-devel
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for openmpi and provides the requred
header files.

%description openmpi
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for openmpi.

%package -n python%{python3_pkgversion}-%{name}-openmpi
Summary:  BOUT++ mpich library for python%{python3_pkgversion}
Requires: %{name}-openmpi
BuildRequires: python%{python3_pkgversion}-devel
Requires: openmpi
Requires: python%{python3_pkgversion}-openmpi
Requires: python%{python3_pkgversion}-numpy
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}-openmpi}

%description  -n python%{python3_pkgversion}-%{name}-openmpi
This is the BOUT++ library python%{python3_pkgversion} with openmpi.


%endif


%package -n python%{python3_pkgversion}-%{name}
Summary: BOUT++ python library
Requires: netcdf4-python%{python3_pkgversion}
Requires: %{name}-common
Requires: python%{python3_pkgversion}-numpy
%if 0%{?fedora}
Suggests: python%{python3_pkgversion}-scipy
%endif
BuildArch: noarch
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description -n python%{python3_pkgversion}-%{name}
Python%{python3_pkgversion} library for pre and post processing of BOUT++ data



%if %{manual}
%package -n %{name}-doc
Summary: BOUT++ Documentation
Requires: %{name}-common
BuildArch: noarch

%description -n %{name}-doc
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This package contains the documentation.
%endif

%package common
Summary: BOUT++ python library
BuildArch: noarch
Conflicts: bout-common
%description  common
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This package contains the common files.

%prep
%setup -q -n BOUT-dev-%{commit}
%patch0 -p 1

autoreconf

%build
%global configure_opts \\\
           --with-netcdf \\\
           --with-hdf5 \\\
           --enable-optimize=3 \\\
           --enable-shared

%{nil}

# MPI builds
export CC=mpicc
export CXX=mpicxx
export PYTHONIOENCODING=utf8

for mpi in %{mpi_list}
do
  mkdir build_$mpi
  cp -al [^b]* build-aux bin build_$mpi
done
for mpi in %{mpi_list}
do
  pushd build_$mpi
  module purge
  module load mpi/$mpi-%{_arch}
  # parallel tests hang on s390(x)
  %configure %{configure_opts} \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share \
    --mandir=%{_libdir}/$mpi/share/man
  # workaround to prevent race condition
  touch lib/.last.o.file
  make %{?_smp_mflags} shared python
  export LD_LIBRARY_PATH=$(pwd)/lib
  %if %{manual}
  make %{?_smp_mflags} -C manual html man
  %endif
  module purge
  popd
done


%install

for mpi in %{mpi_list}
do
  module purge
  module load mpi/$mpi-%{_arch}
  pushd build_$mpi
  make install DESTDIR=${RPM_BUILD_ROOT}
  mv  ${RPM_BUILD_ROOT}/usr/share/bout++/make.config ${RPM_BUILD_ROOT}/%{_includedir}/$mpi-%{_arch}/bout++/
  echo "diff -Naur a/make.config b/make.config
--- a/make.config       2017-05-02 23:03:57.298625399 +0100
+++ b/make.config       2017-05-02 23:04:26.460489477 +0100
@@ -23,6 +23,7 @@
 SLEPC_DIR ?= 
 SLEPC_ARCH ?= 
 
+RELEASED                 = %{version}-%{release}
 
 # These lines can be replaced in \"make install\" to point to install directories
 # They are used in the CXXFLAGS variable below rather than hard-coding the directories
" | patch --no-backup-if-mismatch -p1 --fuzz=0 ${RPM_BUILD_ROOT}/%{_includedir}/${mpi}-%{_arch}/bout++/make.config
  rm -rf  ${RPM_BUILD_ROOT}/usr/share/bout++
  rm -f ${RPM_BUILD_ROOT}/%{_libdir}/${mpi}/lib/*.a
  install lib/*.so.* ${RPM_BUILD_ROOT}/%{_libdir}/${mpi}/lib/
  pushd ${RPM_BUILD_ROOT}/%{_libdir}/${mpi}/lib/
  for f in *.so.*
  do
      ln -s $f ${f%%.so*}.so
  done
  popd
  popd
  module purge
done

# install python libraries
pushd tools/pylib
for d in boutdata bout_runners boututils  post_bout zoidberg
do
    mkdir -p ${RPM_BUILD_ROOT}/%{python3_sitelib}/$d
    cp $d/*py ${RPM_BUILD_ROOT}/%{python3_sitelib}/$d/
done
popd
%if %{manual}
mandir=$(ls build_*/manual -d|head -n1)
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/
install -m 644 $mandir/man/bout.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/bout++.1
mkdir -p ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bout++/
rm -rf $mandir/html/.buildinfo
rm -rf $mandir/html/.doctrees
rm -rf $mandir/html/_sources
cp -r $mandir/html ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bout++/
%endif

# install boutcore library
for mpi in %{mpi_list}
do
    mkdir -p ${RPM_BUILD_ROOT}/%{python3_sitearch}/${mpi}/
    install build_$mpi/tools/pylib/boutcore.*.so ${RPM_BUILD_ROOT}/%{python3_sitearch}/${mpi}/
done

# Fix python interpreter for libraries
for f in $(find -L ${RPM_BUILD_ROOT}/%{python3_sitelib} -executable -type f)
do
    sed -i 's|#!/usr/bin/env python|#!/usr/bin/python3|' $f
    sed -i 's|#!/usr/bin/env python3|#!/usr/bin/python3|' $f
    sed -i 's|#!/usr/bin/python|#!/usr/bin/python3|' $f
    # remove introduced but excessive 3's
    sed -i 's|#!/usr/bin/python333|#!/usr/bin/python3|' $f
    sed -i 's|#!/usr/bin/python33|#!/usr/bin/python3|' $f
done

%check
%if %{test}
for mpi in %{mpi_list}
do
    export PYTHONIOENCODING=utf8
    module purge
    module load mpi/$mpi-%{_arch}
    pushd build_$mpi/tests/integrated
    LD_LIBRARY_PATH_=$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${RPM_BUILD_ROOT}/%{_libdir}/${mpi}/lib/:$LD_LIBRARY_PATH
    export PYTHONPATH=${RPM_BUILD_ROOT}/%{python3_sitelib}:${RPM_BUILD_ROOT}/%{python3_sitearch}/${mpi}/
    ./test_suite
    popd
    pushd build_$mpi/tests/MMS
    ./test_suite
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_
    popd
    module purge
done
%endif

for f in $(find -L ${RPM_BUILD_ROOT}/%{python3_sitelib}/*/*\.py{c,o} -type f)
do
    echo cleaning $f
    rm $f
done



%if %{with_mpich}
%post mpich -p /sbin/ldconfig
%postun mpich -p /sbin/ldconfig
%files mpich
%{_libdir}/mpich/lib/*.so.*
%files mpich-devel
%dir %{_includedir}/mpich-%{_arch}/bout++
%dir %{_includedir}/mpich-%{_arch}/bout++/bout
%dir %{_includedir}/mpich-%{_arch}/bout++/bout/invert
%dir %{_includedir}/mpich-%{_arch}/bout++/bout/sys
%{_includedir}/mpich-%{_arch}/bout++/*.hxx
%{_includedir}/mpich-%{_arch}/bout++/make.config
%{_includedir}/mpich-%{_arch}/bout++/bout/*.hxx
%{_includedir}/mpich-%{_arch}/bout++/bout/invert/*.hxx
%{_includedir}/mpich-%{_arch}/bout++/bout/sys/*.hxx
%{_includedir}/mpich-%{_arch}/bout++/pvode/*.h
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/bin/*
%{_libdir}/mpich/share/locale/*/LC_MESSAGES/libbout.mo
%files -n python%{python3_pkgversion}-%{name}-mpich
%{python3_sitearch}/mpich/*
%endif

%if %{with_openmpi}
%files openmpi
%{_libdir}/openmpi/lib/*.so.*
%files openmpi-devel
%dir %{_includedir}/openmpi-%{_arch}/bout++
%dir %{_includedir}/openmpi-%{_arch}/bout++/bout
%dir %{_includedir}/openmpi-%{_arch}/bout++/bout/invert
%dir %{_includedir}/openmpi-%{_arch}/bout++/bout/sys
%{_includedir}/openmpi-%{_arch}/bout++/*.hxx
%{_includedir}/openmpi-%{_arch}/bout++/bout/*.hxx
%{_includedir}/openmpi-%{_arch}/bout++/make.config
%{_includedir}/openmpi-%{_arch}/bout++/bout/invert/*.hxx
%{_includedir}/openmpi-%{_arch}/bout++/bout/sys/*.hxx
%{_includedir}/openmpi-%{_arch}/bout++/pvode/*.h
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/bin/*
%{_libdir}/openmpi/share/locale/*/LC_MESSAGES/libbout.mo
%files -n python%{python3_pkgversion}-%{name}-openmpi
%{python3_sitearch}/openmpi/*
%endif

%files -n python%{python3_pkgversion}-%{name}
%dir %{python3_sitelib}/*
%{python3_sitelib}/*/*

%if %{manual}
%files -n %{name}-doc
%doc %{_mandir}/man1/bout++*
%doc  %{_defaultdocdir}/bout++/
%endif

%files common
%doc README.md
%doc CITATION.bib
%doc CITATION.cff
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%license LICENSE
%license LICENSE.GPL

%changelog
* Thu Nov 08 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20181108gitc2fbfdc
- Update to version 4.1.2 - c2fbfdc
- Add language support
- Fix mangling of shebangs

* Wed Sep 12 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180719git4ec4d30
- Fixes for epel

* Thu Jul 19 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180719git4ec4d30
- Update to version 4.1.2 - 4ec4d30

* Thu Jul 19 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180719git863517d
- Update to version 4.1.2 - 863517d

* Thu Jul 19 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180719git87dd651
- Update to version 4.1.2 - 87dd651

* Fri Jul 13 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180713git4e9b53f
- Update to version 4.1.2 - 4e9b53f

* Fri Jul 13 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180713gitfa01cbd
- Update to version 4.1.2 - fa01cbd

* Fri Jun 22 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180622gite81eefd
- Update to version 4.1.2 - e81eefd

* Fri Jun 22 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180622gitf57d190
- Update to version 4.1.2 - f57d190

* Fri Jun 22 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180622git3fc8930
- Update to version 4.1.2 - 3fc8930

* Wed May 09 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180509gitbbe2ab7
- Update to version 4.1.2 - bbe2ab7

* Sun Apr 29 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180429gited890c8
- Update to version 4.1.2 - ed890c8

* Tue Apr 24 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180424gitecd8c9e
- Update to version 4.1.2 - ecd8c9e

* Tue Apr 24 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180424git4b13c29
- Update to version 4.1.2 - 4b13c29

* Mon Apr 23 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180423gitaff24d1
- Update to version 4.1.2 - aff24d1

* Thu Apr 12 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180412git4f07065
- Update to version 4.1.2 - 4f07065

* Sat Mar 24 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180324gitb99bb53
- Update to version 4.1.2 - b99bb53

* Sat Mar 24 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180324git349a246
- Update to version 4.1.2 - 349a246

* Sat Mar 24 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180324gitccd4104
- Update to version 4.1.2 - ccd4104

* Sat Mar 24 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180324gitf380cfb
- Update to version 4.1.2 - f380cfb

* Fri Feb 23 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180223git95745b9
- Update to version 4.1.2 - 95745b9

* Thu Feb 22 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180222gitc3df835
- Update to version 4.1.2 - c3df835

- Add documentation package

* Thu Feb 22 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180222git492b9e9
- Update to version 4.1.2 - 492b9e9

* Wed Feb 21 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180221git5f01dad
- Update to version 4.1.2 - 5f01dad

* Tue Feb 13 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180213git595da71
- Update to version 4.1.2 - 595da71
- Add boutcore path for test suite

* Tue Feb 06 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180206git83b2b3d
- Update to version 4.1.2 - 83b2b3d

* Tue Jan 23 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180123git41f8075
- Update to version 4.1.2 - 41f8075

* Mon Jan 22 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180122gitc118c9b
- Update to version 4.1.2 - c118c9b

* Wed Jan 17 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180117gitb142b2a
- Update to version 4.1.2 - b142b2a

* Tue Dec 19 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20171219gita7968f5
- Update to version a7968f5

* Fri Dec 15 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20171215gitbaa0348
- Update version to baa0348

* Tue Dec 12 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.2-1
- Update to new release, remove patch

* Tue May 02 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.1-1
- Initial RPM release.
