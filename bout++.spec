Name:    bout++
Version: 4.0.0
Release: 1%{?dist}
Summary: BOUT++
URL:     https://boutproject.github.io/
License: LGPLv3

Source0: https://github.com/boutproject/BOUT-dev/archive/v%{version}.tar.gz

%description
BOUT++ is a framework for writing fluid and plasma simulations in
curvilinear geometry. It is intended to be quite modular, with a
variety of numerical methods and time-integration solvers available.
BOUT++ is primarily designed and tested with reduced plasma fluid
models in mind, but it can evolve any number of equations, with
equations appearing in a readable form.

%prep
%autosetup -n BOUT-dev-%{version}

%build
%configure --enable-debug
%make_build

%install
%make_install

%files
%{_libdir}/*.a
${_includedir}/*.h
${_includedir}/*/*.h

%changelog
                               
