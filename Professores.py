import requests
from bs4 import BeautifulSoup

class Professor:
    def __init__(self, nome, email, lattes, area, ramal, sala):
        self.nome = nome
        self.email = email
        self.lattes = lattes
        self.area = area
        self.ramal = ramal
        self.sala = sala

class Departamento:
    def __init__(self, url):
        self.url = url
        self.professores = []

    def obter_dados(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if "deenp" in self.url:
            # Parsing do HTML do DEENP
            table = soup.find('table')
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                if len(columns) >= 7:
                    nome = columns[0].text.strip()
                    lattes_element = columns[1].find('a')
                    lattes = lattes_element['href'] if lattes_element else ""
                    area = columns[3].text.strip()
                    ramal = columns[4].text.strip()
                    sala = columns[5].text.strip()
                    email_element = columns[6].find('a')
                    email = email_element['href'].replace('mailto:', '').strip() if email_element else ""
                    professor = Professor(nome, email, lattes, area, ramal, sala)
                    self.professores.append(professor)
        else:
            # Parsing do HTML da DECSI
            professor_elements = soup.find_all('h3')
            for element in professor_elements:
                nome = element.text.strip()
                email_element = element.find_next('a', href=True)
                email = email_element['href'].replace('mailto:', '').strip() if email_element else ""
                lattes_element = element.find_next('strong', text='Lattes:')
                lattes = lattes_element.find_next('a')['href'] if lattes_element else ""
                area_element = element.find_next('strong', text='Linha de pesquisa: ')
                area = area_element.find_next('span').text.strip() if area_element else ""
                professor = Professor(nome, email, lattes, area, None, None)
                self.professores.append(professor)

    def listar_professores(self):
        for professor in self.professores:
            print(f'Nome: {professor.nome}')
            print(f'E-mail: {professor.email}')
            print(f'Lattes: {professor.lattes}')
            print(f'Área: {professor.area}')
            if professor.ramal:
                print(f'Ramal: {professor.ramal}')
            if professor.sala:
                print(f'Sala: {professor.sala}')
            print()

    def buscar_por_area(self, area):
        professores_na_area = [professor for professor in self.professores if area.lower() in professor.area.lower()]
        if professores_na_area:
            print(f'Professores na área de {area}:')
            for professor in professores_na_area:
                print(professor.nome)
        else:
            print(f'Nenhum professor encontrado na área de {area}.')

# Exemplo de uso
if __name__ == "__main__":
    decsi = Departamento('https://decsi.ufop.br/docentes')
    deenp = Departamento('https://deenp.ufop.br/corpo-docente')

    decsi.obter_dados()
    deenp.obter_dados()

    print('Professores do DECSI:')
    decsi.listar_professores()

    print('\nProfessores do DEENP:')
    deenp.listar_professores()

    area_buscada = 'Engenharia Organizacional'  # Substitua pela área desejada
    print(f'\nBuscando professores na área de {area_buscada}:')
    decsi.buscar_por_area(area_buscada)
    deenp.buscar_por_area(area_buscada)
