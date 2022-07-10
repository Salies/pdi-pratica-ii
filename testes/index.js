imgInp.onchange = evt => {
    const [file] = imgInp.files
    if (!file)
        return
    let blah = document.createElement("img")
    blah.src = URL.createObjectURL(file)
    blah.onload = function (){
        // Create a Canvas element
        var canvas = document.getElementById("canv");

        // Size the canvas to the element
        canvas.width = 128;
        canvas.height = 128;

        // Draw image onto the canvas
        var ctx = canvas.getContext('2d');
        ctx.drawImage(blah, 0, 0, 128, 128);

        // Finally, get the image data
        // ('data' is an array of RGBA pixel values for each pixel)
        var imgData = ctx.getImageData(0, 0, 128, 128);
        console.log(imgData)
        toGrayscale(imgData)
        ctx.putImageData(imgData, 0, 0);
        let mtx = toMatrix(imgData)
        let arrrr = toArray(mtx)
        console.log(arrrr)
        console.log(arrrr.length)
    }
}

// Converte imagem para cinza
function toGrayscale(img) {
    let data = img.data;
    for (let i = 0; i < data.length; i += 4) {
        const cinza = (data[i] + data[i + 1] + data[i + 2]) / 3;
        data[i] = cinza;
        data[i + 1] = cinza;
        data[i + 2] = cinza;
    }
}

// Converte uma imagem (array) para uma matriz
// Considera que a imagem é cinza!
function toMatrix(img) {
    let data = img.data, out = [], k = 0;
    for(let i = 0; i < img.width; i++) {
        out[i] = []
        for(let j = 0; j < img.height; j++) {
            out[i].push(data[k])
            k += 4
        }
    }
    return out;
}

// Converte uma matriz de trabalho para um array de dados de um canvas
function toArray(matrix) {
    let flat = matrix.flat();
    for(let i = 0; i < flat.length; i += 4)
        flat.splice(i + 1, 0, flat[i], flat[i], 255);
    return Uint8ClampedArray.from(flat);
}