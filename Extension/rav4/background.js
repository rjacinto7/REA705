//console = chrome.extension.getBackgroundPage().console;

function onReceived(response) {
   //alert(response);
   console.log("hello: " + response);
}

port = chrome.runtime.connectNative('com.submit');
port.onMessage.addListener(onReceived);
port.postMessage("ping");
