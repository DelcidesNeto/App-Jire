from flask import Flask, render_template, redirect, request
from url_api import url
import xmltodict
import re
app = Flask(__name__)
produtos = {}
search_result = ['']
search_value = ['']
#qtd_produto = []
#cod_produto = []
#nome_produto = []
#empresa_produto = []
#n_nfe_produto = []

def descriptografar(descriptografar: str):
    from cryptography.fernet import Fernet
    chave = 'FKr2_X4BgKfkg0g48eYbaXxAT0gTm_tG7WyH82N27Vc='
    tradutor = Fernet(chave)
    str_para_descriptografar = descriptografar.encode()
    str_descriptografada = tradutor.decrypt(str_para_descriptografar)
    return str_descriptografada.decode()

def zerar_lista():
    produtos.clear()


def adicionar_todos_os_produtos():
    for k, v in produtos.keys():
        tooltip = f"Empresa {k['empresa_produto']}\nNota N°: {k['n_nfe_produto']}"


def buscar_produtos(padrao):
    from datetime import datetime
        # Converter padrão para minúsculas
    padrao_lower = padrao.lower()

    # Substituir '%' por '.*' para usar expressões regulares
    padrao_regex = padrao_lower.replace('%', '.*')

    # Compilar a expressão regular para busca insensível a maiúsculas/minúsculas
    regex = re.compile(padrao_regex, re.IGNORECASE)

    # Buscar produtos que correspondem ao padrão
    #fazer um for no dict, para ver se algum produto daquele xml está entre os candidatos
    #caso esteja salvar em uma lista temporária, com seus
    print('Tamanhoooooooooo')
    print(len(produtos))
    for k, v in produtos.items():
        lista = v['nome_produto']
        print('Tamanho listaaaaaaaaa')
        print(len(lista))
        print('listaaaaaaaaa')
        print(lista)
        resultados = {}
        nome_produto = []
        qtd_produto = []
        cod_produto = []
        empresa = v['empresa_produto']
        numero_da_nfe = v['n_nfe_produto']
        data_de_emissao = v['data_de_emissao']
        for i, produto in enumerate(lista):
            if regex.search(produto.lower()):
                nome_produto.append(produto)
                qtd_produto.append(v['qtd_produto'][i])
                cod_produto.append(v['cod_produto'][i])
        resultados[k] = {'nome_produto': nome_produto, 'qtd_produto': qtd_produto, 'cod_produto': cod_produto, 'empresa_produto': empresa, 'n_nfe_produto': numero_da_nfe, 'data_de_emissao': data_de_emissao}
    return resultados   
        #for i, possivel_encomenda in enumerate(resultados):
            #pos_info_produto = lista.index(possivel_encomenda)
            #tooltip = 'Empresa {empresa_produto[pos_info_produto]}\nNota N°: {n_nfe_produto[pos_info_produto]}'


def adicionar_encomendas(): #Esses parâmetros não são utilizados, são apenas para que sejam passados para a função buscar_produtos(), pois, teria de fazer uma variável global e defini-la com true ou false, e isso daria muito trabalho
    zerar_lista()
    import requests
    from datetime import datetime
    xml_nfe = ''
    json = {}
    json_original = requests.get(url).json()
    #try: #Para se caso o Json, estiver vazio, significa, que todos os xmls já estão lançados no sistema, logo temos de limpar a tela, para evitar problemas
        #if len(json_original) == 0:
            #redirect('/')
    #except:
        #pass
    #finally:
    for k, v in json_original.items():
        json[f'{descriptografar(k)}'] = f'{descriptografar(v)}'
    for k, v in json.items():
        xml_nfe = xmltodict.parse(v)
        NFe = xml_nfe['nfeProc']['NFe']['infNFe']['det']
        empresa = xml_nfe['nfeProc']['NFe']['infNFe']['emit'][
            'xNome']  # .upper(), Tirei o .upper, pois na nota pode vir diferente
        numero_da_nfe = xml_nfe['nfeProc']['NFe']['infNFe']['ide']['nNF']
        print(f'Nota N°: {numero_da_nfe}\nEmpresa: {empresa}\n')
        print('#' * 100)
        try:
            nome_produto = []
            qtd_produto = []
            cod_produto = []
            for c in range(0, len(NFe)):
                nome_produto.append(NFe[c]['prod']['xProd'])
                qtd_produto.append(NFe[c]['prod']['qCom'])
                cod_produto.append(NFe[c]['prod']['cProd'])
            
                #qtd_produto.append(NFe[c]['prod']['qCom'])
                #cod_produto.append(NFe[c]['prod']['cProd'])
                #nome_produto.append(NFe[c]['prod']['xProd'])
                #empresa_produto.append(empresa)
                #n_nfe_produto.append(numero_da_nfe)
        except:
            nome_produto.append(NFe['prod']['xProd'])
            qtd_produto.append(NFe['prod']['qCom'])
            cod_produto.append(NFe['prod']['cProd'])
            #qtd_produto.append(NFe['prod']['qCom'])
            print('aqui')
            #cod_produto.append(NFe['prod']['cProd'])
            #nome_produto.append(NFe['prod']['xProd'])
            #empresa_produto.append(empresa)
            #n_nfe_produto.append(numero_da_nfe)
        finally:
            data_de_emissao = datetime.fromisoformat(xml_nfe['nfeProc']['NFe']['infNFe']['ide']['dhEmi']).strftime("%d/%m/%Y-%H:%M:%S")
            produtos[k] = {'nome_produto': nome_produto, 'qtd_produto': qtd_produto, 'cod_produto': cod_produto, 'empresa_produto': empresa, 'n_nfe_produto': numero_da_nfe, 'data_de_emissao': data_de_emissao}
            ##buscar_produtos(padrao, lista)
    #print(produtos)



@app.route('/')
def homepage():
    if search_result[0] == '':
        adicionar_encomendas()
        return render_template('index.html', produtos=produtos, search_value=search_value[0])
    else:
        return render_template('index.html', produtos=search_result[0], search_value=search_value[0])

@app.route('/search', methods=['POST'])
def search_produto():
    search = request.form['search']
    search_value[0] = search
    if search == '' or search == '%':
        search_result[0] = ''
    else:
        search_result[0] = buscar_produtos(search)
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Usa a variável de ambiente PORT ou 5000 se não estiver definida
    app.run(host='0.0.0.0', port=port)       # Escuta na porta fornecida
