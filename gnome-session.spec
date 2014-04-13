Summary:	GNOME session manager
Name:		gnome-session
Version:	3.12.0
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	cf08255030b0ff968a4900eff1c125c6
Source1:	%{name}-gnome.desktop
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	intltool
BuildRequires:	json-glib-devel
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	pkg-config
BuildRequires:	systemd-devel
BuildRequires:	upower-devel >= 0.99.0
Requires(post,preun):	glib-gio-gsettings
Requires:	upower >= 0.99.0
Provides:	xsession
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GNOME session manager and several other session management
related utilities.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

# 3d with llvmpipe
%{__sed} -i "/-llvmpipe/d" data/hardware-compatibility

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--enable-systemd
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/{autostart,default-session,shutdown}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,ha,ig,tk,ps}

%find_lang %{name} --with-gnome --all-name

%clean
rm -fr $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-inhibit
%attr(755,root,root) %{_bindir}/gnome-session-quit
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated-helper
%attr(755,root,root) %{_libexecdir}/gnome-session-failed
%dir %{_datadir}/gnome/autostart
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%dir %{_datadir}/gnome-session/sessions
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%{_datadir}/gnome-session/hardware-compatibility
%{_datadir}/gnome-session/session-properties.ui
%{_datadir}/gnome-session/sessions/gnome-dummy.session
%{_datadir}/gnome-session/sessions/gnome.session
%{_datadir}/xsessions/gnome.desktop
%{_iconsdir}/hicolor/*/*/session-properties.*
%{_mandir}/man[15]/*

