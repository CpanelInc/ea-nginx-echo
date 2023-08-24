Name:           ea-nginx-echo
Version:        0.63
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4552 for more details
%define release_prefix 3
Release:        %{release_prefix}%{?dist}.cpanel
Summary:        Echo provides various utilities that help testing and debugging of other modules.
License:        Custom, see LICENSE file.
Group:          System Environment/Libraries
URL:            http://www.cpanel.net
Vendor:         cPanel, Inc.
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  ea-nginx-ngxdev
BuildRequires:  libxml2
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
Requires:       ea-nginx

Source0:        v%{version}.tar.gz
Source1:        ea-nginx-echo-module.conf

%description
This module wraps lots of Nginx internal APIs for streaming input and output, parallel/sequential subrequests, timers and sleeping, as well as various meta data accessing.

Basically it provides various utilities that help testing and debugging of other modules by trivially emulating different kinds of faked subrequest locations.

%prep
%setup -q -n echo-nginx-module-%{version}

%build
set -x

mypwd=`pwd`
# You will be in ./nginx-build after this source()
#    so that configure and make etc can happen.
# We probably want to popd back when we are done in there
. /opt/cpanel/ea-nginx-ngxdev/set_NGINX_CONFIGURE_array.sh
./configure "${NGINX_CONFIGURE[@]}" --add-dynamic-module=$mypwd

make
popd

%install
set -x 

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/nginx/conf.d/modules/ea-nginx-echo-module.conf
install -D ./nginx-build/objs/ngx_http_echo_module.so $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_echo_module.so

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/nginx/conf.d/modules/ea-nginx-echo-module.conf
%attr(0755,root,root) %{_libdir}/nginx/modules/ngx_http_echo_module.so

%changelog
* Thu Aug 24 2023 Cory McIntire <cory@cpanel.net> - 0.63-3
- EA-11631: Build against ea-nginx version v1.25.2

* Thu Jun 15 2023 Cory McIntire <cory@cpanel.net> - 0.63-2
- EA-11496: Build against ea-nginx version v1.25.1

* Tue Apr 11 2023 Julian Brown <julian.brown@cpanel.net> - 0.63-1
- ZC-10483: Create ea-nginx-echo module

