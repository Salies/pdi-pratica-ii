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
        console.log(toMatrix(imgData))
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
