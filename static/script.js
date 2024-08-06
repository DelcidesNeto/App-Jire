var abrir_descricao = [true]

function atribuir_ids(){
    var lista_pai = window.document.querySelector('#produtos')
    lista_descricao_produtos = Array.from(lista_pai.getElementsByClassName('descricao_produto'))
    lista_descricao_produtos.forEach((produto, i) => {
        produto.id = `desc_prod_${i}`;
    });
    var lista_produtos = Array.from(lista_pai.getElementsByClassName('prod'))
    lista_produtos.forEach((produto, i) => {
        produto.onclick = function() {
            mostrar(`desc_prod_${i}`)
        }
    });
}


function alterar_enter_descricao(valor_bool){
    abrir_descricao[0] = valor_bool
        
}

document.addEventListener('DOMContentLoaded', function () {
    atribuir_ids()
    const lista = document.querySelector('#produtos');
    const items = Array.from(lista.getElementsByClassName('prod'));
    let currentIndex = 0;

    function updateSelection(index) {
        items.forEach((item, i) => {
            item.classList.toggle('selected', i === index);
        });
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') {
            currentIndex = (currentIndex + 1) % items.length;
            updateSelection(currentIndex);
        } else if (e.key === 'ArrowUp') {
            currentIndex = (currentIndex - 1 + items.length) % items.length;
            updateSelection(currentIndex);
        }
        else if (e.key === 'Enter'){
            if (abrir_descricao[0] === true){
                mostrar(`desc_prod_${currentIndex}`)
            }
                
        }
    });

    // Inicializa a seleção do primeiro item
    updateSelection(currentIndex);
});


function selecionar(pos_elemento){
    const lista = document.querySelector('#produtos');
    const items = Array.from(lista.getElementsByClassName('prod'));
    items.forEach((item, i) => {
        item.classList.toggle('selected', i === pos_elemento)
    });
}


function mostrar(element){
    var posicao = parseInt(element.replace('desc_prod_', ''), 10)
    selecionar(posicao)
    console.log(`Clicou ${element}`)
    var descricao = window.document.getElementById(element)
    var display_descricao = descricao.style.display
    if (display_descricao == 'block'){
        descricao.style.display = 'none'
    }else{
        descricao.style.display = 'block'
    }
}
