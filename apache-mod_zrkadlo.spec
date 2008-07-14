%define snap r2137

#Module-Specific definitions
%define mod_name mod_zrkadlo
%define mod_conf B16_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Redirect clients to mirror servers, based on sql database
Name:		apache-%{mod_name}
Version:	1.0
Release:	%mkrel 0.%{snap}.4
Group:		System/Servers
License:	Apache License
URL:		http://en.opensuse.org/Build_Service/Redirector
Source0:	%{mod_name}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_zrkadlo-apu13.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache-mpm-prefork >= 2.2.0
Requires(pre):	apache-mod_form
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_form
Requires:	geoip
Requires:	apr-util-dbd-mysql
Requires:	apache-mod_dbd
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	apr-util-devel >= 1.3.0
BuildRequires:	GeoIP-devel
BuildRequires:	apache-mod_form-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This apache module redirects clients to mirror servers, using an SQL backend.

%prep

%setup -q -n %{mod_name}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c -lGeoIP `apu-1-config --link-ld` -Wc,"-Wall -g" mod_zrkadlo.c

gcc %{optflags} -Wall -lGeoIP -o geoiplookup_continent geoiplookup_continent.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_bindir}

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -m0755 geoiplookup_continent %{buildroot}%{_bindir}/geoiplookup_continent

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt TODO mod_dbd.conf mod_zrkadlo.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%attr(0755,root,root) %{_bindir}/geoiplookup_continent
