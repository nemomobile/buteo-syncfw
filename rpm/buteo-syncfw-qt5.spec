Name: buteo-syncfw-qt5
Version: 0.7.20
Release: 1
Summary: Synchronization backend
Group: System/Libraries
URL: https://github.com/nemomobile/buteo-syncfw
License: LGPLv2.1
Source0: %{name}-%{version}.tar.gz
BuildRequires: doxygen, fdupes
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(accounts-qt5) >= 1.13
BuildRequires: pkgconfig(libsignon-qt5)
BuildRequires: pkgconfig(Qt5SystemInfo)
BuildRequires: pkgconfig(libiphb)
BuildRequires: pkgconfig(qt5-boostable)
BuildRequires: pkgconfig(keepalive)
BuildRequires: oneshot
BuildRequires: doxygen
Requires: mapplauncherd-qt5
Requires: oneshot
%{_oneshot_requires_post}

%description
%{summary}.

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_oneshotdir}/msyncd-storage-perm

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.prl
%{_libdir}/pkgconfig/*.pc

%package msyncd
Summary: Buteo sync daemon
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: systemd
Requires: systemd-user-session-targets
Provides: buteo-syncfw-msyncd = %{version}
Obsoletes: buteo-syncfw-msyncd < %{version}

%description msyncd
%{summary}.

%files msyncd
%defattr(-,root,root,-)
%config %{_libdir}/systemd/user/*.service
%{_libdir}/systemd/user/user-session.target.wants/*.service
%config %{_sysconfdir}/syncwidget/*
%{_bindir}/msyncd

%package doc
Summary: Documentation for %{name}
Group: Documentation

%description doc
%{summary}.

%files doc
%defattr(-,root,root,-)
%{_docdir}/buteo-syncfw-doc/*

%package tests
Summary: Tests for %{name}
Group: Development/Libraries

%description tests
%{summary}.

%files tests
%defattr(-,root,root,-)
/opt/tests/buteo-syncfw/*
%{_datadir}/accounts/services/*.service


%prep
%setup -q


%build
%qmake5 -recursive CONFIG+=usb-moded DEFINES+=USE_KEEPALIVE
make %{_smp_mflags}
make doc %{_smp_mflags}


%install
make INSTALL_ROOT=%{buildroot} install
chmod +x %{buildroot}/opt/tests/buteo-syncfw/*.pl %{buildroot}/opt/tests/buteo-syncfw/*.sh
%fdupes %{buildroot}/opt/tests/buteo-syncfw/
mkdir -p %{buildroot}%{_libdir}/systemd/user/user-session.target.wants
ln -s ../msyncd.service %{buildroot}%{_libdir}/systemd/user/user-session.target.wants/

mkdir -p %{buildroot}/%{_oneshotdir}
install -D -m 755 oneshot/msyncd-storage-perm %{buildroot}/%{_oneshotdir}

%post
/sbin/ldconfig
%{_bindir}/add-oneshot msyncd-storage-perm
if [ "$1" -ge 1 ]; then
    echo "if you manually installed the package, you should invoke 'systemctl --user daemon-reload' and then 'systemctl --user restart msyncd'" || :
fi

%postun
/sbin/ldconfig
if [ "$1" -eq 0 ]; then
    echo "if you manually uninstalled the package, you should invoke 'systemctl --user stop msyncd' and then 'systemctl --user daemon-reload'" || :
fi
