from pathlib import Path
import urllib.request
from html.parser import HTMLParser
import pandas as pd

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.data_buffer = []
        self.rows = []  # Stocker toutes les lignes
        self.ignore_first_row = True  # Marqueur pour ignorer la première ligne (en-tête)

    def handle_starttag(self, tag, attrs):
        if tag == "table" :  # Repérer une table
            self.in_table = True
        if tag == "tr" and self.in_table:  # Repérer une ligne dans la table
            self.in_row = True
            self.data_buffer = []  # Réinitialiser le buffer des données
            # Si la balise est un <span> avec une classe contenant 'flag', extraire le code du pays
        if tag == "span" and self.in_row:
            for attr in attrs:
                if attr[0] == "class" and "flag" in attr[1]:
                    country_code = attr[1].split()[-1]  # Extraire le code pays (le dernier dans la classe)
                    country_name = country_mapping.get(country_code, 'Unknown Country')
                    self.data_buffer.append(country_name)  # Ajouter le nom du pays au buffer
                if attr[0]=="style":
                    self.data_buffer.append(None)
        
                    
        if tag == "a" and self.in_row :
            for attr in attrs:
                if "team/" in attr[1]:  # Détecter un lien vers une équipe
                        team_link = attr[1]
                        if team_link == "team/":  # Si le lien est vide, ajouter None
                            self.data_buffer.append(None)
        
    
        
    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        if tag == "tr" and self.in_row:
            self.in_row = False
            if self.ignore_first_row:  # Ignorer la première ligne
                self.ignore_first_row = False
            else :
                if self.data_buffer:
                    self.rows.append(self.data_buffer)  # Ajouter la ligne extraite à rows
            #print("Row data: ", self.data_buffer)  # Afficher les données extraites de la ligne
            #print(">> Trouvé balise fermante :", tag)
            
    def handle_data(self, data):
        if self.in_row and data.strip():
            self.data_buffer.append(data.strip())  # Stocker le contenu texte des cellules
    
    def get_data(self):
        return self.rows  # Retourner toutes les lignes

# Dictionnaire de correspondance entre les codes pays et les noms des pays
country_mapping = {
    'si': 'Slovenia',
    'fr': 'France',
    'us': 'United States',
    'it': 'Italy',
    'be':'Belgium',
    'ch': 'Swiss',
    'au':'Australia',
    'dk': 'Denmark',
    'er': 'Eritrea',
    'gb': 'Great Britain',
    'es': 'Spain',
    'nl': 'Dutch',
    'ru':'Russia',
    'pt': 'Portuguese',
    'ec': 'Ecuadore',
    'no': 'Norwegia',
    'mx': 'Mexico',
    'lv':'Latvia',
    'co':'Colombia',
    'nz': 'new zealand',
    'cz': 'Czech Republic',
    'ca': 'Canada',
    'de': 'Germany',
    've': 'Venezuela',
    'ie': 'Ireland',
    'af':'Afghanistan',
    'at': 'Austria',
    'al':'Albanie',
    'dz':'Algeria',
    'ag':'Antigua and Barbuda',
    'ao':'Angola',
    'ar':'Argentina',
    'az':'Azebaijan',
    'ba':'Bosnia and Erzegovina',
    'bb':'Barbados',
    'bh':'Bahrain',
    'bj':'Benin',
    'by':'Belarus',
    'bz':'Belize',
    'bm':'Bermuda',
    'bw':'Botswana',
    'br':'Brazil',
    'bg': 'Bulgaria',
    'bf':'Burkina Faso',
    'bo':'Bolivia',
    'cd': 'Democratic Replublic of the Congo',
    'ci':'Ivory Coast',
    'cm':'Cameroon',
    'cv':'Cape Verde',
    'cl':'chile',
    'cn':'China',
    'cr': 'Costa Rica',
    'hr': 'Crotia',
    'cu': 'Cuba',
    'cw': 'Curaçao',
    'cy': 'Cyprus',
    'do':'Dominican Republic',
    'sv': 'El Salvador',
    'ee': 'Estonia',
    'eg':'Egypt',
    'et': 'Etiopia',
    'fi': 'Finland',
    'gd':'Grenada',
    'ge': 'Georgia',
    'gh':'Gahna',
    'gr': 'Greece',
    'gt': 'Giatemala',
    'gu':'Guam',
    'hk': 'Honkong',
    'hn':'Honduras',
    'hu': 'Hungary',
    'in': 'India',
    'id': 'Indonesia',
    'ir': 'Iran',
    'il': 'Israel',
    'ic':'Ivory Coast',
    'is':'Iceland',
    'iq':'Iraq',
    'jm':'Jamaica',
    'jp': 'Japan',
    'kz': 'Kazakhstan',
    'ke': 'Kenya',
    'xk': 'Kosovo',
    'la': 'laos',
    'lc':'Saint Lucia',
    'lb': 'Lebanon',
    'lt': 'Lithuania',
    'lu': 'Luxembourg',
    'my': 'Malaysia',
    'mu': 'Mauritius',
    'mn': 'Mongolia',
    'me': 'Montenegro',
    'ma': 'Morocco',
    'mc':'Monaco',
    'mo':'Macau',
    'mk':'North Macedonia',
    'ml':'Mali',
    'na': 'Namibia',
    'ni':'Nicaragua',
    'nk': 'North Macedonia',
    'om':'Oman',
    'pa': 'Panama',
    'pe':'Peru',
    'ph': 'Philippines',
    'pl': 'Poland',
    'pr': 'Puerto Rico',
    'py':'Paraguay',
    'qa':'qatar',
    'ro':'Romania',
    'rw': 'Rwanda',
    'rs':'Serbia',
    'sa':'Saudi Arabia',
    'sc':'Seychelles',
    'sg':'Singapore',
    'so':'Somalia',
    'sk':'Slovakia',
    'za':'South Africa',
    'kr':'South Korea',
    'se':'Sweden',
    'tw':'Taiwan',
    'th':'Thailand',
    'tn':'Tunisia',
    'tr':'Türkiye',
    'tt':'Trinitad & Tobago',
    'tz':'Tanzania',
    'ug':'Uganda',
    'ua':'Ukraine',
    'ae':'United Arabes Emirates',
    'uy':'Uruguay',
    'uz':'Uzbekistan',
    'vc':'Saint Vincent and the Grenadines',
    'vg':'Virgin Island',
    'vn':'Vietnam',
    'zw':'Zimbabwe'
    
}

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "cycling_rankings_by_year.csv"
DATES = [
    '2024-10-13', '2020-12-31', '2000-12-31', '1980-12-31',
    '1960-12-31', '1940-12-31', '1920-12-31', '1910-12-31',
]
USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
)


def fetch_rankings(output_path=OUTPUT_PATH):
    parser = MyHTMLParser()
    for date in DATES:
        for offset in range(0, 2600, 100):
            url = (
                "https://www.procyclingstats.com/rankings.php"
                f"?date={date}&nation=&age=&zage=&page=smallerorequal"
                f"&team=&offset={offset}&filter=Filter&p=me&s=season-individual"
            )
            request = urllib.request.Request(url)
            request.add_header('User-Agent', USER_AGENT)
            parser.ignore_first_row = True
            with urllib.request.urlopen(request) as response:
                parser.feed(response.read().decode('utf8'))

    columns = ['ranking', 'previous', 'diff', 'country', 'rider', 'team', 'points']
    df = pd.DataFrame(parser.get_data(), columns=columns)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    print(f"Data saved to {fetch_rankings()}")
