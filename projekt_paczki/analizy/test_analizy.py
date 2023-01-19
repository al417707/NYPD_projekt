import pytest
import pandas as pd

from analizy import top_5_na_rok
from analizy import diff


Pop1 = pd.read_csv(r'Dane\API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv', skiprows = 3)
GDP1 = pd.read_csv(r'Dane\GDP1.csv', skiprows = 4)
co2 = pd.read_csv(r'Dane\fossil-fuel-co2-emissions-by-nation_csv.csv')

#złe nazwy którejś kolumny
def test_top5_kolumny():
    with pytest.raises(KeyError):
        top_5_na_rok(co2, 'sadasdsad','Per Capita','Total')
    with pytest.raises(KeyError):
        top_5_na_rok(co2, 'Country','PER CAPITA','Total')
    with pytest.raises(KeyError):
        top_5_na_rok(co2, 'Country','PER CAPITA','TOTALALTA')
def test_top5_data():
    # czy typ wyniku się zgadza?
    assert isinstance(top_5_na_rok(co2, 'Country','Per Capita','Total'), pd.DataFrame)


def test_diff_kolumny():
    with pytest.raises(KeyError):
        diff(co2,1900,2000,'asdfsadfsdf','Total')
    with pytest.raises(KeyError):
        diff(co2,1900,2000,'Cement','Totaasdfsadfsdfl')


def test_diff_data():
    # źle podane daty
    assert ((diff(co2,2000,1900,'Cement','Total')).empty)
    assert ((diff(co2, 2002, 2002, 'Cement', 'Total')).empty)
    # czy typ wyniku się zgadza?
    assert isinstance(diff(co2, 2001, 2002, 'Per Capita', 'Total'), pd.DataFrame)
