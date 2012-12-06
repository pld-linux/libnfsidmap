#
# Conditional build:
%bcond_without	dietlibc	# don't build static dietlibc library
#
Summary:	Library to help mapping id's, mainly for NFSv4
Summary(pl.UTF-8):	Biblioteka pomagająca w mapowaniu identyfikatorów, głównie dla NFSv4
Name:		libnfsidmap
Version:	0.25
Release:	4
License:	BSD
Group:		Libraries
Source0:	http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/%{name}-%{version}.tar.gz
# Source0-md5:	2ac4893c92716add1a1447ae01df77ab
Patch0:		%{name}-idmapd.conf.patch
Patch1:		%{name}-user@domain.patch
Patch2:		%{name}-diet.patch
URL:		http://www.citi.umich.edu/projects/nfsv4/linux/
%{?with_dietlibc:BuildRequires:	dietlibc-static >= 2:0.31-5}
BuildRequires:	openldap-devel
Obsoletes:	nfsidmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

# to get backslash, we need to escape it from spec parser. therefore "\\|" not "\|" here
%define		dietarch	%(echo %{_target_cpu} | sed -e 's/i.86\\|pentium.\\|athlon/i386/;s/amd64/x86_64/;s/armv.*/arm/')
%define		dietlibdir	%{_prefix}/lib/dietlibc/lib-%{dietarch}

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

%package dietlibc
Summary:	Static dietlibc libnfsidmap library
Summary(pl.UTF-8):	Biblioteka statyczna dietlibc libnfsidmap
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description dietlibc
Static dietlibc libnfsidmap library.

%description dietlibc -l pl.UTF-8
Biblioteka statyczna dietlibc libnfsidmap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%if %{with dietlibc}
%configure \
	CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -Os -D_BSD_SOURCE -D_GNU_SOURCE" \
	--enable-static \
	--disable-shared \
	--disable-ldap

%{__make}
mv .libs/libnfsidmap.a diet-libnfsidmap.a
%{__make} clean
%endif

%configure \
	--with-pluginpath=/%{_lib}/libnfsidmap
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/%{_lib}}
%{?with_dietlibc:install -d $RPM_BUILD_ROOT%{dietlibdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install idmapd.conf $RPM_BUILD_ROOT%{_sysconfdir}

%{?with_dietlibc:install diet-libnfsidmap.a $RPM_BUILD_ROOT%{dietlibdir}/libnfsidmap.a}

mv $RPM_BUILD_ROOT%{_libdir}/libnfsidmap $RPM_BUILD_ROOT/%{_lib}
mv -f $RPM_BUILD_ROOT%{_libdir}/libnfsidmap.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libnfsidmap.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libnfsidmap.so

%{__rm} $RPM_BUILD_ROOT/%{_lib}/libnfsidmap/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/idmapd.conf
%attr(755,root,root) /%{_lib}/libnfsidmap.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libnfsidmap.so.0
%dir /%{_lib}/libnfsidmap
%attr(755,root,root) /%{_lib}/libnfsidmap/nsswitch.so
%attr(755,root,root) /%{_lib}/libnfsidmap/static.so
# -plugin-ldap subpackage?
%attr(755,root,root) /%{_lib}/libnfsidmap/umich_ldap.so
# -plugin-gums subpackage (BR: some datagrid software - VOMS?)
#%attr(755,root,root) /%{_lib}/libnfsidmap/gums.so
%{_mandir}/man5/idmapd.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnfsidmap.so
%{_includedir}/nfsidmap.h
%{_pkgconfigdir}/libnfsidmap.pc
%{_mandir}/man3/nfs4_uid_to_name.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnfsidmap.a

%if %{with dietlibc}
%files dietlibc
%defattr(644,root,root,755)
%{dietlibdir}/libnfsidmap.a
%endif
