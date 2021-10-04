console = chrome.extension.getBackgroundPage().console;

let submit = document.getElementById("submit")
let num = document.getElementById("num")

let port = null;

function onReceived(response) {
    alert(response);
}

submit.addEventListener('click', () => {
    //TODO
    port = chrome.runtime.connectNative('com.submit');
    port.onMessage.addListener(onReceived);
    port.postMessage(num.value);
})