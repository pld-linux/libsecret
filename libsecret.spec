#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_without	static_libs	# static library
%bcond_without	tpm2		# TPM2 support
%bcond_without	vala            # Vala API

Summary:	Library for storing and retrieving passwords and other secrets
Summary(pl.UTF-8):	Biblioteka do przechowywania i odczytu haseł oraz innych tajnych informacji
Name:		libsecret
Version:	0.20.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libsecret/0.20/%{name}-%{version}.tar.xz
# Source0-md5:	5c9e5a011852c82fa9ed9e61ba91efb5
URL:		https://wiki.gnome.org/Projects/Libsecret
BuildRequires:	gettext-tools >= 0.19.8
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.7}
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 1.29
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.50
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.746
BuildRequires:	tar >= 1:1.22
%{?with_tpm2:BuildRequires:	tpm2-tss-devel >= 3.0.3}
%{?with_vala:BuildRequires:	vala >= 2:0.17.2.12}
BuildRequires:	xz
Requires:	glib2 >= 1:2.44.0
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
Requires:	glib2-devel >= 1:2.38.0
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
BuildArch:	noarch

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
BuildArch:	noarch

%description -n vala-libsecret
libsecret API for Vala language.

%description -n vala-libsecret -l pl.UTF-8
API libsecret dla języka Vala.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dbashcompdir=%{bash_compdir} \
	%{!?with_apidocs:-Dgtk_doc=false} \
	%{?with_tpm2:-Dtpm2=true} \
	%{!?with_vala:-Dvapi=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libsecret-1 $RPM_BUILD_ROOT%{_gtkdocdir}/libsecret
%endif

%find_lang libsecret

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libsecret.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/secret-tool
%attr(755,root,root) %{_libdir}/libsecret-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsecret-1.so.0
%{_libdir}/girepository-1.0/Secret-1.typelib
%{_mandir}/man1/secret-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsecret-1.so
%{_includedir}/libsecret-1
%{_pkgconfigdir}/libsecret-1.pc
%{_pkgconfigdir}/libsecret-unstable.pc
%{_datadir}/gir-1.0/Secret-1.gir

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
%endif
