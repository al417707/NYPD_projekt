import pytest

from analizy import wczytaj

def test_wczytaj_sciezka():
    with pytest.raises(FileNotFoundError):
        wczytaj('v','v','v',2004, 2014, {})

def test_wczytaj_lata(capsys):
    wczytaj(r'Dane\API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv',
            r'Dane\GDP1.csv',
            r'Dane\fossil-fuel-co2-emissions-by-nation_csv.csv',
            2024, 2014, {})
    captured = capsys.readouterr()

    #strip bo czyta też znak nowej linii
    assert captured.out.strip() == 'Dla takiego przedziału lat nie ma danych'