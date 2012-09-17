Name:		python-django-tastypie-mongoengine
Version:	0.2.3
Release:	2%{?dist}
Summary:	MongoEngine support for django-tastypie.

Group:		Development/Languages
License:	GPLv3+
URL:		https://github.com/mitar/django-tastypie-mongoengine
Source0:	django-tastypie-mongoengine-%{version}.tar.gz

BuildRequires:	python2-devel
BuildRequires:  python-setuptools
Requires:	    python-django-tastypie
Requires:       Django

%description
MongoEngine support for django-tastypie.


%prep
%setup -q -n %{name}-%{version}
rm -rf *egg-info
tar xzf %{SOURCE1}


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{docdir}
cp -p LICENSE README.rst AUTHORS -t $RPM_BUILD_ROOT%{docdir}


%files
%doc README.rst AUTHORS LICENSE
%dir %{python_sitelib}/tastypie_mongoengine
%{python_sitelib}/tastypie_mongoengine/*
%doc %{docdir}

%changelog
* Mon Sep 17 2012 James Slagle <slagle@redhat.com> 0.2.3-2
- new package built with tito

