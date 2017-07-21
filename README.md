# UKCP18 CVs
Controlled Vocabularies (CVs) for use in UKCP18

## Using these vocabularies

We strongly recommend that you use the following recipe for working with these vocabularies:

### 1. Set up working directory and a virtualenv

```
mkdir vocabs
cd vocabs/
```

If you are at the Met Office do:

```
/usr/local/sci/bin/virtualenv venv
```

At CEDA/JASMIN, do:

```
virtualenv venv
```

And activate the virtual environment with:

```
source venv/bin/activate
```

### 2. Clone this repository and install the pyessv tool

```
git clone https://github.com/ukcp-data/UKCP18_CVs
pip install pyessv
```

### 3. Clone the "writer" repository 

The `pyessv-writer` repository includes a script to cache the JSON vocabularies in the `UKCP18_CVs` repository on to the local file system (under `~/.esdoc/pyessv-archive/`). Clone it and run the script:

```
git clone https://github.com/ukcp-data/pyessv-writer
cd pyessv-writer/
mkdir  -p ~/.esdoc/pyessv-archive
python sh/write_ukcp18_cvs.py --source=../UKCP18_CVs
```

### 4. Test that it works - using the pyessv library

```
$ python
Python 2.7.3 (default, Feb 21 2014, 13:11:38)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyessv
2017-07-13T07:41:27.655177 [INFO] :: ES-DOC PYESSV :: Loading vocabularies from /home/users/astephen/.esdoc/pyessv-archive:
/home/users/astephen/.esdoc/pyessv-archive/ukcp

insts = pyessv.load('ukcp', 'ukcp18', 'institution-id')

2017-07-13T07:41:35.731509 [INFO] :: ES-DOC PYESSV :: ... loaded: eustace-team
2017-07-13T07:41:35.732493 [INFO] :: ES-DOC PYESSV :: ... loaded: glamod-team
2017-07-13T07:41:35.733418 [INFO] :: ES-DOC PYESSV :: ... loaded: ukcp
2017-07-13T07:41:35.742762 [INFO] :: ES-DOC PYESSV :: ... loaded: wcrp
>>> insts = pyessv.load('ukcp', 'ukcp18', 'institution-id')

>>> for i in insts: print i
...
ukcp:ukcp18:institution-id:awi
ukcp:ukcp18:institution-id:bnu
ukcp:ukcp18:institution-id:cams
ukcp:ukcp18:institution-id:cccma
ukcp:ukcp18:institution-id:cccr-iitm
ukcp:ukcp18:institution-id:cmcc
...
ukcp:ukcp18:institution-id:noaa-ncep
ukcp:ukcp18:institution-id:nuist
ukcp:ukcp18:institution-id:pcmdi
ukcp:ukcp18:institution-id:thu
```

See examples at:

https://github.com/ES-DOC/pyessv/blob/master/notebooks/pyessv-and-cmip6.ipynb

## Doing the entire install in a script

To do the above in one go, put this in a script (such as `install-vocabs.sh`), give it execute permission, and then run it.

Before you run it, set this environment variable for your `virtualenv` path:

```
# At CEDA/JASMIN:
export VIRTUALENV_DIR=/usr/bin

# At the Met Office:
export VIRTUALENV_DIR=/usr/local/sci/bin
```

Then run this script:

```
mkdir vocabs
cd vocabs/
${VIRTUALENV_DIR}/virtualenv venv
source venv/bin/activate

git clone https://github.com/ukcp-data/UKCP18_CVs
pip install pyessv

git clone https://github.com/ukcp-data/pyessv-writer
cd pyessv-writer/
mkdir  -p ~/.esdoc/pyessv-archive
python sh/write_ukcp18_cvs.py --source=../UKCP18_CVs
```

Test it with:

```
$ python
>>> import pyessv
>>> insts = pyessv.load('ukcp', 'ukcp18', 'institution-id')
>>> for i in insts: print i
```
