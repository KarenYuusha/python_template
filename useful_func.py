from collections import Counter
import math

def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_square(v):
    return dot(v, v)

def mean(x):
    return sum(x) / len(x)

def med(x):
    sorted_X = sorted(x)
    n = len(x)
    mid = n // 2
    
    if n % 2:
        return x[mid]
    else:
        return (sorted_X[mid] + sorted_X[mid - 1]) / 2
    
def mode(x):
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items()
            if count == max_count]
    
def data_range(x):
    return max(x) - min(x)

def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x):
    deviation = de_mean(x)
    n = len(x)
    return sum_of_square(deviation) / (n - 1)

def standard_deviation(x):
    return math.sqrt(variance(x))

def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)

def correlation(x, y):
    """test"""
    return covariance(x, y) / standard_deviation(x) / standard_deviation(y)

def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))

def normal_cdf(x, mu=0,sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
    low_z, low_p = -10.0, 0 
    hi_z, hi_p = 10.0, 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2 
        mid_p = normal_cdf(mid_z)
        if mid_p < p:
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z

def parse_header(header_line):
    return header_line.strip().split(',')

def parse_value(data_line):
    values = []
    
    for item in data_line.strip().split(','):
        if item == '':
            values.append(0.0)
        else:
            try:
                values.append(float(item))
            except ValueError:
                values.append(item)
                
    return values

def create_item_dict(headers, values):
    result = {}
    
    for value, header in zip(values, headers):
        result[header] = value
        
    return result

def read_csv(path):
    result = []
    
    with open(path) as file:
        lines = file.readlines()
        headers = parse_header(lines[0])
        
        for data_line in lines[1:]:
            values = parse_value(data_line)
            result.append(create_item_dict(headers, values))
            
    return result

def write_csv(items, path):
    with open(path, 'w') as f:
        if len(items) == 0:
            return
        
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        
        for item in items:
            value = []
            for header in headers:
                value.append(str(item.get(header, '')))
            f.write(','.join(value) + '\n')

def read_csv_columnar(path):
    with open(path) as data:
        lines = data.readlines()
        headers = parse_header(lines[0])
        res = {}
        
        for header in headers:
            res[header] = []
        
        for line in lines[1:]:
            values = parse_value(line)
            for i in range(len(values)):
                res[headers[i]].append(values[i])
    return res