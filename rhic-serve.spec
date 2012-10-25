# rhic-serve package ---------------------------------------------------------

# SELinux
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)

Name:		rhic-serve
Version:	0.23
Release:	1%{?dist}
Summary:	REST/Web Service for creating RHIC's

Group:		Development/Languages
License:	GPLv2+
URL:		https://github.com/splice/rhic-serve
Source0:	%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires:	python-setuptools
BuildRequires:  python2-devel

Requires:   rhic-serve-common = %{version}
Requires:   rhic-serve-rcs = %{version}
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
Requires:   python-certutils
#
# Our own selinux RPM
#
Requires: %{name}-selinux = %{version}-%{release}

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
Requires:   rhic-serve-common = %{version}
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


%description rcs
API's for querying RHIC data for use by the RCS.

%package        selinux
Summary:        Splice SELinux policy
Group:          Development/Languages
BuildRequires:  rpm-python
BuildRequires:  make
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy-devel
# el6, selinux-policy-doc is the required RPM which will bring below 'policyhelp'
BuildRequires:  /usr/share/selinux/devel/policyhelp
BuildRequires:  hardlink
Requires: selinux-policy >= %{selinux_policyver}
Requires(post): policycoreutils-python 
Requires(post): selinux-policy-targeted
Requires(post): /usr/sbin/semodule, /sbin/fixfiles, /usr/sbin/semanage
Requires(postun): /usr/sbin/semodule

%description  selinux
SELinux policy for rhic-serve

# ----------------------------------------------------------------------------
%prep
%setup -q


%build
pushd src
%{__python} setup.py build
popd
# SELinux Configuration
cd selinux
perl -i -pe 'BEGIN { $VER = join ".", grep /^\d+$/, split /\./, "%{version}.%{release}"; } s!0.0.0!$VER!g;' rhic-serve.te
./build.sh
cd -

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

# Install SELinux policy modules
cd selinux
./install.sh %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_datadir}/%{name}/selinux
cp enable.sh %{buildroot}%{_datadir}/%{name}/selinux
cp uninstall.sh %{buildroot}%{_datadir}/%{name}/selinux
cp relabel.sh %{buildroot}%{_datadir}/%{name}/selinux
cd -

%clean
rm -rf %{buildroot}

%post selinux
# Enable SELinux policy modules
if /usr/sbin/selinuxenabled ; then
 %{_datadir}/%{name}/selinux/enable.sh %{_datadir}
fi

# Continuing with using posttrans, as we did this for Pulp and it worked for us.
# restorcecon wasn't reading new file contexts we added when running under 'post' so moved to 'posttrans'
# Spacewalk saw same issue and filed BZ here: https://bugzilla.redhat.com/show_bug.cgi?id=505066
%posttrans selinux
if /usr/sbin/selinuxenabled ; then
 %{_datadir}/%{name}/selinux/relabel.sh %{_datadir}
fi

%preun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
  %{_datadir}/%{name}/selinux/uninstall.sh
  %{_datadir}/%{name}/selinux/relabel.sh
fi
exit 0


%post
echo 01 > %{_sysconfdir}/pki/%{name}/rhic-serve-ca.srl
chown apache:apache %{_sysconfdir}/pki/%{name}/rhic-serve-ca.srl


# rhic-serve-common files -------------------------------------------------------
# This %files is listed first so that we can mark the files for the common
# subpackage and use a wildcard in the next section.
%files common
%defattr(-,root,root,-)
%{python_sitelib}/rhic_serve/common
%{python_sitelib}/rhic_serve/__init__.py*
# ----------------------------------------------------------------------------


# rhic-serve files -----------------------------------------------------------
%files
%defattr(-,apache,apache,-)
%dir /srv/%{name}
/srv/%{name}/webservices.wsgi
%dir %{_sysconfdir}/pki/%{name}
%{_sysconfdir}/pki/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
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

%files selinux
%defattr(-,root,root,-)
%doc selinux/%{name}.fc selinux/%{name}.if selinux/%{name}.te
%{_datadir}/%{name}/selinux/*
%{_datadir}/selinux/*/%{name}.pp
%{_datadir}/selinux/devel/include/apps/%{name}.if

%doc


%changelog
* Thu Oct 25 2012 James Slagle <jslagle@redhat.com> 0.23-1
- Use X509 authentication for rcs api (jslagle@redhat.com)
- Doc updates (jslagle@redhat.com)
- Initial sphinx docs (jslagle@redhat.com)

* Tue Oct 16 2012 James Slagle <jslagle@redhat.com> 0.22-1
- Set account_id as Origanization in the rhic subject (jslagle@redhat.com)

* Mon Oct 15 2012 James Slagle <jslagle@redhat.com> 0.21-1
- Build noarch (jslagle@redhat.com)

* Mon Oct 15 2012 James Slagle <jslagle@redhat.com> 0.20-1
- Migrate to use python-certutils package (jslagle@redhat.com)

* Mon Oct 15 2012 John Matthews <jmatthews@redhat.com> 0.19-1
- Fix so selinux module has version info (jmatthews@redhat.com)

* Mon Oct 15 2012 John Matthews <jmatthews@redhat.com> 0.18-1
- Initial cut of a SELinux policy (jmatthews@redhat.com)

* Fri Oct 05 2012 John Matthews <jmatthews@redhat.com> 0.17-1
- Allowing pagination to not have an upper limit (jmatthews@redhat.com)

* Tue Oct 02 2012 James Slagle <slagle@redhat.com> 0.16-1
- Include deleted rhics in response by default for rhic_rcs (slagle@redhat.com)

* Mon Oct 01 2012 James Slagle <slagle@redhat.com> 0.15-1
- rhic-serve-common should not require rhic-serve (slagle@redhat.com)

* Thu Sep 27 2012 James Slagle <slagle@redhat.com> 0.14-1
- Enable pagination for rhic_rcs (slagle@redhat.com)

* Thu Sep 27 2012 James Slagle <slagle@redhat.com> 0.13-1
- Keep all versions of sub-packages at the same versions (slagle@redhat.com)

* Thu Sep 27 2012 James Slagle <slagle@redhat.com> 0.12-1
- Update to latest CA (slagle@redhat.com)
- Grey out label text on disabled selectors as well (slagle@redhat.com)
- Use encompassing <label> tags around rhic choices, so that you can click the
  text, not just the selector (slagle@redhat.com)
- Clear the addedProducts variable from a different method (slagle@redhat.com)

* Thu Sep 20 2012 James Slagle <slagle@redhat.com> 0.11-1
- products and engineering_ids should not be required fields, they can be empty
  (slagle@redhat.com)
- Specify rhic_serve db alias instead of relying on default alias.  This is
  more robust (slagle@redhat.com)

* Wed Sep 19 2012 James Slagle <slagle@redhat.com> 0.10-1
- rhic-serve-rcs is not meant to be a standalone wsgi app so move those files
  back to the rhic-serve package (slagle@redhat.com)
- Merge branch 'master' of github.com:splice/rhic-serve (slagle@redhat.com)
- Default binary to False (slagle@redhat.com)
- Added 'allow_inheritance' on rhic-server-rcs models.RHIC
  (jmatthews@redhat.com)

* Wed Sep 19 2012 James Slagle <slagle@redhat.com> 0.9-1
- Use a versioned top level api (slagle@redhat.com)
- Add LICENSE file (slagle@redhat.com)

* Tue Sep 18 2012 James Slagle <slagle@redhat.com> 0.8-1
- Refactoring fixes (slagle@redhat.com)

* Tue Sep 18 2012 James Slagle <slagle@redhat.com> 0.7-1
- Packaging fixes (slagle@redhat.com)

* Tue Sep 18 2012 James Slagle <slagle@redhat.com> 0.6-1
- Move needed files into -common subpackage (slagle@redhat.com)
- Automatic commit of package [python-django-tastypie-mongoengine] minor
  release [0.2.3-4]. (slagle@redhat.com)
- Add missing Requires (slagle@redhat.com)

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


