%define module xmltodict
%bcond tests 1

Name:		python-xmltodict
Version:	1.0.4
Release:	1
Summary:	Makes working with XML feel like you are working with JSON
Group:		Development/Python
License:	MIT
URL:		https://github.com/martinblech/xmltodict
Source0:	https://files.pythonhosted.org/packages/source/x/%{module}/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildSystem:	python
BuildArch:		noarch

BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%rename python3-xmltodict

%description
xmltodict is a Python module that makes working with XML feel like you are
working with JSON.  It's very fast (Expat-based) and has a streaming mode
with a small memory footprint, suitable for big XML dumps like Discogs or
Wikipedia.

    >>> doc = xmltodict.parse("""
    ... <mydocument has="an attribute">
    ...   <and>
    ...     <many>elements</many>
    ...     <many>more elements</many>
    ...   </and>
    ...   <plus a="complex">
    ...     element as well
    ...   </plus>
    ... </mydocument>
    ... """)
    >>>
    >>> doc['mydocument']['@has']
    u'an attribute'
    >>> doc['mydocument']['and']['many']
    [u'elements', u'more elements']
    >>> doc['mydocument']['plus']['@a']
    u'complex'
    >>> doc['mydocument']['plus']['#text']
    u'element as well'

%prep -a
# Remove bundled egg-info
rm -rf %{module}.egg-info
# fix interpreter
find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
find . -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python|#!%{__python3}|'

%install -a
# set missing executable bit
chmod +x %{buildroot}%{python_sitelib}/%{module}.py

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest -v tests/
%endif

%files
%doc README.md
%license LICENSE
%{python_sitelib}/__pycache__/xmltodict.*.py*
%{python_sitelib}/%{module}.py
%{python_sitelib}/%{module}-%{version}.dist-info
