let submit = document.getElementById("submit")
let input = document.getElementById("input")

let port = null;

function onReceived(response) {
    alert(response);
}

submit.addEventListener('click', () => {
    //URL
    if (document.getElementById('url').checked){
        alert("url")
        port = chrome.runtime.connectNative('com.submit');
        port.onMessage.addListener(onReceived);
        port.postMessage(input.value);
    }
    //Text
    else if (document.getElementById('text').checked){
        alert("text")
        port = chrome.runtime.connectNative('com.submittext');
        port.onMessage.addListener(onReceived);
        port.postMessage(input.value);
    }
    else{
        alert("please select either url or text")
    }
})