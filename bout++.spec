Name:           bout++
Version:        4.0.0
Release:        1%{?dist}
Summary:        Library for the BOUndary Turbulence simulation framework

Group:          Applications/Engineering
License:        LGPLv3
URL:            https://boutproject.github.io/
Source0:        https://github.com/boutproject/BOUT-dev/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         petsc_37
Patch1:         petsc_conf.patch
# BuildRequires:  chrpath
# BuildRequires:  doxygen
# BuildRequires:  netcdf-devel
BuildRequires:  hdf5-devel
# BuildRequires:  gawk
# BuildRequires:  libcurl-devel
BuildRequires:  m4
BuildRequires:  zlib-devel
BuildRequires:  netcdf-devel
# %ifnarch s390 s390x %{arm}
# BuildRequires:  valgrind
# %endif
#mpiexec segfaults if ssh is not present
#https://trac.mcs.anl.gov/projects/mpich2/ticket/1576
BuildRequires:  openssh-clients
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
#Requires:       hdf5%{?_isa} = %{_hdf5_version}
Requires:     netcdf-devel

%global debug_package %{nil}

%global with_mpich 1
%global with_openmpi 0
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
%global mpi_list mpich
%endif
%if %{with_openmpi}
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
Summary: NetCDF mpich libraries
Group: Development/Libraries
#Requires: netcdf-mpich%{?_isa} = %{_hdf5_version}
BuildRequires: mpich-devel
BuildRequires: petsc-mpich-devel
Provides: %{name}-mpich = %{version}-%{release}

%description mpich
BOUT++ library for mpich

%endif


%if %{with_openmpi}
%package openmpi
Summary: NetCDF openmpi libraries
Group: Development/Libraries
Requires: openmpi-devel
#BuildRequires: openmpi-devel
#BuildRequires: hdf5-openmpi-devel >= 1.8.4

%description openmpi
BOUT++ library for openmpi
%endif


%prep
%setup -n BOUT-dev-%{version}

#pushd BOUT-dev-%{version}
#echo fubar
%patch0 -p1
#cat ../petsc_37 | patch -p 1
%patch1 -p1

#popd
#%setup -q -n %{name}-c-%{version}
#m4 libsrc/ncx.m4 > libsrc/ncx.c
# Try to handle builders that can't resolve their own name
#sed -i -s 's/mpiexec/mpiexec -host localhost/' */*.sh
autoreconf

%build
%global configure_opts \\\
           --enable-debug \\\
           --with-netcdf \\\
           --with-hdf5 \\\
           --with-petsc=fedora

%{nil}

# MPI builds
export CC=mpicc
export CXX=mpicxx

for mpi in %{mpi_list}
do
  mkdir build_$mpi
  cp -al [^b][^u][^i]* build-aux bin build_$mpi
done
for mpi in %{mpi_list}
do
  pushd build_$mpi
  module load mpi/$mpi-%{_arch}
  #ln -s ../configure .
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

echo "BOUT++ is a library that needs mpi. Install bout++-openmpi or bout++-mpich" > bin/bout++
chmod +x bin/bout++
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
cp bin/bout++ ${RPM_BUILD_ROOT}/%{_bindir}

for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  make -C build_$mpi install DESTDIR=${RPM_BUILD_ROOT}
  module purge
done


%check
# Set to 1 to fail if tests fail
fail=1
for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  pushd build_$mpi/examples
  ./test_suite_make  &> log || ( cat log ; exit $fail )
  ./test_suite       &> log || ( cat log ; exit $fail )
  popd
  module purge
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/bout++



%if %{with_mpich}
%files mpich
%doc LICENSE README.md
%{_includedir}/mpich-%{_arch}
%{_includedir}/mpich-%{_arch}/bout/
%{_includedir}/mpich-%{_arch}/bout/sys
%{_libdir}/mpich/lib/*.a
%endif

%if %{with_openmpi}
%files openmpi
%doc LICENSE README.md
%{_includedir}/openmpi-%{_arch}
%{_includedir}/openmpi-%{_arch}/bout/
%{_includedir}/openmpi-%{_arch}/bout/sys
%{_libdir}/openmpi/lib/*.a
%endif


%changelog
* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.0
- Initial RPM release.
