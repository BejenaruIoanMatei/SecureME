import Levenshtein
from urllib.parse import urlparse
import string
import pandas as pd
import re

suspicious_keywords = [
    'login', 'signin', 'verify', 'update', 'banking', 'account',
    'secure', 'ebay', 'paypal', 'invoice', 'credentials',
    'password', 'confirm', 'webscr', 'security', 'submit',
    'redirect', 'authentication', 'download', 'free', 'bonus',
    'win', 'reset', 'access', 'click', 'alert', 'support'
]

legit_domains = [
    'google.com', 'facebook.com', 'paypal.com', 'amazon.com',
    'apple.com', 'microsoft.com', 'netflix.com', 'instagram.com',
    'ebay.com', 'linkedin.com', 'bankofamerica.com'
]

def get_min_levenshtein_distance(url, legit_domains):
    try:
        domain = urlparse(url).netloc.lower()
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            main_domain = domain_parts[-2] + '.' + domain_parts[-1]
        else:
            main_domain = domain
        distances = [Levenshtein.distance(main_domain, legit) for legit in legit_domains]
        return min(distances)
    except:
        return 100

def extract_features(url):
    features = {}

    features['url_length'] = len(url)

    features['num_digits'] = sum(c.isdigit() for c in url)

    features['num_special_chars'] = sum(c in string.punctuation for c in url)

    features['num_subdomains'] = url.count('.') - 1

    features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    features['has_https'] = int('https' in url.lower())

    features['num_params'] = url.count('?')

    features['num_fragments'] = url.count('#')

    features['num_slashes'] = url.count('/')

    features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))

    tld = url.split('.')[-1]
    features['tld_length'] = len(tld)

    features['is_common_tld'] = int(tld in ['com', 'org', 'net', 'edu', 'gov'])

    features['has_hex'] = int(bool(re.search(r'%[0-9a-fA-F]{2}', url)))

    features['repeated_chars'] = int(bool(re.search(r'(.)\1{3,}', url)))
    
    features['suspicious_word_count'] = sum(word in url.lower() for word in suspicious_keywords)
    
    features['has_exe'] = int('.exe' in url.lower())
    features['has_zip'] = int('.zip' in url.lower())
    features['has_apk'] = int('.apk' in url.lower())

    features['special_char_ratio'] = features['num_special_chars'] / features['url_length']
    
    features['levenshtein_min'] = get_min_levenshtein_distance(url, legit_domains)
    
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    main_domain = domain.split('.')[-2] if len(domain.split('.')) >= 2 else domain
    features['main_domain_length'] = len(main_domain)


    return pd.Series(features)
