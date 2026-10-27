# WattWise Literature Review and Verified References

Bibliographic details were checked against publisher or academic records on **27 October 2026**. The “WattWise relevance / gap” column is a concise project-specific interpretation; it is not presented as a quotation or as a finding WattWise has independently reproduced.

## Compact 10-paper review table

| No. | Year | Paper / research focus | Method or technology discussed | Relevance to WattWise | Important limitation or gap for this project |
|---:|---:|---|---|---|---|
| [1] | 2007 | *Using intelligent data analysis to detect abnormal energy consumption in buildings* | Robust outlier detection using historical daily energy and day-type groupings | Early evidence that statistical screening can prioritize building-energy investigation | Uses historical building/day-type context; a global hourly IQR is simpler and cannot diagnose operational causes |
| [2] | 2015 | *A clustering approach to domestic electricity load profile characterisation using smart metering data* | k-means, k-medoid, self-organizing maps, and household profile classes | Shows why intraday and day-pattern visualization can be useful | Clustering and household-attribute analysis require more data/complexity; WattWise does not claim consumer segmentation |
| [3] | 2016 | *Probabilistic electric load forecasting: A tutorial review* | Probabilistic load forecasting and evaluation | Identifies forecasting and uncertainty as possible future extensions | Forecasting is not the same as anomaly investigation or waste diagnosis; no forecasting model is built or benchmarked here |
| [4] | 2018 | *A review of data-driven building energy consumption prediction studies* | Review of preprocessing, temporal granularity, features, statistical and ML prediction | Reinforces the importance of data preparation, units, granularity, and evaluation | Primarily prediction-oriented; real features and a valid experiment would be needed before comparing ML with IQR |
| [5] | 2019 | *Review of Smart Meter Data Analytics: Applications, Methodologies, and Challenges* | Descriptive, predictive, and prescriptive smart-meter analytics | Positions WattWise as an understandable descriptive-analysis foundation | Broad smart-meter workflows include data, privacy, and deployment challenges beyond a two-column local CSV tool |
| [6] | 2020 | *Building power consumption datasets: Survey, taxonomy and future directions* | Survey/taxonomy of 31 datasets, sampling, submetering, collection platforms, and privacy | Supports explicit dataset description and careful distinction between synthetic and real measurements | Dataset context and labels vary; WattWise’s synthetic demonstration cannot establish external real-world validity |
| [7] | 2021 | *Artificial intelligence based anomaly detection of energy consumption in buildings: A review, current trends and new perspectives* | Taxonomy of AI anomaly detection, feature extraction, detection levels, and platforms | Supports treating anomaly definition, interpretation, and visualization as central issues | The review identifies challenges including definitions, annotated data, unified metrics, reproducibility, and privacy; simple IQR does not resolve these |
| [8] | 2021 | *Detecting anomalous energy consumption using contextual analysis of smart meter data* | Four heuristics with contextual grouping; investigation of 50 hostel smart meters | Demonstrates why occupancy and meter context should inform follow-up investigation | Multiple meters and contextual variables are unavailable in WattWise’s minimal CSV; its results are not reproduced or claimed |
| [9] | 2023 | *Anomaly detection method for building energy consumption in multivariate time series based on graph attention mechanism* | Graph convolution/attention with multivariate temporal modelling | Provides an advanced multivariate contrast for conceptual future work | Requires multivariate inputs and trained models; no direct performance comparison with WattWise has been conducted |
| [10] | 2025 | *Data-driven models for electricity theft and anomalous power consumption detection: a systematic review* | Systematic review of ML, deep learning, hybrid models, datasets, privacy, and challenges | Recent overview of anomaly-detection directions and limitations | Electricity theft is a different objective from waste investigation; WattWise makes no theft, fraud, or superior-performance claim |

## IEEE-style research references

[1] J. E. Seem, “Using intelligent data analysis to detect abnormal energy consumption in buildings,” *Energy and Buildings*, vol. 39, no. 1, pp. 52–58, Jan. 2007, doi: [10.1016/j.enbuild.2006.03.033](https://doi.org/10.1016/j.enbuild.2006.03.033).

[2] F. McLoughlin, A. Duffy, and M. Conlon, “A clustering approach to domestic electricity load profile characterisation using smart metering data,” *Applied Energy*, vol. 141, pp. 190–199, Mar. 2015, doi: [10.1016/j.apenergy.2014.12.039](https://doi.org/10.1016/j.apenergy.2014.12.039).

[3] T. Hong and S. Fan, “Probabilistic electric load forecasting: A tutorial review,” *International Journal of Forecasting*, vol. 32, no. 3, pp. 914–938, Jul.–Sep. 2016, doi: [10.1016/j.ijforecast.2015.11.011](https://doi.org/10.1016/j.ijforecast.2015.11.011).

[4] K. Amasyali and N. M. El-Gohary, “A review of data-driven building energy consumption prediction studies,” *Renewable and Sustainable Energy Reviews*, vol. 81, pp. 1192–1205, Jan. 2018, doi: [10.1016/j.rser.2017.04.095](https://doi.org/10.1016/j.rser.2017.04.095).

[5] Y. Wang, Q. Chen, T. Hong, and C. Kang, “Review of Smart Meter Data Analytics: Applications, Methodologies, and Challenges,” *IEEE Transactions on Smart Grid*, vol. 10, no. 3, pp. 3125–3148, May 2019, doi: [10.1109/TSG.2018.2818167](https://doi.org/10.1109/TSG.2018.2818167).

[6] Y. Himeur, A. Alsalemi, F. Bensaali, and A. Amira, “Building power consumption datasets: Survey, taxonomy and future directions,” *Energy and Buildings*, vol. 227, Art. no. 110404, Nov. 2020, doi: [10.1016/j.enbuild.2020.110404](https://doi.org/10.1016/j.enbuild.2020.110404).

[7] Y. Himeur, K. Ghanem, A. Alsalemi, F. Bensaali, and A. Amira, “Artificial intelligence based anomaly detection of energy consumption in buildings: A review, current trends and new perspectives,” *Applied Energy*, vol. 287, Art. no. 116601, Apr. 2021, doi: [10.1016/j.apenergy.2021.116601](https://doi.org/10.1016/j.apenergy.2021.116601).

[8] A. Sial, A. Singh, and A. Mahanti, “Detecting anomalous energy consumption using contextual analysis of smart meter data,” *Wireless Networks*, vol. 27, pp. 4275–4292, 2021, doi: [10.1007/s11276-019-02074-8](https://doi.org/10.1007/s11276-019-02074-8). (Published online in 2019; volume/issue year 2021.)

[9] Z. Zhang, Y. Chen, H. Wang, Q. Fu, J. Chen, and Y. Lu, “Anomaly detection method for building energy consumption in multivariate time series based on graph attention mechanism,” *PLOS ONE*, vol. 18, no. 6, Art. no. e0286770, Jun. 2023, doi: [10.1371/journal.pone.0286770](https://doi.org/10.1371/journal.pone.0286770).

[10] R. Nayak and C. D. Jaidhar, “Data-driven models for electricity theft and anomalous power consumption detection: a systematic review,” *Applied Intelligence*, vol. 55, Art. no. 794, 2025, doi: [10.1007/s10489-025-06663-3](https://doi.org/10.1007/s10489-025-06663-3).

## Technical documentation

[11] Python Software Foundation, “Python 3 Documentation,” [https://docs.python.org/3/](https://docs.python.org/3/).

[12] Python Software Foundation, “unittest — Unit testing framework,” [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html).

[13] NumPy Developers, “NumPy User Guide,” [https://numpy.org/doc/stable/user/](https://numpy.org/doc/stable/user/).

[14] pandas Development Team, “pandas User Guide,” [https://pandas.pydata.org/docs/user_guide/](https://pandas.pydata.org/docs/user_guide/).

[15] Matplotlib Development Team, “Matplotlib Documentation,” [https://matplotlib.org/stable/](https://matplotlib.org/stable/).

[16] Streamlit Inc., “Streamlit Documentation,” [https://docs.streamlit.io/](https://docs.streamlit.io/).

## Publisher / academic verification links

- Seem (2007): [ScienceDirect record](https://www.sciencedirect.com/science/article/abs/pii/S0378778806001514)
- McLoughlin et al. (2015): [ScienceDirect record](https://www.sciencedirect.com/science/article/abs/pii/S0306261914012963)
- Hong and Fan (2016): [Monash University record](https://research.monash.edu/en/publications/probabilistic-electric-load-forecasting-a-tutorial-review/)
- Amasyali and El-Gohary (2018): [University of Illinois record](https://experts.illinois.edu/en/publications/a-review-of-data-driven-building-energy-consumption-prediction-st/)
- Wang et al. (2019): [arXiv record linking the IEEE DOI](https://arxiv.org/abs/1802.04117)
- Himeur et al. (2020): [ScienceDirect record](https://www.sciencedirect.com/science/article/pii/S037877882030815X)
- Himeur et al. (2021): [ScienceDirect record](https://www.sciencedirect.com/science/article/pii/S0306261921001409)
- Sial et al. (2021): [Springer record](https://link.springer.com/article/10.1007/s11276-019-02074-8)
- Zhang et al. (2023): [PLOS record](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0286770)
- Nayak and Jaidhar (2025): [Springer record](https://link.springer.com/article/10.1007/s10489-025-06663-3)
