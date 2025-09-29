# TODO: finish bpf
Summary:	stalld - detect starving threads and boost them
Summary(pl.UTF-8):	stalld - wykrywanie głodujących wątków i przyspieszanie ich
Name:		stalld
Version:	1.20.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/utils/stalld/%{name}-%{version}.tar.xz
# Source0-md5:	f16f6462bcbc604b535eafc1a6465783
Patch0:		%{name}-throttlectl.patch
URL:		https://gitlab.com/rt-linux-tools/stalld
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The stalld program (which stands for 'stall daemon') is a mechanism to
prevent the starvation of operating system threads in a Linux system.

%description -l pl.UTF-8
Program stalld (skrót od "stall daemon") to mechanizm zapobiegający
zagłodzeniu wątków systemu operacyjnego pod Linuksem.

%prep
%setup -q
%patch -P0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -DVERSION=\\\"%{version}\\\"" \
	LDFLAGS="%{rpmldflags}" \
	USE_BPF=0

%install
rm -rf $RPM_BUILD_ROOT

# DESTDIR must exist before make install due to realpath call
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	UNITDIR=%{systemdunitdir} \
	USE_BPF=0

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post stalld.service

%preun
%systemd_preun stalld.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/stalld
%attr(755,root,root) %{_bindir}/throttlectl
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stalld
%{systemdunitdir}/stalld.service
%{_mandir}/man8/stalld.8*
