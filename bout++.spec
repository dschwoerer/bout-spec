Name:           bout++
Version:        4.2.2
Release:        1%{?dist}
Summary:        Library for the BOUndary Turbulence simulation framework

# BOUT++ itself is LGPL, but we are linking with GPLed code, so the distributed library is GPL
License:        GPLv3+
URL:            https://boutproject.github.io/
Source0:        https://github.com/boutproject/BOUT-dev/releases/download/v%{version}/BOUT++-v%{version}.tar.gz


# Disable tests and manual on epel < 8
%if 0%{?rhel} && 0%{?rhel} < 8
%bcond_with manual
%bcond_with test
%else
%bcond_without manual
%bcond_without test
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%ifarch ppc64
# No mpich on ppc64 in EL6
%bcond_with mpich
%else
%bcond_without mpich
%endif
%else
%bcond_without mpich
%endif

%ifarch s390 s390x
# No openmpi on s390(x)
%global with_openmpi 0
%bcond_with openmpi
%else
%bcond_without openmpi
%endif

# Enable weak dependencies
%if 0%{?fedora} || 0%{?rhel} && 0%{?rhel} > 7
%bcond_without recommend
%else
%bcond_with recommend
%endif


#
#           DEPENDENCIES
#

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
%if %{with manual}
BuildRequires:  doxygen
BuildRequires:  python3-sphinx
%endif


#
#           DESCRIPTIONS
#


%if %{with mpich}
BuildRequires:  mpich-devel
%global mpi_list mpich
%endif
%if %{with openmpi}
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



%if %{with mpich}
%package mpich
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
Requires: python%{python3_pkgversion}-%{name}
BuildRequires: python%{python3_pkgversion}-devel
Requires: mpich
Requires: python%{python3_pkgversion}-mpich
Requires: python%{python3_pkgversion}-numpy
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}-mpich}
%description  -n python%{python3_pkgversion}-%{name}-mpich
This is the BOUT++ library python%{python3_pkgversion} with mpich.

%endif




%if %{with openmpi}
%package openmpi
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

This BOUT++ library is build for openmpi and provides the required
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
Summary:  BOUT++ openmpi library for python%{python3_pkgversion}
Requires: %{name}-openmpi
Requires: python%{python3_pkgversion}-%{name}
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
Requires: python%{python3_pkgversion}-numpy
%if %{with recommend}
Recommends: python%{python3_pkgversion}-scipy
Recommends: python%{python3_pkgversion}-matplotlib
%endif
BuildArch: noarch
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description -n python%{python3_pkgversion}-%{name}
Python%{python3_pkgversion} library for pre and post processing of BOUT++ data




%if %{with manual}
%package -n %{name}-doc
Summary: BOUT++ Documentation
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

#
#           PREP
#

%prep
%setup -q -n BOUT++-v%{version}

# Remove shebang
for f in $(find -L tools/pylib/ -type f | grep -v _boutcore_build )
do
    sed -i '/^#!\//d' $f
done

autoreconf


#
#           BUILD
#

%build
%global configure_opts \\\
           --with-netcdf \\\
           --with-hdf5 \\\
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
  if [ $mpi = mpich ] ; then
      %_mpich_load
  elif [ $mpi = openmpi ] ; then
      %_openmpi_load
  else
      echo "unknown mpi" &> /dev/stderr
      exit 1
  fi

  %configure %{configure_opts} \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share

  make %{?_smp_mflags} shared python
  export LD_LIBRARY_PATH=$(pwd)/lib
  %if %{with manual}
  make %{?_smp_mflags} -C manual html
  %endif
  if [ $mpi = mpich ] ; then
      %_mpich_unload
  elif [ $mpi = openmpi ] ; then
      %_openmpi_unload
  fi
  popd
done

#
#           INSTALL
#

%install

for mpi in %{mpi_list}
do
  pushd build_$mpi
  if [ $mpi = mpich ] ; then
      %_mpich_load
  else
      %_openmpi_load
  fi
  make install DESTDIR=${RPM_BUILD_ROOT}
  mv  ${RPM_BUILD_ROOT}/usr/share/bout++/make.config ${RPM_BUILD_ROOT}/%{_includedir}/$mpi-%{_arch}/bout++/

  # mark this as a released version, to disable compiling the library
  sed -i '26 i RELEASED                 = %{version}-%{release}' ${RPM_BUILD_ROOT}/%{_includedir}/${mpi}-%{_arch}/bout++/make.config

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
  if [ $mpi = mpich ] ; then
      %_mpich_unload
  else
      %_openmpi_unload
  fi
done

# install python libraries
pushd tools/pylib
for d in boutdata bout_runners boututils  post_bout zoidberg
do
    mkdir -p ${RPM_BUILD_ROOT}/%{python3_sitelib}/$d
    cp $d/*py ${RPM_BUILD_ROOT}/%{python3_sitelib}/$d/
done
popd

# install manual
%if %{with manual}
mandir=$(ls build_*/manual -d|head -n1)
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

#
#           CHECK
#

%check

%if %{with test}
for mpi in %{mpi_list}
do
    if [ $mpi = mpich ] ; then
        %_mpich_load
    else
        %_openmpi_load
    fi
    pushd build_$mpi
    unset MPIRUN
    test $mpi = openmpi && export MPIRUN="mpirun -oversubscribe -np"
    make %{?_smp_mflags} build-check
    make check
    popd
    if [ $mpi = mpich ] ; then
        %_mpich_unload
    else
        %_openmpi_unload
    fi
done
%endif

#
#           FILES SECTION
#

%if %{with mpich}
%files mpich
%{_libdir}/mpich/lib/libbout++.so.4.2.2
%{_libdir}/mpich/lib/*.so.1.0.0
%doc README.md
%doc CITATION.bib
%doc CITATION.cff
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%license LICENSE
%license LICENSE.GPL

%files mpich-devel
%{_includedir}/mpich-%{_arch}/bout++
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/bin/*

%files -n python%{python3_pkgversion}-%{name}-mpich
%{python3_sitearch}/mpich/*
%endif


%if %{with openmpi}
%files openmpi
%{_libdir}/openmpi/lib/libbout++.so.4.2.2
%{_libdir}/openmpi/lib/*.so.1.0.0
%doc README.md
%doc CITATION.bib
%doc CITATION.cff
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%license LICENSE
%license LICENSE.GPL

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}/bout++
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/bin/*

%files -n python%{python3_pkgversion}-%{name}-openmpi
%{python3_sitearch}/openmpi/*
%endif

%files -n python%{python3_pkgversion}-%{name}
%{python3_sitelib}/*bout*
%{python3_sitelib}/zoidberg
%doc README.md
%doc CITATION.bib
%doc CITATION.cff
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%license LICENSE
%license LICENSE.GPL


%if %{with manual}
%files -n %{name}-doc
%doc  %{_defaultdocdir}/bout++/
%endif

#
#           CHANGELOG
#

%changelog
* Fri Aug 23 2019 David Schwörer <schword2mail.dcu.ie> - 4.2.2-1
- Remove ldconfig scriptlets
- Use mpi scriplets
- Ensure sitelib packages do not match arched mpi packages
- Move commons package to the base packages
- Specify so version
- Drop man page for library

* Fri Mar 01 2019 David Schwörer <schword2mail.dcu.ie> - 4.2.2-0
- Update to version 4.2.2

* Thu Feb 07 2019 David Schwörer <schword2mail.dcu.ie> - 4.2.1-0
- Fix license
- Bump to 4.2.1
- Use new release
- Release contains gtest, so we can run make check

* Tue Dec 04 2018 David Schwörer <schword2mail.dcu.ie> - 4.2.0-3
- Fix recommend

* Thu Oct 18 2018 David Schwörer <schword2mail.dcu.ie> - 4.2.0-2
- Update to 4.2.0
- Remove python2 support
- Add boutcore support
- Fix mangling of shebangs

* Tue Dec 12 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.2-2
- Add missing python_provide macro

* Fri Dec 01 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.2-1
- Update to new release, remove patch

* Tue May 02 2017 David Schwörer <schword2mail.dcu.ie> - 4.1.1-1
- Initial RPM release.
