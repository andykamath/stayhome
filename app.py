from flask import Flask, render_template, request
import json
from utils import *

app = Flask(__name__)

@app.route('/whatif')
def main():
    totals = fetch()

    base, r0 = regress(np.arange(0, len(totals)), totals['positive'])
    vals = what_if(totals['positive'], len(totals) - 8, int(request.args.get('pct')))
    totals['expected_positive'] = [base * r0**i for i in range(len(totals))]
    totals['new_positive'] = vals
    mortality_rate = totals['death'][-1] / totals['positive'][-1]
    hosp_rate = totals['hospitalized'][-1] / totals['positive'][-1]
    totals['expected_death'] = mortality_rate * totals['expected_positive']
    totals['expected_hospitalized'] = hosp_rate * totals['expected_positive']
    totals['new_death'] = mortality_rate * totals['new_positive']
    totals['new_hospitalized'] = hosp_rate * totals['new_positive']
    totals['day'] = np.arange(0, len(totals))
    totals['positive_rate'] = totals['positive'] / (totals['positive'] + totals['negative'])
    totals = totals.to_dict('list')
    totals['base'] = int(base * 1000) / 1000
    totals['r0'] = int(r0 * 1000) / 1000
    return totals

@app.route('/')
def hello_world():
    # return main('positive')
    return render_template('index.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=80)
