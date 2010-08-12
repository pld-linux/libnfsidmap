Summary:	Library to help mapping id's, mainly for NFSv4
Summary(pl.UTF-8):	Biblioteka pomagająca w mapowaniu identyfikatorów, głównie dla NFSv4
Name:		libnfsidmap
Version:	0.23
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/%{name}-%{version}.tar.gz
# Source0-md5:	28f3ece648c1dc5d25e8d623d55f8bd6
Patch0:		%{name}-idmapd.conf.patch
Patch1:		%{name}-user@domain.patch
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
BuildRequires:	openldap-devel
Obsoletes:	nfsidmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
Library to help mapping id's, mainly for NFSv4.

%description -l pl.UTF-8
Biblioteka pomagająca w mapowaniu identyfikatorów, głównie dla NFSv4.

%package devel
Summary:	Header files for libnfsidmap library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnfsidmap
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	nfsidmap-devel

%description devel
Header files for libnfsidmap library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnfsidmap.

%package static
Summary:	Static libnfsidmap library
Summary(pl.UTF-8):	Statyczna biblioteka libnfsidmap
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	nfsidmap-static

%description static
Static libnfsidmap library.

%description static -l pl.UTF-8
Statyczna biblioteka libnfsidmap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install idmapd.conf $RPM_BUILD_ROOT%{_sysconfdir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnfsidmap/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/idmapd.conf
%attr(755,root,root) %{_libdir}/libnfsidmap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnfsidmap.so.0
%dir %{_libdir}/libnfsidmap
%attr(755,root,root) %{_libdir}/libnfsidmap/nsswitch.so
%attr(755,root,root) %{_libdir}/libnfsidmap/static.so
# -plugin-ldap subpackage?
%attr(755,root,root) %{_libdir}/libnfsidmap/umich_ldap.so
# -plugin-gums subpackage (BR: some datagrid software - VOMS?)
#%attr(755,root,root) %{_libdir}/libnfsidmap/gums.so
%{_mandir}/man5/idmapd.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnfsidmap.so
%{_libdir}/libnfsidmap.la
%{_includedir}/nfsidmap.h
%{_pkgconfigdir}/libnfsidmap.pc
%{_mandir}/man3/nfs4_uid_to_name.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnfsidmap.a
