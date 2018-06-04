%global git 1
%global commit 8758e09334ef42f4aed8939d7fc59ec2206591be
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           bout++-next
Version:        4.1.2
Release:        20180604git%{shortcommit}%{?dist}
Summary:        Library for the BOUndary Turbulence simulation framework

Group:          Applications/Engineering
License:        LGPLv3
URL:            https://boutproject.github.io/
Source0:        https://github.com/dschwoerer/BOUT-dev/archive/%{commit}/%{name}-%{version}.tar.gz

# Disable plotting PR 751
#Patch0:         fix.patch

BuildRequires:  m4
BuildRequires:  zlib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  environment-modules
BuildRequires:  netcdf-devel
BuildRequires:  netcdf-cxx4-devel
BuildRequires:  hdf5-devel
BuildRequires:  fftw-devel
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-h5py
BuildRequires:  python3-numpy
BuildRequires:  python3-netcdf4
BuildRequires:  python3-scipy
BuildRequires:  python3-Cython
BuildRequires:  python2
BuildRequires:  python2-h5py
BuildRequires:  python2-numpy
BuildRequires:  python2-netcdf4
BuildRequires:  python2-scipy
BuildRequires:  python2-Cython
BuildRequires:  python2-future
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
BuildRequires:  gcc-c++
# cxx generation
BuildRequires:  python3-jinja2
# Documentation
BuildRequires:  python3-sphinx

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
%package mpich-devel
Summary: BOUT++ mpich libraries
Requires: mpich-devel
Requires: netcdf-cxx4-devel
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

%package -n python3-%{name}-mpich
Summary:  BOUT++ mpich library for python3
Requires: %{name}-mpich
Requires: python3
Requires: mpich
Requires: python3-mpich
Requires: python3-numpy
%{?python_provide:%python_provide python3-%{name}-mpich}
%description  -n python3-%{name}-mpich
This is the BOUT++ library python3 with mpich.

%package -n python2-%{name}-mpich
Summary:  BOUT++ mpich library for python2
Requires: %{name}-mpich
Requires: python2
Requires: mpich
Requires: python2-mpich
Requires: python2-numpy
%{?python_provide:%python_provide python2-%{name}-mpich}
%description  -n python2-%{name}-mpich
This is the BOUT++ library python2 with mpich.

%endif


%if %{with_openmpi}

%package openmpi
Requires: %{name}-common
Summary: BOUT++ openmpi libraries
%package openmpi-devel
Summary: BOUT++ openmpi libraries
Requires: openmpi-devel
Requires: netcdf-cxx4-devel
Requires: hdf5-devel
Requires: fftw-devel
Requires: %{name}-openmpi = %{version}-%{release}
Requires: make

%description openmpi-devel
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for openmpi.

%description openmpi
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for openmpi.

%package -n python3-%{name}-openmpi
Summary:  BOUT++ mpich library for python3
Requires: %{name}-openmpi
Requires: python3
Requires: openmpi
Requires: python3-openmpi
Requires: python3-numpy
%{?python_provide:%python_provide python3-%{name}-openmpi}

%description  -n python3-%{name}-openmpi
This is the BOUT++ library python3 with openmpi.

%package -n python2-%{name}-openmpi
Summary:  BOUT++ mpich library for python2

Requires: %{name}-openmpi
Requires: python2
Requires: openmpi
Requires: python2-openmpi
Requires: python2-numpy
%{?python_provide:%python_provide python2-%{name}-openmpi}
%description  -n python2-%{name}-openmpi
This is the BOUT++ library python2 with openmpi.


%endif


%package -n python3-%{name}
Summary: BOUT++ python library
Requires: netcdf4-python3
Requires: %{name}-common
Requires: python3-numpy
Suggests: python3-scipy
BuildArch: noarch
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python3 library for pre and post processing of BOUT++ data


%package -n python2-%{name}
Summary: BOUT++ python library
Requires: netcdf4-python
Requires: %{name}-common
Requires: python2-numpy
Suggests: python2-scipy
BuildArch: noarch
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
Python2 library for pre and post processing of BOUT++ data.

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
  make %{?_smp_mflags} python2
  export LD_LIBRARY_PATH=$(pwd)/lib
  make %{?_smp_mflags} -C manual html man
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
@@ -16,7 +16,7 @@
 # PETSc config variables need to be first, else they may clobber other
 # options (e.g. CXX, CXXFLAGS)
 
-
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
    mkdir -p ${RPM_BUILD_ROOT}/%{python2_sitelib}/$d
    cp $d/*py ${RPM_BUILD_ROOT}/%{python2_sitelib}/$d/
done
popd
mandir=$(ls build_*/manual -d|head -n1)
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/
install -m 644 $mandir/man/bout.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/bout++.1
mkdir -p ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bout++/
rm -rf $mandir/html/.buildinfo
rm -rf $mandir/html/.doctrees
rm -rf $mandir/html/_sources
cp -r $mandir/html ${RPM_BUILD_ROOT}/%{_defaultdocdir}/bout++/


# install boutcore library
for mpi in %{mpi_list}
do
    mkdir -p ${RPM_BUILD_ROOT}/%{python3_sitearch}/${mpi}/
    install build_$mpi/tools/pylib/boutcore.*.so ${RPM_BUILD_ROOT}/%{python3_sitearch}/${mpi}/
    mkdir -p ${RPM_BUILD_ROOT}/%{python2_sitearch}/${mpi}/
    install build_$mpi/tools/pylib/boutcore.so ${RPM_BUILD_ROOT}/%{python2_sitearch}/${mpi}/
done

# Fix python interpreter for libraries
for f in $(find -L ${RPM_BUILD_ROOT}/%{python3_sitelib} -executable -type f)
do
    sed -i 's|#!/usr/bin/env python3|#!/usr/bin/python3|' $f
done
for f in $(find -L ${RPM_BUILD_ROOT}/%{python2_sitelib} -executable -type f)
do
    sed -i 's|#!/usr/bin/env python3|#!/usr/bin/python2|' $f
done

%check
# Set to 1 to fail if tests fail
fail=1
for mpi in %{mpi_list}
do
    module purge
    module load mpi/$mpi-%{_arch}
    pushd build_$mpi/tests/integrated
    LD_LIBRARY_PATH_=$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${RPM_BUILD_ROOT}/%{_libdir}/${mpi}/lib/:$LD_LIBRARY_PATH
    export PYTHONPATH=${RPM_BUILD_ROOT}/%{python3_sitelib}:${RPM_BUILD_ROOT}/%{python3_sitearch}/${mpi}/
    alias python=python3
    export PYTHONIOENCODING=utf8
    ./test_suite       || exit $fail
    popd
    pushd build_$mpi/tests/MMS
    ./test_suite       || exit $fail
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_
    popd
    module purge
done

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
%files -n python3-%{name}-mpich
%{python3_sitearch}/mpich/*
%files -n python2-%{name}-mpich
%{python2_sitearch}/mpich/*
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
%files -n python3-%{name}-openmpi
%{python3_sitearch}/openmpi/*
%files -n python2-%{name}-openmpi
%{python2_sitearch}/openmpi/*
%endif

%files -n python3-%{name}
%dir %{python3_sitelib}/*
%{python3_sitelib}/*/*

%files -n python2-%{name}
%dir %{python2_sitelib}/*
%{python2_sitelib}/*/*

%files -n %{name}-doc
%doc %{_mandir}/man1/bout++*
%doc  %{_defaultdocdir}/bout++/

%files common
%doc README.md
%doc CITATION
%doc CHANGELOG.md
%license LICENSE
%license LICENSE.GPL

%changelog
* Mon Jun 04 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180604git8758e09
- Update to version 4.1.2 - 8758e09

* Thu May 31 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180531git9a61910
- Update to version 4.1.2 - 9a61910

* Sat May 26 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180526gitf02636a
- Update to version 4.1.2 - f02636a

* Wed May 23 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180523gitb3368ca
- Update to version 4.1.2 - b3368ca

* Wed May 09 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-20180509git94be925
- Update to version 4.1.2 - 94be925

* Wed May 09 2018 David Schwörer <schword2mail.dcu.ie> - 4.1.2-1
- Initial RPM release.
