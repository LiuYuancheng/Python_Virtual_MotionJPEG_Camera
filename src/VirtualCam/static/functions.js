function clip_text(a_string){
    var input = document.createElement('input');
    input.id="__copyText__";
    input.value = a_string; // OOPS! document.getElementById(divId).innerText;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    var txt = input.value;
    input.remove();
    console.log("OK COPIED: '"+txt+"'");
}

function clip_div(a_string){
    return clip_text(a_string);
    //return clip_text(document.getElementById(divId).innerText)
}