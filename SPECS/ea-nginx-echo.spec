Name:           ea-nginx-echo
Version:        0.63
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4552 for more details
%define release_prefix 1
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
. /opt/cpanel/ea-nginx-ngxdev/set_NGINX_CONFIGURE_array.sh
./configure "${NGINX_CONFIGURE[@]}" --add-dynamic-module=$mypwd

make

popd

%install
set -x 

if [ "$NAME" = "Ubuntu" ]; then
# This allows me to maintain this code in the SPEC file
# buildroot and libdir are wrong for Ubuntu

install -D %{SOURCE1} $DEB_INSTALL_ROOT/etc/nginx/conf.d/modules/ea-nginx-echo-module.conf
install -D ./nginx-build/objs/ngx_http_echo_module.so $DEB_INSTALL_ROOT/usr/lib64/nginx/modules/ngx_http_echo_module.so
else
# We are CentOS
install -D %{SOURCE1} %{buildroot}/etc/nginx/conf.d/modules/ea-nginx-echo-module.conf
install -D ./nginx-build/objs/ngx_http_echo_module.so %{buildroot}%{_libdir}/nginx/modules/ngx_http_echo_module.so
fi

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/nginx/conf.d/modules/ea-nginx-echo-module.conf
%attr(0755,root,root) %{_libdir}/nginx/modules/ngx_http_echo_module.so

%changelog
* Tue Apr 11 2023 Julian Brown <julian.brown@cpanel.net> - 0.63-1
- ZC-10483: Create ea-nginx-echo module

