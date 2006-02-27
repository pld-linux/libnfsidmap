Summary:	Library to help mapping id's, mainly for NFSv4
Summary(pl):	Biblioteka pomagaj±ca w mapowaniu identyfikatorów, g³ównie dla NFSv4
Name:		libnfsidmap
Version:	0.13
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/%{name}-%{version}.tar.gz
# Source0-md5:	64dc85168cabf5c5d1009200f9f3813c
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
BuildRequires:	openldap-devel >= 2.3.0
Obsoletes:	nfsidmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library to help mapping id's, mainly for NFSv4.

%description -l pl
Biblioteka pomagaj±ca w mapowaniu identyfikatorów, g³ównie dla NFSv4.

%package devel
Summary:	Header files for libnfsidmap library
Summary(pl):	Pliki nag³ówkowe biblioteki libnfsidmap
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openldap-devel >= 2.3.0
Obsoletes:	nfsidmap-devel

%description devel
Header files for libnfsidmap library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libnfsidmap.

%package static
Summary:	Static libnfsidmap library
Summary(pl):	Statyczna biblioteka libnfsidmap
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	nfsidmap-static

%description static
Static libnfsidmap library.

%description static -l pl
Statyczna biblioteka libnfsidmap.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libnfsidmap.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnfsidmap.so
%{_libdir}/libnfsidmap.la
%{_includedir}/nfsidmap.h
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnfsidmap.a
