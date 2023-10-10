import requests
from bs4 import BeautifulSoup

class Professor:
    def __init__(self, nome, email, ramal, sala, areas):
        self.nome = nome
        self.email = email
        self.ramal = ramal
        self.sala = sala
        self.areas = areas

class Departamento:
    def __init__(self, url):
        self.url = url
        self.professores = []

    def obter_dados(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Localizar e extrair informações dos professores
        professores_divs = soup.find_all('div', class_='professor')
        for professor_div in professores_divs:
            nome = professor_div.find('div', class_='nome').text.strip()
            email = professor_div.find('div', class_='email').text.strip()
            ramal = professor_div.find('div', class_='ramal').text.strip()
            sala = professor_div.find('div', class_='sala').text.strip()
            areas = professor_div.find('div', class_='areas').text.strip().split(', ')
            
            professor = Professor(nome, email, ramal, sala, areas)
            self.professores.append(professor)

    def listar_professores(self):
        for professor in self.professores:
            print(f'Nome: {professor.nome}')
            print(f'E-mail: {professor.email}')
            print(f'Ramal: {professor.ramal}')
            print(f'Sala: {professor.sala}')
            print(f'Áreas: {", ".join(professor.areas)}')
            print()

    def buscar_por_area(self, area):
        professores_na_area = [professor for professor in self.professores if area in professor.areas]
        if len(professores_na_area) > 0:
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

    area_buscada = 'Inteligência Artificial'  # Substitua pela área desejada
    print(f'\nBuscando professores na área de {area_buscada}:')
    decsi.buscar_por_area(area_buscada)
git     deenp.buscar_por_area(area_buscada)