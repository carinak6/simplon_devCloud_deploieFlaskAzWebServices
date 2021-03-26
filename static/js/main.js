console.log('Hola');
document.querySelector("#envoyer").addEventListener('click', function(){
    console.log();
    document.querySelector("section").appendChild(document.createElement("img").src("static/img/en_charge.gif"));
})