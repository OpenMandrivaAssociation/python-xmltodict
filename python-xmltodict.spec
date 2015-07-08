%global srcname xmltodict
%define py3dir python3

Name:               python-xmltodict
Version:            0.9.2
Release:            1
Summary:            Makes working with XML feel like you are working with JSON

Group:              Development/Python
License:            MIT
URL:                https://github.com/martinblech/xmltodict
Source0:            http://pypi.python.org/packages/source/x/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      pkgconfig(python2)
BuildRequires:      python-nose

BuildRequires:      pkgconfig(python3)
BuildRequires:      python3-nose

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


%package -n python3-xmltodict
Summary:            Makes working with XML feel like you are working with JSON
Group:              Development/Python

Requires:           python3

%description -n python3-xmltodict
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

%prep
%setup -q -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'
rm -rf ../%{py3dir}
cp -a . ../%{py3dir}
mv ../%{py3dir} .
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%{__python} setup.py build
pushd %{py3dir}
%{__python3} setup.py build
popd

%install
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

%check
nosetests-%{py_ver}
pushd %{py3dir}
nosetests-%{py3_ver}
popd

%files
%doc README.md LICENSE PKG-INFO
%{python_sitelib}/%{srcname}.py*
%{python_sitelib}/%{srcname}-%{version}*

%files -n python3-xmltodict
%doc README.md LICENSE PKG-INFO
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/%{srcname}-%{version}-*

