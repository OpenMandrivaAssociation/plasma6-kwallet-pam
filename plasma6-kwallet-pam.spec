%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define git 20230918

Name: plasma6-kwallet-pam
Version: 5.240.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/plasma/kwallet-pam/-/archive/master/kwallet-pam-master.tar.bz2#/kwallet-pam-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/plasma/%{plasmaver}/%{name}-%{version}.tar.xz
%endif
Summary: PAM support for Kwallet
URL: http://kde.org/
License: GPL
Group: System/Libraries
Patch0: pam_kwallet_init-use-unidirectional-mode-for-socat-v2.patch
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6Wallet)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(KF6Wallet)
BuildRequires: pam-devel
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: socat
# Just to avoid pulling in KF5
BuildRequires: plasma6-xdg-desktop-portal-kde
Requires: socat
Requires: kf6-kwallet

%description
PAM support for Kwallet.
To enable it add these lines to /etc/pam.d/kde:

---------------------
-auth            optional        pam_kwallet5.so
-session         optional        pam_kwallet5.so
---------------------

%prep
%autosetup -p1 -n kwallet-pam-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%{_sysconfdir}/xdg/autostart/pam_kwallet_init.desktop
%{_libdir}/security/pam_kwallet5.so
%{_libdir}/libexec/pam_kwallet_init
%{_userunitdir}/plasma-kwallet-pam.service
