// Ensure that every query has a sessionId

function stringRandom(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }
    return result;
}

function generateSessionId() {
    sessionId = null;
    for (let entry of document.cookie.split(';').map(x => x.trim())) {
        const dict = entry.split('=');
        if (dict[0] == 'sessionId') {
            sessionId = dict[1];
            break;
        }
    }
    if(!sessionId) {
        const newSessionId = stringRandom(32);
        document.cookie = "sessionId=" +  newSessionId;// Update Cookie Property
        sessionId = newSessionId;
    }
    return sessionId;
}

generateSessionId();