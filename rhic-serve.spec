Name:		rhic-serve
Version:	0.3
Release:	1%{?dist}
Summary:	REST/Web Service for creating RHIC's

Group:		Development/Languages
License:	GPLv2+
URL:		https://github.com/splice/rhic-serve
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python-setuptools
BuildRequires:  python2-devel

Requires:   mongodb-server
Requires:   pymongo
Requires:   pymongo-gridfs
Requires:   httpd
Requires:   mod_wsgi
Requires:   mod_ssl


%description
REST/Web Service for creating RHIC's


%prep
%setup -q


%build
pushd src
%{__python} setup.py build
popd


%install
rm -rf %{buildroot}
pushd src
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}/%{_sysconfdir}/pki/%{name}
mkdir -p %{buildroot}/%{_var}/log/%{name}
mkdir -p %{buildroot}/%{_usr}/lib/rhic_webui
mkdir -p %{buildroot}/%{_localstatedir}/www/html/rhic_webui/

# Install template files
cp -R src/rhic_serve/rhic_webui/templates %{buildroot}/%{_usr}/lib/rhic_webui

# Install static files
cp -R src/rhic_serve/rhic_webui/static %{buildroot}/%{_localstatedir}/www/html/rhic_webui

# Install WSGI script & httpd conf
cp -R srv %{buildroot}
cp etc/httpd/conf.d/%{name}.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/

# Install CA cert and key
cp -R etc/pki/rhic-serve %{buildroot}/%{_sysconfdir}/pki/

# Remove egg info
rm -rf %{buildroot}/%{python_sitelib}/*.egg-info


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}/rhic_serve
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%defattr(-,apache,apache,-)
%dir %{_sysconfdir}/pki/%{name}
%{_sysconfdir}/pki/%{name}
%dir /srv/%{name}
%dir %{_var}/log/%{name}
/srv/%{name}/webservices.wsgi
%{_usr}/lib/rhic_webui/templates
%{_localstatedir}/www/html/rhic_webui/static


%doc


%changelog
* Tue Aug 28 2012 James Slagle <slagle@redhat.com> 0.3-1
- Update apache config (slagle@redhat.com)
- package test ca cert and key (slagle@redhat.com)
- Set new templates dir path in settings.py (slagle@redhat.com)
- Install Django templates (slagle@redhat.com)
- Packaging fixes. (slagle@redhat.com)
- wsgi script (slagle@redhat.com)
- setup.py (slagle@redhat.com)
- Add apache config file (slagle@redhat.com)

* Tue Aug 28 2012 James Slagle <slagle@redhat.com> 0.2-1
- new package built with tito


