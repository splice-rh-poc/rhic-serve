# rhic-serve package ---------------------------------------------------------
Name:		rhic-serve
Version:	0.5
Release:	1%{?dist}
Summary:	REST/Web Service for creating RHIC's

Group:		Development/Languages
License:	GPLv2+
URL:		https://github.com/splice/rhic-serve
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python-setuptools
BuildRequires:  python2-devel

Requires:   rhic-serve-common
Requires:   rhic-serve-rcs
Requires:   mongodb-server
Requires:   pymongo
Requires:   pymongo-gridfs
Requires:   httpd
Requires:   mod_wsgi
Requires:   mod_ssl
Requires:   python-isodate
Requires:   Django
Requires:   python-django-tastypie
Requires:   python-django-tastypie-mongoengine
Requires:   python-mongoengine


%description
REST/Web Service for creating RHIC's
# ----------------------------------------------------------------------------


# rhic-serve-common subpackage --------------------------------------------------
%package common
Summary:    Common libraries for rhic-serve.
Group:      Development/Languages

%description common
Common libraries for rhic-serve.
# ----------------------------------------------------------------------------


# rhic-serve-rcs subpackage --------------------------------------------------
%package rcs
Summary:    API's for querying RHIC data for use by the RCS.
Group:      Development/Languages
Requires:   rhic-serve-common
Requires:   mongodb-server
Requires:   pymongo
Requires:   httpd
Requires:   mod_wsgi
Requires:   mod_ssl
Requires:   python-isodate
Requires:   Django
Requires:   python-django-tastypie
Requires:   python-django-tastypie-mongoengine
Requires:   python-mongoengine


%description rcs
API's for querying RHIC data for use by the RCS.
# ----------------------------------------------------------------------------


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


%post
echo 01 > %{_sysconfdir}/pki/%{name}/rhic-serve-ca.srl
chown apache:apache %{_sysconfdir}/pki/%{name}/rhic-serve-ca.srl


# rhic-serve-common files -------------------------------------------------------
# This %files is listed first so that we can mark the files for the common
# subpackage and use a wildcard in the next section.
%files common
%defattr(-,apache,apache,-)
%dir /srv/%{name}
/srv/%{name}/webservices.wsgi
%dir %{_sysconfdir}/pki/%{name}
%{_sysconfdir}/pki/%{name}
%defattr(-,root,root,-)
%{python_sitelib}/rhic_serve/common
%{python_sitelib}/rhic_serve/urls.py*
%{python_sitelib}/rhic_serve/settings.py*
%{python_sitelib}/rhic_serve/__init__.py*
# ----------------------------------------------------------------------------


# rhic-serve files -----------------------------------------------------------
%files
%defattr(-,root,root,-)
%{python_sitelib}/rhic_serve/*.py*
%{python_sitelib}/rhic_serve/rhic_rest
%{python_sitelib}/rhic_serve/rhic_webui
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%defattr(-,apache,apache,-)
%{_usr}/lib/rhic_webui/templates
%{_localstatedir}/www/html/rhic_webui/static
# ----------------------------------------------------------------------------


# rhic-serve-rcs files -------------------------------------------------------
%files rcs
%defattr(-,root,root,-)
%{python_sitelib}/rhic_serve/rhic_rcs
# ----------------------------------------------------------------------------


%doc


%changelog
* Mon Sep 17 2012 James Slagle <slagle@redhat.com> 0.5-1
- Spec file updates (slagle@redhat.com)

* Mon Sep 17 2012 James Slagle <slagle@redhat.com> 0.4-1
- Automatic commit of package [python-django-tastypie-mongoengine] minor
  release [0.2.3-3]. (slagle@redhat.com)
- Add docs (slagle@redhat.com)
- package build fixes (slagle@redhat.com)
- Automatic commit of package [python-django-tastypie-mongoengine] minor
  release [0.2.3-2]. (slagle@redhat.com)
- New dep build for django-tastypie-mongoengine (slagle@redhat.com)
- Update exception middleware to use new logging (slagle@redhat.com)
- Add tests for getting deleted and modified rhics (slagle@redhat.com)
- Add tests for rhic_rcs (slagle@redhat.com)
- Refactor web client methods into common base class (slagle@redhat.com)
- Add tests and refactor into a common lib (slagle@redhat.com)
- Override for django-tastypie-mongoengine (slagle@redhat.com)
- Mark required fields as such (slagle@redhat.com)
- use new logging configuration (slagle@redhat.com)
- Fix logging configuration (slagle@redhat.com)
- fix typo (slagle@redhat.com)
- Move dev outside of src/ (slagle@redhat.com)
- sample data load update (slagle@redhat.com)
- CA srl file does not need to be version controlled.  Instead generated it and
  the %%post and the dev settings.py (slagle@redhat.com)
- Add settings.py file for development, so that CA does not have to be
  installed as root (slagle@redhat.com)
- mongo connection should use tz's (slagle@redhat.com)
- Add deleted logic to rhic_rcs (slagle@redhat.com)
- Add deleted flag, and querying ability on delete (slagle@redhat.com)
- Set serializer at the base class level (slagle@redhat.com)
- Add Requires for new dep (slagle@redhat.com)
- Serialize all dates with timezone information in ISO8601 format
  (slagle@redhat.com)
- Add querying for a RHIC based on a date range (slagle@redhat.com)
- Module no longer needed after using latest django-tastypie-mongoengine from
  git (slagle@redhat.com)
- Include resource_uri in fields (slagle@redhat.com)
- Merge branch 'master' into js-refactor (slagle@redhat.com)
- Full module path needed in include() (slagle@redhat.com)
- Fix bug in row selection (slagle@redhat.com)
- Add missing alias for /static (slagle@redhat.com)
- Update sample load script (slagle@redhat.com)
- Undo dev changes to settings.py (slagle@redhat.com)
- Consolidate under one common dir (slagle@redhat.com)
- Fixes for application refactoring (slagle@redhat.com)
- Refactor rhic-serve into seperate apps (slagle@redhat.com)
- exception handling for engineering product conflict (slagle@redhat.com)
- fix create rhic scripts (slagle@redhat.com)
- refactor a bit more (slagle@redhat.com)
- Add script for global variable declaration (slagle@redhat.com)
- A couple more fixes (slagle@redhat.com)
- Move js files under /static and other fixes (slagle@redhat.com)
- Initial attempt at breaking out into seperate js files (slagle@redhat.com)
- Fix product logic on edit screen (slagle@redhat.com)
- Fix product logic on edit screen (slagle@redhat.com)
- UI support for marketing/eng product enable/disable logic (slagle@redhat.com)
- Fix data load scripts and add an example of a marketing product with multiple
  engineering id's (slagle@redhat.com)
- Remove old random data generator (slagle@redhat.com)
- Handle 500's a bit more gracefully in the js UI (slagle@redhat.com)
- Fix button enablement (slagle@redhat.com)
- Serve dataTables js from app instead of remote download (slagle@redhat.com)
- Add uuid field to manage products popup (slagle@redhat.com)
- Don't enable the create cert button until a name, sla, and support level have
  been chosen (which inturn imply has a contract has been chosen
  (slagle@redhat.com)
- Fix row selection again (slagle@redhat.com)
- Fix row highlight and selecting the current row (slagle@redhat.com)
- Add text about pem download (slagle@redhat.com)
- Fix multiple entries on confirmation dialog (slagle@redhat.com)
- set up row_click as a callback (slagle@redhat.com)
- Use uuid to download certificate (slagle@redhat.com)
- Use rhic uuid as resource identifier instead of internal id
  (slagle@redhat.com)
- Add check for username on request.user.  It should always be set, but just to
  be safe. (slagle@redhat.com)
- Switch to using PATCH method, update button/title names (slagle@redhat.com)
- UI fixes (slagle@redhat.com)
- Fix path to ca (slagle@redhat.com)
- Fix path to ca (slagle@redhat.com)
- Install static js files (slagle@redhat.com)
- Change top level of the python packaging (slagle@redhat.com)
- Change top level of the python packaging (slagle@redhat.com)

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


