Name:           bout++
Version:        4.0.0
Release:        1%{?dist}
Summary:        Library for the BOUndary Turbulence simulation framework

Group:          Applications/Engineering
License:        LGPLv3
URL:            https://boutproject.github.io/
Source0:        https://github.com/boutproject/BOUT-dev/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Allow installation in configured location #550
Patch0:         fix_makefile.patch
# Cleanup of pylib #548
Patch1:         pylib.patch
# for integration with fedora #550
Patch2:         make_config.patch 

# BuildRequires:  chrpath
# BuildRequires:  doxygen
# BuildRequires:  netcdf-devel
# BuildRequires:  gawk
# BuildRequires:  libcurl-devel
BuildRequires:  m4
BuildRequires:  zlib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  environment-modules
#mpiexec segfaults if ssh is not present
#https://trac.mcs.anl.gov/projects/mpich2/ticket/1576
BuildRequires:  openssh-clients
BuildRequires:  netcdf-devel
BuildRequires:  hdf5-devel
BuildRequires:  fftw-devel
BuildRequires:  make
BuildRequires:  netcdf-cxx-devel
BuildRequires:  python3
BuildRequires:  python3-h5py
BuildRequires:  netcdf4-python3
BuildRequires:  python3-numpy
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
BuildRequires:  python2
BuildRequires:  python2-h5py
BuildRequires:  netcdf4-python
BuildRequires:  python2-numpy
BuildRequires:  python2-numpy
BuildRequires:  python2-scipy

#BuildRequires:  blas-devel
#BuildRequires:  lapack-devel
#Requires:     netcdf-devel

%global debug_package %{nil}

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
%package mpich-devel
Summary: BOUT++ mpich libraries
Group: Development/Libraries
Requires: mpich-devel
Requires: netcdf-devel
Requires: hdf5-devel
Requires: fftw-devel
Requires: make
#Requires: petsc-mpich-devel
Provides: %{name}-mpich = %{version}-%{release}
Provides: %{name}-mpich-static = %{version}-%{release}

%description mpich-devel
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for mpich.

%endif


%if %{with_openmpi}
%package openmpi-devel
Summary: NetCDF openmpi libraries
Group: Development/Libraries
Requires: openmpi-devel
Requires: netcdf-devel
Requires: hdf5-devel
Requires: fftw-devel
Requires: make
Provides: %{name}-openmp = %{version}-%{release}
Provides: %{name}-openmp-static = %{version}-%{release}
%description openmpi-devel
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

This BOUT++ library is build for openmpi.
%endif


%package -n python3-%{name}
Summary: BOUT++ python library
Group: Development/Libraries
Requires: netcdf4-python3

%description -n python3-%{name}
Python3 library for pre and post processing of BOUT++ data.


%package -n python2-%{name}
Summary: BOUT++ python library
Group: Development/Libraries
Requires: netcdf4-python

%description -n python2-%{name}
Python2 library for pre and post processing of BOUT++ data.


%prep
%setup -n BOUT-dev-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1

autoreconf

%build
%global configure_opts \\\
           --with-netcdf \\\
           --with-hdf5

%{nil}

#           --enable-debug \\\
#           --with-petsc=/home/dave/rpmbuild/petsc/petsc-3.7.5/buildmpich_dir/ \\\

# MPI builds
export CC=mpicc
export CXX=mpicxx

for mpi in %{mpi_list}
do
  mkdir build_$mpi
  cp -al [^b][^u][^i]* build-aux bin ?? build_$mpi
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
  make %{?_smp_mflags}
  module purge
  popd
done


%install

for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  make -C build_$mpi install DESTDIR=${RPM_BUILD_ROOT}
  echo "diff -Naur a/make.config b/make.config
--- a/make.config       2017-05-02 23:03:57.298625399 +0100
+++ b/make.config       2017-05-02 23:04:26.460489477 +0100
@@ -16,7 +16,7 @@
 # PETSc config variables need to be first, else they may clobber other
 # options (e.g. CXX, CXXFLAGS)
 
-
+RELEASE                 = %{version}-%{?dist}
 
 # Created this variable so that a user won't overwrite the CXXFLAGS variable
 # on the command line, just add to this one
" | patch -p1 ${RPM_BUILD_ROOT}/%{_includedir}/${mpi}-%{_arch}/bout/make.config
  module purge
done

pushd tools/pylib
for d in bout* zoidberg post_bout
do
    mkdir -p ${RPM_BUILD_ROOT}/%{python3_sitearch}/$d
    cp $d/*py ${RPM_BUILD_ROOT}/%{python3_sitearch}/$d/
    #python3 -O -m compileall ${RPM_BUILD_ROOT}/%{python3_sitearch}/$d
    #python3 -m compileall ${RPM_BUILD_ROOT}/%{python3_sitearch}/$d
    mkdir -p ${RPM_BUILD_ROOT}/%{python2_sitearch}/$d
    cp $d/*py ${RPM_BUILD_ROOT}/%{python2_sitearch}/$d/
    #python2 -O -m compileall ${RPM_BUILD_ROOT}/%{python2_sitearch}/$d
    #python2 -m compileall ${RPM_BUILD_ROOT}/%{python2_sitearch}/$d
done
for f in $(find -L ${RPM_BUILD_ROOT}/%{python3_sitearch} -executable -type f)
do
    sed -i 's/#!\/usr\/bin\/env python/#!\/usr\/bin\/python3/' $f
done
for f in $(find -L ${RPM_BUILD_ROOT}/%{python2_sitearch} -executable -type f)
do
    sed -i 's/#!\/usr\/bin\/env python/#!\/usr\/bin\/python2/' $f
done

%check
# Set to 1 to fail if tests fail
fail=1
for mpi in %{mpi_list}
do
    module load mpi/$mpi-%{_arch}
    pushd build_$mpi/examples
    export PYTHONPATH=${RPM_BUILD_ROOT}/%{python3_sitearch}
    ./test_suite_make  &> log || ( cat log ; exit $fail )
    ./test_suite       &> log || ( cat log ; exit $fail )
    popd
    module purge
done
for f in $(find -L ${RPM_BUILD_ROOT}/%{python3_sitearch}/*/*\.py{c,o} -type f)
do
    echo cleaning $f
    rm $f
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if %{with_mpich}
%files mpich-devel
%doc README.md
%license LICENSE
%dir %{_includedir}/mpich-%{_arch}/bout
%dir %{_includedir}/mpich-%{_arch}/bout/sys
%{_includedir}/mpich-%{_arch}/*.hxx
%{_includedir}/mpich-%{_arch}/bout/make.config
%{_includedir}/mpich-%{_arch}/bout/*.hxx
%{_includedir}/mpich-%{_arch}/bout/sys/*.hxx
%{_libdir}/mpich/lib/*.a
%endif

%if %{with_openmpi}
%files openmpi-devel
%doc README.md
%license LICENSE
%dir %{_includedir}/openmpi-%{_arch}/bout
%dir %{_includedir}/openmpi-%{_arch}/bout/sys
%{_includedir}/openmpi-%{_arch}/*.hxx
%{_includedir}/openmpi-%{_arch}/bout/*.hxx
%{_includedir}/openmpi-%{_arch}/bout/make.config
%{_includedir}/openmpi-%{_arch}/bout/sys/*.hxx
%{_libdir}/openmpi/lib/*.a
%endif

%files -n python3-%{name}
%dir %{python3_sitearch}/*
%{python3_sitearch}/*/*

%files -n python2-%{name}
%dir %{python2_sitearch}/*
%{python2_sitearch}/*/*

%changelog
* Tue May 02 2017 David Schwörer <schword2mail.dcu.ie> - 4.0.0-1
- Initial RPM release.
