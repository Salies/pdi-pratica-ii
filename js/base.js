// Funções úteis para construção de interfaces

function $(el) {
    let e = document.querySelectorAll(el);
    if(e.length === 0)
        return null;
    else if(e.length > 1)
        return e;
    return e[0];
}