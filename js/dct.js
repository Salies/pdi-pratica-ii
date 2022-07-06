// Função alpha para transformada discreta do cosseno
function alpha(u, N) {
    if(u == 0)
        return Math.sqrt(1.0 / N);
    return Math.sqrt(2.0 / N)
}

// Transformada discreta do cosseno
function dct(img) {
    // Considera-se a imagem quadrada (N x N)
    let N = img.length, C = [];

    for(let u = 0; u < N; u++) {
        C[u] = [];
        for(let v = 0; v < N; v++) {
            sum = 0;
            for(let x = 0; x < N; x++) {
                for(let y = 0; y < N; y++) {
                    sum += img[x][y] * Math.cos((((2 * x) + 1) * u * Math.PI) / (2 * N)) * Math.cos((((2 * y) + 1) * v * Math.PI) / (2 * N));
                }
            }
            C[u][v] = alpha(u, N) * alpha(v, N) * sum;
        }
    }

    return C;
}

// Transformada discreta inversa do coseno
function idct(C) {
    let N = C.length, f = [];
    
    for(let x = 0; x < N; x++) {
        f[x] = [];
        for(let y = 0; y < N; y++) {
            sum = 0;
            for(let u = 0; u < N; u++){
                for(let v = 0; v < N; v++) {
                    sum += alpha(u, N) * alpha(v, N) * C[u][v] * Math.cos((((2 * x) + 1) * u * Math.PI) / (2 * N)) * Math.cos((((2 * y) + 1) * v * Math.PI) / (2 * N));
                }
            }
            f[x][y] = Math.round(sum);
        }
    }

    return f;
}

var A = [
    [208, 24, 40, 36, 167],
    [231, 71, 248, 107, 9],
    [32, 140, 245, 234, 217],
    [233, 245, 124, 202, 239],
    [161, 247, 204, 245, 173]
];

var dctA = dct(A);

var Arev = idct(dctA);

console.log(dctA)
console.log(Arev)
console.log(A.toString() === Arev.toString())

