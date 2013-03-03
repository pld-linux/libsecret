#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
%bcond_without	vala            # do not build Vala API
#
Summary:	Library for storing and retrieving passwords and other secrets
Summary(pl.UTF-8):	Biblioteka do przechowywania i odczytu haseł oraz innych tajnych informacji
Name:		libsecret
Version:	0.13
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libsecret/0.13/%{name}-%{version}.tar.xz
# Source0-md5:	701d96d12c0e026437911ba05abc72b1
URL:		https://live.gnome.org/Libsecret
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 1.29
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
%{?with_vala:BuildRequires:	vala >= 2:0.17.2.12}
Requires:	glib2 >= 1:2.32.0
Requires:	libgcrypt >= 1.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsecret is a library for storing and retrieving passwords and other
secrets. It communicates with the "Secret Service" using DBus.
gnome-keyring and KSecretService are both implementations of a Secret
Service.

%description -l pl.UTF-8
libsecret to biblioteka do przechowywania i odczytu haseł oraz innych
tajnych informacji. Komunikuje się z usługą informacji tajnych
("Secret Service") poprzez DBus. Zarówno gnome-keyring, jak i
KSecretService są implementacjami tej usługi.

%package devel
Summary:	Header files for libsecret library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsecret
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	libgcrypt-devel >= 1.2.2

%description devel
Header files for libsecret library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsecret.

%package static
Summary:	Static libsecret library
Summary(pl.UTF-8):	Statyczna biblioteka libsecret
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsecret library.

%description static -l pl.UTF-8
Statyczna biblioteka libsecret.

%package apidocs
Summary:	libsecret API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libsecret
Group:		Documentation

%description apidocs
libsecret API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libsecret.

%package -n vala-libsecret
Summary:	libsecret API for Vala language
Summary(pl.UTF-8):	API libsecret dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.17.2.12

%description -n vala-libsecret
libsecret API for Vala language.

%description -n vala-libsecret -l pl.UTF-8
API libsecret dla języka Vala.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable vala vala} \
	--with-html-dir=%{_gtkdocdir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang libsecret

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libsecret.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/secret-tool
%attr(755,root,root) %{_libdir}/libsecret-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsecret-1.so.0
%{_libdir}/girepository-1.0/Secret-1.typelib
%{_libdir}/girepository-1.0/SecretUnstable-0.typelib
%{_mandir}/man1/secret-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsecret-1.so
%{_libdir}/libsecret-1.la
%{_includedir}/libsecret-1
%{_pkgconfigdir}/libsecret-1.pc
%{_pkgconfigdir}/libsecret-unstable.pc
%{_datadir}/gir-1.0/Secret-1.gir
%{_datadir}/gir-1.0/SecretUnstable-0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsecret-1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif

%if %{with vala}
%files -n vala-libsecret
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libsecret-1.deps
%{_datadir}/vala/vapi/libsecret-1.vapi
%{_datadir}/vala/vapi/libsecret-unstable.deps
%{_datadir}/vala/vapi/libsecret-unstable.vapi
%{_datadir}/vala/vapi/mock-service-0.vapi
%endif
