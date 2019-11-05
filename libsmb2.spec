# TODO: switch to MIT Kerberos, heimdal is missing gss_set_neg_mechs()
#
# Conditional build:
%bcond_without	kerberos5	# system KRB5 library (or builtin NTLMSSP module if disabled)
%bcond_without	static_libs	# static library
%bcond_with	krb5		# MIT Kerberos instead of Heimdal
#
Summary:	Client library for accessing SMB shares over a network
Summary(pl.UTF-8):	Biblioteka kliencka do dostępu do udziałów SMB w sieci
Name:		libsmb2
Version:	3.0.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/sahlberg/libsmb2/releases
Source0:	https://github.com/sahlberg/libsmb2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e70c2c1e4cd3b04c1993c9fa6c37ed89
Patch0:		%{name}-heimdal.patch
URL:		https://github.com/sahlberg/libsmb2
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
Suggests:	gssntlmssp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Client library for accessing SMB shares over a network.

%description -l pl.UTF-8
Biblioteka kliencka do dostępu do udziałów SMB w sieci.

%package devel
Summary:	Header files for libsmb2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsmb2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libsmb2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsmb2.

%package static
Summary:	Static libsmb2 library
Summary(pl.UTF-8):	Statyczna biblioteka libsmb2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsmb2 library.

%description static -l pl.UTF-8
Statyczna biblioteka libsmb2.

%prep
%setup -q
%if %{without krb5}
%patch0 -p1
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{!?with_kerberos5:--without-libkrb5}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsmb2.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libsmb2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsmb2.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsmb2.so
%{_includedir}/smb2
%{_pkgconfigdir}/libsmb2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsmb2.a
%endif
