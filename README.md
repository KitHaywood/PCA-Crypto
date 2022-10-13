# PCA-Crypto

## Definition
Repo to make a pairplot comparing the covariance of multiple cryptos and their principle components

This tool is a pure python module for producing technical indicators based on the PCA analysis of a set of cryptocurrency instruments, defined in the yaml file. This PCA is produced, cleaned and made available for access as json. It will also take CLI arguments which allow the user to toggle saving the output graphics to a png. 

## Usage - Local Python Environment

First create and install a python virtual environment (note these instructions cater for the linux user).
```bash
python3 -m venv venv/
```
```bash
pip install -r requirements.txt
```
Then activate the virtual environemnt
```bash
source venv/bin/activate
```
Then run the main.py file with the following optional CLI arguments, also noting that these arguments may be found in the yaml file for single space control. The CLI arguments will override the content of the yaml file. 
```bash
python3 main.py --png=True --outfmt='json'
```
## Usage - Docker

This tool is also available as a docker container on dockerhub. 

```bash
docker pull kithaywood/pca-crypto
```
 Then run
 
 ```bash
 docker run pca-crypto
 ```
