var loadingElementList = document.getElementsByClassName("prompt-loading");
var loadingHiddenElementList = document.getElementsByClassName("prompt-loading-hidden");

function prompt_loading(e) {
    console.log('registered');
    for (let i = 0; i < loadingElementList.length; i++) {
        loadingElementList[i].style.display = 'block';
    };
    for (let i = 0; i < loadingHiddenElementList.length; i++) {
        loadingHiddenElementList[i].style.display = 'none';
    }
}

document.addEventListener("DOMContentLoaded", function (event) {
    promptButton = document.getElementById('prompt-button');
    if (promptButton !== null) {
        promptButton.addEventListener('click', prompt_loading)
    };
    acceptButton = document.getElementById('accept-proposal-button');
    if (acceptButton !== null) {
        acceptButton.addEventListener('click', prompt_loading)
    };
});


