from re import L
import yfinance as yf
import yaml
from pathlib import Path
import argparse
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import json,os
from itertools import combinations
import pandas as pd
import fitfuncs
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns


def load_model_params(filename):
    """
    Loads yaml file to dict

    Args:
        filename (str): name of file in current working directory

    Returns:
        dict: dictionary of model parameters
    """
    data = yaml.safe_load(Path(filename).read_text())
    return data

def make_pca_analysis(**params):
    """
    Main function - collects/collates data
    calculates PCA and fits defined in params

    Returns:
        pd.DataFrame: df of PCA results
    """
    
    # Extract your instrument packet here
    cryptos = params['instruments']
    
    # Get cryptocurrency base-quote pairs from yahoo finance
    data = {}
    for c1 in cryptos:
        for c2 in cryptos:
            if c1==c2:
                continue
            else:
                data[(c1,c2)] = yf.download(f"{c1}-{c2}", start=params['start_date'], end=params['end_date'],progress=False, show_errors=False)
                
    # filter the cases where the request returned some data           
    basket = dict(filter(lambda t: len(t[1])>0, data.items()))
    
    # create a df of pairs of base-quote on open price
    basket_df = pd.DataFrame({'-'.join(k): v['Open'] for k,v in basket.items()}).fillna(method='ffill').dropna()
    
    # Initialise an sklearn Standard Scaler object for data standardisation (subtract mean / divide by std)
    scale = StandardScaler()
    
    # Define an sklearn PCA object with n_components from **kwargs
    pca = PCA(n_components=int(params['numPC']))
    
    # Standardise the basket of data
    scaled = scale.fit_transform(basket_df)
    
    # Evaluate the principle components on the scaled data
    components = pd.DataFrame(pca.fit_transform(scaled), index = basket_df.index)
    
    # Concatenate the scaled base-quote data and the components to create a features dataframe
    features = pd.concat([pd.DataFrame(scaled, index=basket_df.index, columns=basket_df.columns), components], axis=1)['2020':]
    
    # Create pair combinations of all columns in features (pair-pair + pair-PC)
    combs = list(combinations(features.columns,2))
    
    # Add a polyomial fit degree to comb list of tuples
    combdata = [(x,y,z) for x,y in combs for z in range(params['fitfuncrange']['start'],params['fitfuncrange']['end'])]
    
    # define your fit function as a selection from 'fitfuncs' - can be passed as CLI
    func = fitfuncs.x_deg_sin_x
    
    # fit a function to the features data for a given 
    results = [curve_fit(func,features[x].values,features[y].values,[1.0]*z) for x,y,z in combdata]
    
    # Calculate the mean absolute erroe (mae) for later use in finding 'goodness of fit'
    maes = [np.mean(abs(features[c[1]] - func(features[c[0]], *r[0]))) for r,c in zip(results, combdata)]
    
    # create a resulting dataframe including the x,y,z values from combdata and the mae
    df = pd.DataFrame([(x, y, z, mae) for (x,y,z), mae in zip(combdata, maes)], columns=['x','y','z','mae'])
    
    if params['png']:
        
        fig,axs = plt.subplots(nrows=4,ncols=5,figsize=(25, 25))
        for idx,col in zip(df.sort_values('mae').index[:20],axs.ravel()):
            sns.scatterplot(x=features[df['x'][idx]], y=features[df['y'][idx]], hue=list(range(len(features))),ax=col)
            sns.lineplot(x=features[df['x'][idx]], y=func(features[df['x'][idx]], *results[idx][0]), color='red',ax=col)
        
        fig.suptitle(f"N-{params['numPC']} PCA Analysis on {params['instruments']}")
        # fig.savefig('output.png')
        return fig
        
    if params['outfmt']=='json':
        with open('output.json','w+') as f:
            json.dump(df.to_dict(orient='records'),f)
            
    
    if params['outfmt']=='csv':
        df.to_csv(os.path.join(os.getcwd(),'photos','output.csv'))
        
    return None        
        
    
    
if __name__=='__main__':
    # Load params from yaml
    params = load_model_params('model.yaml')
    
    # Load params from CLI - these will override yaml
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--png',
        type=bool,
        required=False
    )
    parser.add_argument(
        '--outfmt',
        type=str,
        required=False
    )
    parser.add_argument(
        '--fitfunc',
        type=str,
        required=False
    )
    args = parser.parse_args()
    if args.png:
        params['png'] = args.png
    if args.outfmt:
        params['outfmt'] = args.outfmt
    if args.fitfunc:
        params['fitfunc'] = args.fitfunc
        
    # Main lifter
    df = make_pca_analysis(**params)
    
